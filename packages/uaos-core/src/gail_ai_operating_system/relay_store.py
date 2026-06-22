"""Local relay record store and trusted-worker claim proof."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .mission_spine import MissionAction
from .relay_envelope import DEVICE_ROLES, RelayEnvelope, RelayValidationContext, validate_relay_envelope


RELAY_STORE_SCHEMA_VERSION = "rev2.relay-store.v1"

RELAY_RECORD_STATUSES = frozenset(
    {
        "draft",
        "proposed",
        "approved",
        "claimed",
        "completed",
        "stopped",
        "superseded",
        "conflicted",
    }
)
CLAIMABLE_RECORD_STATUSES = frozenset({"proposed", "approved"})
TRUSTED_WORKER_ROLES = frozenset({"linux_trusted_worker", "windows_trusted_worker"})
SAFE_WORKER_CLAIM_CAPABILITIES = frozenset({"status-read", "local-validation", "readiness-check", "evidence-summary"})
EVIDENCE_BLOCKED_STATUSES = frozenset({"superseded", "conflicted", "stopped"})

SENSITIVE_SUMMARY_KEYS = frozenset(
    {
        "secret",
        "secrets",
        "secret_value",
        "credential",
        "credentials",
        "password",
        "token",
        "api_key",
        "private_key",
        "raw_log",
        "raw_logs",
        "raw_audio",
        "audio_blob",
        "client_data_full",
        "unscoped_client_data",
        "unrestricted_filesystem",
        "live_connector_session",
    }
)
SENSITIVE_VALUE_MARKERS = (
    "begin private key",
    "password=",
    "passwd=",
    "token:",
    "api_key=",
    "client_secret=",
    "raw audio",
    "raw log",
    "client data full",
    "unredacted payload",
)
SENSITIVE_REFERENCE_HINTS = (
    ".env",
    "credential",
    "secret",
    "token",
    "private-key",
    "private_key",
    "raw-log",
    "raw_log",
    "raw-audio",
    "raw_audio",
    "client-data",
    "client_data",
    "invoice",
    "accounting-export",
)


@dataclass(frozen=True)
class RelayStatusChange:
    """One local status transition for a relay record."""

    status: str
    changed_at: str
    reason: str
    observed_state_refs: Mapping[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "changed_at": self.changed_at,
            "reason": self.reason,
            "observed_state_refs": dict(self.observed_state_refs),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "RelayStatusChange":
        return cls(
            status=str(payload["status"]),
            changed_at=str(payload["changed_at"]),
            reason=str(payload["reason"]),
            observed_state_refs=_read_text_mapping(payload, "observed_state_refs", default={}),
        )


@dataclass(frozen=True)
class RelayWorkerClaim:
    """A local proof claim from exactly one trusted worker for one mission."""

    claim_id: str
    envelope_id: str
    mission_id: str
    worker_device_id: str
    worker_role: str
    observed_state_refs: Mapping[str, str]
    connector_profile_ids: tuple[str, ...]
    claimed_at: str
    requested_capability: str = "local-validation"
    evidence_refs: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "envelope_id": self.envelope_id,
            "mission_id": self.mission_id,
            "worker_device_id": self.worker_device_id,
            "worker_role": self.worker_role,
            "observed_state_refs": dict(self.observed_state_refs),
            "connector_profile_ids": list(self.connector_profile_ids),
            "claimed_at": self.claimed_at,
            "requested_capability": self.requested_capability,
            "evidence_refs": list(self.evidence_refs),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "RelayWorkerClaim":
        return cls(
            claim_id=str(payload["claim_id"]),
            envelope_id=str(payload["envelope_id"]),
            mission_id=str(payload["mission_id"]),
            worker_device_id=str(payload["worker_device_id"]),
            worker_role=str(payload["worker_role"]),
            observed_state_refs=_read_text_mapping(payload, "observed_state_refs"),
            connector_profile_ids=_read_text_tuple(payload, "connector_profile_ids"),
            claimed_at=str(payload["claimed_at"]),
            requested_capability=str(payload.get("requested_capability", "local-validation")),
            evidence_refs=_read_text_tuple(payload, "evidence_refs", default=()),
        )

    def to_mission_action(self) -> MissionAction:
        """Represent a worker claim as local dry-run policy-gate input."""

        return MissionAction(
            action_id=f"relay-claim-{self.claim_id}",
            action_type="relay_worker_claim_validate",
            title=f"Validate relay worker claim {self.claim_id}",
            arguments={
                "claim_id": self.claim_id,
                "envelope_id": self.envelope_id,
                "mission_id": self.mission_id,
                "worker_device_id": self.worker_device_id,
                "worker_role": self.worker_role,
                "requested_capability": self.requested_capability,
                "connector_profile_ids": list(self.connector_profile_ids),
                "observed_state_refs": dict(self.observed_state_refs),
                "evidence_refs": list(self.evidence_refs),
            },
            risk_tier=2,
        )


@dataclass(frozen=True)
class RelayEvidenceRecord:
    """Reference-only local evidence linked to a relay record."""

    evidence_id: str
    envelope_id: str
    mission_id: str
    recorder_device_id: str
    recorder_role: str
    recorded_at: str
    safe_summary: Mapping[str, Any]
    evidence_refs: tuple[str, ...]
    observed_state_refs: Mapping[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "envelope_id": self.envelope_id,
            "mission_id": self.mission_id,
            "recorder_device_id": self.recorder_device_id,
            "recorder_role": self.recorder_role,
            "recorded_at": self.recorded_at,
            "safe_summary": dict(self.safe_summary),
            "evidence_refs": list(self.evidence_refs),
            "observed_state_refs": dict(self.observed_state_refs),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "RelayEvidenceRecord":
        return cls(
            evidence_id=str(payload["evidence_id"]),
            envelope_id=str(payload["envelope_id"]),
            mission_id=str(payload["mission_id"]),
            recorder_device_id=str(payload["recorder_device_id"]),
            recorder_role=str(payload["recorder_role"]),
            recorded_at=str(payload["recorded_at"]),
            safe_summary=_read_mapping(payload, "safe_summary"),
            evidence_refs=_read_text_tuple(payload, "evidence_refs"),
            observed_state_refs=_read_text_mapping(payload, "observed_state_refs"),
        )


@dataclass(frozen=True)
class RelayClaimReport:
    """Outcome of a local trusted-worker claim attempt."""

    claim_id: str
    accepted: bool
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class RelayRecordReport:
    """Outcome of a relay store record operation."""

    envelope_id: str
    accepted: bool
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class RelayEvidenceReport:
    """Outcome of a local evidence write."""

    evidence_id: str
    accepted: bool
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class RelayRecord:
    """One validated relay envelope plus local status, claim, and evidence records."""

    envelope: RelayEnvelope
    status: str
    created_at: str
    updated_at: str
    status_history: tuple[RelayStatusChange, ...] = ()
    claim_attempts: tuple[RelayWorkerClaim, ...] = ()
    evidence_records: tuple[RelayEvidenceRecord, ...] = ()
    accepted_claim_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "envelope": self.envelope.to_dict(),
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status_history": [change.to_dict() for change in self.status_history],
            "claim_attempts": [claim.to_dict() for claim in self.claim_attempts],
            "evidence_records": [evidence.to_dict() for evidence in self.evidence_records],
            "accepted_claim_id": self.accepted_claim_id,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "RelayRecord":
        return cls(
            envelope=RelayEnvelope.from_dict(_read_mapping(payload, "envelope")),
            status=str(payload["status"]),
            created_at=str(payload["created_at"]),
            updated_at=str(payload["updated_at"]),
            status_history=tuple(RelayStatusChange.from_dict(change) for change in payload.get("status_history", ())),
            claim_attempts=tuple(RelayWorkerClaim.from_dict(claim) for claim in payload.get("claim_attempts", ())),
            evidence_records=tuple(
                RelayEvidenceRecord.from_dict(evidence) for evidence in payload.get("evidence_records", ())
            ),
            accepted_claim_id=str(payload.get("accepted_claim_id", "")),
        )


class LocalRelayRecordStore:
    """A deterministic JSON-backed local proof store for relay records."""

    def __init__(self, path: str | Path, *, context: RelayValidationContext | None = None) -> None:
        self.path = Path(path)
        self.context = context or RelayValidationContext()
        self.records: dict[str, RelayRecord] = {}
        self._load()

    def add_envelope(
        self,
        envelope: RelayEnvelope,
        *,
        observed_at: str,
        context: RelayValidationContext | None = None,
    ) -> RelayRecordReport:
        """Persist a locally validated relay envelope as a record."""

        validation_context = context or self.context
        validation_report = validate_relay_envelope(envelope, context=validation_context)
        reasons = list(validation_report.reasons)

        if envelope.envelope_id in self.records:
            reasons.append("relay envelope already exists in the local record store")
        if envelope.relay_status not in RELAY_RECORD_STATUSES:
            reasons.append("relay record status is not supported by the local store")
        if not observed_at.strip():
            reasons.append("observed_at is required for relay record persistence")

        if reasons:
            return RelayRecordReport(envelope_id=envelope.envelope_id or "unknown", accepted=False, reasons=tuple(reasons))

        status_change = RelayStatusChange(
            status=envelope.relay_status,
            changed_at=observed_at,
            reason="validated relay envelope recorded",
            observed_state_refs=dict(envelope.observed_state_refs),
        )
        self.records[envelope.envelope_id] = RelayRecord(
            envelope=envelope,
            status=envelope.relay_status,
            created_at=observed_at,
            updated_at=observed_at,
            status_history=(status_change,),
        )
        self._save()
        return RelayRecordReport(envelope_id=envelope.envelope_id, accepted=True)

    def update_status(
        self,
        envelope_id: str,
        status: str,
        *,
        changed_at: str,
        reason: str,
        observed_state_refs: Mapping[str, str],
        context: RelayValidationContext | None = None,
    ) -> RelayRecordReport:
        """Record a local relay status transition with current observed state."""

        record = self.records.get(envelope_id)
        validation_context = context or self.context
        reasons: list[str] = []

        if record is None:
            reasons.append("relay envelope is not known in the local record store")
        if status not in RELAY_RECORD_STATUSES:
            reasons.append("relay record status is not supported by the local store")
        if not changed_at.strip():
            reasons.append("changed_at is required for relay status changes")
        if not reason.strip():
            reasons.append("status change reason is required")
        if not observed_state_refs:
            reasons.append("observed_state_refs are required for relay status changes")
        elif stale := _stale_state_refs(observed_state_refs, validation_context.current_state_refs):
            reasons.append(f"status change observed_state_refs are stale: {', '.join(stale)}")

        if reasons or record is None:
            return RelayRecordReport(envelope_id=envelope_id or "unknown", accepted=False, reasons=tuple(reasons))

        status_change = RelayStatusChange(
            status=status,
            changed_at=changed_at,
            reason=reason,
            observed_state_refs=dict(observed_state_refs),
        )
        self.records[envelope_id] = RelayRecord(
            envelope=record.envelope,
            status=status,
            created_at=record.created_at,
            updated_at=changed_at,
            status_history=record.status_history + (status_change,),
            claim_attempts=record.claim_attempts,
            evidence_records=record.evidence_records,
            accepted_claim_id=record.accepted_claim_id,
        )
        self._save()
        return RelayRecordReport(envelope_id=envelope_id, accepted=True)

    def claim_worker(
        self,
        claim: RelayWorkerClaim,
        *,
        context: RelayValidationContext | None = None,
    ) -> RelayClaimReport:
        """Attempt to claim exactly one mission for one trusted local worker."""

        validation_context = context or self.context
        record = self.records.get(claim.envelope_id)
        reasons = self._claim_rejection_reasons(claim, record, validation_context)
        accepted = not reasons

        if record is not None:
            next_status = "claimed" if accepted else record.status
            status_history = record.status_history
            if accepted:
                status_history = status_history + (
                    RelayStatusChange(
                        status="claimed",
                        changed_at=claim.claimed_at,
                        reason=f"accepted trusted-worker claim {claim.claim_id}",
                        observed_state_refs=dict(claim.observed_state_refs),
                    ),
                )
            self.records[claim.envelope_id] = RelayRecord(
                envelope=record.envelope,
                status=next_status,
                created_at=record.created_at,
                updated_at=claim.claimed_at if claim.claimed_at.strip() else record.updated_at,
                status_history=status_history,
                claim_attempts=record.claim_attempts + (claim,),
                evidence_records=record.evidence_records,
                accepted_claim_id=claim.claim_id if accepted else record.accepted_claim_id,
            )
            self._save()

        return RelayClaimReport(claim_id=claim.claim_id or "unknown", accepted=accepted, reasons=tuple(reasons))

    def add_evidence(
        self,
        evidence: RelayEvidenceRecord,
        *,
        context: RelayValidationContext | None = None,
    ) -> RelayEvidenceReport:
        """Append safe reference-only evidence to a local relay record."""

        validation_context = context or self.context
        record = self.records.get(evidence.envelope_id)
        reasons: list[str] = []

        if record is None:
            reasons.append("relay envelope is not known in the local record store")
        else:
            if record.envelope.mission_id != evidence.mission_id:
                reasons.append("evidence mission_id does not match the relay envelope")
            if record.status in EVIDENCE_BLOCKED_STATUSES:
                reasons.append("relay record cannot accept evidence in its current status")
            if any(existing.evidence_id == evidence.evidence_id for existing in record.evidence_records):
                reasons.append("evidence_id already exists for this relay record")

        if not evidence.evidence_id.strip():
            reasons.append("evidence_id is required")
        if not evidence.recorded_at.strip():
            reasons.append("recorded_at is required")
        if evidence.recorder_role not in DEVICE_ROLES:
            reasons.append("recorder_role is not approved for relay evidence")
        if validation_context.approved_device_ids and evidence.recorder_device_id not in validation_context.approved_device_ids:
            reasons.append("recorder_device_id is not in the approved device list")
        if not evidence.evidence_refs:
            reasons.append("evidence_refs must include at least one safe evidence reference")
        elif unsafe_refs := _unsafe_refs(evidence.evidence_refs):
            reasons.append(f"evidence_refs must be relative non-sensitive references: {', '.join(unsafe_refs)}")
        if not evidence.safe_summary:
            reasons.append("safe_summary is required for relay evidence")
        elif _contains_sensitive_summary(evidence.safe_summary):
            reasons.append("safe_summary must not include raw secrets, credentials, raw logs, raw audio, client payloads, or live sessions")
        if not evidence.observed_state_refs:
            reasons.append("observed_state_refs are required for relay evidence")
        elif stale := _stale_state_refs(evidence.observed_state_refs, validation_context.current_state_refs):
            reasons.append(f"evidence observed_state_refs are stale: {', '.join(stale)}")

        if reasons or record is None:
            return RelayEvidenceReport(evidence_id=evidence.evidence_id or "unknown", accepted=False, reasons=tuple(reasons))

        self.records[evidence.envelope_id] = RelayRecord(
            envelope=record.envelope,
            status=record.status,
            created_at=record.created_at,
            updated_at=evidence.recorded_at,
            status_history=record.status_history,
            claim_attempts=record.claim_attempts,
            evidence_records=record.evidence_records + (evidence,),
            accepted_claim_id=record.accepted_claim_id,
        )
        self._save()
        return RelayEvidenceReport(evidence_id=evidence.evidence_id, accepted=True)

    def get_record(self, envelope_id: str) -> RelayRecord | None:
        """Return one local relay record if it exists."""

        return self.records.get(envelope_id)

    def _claim_rejection_reasons(
        self,
        claim: RelayWorkerClaim,
        record: RelayRecord | None,
        validation_context: RelayValidationContext,
    ) -> list[str]:
        reasons: list[str] = []

        if record is None:
            reasons.append("relay envelope is not known in the local record store")
        else:
            envelope_report = validate_relay_envelope(record.envelope, context=validation_context)
            reasons.extend(envelope_report.reasons)
            if record.status not in CLAIMABLE_RECORD_STATUSES:
                reasons.append("relay record is not claimable in its current status")
            if record.envelope.mission_id != claim.mission_id:
                reasons.append("worker claim mission_id does not match the relay envelope")
            if set(claim.connector_profile_ids) - set(record.envelope.connector_profile_ids):
                reasons.append("worker claim connector_profile_ids exceed the relay envelope boundary")

        if not claim.claim_id.strip():
            reasons.append("claim_id is required")
        if not claim.claimed_at.strip():
            reasons.append("claimed_at is required")
        if not claim.worker_device_id.strip():
            reasons.append("worker_device_id is required")
        if claim.worker_role not in TRUSTED_WORKER_ROLES:
            reasons.append("worker_role must be a trusted Linux or Windows worker")
        if validation_context.approved_device_ids and claim.worker_device_id not in validation_context.approved_device_ids:
            reasons.append("worker_device_id is not in the approved device list")
        if claim.requested_capability not in SAFE_WORKER_CLAIM_CAPABILITIES:
            reasons.append("worker claim requested_capability must remain local validation, status, readiness, or evidence only")
        if not claim.observed_state_refs:
            reasons.append("worker claim observed_state_refs are required before acting")
        elif stale := _stale_state_refs(claim.observed_state_refs, validation_context.current_state_refs):
            reasons.append(f"worker claim observed_state_refs are stale: {', '.join(stale)}")
        if unsafe_refs := _unsafe_refs(claim.evidence_refs):
            reasons.append(f"worker claim evidence_refs must be relative non-sensitive references: {', '.join(unsafe_refs)}")

        unknown_connectors = sorted(set(claim.connector_profile_ids) - set(validation_context.known_connector_profile_ids))
        if unknown_connectors:
            reasons.append(f"unknown connector_profile_ids: {', '.join(unknown_connectors)}")

        existing_claim = self._accepted_claim_for_mission(claim.mission_id)
        if existing_claim and existing_claim != claim.claim_id:
            reasons.append("mission already has an accepted trusted-worker claim")

        return reasons

    def _accepted_claim_for_mission(self, mission_id: str) -> str:
        for record in self.records.values():
            if record.envelope.mission_id == mission_id and record.accepted_claim_id:
                return record.accepted_claim_id
        return ""

    def _load(self) -> None:
        if not self.path.exists():
            return
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != RELAY_STORE_SCHEMA_VERSION:
            raise ValueError(f"Relay store schema_version must be {RELAY_STORE_SCHEMA_VERSION}.")
        raw_records = payload.get("records", {})
        if not isinstance(raw_records, Mapping):
            raise ValueError("Relay store records must be a JSON object.")
        self.records = {
            str(envelope_id): RelayRecord.from_dict(raw_record)
            for envelope_id, raw_record in raw_records.items()
        }

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": RELAY_STORE_SCHEMA_VERSION,
            "records": {
                envelope_id: record.to_dict()
                for envelope_id, record in sorted(self.records.items())
            },
        }
        document = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        temp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        temp_path.write_text(document, encoding="utf-8")
        temp_path.replace(self.path)


def _read_text_tuple(
    payload: Mapping[str, Any],
    key: str,
    *,
    default: Iterable[str] | None = None,
) -> tuple[str, ...]:
    value = payload.get(key, default if default is not None else ())
    if isinstance(value, str):
        raise ValueError(f"{key} must be a JSON array of strings.")
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{key} must be a JSON array of strings.")
    return tuple(str(item).strip() for item in value if str(item).strip())


def _read_text_mapping(
    payload: Mapping[str, Any],
    key: str,
    *,
    default: Mapping[str, str] | None = None,
) -> dict[str, str]:
    value = payload.get(key, default)
    if not isinstance(value, Mapping):
        raise ValueError(f"{key} must be a JSON object.")
    return {str(item_key): str(item_value) for item_key, item_value in value.items()}


def _read_mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"{key} must be a JSON object.")
    return dict(value)


def _stale_state_refs(observed: Mapping[str, str], current: Mapping[str, str]) -> list[str]:
    return [key for key, current_value in current.items() if observed.get(key) != current_value]


def _unsafe_refs(values: Iterable[str]) -> list[str]:
    return [value for value in values if _unsafe_ref(value) or _contains_sensitive_reference(value)]


def _unsafe_ref(value: str) -> bool:
    normalized = value.strip().replace("\\", "/")
    if not normalized:
        return True
    if normalized.startswith("/") or normalized.startswith("//"):
        return True
    if ":" in normalized.split("/", 1)[0]:
        return True
    return ".." in normalized.split("/")


def _contains_sensitive_reference(value: str) -> bool:
    lowered = value.strip().replace("\\", "/").lower()
    return any(hint in lowered for hint in SENSITIVE_REFERENCE_HINTS)


def _contains_sensitive_summary(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if isinstance(key, str) and key.lower().strip() in SENSITIVE_SUMMARY_KEYS:
                return True
            if _contains_sensitive_summary(nested):
                return True
        return False
    if isinstance(value, list):
        return any(_contains_sensitive_summary(item) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        return any(marker in lowered for marker in SENSITIVE_VALUE_MARKERS)
    return False
