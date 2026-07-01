"""Shared read model and CNS trace spine for GAIL OS.

This module owns the local, append-only trace events used by operator
surfaces. It deliberately stores references and safe summaries rather than raw
provider payloads, and it does not call external systems.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any, Iterable, Mapping
from uuid import uuid4

from .agent_registry import AgentRegistry
from .action import Action, LocalActionStore
from .approval_actions import ApprovalDecision, ApprovalStore
from .authority_registry import authority_registry_payload
from .connector_registry import ConnectorRegistry
from .evidence_packet import EvidencePacket
from .m365_auth import graph_auth_status_from_env
from .trace_identity import (
    CNS_TRACE_ID_PATTERN,
    create_cns_trace_id,
    ensure_cns_trace_id,
    utc_z_timestamp,
    validate_cns_trace_id,
)


TRACE_EVENT_SCHEMA_VERSION = "rev2.trace-event.v1"
TRACE_READ_MODEL_SCHEMA_VERSION = "rev2.trace-read-model.v1"
SHARED_READ_MODEL_SCHEMA_VERSION = "rev2.shared-read-model.v1"
FREEDOM_RELATIONSHIP_BRIEF_SCHEMA_VERSION = "rev2.freedom-relationship-brief.v1"
FREEDOM_BRIEF_STALE_AFTER_SECONDS = 900

ALLOWED_FREEDOM_BRIEF_TYPES = frozenset(
    {
        "mission_context",
        "approval_request",
        "learning_feedback",
        "risk_warning",
        "similar_case",
    }
)

ALLOWED_TRACE_EVENT_TYPES = frozenset(
    {
        "mission.created",
        "action.validated",
        "authority.override_requested",
        "approval.decided",
        "evidence.recorded",
        "graphify.fact_candidate_prepared",
        "tactile.dry_run_recorded",
    }
)

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


@dataclass(frozen=True)
class TraceEvent:
    """One persisted event in the local CNS trace ledger."""

    event_id: str
    cns_trace_id: str
    event_type: str
    occurred_at: str
    source_system: str
    source_ref: str
    summary: str
    mission_id: str | None = None
    action_id: str | None = None
    evidence_id: str | None = None
    authority_ref: str | None = None
    status: str | None = None
    risk_tier: int | None = None
    idempotency_key: str | None = None
    duplicate_of_event_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def duplicate_detected(self) -> bool:
        return self.duplicate_of_event_id is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": TRACE_EVENT_SCHEMA_VERSION,
            "event_id": self.event_id,
            "cns_trace_id": self.cns_trace_id,
            "event_type": self.event_type,
            "occurred_at": self.occurred_at,
            "source_system": self.source_system,
            "source_ref": self.source_ref,
            "summary": self.summary,
            "mission_id": self.mission_id,
            "action_id": self.action_id,
            "evidence_id": self.evidence_id,
            "authority_ref": self.authority_ref,
            "status": self.status,
            "risk_tier": self.risk_tier,
            "idempotency_key": self.idempotency_key,
            "duplicate_detected": self.duplicate_detected,
            "duplicate_of_event_id": self.duplicate_of_event_id,
            "metadata": _safe_metadata(self.metadata),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "TraceEvent":
        schema_version = str(payload.get("schema_version", TRACE_EVENT_SCHEMA_VERSION))
        if schema_version != TRACE_EVENT_SCHEMA_VERSION:
            raise ValueError("TraceEvent schema_version is not supported.")
        risk_tier = payload.get("risk_tier")
        metadata = payload.get("metadata", {})
        if not isinstance(metadata, Mapping):
            raise ValueError("metadata must be a JSON object.")
        return cls(
            event_id=str(payload["event_id"]),
            cns_trace_id=str(payload["cns_trace_id"]),
            event_type=str(payload["event_type"]),
            occurred_at=str(payload["occurred_at"]),
            source_system=str(payload["source_system"]),
            source_ref=str(payload["source_ref"]),
            summary=str(payload["summary"]),
            mission_id=_optional_text(payload, "mission_id"),
            action_id=_optional_text(payload, "action_id"),
            evidence_id=_optional_text(payload, "evidence_id"),
            authority_ref=_optional_text(payload, "authority_ref"),
            status=_optional_text(payload, "status"),
            risk_tier=int(risk_tier) if risk_tier is not None else None,
            idempotency_key=_optional_text(payload, "idempotency_key"),
            duplicate_of_event_id=_optional_text(payload, "duplicate_of_event_id"),
            metadata=dict(metadata),
        )


class LocalTraceEventStore:
    """Small JSON-backed append-only event store."""

    def __init__(self, base_path: str | Path) -> None:
        self._base_path = Path(base_path)

    @property
    def base_path(self) -> Path:
        return self._base_path

    def path_for(self, event_id: str) -> Path:
        safe_id = event_id.strip()
        if not _safe_prefixed_id(safe_id, "event-"):
            raise ValueError("event_id is not safe for local storage.")
        return self._base_path / f"{safe_id}.json"

    def save(self, event: TraceEvent) -> Path:
        errors = validate_trace_event(event)
        if errors:
            raise ValueError(f"TraceEvent is invalid: {'; '.join(errors)}")
        self._base_path.mkdir(parents=True, exist_ok=True)
        path = self.path_for(event.event_id)
        path.write_text(json.dumps(event.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def read(self, event_id: str) -> TraceEvent:
        return TraceEvent.from_dict(json.loads(self.path_for(event_id).read_text(encoding="utf-8")))

    def list_recent(self, *, limit: int = 25) -> tuple[TraceEvent, ...]:
        events = self._load_all()
        events.sort(key=lambda event: event.occurred_at, reverse=True)
        return tuple(events[:limit])

    def find_by_trace(self, cns_trace_id: str) -> tuple[TraceEvent, ...]:
        _require_valid_cns_trace_id(cns_trace_id)
        events = [event for event in self._load_all() if event.cns_trace_id == cns_trace_id]
        events.sort(key=lambda event: (event.occurred_at, event.duplicate_detected, event.event_id))
        return tuple(events)

    def find_first_by_idempotency_key(self, idempotency_key: str | None) -> TraceEvent | None:
        if not idempotency_key:
            return None
        matches = [event for event in self._load_all() if event.idempotency_key == idempotency_key]
        if not matches:
            return None
        matches.sort(key=lambda event: event.occurred_at)
        return matches[0]

    def _load_all(self) -> list[TraceEvent]:
        if not self._base_path.exists():
            return []
        events: list[TraceEvent] = []
        for path in sorted(self._base_path.glob("event-*.json")):
            try:
                events.append(TraceEvent.from_dict(json.loads(path.read_text(encoding="utf-8"))))
            except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
                continue
        return events


def default_store_root() -> Path:
    return Path(os.environ.get("GAIL_OS_STORE_PATH", "./local_store"))


def default_trace_event_store_path(store_root: str | Path | None = None) -> Path:
    root = Path(store_root) if store_root is not None else default_store_root()
    return root / "trace-events"


def default_evidence_store_path(store_root: str | Path | None = None) -> Path:
    root = Path(store_root) if store_root is not None else default_store_root()
    return root / "evidence"


def default_action_store_path(store_root: str | Path | None = None) -> Path:
    root = Path(store_root) if store_root is not None else default_store_root()
    return root / "actions"


def default_approval_store_path(store_root: str | Path | None = None) -> Path:
    root = Path(store_root) if store_root is not None else default_store_root()
    return root / "approvals"


def create_trace_event(
    *,
    cns_trace_id: str,
    event_type: str,
    source_system: str,
    source_ref: str,
    summary: str,
    occurred_at: str | None = None,
    mission_id: str | None = None,
    action_id: str | None = None,
    evidence_id: str | None = None,
    authority_ref: str | None = None,
    status: str | None = None,
    risk_tier: int | None = None,
    idempotency_key: str | None = None,
    duplicate_of_event_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> TraceEvent:
    event = TraceEvent(
        event_id=f"event-{uuid4().hex[:12]}",
        cns_trace_id=ensure_cns_trace_id(cns_trace_id),
        event_type=event_type,
        occurred_at=occurred_at or utc_z_timestamp(),
        source_system=source_system,
        source_ref=source_ref,
        summary=summary,
        mission_id=mission_id,
        action_id=action_id,
        evidence_id=evidence_id,
        authority_ref=authority_ref,
        status=status,
        risk_tier=risk_tier,
        idempotency_key=idempotency_key,
        duplicate_of_event_id=duplicate_of_event_id,
        metadata=_safe_metadata(metadata or {}),
    )
    errors = validate_trace_event(event)
    if errors:
        raise ValueError("; ".join(errors))
    return event


def validate_trace_event(event: TraceEvent) -> list[str]:
    errors: list[str] = []
    if not _safe_prefixed_id(event.event_id, "event-"):
        errors.append("event_id must use the event- prefix and safe characters.")
    errors.extend(validate_cns_trace_id(event.cns_trace_id, required=True))
    if event.event_type not in ALLOWED_TRACE_EVENT_TYPES:
        errors.append("event_type is outside the approved trace event set.")
    if not _valid_timestamp(event.occurred_at):
        errors.append("occurred_at must be a timezone-aware ISO timestamp.")
    for field_name, value in {
        "source_system": event.source_system,
        "source_ref": event.source_ref,
        "summary": event.summary,
    }.items():
        if not value.strip():
            errors.append(f"{field_name} is required.")
        if _contains_secret_marker(value):
            errors.append(f"{field_name} must not contain secret markers.")
    errors.extend(_validate_optional_prefix("mission_id", event.mission_id, "mission-"))
    errors.extend(_validate_optional_prefix("action_id", event.action_id, "action-"))
    errors.extend(_validate_optional_prefix("evidence_id", event.evidence_id, "evidence-"))
    if event.authority_ref is not None and not (
        _safe_prefixed_id(event.authority_ref, "env-")
        or _safe_prefixed_id(event.authority_ref, "override-")
        or _safe_prefixed_id(event.authority_ref, "aprv-")
    ):
        errors.append("authority_ref must use env-, override-, or aprv- when present.")
    if event.risk_tier is not None and (
        isinstance(event.risk_tier, bool) or not isinstance(event.risk_tier, int) or not 0 <= event.risk_tier <= 5
    ):
        errors.append("risk_tier must be an integer between 0 and 5 when present.")
    if event.idempotency_key is not None and (
        not event.idempotency_key.strip() or _contains_secret_marker(event.idempotency_key)
    ):
        errors.append("idempotency_key must be non-empty and secret-free when present.")
    if event.duplicate_of_event_id is not None and not _safe_prefixed_id(event.duplicate_of_event_id, "event-"):
        errors.append("duplicate_of_event_id must use the event- prefix when present.")
    try:
        _safe_metadata(event.metadata)
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def recent_evidence_refs(
    *,
    limit: int = 25,
    store_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    packets = _load_evidence_packets(store_root=store_root)
    packets.sort(key=lambda packet: packet.created_at, reverse=True)
    return [_evidence_ref(packet) for packet in packets[:limit]]


def evidence_refs_for_mission(
    mission_id: str,
    *,
    store_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    packets = [packet for packet in _load_evidence_packets(store_root=store_root) if packet.mission_id == mission_id]
    packets.sort(key=lambda packet: packet.created_at)
    return [_evidence_ref(packet) for packet in packets]


def evidence_refs_for_trace(
    cns_trace_id: str,
    *,
    store_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    _require_valid_cns_trace_id(cns_trace_id)
    packets = [packet for packet in _load_evidence_packets(store_root=store_root) if packet.cns_trace_id == cns_trace_id]
    packets.sort(key=lambda packet: packet.created_at)
    return [_evidence_ref(packet) for packet in packets]


def action_refs_for_trace(
    cns_trace_id: str,
    *,
    store_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    _require_valid_cns_trace_id(cns_trace_id)
    store = LocalActionStore(default_action_store_path(store_root))
    return [_action_ref(action) for action in store.list_by_trace(cns_trace_id)]


def approval_refs_for_trace(
    cns_trace_id: str,
    *,
    store_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    _require_valid_cns_trace_id(cns_trace_id)
    store = ApprovalStore(default_approval_store_path(store_root))
    return [_approval_ref(decision) for decision in store.list_by_trace(cns_trace_id)]


def mission_refs_for_trace(
    cns_trace_id: str,
    *,
    store_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    _require_valid_cns_trace_id(cns_trace_id)
    root = Path(store_root) if store_root is not None else default_store_root()
    mission_path = root / "missions"
    if not mission_path.exists():
        return []
    refs: list[dict[str, Any]] = []
    for path in sorted(mission_path.glob("mission-*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if payload.get("cns_trace_id") != cns_trace_id:
            continue
        refs.append(
            {
                "mission_id": payload.get("mission_id"),
                "request_id": payload.get("request_id"),
                "domain": payload.get("domain"),
                "status": payload.get("status"),
                "created_at": payload.get("created_at"),
                "data_classification": payload.get("data_classification"),
            }
        )
    return refs


def build_trace_read_model(
    cns_trace_id: str,
    *,
    store_root: str | Path | None = None,
) -> dict[str, Any]:
    _require_valid_cns_trace_id(cns_trace_id)
    root = Path(store_root) if store_root is not None else default_store_root()
    store = LocalTraceEventStore(default_trace_event_store_path(root))
    events = store.find_by_trace(cns_trace_id)
    evidence_refs = evidence_refs_for_trace(cns_trace_id, store_root=root)
    action_refs = action_refs_for_trace(cns_trace_id, store_root=root)
    approval_refs = approval_refs_for_trace(cns_trace_id, store_root=root)
    mission_refs = mission_refs_for_trace(cns_trace_id, store_root=root)
    mission_ids = sorted(
        {
            str(value)
            for value in (
                [event.mission_id for event in events]
                + [ref.get("mission_id") for ref in evidence_refs]
                + [ref.get("mission_id") for ref in action_refs]
                + [ref.get("mission_id") for ref in approval_refs]
                + [ref.get("mission_id") for ref in mission_refs]
            )
            if value
        }
    )
    action_ids = sorted(
        {
            str(value)
            for value in (
                [event.action_id for event in events]
                + [ref.get("action_id") for ref in evidence_refs]
                + [ref.get("action_id") for ref in action_refs]
                + [ref.get("action_id") for ref in approval_refs]
            )
            if value
        }
    )
    evidence_ids = sorted({str(value) for value in [event.evidence_id for event in events] + [ref.get("evidence_id") for ref in evidence_refs] if value})
    authority_refs = sorted(
        {str(event.authority_ref) for event in events if event.authority_ref}
        | {str(ref["decision_id"]) for ref in approval_refs if ref.get("decision_id")}
    )
    return {
        "schema_version": TRACE_READ_MODEL_SCHEMA_VERSION,
        "cns_trace_id": cns_trace_id,
        "found": bool(events or evidence_refs or action_refs or approval_refs or mission_refs),
        "mission_ids": mission_ids,
        "action_ids": action_ids,
        "evidence_ids": evidence_ids,
        "authority_refs": authority_refs,
        "mission_refs": mission_refs,
        "action_refs": action_refs,
        "approval_refs": approval_refs,
        "evidence_refs": evidence_refs,
        "events": [event.to_dict() for event in events],
    }


def build_freedom_relationship_brief(
    cns_trace_id: str,
    *,
    store_root: str | Path | None = None,
    brief_type: str = "mission_context",
    operator_question: str | None = None,
    generated_at: str | None = None,
    stale_after_seconds: int = FREEDOM_BRIEF_STALE_AFTER_SECONDS,
) -> dict[str, Any]:
    """Build the read-only Freedom briefing view over the shared trace model.

    The brief is intentionally non-executing: it summarizes posture and
    references for Freedom/operator reasoning, but it does not approve,
    enqueue, or perform actions.
    """

    _require_valid_cns_trace_id(cns_trace_id)
    if brief_type not in ALLOWED_FREEDOM_BRIEF_TYPES:
        raise ValueError("brief_type is outside the approved Freedom relationship brief set.")
    if stale_after_seconds < 0:
        raise ValueError("stale_after_seconds must be zero or greater.")

    generated = generated_at or utc_z_timestamp()
    trace = build_trace_read_model(cns_trace_id, store_root=store_root)
    events = list(trace["events"])
    mission_refs = list(trace["mission_refs"])
    action_refs = list(trace["action_refs"])
    approval_refs = list(trace["approval_refs"])
    evidence_refs = list(trace["evidence_refs"])
    latest_observed_at = _latest_observed_at(events, mission_refs, action_refs, approval_refs, evidence_refs)
    stale = _is_stale(latest_observed_at, generated, stale_after_seconds) if trace["found"] else False
    data_state = _brief_data_state(found=bool(trace["found"]), stale=stale)
    graph_context_refs = _graph_context_refs_from_events(events)

    return {
        "schema_version": FREEDOM_RELATIONSHIP_BRIEF_SCHEMA_VERSION,
        "generated_at": generated,
        "cns_trace_id": cns_trace_id,
        "found": bool(trace["found"]),
        "data_state": data_state,
        "brief_type": brief_type,
        "operator_question": operator_question or _default_operator_question(data_state),
        "operator_context": _freedom_operator_context(),
        "relationship_map": {
            "mission_ids": trace["mission_ids"],
            "action_ids": trace["action_ids"],
            "evidence_ids": trace["evidence_ids"],
            "authority_refs": trace["authority_refs"],
            "mission_refs": mission_refs,
            "action_refs": action_refs,
            "approval_refs": approval_refs,
            "evidence_refs": evidence_refs,
            "event_refs": _event_refs(events),
        },
        "mission_snapshot": _mission_snapshot(mission_refs),
        "action_snapshot": _action_snapshot(action_refs),
        "approval_snapshot": _approval_snapshot(approval_refs),
        "authority_snapshot": _authority_snapshot(events, trace["authority_refs"]),
        "connector_state": _connector_state_snapshot(),
        "evidence_snapshot": _evidence_snapshot(evidence_refs),
        "event_snapshot": _event_snapshot(events),
        "graph_context_state": "local_fact_candidates" if graph_context_refs else "none_recorded",
        "graph_context_refs": graph_context_refs,
        "options": _freedom_reasoning_options(bool(trace["found"])),
        "confidence": _brief_confidence(bool(trace["found"]), stale),
        "failure_semantics": _brief_failure_semantics(data_state, stale_after_seconds),
        "source_alignment": {
            "trace_endpoint": f"/api/v1/traces/{cns_trace_id}",
            "command_center_read_model": "/api/v1/read-model",
            "source_of_truth": "local GAIL OS trace, mission, and evidence stores",
        },
        "execution_authority": {
            "granted": False,
            "reason": "FreedomRelationshipBrief is a read-only briefing surface, not an execution command.",
            "blocked_capabilities": [
                "live_connector_action",
                "m365_live_read_write_send_or_config",
                "graphify_persistent_ingest",
                "r4_live_execution",
            ],
        },
    }


def _load_evidence_packets(*, store_root: str | Path | None = None) -> list[EvidencePacket]:
    store = default_evidence_store_path(store_root)
    if not store.exists():
        return []
    packets: list[EvidencePacket] = []
    for path in sorted(store.glob("evidence-*.json")):
        try:
            packets.append(EvidencePacket.from_dict(json.loads(path.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            continue
    return packets


def _require_valid_cns_trace_id(cns_trace_id: str) -> None:
    errors = validate_cns_trace_id(cns_trace_id, required=True)
    if errors:
        raise ValueError("; ".join(errors))


def _evidence_ref(packet: EvidencePacket) -> dict[str, Any]:
    return {
        "evidence_id": packet.evidence_id,
        "cns_trace_id": packet.cns_trace_id,
        "mission_id": packet.mission_id,
        "action_id": packet.action_id,
        "result": packet.result,
        "execution_mode": packet.execution_mode,
        "action_type": packet.action_type,
        "created_at": packet.created_at,
        "outcome_summary": packet.outcome_summary,
    }


def _action_ref(action: Action) -> dict[str, Any]:
    return {
        "action_id": action.action_id,
        "cns_trace_id": action.cns_trace_id,
        "mission_id": action.mission_id,
        "action_type": action.action_type,
        "title": action.title,
        "actor": action.actor,
        "status": action.status.value,
        "authority_level": action.authority_level,
        "risk_tier": action.risk_tier,
        "created_at": action.created_at,
        "claimed_at": action.claimed_at,
        "executed_at": action.executed_at,
        "envelope_id": action.envelope_id,
    }


def _approval_ref(decision: ApprovalDecision) -> dict[str, Any]:
    return {
        "decision_id": decision.decision_id,
        "cns_trace_id": decision.cns_trace_id,
        "action_id": decision.action_id,
        "mission_id": decision.mission_id,
        "decision_type": decision.decision_type,
        "decided_by": decision.decided_by,
        "decided_at": decision.decided_at,
        "authority_basis": decision.authority_basis,
        "envelope_id": decision.envelope_id,
        "hold_until": decision.hold_until,
        "info_requested": decision.info_requested,
        "info_from": decision.info_from,
    }


def _freedom_operator_context() -> dict[str, Any]:
    registry = AgentRegistry()
    return {
        "primary_surface": "freedom",
        "supported_surfaces": [
            "freedom",
            "command_center",
            "laptop_browser",
            "tablet_browser",
            "phone_browser_fallback",
        ],
        "freedom_registered": registry.by_id("freedom-executive") is not None,
        "gail_os_role": "CNS mid-brain and brain-stem authority/evidence layer",
        "live_execution_enabled": False,
    }


def _authority_snapshot(events: list[dict[str, Any]], authority_refs: Iterable[str]) -> dict[str, Any]:
    posture = authority_registry_payload()
    refs = sorted({str(ref) for ref in authority_refs if ref})
    return {
        "autonomy_level": posture["autonomy_level"],
        "boundary": posture["boundary"],
        "live_execution_enabled": posture["live_execution_enabled"],
        "r4_requires_authority_envelope": posture["r4_requires_authority_envelope"],
        "r5_human_only": posture["r5_human_only"],
        "authority_refs": refs,
        "authority_ref_state": "referenced" if refs else "none_recorded",
        "highest_observed_risk_tier": _highest_observed_risk_tier(events),
        "stop_conditions": [
            "relationship_brief_is_read_only",
            "freedom_receives_no_hidden_execution_authority",
            "live_connector_actions_remain_owner_gated",
        ],
    }


def _connector_state_snapshot() -> dict[str, Any]:
    registry = ConnectorRegistry()
    report = registry.validate()
    by_state = Counter(profile.current_state for profile in registry.profiles)
    by_family = Counter(profile.system_family for profile in registry.profiles)
    return {
        "registry_valid": report.valid,
        "connector_count": len(registry.profiles),
        "live_access_enabled": any(profile.live_access_enabled for profile in registry.profiles),
        "by_state": dict(sorted(by_state.items())),
        "by_system_family": dict(sorted(by_family.items())),
        "m365": graph_auth_status_from_env(),
    }


def _mission_snapshot(mission_refs: list[dict[str, Any]]) -> dict[str, Any]:
    sorted_refs = _sort_refs_by_timestamp(mission_refs, "created_at")
    status_counts = Counter(str(ref.get("status")) for ref in sorted_refs if ref.get("status"))
    return {
        "mission_count": len(sorted_refs),
        "current_mission_id": sorted_refs[-1].get("mission_id") if sorted_refs else None,
        "by_status": dict(sorted(status_counts.items())),
        "missions": sorted_refs,
    }


def _action_snapshot(action_refs: list[dict[str, Any]]) -> dict[str, Any]:
    sorted_refs = _sort_refs_by_timestamp(action_refs, "created_at")
    status_counts = Counter(str(ref.get("status")) for ref in sorted_refs if ref.get("status"))
    type_counts = Counter(str(ref.get("action_type")) for ref in sorted_refs if ref.get("action_type"))
    return {
        "action_count": len(sorted_refs),
        "current_action_id": sorted_refs[-1].get("action_id") if sorted_refs else None,
        "by_status": dict(sorted(status_counts.items())),
        "by_action_type": dict(sorted(type_counts.items())),
        "actions": sorted_refs,
    }


def _approval_snapshot(approval_refs: list[dict[str, Any]]) -> dict[str, Any]:
    sorted_refs = _sort_refs_by_timestamp(approval_refs, "decided_at")
    decision_counts = Counter(str(ref.get("decision_type")) for ref in sorted_refs if ref.get("decision_type"))
    return {
        "approval_count": len(sorted_refs),
        "latest_decision_at": sorted_refs[-1].get("decided_at") if sorted_refs else None,
        "by_decision_type": dict(sorted(decision_counts.items())),
        "approvals": sorted_refs,
    }


def _evidence_snapshot(evidence_refs: list[dict[str, Any]]) -> dict[str, Any]:
    sorted_refs = _sort_refs_by_timestamp(evidence_refs, "created_at")
    result_counts = Counter(str(ref.get("result")) for ref in sorted_refs if ref.get("result"))
    mode_counts = Counter(str(ref.get("execution_mode")) for ref in sorted_refs if ref.get("execution_mode"))
    return {
        "evidence_count": len(sorted_refs),
        "latest_evidence_at": sorted_refs[-1].get("created_at") if sorted_refs else None,
        "by_result": dict(sorted(result_counts.items())),
        "by_execution_mode": dict(sorted(mode_counts.items())),
        "evidence": sorted_refs,
    }


def _event_snapshot(events: list[dict[str, Any]]) -> dict[str, Any]:
    event_types = Counter(str(event.get("event_type")) for event in events if event.get("event_type"))
    statuses = Counter(str(event.get("status")) for event in events if event.get("status"))
    duplicate_count = sum(1 for event in events if event.get("duplicate_detected") is True)
    return {
        "event_count": len(events),
        "latest_event_at": _latest_timestamp_value(event.get("occurred_at") for event in events),
        "by_event_type": dict(sorted(event_types.items())),
        "by_status": dict(sorted(statuses.items())),
        "duplicate_event_count": duplicate_count,
    }


def _event_refs(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "event_id": event.get("event_id"),
            "event_type": event.get("event_type"),
            "occurred_at": event.get("occurred_at"),
            "source_system": event.get("source_system"),
            "source_ref": event.get("source_ref"),
            "status": event.get("status"),
            "duplicate_detected": event.get("duplicate_detected"),
        }
        for event in events
    ]


def _graph_context_refs_from_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_type") != "graphify.fact_candidate_prepared":
            continue
        metadata = event.get("metadata") if isinstance(event.get("metadata"), Mapping) else {}
        refs.append(
            {
                "event_id": event.get("event_id"),
                "source_ref": event.get("source_ref"),
                "occurred_at": event.get("occurred_at"),
                "status": event.get("status") or "prepared",
                "summary": event.get("summary"),
                "graphify_record_id": metadata.get("graphify_record_id"),
                "authority": "non_authoritative_context_only",
            }
        )
    return refs


def _freedom_reasoning_options(found: bool) -> list[dict[str, str]]:
    if not found:
        return [
            {
                "option_id": "verify_trace_id",
                "label": "Verify trace ID",
                "authority": "read_only",
            },
            {
                "option_id": "request_recent_posture",
                "label": "Ask GAIL OS for recent posture",
                "authority": "read_only",
            },
        ]
    return [
        {
            "option_id": "summarize_trace",
            "label": "Summarize trace posture and evidence",
            "authority": "read_only",
        },
        {
            "option_id": "ask_owner_next_boundary",
            "label": "Ask Adam for the next governed action boundary",
            "authority": "human_decision_required",
        },
    ]


def _brief_confidence(found: bool, stale: bool) -> dict[str, str]:
    if not found:
        return {
            "level": "low",
            "basis": "No local mission, event, or evidence refs were found for this cns_trace_id.",
        }
    if stale:
        return {
            "level": "medium",
            "basis": "Local records exist, but the freshest observed record is outside the freshness window.",
        }
    return {
        "level": "high",
        "basis": "Brief is grounded in local GAIL OS trace, mission, and evidence records.",
    }


def _brief_failure_semantics(data_state: str, stale_after_seconds: int) -> dict[str, Any]:
    retry_recommended = data_state in {"not_found", "stale"}
    return {
        "data_state": data_state,
        "not_found": {
            "http_status": 200,
            "found": False,
            "meaning": "The trace ID is valid, but no local records currently reference it.",
        },
        "invalid_trace_id": {
            "http_status": 422,
            "meaning": "The trace ID failed the cns-YYYYMMDD-12safechars contract.",
        },
        "unauthorized": {
            "http_status": 401,
            "meaning": "The caller did not present the configured GAIL OS API key.",
        },
        "unavailable": {
            "meaning": "If GAIL OS or its local store cannot be reached, Freedom should report a degraded posture and retry later.",
        },
        "stale": {
            "current": data_state == "stale",
            "stale_after_seconds": stale_after_seconds,
            "meaning": "The brief remains readable, but Freedom should label it stale before advising next steps.",
        },
        "retry": {
            "recommended": retry_recommended,
            "after_seconds": 30 if data_state == "not_found" else 120 if data_state == "stale" else None,
        },
    }


def _default_operator_question(data_state: str) -> str:
    if data_state == "not_found":
        return "No local records were found for this trace. Should Freedom verify the trace ID or ask for current posture?"
    if data_state == "stale":
        return "This trace has local records, but they may be stale. What should Adam verify before the next step?"
    return "What should Adam or Freedom understand before the next governed step?"


def _brief_data_state(*, found: bool, stale: bool) -> str:
    if not found:
        return "not_found"
    if stale:
        return "stale"
    return "ready"


def _highest_observed_risk_tier(events: list[dict[str, Any]]) -> int | None:
    tiers = [
        int(event["risk_tier"])
        for event in events
        if isinstance(event.get("risk_tier"), int) and not isinstance(event.get("risk_tier"), bool)
    ]
    return max(tiers) if tiers else None


def _latest_observed_at(
    events: list[dict[str, Any]],
    mission_refs: list[dict[str, Any]],
    action_refs: list[dict[str, Any]],
    approval_refs: list[dict[str, Any]],
    evidence_refs: list[dict[str, Any]],
) -> str | None:
    values = [event.get("occurred_at") for event in events]
    values.extend(ref.get("created_at") for ref in mission_refs)
    values.extend(ref.get("created_at") for ref in action_refs)
    values.extend(ref.get("decided_at") for ref in approval_refs)
    values.extend(ref.get("created_at") for ref in evidence_refs)
    return _latest_timestamp_value(values)


def _latest_timestamp_value(values: Iterable[Any]) -> str | None:
    parsed: list[datetime] = []
    for value in values:
        if not isinstance(value, str):
            continue
        try:
            parsed.append(_parse_utc_timestamp(value))
        except ValueError:
            continue
    if not parsed:
        return None
    return utc_z_timestamp(max(parsed))


def _is_stale(latest_observed_at: str | None, generated_at: str, stale_after_seconds: int) -> bool:
    if latest_observed_at is None:
        return True
    try:
        latest = _parse_utc_timestamp(latest_observed_at)
        generated = _parse_utc_timestamp(generated_at)
    except ValueError:
        return True
    return (generated - latest).total_seconds() > stale_after_seconds


def _sort_refs_by_timestamp(refs: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    return sorted(refs, key=lambda ref: _timestamp_sort_key(ref.get(key)))


def _timestamp_sort_key(value: Any) -> datetime:
    if not isinstance(value, str):
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        return _parse_utc_timestamp(value)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def _parse_utc_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _safe_metadata(metadata: Mapping[str, Any]) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    for key, value in metadata.items():
        key_text = str(key).strip()
        if not key_text:
            raise ValueError("metadata keys must be non-empty.")
        if _contains_secret_marker(key_text):
            raise ValueError("metadata keys must not contain secret markers.")
        safe[key_text] = _safe_metadata_value(value)
    return safe


def _safe_metadata_value(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        if _contains_secret_marker(value):
            return "[redacted-sensitive-marker]"
        return value[:500]
    if isinstance(value, Mapping):
        return _safe_metadata(value)
    if isinstance(value, (list, tuple)):
        return [_safe_metadata_value(item) for item in value[:20]]
    return str(value)[:500]


def _optional_text(payload: Mapping[str, Any], key: str) -> str | None:
    value = payload.get(key)
    if value is None:
        return None
    return str(value)


def _valid_timestamp(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _validate_optional_prefix(field_name: str, value: str | None, prefix: str) -> list[str]:
    if value is None:
        return []
    if not _safe_prefixed_id(value, prefix):
        return [f"{field_name} must use the {prefix} prefix when present."]
    return []


def _safe_prefixed_id(value: str, prefix: str) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.strip()
    if not normalized.startswith(prefix):
        return False
    if any(part in normalized for part in ("/", "\\", "..")):
        return False
    return all(character.isalnum() or character in {"-", "_"} for character in normalized)


def _contains_secret_marker(value: str) -> bool:
    lowered = value.lower()
    return any(marker in lowered for marker in _SECRET_TEXT_MARKERS)


__all__ = [
    "ALLOWED_TRACE_EVENT_TYPES",
    "ALLOWED_FREEDOM_BRIEF_TYPES",
    "CNS_TRACE_ID_PATTERN",
    "FREEDOM_BRIEF_STALE_AFTER_SECONDS",
    "FREEDOM_RELATIONSHIP_BRIEF_SCHEMA_VERSION",
    "SHARED_READ_MODEL_SCHEMA_VERSION",
    "TRACE_EVENT_SCHEMA_VERSION",
    "TRACE_READ_MODEL_SCHEMA_VERSION",
    "LocalTraceEventStore",
    "TraceEvent",
    "action_refs_for_trace",
    "approval_refs_for_trace",
    "build_freedom_relationship_brief",
    "build_trace_read_model",
    "create_cns_trace_id",
    "create_trace_event",
    "default_action_store_path",
    "default_approval_store_path",
    "default_evidence_store_path",
    "default_store_root",
    "default_trace_event_store_path",
    "ensure_cns_trace_id",
    "evidence_refs_for_mission",
    "evidence_refs_for_trace",
    "mission_refs_for_trace",
    "recent_evidence_refs",
    "utc_z_timestamp",
    "validate_cns_trace_id",
    "validate_trace_event",
]
