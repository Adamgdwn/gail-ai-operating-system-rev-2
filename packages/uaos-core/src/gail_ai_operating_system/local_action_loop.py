"""Governed local action request and decision orchestration.

This module is transport-independent. It owns the vertical local path from an
approved mission to a persisted local action request, approval decision,
evidence packet, and trace events. It never calls live connectors.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .action import Action, LocalActionStore, create_action, transition_action
from .approval_actions import (
    ApprovalDecision,
    ApprovalDecisionType,
    ApprovalError,
    ApprovalStore,
    approve_action,
    hold_action,
    reject_action,
    request_more_info,
)
from .evidence_packet import EvidencePacket, EvidenceResult, ExecutionMode, create_evidence_packet
from .evidence_store import load_evidence_packet, save_evidence_packet
from .mission import MissionStatus
from .mission_spine import MissionAction, MissionEnvelope, PermissionGate, PolicyDecision
from .read_model import LocalTraceEventStore, TraceEvent, create_trace_event, utc_z_timestamp
from .trace_identity import ensure_cns_trace_id


LOCAL_ACTION_REQUEST_SCHEMA_VERSION = "rev2.local-action-request.v1"
LOCAL_ACTION_DECISION_SCHEMA_VERSION = "rev2.local-action-decision.v1"
LOCAL_ACTION_ALLOWED_AUTHORITY_LEVELS = frozenset({"R0", "R1"})

_SECRET_TEXT_MARKERS = (
    "access_token=",
    "api_key=",
    "authorization:",
    "bearer ",
    "client_secret=",
    "password=",
    "private key",
    "refresh_token=",
    "secret=",
    "token:",
)


class LocalActionLoopError(ValueError):
    """Base class for governed local action loop failures."""


class LocalActionNotFoundError(LocalActionLoopError):
    """Raised when a referenced local action, mission, or duplicate record is absent."""


class LocalActionConflictError(LocalActionLoopError):
    """Raised when a local action write would conflict with current state."""


class LocalActionPolicyBlockedError(LocalActionLoopError):
    """Raised when the local policy gate denies a requested action."""

    def __init__(self, decision: PolicyDecision) -> None:
        self.decision = decision
        super().__init__(decision.stop_reason or decision.reason)


def create_local_action_request(
    *,
    mission: MissionEnvelope,
    action_type: str,
    title: str,
    actor: str,
    idempotency_key: str,
    action_store: LocalActionStore,
    trace_event_store: LocalTraceEventStore,
    authority_level: str = "R1",
    risk_tier: int = 1,
    arguments: Mapping[str, Any] | None = None,
    envelope_id: str | None = None,
    cns_trace_id: str | None = None,
) -> dict[str, Any]:
    """Create a persisted local action in approval_requested state."""

    _validate_idempotency_key(idempotency_key)
    trace_id = _resolve_trace_id(mission.cns_trace_id, cns_trace_id)
    trace_key = f"local-action-request:{mission.mission_id}:{idempotency_key}"
    duplicate = trace_event_store.find_first_by_idempotency_key(trace_key)
    if duplicate is not None:
        return _duplicate_action_request_payload(
            duplicate,
            action_store=action_store,
        )

    if authority_level not in LOCAL_ACTION_ALLOWED_AUTHORITY_LEVELS:
        raise LocalActionConflictError("GLW-1 local action requests are limited to R0/R1 authority.")

    action = create_action(
        mission_id=mission.mission_id,
        action_type=action_type,
        title=title,
        actor=actor,
        authority_level=authority_level,
        risk_tier=risk_tier,
        arguments=arguments or {},
        envelope_id=envelope_id,
        cns_trace_id=trace_id,
    )
    proposal = MissionAction(
        action_id=action.action_id,
        action_type=action.action_type,
        title=action.title,
        arguments=action.arguments,
        risk_tier=action.risk_tier,
    )
    policy_decision = PermissionGate().evaluate(mission, proposal)
    if not policy_decision.allowed:
        event = _save_trace_event(
            trace_event_store,
            cns_trace_id=trace_id,
            event_type="action.validated",
            source_ref=f"api/v1/actions/local/{action.action_id}",
            summary="Local action request blocked by the GAIL OS policy gate.",
            mission_id=mission.mission_id,
            action_id=action.action_id,
            status="blocked",
            risk_tier=action.risk_tier,
            idempotency_key=trace_key,
            metadata={
                "policy_decision": _policy_decision_payload(policy_decision),
                "action_type": action.action_type,
                "authority_level": action.authority_level,
                "target_action_executed": False,
            },
        )
        raise LocalActionPolicyBlockedError(policy_decision)

    pending_action = _advance_to_approval_requested(action)
    action_store.save(pending_action)
    event = _save_trace_event(
        trace_event_store,
        cns_trace_id=trace_id,
        event_type="action.validated",
        source_ref=f"api/v1/actions/local/{pending_action.action_id}",
        summary="Local action request persisted and placed in approval_requested state.",
        mission_id=mission.mission_id,
        action_id=pending_action.action_id,
        status=pending_action.status.value,
        risk_tier=pending_action.risk_tier,
        idempotency_key=trace_key,
        metadata={
            "policy_decision": _policy_decision_payload(policy_decision),
            "action_type": pending_action.action_type,
            "authority_level": pending_action.authority_level,
            "target_action_executed": False,
        },
    )
    return _action_request_payload(
        action=pending_action,
        policy_decision=policy_decision,
        trace_event=event,
        duplicate_detected=False,
    )


def record_local_action_decision(
    *,
    action_id: str,
    decision_type: str,
    decided_by: str,
    rationale: str,
    authority_basis: str,
    idempotency_key: str,
    action_store: LocalActionStore,
    approval_store: ApprovalStore,
    evidence_store_path: str | Path,
    trace_event_store: LocalTraceEventStore,
    expected_status: str = MissionStatus.APPROVAL_REQUESTED.value,
    decided_at: str | None = None,
    hold_until: str | None = None,
    info_requested: str | None = None,
    info_from: str | None = None,
    envelope_id: str | None = None,
    cns_trace_id: str | None = None,
) -> dict[str, Any]:
    """Record a local approval decision, evidence, and trace events for an action."""

    _validate_idempotency_key(idempotency_key)
    trace_key = f"local-action-decision:{action_id}:{idempotency_key}"
    duplicate = trace_event_store.find_first_by_idempotency_key(trace_key)
    if duplicate is not None:
        return _duplicate_action_decision_payload(
            duplicate,
            action_store=action_store,
            approval_store=approval_store,
            evidence_store_path=Path(evidence_store_path),
        )

    try:
        action = action_store.load(action_id)
    except (OSError, KeyError, ValueError, FileNotFoundError) as exc:
        raise LocalActionNotFoundError(f"Local action {action_id!r} was not found.") from exc

    trace_id = _resolve_trace_id(action.cns_trace_id, cns_trace_id)
    expected = _mission_status_from_text(expected_status)
    if action.status != expected:
        raise LocalActionConflictError(
            f"Action {action.action_id!r} is in state {action.status.value!r}; "
            f"expected {expected.value!r}."
        )
    if action.status != MissionStatus.APPROVAL_REQUESTED:
        raise LocalActionConflictError("Local approval decisions require approval_requested state.")

    decided_timestamp = decided_at or utc_z_timestamp()
    updated_action, decision = _apply_decision(
        action,
        decision_type=decision_type,
        decided_by=decided_by,
        rationale=rationale,
        authority_basis=authority_basis,
        decided_at=decided_timestamp,
        hold_until=hold_until,
        info_requested=info_requested,
        info_from=info_from,
        envelope_id=envelope_id,
        cns_trace_id=trace_id,
    )
    action_store.save(updated_action)
    approval_store.write(decision)
    evidence = _create_decision_evidence(updated_action, decision)
    save_evidence_packet(evidence, store_path=Path(evidence_store_path))

    decision_event = _save_trace_event(
        trace_event_store,
        cns_trace_id=trace_id,
        event_type="approval.decided",
        source_ref=f"api/v1/actions/local/{action.action_id}/decisions/{decision.decision_id}",
        summary="Local approval decision recorded without executing the target action.",
        mission_id=action.mission_id,
        action_id=action.action_id,
        authority_ref=decision.decision_id,
        status=decision.decision_type,
        risk_tier=action.risk_tier,
        idempotency_key=trace_key,
        metadata={
            "decision_id": decision.decision_id,
            "decision_type": decision.decision_type,
            "evidence_id": evidence.evidence_id,
            "target_action_status": updated_action.status.value,
            "target_action_executed": False,
            "execution_mode": ExecutionMode.DRY_RUN.value,
        },
    )
    evidence_event = _save_trace_event(
        trace_event_store,
        cns_trace_id=trace_id,
        event_type="evidence.recorded",
        source_ref=f"api/v1/evidence/{evidence.evidence_id}",
        summary="Evidence packet recorded for the local approval decision.",
        mission_id=action.mission_id,
        action_id=action.action_id,
        evidence_id=evidence.evidence_id,
        authority_ref=decision.decision_id,
        status=evidence.result,
        risk_tier=action.risk_tier,
        idempotency_key=f"local-action-decision-evidence:{evidence.evidence_id}",
        metadata={
            "decision_id": decision.decision_id,
            "decision_type": decision.decision_type,
            "target_action_executed": False,
            "execution_mode": evidence.execution_mode,
        },
    )
    return _action_decision_payload(
        action=updated_action,
        decision=decision,
        evidence=evidence,
        trace_events=(decision_event, evidence_event),
        duplicate_detected=False,
    )


def _advance_to_approval_requested(action: Action) -> Action:
    for status in (MissionStatus.PROPOSED, MissionStatus.CLASSIFIED, MissionStatus.APPROVAL_REQUESTED):
        action = transition_action(action, status)
    return action


def _apply_decision(
    action: Action,
    *,
    decision_type: str,
    decided_by: str,
    rationale: str,
    authority_basis: str,
    decided_at: str,
    hold_until: str | None,
    info_requested: str | None,
    info_from: str | None,
    envelope_id: str | None,
    cns_trace_id: str,
) -> tuple[Action, ApprovalDecision]:
    try:
        normalized = ApprovalDecisionType(decision_type)
    except ValueError as exc:
        raise LocalActionLoopError("decision_type is outside the approved local decision set.") from exc

    try:
        if normalized == ApprovalDecisionType.APPROVED:
            return approve_action(
                action,
                approver=decided_by,
                rationale=rationale,
                authority_basis=authority_basis,
                decided_at=decided_at,
                envelope_id=envelope_id,
                cns_trace_id=cns_trace_id,
            )
        if normalized == ApprovalDecisionType.REJECTED:
            return reject_action(
                action,
                rejecter=decided_by,
                rationale=rationale,
                authority_basis=authority_basis,
                decided_at=decided_at,
                envelope_id=envelope_id,
                cns_trace_id=cns_trace_id,
            )
        if normalized == ApprovalDecisionType.HELD:
            return hold_action(
                action,
                holder=decided_by,
                rationale=rationale,
                authority_basis=authority_basis,
                decided_at=decided_at,
                hold_until=hold_until,
                envelope_id=envelope_id,
                cns_trace_id=cns_trace_id,
            )
        return request_more_info(
            action,
            requester=decided_by,
            info_requested=info_requested or "",
            info_from=info_from or "",
            rationale=rationale,
            authority_basis=authority_basis,
            decided_at=decided_at,
            envelope_id=envelope_id,
            cns_trace_id=cns_trace_id,
        )
    except ApprovalError as exc:
        raise LocalActionConflictError(str(exc)) from exc


def _create_decision_evidence(action: Action, decision: ApprovalDecision) -> EvidencePacket:
    result = (
        EvidenceResult.STOPPED.value
        if decision.decision_type == ApprovalDecisionType.REJECTED.value
        else EvidenceResult.SUCCESS.value
    )
    return create_evidence_packet(
        mission_id=action.mission_id,
        action_id=action.action_id,
        actor=decision.decided_by,
        action_type="local_approval_decision",
        authority_basis=decision.authority_basis,
        result=result,
        execution_mode=ExecutionMode.DRY_RUN.value,
        created_at=decision.decided_at,
        envelope_id=decision.envelope_id,
        rollback_note=(
            "Decision records are append-only. Recovery is a new governed action "
            "request or a later approved state-correction chunk."
        ),
        outcome_summary=(
            f"Recorded {decision.decision_type} local approval decision "
            f"{decision.decision_id} for {action.action_id}; target action was not executed."
        ),
        cns_trace_id=decision.cns_trace_id,
    )


def _save_trace_event(
    store: LocalTraceEventStore,
    **kwargs: Any,
) -> TraceEvent:
    kwargs.setdefault("source_system", "gail-os-local-action-loop")
    event = create_trace_event(**kwargs)
    store.save(event)
    return event


def _duplicate_action_request_payload(
    duplicate: TraceEvent,
    *,
    action_store: LocalActionStore,
) -> dict[str, Any]:
    action_id = _metadata_text(duplicate.metadata, "action_id") or duplicate.action_id
    if not action_id:
        raise LocalActionConflictError("Duplicate local action request did not record an action_id.")
    try:
        action = action_store.load(action_id)
    except (OSError, KeyError, ValueError, FileNotFoundError) as exc:
        raise LocalActionNotFoundError("Duplicate local action request references a missing action.") from exc
    policy_payload = duplicate.metadata.get("policy_decision")
    policy_decision = _policy_decision_from_payload(policy_payload, action_id=action.action_id)
    return _action_request_payload(
        action=action,
        policy_decision=policy_decision,
        trace_event=duplicate,
        duplicate_detected=True,
    )


def _duplicate_action_decision_payload(
    duplicate: TraceEvent,
    *,
    action_store: LocalActionStore,
    approval_store: ApprovalStore,
    evidence_store_path: Path,
) -> dict[str, Any]:
    action_id = duplicate.action_id
    decision_id = _metadata_text(duplicate.metadata, "decision_id") or duplicate.authority_ref
    evidence_id = _metadata_text(duplicate.metadata, "evidence_id")
    if not action_id or not decision_id or not evidence_id:
        raise LocalActionConflictError("Duplicate local action decision is missing action, decision, or evidence refs.")
    try:
        action = action_store.load(action_id)
        decision = approval_store.read(decision_id)
        evidence = load_evidence_packet(evidence_id, store_path=evidence_store_path)
    except (OSError, KeyError, ValueError, FileNotFoundError) as exc:
        raise LocalActionNotFoundError("Duplicate local action decision references missing local records.") from exc
    return _action_decision_payload(
        action=action,
        decision=decision,
        evidence=evidence,
        trace_events=(duplicate,),
        duplicate_detected=True,
    )


def _action_request_payload(
    *,
    action: Action,
    policy_decision: PolicyDecision,
    trace_event: TraceEvent,
    duplicate_detected: bool,
) -> dict[str, Any]:
    return {
        "schema_version": LOCAL_ACTION_REQUEST_SCHEMA_VERSION,
        "cns_trace_id": action.cns_trace_id,
        "duplicate_detected": duplicate_detected,
        "action": action.to_dict(),
        "policy_decision": _policy_decision_payload(policy_decision),
        "trace_event": trace_event.to_dict(),
        "write_state": {
            "persisted": True,
            "stores": ["actions", "trace-events"],
            "target_action_executed": False,
        },
        "execution_authority": _no_execution_authority(),
    }


def _action_decision_payload(
    *,
    action: Action,
    decision: ApprovalDecision,
    evidence: EvidencePacket,
    trace_events: tuple[TraceEvent, ...],
    duplicate_detected: bool,
) -> dict[str, Any]:
    return {
        "schema_version": LOCAL_ACTION_DECISION_SCHEMA_VERSION,
        "cns_trace_id": action.cns_trace_id,
        "duplicate_detected": duplicate_detected,
        "action": action.to_dict(),
        "decision": decision.to_dict(),
        "evidence": evidence.to_dict(),
        "trace_events": [event.to_dict() for event in trace_events],
        "write_state": {
            "persisted": True,
            "stores": ["actions", "approvals", "evidence", "trace-events"],
            "target_action_executed": False,
        },
        "execution_authority": _no_execution_authority(),
    }


def _policy_decision_payload(decision: PolicyDecision) -> dict[str, Any]:
    return {
        "action_id": decision.action_id,
        "allowed": decision.allowed,
        "mode": decision.mode,
        "reason": decision.reason,
        "stop_reason": decision.stop_reason,
    }


def _policy_decision_from_payload(payload: Any, *, action_id: str) -> PolicyDecision:
    if not isinstance(payload, Mapping):
        return PolicyDecision(
            action_id=action_id,
            allowed=True,
            mode="dry-run",
            reason="Duplicate request references an existing persisted local action.",
            stop_reason=None,
        )
    return PolicyDecision(
        action_id=str(payload.get("action_id") or action_id),
        allowed=bool(payload.get("allowed", True)),
        mode=str(payload.get("mode") or "dry-run"),
        reason=str(payload.get("reason") or "Duplicate request references an existing persisted local action."),
        stop_reason=str(payload["stop_reason"]) if payload.get("stop_reason") is not None else None,
    )


def _no_execution_authority() -> dict[str, Any]:
    return {
        "granted": False,
        "target_action_executed": False,
        "live_connector_action": False,
        "reason": "GLW-1 records local governed action state and evidence only; it does not execute connectors.",
        "blocked_capabilities": [
            "m365_live_read_write_send_or_config",
            "graphify_persistent_ingest",
            "r4_live_execution",
            "external_system_mutation",
        ],
    }


def _resolve_trace_id(existing_trace_id: str | None, requested_trace_id: str | None) -> str:
    trace_id = ensure_cns_trace_id(requested_trace_id or existing_trace_id)
    if existing_trace_id and requested_trace_id and trace_id != existing_trace_id:
        raise LocalActionConflictError("Requested cns_trace_id does not match the existing local record trace.")
    return trace_id


def _mission_status_from_text(value: str) -> MissionStatus:
    try:
        return MissionStatus(value)
    except ValueError as exc:
        raise LocalActionLoopError("expected_status is outside the action state machine.") from exc


def _validate_idempotency_key(value: str) -> None:
    cleaned = value.strip()
    if not cleaned:
        raise LocalActionLoopError("idempotency_key is required.")
    if any(part in cleaned for part in ("/", "\\", "..")):
        raise LocalActionLoopError("idempotency_key must not contain path separators.")
    lowered = cleaned.lower()
    if any(marker in lowered for marker in _SECRET_TEXT_MARKERS):
        raise LocalActionLoopError("idempotency_key must not contain secret markers.")


def _metadata_text(metadata: Mapping[str, Any], key: str) -> str | None:
    value = metadata.get(key)
    if value is None:
        return None
    return str(value)


__all__ = [
    "LOCAL_ACTION_ALLOWED_AUTHORITY_LEVELS",
    "LOCAL_ACTION_DECISION_SCHEMA_VERSION",
    "LOCAL_ACTION_REQUEST_SCHEMA_VERSION",
    "LocalActionConflictError",
    "LocalActionLoopError",
    "LocalActionNotFoundError",
    "LocalActionPolicyBlockedError",
    "create_local_action_request",
    "record_local_action_decision",
]
