"""EvidencePacket schema for GAIL AI Operating System Rev 2.

An EvidencePacket is the auditable record produced when a governed action
completes (whether executed or stopped). An action is not considered done
until its EvidencePacket exists. Evidence feeds the review → learned cycle
in the CNS learning loop.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping
from uuid import uuid4


class EvidenceResult(str, Enum):
    """Outcome classification for a governed action."""

    SUCCESS = "success"
    FAILURE = "failure"
    STOPPED = "stopped"
    PARTIAL = "partial"


class ExecutionMode(str, Enum):
    """Execution mode under which the action ran."""

    DRY_RUN = "dry-run"
    LIVE = "live"


@dataclass(frozen=True)
class EvidencePacket:
    """Auditable record produced when a governed action completes.

    Fields align with Chunk 20 spec: mission_id, actor, action_type,
    authority_basis, result, rollback_note, created_at — plus identity
    and mode fields required for a complete audit trail.
    """

    evidence_id: str
    mission_id: str
    action_id: str
    actor: str
    action_type: str
    authority_basis: str
    result: str
    execution_mode: str
    created_at: str
    envelope_id: str | None
    rollback_note: str | None
    outcome_summary: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "mission_id": self.mission_id,
            "action_id": self.action_id,
            "actor": self.actor,
            "action_type": self.action_type,
            "authority_basis": self.authority_basis,
            "result": self.result,
            "execution_mode": self.execution_mode,
            "created_at": self.created_at,
            "envelope_id": self.envelope_id,
            "rollback_note": self.rollback_note,
            "outcome_summary": self.outcome_summary,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "EvidencePacket":
        return cls(
            evidence_id=str(payload["evidence_id"]),
            mission_id=str(payload["mission_id"]),
            action_id=str(payload["action_id"]),
            actor=str(payload["actor"]),
            action_type=str(payload["action_type"]),
            authority_basis=str(payload["authority_basis"]),
            result=str(payload["result"]),
            execution_mode=str(payload.get("execution_mode", ExecutionMode.DRY_RUN.value)),
            created_at=str(payload["created_at"]),
            envelope_id=str(payload["envelope_id"]) if payload.get("envelope_id") is not None else None,
            rollback_note=str(payload["rollback_note"]) if payload.get("rollback_note") is not None else None,
            outcome_summary=str(payload.get("outcome_summary", "")),
        )


def create_evidence_packet(
    *,
    mission_id: str,
    action_id: str,
    actor: str,
    action_type: str,
    authority_basis: str,
    result: str,
    created_at: str,
    execution_mode: str = ExecutionMode.DRY_RUN.value,
    envelope_id: str | None = None,
    rollback_note: str | None = None,
    outcome_summary: str = "",
) -> EvidencePacket:
    """Create a new EvidencePacket with a generated evidence_id."""

    errors = _validate_inputs(mission_id, action_id, actor, action_type, authority_basis, result, created_at)
    if errors:
        raise ValueError("; ".join(errors))

    return EvidencePacket(
        evidence_id=f"evidence-{uuid4().hex[:12]}",
        mission_id=mission_id,
        action_id=action_id,
        actor=actor,
        action_type=action_type,
        authority_basis=authority_basis,
        result=result,
        execution_mode=execution_mode,
        created_at=created_at,
        envelope_id=envelope_id,
        rollback_note=rollback_note,
        outcome_summary=outcome_summary,
    )


def validate_evidence_packet(packet: EvidencePacket) -> list[str]:
    """Validate an EvidencePacket. Returns list of error messages (empty = valid)."""

    return _validate_inputs(
        packet.mission_id,
        packet.action_id,
        packet.actor,
        packet.action_type,
        packet.authority_basis,
        packet.result,
        packet.created_at,
    )


def _validate_inputs(
    mission_id: str,
    action_id: str,
    actor: str,
    action_type: str,
    authority_basis: str,
    result: str,
    created_at: str,
) -> list[str]:
    errors: list[str] = []
    if not mission_id.startswith("mission-"):
        errors.append("mission_id must use the mission- prefix.")
    if not action_id.strip():
        errors.append("action_id is required.")
    if not actor.strip():
        errors.append("actor is required.")
    if not action_type.strip():
        errors.append("action_type is required.")
    if not authority_basis.strip():
        errors.append("authority_basis is required.")
    try:
        EvidenceResult(result)
    except ValueError:
        errors.append(f"result must be one of {[r.value for r in EvidenceResult]}.")
    if not created_at.strip():
        errors.append("created_at is required.")
    return errors


__all__ = [
    "EvidencePacket",
    "EvidenceResult",
    "ExecutionMode",
    "create_evidence_packet",
    "validate_evidence_packet",
]
