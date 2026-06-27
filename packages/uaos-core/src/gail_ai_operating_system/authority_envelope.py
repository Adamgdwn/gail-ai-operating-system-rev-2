"""AuthorityEnvelope schema for GAIL AI Operating System Rev 2.

An AuthorityEnvelope is the governance charter that authorizes a specific class
of actions at a given R-level. R4 (delegated autonomous restricted action)
requires a signed AuthorityEnvelope with an explicit charter, stop conditions,
rollback path, and review cadence. No R4 without a charter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class AuthorityLevel(str, Enum):
    """R0–R5 authority ladder — classifies how much external effect an action may have."""

    R0 = "R0"
    R1 = "R1"
    R2 = "R2"
    R3 = "R3"
    R4 = "R4"
    R5 = "R5"


class AutonomyLevel(str, Enum):
    """A0–A6 autonomy maturity ladder — describes operating posture."""

    A0 = "A0"
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    A5 = "A5"
    A6 = "A6"


class EnvelopeStatus(str, Enum):
    """Lifecycle status of an AuthorityEnvelope."""

    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
    PENDING = "pending"


@dataclass(frozen=True)
class AuthorityEnvelope:
    """Governance charter that authorizes actions at a specific R-level.

    Contains 14 charter fields covering identity, authority bounds, scope,
    safety constraints, and lifecycle. Required for all R4 actions.
    """

    envelope_id: str
    mission_id: str
    authority_level: str
    autonomy_level: str
    domain: str
    granted_by: str
    granted_at: str
    expires_at: str | None
    allowed_action_types: tuple[str, ...]
    max_risk_tier: int
    stop_conditions: tuple[str, ...]
    rollback_path: str
    review_cadence: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "envelope_id": self.envelope_id,
            "mission_id": self.mission_id,
            "authority_level": self.authority_level,
            "autonomy_level": self.autonomy_level,
            "domain": self.domain,
            "granted_by": self.granted_by,
            "granted_at": self.granted_at,
            "expires_at": self.expires_at,
            "allowed_action_types": list(self.allowed_action_types),
            "max_risk_tier": self.max_risk_tier,
            "stop_conditions": list(self.stop_conditions),
            "rollback_path": self.rollback_path,
            "review_cadence": self.review_cadence,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "AuthorityEnvelope":
        return cls(
            envelope_id=str(payload["envelope_id"]),
            mission_id=str(payload["mission_id"]),
            authority_level=str(payload["authority_level"]),
            autonomy_level=str(payload["autonomy_level"]),
            domain=str(payload["domain"]),
            granted_by=str(payload["granted_by"]),
            granted_at=str(payload["granted_at"]),
            expires_at=str(payload["expires_at"]) if payload.get("expires_at") is not None else None,
            allowed_action_types=tuple(str(a) for a in payload.get("allowed_action_types", [])),
            max_risk_tier=int(payload["max_risk_tier"]),
            stop_conditions=tuple(str(c) for c in payload.get("stop_conditions", [])),
            rollback_path=str(payload["rollback_path"]),
            review_cadence=str(payload["review_cadence"]),
            status=str(payload.get("status", EnvelopeStatus.PENDING.value)),
        )


def validate_authority_envelope(envelope: AuthorityEnvelope) -> list[str]:
    """Validate an AuthorityEnvelope. Returns list of error messages (empty = valid)."""

    errors: list[str] = []

    if not envelope.envelope_id.startswith("env-"):
        errors.append("envelope_id must use the env- prefix.")
    if not envelope.mission_id.startswith("mission-"):
        errors.append("mission_id must use the mission- prefix.")
    try:
        AuthorityLevel(envelope.authority_level)
    except ValueError:
        errors.append(f"authority_level must be one of {[l.value for l in AuthorityLevel]}.")
    try:
        AutonomyLevel(envelope.autonomy_level)
    except ValueError:
        errors.append(f"autonomy_level must be one of {[l.value for l in AutonomyLevel]}.")
    if not envelope.domain.strip():
        errors.append("domain is required.")
    if not envelope.granted_by.strip():
        errors.append("granted_by is required.")
    if not envelope.granted_at.strip():
        errors.append("granted_at is required.")
    if not (0 <= envelope.max_risk_tier <= 5):
        errors.append("max_risk_tier must be between 0 and 5.")
    if not envelope.rollback_path.strip():
        errors.append("rollback_path is required.")
    if not envelope.review_cadence.strip():
        errors.append("review_cadence is required.")
    try:
        EnvelopeStatus(envelope.status)
    except ValueError:
        errors.append(f"status must be one of {[s.value for s in EnvelopeStatus]}.")

    return errors


__all__ = [
    "AuthorityEnvelope",
    "AuthorityLevel",
    "AutonomyLevel",
    "EnvelopeStatus",
    "validate_authority_envelope",
]
