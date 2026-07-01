"""Local approval service functions for GAIL AI Operating System Rev 2.

Transport-independent. No FastAPI import. No HTTP dependency. No live connectors.
All decision logic is pure; disk I/O is in ApprovalStore. A1 local boundary.

Four governed approval actions:
  approve_action        — APPROVAL_REQUESTED → APPROVED
  reject_action         — APPROVAL_REQUESTED → REJECTED (terminal)
  hold_action           — stays at APPROVAL_REQUESTED, writes hold record
  request_more_info     — stays at APPROVAL_REQUESTED, writes info-request record
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4

from .action import Action, transition_action
from .mission import MissionStatus
from .trace_identity import ensure_cns_trace_id, validate_cns_trace_id


class ApprovalDecisionType(str, Enum):
    """Classification of a local approval action."""

    APPROVED = "approved"
    REJECTED = "rejected"
    HELD = "held"
    MORE_INFO_REQUESTED = "more_info_requested"


class ApprovalError(ValueError):
    """Raised when an approval action cannot be performed on the given action."""


_APPROVAL_REQUIRED_STATE = MissionStatus.APPROVAL_REQUESTED


@dataclass(frozen=True)
class ApprovalDecision:
    """Governed local record of an approval decision or administrative annotation.

    decision_id must use the 'aprv-' prefix.
    APPROVED/REJECTED decisions accompany a state machine transition.
    HELD/MORE_INFO_REQUESTED decisions leave the action at APPROVAL_REQUESTED.
    """

    decision_id: str
    action_id: str
    mission_id: str
    decision_type: str
    decided_by: str
    decided_at: str
    rationale: str
    authority_basis: str
    envelope_id: str | None
    hold_until: str | None
    info_requested: str | None
    info_from: str | None
    cns_trace_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "cns_trace_id": self.cns_trace_id,
            "action_id": self.action_id,
            "mission_id": self.mission_id,
            "decision_type": self.decision_type,
            "decided_by": self.decided_by,
            "decided_at": self.decided_at,
            "rationale": self.rationale,
            "authority_basis": self.authority_basis,
            "envelope_id": self.envelope_id,
            "hold_until": self.hold_until,
            "info_requested": self.info_requested,
            "info_from": self.info_from,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ApprovalDecision":
        return cls(
            decision_id=str(payload["decision_id"]),
            action_id=str(payload["action_id"]),
            mission_id=str(payload["mission_id"]),
            decision_type=str(payload["decision_type"]),
            decided_by=str(payload["decided_by"]),
            decided_at=str(payload["decided_at"]),
            rationale=str(payload["rationale"]),
            authority_basis=str(payload["authority_basis"]),
            envelope_id=str(payload["envelope_id"]) if payload.get("envelope_id") is not None else None,
            hold_until=str(payload["hold_until"]) if payload.get("hold_until") is not None else None,
            info_requested=str(payload["info_requested"]) if payload.get("info_requested") is not None else None,
            info_from=str(payload["info_from"]) if payload.get("info_from") is not None else None,
            cns_trace_id=str(payload["cns_trace_id"]) if payload.get("cns_trace_id") else None,
        )


def validate_approval_decision(decision: ApprovalDecision) -> list[str]:
    """Return validation errors for an ApprovalDecision (empty list = valid)."""
    errors: list[str] = []
    if not decision.decision_id.startswith("aprv-"):
        errors.append("decision_id must use the aprv- prefix.")
    if not decision.action_id.startswith("action-"):
        errors.append("action_id must use the action- prefix.")
    if not decision.mission_id.startswith("mission-"):
        errors.append("mission_id must use the mission- prefix.")
    try:
        ApprovalDecisionType(decision.decision_type)
    except ValueError:
        errors.append(f"decision_type must be one of {[t.value for t in ApprovalDecisionType]}.")
    if not decision.decided_by.strip():
        errors.append("decided_by is required.")
    if not decision.decided_at.strip():
        errors.append("decided_at is required.")
    if not decision.rationale.strip():
        errors.append("rationale is required.")
    if not decision.authority_basis.strip():
        errors.append("authority_basis is required.")
    if decision.envelope_id is not None and not decision.envelope_id.startswith("env-"):
        errors.append("envelope_id must use the env- prefix when present.")
    errors.extend(validate_cns_trace_id(decision.cns_trace_id))
    if decision.decision_type == ApprovalDecisionType.MORE_INFO_REQUESTED.value:
        if not decision.info_requested or not decision.info_requested.strip():
            errors.append("info_requested is required for more_info_requested decisions.")
        if not decision.info_from or not decision.info_from.strip():
            errors.append("info_from is required for more_info_requested decisions.")
    return errors


def _require_approval_requested(action: Action) -> None:
    if action.status != _APPROVAL_REQUIRED_STATE:
        raise ApprovalError(
            f"Action {action.action_id!r} is in state {action.status.value!r}; "
            f"approval actions require {_APPROVAL_REQUIRED_STATE.value!r} state."
        )


def _new_decision_id() -> str:
    return f"aprv-{uuid4().hex[:12]}"


def approve_action(
    action: Action,
    *,
    approver: str,
    rationale: str,
    authority_basis: str,
    decided_at: str,
    envelope_id: str | None = None,
    cns_trace_id: str | None = None,
) -> tuple[Action, ApprovalDecision]:
    """Approve an action in APPROVAL_REQUESTED state.

    Transitions action to APPROVED and produces a governed ApprovalDecision record.
    Returns (approved_action, decision). Both must be persisted by the caller.
    R5 actions are blocked by the state machine in transition_action.
    """
    _require_approval_requested(action)
    if not approver.strip():
        raise ApprovalError("approver is required.")
    if not rationale.strip():
        raise ApprovalError("rationale is required.")
    if not authority_basis.strip():
        raise ApprovalError("authority_basis is required.")

    approved_action = transition_action(action, MissionStatus.APPROVED)
    decision = ApprovalDecision(
        decision_id=_new_decision_id(),
        action_id=action.action_id,
        mission_id=action.mission_id,
        decision_type=ApprovalDecisionType.APPROVED.value,
        decided_by=approver,
        decided_at=decided_at,
        rationale=rationale,
        authority_basis=authority_basis,
        envelope_id=envelope_id,
        hold_until=None,
        info_requested=None,
        info_from=None,
        cns_trace_id=ensure_cns_trace_id(cns_trace_id or action.cns_trace_id),
    )
    return approved_action, decision


def reject_action(
    action: Action,
    *,
    rejecter: str,
    rationale: str,
    authority_basis: str,
    decided_at: str,
    envelope_id: str | None = None,
    cns_trace_id: str | None = None,
) -> tuple[Action, ApprovalDecision]:
    """Reject an action in APPROVAL_REQUESTED state.

    Transitions action to REJECTED (terminal state) and produces a governed record.
    Returns (rejected_action, decision).
    """
    _require_approval_requested(action)
    if not rejecter.strip():
        raise ApprovalError("rejecter is required.")
    if not rationale.strip():
        raise ApprovalError("rationale is required.")
    if not authority_basis.strip():
        raise ApprovalError("authority_basis is required.")

    rejected_action = transition_action(action, MissionStatus.REJECTED)
    decision = ApprovalDecision(
        decision_id=_new_decision_id(),
        action_id=action.action_id,
        mission_id=action.mission_id,
        decision_type=ApprovalDecisionType.REJECTED.value,
        decided_by=rejecter,
        decided_at=decided_at,
        rationale=rationale,
        authority_basis=authority_basis,
        envelope_id=envelope_id,
        hold_until=None,
        info_requested=None,
        info_from=None,
        cns_trace_id=ensure_cns_trace_id(cns_trace_id or action.cns_trace_id),
    )
    return rejected_action, decision


def hold_action(
    action: Action,
    *,
    holder: str,
    rationale: str,
    authority_basis: str,
    decided_at: str,
    hold_until: str | None = None,
    envelope_id: str | None = None,
    cns_trace_id: str | None = None,
) -> tuple[Action, ApprovalDecision]:
    """Place an action on administrative hold.

    Does NOT transition the state machine — action stays at APPROVAL_REQUESTED.
    Produces a governed hold record for audit trail.
    Returns (action, decision) — action is unchanged.
    """
    _require_approval_requested(action)
    if not holder.strip():
        raise ApprovalError("holder is required.")
    if not rationale.strip():
        raise ApprovalError("rationale is required.")
    if not authority_basis.strip():
        raise ApprovalError("authority_basis is required.")

    decision = ApprovalDecision(
        decision_id=_new_decision_id(),
        action_id=action.action_id,
        mission_id=action.mission_id,
        decision_type=ApprovalDecisionType.HELD.value,
        decided_by=holder,
        decided_at=decided_at,
        rationale=rationale,
        authority_basis=authority_basis,
        envelope_id=envelope_id,
        hold_until=hold_until,
        info_requested=None,
        info_from=None,
        cns_trace_id=ensure_cns_trace_id(cns_trace_id or action.cns_trace_id),
    )
    return action, decision


def request_more_info(
    action: Action,
    *,
    requester: str,
    info_requested: str,
    info_from: str,
    rationale: str,
    authority_basis: str,
    decided_at: str,
    envelope_id: str | None = None,
    cns_trace_id: str | None = None,
) -> tuple[Action, ApprovalDecision]:
    """Request additional information before deciding on an action.

    Does NOT transition the state machine — action stays at APPROVAL_REQUESTED.
    Produces a governed record stating what information is needed and from whom.
    Returns (action, decision) — action is unchanged.
    """
    _require_approval_requested(action)
    if not requester.strip():
        raise ApprovalError("requester is required.")
    if not info_requested.strip():
        raise ApprovalError("info_requested is required.")
    if not info_from.strip():
        raise ApprovalError("info_from is required.")
    if not rationale.strip():
        raise ApprovalError("rationale is required.")
    if not authority_basis.strip():
        raise ApprovalError("authority_basis is required.")

    decision = ApprovalDecision(
        decision_id=_new_decision_id(),
        action_id=action.action_id,
        mission_id=action.mission_id,
        decision_type=ApprovalDecisionType.MORE_INFO_REQUESTED.value,
        decided_by=requester,
        decided_at=decided_at,
        rationale=rationale,
        authority_basis=authority_basis,
        envelope_id=envelope_id,
        hold_until=None,
        info_requested=info_requested,
        info_from=info_from,
        cns_trace_id=ensure_cns_trace_id(cns_trace_id or action.cns_trace_id),
    )
    return action, decision


class ApprovalStore:
    """Local file-backed store for ApprovalDecision records.

    Writes governed JSON records to base_path/{decision_id}.json.
    No live connectors. No HTTP. A1 local no-network boundary.
    """

    def __init__(self, base_path: str | Path) -> None:
        self._base_path = Path(base_path)

    def path_for(self, decision_id: str) -> Path:
        safe_id = decision_id.strip()
        if not _safe_decision_id(safe_id):
            raise ValueError("Approval decision ID is not safe for local storage.")
        return self._base_path / f"{safe_id}.json"

    def write(self, decision: ApprovalDecision) -> Path:
        """Write an ApprovalDecision to local JSON. Returns the written file path."""
        errors = validate_approval_decision(decision)
        if errors:
            raise ValueError(f"ApprovalDecision is invalid: {'; '.join(errors)}")
        self._base_path.mkdir(parents=True, exist_ok=True)
        path = self.path_for(decision.decision_id)
        path.write_text(json.dumps(decision.to_dict(), indent=2), encoding="utf-8")
        return path

    def read(self, decision_id: str) -> ApprovalDecision:
        """Read an ApprovalDecision by decision_id from local JSON."""
        path = self.path_for(decision_id)
        payload = json.loads(path.read_text(encoding="utf-8"))
        return ApprovalDecision.from_dict(payload)

    def exists(self, decision_id: str) -> bool:
        """Return True if a decision record file exists for this decision_id."""
        return self.path_for(decision_id).exists()

    def list_by_trace(self, cns_trace_id: str) -> tuple[ApprovalDecision, ...]:
        """Return valid decisions for one CNS trace."""
        decisions = [decision for decision in self._load_all() if decision.cns_trace_id == cns_trace_id]
        decisions.sort(key=lambda decision: (decision.decided_at, decision.decision_id))
        return tuple(decisions)

    def list_by_action(self, action_id: str) -> tuple[ApprovalDecision, ...]:
        """Return valid decisions for one action."""
        decisions = [decision for decision in self._load_all() if decision.action_id == action_id]
        decisions.sort(key=lambda decision: (decision.decided_at, decision.decision_id))
        return tuple(decisions)

    def _load_all(self) -> list[ApprovalDecision]:
        if not self._base_path.exists():
            return []
        decisions: list[ApprovalDecision] = []
        for path in sorted(self._base_path.glob("aprv-*.json")):
            try:
                decision = ApprovalDecision.from_dict(json.loads(path.read_text(encoding="utf-8")))
                if not validate_approval_decision(decision):
                    decisions.append(decision)
            except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
                continue
        return decisions


def _safe_decision_id(value: str) -> bool:
    if not value.startswith("aprv-"):
        return False
    if any(part in value for part in ("/", "\\", "..")):
        return False
    return all(character.isalnum() or character in {"-", "_"} for character in value)


__all__ = [
    "ApprovalDecision",
    "ApprovalDecisionType",
    "ApprovalError",
    "ApprovalStore",
    "approve_action",
    "hold_action",
    "reject_action",
    "request_more_info",
    "validate_approval_decision",
]
