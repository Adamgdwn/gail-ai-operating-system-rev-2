"""Tests for action.py — Action schema and state machine."""

from contextlib import contextmanager
import re
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "packages", "uaos-core", "src"))

from gail_ai_operating_system.action import (
    Action,
    ActionTransitionError,
    TERMINAL_STATES,
    VALID_TRANSITIONS,
    create_action,
    transition_action,
    validate_action,
)
from gail_ai_operating_system.mission import MissionStatus


@contextmanager
def raises(expected_exception, match=None):
    try:
        yield
    except expected_exception as error:
        if match is not None and re.search(match, str(error)) is None:
            raise AssertionError(f"{match!r} did not match {error!r}") from error
        return
    raise AssertionError(f"{expected_exception.__name__} was not raised")


def make_action(**kwargs) -> Action:
    defaults = dict(
        mission_id="mission-abc123def456",
        action_type="local_mission_record",
        title="Test action",
        actor="Adam Goodwin",
    )
    defaults.update(kwargs)
    return create_action(**defaults)


# ── MissionStatus enum coverage ────────────────────────────────────────────

def test_all_state_machine_stages_present():
    stages = {s.value for s in MissionStatus}
    expected = {
        "observed", "proposed", "classified", "approval_requested",
        "approved", "rejected", "claimed", "executed", "stopped",
        "evidenced", "reviewed", "learned",
    }
    assert stages == expected


def test_valid_transitions_covers_all_statuses():
    for status in MissionStatus:
        assert status in VALID_TRANSITIONS


# ── create_action factory ─────────────────────────────────────────────

def test_create_action_returns_observed():
    assert make_action().status == MissionStatus.OBSERVED


def test_create_action_generates_action_prefix():
    assert make_action().action_id.startswith("action-")


def test_create_action_bad_mission_prefix_raises():
    with raises(ValueError, match="mission- prefix"):
        create_action(
            mission_id="bad-id-123",
            action_type="local_mission_record",
            title="Test",
            actor="Adam Goodwin",
        )


def test_create_action_empty_type_raises():
    with raises(ValueError, match="action_type"):
        create_action(
            mission_id="mission-abc123",
            action_type="",
            title="Test",
            actor="Adam Goodwin",
        )


def test_create_action_empty_actor_raises():
    with raises(ValueError, match="actor"):
        create_action(
            mission_id="mission-abc123",
            action_type="local_mission_record",
            title="Test",
            actor="",
        )


def test_create_action_invalid_authority_level_raises():
    with raises(ValueError, match="authority_level"):
        make_action(authority_level="R9")


def test_create_action_invalid_risk_tier_raises():
    with raises(ValueError, match="risk_tier"):
        make_action(risk_tier=6)


def test_create_action_r4_requires_envelope():
    with raises(ValueError, match="R4 actions require"):
        make_action(authority_level="R4")


def test_create_action_r4_accepts_envelope_reference():
    action = make_action(authority_level="R4", envelope_id="env-r4-charter-001")
    assert action.authority_level == "R4"
    assert action.envelope_id == "env-r4-charter-001"


# ── State machine transitions ──────────────────────────────────────────────

def test_observed_to_proposed():
    action = transition_action(make_action(), MissionStatus.PROPOSED)
    assert action.status == MissionStatus.PROPOSED


def test_full_approval_path_reaches_learned():
    action = make_action()
    for stage in [
        MissionStatus.PROPOSED,
        MissionStatus.CLASSIFIED,
        MissionStatus.APPROVAL_REQUESTED,
        MissionStatus.APPROVED,
        MissionStatus.CLAIMED,
        MissionStatus.EXECUTED,
        MissionStatus.EVIDENCED,
        MissionStatus.REVIEWED,
        MissionStatus.LEARNED,
    ]:
        action = transition_action(action, stage)
    assert action.status == MissionStatus.LEARNED


