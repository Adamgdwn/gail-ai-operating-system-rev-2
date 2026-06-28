"""
Tests for gail_ai_operating_system.r4_live_executor — R4 live execution authority layer.

No datetime.now() — all timestamps use FIXED_TS.
No HTTP calls — all execution results are synthetic.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

import pytest

from gail_ai_operating_system.evidence_packet import validate_evidence_packet
from gail_ai_operating_system.r4_live_executor import (
    R4LiveResult,
    build_live_evidence_packet,
    build_live_okp,
    run_r4_live_execution,
)
from gail_ai_operating_system.r4_dry_run_simulator import build_r4_001_charter

FIXED_TS = "2026-06-28T12:00:00Z"

SYNTHETIC_GRAPHIFY_RESULT = {
    "charter_id": "charter-r4-001-graphify-stale-claim",
    "action_count": 3,
    "candidates_reviewed": [
        {"entity_id": "claim-r4-001-1", "prior_status": "stale", "new_status": "review_required"},
        {"entity_id": "claim-r4-001-2", "prior_status": "stale", "new_status": "review_required"},
        {"entity_id": "claim-r4-001-3", "prior_status": "stale", "new_status": "review_required"},
    ],
    "rollback_data": [
        {"entity_id": "claim-r4-001-1", "prior_status": "stale"},
        {"entity_id": "claim-r4-001-2", "prior_status": "stale"},
        {"entity_id": "claim-r4-001-3", "prior_status": "stale"},
    ],
    "execution_timestamp": FIXED_TS,
    "charter_scope_verified": True,
}


# ---------------------------------------------------------------------------
# run_r4_live_execution tests
# ---------------------------------------------------------------------------

class TestRunR4LiveExecution:
    def test_no_live_mutations_is_false(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=FIXED_TS)
        assert result.no_live_mutations is False

    def test_evidence_execution_mode_is_live(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=FIXED_TS)
        assert result.evidence_packet["execution_mode"] == "live"

    def test_evidence_result_is_success(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=FIXED_TS)
        assert result.evidence_packet["result"] == "success"

    def test_evidence_id_starts_with_evidence_prefix(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=FIXED_TS)
        assert result.evidence_packet["evidence_id"].startswith("evidence-")

    def test_mission_id_starts_with_mission_prefix(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=FIXED_TS)
        assert result.evidence_packet["mission_id"].startswith("mission-")

    def test_action_id_starts_with_action_prefix(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=FIXED_TS)
        assert result.evidence_packet["action_id"].startswith("action-")

    def test_okp_record_type_is_charter_executed(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=FIXED_TS)
        assert result.okp["record_type"] == "charter.executed"

    def test_okp_execution_mode_is_live(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=FIXED_TS)
        assert result.okp["execution_mode"] == "live"

    def test_rollback_data_passes_through_from_graphify_result(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=FIXED_TS)
        assert result.rollback_data == SYNTHETIC_GRAPHIFY_RESULT["rollback_data"]
        assert len(result.rollback_data) == 3

    def test_charter_valid_is_true(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=FIXED_TS)
        assert result.charter_valid is True

    def test_action_count_from_graphify_result_is_passed_through(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=FIXED_TS)
        assert result.action_count == SYNTHETIC_GRAPHIFY_RESULT["action_count"]

    def test_default_timestamp_used_when_none(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=None)
        assert result.execution_timestamp == "2026-06-28T00:00:00Z"

    def test_result_type_is_r4_live_result(self):
        result = run_r4_live_execution(SYNTHETIC_GRAPHIFY_RESULT, execution_timestamp=FIXED_TS)
        assert isinstance(result, R4LiveResult)


# ---------------------------------------------------------------------------
# build_live_evidence_packet — allow_live=True means validate passes
# ---------------------------------------------------------------------------

class TestBuildLiveEvidencePacket:
    def test_allow_live_true_means_validate_evidence_packet_passes(self):
        charter = build_r4_001_charter(expiry="2026-07-12T00:00:00Z")
        packet = build_live_evidence_packet(
            charter=charter,
            action_count=3,
            execution_timestamp=FIXED_TS,
            graphify_execution_result=SYNTHETIC_GRAPHIFY_RESULT,
        )
        errors = validate_evidence_packet(packet, allow_live=True)
        assert errors == []

    def test_evidence_packet_execution_mode_is_live(self):
        charter = build_r4_001_charter(expiry="2026-07-12T00:00:00Z")
        packet = build_live_evidence_packet(
            charter=charter,
            action_count=3,
            execution_timestamp=FIXED_TS,
            graphify_execution_result=SYNTHETIC_GRAPHIFY_RESULT,
        )
        assert packet.execution_mode == "live"

    def test_evidence_packet_result_is_success(self):
        charter = build_r4_001_charter(expiry="2026-07-12T00:00:00Z")
        packet = build_live_evidence_packet(
            charter=charter,
            action_count=3,
            execution_timestamp=FIXED_TS,
            graphify_execution_result=SYNTHETIC_GRAPHIFY_RESULT,
        )
        assert packet.result == "success"

    def test_rollback_note_contains_entity_count(self):
        charter = build_r4_001_charter(expiry="2026-07-12T00:00:00Z")
        packet = build_live_evidence_packet(
            charter=charter,
            action_count=3,
            execution_timestamp=FIXED_TS,
            graphify_execution_result=SYNTHETIC_GRAPHIFY_RESULT,
        )
        assert "3 entities" in packet.rollback_note

    def test_outcome_summary_contains_action_count(self):
        charter = build_r4_001_charter(expiry="2026-07-12T00:00:00Z")
        packet = build_live_evidence_packet(
            charter=charter,
            action_count=3,
            execution_timestamp=FIXED_TS,
            graphify_execution_result=SYNTHETIC_GRAPHIFY_RESULT,
        )
        assert "3" in packet.outcome_summary
        assert "review_required" in packet.outcome_summary
