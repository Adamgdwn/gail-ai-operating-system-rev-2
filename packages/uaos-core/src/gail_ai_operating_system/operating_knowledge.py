"""OperatingKnowledgePacket schema and EvidencePacket-to-OKP converter (Phase 5)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


_UNSAFE_SOURCE_REF_SUBSTRINGS = (".env", "secret", "token", "password")
_UNSAFE_ABSOLUTE_PREFIXES = ("/", "\\")

_VALID_AUTHORITY_LEVELS = {"R0", "R1", "R2", "R3", "R4", "R5"}
_VALID_AUTONOMY_LEVELS = {"A0", "A1", "A2", "A3", "A4", "A5", "A6"}
_VALID_RISK_TIERS = {1, 2, 3, 4, 5}
_VALID_DATA_CLASSIFICATIONS = {"public", "internal", "synthetic", "restricted"}
_VALID_STATUSES = {"observed", "accepted", "rejected", "superseded", "review_required", "learned"}


class OkpRecordType(str, Enum):
    # Action lifecycle
    ACTION_VALIDATED       = "action.validated"
    ACTION_BLOCKED         = "action.blocked"
    # Authority
    AUTHORITY_OVERRIDE_REQ = "authority.override_requested"
    # Evidence
    EVIDENCE_CREATED       = "evidence.created"
    # Mission
    MISSION_CREATED        = "mission.created"
    MISSION_REVIEWED       = "mission.reviewed"
    # Graph / relationship
    GRAPH_RELATIONSHIP     = "graph.relationship_detected"
    GRAPH_CLAIM_STALE      = "graph.claim_stale_candidate"
    # M365
    M365_SIGNAL_OBSERVED   = "m365.signal_observed"
    M365_ACTION_LOG        = "m365.action_log_observed"
    # Freedom
    FREEDOM_BRIEF          = "freedom.brief_created"
    # Build
    BUILD_BRANCH_ABANDONED = "build.branch_abandoned"
    BUILD_BLOCKER_DETECTED = "build.blocker_detected"
    # Capability
    CAPABILITY_GAP         = "capability.gap_detected"
    # Charter (Phase 6)
    CHARTER_PROPOSED       = "charter.proposed"
    CHARTER_EXECUTED       = "charter.executed"
    # Signal Gravity
    GRAVITY_CALIBRATION    = "gravity.calibration_proposed"


def _compute_fingerprint(source_ref: str, record_type: str, summary: str) -> str:
    """Deterministic SHA-256 hash of source_ref + record_type + summary, 32-char hex."""
    raw = f"{source_ref}|{record_type}|{summary}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def _validate_source_ref(source_ref: str) -> None:
    lower = source_ref.lower()
    for substring in _UNSAFE_SOURCE_REF_SUBSTRINGS:
        if substring in lower:
            raise ValueError(
                f"source_ref contains unsafe substring '{substring}': {source_ref!r}"
            )
    for prefix in _UNSAFE_ABSOLUTE_PREFIXES:
        if source_ref.startswith(prefix):
            raise ValueError(
                f"source_ref is an absolute path (unsafe): {source_ref!r}"
            )
    # Reject Windows absolute paths like C:\ or C:/
    if len(source_ref) >= 3 and source_ref[1] == ":" and source_ref[2] in ("/", "\\"):
        raise ValueError(
            f"source_ref is an absolute path (unsafe): {source_ref!r}"
        )


@dataclass(frozen=True)
class OperatingKnowledgePacket:
    """Canonical OKP schema. Validates on construction via __post_init__."""

    # Core identity
    okp_id: str
    source_system: str
    source_ref: str
    record_type: OkpRecordType
    summary: str
    authority_level: str
    autonomy_level: str
    risk_tier: int
    data_classification: str
    status: str
    created_at: datetime
    observed_at: datetime
    confidence: float
    fingerprint: str
    raw_payload_retained: bool

    # Optional links
    related_mission_id: str | None = None
    related_action_id: str | None = None
    related_evidence_id: str | None = None
    related_connector_id: str | None = None
    related_agent_id: str | None = None

    # Scoring (populated by ingest service; enriched by Graphify)
    gravity_score_l1: float | None = None
    gravity_score_l2: float | None = None
    gravity_score_used: float | None = None

    def __post_init__(self) -> None:
        if not self.okp_id.startswith("okp-"):
            raise ValueError("okp_id must use the 'okp-' prefix.")
        if self.raw_payload_retained:
            raise ValueError(
                "raw_payload_retained must be False; retaining raw payloads is not permitted."
            )
        if self.authority_level not in _VALID_AUTHORITY_LEVELS:
            raise ValueError(
                f"authority_level must be one of {sorted(_VALID_AUTHORITY_LEVELS)}, "
                f"got {self.authority_level!r}."
            )
        if self.autonomy_level not in _VALID_AUTONOMY_LEVELS:
            raise ValueError(
                f"autonomy_level must be one of {sorted(_VALID_AUTONOMY_LEVELS)}, "
                f"got {self.autonomy_level!r}."
            )
        if self.risk_tier not in _VALID_RISK_TIERS:
            raise ValueError(
                f"risk_tier must be an integer 1-5, got {self.risk_tier!r}."
            )
        if self.data_classification not in _VALID_DATA_CLASSIFICATIONS:
            raise ValueError(
                f"data_classification must be one of {sorted(_VALID_DATA_CLASSIFICATIONS)}, "
                f"got {self.data_classification!r}."
            )
        if self.status not in _VALID_STATUSES:
            raise ValueError(
                f"status must be one of {sorted(_VALID_STATUSES)}, got {self.status!r}."
            )
        if len(self.summary) > 1000:
            raise ValueError("summary must not exceed 1000 characters.")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                f"confidence must be between 0.0 and 1.0, got {self.confidence!r}."
            )
        _validate_source_ref(self.source_ref)
        for field_name, value in [
            ("gravity_score_l1", self.gravity_score_l1),
            ("gravity_score_l2", self.gravity_score_l2),
            ("gravity_score_used", self.gravity_score_used),
        ]:
            if value is not None and not (0.0 <= value <= 1.0):
                raise ValueError(f"{field_name} must be between 0.0 and 1.0.")


def create_operating_knowledge_packet(
    *,
    source_system: str,
    source_ref: str,
    record_type: OkpRecordType,
    summary: str,
    authority_level: str,
    autonomy_level: str,
    risk_tier: int,
    data_classification: str,
    confidence: float,
    observed_at: datetime | None = None,
    status: str = "observed",
    related_mission_id: str | None = None,
    related_action_id: str | None = None,
    related_evidence_id: str | None = None,
    related_connector_id: str | None = None,
    related_agent_id: str | None = None,
    gravity_score_l1: float | None = None,
    gravity_score_l2: float | None = None,
    gravity_score_used: float | None = None,
) -> OperatingKnowledgePacket:
    """Factory: validates inputs, computes fingerprint, assigns okp_id."""
    _validate_source_ref(source_ref)
    now = datetime.now(timezone.utc)
    okp_id = f"okp-{uuid4().hex[:12]}"
    fingerprint = _compute_fingerprint(source_ref, record_type.value, summary)
    return OperatingKnowledgePacket(
        okp_id=okp_id,
        source_system=source_system,
        source_ref=source_ref,
        record_type=record_type,
        summary=summary,
        authority_level=authority_level,
        autonomy_level=autonomy_level,
        risk_tier=risk_tier,
        data_classification=data_classification,
        status=status,
        created_at=now,
        observed_at=observed_at or now,
        confidence=confidence,
        fingerprint=fingerprint,
        raw_payload_retained=False,
        related_mission_id=related_mission_id,
        related_action_id=related_action_id,
        related_evidence_id=related_evidence_id,
        related_connector_id=related_connector_id,
        related_agent_id=related_agent_id,
        gravity_score_l1=gravity_score_l1,
        gravity_score_l2=gravity_score_l2,
        gravity_score_used=gravity_score_used,
    )


class EvidencePacketToOkpConverter:
    """Converts a Phase 4 EvidencePacket into an OperatingKnowledgePacket of type evidence.created."""

    @staticmethod
    def convert(evidence_packet: Any) -> OperatingKnowledgePacket:
        """Convert an EvidencePacket to an OKP.

        Mapping:
          evidence_id     -> source_ref, related_evidence_id
          mission_id      -> related_mission_id
          action_id       -> related_action_id
          outcome_summary -> summary (capped at 1000 chars)
          created_at      -> observed_at
        """
        raw_created_at = evidence_packet.created_at
        if isinstance(raw_created_at, str):
            try:
                observed_at = datetime.fromisoformat(raw_created_at.replace("Z", "+00:00"))
            except ValueError:
                observed_at = datetime.now(timezone.utc)
        elif isinstance(raw_created_at, datetime):
            observed_at = raw_created_at
        else:
            observed_at = datetime.now(timezone.utc)

        summary = str(evidence_packet.outcome_summary or "")[:1000]
        if not summary:
            summary = (
                f"Evidence from {evidence_packet.action_type} action by {evidence_packet.actor}"
            )[:1000]

        source_ref = evidence_packet.evidence_id
        record_type = OkpRecordType.EVIDENCE_CREATED
        fingerprint = _compute_fingerprint(source_ref, record_type.value, summary)
        okp_id = f"okp-{uuid4().hex[:12]}"
        now = datetime.now(timezone.utc)

        return OperatingKnowledgePacket(
            okp_id=okp_id,
            source_system="gail-os-evidence",
            source_ref=source_ref,
            record_type=record_type,
            summary=summary,
            authority_level="R1",
            autonomy_level="A1",
            risk_tier=2,
            data_classification="internal",
            status="observed",
            created_at=now,
            observed_at=observed_at,
            confidence=0.9,
            fingerprint=fingerprint,
            raw_payload_retained=False,
            related_mission_id=evidence_packet.mission_id,
            related_action_id=evidence_packet.action_id,
            related_evidence_id=evidence_packet.evidence_id,
        )


__all__ = [
    "OkpRecordType",
    "OperatingKnowledgePacket",
    "EvidencePacketToOkpConverter",
    "create_operating_knowledge_packet",
]
