"""Local contract for future Graphify acceleration facts.

This module defines safe, inspectable records that GAIL OS can emit later so
Graphify does not need to rediscover governed relationships from raw source or
long documents. It does not persist records, call Graphify, expose transport,
or grant execution authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime
import hashlib
import json
from typing import Any, Iterable, Mapping

from .action import Action, validate_action
from .authority_envelope import (
    AuthorityEnvelope,
    AuthorityLevel,
    EnvelopeStatus,
    validate_authority_envelope,
)
from .evidence_packet import EvidencePacket, validate_evidence_packet
from .mission import MissionStatus
from .relay_store import RELAY_RECORD_STATUSES


GRAPHIFY_ACCELERATION_SCHEMA_VERSION = "rev2.graphify-acceleration.v1"
GRAPHIFY_ACCELERATION_SOURCE_SYSTEM = "gail-ai-operating-system-rev-2"
GRAPHIFY_FINGERPRINT_EXCLUDED_FIELDS = ("fingerprint", "generated_at")
DEFAULT_GRAPHIFY_ACCELERATION_STOP_TRIGGERS = (
    "graphify_action_execution",
    "secret_exposure",
    "client_data_access",
    "raw_payload_retention",
)
DEFAULT_GRAPHIFY_ACCELERATION_NON_GOALS = (
    "No Graphify runtime modification",
    "No live connector access",
    "No execution authority",
)

ALLOWED_GRAPHIFY_ACCELERATION_OPERATIONS = frozenset(
    {
        "created",
        "transitioned",
        "evidenced",
        "reviewed",
        "learned",
        "linked",
        "superseded",
    }
)
ALLOWED_GRAPHIFY_ACCELERATION_ENTITY_TYPES = frozenset(
    {
        "mission",
        "action",
        "authority_envelope",
        "evidence_packet",
        "connector",
        "system",
    }
)
ALLOWED_GRAPHIFY_DATA_CLASSIFICATIONS = frozenset({"public", "internal", "synthetic"})
ALLOWED_GRAPHIFY_RELATIONSHIPS = frozenset(
    {
        "authorized_by",
        "belongs_to",
        "blocks",
        "depends_on",
        "derived_from",
        "emits",
        "evidenced_by",
        "links_to",
        "produced_by",
        "references",
        "related_to",
        "reviewed_by",
        "supersedes",
    }
)

ALLOWED_GRAPHIFY_APPROVAL_STATES = frozenset(
    {status.value for status in MissionStatus}
    | {status.value for status in EnvelopeStatus}
    | set(RELAY_RECORD_STATUSES)
    | {
        "approved",
        "held",
        "not_applicable",
        "pending",
        "rejected",
        "request_more_info",
    }
)

ENTITY_ID_PREFIXES: Mapping[str, str] = {
    "mission": "mission-",
    "action": "action-",
    "authority_envelope": "env-",
    "evidence_packet": "evidence-",
}

SENSITIVE_REFERENCE_HINTS = (
    ".env",
    "access-token",
    "access_token",
    "accounting-export",
    "api-key",
    "api_key",
    "auth-token",
    "auth_token",
    "audio-blob",
    "audio_blob",
    "client-data",
    "client-data-full",
    "client-payload",
    "client_data",
    "client_data_full",
    "client_payload",
    "client-secret",
    "client_secret",
    "credential",
    "full-payload",
    "full_payload",
    "invoice-export",
    "live-connector",
    "live_connector",
    "m365-export",
    "microsoft-365-export",
    "password",
    "private-key",
    "private_key",
    "quickbooks-export",
    "raw-audio",
    "raw_audio",
    "raw-log",
    "raw_log",
    "recording",
    "sharepoint-content",
    "secret",
    "sharepoint-export",
    "token",
    "transcript-raw",
)

RAW_PAYLOAD_SUMMARY_MARKERS = (
    "full payload",
    "payload dump",
    "raw audio",
    "raw log",
    "raw payload",
    "transcript raw",
    "unredacted payload",
)
SECRET_SUMMARY_MARKERS = (
    "access_token=",
    "api_key=",
    "authorization:",
    "bearer ",
    "begin private key",
    "client_secret=",
    "credential",
    "password=",
    "passwd=",
    "private key",
    "refresh_token=",
    "secret=",
    "token:",
)
SENSITIVE_DATA_SUMMARY_MARKERS = (
    "client data",
    "client-controlled",
    "client payload",
    "client_data",
    "invoice export",
    "quickbooks export",
    "sharepoint export",
)
LIVE_SOURCE_SUMMARY_MARKERS = (
    "live connector",
    "m365 tenant",
    "microsoft 365 content",
    "sharepoint content",
)
BOUNDARY_TEXT_SECRET_MARKERS = (
    "access_token=",
    "api_key=",
    "authorization:",
    "bearer ",
    "begin private key",
    "client_secret=",
    "password=",
    "passwd=",
    "refresh_token=",
    "secret=",
    "token:",
)
GENERATED_GRAPH_REFERENCE_HINTS = (
    "graph-viewer",
    "graph-report",
    "graphify-out/",
    "graphify-workspace/out",
    "workspace/out/graph.json",
)
LOG_REFERENCE_SEGMENTS = frozenset(
    {"log", "logs", "raw-log", "raw-logs", "raw_log", "raw_logs"}
)
AUDIO_REFERENCE_SEGMENTS = frozenset(
    {"audio", "audios", "raw-audio", "raw-audios", "raw_audio", "raw_audios", "recordings"}
)
LOG_REFERENCE_SUFFIXES = (".log",)
AUDIO_REFERENCE_SUFFIXES = (".aac", ".flac", ".m4a", ".mp3", ".ogg", ".wav")


class GraphifyAccelerationValidationError(ValueError):
    """Raised when an acceleration record is unsafe or invalid."""

    def __init__(self, issues: Iterable[str]) -> None:
        self.issues = tuple(issues)
        super().__init__("; ".join(self.issues) or "Graphify acceleration record is invalid.")


@dataclass(frozen=True)
class GraphifyAccelerationSafetyCheck:
    """Safe classification result for one text, reference, or relationship value."""

    field_name: str
    accepted: bool
    indicators: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class GraphifyRelatedEntity:
    """One typed edge from an acceleration record to another GAIL OS entity."""

    relationship: str
    entity_type: str
    entity_id: str

    def to_dict(self) -> dict[str, str]:
        return {
            "relationship": self.relationship,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "GraphifyRelatedEntity":
        return cls(
            relationship=_required_text(payload, "relationship"),
            entity_type=_required_text(payload, "entity_type"),
            entity_id=_required_text(payload, "entity_id"),
        )


@dataclass(frozen=True)
class GraphifyAccelerationRecord:
    """Sanitized fact intended for future Graphify indexing or ingestion."""

    schema_version: str
    record_id: str
    source_system: str
    generated_at: str
    operation: str
    entity_type: str
    entity_id: str
    entity_version: str | None
    title: str
    summary: str
    authority_level: str
    risk_tier: int
    authority_envelope_id: str | None
    approval_state: str | None
    data_classification: str
    source_refs: tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    related_entities: tuple[GraphifyRelatedEntity, ...] = field(default_factory=tuple)
    stop_triggers: tuple[str, ...] = field(default_factory=tuple)
    non_goals: tuple[str, ...] = field(default_factory=tuple)
    contains_raw_payload: bool = False
    fingerprint: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "record_id": self.record_id,
            "source_system": self.source_system,
            "generated_at": self.generated_at,
            "operation": self.operation,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "entity_version": self.entity_version,
            "title": self.title,
            "summary": self.summary,
            "authority_level": self.authority_level,
            "risk_tier": self.risk_tier,
            "authority_envelope_id": self.authority_envelope_id,
            "approval_state": self.approval_state,
            "data_classification": self.data_classification,
            "source_refs": list(self.source_refs),
            "evidence_refs": list(self.evidence_refs),
            "related_entities": [entity.to_dict() for entity in self.related_entities],
            "stop_triggers": list(self.stop_triggers),
            "non_goals": list(self.non_goals),
            "contains_raw_payload": self.contains_raw_payload,
            "fingerprint": self.fingerprint,
        }

    def to_json(self) -> str:
        """Serialize as deterministic, JSON-safe text."""

        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"

    def require_valid(self) -> None:
        """Raise if this record is unsafe for future Graphify consumption."""

        issues = validate_graphify_acceleration_record(self)
        if issues:
            raise GraphifyAccelerationValidationError(issues)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "GraphifyAccelerationRecord":
        return cls(
            schema_version=_required_text(payload, "schema_version"),
            record_id=_required_text(payload, "record_id"),
            source_system=_required_text(payload, "source_system"),
            generated_at=_required_text(payload, "generated_at"),
            operation=_required_text(payload, "operation"),
            entity_type=_required_text(payload, "entity_type"),
            entity_id=_required_text(payload, "entity_id"),
            entity_version=_optional_text(payload, "entity_version"),
            title=_required_text(payload, "title"),
            summary=_required_text(payload, "summary"),
            authority_level=_required_text(payload, "authority_level"),
            risk_tier=_required_int(payload, "risk_tier"),
            authority_envelope_id=_optional_text(payload, "authority_envelope_id"),
            approval_state=_optional_text(payload, "approval_state"),
            data_classification=_required_text(payload, "data_classification"),
            source_refs=_read_text_tuple(payload, "source_refs"),
            evidence_refs=_read_text_tuple(payload, "evidence_refs"),
            related_entities=_read_related_entities(payload),
            stop_triggers=_read_text_tuple(payload, "stop_triggers"),
            non_goals=_read_text_tuple(payload, "non_goals"),
            contains_raw_payload=_required_bool(payload, "contains_raw_payload"),
            fingerprint=_required_text(payload, "fingerprint"),
        )

    @classmethod
    def from_json(cls, document: str) -> "GraphifyAccelerationRecord":
        payload = json.loads(document)
        if not isinstance(payload, Mapping):
            raise ValueError("Graphify acceleration JSON must be an object.")
        return cls.from_dict(payload)


def classify_graphify_summary(value: str, *, field_name: str = "summary") -> GraphifyAccelerationSafetyCheck:
    """Classify safe-summary text without echoing sensitive contents."""

    indicators: list[str] = []
    if not isinstance(value, str):
        return _safety_check(field_name, ("non_text",))
    lowered = value.lower()
    if not value.strip():
        indicators.append("blank_text")
    if any(marker in lowered for marker in RAW_PAYLOAD_SUMMARY_MARKERS):
        indicators.append("raw_payload_marker")
    if any(marker in lowered for marker in SECRET_SUMMARY_MARKERS):
        indicators.append("secret_marker")
    if any(marker in lowered for marker in SENSITIVE_DATA_SUMMARY_MARKERS):
        indicators.append("sensitive_data_label")
    if any(marker in lowered for marker in LIVE_SOURCE_SUMMARY_MARKERS):
        indicators.append("live_source_marker")
    return _safety_check(field_name, indicators)


def classify_graphify_boundary_text(value: str, *, field_name: str) -> GraphifyAccelerationSafetyCheck:
    """Classify stop-trigger and non-goal text while allowing boundary labels."""

    indicators: list[str] = []
    if not isinstance(value, str):
        return _safety_check(field_name, ("non_text",))
    lowered = value.lower()
    if not value.strip():
        indicators.append("blank_text")
    if any(marker in lowered for marker in RAW_PAYLOAD_SUMMARY_MARKERS):
        indicators.append("raw_payload_marker")
    if any(marker in lowered for marker in BOUNDARY_TEXT_SECRET_MARKERS):
        indicators.append("secret_marker")
    return _safety_check(field_name, indicators)


def classify_graphify_reference(value: str, *, field_name: str = "reference") -> GraphifyAccelerationSafetyCheck:
    """Classify whether a reference is relative, local, and non-sensitive."""

    if not isinstance(value, str):
        return _safety_check(field_name, ("non_text",))
    normalized = _normalize_reference(value)
    indicators: list[str] = []
    if not normalized:
        indicators.append("blank_reference")
        return _safety_check(field_name, indicators)
    if "://" in normalized:
        indicators.append("url_reference")
    if normalized.startswith("/") or normalized.startswith("//"):
        indicators.append("absolute_path")
    if ":" in normalized.split("/", 1)[0]:
        indicators.append("drive_letter_path")
    if ".." in normalized.split("/"):
        indicators.append("parent_traversal")
    if _contains_sensitive_text(normalized):
        indicators.append(_sensitive_reference_indicator(normalized))
    if _contains_generated_graph_reference(normalized):
        indicators.append("generated_graph_output")
    if _contains_log_reference(normalized):
        indicators.append("raw_log_reference")
    if _contains_audio_reference(normalized):
        indicators.append("raw_audio_reference")
    return _safety_check(field_name, indicators)


def classify_graphify_relationship(entity: GraphifyRelatedEntity) -> GraphifyAccelerationSafetyCheck:
    """Classify one typed relationship edge."""

    indicators: list[str] = []
    relationship = entity.relationship if isinstance(entity.relationship, str) else ""
    entity_type = entity.entity_type if isinstance(entity.entity_type, str) else ""
    entity_id = entity.entity_id if isinstance(entity.entity_id, str) else ""
    if not relationship or relationship not in ALLOWED_GRAPHIFY_RELATIONSHIPS:
        indicators.append("unknown_relationship")
    if not entity_type or entity_type not in ALLOWED_GRAPHIFY_ACCELERATION_ENTITY_TYPES:
        indicators.append("unknown_entity_type")
    if not entity_id or _validate_entity_id(entity_type, entity_id):
        indicators.append("invalid_entity_id")
    return _safety_check("related_entities", indicators)


def generate_graphify_acceleration_fingerprint(record: GraphifyAccelerationRecord) -> str:
    """Build a deterministic fingerprint for cache and delta comparison.

    `generated_at` is deliberately excluded because it describes when the fact
    was emitted, not the governed fact identity. `fingerprint` is excluded to
    avoid self-reference. All other contract fields are included.
    """

    placeholder = replace(record, fingerprint="sha256-placeholder")
    issues = validate_graphify_acceleration_record(placeholder)
    if issues:
        raise GraphifyAccelerationValidationError(issues)

    payload = record.to_dict()
    for field_name in GRAPHIFY_FINGERPRINT_EXCLUDED_FIELDS:
        payload.pop(field_name, None)
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return f"sha256-{hashlib.sha256(normalized.encode('utf-8')).hexdigest()}"


def with_graphify_acceleration_fingerprint(record: GraphifyAccelerationRecord) -> GraphifyAccelerationRecord:
    """Return a copy of the record with its deterministic fingerprint set."""

    fingerprint = generate_graphify_acceleration_fingerprint(record)
    completed = replace(record, fingerprint=fingerprint)
    completed.require_valid()
    return completed


def build_graphify_action_record(
    action: Action,
    *,
    generated_at: str | None = None,
    entity_version: str | None = None,
    source_refs: Iterable[str] = (),
    evidence_refs: Iterable[str] = (),
    stop_triggers: Iterable[str] = DEFAULT_GRAPHIFY_ACCELERATION_STOP_TRIGGERS,
    non_goals: Iterable[str] = DEFAULT_GRAPHIFY_ACCELERATION_NON_GOALS,
    data_classification: str = "internal",
) -> GraphifyAccelerationRecord:
    """Build a local sanitized graph fact from an Action."""

    _raise_source_validation_errors("action", validate_action(action))
    related_entities = [
        GraphifyRelatedEntity("belongs_to", "mission", action.mission_id),
    ]
    if action.envelope_id:
        related_entities.append(
            GraphifyRelatedEntity("authorized_by", "authority_envelope", action.envelope_id)
        )

    record = GraphifyAccelerationRecord(
        schema_version=GRAPHIFY_ACCELERATION_SCHEMA_VERSION,
        record_id=f"graphify-fact-{action.action_id}",
        source_system=GRAPHIFY_ACCELERATION_SOURCE_SYSTEM,
        generated_at=generated_at or action.created_at,
        operation=_operation_for_action_status(action.status),
        entity_type="action",
        entity_id=action.action_id,
        entity_version=entity_version or action.status.value,
        title=action.title,
        summary=(
            f"Action {action.action_type} is {action.status.value} under "
            f"{action.authority_level} with risk tier {action.risk_tier}."
        ),
        authority_level=action.authority_level,
        risk_tier=action.risk_tier,
        authority_envelope_id=action.envelope_id,
        approval_state=action.status.value,
        data_classification=data_classification,
        source_refs=_as_text_tuple(source_refs),
        evidence_refs=_as_text_tuple(evidence_refs),
        related_entities=tuple(related_entities),
        stop_triggers=_as_text_tuple(stop_triggers),
        non_goals=_as_text_tuple(non_goals),
        contains_raw_payload=False,
        fingerprint="",
    )
    return with_graphify_acceleration_fingerprint(record)


def build_graphify_authority_envelope_record(
    envelope: AuthorityEnvelope,
    *,
    generated_at: str | None = None,
    entity_version: str | None = None,
    source_refs: Iterable[str] = (),
    evidence_refs: Iterable[str] = (),
    non_goals: Iterable[str] = DEFAULT_GRAPHIFY_ACCELERATION_NON_GOALS,
    data_classification: str = "internal",
) -> GraphifyAccelerationRecord:
    """Build a local sanitized graph fact from an AuthorityEnvelope."""

    _raise_source_validation_errors("authority_envelope", validate_authority_envelope(envelope))
    record = GraphifyAccelerationRecord(
        schema_version=GRAPHIFY_ACCELERATION_SCHEMA_VERSION,
        record_id=f"graphify-fact-{envelope.envelope_id}",
        source_system=GRAPHIFY_ACCELERATION_SOURCE_SYSTEM,
        generated_at=generated_at or envelope.granted_at,
        operation="reviewed" if envelope.status == "active" else "transitioned",
        entity_type="authority_envelope",
        entity_id=envelope.envelope_id,
        entity_version=entity_version or envelope.status,
        title=f"Authority boundary for {envelope.domain}",
        summary=(
            f"Authority envelope is {envelope.status} for {envelope.authority_level}/"
            f"{envelope.autonomy_level} in {envelope.domain} with max risk tier "
            f"{envelope.max_risk_tier}."
        ),
        authority_level=envelope.authority_level,
        risk_tier=envelope.max_risk_tier,
        authority_envelope_id=envelope.envelope_id,
        approval_state=envelope.status,
        data_classification=data_classification,
        source_refs=_as_text_tuple(source_refs),
        evidence_refs=_as_text_tuple(evidence_refs),
        related_entities=(
            GraphifyRelatedEntity("belongs_to", "mission", envelope.mission_id),
        ),
        stop_triggers=_as_text_tuple(envelope.stop_conditions),
        non_goals=_as_text_tuple(non_goals),
        contains_raw_payload=False,
        fingerprint="",
    )
    return with_graphify_acceleration_fingerprint(record)


def build_graphify_evidence_record(
    packet: EvidencePacket,
    *,
    generated_at: str | None = None,
    entity_version: str | None = None,
    source_refs: Iterable[str] = (),
    evidence_refs: Iterable[str] | None = None,
    stop_triggers: Iterable[str] = DEFAULT_GRAPHIFY_ACCELERATION_STOP_TRIGGERS,
    non_goals: Iterable[str] = DEFAULT_GRAPHIFY_ACCELERATION_NON_GOALS,
    authority_level: str = "R0",
    risk_tier: int = 0,
    data_classification: str = "internal",
) -> GraphifyAccelerationRecord:
    """Build a local sanitized graph fact from an EvidencePacket."""

    _raise_source_validation_errors("evidence_packet", validate_evidence_packet(packet))
    related_entities = [
        GraphifyRelatedEntity("belongs_to", "mission", packet.mission_id),
        GraphifyRelatedEntity("references", "action", packet.action_id),
    ]
    if packet.envelope_id:
        related_entities.append(
            GraphifyRelatedEntity("authorized_by", "authority_envelope", packet.envelope_id)
        )
    summary = (
        f"Evidence packet reports {packet.result} for {packet.action_type} "
        f"in {packet.execution_mode} mode."
    )
    if packet.outcome_summary.strip():
        summary = f"{summary} {packet.outcome_summary.strip()}"

    record = GraphifyAccelerationRecord(
        schema_version=GRAPHIFY_ACCELERATION_SCHEMA_VERSION,
        record_id=f"graphify-fact-{packet.evidence_id}",
        source_system=GRAPHIFY_ACCELERATION_SOURCE_SYSTEM,
        generated_at=generated_at or packet.created_at,
        operation="evidenced",
        entity_type="evidence_packet",
        entity_id=packet.evidence_id,
        entity_version=entity_version or packet.result,
        title=f"Evidence for {packet.action_type}",
        summary=summary,
        authority_level=authority_level,
        risk_tier=risk_tier,
        authority_envelope_id=packet.envelope_id,
        approval_state="not_applicable",
        data_classification=data_classification,
        source_refs=_as_text_tuple(source_refs),
        evidence_refs=_as_text_tuple(evidence_refs or (f"records/evidence/{packet.evidence_id}",)),
        related_entities=tuple(related_entities),
        stop_triggers=_as_text_tuple(stop_triggers),
        non_goals=_as_text_tuple(non_goals),
        contains_raw_payload=False,
        fingerprint="",
    )
    return with_graphify_acceleration_fingerprint(record)


def validate_graphify_acceleration_record(record: GraphifyAccelerationRecord) -> list[str]:
    """Return safe validation errors for one acceleration record."""

    errors: list[str] = []

    if record.schema_version != GRAPHIFY_ACCELERATION_SCHEMA_VERSION:
        errors.append("schema_version must match the approved Graphify acceleration v1 contract.")
    if not _safe_prefixed_id(record.record_id, "graphify-fact-"):
        errors.append("record_id must use the graphify-fact- prefix and safe ID characters.")
    if record.source_system != GRAPHIFY_ACCELERATION_SOURCE_SYSTEM:
        errors.append("source_system must identify the local Rev 2 system.")
    if not _valid_timestamp(record.generated_at):
        errors.append("generated_at must be a timezone-aware ISO timestamp.")
    if record.operation not in ALLOWED_GRAPHIFY_ACCELERATION_OPERATIONS:
        errors.append("operation is outside the approved Graphify acceleration operation set.")
    if record.entity_type not in ALLOWED_GRAPHIFY_ACCELERATION_ENTITY_TYPES:
        errors.append("entity_type is outside the approved Graphify acceleration entity set.")
    errors.extend(_validate_entity_id(record.entity_type, record.entity_id))
    if record.entity_version is not None:
        if not isinstance(record.entity_version, str):
            errors.append("entity_version must be text when present.")
        elif _contains_sensitive_text(record.entity_version):
            errors.append("entity_version must not contain sensitive markers.")
    if not isinstance(record.title, str) or not record.title.strip():
        errors.append("title is required.")
    else:
        errors.extend(classify_graphify_summary(record.title, field_name="title").reasons)
    if not isinstance(record.summary, str) or not record.summary.strip():
        errors.append("summary is required.")
    else:
        errors.extend(classify_graphify_summary(record.summary, field_name="summary").reasons)
    try:
        AuthorityLevel(record.authority_level)
    except ValueError:
        errors.append("authority_level must be one of R0, R1, R2, R3, R4, or R5.")
    if isinstance(record.risk_tier, bool) or not isinstance(record.risk_tier, int) or not (0 <= record.risk_tier <= 5):
        errors.append("risk_tier must be an integer between 0 and 5.")
    if record.authority_envelope_id is not None and not _safe_prefixed_id(record.authority_envelope_id, "env-"):
        errors.append("authority_envelope_id must use the env- prefix when present.")
    if record.approval_state is not None and record.approval_state not in ALLOWED_GRAPHIFY_APPROVAL_STATES:
        errors.append("approval_state is outside the approved local action or relay state set.")
    if record.data_classification not in ALLOWED_GRAPHIFY_DATA_CLASSIFICATIONS:
        errors.append("data_classification must be public, internal, or synthetic.")
    if not isinstance(record.contains_raw_payload, bool) or record.contains_raw_payload is not False:
        errors.append("contains_raw_payload must be the JSON boolean false.")
    if not isinstance(record.fingerprint, str) or not record.fingerprint.strip():
        errors.append("fingerprint is required.")
    elif _contains_sensitive_text(record.fingerprint) or _unsafe_stable_id(record.fingerprint):
        errors.append("fingerprint must be a safe deterministic identifier.")

    errors.extend(_validate_refs("source_refs", record.source_refs))
    errors.extend(_validate_refs("evidence_refs", record.evidence_refs))
    errors.extend(_validate_related_entities(record.related_entities))
    errors.extend(_validate_text_tuple("stop_triggers", record.stop_triggers))
    errors.extend(_validate_text_tuple("non_goals", record.non_goals))

    return errors


def _required_text(payload: Mapping[str, Any], key: str) -> str:
    if key not in payload or payload[key] is None:
        raise ValueError(f"{key} is required.")
    value = payload[key]
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string.")
    if not value.strip():
        raise ValueError(f"{key} is required.")
    return value.strip()


def _optional_text(payload: Mapping[str, Any], key: str) -> str | None:
    value = payload.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string when present.")
    return value.strip() or None


def _required_bool(payload: Mapping[str, Any], key: str) -> bool:
    if key not in payload:
        raise ValueError(f"{key} is required.")
    value = payload[key]
    if not isinstance(value, bool):
        raise ValueError(f"{key} must be a JSON boolean.")
    return value


def _required_int(payload: Mapping[str, Any], key: str) -> int:
    if key not in payload:
        raise ValueError(f"{key} is required.")
    value = payload[key]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{key} must be an integer.")
    return value


def _read_text_tuple(payload: Mapping[str, Any], key: str) -> tuple[str, ...]:
    value = payload.get(key, ())
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise ValueError(f"{key} must be a JSON array of strings.")
    values: list[str] = []
    for item in value:
        if not isinstance(item, str):
            raise ValueError(f"{key} must contain only strings.")
        text = item.strip()
        if not text:
            raise ValueError(f"{key} must contain only non-empty strings.")
        values.append(text)
    return tuple(values)


def _read_related_entities(payload: Mapping[str, Any]) -> tuple[GraphifyRelatedEntity, ...]:
    value = payload.get("related_entities", ())
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise ValueError("related_entities must be a JSON array of objects.")
    entities: list[GraphifyRelatedEntity] = []
    for item in value:
        if not isinstance(item, Mapping):
            raise ValueError("related_entities must contain JSON objects.")
        entities.append(GraphifyRelatedEntity.from_dict(item))
    return tuple(entities)


def _as_text_tuple(values: Iterable[str]) -> tuple[str, ...]:
    items: list[str] = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError("Graphify acceleration text collections must contain only strings.")
        text = value.strip()
        if not text:
            raise ValueError("Graphify acceleration text collections must not contain blank values.")
        items.append(text)
    return tuple(items)


def _raise_source_validation_errors(source_name: str, errors: Iterable[str]) -> None:
    issues = tuple(errors)
    if issues:
        raise GraphifyAccelerationValidationError(
            [f"{source_name} source object failed validation."] + list(issues)
        )


def _operation_for_action_status(status: MissionStatus) -> str:
    if status == MissionStatus.OBSERVED:
        return "created"
    if status == MissionStatus.EVIDENCED:
        return "evidenced"
    if status == MissionStatus.REVIEWED:
        return "reviewed"
    if status == MissionStatus.LEARNED:
        return "learned"
    return "transitioned"


def _safety_check(field_name: str, indicators: Iterable[str]) -> GraphifyAccelerationSafetyCheck:
    unique_indicators = tuple(dict.fromkeys(indicators))
    reasons = tuple(_indicator_reason(field_name, indicator) for indicator in unique_indicators)
    return GraphifyAccelerationSafetyCheck(
        field_name=field_name,
        accepted=not unique_indicators,
        indicators=unique_indicators,
        reasons=reasons,
    )


def _indicator_reason(field_name: str, indicator: str) -> str:
    if indicator == "non_text":
        return f"{field_name} must contain text values only."
    if indicator == "blank_text":
        return f"{field_name} cannot contain blank values."
    if indicator == "blank_reference":
        return f"{field_name} cannot contain blank references."
    if indicator == "url_reference":
        return f"{field_name} must use relative local references, not URLs."
    if indicator in {"absolute_path", "drive_letter_path"}:
        return f"{field_name} must use relative references, not absolute local paths."
    if indicator == "parent_traversal":
        return f"{field_name} must not use parent traversal."
    if indicator == "env_material":
        return f"{field_name} must not reference environment or secret material."
    if indicator == "secret_reference":
        return f"{field_name} must not reference secrets, credentials, or tokens."
    if indicator == "client_payload_reference":
        return f"{field_name} must not reference client payload material."
    if indicator == "live_connector_reference":
        return f"{field_name} must not reference live connector exports or live-system content."
    if indicator == "generated_graph_output":
        return f"{field_name} must not point at generated graph output."
    if indicator == "raw_log_reference":
        return f"{field_name} must not point at raw logs or log dumps."
    if indicator == "raw_audio_reference":
        return f"{field_name} must not point at raw audio or recordings."
    if indicator == "raw_payload_marker":
        return f"{field_name} must not include raw payload, raw log, raw audio, or unredacted payload markers."
    if indicator == "secret_marker":
        return f"{field_name} must not include secret, credential, token, password, or private-key markers."
    if indicator == "sensitive_data_label":
        return f"{field_name} must not include client, finance, billing, or external-system payload labels."
    if indicator == "live_source_marker":
        return f"{field_name} must not include live connector or live business-system content markers."
    if indicator == "unknown_relationship":
        return "related_entities relationships must use approved typed edge names."
    if indicator == "unknown_entity_type":
        return "related_entities entity_type values must use approved acceleration entity types."
    if indicator == "invalid_entity_id":
        return "related_entities entity_id values must be stable, non-sensitive GAIL OS identifiers."
    return f"{field_name} is outside the approved Graphify acceleration safety boundary."


def _valid_timestamp(value: str) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _validate_entity_id(entity_type: str, entity_id: str) -> list[str]:
    if not isinstance(entity_id, str):
        return ["entity_id must be a stable text identifier."]
    if not isinstance(entity_type, str):
        return ["entity_type must be text."]
    if not entity_id.strip():
        return ["entity_id is required."]
    if _unsafe_stable_id(entity_id) or _contains_sensitive_text(entity_id):
        return ["entity_id must be a stable, non-sensitive GAIL OS identifier."]

    expected_prefix = ENTITY_ID_PREFIXES.get(entity_type)
    if expected_prefix and not entity_id.startswith(expected_prefix):
        return [f"{entity_type} entity_id must use the {expected_prefix} prefix."]
    if entity_type == "system" and entity_id != GRAPHIFY_ACCELERATION_SOURCE_SYSTEM:
        return ["system entity_id must identify the local Rev 2 system."]
    return []


def _validate_refs(field_name: str, refs: Iterable[str]) -> list[str]:
    errors: list[str] = []
    for ref in refs:
        errors.extend(classify_graphify_reference(ref, field_name=field_name).reasons)
    return errors


def _validate_related_entities(entities: Iterable[GraphifyRelatedEntity]) -> list[str]:
    errors: list[str] = []
    for entity in entities:
        errors.extend(classify_graphify_relationship(entity).reasons)
    return errors


def _validate_text_tuple(field_name: str, values: Iterable[str]) -> list[str]:
    errors: list[str] = []
    for value in values:
        errors.extend(classify_graphify_boundary_text(value, field_name=field_name).reasons)
    return errors


def _safe_prefixed_id(value: str, prefix: str) -> bool:
    if not isinstance(value, str):
        return False
    return value.startswith(prefix) and not _unsafe_stable_id(value) and not _contains_sensitive_text(value)


def _unsafe_stable_id(value: str) -> bool:
    if not isinstance(value, str):
        return True
    normalized = value.strip().replace("\\", "/")
    if not normalized:
        return True
    if normalized.startswith("/") or normalized.startswith("//"):
        return True
    if ":" in normalized.split("/", 1)[0]:
        return True
    if ".." in normalized.split("/"):
        return True
    return any(character.isspace() for character in normalized)


def _unsafe_ref(value: str) -> bool:
    normalized = _normalize_reference(value)
    if not normalized:
        return True
    if normalized.startswith("/") or normalized.startswith("//"):
        return True
    if ":" in normalized.split("/", 1)[0]:
        return True
    return ".." in normalized.split("/")


def _contains_sensitive_text(value: str) -> bool:
    if not isinstance(value, str):
        return True
    lowered = _normalize_reference(value)
    return any(hint in lowered for hint in SENSITIVE_REFERENCE_HINTS)


def _contains_sensitive_summary(value: str) -> bool:
    return not classify_graphify_summary(value).accepted


def _normalize_reference(value: str) -> str:
    return value.strip().replace("\\", "/").lower()


def _path_segments(value: str) -> tuple[str, ...]:
    return tuple(segment for segment in _normalize_reference(value).split("/") if segment)


def _contains_generated_graph_reference(value: str) -> bool:
    normalized = _normalize_reference(value)
    return (
        any(hint in normalized for hint in GENERATED_GRAPH_REFERENCE_HINTS)
        or normalized.endswith("/graph.json")
        or normalized == "graph.json"
    )


def _contains_log_reference(value: str) -> bool:
    normalized = _normalize_reference(value)
    return normalized.endswith(LOG_REFERENCE_SUFFIXES) or any(
        segment in LOG_REFERENCE_SEGMENTS for segment in _path_segments(value)
    )


def _contains_audio_reference(value: str) -> bool:
    normalized = _normalize_reference(value)
    return normalized.endswith(AUDIO_REFERENCE_SUFFIXES) or any(
        segment in AUDIO_REFERENCE_SEGMENTS for segment in _path_segments(value)
    )


def _sensitive_reference_indicator(value: str) -> str:
    normalized = _normalize_reference(value)
    if ".env" in normalized:
        return "env_material"
    if any(
        marker in normalized
        for marker in (
            "client-data",
            "client_data",
            "client-payload",
            "client_payload",
            "client-data-full",
            "client_data_full",
        )
    ):
        return "client_payload_reference"
    if any(
        marker in normalized
        for marker in (
            "live-connector",
            "live_connector",
            "m365-export",
            "microsoft-365-export",
            "sharepoint-content",
            "sharepoint-export",
            "quickbooks-export",
            "accounting-export",
            "invoice-export",
        )
    ):
        return "live_connector_reference"
    return "secret_reference"


__all__ = [
    "ALLOWED_GRAPHIFY_ACCELERATION_ENTITY_TYPES",
    "ALLOWED_GRAPHIFY_ACCELERATION_OPERATIONS",
    "ALLOWED_GRAPHIFY_APPROVAL_STATES",
    "ALLOWED_GRAPHIFY_DATA_CLASSIFICATIONS",
    "ALLOWED_GRAPHIFY_RELATIONSHIPS",
    "DEFAULT_GRAPHIFY_ACCELERATION_NON_GOALS",
    "DEFAULT_GRAPHIFY_ACCELERATION_STOP_TRIGGERS",
    "GRAPHIFY_ACCELERATION_SCHEMA_VERSION",
    "GRAPHIFY_ACCELERATION_SOURCE_SYSTEM",
    "GRAPHIFY_FINGERPRINT_EXCLUDED_FIELDS",
    "GraphifyAccelerationRecord",
    "GraphifyAccelerationSafetyCheck",
    "GraphifyAccelerationValidationError",
    "GraphifyRelatedEntity",
    "build_graphify_action_record",
    "build_graphify_authority_envelope_record",
    "build_graphify_evidence_record",
    "classify_graphify_boundary_text",
    "classify_graphify_reference",
    "classify_graphify_relationship",
    "classify_graphify_summary",
    "generate_graphify_acceleration_fingerprint",
    "validate_graphify_acceleration_record",
    "with_graphify_acceleration_fingerprint",
]
