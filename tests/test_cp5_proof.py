"""CP-5 Dry-Run Proof — GAIL OS layer.

Demonstrates the GAIL OS segment of the operating knowledge flow:
  Phase 4 EvidencePacket (dry-run M365 Planner task)
    -> EvidencePacketToOkpConverter -> OperatingKnowledgePacket (evidence.created)
    -> OkpStore.save() -> gravity_score_l1 calculated and stored

Uses an isolated temp-dir store; no live HTTP, no M365, no Supabase writes.
"""
from __future__ import annotations

import dataclasses

import pytest

from gail_ai_operating_system.evidence_packet import EvidencePacket
from gail_ai_operating_system.operating_knowledge import (
    EvidencePacketToOkpConverter,
    OkpRecordType,
)
from gail_ai_operating_system.operating_knowledge_store import OkpStore
from gail_ai_operating_system.signal_gravity import SignalGravityL1Calculator

# ---------------------------------------------------------------------------
# Synthetic Phase 4 EvidencePacket — mirrors the CP-4 dry-run M365 Planner proof
# ---------------------------------------------------------------------------

CP4_EVIDENCE = EvidencePacket(
    evidence_id="evidence-cp4-planner-001",
    mission_id="mission-cns-phase4-prove-m365",
    action_id="action-planner-task-write",
    actor="gail-os-a1",
    action_type="planner_task_create",
    authority_basis="R2-connector-registry-dry-run",
    result="success",
    execution_mode="dry-run",
    created_at="2026-06-28T00:00:00+00:00",
    envelope_id="env-cp4-001",
    rollback_note="Dry-run only. No Planner task was actually created.",
    outcome_summary=(
        "CP-4 dry-run: GAIL OS wrote a Planner task record to the OS evidence "
        "store via the M365 connector (dry-run mode). The task content was the "
        "Phase 4 proof-of-concept mission record. No live M365 write occurred. "
        "Evidence verified by Freedom brief inspection."
    ),
)


@pytest.fixture
def tmp_store(tmp_path):
    store = OkpStore(store_path=str(tmp_path))
    calc = SignalGravityL1Calculator(store_path=str(tmp_path))
    return store, calc


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_evidence_packet_converts_to_valid_okp(tmp_store):
    """EvidencePacketToOkpConverter produces a valid OKP from CP-4 evidence."""
    _, _ = tmp_store
    okp = EvidencePacketToOkpConverter.convert(CP4_EVIDENCE)
    assert okp.record_type == OkpRecordType.EVIDENCE_CREATED
    assert okp.okp_id.startswith("okp-")
    assert okp.raw_payload_retained is False
    assert len(okp.fingerprint) == 32


def test_converted_okp_links_to_source_evidence(tmp_store):
    """Converted OKP carries source_ref and all related IDs from EvidencePacket."""
    _, _ = tmp_store
    okp = EvidencePacketToOkpConverter.convert(CP4_EVIDENCE)
    assert okp.related_evidence_id == "evidence-cp4-planner-001"
    assert okp.source_ref == "evidence-cp4-planner-001"
    assert okp.related_mission_id == "mission-cns-phase4-prove-m365"
    assert okp.related_action_id == "action-planner-task-write"


def test_l1_gravity_score_in_valid_range(tmp_store):
    """Signal Gravity L1 score for the CP-4 OKP is within [0.0, 1.0]."""
    _, calc = tmp_store
    okp = EvidencePacketToOkpConverter.convert(CP4_EVIDENCE)
    score = calc.calculate(okp)
    assert 0.0 <= score <= 1.0


def test_l1_weights_sum_to_one(tmp_store):
    """Default weight config file sums to exactly 1.0."""
    _, calc = tmp_store
    weights = calc.load_weights()
    assert abs(sum(weights.values()) - 1.0) < 0.001


def test_l1_weights_cover_all_9_factors(tmp_store):
    """Weight config has exactly the 9 required Signal Gravity factors."""
    _, calc = tmp_store
    weights = calc.load_weights()
    expected = {
        "recent_evidence", "unresolved_risk", "operational_value",
        "repeated_recurrence", "pending_authority", "connected_blockers",
        "client_impact", "prior_failure_relation", "strategic_alignment",
    }
    assert set(weights.keys()) == expected


def test_okp_stored_and_retrieved_with_l1_gravity(tmp_store):
    """OKP is saved to OkpStore with gravity_score_l1 and can be retrieved."""
    store, calc = tmp_store
    raw = EvidencePacketToOkpConverter.convert(CP4_EVIDENCE)
    score = calc.calculate(raw)
    okp = dataclasses.replace(raw, gravity_score_l1=score)
    stored_id = store.save(okp)
    retrieved = store.get(stored_id)
    assert retrieved is not None
    assert retrieved.gravity_score_l1 is not None
    assert 0.0 <= retrieved.gravity_score_l1 <= 1.0


def test_list_by_record_type_finds_stored_okp(tmp_store):
    """OkpStore.list_by_record_type returns the stored evidence.created OKP."""
    store, calc = tmp_store
    raw = EvidencePacketToOkpConverter.convert(CP4_EVIDENCE)
    score = calc.calculate(raw)
    okp = dataclasses.replace(raw, gravity_score_l1=score)
    store.save(okp)
    results = store.list_by_record_type("evidence.created")
    assert len(results) == 1
    assert results[0].related_evidence_id == "evidence-cp4-planner-001"


def test_okp_summary_contains_cp4_context(tmp_store):
    """OKP summary is sourced from EvidencePacket.outcome_summary."""
    _, _ = tmp_store
    okp = EvidencePacketToOkpConverter.convert(CP4_EVIDENCE)
    assert "CP-4 dry-run" in okp.summary


def test_fingerprint_is_deterministic_across_conversions(tmp_store):
    """Two conversions of the same EvidencePacket produce identical fingerprints."""
    _, _ = tmp_store
    okp1 = EvidencePacketToOkpConverter.convert(CP4_EVIDENCE)
    okp2 = EvidencePacketToOkpConverter.convert(CP4_EVIDENCE)
    assert okp1.fingerprint == okp2.fingerprint


def test_proof_chain_fields_are_complete(tmp_store):
    """Stored OKP contains all Synaptic Proof Chain L1 fields."""
    store, calc = tmp_store
    raw = EvidencePacketToOkpConverter.convert(CP4_EVIDENCE)
    score = calc.calculate(raw)
    okp = dataclasses.replace(raw, gravity_score_l1=score)
    store.save(okp)
    retrieved = store.get(okp.okp_id)
    assert retrieved is not None
    assert retrieved.okp_id.startswith("okp-")
    assert retrieved.source_system == "gail-os-evidence"
    assert retrieved.source_ref == "evidence-cp4-planner-001"
    assert retrieved.record_type == OkpRecordType.EVIDENCE_CREATED
    assert retrieved.authority_level in {"R0", "R1", "R2", "R3", "R4", "R5"}
    assert retrieved.fingerprint != ""
    assert retrieved.gravity_score_l1 is not None
    assert retrieved.data_classification in {
        "public", "internal", "synthetic", "restricted"
    }


def test_no_raw_payload_retained(tmp_store):
    """raw_payload_retained is always False on converted OKPs."""
    _, _ = tmp_store
    okp = EvidencePacketToOkpConverter.convert(CP4_EVIDENCE)
    assert okp.raw_payload_retained is False


def test_data_classification_is_internal(tmp_store):
    """EvidencePacket-derived OKPs default to 'internal' data classification."""
    _, _ = tmp_store
    okp = EvidencePacketToOkpConverter.convert(CP4_EVIDENCE)
    assert okp.data_classification == "internal"
