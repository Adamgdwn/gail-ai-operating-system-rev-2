"""Signal Gravity L1 Calculator — local factor scoring for OKPs (Phase 5).

L1 uses only data available within the OKP itself (no Graphify, no M365,
no live network calls).  Factors that require graph context are held at the
L2 placeholder value of 0.5.

Weight keys must sum to exactly 1.0.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


DEFAULT_WEIGHTS: dict[str, float] = {
    "recent_evidence":      0.18,
    "unresolved_risk":      0.17,
    "operational_value":    0.15,
    "repeated_recurrence":  0.12,
    "pending_authority":    0.13,
    "connected_blockers":   0.10,
    "client_impact":        0.07,
    "prior_failure_relation": 0.05,
    "strategic_alignment":  0.03,
}

_VALID_FACTOR_NAMES = frozenset(DEFAULT_WEIGHTS.keys())


@dataclass(frozen=True)
class CalibrationProposal:
    """A proposal to change a single factor weight."""
    proposal_id: str       # "proposal-" prefix + uuid4 hex[:12]
    factor_name: str
    current_weight: float
    proposed_weight: float
    delta: float
    rationale: str
    created_at: str        # ISO string


class SignalGravityL1Calculator:
    """Calculate L1 gravity scores for OperatingKnowledgePackets.

    Scores are weighted sums of nine factors, clamped to [0.0, 1.0].  Factors
    that require Graphify graph context (4, 6, 7, 8, 9) are held at 0.5 until
    L2 enrichment runs.
    """

    def __init__(self, store_path: str = "local_store") -> None:
        self.store_path = store_path
        self._config_path = os.path.join(store_path, "signal_gravity_config.json")
        self._proposals_path = os.path.join(
            store_path, "signal_gravity_calibration_proposals.json"
        )

    # ------------------------------------------------------------------
    # Weight management
    # ------------------------------------------------------------------

    def load_weights(self) -> dict[str, float]:
        """Load weights from config file, creating it with defaults if missing."""
        if os.path.exists(self._config_path):
            try:
                with open(self._config_path, encoding="utf-8") as fh:
                    data = json.load(fh)
                if isinstance(data, dict):
                    return data
            except (json.JSONDecodeError, OSError):
                pass
        # File missing or unreadable — write defaults then return them
        self._write_weights(DEFAULT_WEIGHTS)
        return dict(DEFAULT_WEIGHTS)

    def _write_weights(self, weights: dict[str, float]) -> None:
        os.makedirs(self.store_path, exist_ok=True)
        with open(self._config_path, "w", encoding="utf-8") as fh:
            json.dump(weights, fh, indent=2)

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def calculate(self, okp, weights: dict[str, float] | None = None) -> float:  # noqa: ANN001
        """Return an L1 gravity score in [0.0, 1.0] for *okp*.

        Factor mapping
        --------------
        1. recent_evidence      — time-decay based on age vs 1-week horizon
        2. unresolved_risk      — normalised risk_tier (1-5 -> 0.0-1.0)
        3. operational_value    — okp.confidence
        4. repeated_recurrence  — L2 placeholder: 0.5
        5. pending_authority    — 1.0 if status=="review_required" or authority_level in {R3,R4}
        6. connected_blockers   — L2 placeholder: 0.5
        7. client_impact        — L2 placeholder: 0.5
        8. prior_failure_relation — L2 placeholder: 0.5
        9. strategic_alignment  — L2 placeholder: 0.5
        """
        if weights is None:
            weights = self.load_weights()

        now = datetime.now(timezone.utc)
        observed_at = okp.observed_at
        if observed_at.tzinfo is None:
            # Treat naive datetimes as UTC
            from datetime import timezone as _tz
            observed_at = observed_at.replace(tzinfo=_tz.utc)

        age_hours = (now - observed_at).total_seconds() / 3600
        factor1 = max(0.0, 1.0 - age_hours / 168)  # 1-week (168 h) linear decay

        factor2 = (okp.risk_tier - 1) / 4  # risk_tier 1 -> 0.0, 5 -> 1.0

        factor3 = float(okp.confidence)

        factor4 = 0.5  # L2 placeholder

        factor5 = (
            1.0
            if (
                okp.status == "review_required"
                or okp.authority_level in {"R3", "R4"}
            )
            else 0.0
        )

        factor6 = 0.5  # L2 placeholder
        factor7 = 0.5  # L2 placeholder
        factor8 = 0.5  # L2 placeholder
        factor9 = 0.5  # L2 placeholder

        factors = [
            ("recent_evidence",       factor1),
            ("unresolved_risk",       factor2),
            ("operational_value",     factor3),
            ("repeated_recurrence",   factor4),
            ("pending_authority",     factor5),
            ("connected_blockers",    factor6),
            ("client_impact",         factor7),
            ("prior_failure_relation", factor8),
            ("strategic_alignment",   factor9),
        ]

        score = sum(weights.get(name, 0.0) * value for name, value in factors)
        return max(0.0, min(1.0, score))

    # ------------------------------------------------------------------
    # Calibration proposals
    # ------------------------------------------------------------------

    def propose_calibration(
        self,
        factor_name: str,
        proposed_weight: float,
        rationale: str,
    ) -> CalibrationProposal:
        """Create and persist a calibration proposal for a factor weight."""
        if factor_name not in _VALID_FACTOR_NAMES:
            raise ValueError(
                f"factor_name {factor_name!r} is not a recognised factor. "
                f"Valid factors: {sorted(_VALID_FACTOR_NAMES)}"
            )
        current_weights = self.load_weights()
        current_weight = current_weights[factor_name]
        delta = round(proposed_weight - current_weight, 10)
        proposal = CalibrationProposal(
            proposal_id=f"proposal-{uuid4().hex[:12]}",
            factor_name=factor_name,
            current_weight=current_weight,
            proposed_weight=proposed_weight,
            delta=delta,
            rationale=rationale,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        # Append to proposals file
        import dataclasses
        os.makedirs(self.store_path, exist_ok=True)
        existing: list[dict] = []
        if os.path.exists(self._proposals_path):
            try:
                with open(self._proposals_path, encoding="utf-8") as fh:
                    existing = json.load(fh)
                if not isinstance(existing, list):
                    existing = []
            except (json.JSONDecodeError, OSError):
                existing = []
        existing.append(dataclasses.asdict(proposal))
        with open(self._proposals_path, "w", encoding="utf-8") as fh:
            json.dump(existing, fh, indent=2)
        return proposal


__all__ = ["DEFAULT_WEIGHTS", "CalibrationProposal", "SignalGravityL1Calculator"]
