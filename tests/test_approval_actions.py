"""Tests for approval_actions.py — transport-independent local approval service."""

from contextlib import contextmanager
import json
import re
import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "packages", "uaos-core", "src"))

from gail_ai_operating_system.action import create_action, transition_action
from gail_ai_operating_system.approval_actions import (
    ApprovalDecision,
    ApprovalDecisionType,
    ApprovalError,
    ApprovalStore,
    approve_action,
    hold_action,
    reject_action,
    request_more_info,
    validate_approval_decision,
)
from gail_ai_operating_system.mission import MissionStatus


DECIDED_AT = "2026-06-28T00:00:00-06:00"


@contextmanager
def raises(expected_exception, match=None):
    try:
        yield
    except expected_exception as error:
        if match is not None and re.search(match, str(error)) is None:
            raise AssertionError(f"{match!r} did not match {error!r}") from error
        return
    raise AssertionError(f"{expected_exception.__name__} was not raised")


def make_approval_requested_action(**kwargs):
    """Advance an action to APPROVAL_REQUESTED state."""
    defaults = dict(
        mission_id="mission-abc123def456",
        action_type="local_approval_test",
        title="Test approval action",
        actor="Adam Goodwin",
    )
    defaults.update(kwargs)
    action = create_action(**defaults)
    action = transition_action(action, MissionStatus.PROPOSED)
    action = transition_action(action, MissionStatus.CLASSIFIED)
    action = transition_action(action, MissionStatus.APPROVAL_REQUESTED)
    return action


def make_decision(**kwargs) -> ApprovalDecision:
    """Build a minimal valid APPROVED ApprovalDecision for validation tests."""
    defaults = dict(
        decision_id="aprv-aabbcc112233",
        action_id="action-aabbcc112233",
        mission_id="mission-aabbcc112233",
        decision_type=ApprovalDecisionType.APPROVED.value,
        decided_by="Adam Goodwin",
        decided_at=DECIDED_AT,
        rationale="Test rationale",
        authority_basis="R0 — local test approval",
        envelope_id=None,
        hold_until=None,
        info_requested=None,
        info_from=None,
    )
    defaults.update(kwargs)
    return ApprovalDecision(**defaults)


# ── ApprovalDecisionType enum ────────────────────────────────────────────────

def test_decision_type_values_complete():
    values = {t.value for t in ApprovalDecisionType}
    assert values == {"approved", "rejected", "held", "more_info_requested"}


# ── approve_action ───────────────────────────────────────────────────────────

def test_approve_transitions_to_approved():
    action = make_approval_requested_action()
    approved, decision = approve_action(
        action,
        approver="Adam Goodwin",
        rationale="Mission is low-risk and well-scoped.",
        authority_basis="R0 — local dry-run",
        decided_at=DECIDED_AT,
    )
    assert approved.status == MissionStatus.APPROVED
    assert decision.decision_type == ApprovalDecisionType.APPROVED.value


def test_approve_decision_id_prefix():
    action = make_approval_requested_action()
    _, decision = approve_action(
        action,
        approver="Adam Goodwin",
        rationale="OK",
        authority_basis="R0",
        decided_at=DECIDED_AT,
    )
    assert decision.decision_id.startswith("aprv-")


def test_approve_decision_has_cns_trace_id():
    action = make_approval_requested_action()
    _, decision = approve_action(
        action,
        approver="Adam Goodwin",
        rationale="OK",
        authority_basis="R0",
        decided_at=DECIDED_AT,
    )
    assert decision.cns_trace_id.startswith("cns-")


def test_approve_preserves_action_identity():
    action = make_approval_requested_action()
    approved, decision = approve_action(
        action,
        approver="Adam Goodwin",
        rationale="OK",
        authority_basis="R0",
        decided_at=DECIDED_AT,
    )
    assert approved.action_id == action.action_id
    assert decision.action_id == action.action_id
    assert decision.mission_id == action.mission_id


def test_approve_wrong_state_raises():
    action = create_action(
        mission_id="mission-abc123def456",
        action_type="test",
        title="Test",
        actor="Adam",
    )
    with raises(ApprovalError, match="approval_requested"):
        approve_action(
            action,
            approver="Adam",
            rationale="OK",
            authority_basis="R0",
            decided_at=DECIDED_AT,
        )


def test_approve_empty_approver_raises():
    action = make_approval_requested_action()
    with raises(ApprovalError, match="approver"):
        approve_action(action, approver="  ", rationale="OK", authority_basis="R0", decided_at=DECIDED_AT)


