"""Tests for OperatingKnowledgePacket, OkpRecordType, and EvidencePacketToOkpConverter."""

import pytest
from datetime import datetime, timezone

from gail_ai_operating_system.operating_knowledge import (
    OkpRecordType,
    OperatingKnowledgePacket,
    EvidencePacketToOkpConverter,
    create_operating_knowledge_packet,
    _compute_fingerprint,
)
from gail_ai_operating_system.evidence_packet import create_evidence_packet


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now() -> datetime:
    return datetime.now(timezone.utc)


def _make_okp(**overrides):
    defaults = dict(
        okp_id="okp-abc123def456",
        source_system="gail-os",
        source_ref="reports/daily-update",
        record_type=OkpRecordType.EVIDENCE_CREATED,
        summary="A test signal summary",
        authority_level="R1",
        autonomy_level="A1",
        risk_tier=2,
        data_classification="internal",
        status="observed",
        created_at=_now(),
        observed_at=_now(),
        confidence=0.8,
        fingerprint="abc123def456abc123def456abc12345",
        raw_payload_retained=False,
    )
    defaults.update(overrides)
    return OperatingKnowledgePacket(**defaults)


def _make_evidence():
    return create_evidence_packet(
        mission_id="mission-test001",
        action_id="action-test001",
        actor="test-agent",
        action_type="planner.task.create",
        authority_basis="R1 auto-approved",
        result="success",
        created_at="2026-06-28T12:00:00+00:00",
        execution_mode="dry-run",
        outcome_summary="Created test task in Planner (dry-run)",
    )


# ---------------------------------------------------------------------------
# OkpRecordType enum
# ---------------------------------------------------------------------------

def test_okp_record_type_has_18_values():
    assert len(OkpRecordType) == 18


def test_okp_record_type_all_values():
    expected = {
        "action.validated",
        "action.blocked",
        "authority.override_requested",
        "evidence.created",
        "mission.created",
        "mission.reviewed",
        "graph.relationship_detected",
        "graph.claim_stale_candidate",
        "m365.signal_observed",
        "m365.action_log_observed",
        "freedom.brief_created",
        "build.branch_abandoned",
        "build.blocker_detected",
        "capability.gap_detected",
        "charter.proposed",
        "charter.executed",
        "gravity.calibration_proposed",
    }
    actual = {rt.value for rt in OkpRecordType}
    assert actual == expected


def test_okp_record_type_is_str_enum():
    assert OkpRecordType.EVIDENCE_CREATED == "evidence.created"
    assert isinstance(OkpRecordType.EVIDENCE_CREATED, str)


def test_okp_record_type_action_lifecycle():
    assert OkpRecordType.ACTION_VALIDATED == "action.validated"
    assert OkpRecordType.ACTION_BLOCKED == "action.blocked"


def test_okp_record_type_charter_types():
    assert OkpRecordType.CHARTER_PROPOSED == "charter.proposed"
    assert OkpRecordType.CHARTER_EXECUTED == "charter.executed"


def test_okp_record_type_gravity_calibration():
    assert OkpRecordType.GRAVITY_CALIBRATION == "gravity.calibration_proposed"


# ---------------------------------------------------------------------------
# Schema construction
# ---------------------------------------------------------------------------

def test_okp_constructs_with_all_required_fields():
    okp = _make_okp()
    assert okp.okp_id == "okp-abc123def456"
    assert okp.source_system == "gail-os"
    assert okp.record_type == OkpRecordType.EVIDENCE_CREATED
    assert okp.confidence == 0.8
    assert okp.raw_payload_retained is False


def test_okp_optional_links_default_to_none():
    okp = _make_okp()
    assert okp.related_mission_id is None
    assert okp.related_action_id is None
    assert okp.related_evidence_id is None
    assert okp.related_connector_id is None
    assert okp.related_agent_id is None


def test_okp_gravity_scores_default_to_none():
    okp = _make_okp()
    assert okp.gravity_score_l1 is None
    assert okp.gravity_score_l2 is None
    assert okp.gravity_score_used is None


