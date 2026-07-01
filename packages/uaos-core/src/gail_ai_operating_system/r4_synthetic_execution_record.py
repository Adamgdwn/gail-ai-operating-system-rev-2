"""R4 synthetic execution-record builder for GAIL AI Operating System Rev 2.

Wraps a synthetic Graphify stale-claim review result in a formal
EvidencePacket and OKP. This records the shape of a future R4 proof path, but
it does not execute external adapters, mutate Graphify, approve R4 live
execution, or create a signed AuthorityEnvelope.

execution_mode = "dry-run", allow_live = False.
No datetime.now() - inject execution_timestamp.
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
class R4SyntheticExecutionRecord:
    """Output of an R4 synthetic execution-record proof."""

    charter_id: str
    charter_valid: bool
    action_count: int
    candidates_reviewed: list[dict]
    evidence_packet: dict          # EvidencePacket.to_dict()
    okp: dict                      # OKP record
    rollback_data: list[dict]
    execution_timestamp: str
    no_live_mutations: bool


def build_synthetic_execution_evidence_packet(
    charter: CharterProfile,
    action_count: int,
    execution_timestamp: str,
    graphify_execution_result: dict,
) -> EvidencePacket:
    """Build a dry-run EvidencePacket for the R4 synthetic record proof."""
    rollback_data = graphify_execution_result.get("rollback_data", [])
    return create_evidence_packet(
        mission_id="mission-r4-001-graphify-stale-claim",
        action_id="action-r4-001-stale-claim-review",
        actor="gail-os-r4-synthetic-recorder",
        action_type="graphify_stale_claim_review",
        authority_basis=(
            "charter-r4-001-graphify-stale-claim [R4/A3] synthetic proof "
            f"record - {action_count} candidates reviewed; no external "
            "mutation approved"
        ),
        result=EvidenceResult.SUCCESS.value,
        execution_mode=ExecutionMode.DRY_RUN.value,
        created_at=execution_timestamp,
        envelope_id=None,
        rollback_note=(
            "Synthetic record only; no external mutation occurred. "
            f"rollback_data describes {len(rollback_data)} entities hypothetically."
        ),
        outcome_summary=(
            f"R4-001 synthetic record: {action_count} stale claims would be "
            "marked review_required if a later signed authority path approved execution."
        ),
        allow_live=False,
    )


def build_synthetic_execution_okp(
    charter: CharterProfile,
    evidence_packet: EvidencePacket,
    graphify_execution_result: dict,
    execution_timestamp: str,
) -> dict:
    """Build an OKP record for the R4 synthetic execution-record proof."""
    action_count = graphify_execution_result.get("action_count", 0)
    date_compact = execution_timestamp[:10].replace("-", "")
    return {
        "okp_id": f"okp-r4-001-synthetic-record-{date_compact}",
        "record_type": "charter.synthetic_execution_recorded",
        "source_system": "gail-os-r4-synthetic-recorder",
        "source_ref": charter.charter_id,
        "summary": (
            f"R4-001 synthetic record: {action_count} candidates would be "
            "marked review_required only after later signed authority approval."
        ),
        "authority_level": "R4",
        "status": "observed",
        "execution_mode": "dry-run",
        "created_at": execution_timestamp,
        "evidence_id": evidence_packet.evidence_id,
    }


def run_r4_synthetic_execution_record(
    graphify_execution_result: dict,
    execution_timestamp: str | None = None,
) -> R4SyntheticExecutionRecord:
    """Run the R4 synthetic execution-record proof end-to-end.

    Accepts a synthetic graphify_execution_result dict, wraps it in a dry-run
    EvidencePacket and OKP, and returns an R4SyntheticExecutionRecord.

    No datetime.now() - defaults to "2026-06-28T00:00:00Z" if not supplied.
    """
    ts = execution_timestamp if execution_timestamp is not None else "2026-06-28T00:00:00Z"

    charter = build_r4_001_charter(expiry="2026-07-12T00:00:00Z")
    charter_valid, charter_errors = validate_charter_authority(charter)
    if not charter_valid:
        raise ValueError(f"Charter authority invalid: {charter_errors}")

    action_count = graphify_execution_result.get("action_count", 0)
    candidates_reviewed = graphify_execution_result.get("candidates_reviewed", [])
    rollback_data = graphify_execution_result.get("rollback_data", [])

    evidence_packet = build_synthetic_execution_evidence_packet(
        charter=charter,
        action_count=action_count,
        execution_timestamp=ts,
        graphify_execution_result=graphify_execution_result,
    )
    okp = build_synthetic_execution_okp(
        charter=charter,
        evidence_packet=evidence_packet,
        graphify_execution_result=graphify_execution_result,
        execution_timestamp=ts,
    )

    return R4SyntheticExecutionRecord(
        charter_id=charter.charter_id,
        charter_valid=charter_valid,
        action_count=action_count,
        candidates_reviewed=candidates_reviewed,
        evidence_packet=evidence_packet.to_dict(),
        okp=okp,
        rollback_data=rollback_data,
        execution_timestamp=ts,
        no_live_mutations=True,
    )


__all__ = [
    "R4SyntheticExecutionRecord",
    "build_synthetic_execution_evidence_packet",
    "build_synthetic_execution_okp",
    "run_r4_synthetic_execution_record",
]
