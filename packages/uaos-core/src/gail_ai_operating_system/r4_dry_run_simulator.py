"""R4 Dry-Run Simulator for GAIL AI Operating System Rev 2.

Simulates the Graphify stale-claim charter R4-001 without mutating production
graph state. Produces evidence, rollback data, OKP, a Graphify preview, and a
Freedom charter execution brief — all from synthetic data.

NO live HTTP calls. NO live M365 calls. NO product repo changes.
no_live_mutations is always True.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .charter_profile import CharterProfile, validate_charter_profile
from .evidence_packet import EvidencePacket


# ---------------------------------------------------------------------------
# Stale claim data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class StaleClaimCandidate:
    """A synthetic Graphify entity candidate for R4 stale-claim review."""

    entity_id: str         # e.g. "claim-001"
    label: str
    prior_status: str      # the current status BEFORE review (e.g. "stale", "unverified")
    proposed_status: str   # what R4 would mark it as (always "review_required")
    claim_age_days: int
    source_repo: str


@dataclass(frozen=True)
class R4DryRunResult:
    """Output of a complete R4 dry-run simulation. No live mutations occurred."""

    charter_id: str
    charter_valid: bool
    charter_errors: list[str]
    candidates: list[StaleClaimCandidate]
    dry_run_preview: list[dict]      # what would be changed (not committed)
    evidence_packet: dict            # EvidencePacket.to_dict()
    okp: dict                        # OKP record dict
    rollback_data: list[dict]        # [{entity_id, prior_status}]
    freedom_brief: dict              # charter execution summary for Freedom
    simulation_timestamp: str
    no_live_mutations: bool          # always True — safeguard assertion


# ---------------------------------------------------------------------------
# R4-001 charter fixture
# ---------------------------------------------------------------------------

def build_r4_001_charter(expiry: str | None = None) -> CharterProfile:
    """Return the synthetic R4-001 Graphify stale-claim charter fixture."""
    return CharterProfile(
        charter_id="charter-r4-001-graphify-stale-claim",
        title="R4-001: Graphify Stale Claim Internal Review",
        authority_level="R4",
        autonomy_level="A3",
        allowed_action_types=("graphify.stale_claim.review",),
        target_resources="Graphify internal claim entities (stale/unverified only)",
        connector_scope=("graphify-workspace-cockpit",),
        agent_scope=("gail-os-graphify-reviewer",),
        max_actions=25,
        expiry=expiry if expiry is not None else "2099-12-31T23:59:59Z",
        stop_conditions=(
            "Error rate > 20% in any batch",
            "Any live M365 write detected",
            "Any product repo change detected",
            "Evidence packet failure",
            "Adam explicit stop",
        ),
        rollback_path="Revert claim status to prior_status using rollback_data list",
        review_cadence="weekly internal review",
        evidence_requirements=(
            "EvidencePacket with execution_mode=dry-run required for every simulation run"
        ),
    )


# ---------------------------------------------------------------------------
# Simulation functions
# ---------------------------------------------------------------------------

_SYNTHETIC_STATUSES = ["stale", "unverified", "stale", "unverified", "stale"]
_SYNTHETIC_AGES = [30, 60, 90, 120, 180]


def generate_stale_claim_candidates(count: int = 5) -> list[StaleClaimCandidate]:
    """Generate synthetic stale claim candidates. No live reads."""
    candidates = []
    for i in range(1, count + 1):
        idx = (i - 1) % len(_SYNTHETIC_STATUSES)
        entity_id = f"claim-{i:03d}"
        prior_status = _SYNTHETIC_STATUSES[idx]
        age_days = _SYNTHETIC_AGES[idx]
        candidates.append(
            StaleClaimCandidate(
                entity_id=entity_id,
                label=f"Synthetic claim entity {i}",
                prior_status=prior_status,
                proposed_status="review_required",
                claim_age_days=age_days,
                source_repo="graphify-workspace-cockpit",
            )
        )
    return candidates


def validate_charter_authority(charter: CharterProfile) -> tuple[bool, list[str]]:
    """Check charter is valid and not expired. Returns (is_valid, errors)."""
    errors = validate_charter_profile(charter)
    if charter.is_expired():
        errors = list(errors) + ["Charter expiry is in the past."]
    if errors:
        return (False, errors)
    return (True, [])


def build_dry_run_preview(candidates: list[StaleClaimCandidate]) -> list[dict]:
    """Return preview of intended changes — NOT applied to any real store."""
    return [
        {
            "entity_id": c.entity_id,
            "from_status": c.prior_status,
            "to_status": "review_required",
            "dry_run": True,
        }
        for c in candidates
    ]


def produce_evidence_packet(
    charter: CharterProfile,
    candidates: list[StaleClaimCandidate],
    simulation_timestamp: str,
) -> EvidencePacket:
    """Produce an EvidencePacket for the dry-run simulation."""
    date_compact = simulation_timestamp[:10].replace("-", "")
    return EvidencePacket(
        evidence_id=f"evidence-r4-001-dry-run-{date_compact}",
        mission_id="mission-r4-001-graphify-stale-review",
        action_id=f"action-r4-001-sim-{date_compact}",
        actor="gail-os-r4-simulator",
        action_type="graphify.stale_claim.review",
        authority_basis=charter.charter_id,
        result="success",
        execution_mode="dry-run",
        created_at=simulation_timestamp,
        envelope_id=None,
        rollback_note=charter.rollback_path,
        outcome_summary=(
            f"R4 dry-run: {len(candidates)} stale claim candidates identified. "
            f"No live mutations. Charter {charter.charter_id} validated."
        ),
    )


def produce_okp(
    charter: CharterProfile,
    candidates: list[StaleClaimCandidate],
    evidence_packet: EvidencePacket,
    simulation_timestamp: str,
) -> dict:
    """Produce an OKP of type charter.executed for this simulation run."""
    date_compact = simulation_timestamp[:10].replace("-", "")
    return {
        "okp_id": f"okp-r4-001-dry-run-{date_compact}",
        "record_type": "charter.executed",
        "source_system": "gail-os-r4-simulator",
        "source_ref": charter.charter_id,
        "summary": (
            f"R4-001 dry-run simulation: {len(candidates)} candidates reviewed. "
            "No mutations."
        ),
        "authority_level": "R4",
        "status": "observed",
        "created_at": simulation_timestamp,
        "evidence_id": evidence_packet.evidence_id,
    }


def produce_rollback_data(candidates: list[StaleClaimCandidate]) -> list[dict]:
    """Return rollback data — list of {entity_id, prior_status} for every candidate."""
    return [
        {"entity_id": c.entity_id, "prior_status": c.prior_status}
        for c in candidates
    ]


def build_freedom_brief(
    charter: CharterProfile,
    candidates: list[StaleClaimCandidate],
    evidence_packet: EvidencePacket,
    simulation_timestamp: str,
) -> dict:
    """Build a Freedom-compatible charter execution brief (informational, no API call)."""
    return {
        "brief_type": "charter_execution",
        "charter_id": charter.charter_id,
        "charter_title": charter.title,
        "authority_level": charter.authority_level,
        "execution_mode": "dry-run",
        "candidate_count": len(candidates),
        "charter_status": "permitted",
        "policy_decision": "approved",
        "recommendation": "proceed_to_6.5_after_adam_approval",
        "evidence_id": evidence_packet.evidence_id,
        "generated_at": simulation_timestamp,
        "note": (
            "Freedom cannot self-approve charter changes. "
            "Chunk 6.5 requires explicit Adam approval."
        ),
    }


def run_r4_dry_run_simulation(
    candidate_count: int = 5,
    simulation_timestamp: str | None = None,
) -> R4DryRunResult:
    """Run the full R4-001 dry-run simulation end-to-end. No live mutations."""
    ts = simulation_timestamp if simulation_timestamp is not None else "2026-06-28T00:00:00Z"

    charter = build_r4_001_charter()
    charter_valid, charter_errors = validate_charter_authority(charter)
    candidates = generate_stale_claim_candidates(candidate_count)
    dry_run_preview = build_dry_run_preview(candidates)
    evidence_packet = produce_evidence_packet(charter, candidates, ts)
    okp = produce_okp(charter, candidates, evidence_packet, ts)
    rollback_data = produce_rollback_data(candidates)
    freedom_brief = build_freedom_brief(charter, candidates, evidence_packet, ts)

    return R4DryRunResult(
        charter_id=charter.charter_id,
        charter_valid=charter_valid,
        charter_errors=charter_errors,
        candidates=candidates,
        dry_run_preview=dry_run_preview,
        evidence_packet=evidence_packet.to_dict(),
        okp=okp,
        rollback_data=rollback_data,
        freedom_brief=freedom_brief,
        simulation_timestamp=ts,
        no_live_mutations=True,
    )


__all__ = [
    "R4DryRunResult",
    "StaleClaimCandidate",
    "build_freedom_brief",
    "build_dry_run_preview",
    "build_r4_001_charter",
    "generate_stale_claim_candidates",
    "produce_evidence_packet",
    "produce_okp",
    "produce_rollback_data",
    "run_r4_dry_run_simulation",
    "validate_charter_authority",
]
