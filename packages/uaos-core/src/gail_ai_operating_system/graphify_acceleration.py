"""Local contract for future Graphify acceleration facts.

This module defines safe, inspectable records that GAIL OS can emit later so
Graphify does not need to rediscover governed relationships from raw source or
long documents. It does not persist records, call Graphify, expose transport,
or grant execution authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import json
from typing import Any, Iterable, Mapping

from .authority_envelope import AuthorityLevel
from .mission import MissionStatus
from .relay_store import RELAY_RECORD_STATUSES


GRAPHIFY_ACCELERATION_SCHEMA_VERSION = "rev2.graphify-acceleration.v1"
GRAPHIFY_ACCELERATION_SOURCE_SYSTEM = "gail-ai-operating-system-rev-2"

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
    "accounting-export",
    "api-key",
    "api_key",
    "audio-blob",
    "audio_blob",
    "client-data",
    "client_data",
    "credential",
    "invoice-export",
    "live-connector",
    "live_connector",
    "private-key",
    "private_key",
    "raw-audio",
    "raw_audio",
    "raw-log",
    "raw_log",
    "secret",
    "sharepoint-export",
    "token",
)

SENSITIVE_SUMMARY_MARKERS = (
    "api_key=",
    "begin private key",
    "client data full",
    "client_secret=",
    "password=",
    "passwd=",
    "raw audio",
    "raw log",
    "token:",
    "unredacted payload",
)


class GraphifyAccelerationValidationError(ValueError):
    """Raised when an acceleration record is unsafe or invalid."""

    def __init__(self, issues: Iterable[str]) -> None:
        self.issues = tuple(issues)
        super().__init__("; ".join(self.issues) or "Graphify acceleration record is invalid.")


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
    if record.entity_version is not None and _contains_sensitive_text(record.entity_version):
        errors.append("entity_version must not contain sensitive markers.")
    if not record.title.strip():
        errors.append("title is required.")
    if not record.summary.strip():
        errors.append("summary is required.")
    elif _contains_sensitive_summary(record.summary):
        errors.append("summary must not include raw payload, secret, credential, raw log, raw audio, or client payload markers.")
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
    if not record.fingerprint.strip():
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
    return tuple(str(item).strip() for item in value if isinstance(item, str) and item.strip())


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


def _valid_timestamp(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _validate_entity_id(entity_type: str, entity_id: str) -> list[str]:
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
        if _unsafe_ref(ref) or _contains_sensitive_text(ref):
            errors.append(f"{field_name} must contain only relative non-sensitive references.")
            break
    return errors


def _validate_related_entities(entities: Iterable[GraphifyRelatedEntity]) -> list[str]:
    errors: list[str] = []
    for entity in entities:
        if entity.relationship not in ALLOWED_GRAPHIFY_RELATIONSHIPS:
            errors.append("related_entities relationships must use approved typed edge names.")
        if entity.entity_type not in ALLOWED_GRAPHIFY_ACCELERATION_ENTITY_TYPES:
            errors.append("related_entities entity_type values must use approved acceleration entity types.")
        errors.extend(_validate_entity_id(entity.entity_type, entity.entity_id))
    return errors


def _validate_text_tuple(field_name: str, values: Iterable[str]) -> list[str]:
    errors: list[str] = []
    for value in values:
        if not value.strip():
            errors.append(f"{field_name} cannot contain blank values.")
            break
        if _contains_sensitive_summary(value):
            errors.append(f"{field_name} must not contain raw payload, secret, credential, raw log, raw audio, or client payload markers.")
            break
    return errors


def _safe_prefixed_id(value: str, prefix: str) -> bool:
    return value.startswith(prefix) and not _unsafe_stable_id(value) and not _contains_sensitive_text(value)


def _unsafe_stable_id(value: str) -> bool:
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
    normalized = value.strip().replace("\\", "/")
    if not normalized:
        return True
    if normalized.startswith("/") or normalized.startswith("//"):
        return True
    if ":" in normalized.split("/", 1)[0]:
        return True
    return ".." in normalized.split("/")


def _contains_sensitive_text(value: str) -> bool:
    lowered = value.strip().replace("\\", "/").lower()
    return any(hint in lowered for hint in SENSITIVE_REFERENCE_HINTS)


def _contains_sensitive_summary(value: str) -> bool:
    lowered = value.lower()
    return any(marker in lowered for marker in SENSITIVE_SUMMARY_MARKERS)


__all__ = [
    "ALLOWED_GRAPHIFY_ACCELERATION_ENTITY_TYPES",
    "ALLOWED_GRAPHIFY_ACCELERATION_OPERATIONS",
    "ALLOWED_GRAPHIFY_APPROVAL_STATES",
    "ALLOWED_GRAPHIFY_DATA_CLASSIFICATIONS",
    "ALLOWED_GRAPHIFY_RELATIONSHIPS",
    "GRAPHIFY_ACCELERATION_SCHEMA_VERSION",
    "GRAPHIFY_ACCELERATION_SOURCE_SYSTEM",
    "GraphifyAccelerationRecord",
    "GraphifyAccelerationValidationError",
    "GraphifyRelatedEntity",
    "validate_graphify_acceleration_record",
]
