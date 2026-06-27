"""Mission schema types for GAIL AI Operating System Rev 2."""

from __future__ import annotations

from enum import Enum

from .mission_spine import (
    MissionAction,
    MissionEnvelope,
    MissionPlan,
    MissionValidationError,
    MissionValidationIssue,
    MissionValidationResult,
    PolicyDecision,
    create_mission,
    validate_mission,
)


class MissionStatus(str, Enum):
    """Canonical action state machine stages for a governed mission.

    Source: GAIL OS authority-ladders.md — Mandatory Action State Machine.
    Every governed action moves through this sequence; no stage may be skipped.
    """

    OBSERVED = "observed"
    PROPOSED = "proposed"
    CLASSIFIED = "classified"
    APPROVAL_REQUESTED = "approval_requested"
    APPROVED = "approved"
    REJECTED = "rejected"
    CLAIMED = "claimed"
    EXECUTED = "executed"
    STOPPED = "stopped"
    EVIDENCED = "evidenced"
    REVIEWED = "reviewed"
    LEARNED = "learned"


__all__ = [
    "MissionAction",
    "MissionEnvelope",
    "MissionPlan",
    "MissionStatus",
    "MissionValidationError",
    "MissionValidationIssue",
    "MissionValidationResult",
    "PolicyDecision",
    "create_mission",
    "validate_mission",
]