def test_approve_empty_rationale_raises():
    action = make_approval_requested_action()
    with raises(ApprovalError, match="rationale"):
        approve_action(action, approver="Adam", rationale="", authority_basis="R0", decided_at=DECIDED_AT)


def test_approve_empty_authority_basis_raises():
    action = make_approval_requested_action()
    with raises(ApprovalError, match="authority_basis"):
        approve_action(action, approver="Adam", rationale="OK", authority_basis="", decided_at=DECIDED_AT)


def test_approve_with_envelope_id():
    action = make_approval_requested_action()
    _, decision = approve_action(
        action,
        approver="Adam Goodwin",
        rationale="Envelope-governed approval",
        authority_basis="R4 — delegated charter",
        decided_at=DECIDED_AT,
        envelope_id="env-abc123def456",
    )
    assert decision.envelope_id == "env-abc123def456"


def test_approve_r5_action_blocked_by_state_machine():
    """R5 approval attempts are blocked by transition_action, not approve_action."""
    from gail_ai_operating_system.action import ActionTransitionError
    action = create_action(
        mission_id="mission-abc123def456",
        action_type="test",
        title="R5 action",
        actor="Adam",
        authority_level="R5",
    )
    action = transition_action(action, MissionStatus.PROPOSED)
    action = transition_action(action, MissionStatus.CLASSIFIED)
    action = transition_action(action, MissionStatus.APPROVAL_REQUESTED)
    with raises(ActionTransitionError, match="R5"):
        approve_action(
            action,
            approver="Adam",
            rationale="Trying to approve R5",
            authority_basis="R5 — human only",
            decided_at=DECIDED_AT,
        )


# ── reject_action ────────────────────────────────────────────────────────────

def test_reject_transitions_to_rejected():
    action = make_approval_requested_action()
    rejected, decision = reject_action(
        action,
        rejecter="Adam Goodwin",
        rationale="Out of scope for current mission.",
        authority_basis="R0 — local dry-run",
        decided_at=DECIDED_AT,
    )
    assert rejected.status == MissionStatus.REJECTED
    assert decision.decision_type == ApprovalDecisionType.REJECTED.value


def test_reject_produces_terminal_state():
    action = make_approval_requested_action()
    rejected, _ = reject_action(
        action,
        rejecter="Adam",
        rationale="Scope mismatch",
        authority_basis="R0",
        decided_at=DECIDED_AT,
    )
    assert rejected.status in (MissionStatus.REJECTED, MissionStatus.LEARNED)


def test_reject_wrong_state_raises():
    action = create_action(
        mission_id="mission-abc123def456",
        action_type="test",
        title="Test",
        actor="Adam",
    )
    with raises(ApprovalError, match="approval_requested"):
        reject_action(action, rejecter="Adam", rationale="No", authority_basis="R0", decided_at=DECIDED_AT)


def test_reject_empty_rejecter_raises():
    action = make_approval_requested_action()
    with raises(ApprovalError, match="rejecter"):
        reject_action(action, rejecter="", rationale="OK", authority_basis="R0", decided_at=DECIDED_AT)


# ── hold_action ──────────────────────────────────────────────────────────────

def test_hold_does_not_transition_state():
    action = make_approval_requested_action()
    held_action, decision = hold_action(
        action,
        holder="Adam Goodwin",
        rationale="Awaiting policy review.",
        authority_basis="R0 — local dry-run",
        decided_at=DECIDED_AT,
    )
    assert held_action.status == MissionStatus.APPROVAL_REQUESTED
    assert decision.decision_type == ApprovalDecisionType.HELD.value


def test_hold_action_identity_preserved():
    action = make_approval_requested_action()
    returned_action, _ = hold_action(
        action,
        holder="Adam",
        rationale="Pending review",
        authority_basis="R0",
        decided_at=DECIDED_AT,
    )
    assert returned_action is action


def test_hold_with_hold_until():
    action = make_approval_requested_action()
    _, decision = hold_action(
        action,
        holder="Adam",
        rationale="Hold for 24h",
        authority_basis="R0",
        decided_at=DECIDED_AT,
        hold_until="2026-06-29T00:00:00-06:00",
    )
    assert decision.hold_until == "2026-06-29T00:00:00-06:00"


def test_hold_wrong_state_raises():
    action = create_action(
        mission_id="mission-abc123def456",
        action_type="test",
        title="Test",
        actor="Adam",
    )
    with raises(ApprovalError, match="approval_requested"):
        hold_action(action, holder="Adam", rationale="Hold", authority_basis="R0", decided_at=DECIDED_AT)