def test_okp_with_optional_links_set():
    okp = _make_okp(
        related_mission_id="mission-001",
        related_evidence_id="evidence-001abc",
        related_action_id="action-001abc",
        related_connector_id="connector-m365",
        related_agent_id="agent-gail",
    )
    assert okp.related_mission_id == "mission-001"
    assert okp.related_evidence_id == "evidence-001abc"
    assert okp.related_action_id == "action-001abc"
    assert okp.related_connector_id == "connector-m365"
    assert okp.related_agent_id == "agent-gail"


def test_okp_with_gravity_scores_set():
    okp = _make_okp(gravity_score_l1=0.65, gravity_score_l2=0.72, gravity_score_used=0.72)
    assert okp.gravity_score_l1 == 0.65
    assert okp.gravity_score_l2 == 0.72
    assert okp.gravity_score_used == 0.72


# ---------------------------------------------------------------------------
# Validation: okp_id prefix
# ---------------------------------------------------------------------------

def test_okp_id_missing_prefix_raises():
    with pytest.raises(ValueError, match="okp-"):
        _make_okp(okp_id="bad-id-123")


# ---------------------------------------------------------------------------
# Validation: raw_payload_retained
# ---------------------------------------------------------------------------

def test_raw_payload_retained_true_raises():
    with pytest.raises(ValueError, match="raw_payload_retained"):
        _make_okp(raw_payload_retained=True)


# ---------------------------------------------------------------------------
# Validation: authority_level
# ---------------------------------------------------------------------------

def test_authority_level_valid_range():
    for level in ["R0", "R1", "R2", "R3", "R4", "R5"]:
        okp = _make_okp(authority_level=level)
        assert okp.authority_level == level


def test_authority_level_invalid_raises():
    with pytest.raises(ValueError, match="authority_level"):
        _make_okp(authority_level="R6")


def test_authority_level_empty_raises():
    with pytest.raises(ValueError, match="authority_level"):
        _make_okp(authority_level="")


# ---------------------------------------------------------------------------
# Validation: autonomy_level
# ---------------------------------------------------------------------------

def test_autonomy_level_valid_range():
    for level in ["A0", "A1", "A2", "A3", "A4", "A5", "A6"]:
        okp = _make_okp(autonomy_level=level)
        assert okp.autonomy_level == level


def test_autonomy_level_invalid_raises():
    with pytest.raises(ValueError, match="autonomy_level"):
        _make_okp(autonomy_level="A7")


# ---------------------------------------------------------------------------
# Validation: risk_tier
# ---------------------------------------------------------------------------

def test_risk_tier_valid_range():
    for tier in [1, 2, 3, 4, 5]:
        okp = _make_okp(risk_tier=tier)
        assert okp.risk_tier == tier


def test_risk_tier_zero_raises():
    with pytest.raises(ValueError, match="risk_tier"):
        _make_okp(risk_tier=0)


def test_risk_tier_six_raises():
    with pytest.raises(ValueError, match="risk_tier"):
        _make_okp(risk_tier=6)


# ---------------------------------------------------------------------------
# Validation: data_classification
# ---------------------------------------------------------------------------

def test_data_classification_valid_values():
    for cls in ["public", "internal", "synthetic", "restricted"]:
        okp = _make_okp(data_classification=cls)
        assert okp.data_classification == cls


def test_data_classification_invalid_raises():
    with pytest.raises(ValueError, match="data_classification"):
        _make_okp(data_classification="confidential")


# ---------------------------------------------------------------------------
# Validation: confidence
# ---------------------------------------------------------------------------

def test_confidence_boundary_values():
    for val in [0.0, 0.5, 1.0]:
        okp = _make_okp(confidence=val)
        assert okp.confidence == val


def test_confidence_below_zero_raises():
    with pytest.raises(ValueError, match="confidence"):
        _make_okp(confidence=-0.1)


def test_confidence_above_one_raises():
    with pytest.raises(ValueError, match="confidence"):
        _make_okp(confidence=1.01)


# ---------------------------------------------------------------------------
# Validation: summary length
# ---------------------------------------------------------------------------

