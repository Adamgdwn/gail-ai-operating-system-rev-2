"""Tests for R4 Dry-Run Simulation — Chunk 6.4.

All tests use synthetic data only. No live system calls. No datetime.now().
"""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

import pytest

from gail_ai_operating_system.r4_dry_run_simulator import (
    R4DryRunResult,
    StaleClaimCandidate,
    build_freedom_brief,
    build_dry_run_preview,
    build_r4_001_charter,
    generate_stale_claim_candidates,
    produce_evidence_packet,
    produce_okp,
    produce_rollback_data,
    run_r4_dry_run_simulation,
    validate_charter_authority,
)
from gail_ai_operating_system.charter_profile import validate_charter_profile

FIXED_TS = "2026-06-28T12:00:00Z"
PAST_EXPIRY = "2020-01-01T00:00:00Z"


# ---------------------------------------------------------------------------
# 1. test_build_r4_001_charter_is_valid
# ---------------------------------------------------------------------------

def test_build_r4_001_charter_is_valid() -> None:
    charter = build_r4_001_charter()
    errors = validate_charter_profile(charter)
    assert errors == [], f"Expected no errors, got: {errors}"


# ---------------------------------------------------------------------------
# 2. test_build_r4_001_charter_not_expired
# ---------------------------------------------------------------------------

def test_build_r4_001_charter_not_expired() -> None:
    charter = build_r4_001_charter()
    assert charter.is_expired() is False


# ---------------------------------------------------------------------------
# 3. test_generate_stale_claim_candidates_count
# ---------------------------------------------------------------------------

def test_generate_stale_claim_candidates_count() -> None:
    candidates = generate_stale_claim_candidates(7)
    assert len(candidates) == 7


# ---------------------------------------------------------------------------
# 4. test_generate_stale_claim_candidates_all_have_review_required
# ---------------------------------------------------------------------------

def test_generate_stale_claim_candidates_all_have_review_required() -> None:
    candidates = generate_stale_claim_candidates(5)
    for c in candidates:
        assert c.proposed_status == "review_required", (
            f"{c.entity_id} has proposed_status={c.proposed_status!r}"
        )


# ---------------------------------------------------------------------------
# 5. test_validate_charter_authority_valid
# ---------------------------------------------------------------------------

def test_validate_charter_authority_valid() -> None:
    charter = build_r4_001_charter()
    is_valid, errors = validate_charter_authority(charter)
    assert is_valid is True
    assert errors == []


# ---------------------------------------------------------------------------
# 6. test_validate_charter_authority_expired_fails
# ---------------------------------------------------------------------------

def test_validate_charter_authority_expired_fails() -> None:
    charter = build_r4_001_charter(expiry=PAST_EXPIRY)
    is_valid, errors = validate_charter_authority(charter)
    assert is_valid is False
    assert len(errors) >= 1


# ---------------------------------------------------------------------------
# 7. test_build_dry_run_preview_structure
# ---------------------------------------------------------------------------

def test_build_dry_run_preview_structure() -> None:
    candidates = generate_stale_claim_candidates(3)
    preview = build_dry_run_preview(candidates)
    assert len(preview) == 3
    for entry in preview:
        assert "entity_id" in entry
        assert "from_status" in entry
        assert "to_status" in entry
        assert entry["dry_run"] is True


# ---------------------------------------------------------------------------
# 8. test_produce_evidence_packet_fields
# ---------------------------------------------------------------------------

def test_produce_evidence_packet_fields() -> None:
    charter = build_r4_001_charter()
    candidates = generate_stale_claim_candidates(5)
    ep = produce_evidence_packet(charter, candidates, FIXED_TS)
    assert ep.execution_mode == "dry-run"
    assert ep.action_type == "graphify.stale_claim.review"
    assert ep.evidence_id.startswith("evidence-")
    assert ep.mission_id.startswith("mission-")
    assert ep.action_id.startswith("action-")


# ---------------------------------------------------------------------------
# 9. test_produce_okp_record_type
# ---------------------------------------------------------------------------

def test_produce_okp_record_type() -> None:
    charter = build_r4_001_charter()
    candidates = generate_stale_claim_candidates(5)
    ep = produce_evidence_packet(charter, candidates, FIXED_TS)
    okp = produce_okp(charter, candidates, ep, FIXED_TS)
    assert okp["record_type"] == "charter.executed"
    assert okp["status"] == "observed"


# ---------------------------------------------------------------------------
# 10. test_produce_rollback_data_all_candidates
# ---------------------------------------------------------------------------

def test_produce_rollback_data_all_candidates() -> None:
    candidates = generate_stale_claim_candidates(5)
    rollback = produce_rollback_data(candidates)
    assert len(rollback) == len(candidates)
    candidate_ids = {c.entity_id for c in candidates}
    for entry in rollback:
        assert entry["entity_id"] in candidate_ids
        assert "prior_status" in entry
        assert entry["prior_status"] in ("stale", "unverified")


# ---------------------------------------------------------------------------
# 11. test_build_freedom_brief_cannot_self_approve
# ---------------------------------------------------------------------------

def test_build_freedom_brief_cannot_self_approve() -> None:
    charter = build_r4_001_charter()
    candidates = generate_stale_claim_candidates(5)
    ep = produce_evidence_packet(charter, candidates, FIXED_TS)
    brief = build_freedom_brief(charter, candidates, ep, FIXED_TS)
    note = brief.get("note", "")
    assert (
        "cannot self-approve" in note or "explicit Adam approval" in note
    ), f"Expected self-approve constraint in note, got: {note!r}"


# ---------------------------------------------------------------------------
# 12. test_run_r4_dry_run_simulation_no_live_mutations
# ---------------------------------------------------------------------------

def test_run_r4_dry_run_simulation_no_live_mutations() -> None:
    result = run_r4_dry_run_simulation(candidate_count=5, simulation_timestamp=FIXED_TS)
    assert result.no_live_mutations is True


# ---------------------------------------------------------------------------
# 13. test_run_r4_dry_run_simulation_all_outputs_present
# ---------------------------------------------------------------------------

def test_run_r4_dry_run_simulation_all_outputs_present() -> None:
    result = run_r4_dry_run_simulation(candidate_count=5, simulation_timestamp=FIXED_TS)
    assert result.charter_valid is True
    assert result.charter_errors == []
    assert len(result.candidates) > 0
    assert len(result.dry_run_preview) > 0
    # evidence_packet is a dict (from .to_dict())
    assert isinstance(result.evidence_packet, dict)
    assert result.evidence_packet.get("execution_mode") == "dry-run"
    # okp is a dict
    assert isinstance(result.okp, dict)
    assert result.okp.get("record_type") == "charter.executed"
    # rollback_data is a list of dicts
    assert isinstance(result.rollback_data, list)
    assert len(result.rollback_data) > 0
    # freedom_brief is a dict
    assert isinstance(result.freedom_brief, dict)
    assert "note" in result.freedom_brief


# ---------------------------------------------------------------------------
# 14. test_run_r4_dry_run_simulation_no_product_repo_changes
# ---------------------------------------------------------------------------

def test_run_r4_dry_run_simulation_no_product_repo_changes() -> None:
    result = run_r4_dry_run_simulation(candidate_count=5, simulation_timestamp=FIXED_TS)
    for candidate in result.candidates:
        assert candidate.source_repo == "graphify-workspace-cockpit", (
            f"Candidate {candidate.entity_id} targets unexpected repo: "
            f"{candidate.source_repo!r}"
        )
