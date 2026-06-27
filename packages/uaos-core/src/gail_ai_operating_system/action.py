"""Action schema and state machine for GAIL AI Operating System Rev 2."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from uuid import uuid4

from .authority_envelope import AuthorityLevel
from .mission import MissionStatus
from .mission_spine import (
    MissionAction,
    PermissionGate,
    PolicyDecision,
    current_timestamp,
)


VALID_TRANSITIONS: dict[MissionStatus, frozenset[MissionStatus]] = {
    MissionStatus.OBSERVED: frozenset({MissionStatus.PROPOSED}),
    MissionStatus.PROPOSED: frozenset({MissionStatus.CLASSIFIED}),
    MissionStatus.CLASSIFIED: frozenset({MissionStatus.APPROVAL_REQUESTED}),
    MissionStatus.APPROVAL_REQUESTED: frozenset({MissionStatus.APPROVED, MissionStatus.REJECTED}),
    MissionStatus.APPROVED: frozenset({MissionStatus.CLAIMED}),
    MissionStatus.REJECTED: frozenset(),
    MissionStatus.CLAIMED: frozenset({MissionStatus.EXECUTED, MissionStatus.STOPPED}),
    MissionStatus.EXECUTED: frozenset({MissionStatus.EVIDENCED}),
    MissionStatus.STOPPED: frozenset({MissionStatus.EVIDENCED}),
    MissionStatus.EVIDENCED: frozenset({MissionStatus.REVIEWED}),
    MissionStatus.REVIEWED: frozenset({MissionStatus.LEARNED}),
    MissionStatus.LEARNED: frozenset(),
}

TERMINAL_STATES: frozenset[MissionStatus] = frozenset(
    {MissionStatus.REJECTED, MissionStatus.LEARNED}
)
ENVELOPE_REQUIRED_LEVELS: frozenset[AuthorityLevel] = frozenset({AuthorityLevel.R4})
R5_AGENT_BLOCKED_STATES: frozenset[MissionStatus] = frozenset(
    {
        MissionStatus.APPROVED,
        MissionStatus.CLAIMED,
        MissionStatus.EXECUTED,
        MissionStatus.STOPPED,
        MissionStatus.EVIDENCED,
        MissionStatus.REVIEWED,
        MissionStatus.LEARNED,
    }
)


class ActionTransitionError(ValueError):
    """Raised when a state machine transition is not permitted."""


@dataclass(frozen=True)
class Action:
    """A governed action moving through the GAIL OS mandatory state machine.

    action_id must use the 'action-' prefix.
    status tracks the current stage of the mandatory action state machine.
    """

    action_id: str
    mission_id: str
    action_type: str
    title: str
    actor: str
    status: MissionStatus = MissionStatus.OBSERVED
    authority_level: str = "R0"
    risk_tier: int = 1
    arguments: Mapping[str, Any] = field(default_factory=dict)
    created_at: str = ""
    claimed_at: str | None = None
    executed_at: str | None = None
    envelope_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "mission_id": self.mission_id,
            "action_type": self.action_type,
            "title": self.title,
            "actor": self.actor,
            "status": self.status.value,
            "authority_level": self.authority_level,
            "risk_tier": self.risk_tier,
            "arguments": dict(self.arguments),
            "created_at": self.created_at,
            "claimed_at": self.claimed_at,
            "executed_at": self.executed_at,
            "envelope_id": self.envelope_id,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Action":
        return cls(
            action_id=str(payload["action_id"]),
            mission_id=str(payload["mission_id"]),
            action_type=str(payload["action_type"]),
            title=str(payload["title"]),
            actor=str(payload["actor"]),
            status=MissionStatus(payload["status"]),
            authority_level=str(payload.get("authority_level", "R0")),
            risk_tier=int(payload.get("risk_tier", 1)),
            arguments=dict(payload.get("arguments", {})),
            created_at=str(payload.get("created_at", "")),
            claimed_at=str(payload["claimed_at"]) if payload.get("claimed_at") else None,
            executed_at=str(payload["executed_at"]) if payload.get("executed_at") else None,
            envelope_id=str(payload["envelope_id"]) if payload.get("envelope_id") else None,
        )


def create_action(
    mission_id: str,
    action_type: str,
    title: str,
    actor: str,
    *,
    authority_level: str = "R0",
    risk_tier: int = 1,
    arguments: Mapping[str, Any] | None = None,
    envelope_id: str | None = None,
) -> Action:
    """Create a new Action in the OBSERVED state."""
    if not mission_id.startswith("mission-"):
        raise ValueError("mission_id must use the mission- prefix.")
    if not action_type.strip():
        raise ValueError("action_type is required.")
    if not title.strip():
        raise ValueError("title is required.")
    if not actor.strip():
        raise ValueError("actor is required.")
    authority_errors = _validate_authority_fields(authority_level, risk_tier, envelope_id)
    if authority_errors:
        raise ValueError("; ".join(authority_errors))
    return Action(
        action_id=f"action-{uuid4().hex[:12]}",
        mission_id=mission_id,
        action_type=action_type.strip(),
        title=title.strip(),
        actor=actor.strip(),
        status=MissionStatus.OBSERVED,
        authority_level=authority_level,
        risk_tier=risk_tier,
        arguments=dict(arguments) if arguments else {},
        created_at=current_timestamp(),
        envelope_id=envelope_id,
    )


def transition_action(action: Action, to_status: MissionStatus) -> Action:
    """Advance an action to the next state machine stage.

    Raises ActionTransitionError if the transition is not permitted.
    """
    validation_errors = validate_action(action)
    if validation_errors:
        raise ActionTransitionError(f"Action failed validation: {'; '.join(validation_errors)}")
    if action.authority_level == AuthorityLevel.R5.value and to_status in R5_AGENT_BLOCKED_STATES:
        raise ActionTransitionError("R5 actions are human-only and cannot enter agent execution states.")
    allowed = VALID_TRANSITIONS.get(action.status, frozenset())
    if to_status not in allowed:
        if action.status in TERMINAL_STATES:
            raise ActionTransitionError(
                f"Action is in terminal state {action.status.value!r} — no further transitions allowed."
            )
        raise ActionTransitionError(
            f"Transition from {action.status.value!r} to {to_status.value!r} is not allowed. "
            f"Allowed next states: {sorted(s.value for s in allowed) or 'none (terminal)'}."
        )
    now = current_timestamp()
    claimed_at = action.claimed_at
    executed_at = action.executed_at
    if to_status == MissionStatus.CLAIMED:
        claimed_at = now
    elif to_status in (MissionStatus.EXECUTED, MissionStatus.STOPPED):
        executed_at = now
    return Action(
        action_id=action.action_id,
        mission_id=action.mission_id,
        action_type=action.action_type,
        title=action.title,
        actor=action.actor,
        status=to_status,
        authority_level=action.authority_level,
        risk_tier=action.risk_tier,
        arguments=action.arguments,
        created_at=action.created_at,
        claimed_at=claimed_at,
        executed_at=executed_at,
        envelope_id=action.envelope_id,
    )


def validate_action(action: Action) -> list[str]:
    """Return a list of validation errors; empty list means valid."""
    errors: list[str] = []
    if not action.action_id.startswith("action-"):
        errors.append("action_id must use the action- prefix.")
    if not action.mission_id.startswith("mission-"):
        errors.append("mission_id must use the mission- prefix.")
    if not action.action_type.strip():
        errors.append("action_type is required.")
    if not action.title.strip():
        errors.append("title is required.")
    if not action.actor.strip():
        errors.append("actor is required.")
    if not isinstance(action.status, MissionStatus):
        errors.append(f"status {action.status!r} is not a valid MissionStatus.")
    errors.extend(_validate_authority_fields(action.authority_level, action.risk_tier, action.envelope_id))
    if action.authority_level == AuthorityLevel.R5.value and action.status in R5_AGENT_BLOCKED_STATES:
        errors.append("R5 actions are human-only and cannot enter approved or execution states.")
    return errors


def _validate_authority_fields(
    authority_level: str,
    risk_tier: int,
    envelope_id: str | None,
) -> list[str]:
    errors: list[str] = []

    try:
        authority = AuthorityLevel(authority_level)
    except ValueError:
        errors.append(f"authority_level must be one of {[level.value for level in AuthorityLevel]}.")
        authority = None

    if isinstance(risk_tier, bool) or not isinstance(risk_tier, int):
        errors.append("risk_tier must be an integer between 0 and 5.")
    elif risk_tier < 0 or risk_tier > 5:
        errors.append("risk_tier must be between 0 and 5.")

    if envelope_id is not None and not envelope_id.startswith("env-"):
        errors.append("envelope_id must use the env- prefix when present.")
    if authority in ENVELOPE_REQUIRED_LEVELS and envelope_id is None:
        errors.append("R4 actions require an AuthorityEnvelope envelope_id.")

    return errors


__all__ = [
    "Action",
    "ActionTransitionError",
    "ENVELOPE_REQUIRED_LEVELS",
    "R5_AGENT_BLOCKED_STATES",
    "TERMINAL_STATES",
    "VALID_TRANSITIONS",
    "create_action",
    "transition_action",
    "validate_action",
    "MissionAction",
    "PermissionGate",
    "PolicyDecision",
]