def test_summary_at_max_length_ok():
    okp = _make_okp(summary="x" * 1000)
    assert len(okp.summary) == 1000


def test_summary_exceeds_max_length_raises():
    with pytest.raises(ValueError, match="summary"):
        _make_okp(summary="x" * 1001)


# ---------------------------------------------------------------------------
# Validation: unsafe source_ref
# ---------------------------------------------------------------------------

def test_unsafe_source_ref_dotenv_raises():
    with pytest.raises(ValueError, match="unsafe"):
        _make_okp(source_ref=".env")


def test_unsafe_source_ref_dotenv_in_path_raises():
    with pytest.raises(ValueError, match="unsafe"):
        _make_okp(source_ref="config/.env.production")


def test_unsafe_source_ref_secret_raises():
    with pytest.raises(ValueError, match="unsafe"):
        _make_okp(source_ref="reports/secret-config")


def test_unsafe_source_ref_token_raises():
    with pytest.raises(ValueError, match="unsafe"):
        _make_okp(source_ref="auth/token-store")


def test_unsafe_source_ref_password_raises():
    with pytest.raises(ValueError, match="unsafe"):
        _make_okp(source_ref="config/password.yaml")


def test_unsafe_source_ref_absolute_unix_path_raises():
    with pytest.raises(ValueError, match="unsafe"):
        _make_okp(source_ref="/etc/passwd")


def test_unsafe_source_ref_absolute_windows_path_raises():
    with pytest.raises(ValueError, match="unsafe"):
        _make_okp(source_ref="C:/Users/data")


def test_safe_source_ref_passes():
    okp = _make_okp(source_ref="reports/daily-update-2026-06-28")
    assert okp.source_ref == "reports/daily-update-2026-06-28"


def test_evidence_id_source_ref_passes():
    # evidence- prefixed IDs must not be rejected
    okp = _make_okp(source_ref="evidence-abc123def456")
    assert okp.source_ref == "evidence-abc123def456"


# ---------------------------------------------------------------------------
# Fingerprint determinism
# ---------------------------------------------------------------------------

def test_fingerprint_determinism():
    fp1 = _compute_fingerprint("ref-abc", "evidence.created", "summary text")
    fp2 = _compute_fingerprint("ref-abc", "evidence.created", "summary text")
    assert fp1 == fp2


def test_fingerprint_changes_with_different_source_ref():
    fp1 = _compute_fingerprint("ref-abc", "evidence.created", "summary text")
    fp2 = _compute_fingerprint("ref-xyz", "evidence.created", "summary text")
    assert fp1 != fp2


def test_fingerprint_changes_with_different_summary():
    fp1 = _compute_fingerprint("ref-abc", "evidence.created", "summary A")
    fp2 = _compute_fingerprint("ref-abc", "evidence.created", "summary B")
    assert fp1 != fp2


def test_fingerprint_is_32_chars():
    fp = _compute_fingerprint("ref-abc", "evidence.created", "summary text")
    assert len(fp) == 32


# ---------------------------------------------------------------------------
# create_operating_knowledge_packet factory
# ---------------------------------------------------------------------------

def test_factory_assigns_okp_id_and_fingerprint():
    okp = create_operating_knowledge_packet(
        source_system="gail-os",
        source_ref="reports/test-signal",
        record_type=OkpRecordType.MISSION_CREATED,
        summary="Test mission created",
        authority_level="R2",
        autonomy_level="A2",
        risk_tier=3,
        data_classification="internal",
        confidence=0.75,
    )
    assert okp.okp_id.startswith("okp-")
    assert len(okp.fingerprint) == 32
    assert okp.raw_payload_retained is False
    assert okp.status == "observed"


