"""
R4 live executor for GAIL AI Operating System Rev 2.

Wraps graphify-workspace-cockpit charter execution results in a formal
EvidencePacket and OKP. This is the GAIL OS authority layer for live
R4 execution — it does not perform graph mutations directly.

execution_mode = "live", allow_live = True.
No datetime.now() — inject execution_timestamp.
"""
from __future__ import annotations

from dataclasses import dataclass

from .charter_profile import CharterProfile, validate_charter_profile
from .evidence_packet import (
    EvidencePacket,
    EvidenceResult,
    ExecutionMode,
    create_evidence_packet,
)
from .r4_dry_run_simulator import build_r4_001_charter, validate_charter_authority


@dataclass(frozen=True)
class R4LiveResult:
    """Output of a complete R4 live execution. no_live_mutations is always False."""

    charter_id: str
    charter_valid: bool
    action_count: int
    candidates_reviewed: list[dict]
    evidence_packet: dict          # EvidencePacket.to_dict()
    okp: dict                      # OKP record
    rollback_data: list[dict]
    execution_timestamp: str
    no_live_mutations: bool        # always False for live execution


def build_live_evidence_packet(
    charter: CharterProfile,
    action_count: int,
    execution_timestamp: str,
    graphify_execution_result: dict,
) -> EvidencePacket:
    """
    Build a live EvidencePacket for a completed R4 stale-claim review.

    Uses allow_live=True — this is the key gate that differentiates live
    evidence from dry-run evidence.
    """
    rollback_data = graphify_execution_result.get("rollback_data", [])
    return create_evidence_packet(
        mission_id="mission-r4-001-graphify-stale-claim",
        action_id="action-r4-001-stale-claim-review",
        actor="gail-os-r4-executor",
        action_type="graphify_stale_claim_review",
        authority_basis=(
            f"charter-r4-001-graphify-stale-claim [R4/A3] — {action_count} candidates reviewed"
        ),
        result=EvidenceResult.SUCCESS.value,
        execution_mode=ExecutionMode.LIVE.value,
        created_at=execution_timestamp,
        envelope_id=None,
        rollback_note=(
            f"rollback_data: {len(rollback_data)} entities — restore prior_status to revert"
        ),
        outcome_summary=(
            f"R4-001 executed live: {action_count} stale claims marked review_required"
        ),
        allow_live=True,
    )


def build_live_okp(
    charter: CharterProfile,
    evidence_packet: EvidencePacket,
    graphify_execution_result: dict,
    execution_timestamp: str,
) -> dict:
    """
    Build an OKP record for a completed live R4 execution.

    record_type = "charter.executed", execution_mode = "live", status = "observed".
    """
    action_count = graphify_execution_result.get("action_count", 0)
    date_compact = execution_timestamp[:10].replace("-", "")
    return {
        "okp_id": f"okp-r4-001-live-{date_compact}",
        "record_type": "charter.executed",
        "source_system": "gail-os-r4-executor",
        "source_ref": charter.charter_id,
        "summary": (
            f"R4-001 live execution: {action_count} candidates marked review_required."
        ),
        "authority_level": "R4",
        "status": "observed",
        "execution_mode": "live",
        "created_at": execution_timestamp,
        "evidence_id": evidence_packet.evidence_id,
    }


def run_r4_live_execution(
    graphify_execution_result: dict,
    execution_timestamp: str | None = None,
) -> R4LiveResult:
    """
    Run the R4 live execution authority layer end-to-end.

    Accepts a graphify_execution_result dict produced by
    graphify-workspace-cockpit's execute_r4_stale_claim_review, wraps it in
    a validated EvidencePacket and OKP, and returns an R4LiveResult.

    No datetime.now() — defaults to "2026-06-28T00:00:00Z" if not supplied.
    """
    ts = execution_timestamp if execution_timestamp is not None else "2026-06-28T00:00:00Z"

    charter = build_r4_001_charter(expiry="2026-07-12T00:00:00Z")
    charter_valid, charter_errors = validate_charter_authority(charter)
    if not charter_valid:
        raise ValueError(f"Charter authority invalid: {charter_errors}")

    action_count = graphify_execution_result.get("action_count", 0)
    candidates_reviewed = graphify_execution_result.get("candidates_reviewed", [])
    rollback_data = graphify_execution_result.get("rollback_data", [])

    evidence_packet = build_live_evidence_packet(
        charter=charter,
        action_count=action_count,
        execution_timestamp=ts,
        graphify_execution_result=graphify_execution_result,
    )
    okp = build_live_okp(
        charter=charter,
        evidence_packet=evidence_packet,
        graphify_execution_result=graphify_execution_result,
        execution_timestamp=ts,
    )

    return R4LiveResult(
        charter_id=charter.charter_id,
        charter_valid=charter_valid,
        action_count=action_count,
        candidates_reviewed=candidates_reviewed,
        evidence_packet=evidence_packet.to_dict(),
        okp=okp,
        rollback_data=rollback_data,
        execution_timestamp=ts,
        no_live_mutations=False,
    )


__all__ = [
    "R4LiveResult",
    "build_live_evidence_packet",
    "build_live_okp",
    "run_r4_live_execution",
]