def test_hold_empty_holder_raises():
    action = make_approval_requested_action()
    with raises(ApprovalError, match="holder"):
        hold_action(action, holder="", rationale="Hold", authority_basis="R0", decided_at=DECIDED_AT)


# ── request_more_info ────────────────────────────────────────────────────────

def test_request_more_info_does_not_transition_state():
    action = make_approval_requested_action()
    returned_action, decision = request_more_info(
        action,
        requester="Adam Goodwin",
        info_requested="Confirm risk tier classification.",
        info_from="mission proposer",
        rationale="Risk tier is unclear.",
        authority_basis="R0 — local dry-run",
        decided_at=DECIDED_AT,
    )
    assert returned_action.status == MissionStatus.APPROVAL_REQUESTED
    assert decision.decision_type == ApprovalDecisionType.MORE_INFO_REQUESTED.value


def test_request_more_info_fields_stored():
    action = make_approval_requested_action()
    _, decision = request_more_info(
        action,
        requester="Adam",
        info_requested="Need full scope doc",
        info_from="Freedom operator",
        rationale="Incomplete proposal",
        authority_basis="R0",
        decided_at=DECIDED_AT,
    )
    assert decision.info_requested == "Need full scope doc"
    assert decision.info_from == "Freedom operator"


def test_request_more_info_wrong_state_raises():
    action = create_action(
        mission_id="mission-abc123def456",
        action_type="test",
        title="Test",
        actor="Adam",
    )
    with raises(ApprovalError, match="approval_requested"):
        request_more_info(
            action,
            requester="Adam",
            info_requested="Need scope",
            info_from="proposer",
            rationale="Unclear",
            authority_basis="R0",
            decided_at=DECIDED_AT,
        )


def test_request_more_info_empty_info_requested_raises():
    action = make_approval_requested_action()
    with raises(ApprovalError, match="info_requested"):
        request_more_info(
            action,
            requester="Adam",
            info_requested="",
            info_from="proposer",
            rationale="Unclear",
            authority_basis="R0",
            decided_at=DECIDED_AT,
        )


def test_request_more_info_empty_info_from_raises():
    action = make_approval_requested_action()
    with raises(ApprovalError, match="info_from"):
        request_more_info(
            action,
            requester="Adam",
            info_requested="Need scope",
            info_from="",
            rationale="Unclear",
            authority_basis="R0",
            decided_at=DECIDED_AT,
        )


# ── ApprovalDecision roundtrip ───────────────────────────────────────────────

def test_approval_decision_to_dict_from_dict_roundtrip():
    action = make_approval_requested_action()
    _, decision = approve_action(
        action,
        approver="Adam Goodwin",
        rationale="All good",
        authority_basis="R0",
        decided_at=DECIDED_AT,
    )
    roundtripped = ApprovalDecision.from_dict(decision.to_dict())
    assert roundtripped == decision


def test_hold_decision_roundtrip():
    action = make_approval_requested_action()
    _, decision = hold_action(
        action,
        holder="Adam",
        rationale="Pending review",
        authority_basis="R0",
        decided_at=DECIDED_AT,
        hold_until="2026-06-29T00:00:00-06:00",
    )
    roundtripped = ApprovalDecision.from_dict(decision.to_dict())
    assert roundtripped.hold_until == "2026-06-29T00:00:00-06:00"


def test_more_info_decision_roundtrip():
    action = make_approval_requested_action()
    _, decision = request_more_info(
        action,
        requester="Adam",
        info_requested="Scope doc",
        info_from="Freedom",
        rationale="Missing scope",
        authority_basis="R0",
        decided_at=DECIDED_AT,
    )
    roundtripped = ApprovalDecision.from_dict(decision.to_dict())
    assert roundtripped.info_requested == "Scope doc"
    assert roundtripped.info_from == "Freedom"


# ── validate_approval_decision ───────────────────────────────────────────────

def test_validate_valid_decision_returns_no_errors():
    decision = make_decision()
    assert validate_approval_decision(decision) == []


def test_validate_bad_decision_id_prefix():
    decision = make_decision(decision_id="bad-123")
    errors = validate_approval_decision(decision)
    assert any("aprv-" in e for e in errors)


def test_validate_bad_action_id_prefix():
    decision = make_decision(action_id="bad-123")
    errors = validate_approval_decision(decision)
    assert any("action-" in e for e in errors)


def test_validate_bad_mission_id_prefix():
    decision = make_decision(mission_id="bad-123")
    errors = validate_approval_decision(decision)
    assert any("mission-" in e for e in errors)