def test_factory_fingerprint_is_deterministic_for_same_inputs():
    kwargs = dict(
        source_system="gail-os",
        source_ref="reports/determinism-check",
        record_type=OkpRecordType.EVIDENCE_CREATED,
        summary="Identical summary",
        authority_level="R1",
        autonomy_level="A1",
        risk_tier=1,
        data_classification="internal",
        confidence=0.5,
    )
    okp1 = create_operating_knowledge_packet(**kwargs)
    okp2 = create_operating_knowledge_packet(**kwargs)
    assert okp1.fingerprint == okp2.fingerprint
    assert okp1.okp_id != okp2.okp_id  # Different UUIDs


def test_factory_rejects_unsafe_source_ref():
    with pytest.raises(ValueError, match="unsafe"):
        create_operating_knowledge_packet(
            source_system="gail-os",
            source_ref="/etc/secret",
            record_type=OkpRecordType.MISSION_CREATED,
            summary="should fail",
            authority_level="R1",
            autonomy_level="A1",
            risk_tier=1,
            data_classification="internal",
            confidence=0.5,
        )


# ---------------------------------------------------------------------------
# EvidencePacketToOkpConverter
# ---------------------------------------------------------------------------

def test_converter_produces_valid_okp():
    ep = _make_evidence()
    okp = EvidencePacketToOkpConverter.convert(ep)
    assert okp.okp_id.startswith("okp-")
    assert okp.record_type == OkpRecordType.EVIDENCE_CREATED
    assert okp.related_evidence_id == ep.evidence_id
    assert okp.related_mission_id == ep.mission_id
    assert okp.related_action_id == ep.action_id
    assert okp.raw_payload_retained is False


def test_converter_sets_source_ref_to_evidence_id():
    ep = _make_evidence()
    okp = EvidencePacketToOkpConverter.convert(ep)
    assert okp.source_ref == ep.evidence_id


def test_converter_sets_source_system():
    ep = _make_evidence()
    okp = EvidencePacketToOkpConverter.convert(ep)
    assert okp.source_system == "gail-os-evidence"


def test_converter_sets_data_classification_internal():
    ep = _make_evidence()
    okp = EvidencePacketToOkpConverter.convert(ep)
    assert okp.data_classification == "internal"


def test_converter_maps_outcome_summary():
    ep = _make_evidence()
    okp = EvidencePacketToOkpConverter.convert(ep)
    assert ep.outcome_summary in okp.summary


def test_converter_parses_iso_created_at():
    ep = _make_evidence()
    okp = EvidencePacketToOkpConverter.convert(ep)
    assert isinstance(okp.observed_at, datetime)
    assert okp.observed_at.year == 2026
    assert okp.observed_at.month == 6
    assert okp.observed_at.day == 28


def test_converter_caps_summary_at_1000_chars():
    ep = create_evidence_packet(
        mission_id="mission-long001",
        action_id="action-long001",
        actor="test-agent",
        action_type="test.action",
        authority_basis="R1",
        result="success",
        created_at="2026-06-28T12:00:00+00:00",
        outcome_summary="x" * 2000,
    )
    okp = EvidencePacketToOkpConverter.convert(ep)
    assert len(okp.summary) <= 1000


def test_converter_fingerprint_is_deterministic_for_same_evidence():
    ep = _make_evidence()
    okp1 = EvidencePacketToOkpConverter.convert(ep)
    okp2 = EvidencePacketToOkpConverter.convert(ep)
    assert okp1.fingerprint == okp2.fingerprint
    assert okp1.okp_id != okp2.okp_id  # Different UUIDs each call


def test_converter_sets_status_observed():
    ep = _make_evidence()
    okp = EvidencePacketToOkpConverter.convert(ep)
    assert okp.status == "observed"


def test_converter_sets_authority_r1():
    ep = _make_evidence()
    okp = EvidencePacketToOkpConverter.convert(ep)
    assert okp.authority_level == "R1"


# ---------------------------------------------------------------------------
# Package exports
# ---------------------------------------------------------------------------

def test_package_exports_okp_symbols():
    import gail_ai_operating_system as pkg
    assert hasattr(pkg, "OkpRecordType")
    assert hasattr(pkg, "OperatingKnowledgePacket")
    assert hasattr(pkg, "EvidencePacketToOkpConverter")
    assert hasattr(pkg, "create_operating_knowledge_packet")
