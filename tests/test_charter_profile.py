"""Tests for CharterProfile schema — Chunk 6.1."""

import pytest

from gail_ai_operating_system.charter_profile import CharterProfile, validate_charter_profile


FUTURE_EXPIRY = "2099-12-31T23:59:59Z"
PAST_EXPIRY = "2020-01-01T00:00:00Z"


def _valid_r4() -> CharterProfile:
    return CharterProfile(
        charter_id="charter-r4-001",
        title="Graphify Stale Claim Review",
        authority_level="R4",
        autonomy_level="A3",
        allowed_action_types=("graphify.node.read", "graphify.node.status_update"),
        target_resources="Graphify CNS SQLite OKP nodes age > 7 days OR confidence < 0.4",
        connector_scope=("connector-graphify-internal",),
        agent_scope=("agent-gail-os",),
        max_actions=25,
        expiry=FUTURE_EXPIRY,
        stop_conditions=("delete node", "modify client data", "live M365 write"),
        rollback_path="PATCH /api/v1/okp/{okp_id} with original_status from evidence packet",
        review_cadence="Adam reviews before charter renewal",
        evidence_requirements="evidence.created OKP for each status change",
    )


def _valid_r2() -> CharterProfile:
    return CharterProfile(
        charter_id="charter-r2-001",
        title="Internal Write Charter",
        authority_level="R2",
        autonomy_level="A1",
        allowed_action_types=("okp.create",),
        target_resources="GAIL OS internal OKP store",
        connector_scope=(),
        agent_scope=("agent-gail-os",),
        max_actions=100,
        expiry=FUTURE_EXPIRY,
        stop_conditions=(),
        rollback_path="",
        review_cadence="monthly",
        evidence_requirements="okp_id logged per action",
    )


# --- Construction ---

def test_r4_charter_creates_successfully():
    charter = _valid_r4()
    assert charter.charter_id == "charter-r4-001"
    assert charter.authority_level == "R4"


def test_r2_charter_creates_successfully():
    charter = _valid_r2()
    assert charter.authority_level == "R2"


def test_all_14_fields_present():
    charter = _valid_r4()
    assert charter.charter_id
    assert charter.title
    assert charter.authority_level
    assert charter.autonomy_level
    assert charter.allowed_action_types
    assert charter.target_resources
    assert charter.connector_scope is not None
    assert charter.agent_scope is not None
    assert charter.max_actions
    assert charter.expiry
    assert charter.stop_conditions
    assert charter.rollback_path
    assert charter.review_cadence
    assert charter.evidence_requirements


# --- charter_id prefix ---

def test_charter_id_missing_prefix_fails():
    charter = CharterProfile(
        charter_id="r4-001",
        title="Test",
        authority_level="R4",
        autonomy_level="A3",
        allowed_action_types=("graphify.node.read",),
        target_resources="graphify nodes",
        connector_scope=(),
        agent_scope=(),
        max_actions=10,
        expiry=FUTURE_EXPIRY,
        stop_conditions=("halt on error",),
        rollback_path="revert via API",
        review_cadence="monthly",
        evidence_requirements="evidence packet per action",
    )
    errors = validate_charter_profile(charter)
    assert any("charter-" in e for e in errors)


# --- R5 rejection ---

def test_r5_authority_fails_validation():
    charter = CharterProfile(
        charter_id="charter-r5-attempt",
        title="Attempt R5",
        authority_level="R5",
        autonomy_level="A6",
        allowed_action_types=("anything",),
        target_resources="everything",
        connector_scope=(),
        agent_scope=(),
        max_actions=1,
        expiry=FUTURE_EXPIRY,
        stop_conditions=("stop",),
        rollback_path="none",
        review_cadence="never",
        evidence_requirements="none",
    )
    errors = validate_charter_profile(charter)
    assert any("R5" in e for e in errors)


# --- R4 requirements ---

def test_r4_requires_stop_conditions():
    charter = CharterProfile(
        charter_id="charter-r4-test",
        title="Missing stop conditions",
        authority_level="R4",
        autonomy_level="A3",
        allowed_action_types=("graphify.node.read",),
        target_resources="graphify nodes",
        connector_scope=(),
        agent_scope=(),
        max_actions=10,
        expiry=FUTURE_EXPIRY,
        stop_conditions=(),
        rollback_path="revert via API",
        review_cadence="monthly",
        evidence_requirements="evidence packet per action",
    )
    errors = validate_charter_profile(charter)
    assert any("stop_condition" in e for e in errors)


def test_r4_requires_rollback_path():
    charter = CharterProfile(
        charter_id="charter-r4-test",
        title="Missing rollback",
        authority_level="R4",
        autonomy_level="A3",
        allowed_action_types=("graphify.node.read",),
        target_resources="graphify nodes",
        connector_scope=(),
        agent_scope=(),
        max_actions=10,
        expiry=FUTURE_EXPIRY,
        stop_conditions=("halt on error",),
        rollback_path="",
        review_cadence="monthly",
        evidence_requirements="evidence packet per action",
    )
    errors = validate_charter_profile(charter)
    assert any("rollback_path" in e for e in errors)