def test_rejection_path():
    action = make_action()
    for stage in [
        MissionStatus.PROPOSED,
        MissionStatus.CLASSIFIED,
        MissionStatus.APPROVAL_REQUESTED,
        MissionStatus.REJECTED,
    ]:
        action = transition_action(action, stage)
    assert action.status == MissionStatus.REJECTED


def test_stop_path_reaches_evidenced():
    action = make_action()
    for stage in [
        MissionStatus.PROPOSED,
        MissionStatus.CLASSIFIED,
        MissionStatus.APPROVAL_REQUESTED,
        MissionStatus.APPROVED,
        MissionStatus.CLAIMED,
        MissionStatus.STOPPED,
        MissionStatus.EVIDENCED,
    ]:
        action = transition_action(action, stage)
    assert action.status == MissionStatus.EVIDENCED


def test_invalid_transition_raises():
    with raises(ActionTransitionError):
        transition_action(make_action(), MissionStatus.EXECUTED)


def test_transition_blocks_r4_without_envelope():
    action = Action(
        action_id="action-abc123",
        mission_id="mission-def456",
        action_type="local_mission_record",
        title="Test",
        actor="Adam Goodwin",
        status=MissionStatus.OBSERVED,
        authority_level="R4",
        risk_tier=4,
        arguments={},
        created_at="2026-06-27T00:00:00+00:00",
    )
    with raises(ActionTransitionError, match="R4 actions require"):
        transition_action(action, MissionStatus.PROPOSED)


def test_transition_blocks_r5_agent_approval():
    action = make_action(authority_level="R5", risk_tier=5)
    for stage in [
        MissionStatus.PROPOSED,
        MissionStatus.CLASSIFIED,
        MissionStatus.APPROVAL_REQUESTED,
    ]:
        action = transition_action(action, stage)
    with raises(ActionTransitionError, match="R5 actions are human-only"):
        transition_action(action, MissionStatus.APPROVED)


def test_terminal_rejected_raises_on_next_transition():
    action = make_action()
    for stage in [
        MissionStatus.PROPOSED,
        MissionStatus.CLASSIFIED,
        MissionStatus.APPROVAL_REQUESTED,
        MissionStatus.REJECTED,
    ]:
        action = transition_action(action, stage)
    with raises(ActionTransitionError, match="terminal"):
        transition_action(action, MissionStatus.CLAIMED)


def test_terminal_learned_raises_on_next_transition():
    action = make_action()
    for stage in [
        MissionStatus.PROPOSED,
        MissionStatus.CLASSIFIED,
        MissionStatus.APPROVAL_REQUESTED,
        MissionStatus.APPROVED,
        MissionStatus.CLAIMED,
        MissionStatus.EXECUTED,
        MissionStatus.EVIDENCED,
        MissionStatus.REVIEWED,
        MissionStatus.LEARNED,
    ]:
        action = transition_action(action, stage)
    with raises(ActionTransitionError, match="terminal"):
        transition_action(action, MissionStatus.REVIEWED)


def test_claimed_at_set_when_claimed():
    action = make_action()
    for stage in [
        MissionStatus.PROPOSED,
        MissionStatus.CLASSIFIED,
        MissionStatus.APPROVAL_REQUESTED,
        MissionStatus.APPROVED,
    ]:
        action = transition_action(action, stage)
    assert action.claimed_at is None
    action = transition_action(action, MissionStatus.CLAIMED)
    assert action.claimed_at is not None


def test_executed_at_set_when_executed():
    action = make_action()
    for stage in [
        MissionStatus.PROPOSED,
        MissionStatus.CLASSIFIED,
        MissionStatus.APPROVAL_REQUESTED,
        MissionStatus.APPROVED,
        MissionStatus.CLAIMED,
    ]:
        action = transition_action(action, stage)
    assert action.executed_at is None
    action = transition_action(action, MissionStatus.EXECUTED)
    assert action.executed_at is not None


