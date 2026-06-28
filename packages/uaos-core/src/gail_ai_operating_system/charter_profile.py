"""CharterProfile schema for GAIL AI Operating System Rev 2.

A CharterProfile pre-authorizes a narrow class of autonomous actions under
R4 delegated authority without requiring per-action human approval. No
CharterProfile may grant R5 authority. R4 charters require stop conditions,
rollback path, max action count, and a non-expired expiry.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from .authority_envelope import AuthorityLevel, AutonomyLevel


@dataclass(frozen=True)
class CharterProfile:
    """Pre-authorized autonomous action class under R4 delegated authority.

    Links to an AuthorityEnvelope by reference via envelope_id — not embedded.
    R5 authority cannot be granted by any charter.
    """

    charter_id: str                         # 'charter-' prefix required
    title: str
    authority_level: str                    # R0–R4 only; R5 rejected by validator
    autonomy_level: str                     # A0–A6
    allowed_action_types: tuple[str, ...]   # closed vocabulary
    target_resources: str                   # scope description
    connector_scope: tuple[str, ...]        # registered connector IDs
    agent_scope: tuple[str, ...]            # registered agent IDs
    max_actions: int                        # required for R4; must be > 0
    expiry: str                             # ISO 8601; required for R4; must not be past
    stop_conditions: tuple[str, ...]        # required non-empty for R4
    rollback_path: str                      # required non-empty for R4
    review_cadence: str
    evidence_requirements: str
    envelope_id: str | None = None          # optional back-reference to AuthorityEnvelope

    def is_expired(self) -> bool:
        """Return True if expiry has passed or cannot be parsed."""
        try:
            expiry_dt = datetime.fromisoformat(self.expiry.replace("Z", "+00:00"))
            if expiry_dt.tzinfo is None:
                expiry_dt = expiry_dt.replace(tzinfo=timezone.utc)
            return datetime.now(timezone.utc) >= expiry_dt
        except (ValueError, AttributeError):
            return True

    def to_dict(self) -> dict[str, Any]:
        return {
            "charter_id": self.charter_id,
            "title": self.title,
            "authority_level": self.authority_level,
            "autonomy_level": self.autonomy_level,
            "allowed_action_types": list(self.allowed_action_types),
            "target_resources": self.target_resources,
            "connector_scope": list(self.connector_scope),
            "agent_scope": list(self.agent_scope),
            "max_actions": self.max_actions,
            "expiry": self.expiry,
            "stop_conditions": list(self.stop_conditions),
            "rollback_path": self.rollback_path,
            "review_cadence": self.review_cadence,
            "evidence_requirements": self.evidence_requirements,
            "envelope_id": self.envelope_id,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "CharterProfile":
        return cls(
            charter_id=str(payload["charter_id"]),
            title=str(payload["title"]),
            authority_level=str(payload["authority_level"]),
            autonomy_level=str(payload["autonomy_level"]),
            allowed_action_types=tuple(str(a) for a in payload.get("allowed_action_types", [])),
            target_resources=str(payload["target_resources"]),
            connector_scope=tuple(str(c) for c in payload.get("connector_scope", [])),
            agent_scope=tuple(str(a) for a in payload.get("agent_scope", [])),
            max_actions=int(payload["max_actions"]),
            expiry=str(payload["expiry"]),
            stop_conditions=tuple(str(c) for c in payload.get("stop_conditions", [])),
            rollback_path=str(payload["rollback_path"]),
            review_cadence=str(payload["review_cadence"]),
            evidence_requirements=str(payload["evidence_requirements"]),
            envelope_id=str(payload["envelope_id"]) if payload.get("envelope_id") is not None else None,
        )


def validate_charter_profile(charter: CharterProfile) -> list[str]:
    """Validate a CharterProfile. Returns a list of error strings (empty = valid)."""
    errors: list[str] = []

    if not charter.charter_id.startswith("charter-"):
        errors.append("charter_id must use the 'charter-' prefix.")

    if not charter.title.strip():
        errors.append("title is required.")

    level_valid = True
    try:
        level = AuthorityLevel(charter.authority_level)
        if level == AuthorityLevel.R5:
            errors.append("CharterProfile cannot grant R5 authority. R5 is human-only.")
            level_valid = False
    except ValueError:
        errors.append(
            f"authority_level '{charter.authority_level}' is not valid. "
            f"Must be one of {[l.value for l in AuthorityLevel if l != AuthorityLevel.R5]}."
        )
        level_valid = False

    try:
        AutonomyLevel(charter.autonomy_level)
    except ValueError:
        errors.append(
            f"autonomy_level '{charter.autonomy_level}' is not valid. "
            f"Must be one of {[l.value for l in AutonomyLevel]}."
        )

    if not charter.allowed_action_types:
        errors.append("allowed_action_types must include at least one entry.")
    elif any(not a.strip() for a in charter.allowed_action_types):
        errors.append("allowed_action_types cannot include blank values.")

    if not charter.target_resources.strip():
        errors.append("target_resources is required.")

    if not charter.review_cadence.strip():
        errors.append("review_cadence is required.")

    if not charter.evidence_requirements.strip():
        errors.append("evidence_requirements is required.")

    if isinstance(charter.max_actions, bool) or not isinstance(charter.max_actions, int):
        errors.append("max_actions must be a positive integer.")
    elif charter.max_actions <= 0:
        errors.append("max_actions must be greater than zero.")

    if level_valid and AuthorityLevel(charter.authority_level) == AuthorityLevel.R4:
        if not charter.stop_conditions:
            errors.append("R4 charter requires at least one stop_condition.")
        elif any(not c.strip() for c in charter.stop_conditions):
            errors.append("stop_conditions cannot include blank values.")

        if not charter.rollback_path.strip():
            errors.append("R4 charter requires a non-empty rollback_path.")

        if not charter.expiry.strip():
            errors.append("R4 charter requires a non-empty expiry.")
        else:
            try:
                expiry_dt = datetime.fromisoformat(charter.expiry.replace("Z", "+00:00"))
                if expiry_dt.tzinfo is None:
                    expiry_dt = expiry_dt.replace(tzinfo=timezone.utc)
                if datetime.now(timezone.utc) >= expiry_dt:
                    errors.append("R4 charter expiry is in the past.")
            except ValueError:
                errors.append(f"expiry '{charter.expiry}' is not a valid ISO 8601 datetime.")

    return errors


__all__ = [
    "CharterProfile",
    "validate_charter_profile",
]