def test_r4_with_past_expiry_fails_validation():
    charter = CharterProfile(
        charter_id="charter-r4-test",
        title="Expired charter",
        authority_level="R4",
        autonomy_level="A3",
        allowed_action_types=("graphify.node.read",),
        target_resources="graphify nodes",
        connector_scope=(),
        agent_scope=(),
        max_actions=10,
        expiry=PAST_EXPIRY,
        stop_conditions=("halt on error",),
        rollback_path="revert via API",
        review_cadence="monthly",
        evidence_requirements="evidence packet per action",
    )
    errors = validate_charter_profile(charter)
    assert any("expiry" in e.lower() for e in errors)


def test_valid_r4_passes_validation():
    errors = validate_charter_profile(_valid_r4())
    assert errors == []


# --- is_expired() ---

def test_is_expired_returns_false_for_future_expiry():
    assert _valid_r4().is_expired() is False


def test_is_expired_returns_true_for_past_expiry():
    charter = CharterProfile(
        charter_id="charter-r4-expired",
        title="Expired",
        authority_level="R4",
        autonomy_level="A3",
        allowed_action_types=("graphify.node.read",),
        target_resources="graphify nodes",
        connector_scope=(),
        agent_scope=(),
        max_actions=10,
        expiry=PAST_EXPIRY,
        stop_conditions=("halt",),
        rollback_path="revert",
        review_cadence="monthly",
        evidence_requirements="evidence",
    )
    assert charter.is_expired() is True


def test_is_expired_returns_true_for_unparseable_expiry():
    charter = CharterProfile(
        charter_id="charter-test",
        title="Bad expiry",
        authority_level="R2",
        autonomy_level="A1",
        allowed_action_types=("okp.create",),
        target_resources="internal",
        connector_scope=(),
        agent_scope=(),
        max_actions=10,
        expiry="not-a-date",
        stop_conditions=(),
        rollback_path="",
        review_cadence="monthly",
        evidence_requirements="evidence",
    )
    assert charter.is_expired() is True


# --- to_dict / from_dict round-trip ---

def test_round_trip_via_dict():
    original = _valid_r4()
    restored = CharterProfile.from_dict(original.to_dict())
    assert restored.charter_id == original.charter_id
    assert restored.authority_level == original.authority_level
    assert restored.stop_conditions == original.stop_conditions
    assert restored.max_actions == original.max_actions
    assert restored.expiry == original.expiry


# --- Other field validation ---

def test_empty_allowed_action_types_fails():
    charter = CharterProfile(
        charter_id="charter-test",
        title="No actions",
        authority_level="R2",
        autonomy_level="A1",
        allowed_action_types=(),
        target_resources="internal",
        connector_scope=(),
        agent_scope=(),
        max_actions=10,
        expiry=FUTURE_EXPIRY,
        stop_conditions=(),
        rollback_path="",
        review_cadence="monthly",
        evidence_requirements="evidence",
    )
    errors = validate_charter_profile(charter)
    assert any("allowed_action_types" in e for e in errors)


def test_max_actions_zero_fails():
    charter = CharterProfile(
        charter_id="charter-test",
        title="Zero actions",
        authority_level="R2",
        autonomy_level="A1",
        allowed_action_types=("okp.create",),
        target_resources="internal",
        connector_scope=(),
        agent_scope=(),
        max_actions=0,
        expiry=FUTURE_EXPIRY,
        stop_conditions=(),
        rollback_path="",
        review_cadence="monthly",
        evidence_requirements="evidence",
    )
    errors = validate_charter_profile(charter)
    assert any("max_actions" in e for e in errors)


def test_invalid_authority_level_fails():
    charter = CharterProfile(
        charter_id="charter-test",
        title="Bad authority",
        authority_level="R9",
        autonomy_level="A1",
        allowed_action_types=("okp.create",),
        target_resources="internal",
        connector_scope=(),
        agent_scope=(),
        max_actions=10,
        expiry=FUTURE_EXPIRY,
        stop_conditions=(),
        rollback_path="",
        review_cadence="monthly",
        evidence_requirements="evidence",
    )
    errors = validate_charter_profile(charter)
    assert any("authority_level" in e for e in errors)


def test_invalid_autonomy_level_fails():
    charter = CharterProfile(
        charter_id="charter-test",
        title="Bad autonomy",
        authority_level="R2",
        autonomy_level="A9",
        allowed_action_types=("okp.create",),
        target_resources="internal",
        connector_scope=(),
        agent_scope=(),
        max_actions=10,
        expiry=FUTURE_EXPIRY,
        stop_conditions=(),
        rollback_path="",
        review_cadence="monthly",
        evidence_requirements="evidence",
    )
    errors = validate_charter_profile(charter)
    assert any("autonomy_level" in e for e in errors)


def test_envelope_id_is_optional_and_roundtrips():
    charter = _valid_r4()
    assert charter.envelope_id is None
    with_envelope = CharterProfile.from_dict({**charter.to_dict(), "envelope_id": "env-001"})
    assert with_envelope.envelope_id == "env-001"


def test_r4_invalid_expiry_format_fails_validation():
    charter = CharterProfile(
        charter_id="charter-r4-test",
        title="Bad expiry format",
        authority_level="R4",
        autonomy_level="A3",
        allowed_action_types=("graphify.node.read",),
        target_resources="graphify nodes",
        connector_scope=(),
        agent_scope=(),
        max_actions=10,
        expiry="tomorrow",
        stop_conditions=("halt on error",),
        rollback_path="revert via API",
        review_cadence="monthly",
        evidence_requirements="evidence packet per action",
    )
    errors = validate_charter_profile(charter)
    assert any("expiry" in e.lower() for e in errors)