def test_executed_at_set_when_stopped():
    action = make_action()
    for stage in [
        MissionStatus.PROPOSED,
        MissionStatus.CLASSIFIED,
        MissionStatus.APPROVAL_REQUESTED,
        MissionStatus.APPROVED,
        MissionStatus.CLAIMED,
    ]:
        action = transition_action(action, stage)
    action = transition_action(action, MissionStatus.STOPPED)
    assert action.executed_at is not None


# ── Serialization round-trip ──────────────────────────────────────────

def test_round_trip_serialization():
    action = make_action()
    restored = Action.from_dict(action.to_dict())
    assert restored.action_id == action.action_id
    assert restored.mission_id == action.mission_id
    assert restored.status == action.status
    assert restored.actor == action.actor
    assert restored.risk_tier == action.risk_tier
    assert restored.arguments == dict(action.arguments)


# ── validate_action ────────────────────────────────────────────────

def test_validate_action_clean():
    assert validate_action(make_action()) == []


def test_validate_action_bad_action_prefix():
    action = Action(
        action_id="bad-id",
        mission_id="mission-abc123",
        action_type="local_mission_record",
        title="Test",
        actor="Adam Goodwin",
        status=MissionStatus.OBSERVED,
        authority_level="R0",
        risk_tier=1,
        arguments={},
        created_at="2026-06-27T00:00:00+00:00",
    )
    errors = validate_action(action)
    assert any("action- prefix" in e for e in errors)


def test_validate_action_bad_risk_tier():
    action = Action(
        action_id="action-abc123",
        mission_id="mission-def456",
        action_type="local_mission_record",
        title="Test",
        actor="Adam Goodwin",
        status=MissionStatus.OBSERVED,
        authority_level="R0",
        risk_tier=99,
        arguments={},
        created_at="2026-06-27T00:00:00+00:00",
    )
    errors = validate_action(action)
    assert any("risk_tier" in e for e in errors)


def test_validate_action_bad_authority_level():
    action = Action(
        action_id="action-abc123",
        mission_id="mission-def456",
        action_type="local_mission_record",
        title="Test",
        actor="Adam Goodwin",
        status=MissionStatus.OBSERVED,
        authority_level="R9",
        risk_tier=1,
        arguments={},
        created_at="2026-06-27T00:00:00+00:00",
    )
    errors = validate_action(action)
    assert any("authority_level" in e for e in errors)


def test_validate_action_r4_requires_envelope():
    action = Action(
        action_id="action-abc123",
        mission_id="mission-def456",
        action_type="local_mission_record",
        title="Test",
        actor="Adam Goodwin",
        status=MissionStatus.OBSERVED,
        authority_level="R4",
        risk_tier=4,
        arguments={},
        created_at="2026-06-27T00:00:00+00:00",
    )
    errors = validate_action(action)
    assert any("R4 actions require" in e for e in errors)


def test_validate_action_bad_envelope_prefix():
    action = Action(
        action_id="action-abc123",
        mission_id="mission-def456",
        action_type="local_mission_record",
        title="Test",
        actor="Adam Goodwin",
        status=MissionStatus.OBSERVED,
        authority_level="R0",
        risk_tier=1,
        arguments={},
        created_at="2026-06-27T00:00:00+00:00",
        envelope_id="bad-envelope",
    )
    errors = validate_action(action)
    assert any("env- prefix" in e for e in errors)


def test_validate_action_r5_execution_state_rejected():
    action = Action(
        action_id="action-abc123",
        mission_id="mission-def456",
        action_type="local_mission_record",
        title="Test",
        actor="Adam Goodwin",
        status=MissionStatus.APPROVED,
        authority_level="R5",
        risk_tier=5,
        arguments={},
        created_at="2026-06-27T00:00:00+00:00",
    )
    errors = validate_action(action)
    assert any("R5 actions are human-only" in e for e in errors)


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTests(tests)
    for name, value in sorted(globals().items()):
        if name.startswith("test_") and callable(value):
            suite.addTest(unittest.FunctionTestCase(value))
    return suite