def test_validate_invalid_decision_type():
    decision = make_decision(decision_type="unknown_type")
    errors = validate_approval_decision(decision)
    assert any("decision_type" in e for e in errors)


def test_validate_empty_decided_by():
    decision = make_decision(decided_by="")
    errors = validate_approval_decision(decision)
    assert any("decided_by" in e for e in errors)


def test_validate_bad_envelope_prefix():
    decision = make_decision(envelope_id="bad-env-prefix")
    errors = validate_approval_decision(decision)
    assert any("env-" in e for e in errors)


def test_validate_more_info_missing_info_requested():
    decision = make_decision(
        decision_type=ApprovalDecisionType.MORE_INFO_REQUESTED.value,
        info_requested=None,
        info_from="Freedom",
    )
    errors = validate_approval_decision(decision)
    assert any("info_requested" in e for e in errors)


def test_validate_more_info_missing_info_from():
    decision = make_decision(
        decision_type=ApprovalDecisionType.MORE_INFO_REQUESTED.value,
        info_requested="Need scope",
        info_from=None,
    )
    errors = validate_approval_decision(decision)
    assert any("info_from" in e for e in errors)


# ── ApprovalStore ────────────────────────────────────────────────────────────

def test_approval_store_write_and_read_roundtrip():
    action = make_approval_requested_action()
    _, decision = approve_action(
        action,
        approver="Adam Goodwin",
        rationale="Approved for local dry-run.",
        authority_basis="R0",
        decided_at=DECIDED_AT,
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ApprovalStore(tmpdir)
        path = store.write(decision)
        assert path.exists()
        loaded = store.read(decision.decision_id)
        assert loaded == decision


def test_approval_store_exists():
    action = make_approval_requested_action()
    _, decision = approve_action(
        action,
        approver="Adam",
        rationale="OK",
        authority_basis="R0",
        decided_at=DECIDED_AT,
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ApprovalStore(tmpdir)
        assert not store.exists(decision.decision_id)
        store.write(decision)
        assert store.exists(decision.decision_id)


def test_approval_store_lists_by_trace():
    action = make_approval_requested_action(cns_trace_id="cns-20260701-aabbccddeeff")
    _, decision = approve_action(
        action,
        approver="Adam",
        rationale="OK",
        authority_basis="R0",
        decided_at=DECIDED_AT,
        cns_trace_id="cns-20260701-aabbccddeeff",
    )
    other_action = make_approval_requested_action(cns_trace_id="cns-20260701-ffeeddccbbaa")
    _, other = approve_action(
        other_action,
        approver="Adam",
        rationale="OK",
        authority_basis="R0",
        decided_at=DECIDED_AT,
        cns_trace_id="cns-20260701-ffeeddccbbaa",
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ApprovalStore(tmpdir)
        store.write(decision)
        store.write(other)

        refs = store.list_by_trace("cns-20260701-aabbccddeeff")

        assert refs == (decision,)


def test_approval_store_rejects_unsafe_id():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ApprovalStore(tmpdir)
        with raises(ValueError, match="safe"):
            store.read("../aprv-bad")


def test_approval_store_json_is_readable():
    action = make_approval_requested_action()
    _, decision = reject_action(
        action,
        rejecter="Adam",
        rationale="Scope mismatch",
        authority_basis="R0",
        decided_at=DECIDED_AT,
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ApprovalStore(tmpdir)
        path = store.write(decision)
        raw = json.loads(path.read_text(encoding="utf-8"))
        assert raw["decision_type"] == "rejected"
        assert raw["decided_by"] == "Adam"


def test_approval_store_creates_directories():
    action = make_approval_requested_action()
    _, decision = approve_action(
        action,
        approver="Adam",
        rationale="OK",
        authority_basis="R0",
        decided_at=DECIDED_AT,
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        nested_path = os.path.join(tmpdir, "approvals", "local")
        store = ApprovalStore(nested_path)
        store.write(decision)
        assert store.exists(decision.decision_id)


def test_approval_store_rejects_invalid_decision():
    bad_decision = make_decision(decision_id="bad-prefix")
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ApprovalStore(tmpdir)
        with raises(ValueError, match="invalid"):
            store.write(bad_decision)


# ── no HTTP / transport dependencies ────────────────────────────────────────

def test_no_http_transport_imports():
    import ast
    import gail_ai_operating_system.approval_actions as mod
    source = open(mod.__file__).read()
    tree = ast.parse(source)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split(".")[0])
    http_libs = {"fastapi", "httpx", "requests", "aiohttp", "flask", "starlette"}
    found = http_libs & set(imports)
    assert not found, f"HTTP transport imports found: {found}"
