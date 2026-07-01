"""Shared read model and CNS trace spine for GAIL OS.

This module owns the local, append-only trace events used by operator
surfaces. It deliberately stores references and safe summaries rather than raw
provider payloads, and it does not call external systems.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import json
import os
from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4

from .evidence_packet import EvidencePacket
from .trace_identity import (
    CNS_TRACE_ID_PATTERN,
    create_cns_trace_id,
    ensure_cns_trace_id,
    utc_z_timestamp,
    validate_cns_trace_id,
)


TRACE_EVENT_SCHEMA_VERSION = "rev2.trace-event.v1"
TRACE_READ_MODEL_SCHEMA_VERSION = "rev2.trace-read-model.v1"
SHARED_READ_MODEL_SCHEMA_VERSION = "rev2.shared-read-model.v1"

ALLOWED_TRACE_EVENT_TYPES = frozenset(
    {
        "mission.created",
        "action.validated",
        "authority.override_requested",
        "approval.decided",
        "evidence.recorded",
        "graphify.fact_candidate_prepared",
        "tactile.dry_run_recorded",
    }
)

_SECRET_TEXT_MARKERS = (
    "access_token=",
    "api_key=",
    "authorization:",
    "bearer ",
    "client_secret=",
    "password=",
    "private key",
    "refresh_token=",
    "secret=",
    "token:",
)


@dataclass(frozen=True)
class TraceEvent:
    """One persisted event in the local CNS trace ledger."""

    event_id: str
    cns_trace_id: str
    event_type: str
    occurred_at: str
    source_system: str
    source_ref: str
    summary: str
    mission_id: str | None = None
    action_id: str | None = None
    evidence_id: str | None = None
    authority_ref: str | None = None
    status: str | None = None
    risk_tier: int | None = None
    idempotency_key: str | None = None
    duplicate_of_event_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def duplicate_detected(self) -> bool:
        return self.duplicate_of_event_id is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": TRACE_EVENT_SCHEMA_VERSION,
            "event_id": self.event_id,
            "cns_trace_id": self.cns_trace_id,
            "event_type": self.event_type,
            "occurred_at": self.occurred_at,
            "source_system": self.source_system,
            "source_ref": self.source_ref,
            "summary": self.summary,
            "mission_id": self.mission_id,
            "action_id": self.action_id,
            "evidence_id": self.evidence_id,
            "authority_ref": self.authority_ref,
            "status": self.status,
            "risk_tier": self.risk_tier,
            "idempotency_key": self.idempotency_key,
            "duplicate_detected": self.duplicate_detected,
            "duplicate_of_event_id": self.duplicate_of_event_id,
            "metadata": _safe_metadata(self.metadata),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "TraceEvent":
        schema_version = str(payload.get("schema_version", TRACE_EVENT_SCHEMA_VERSION))
        if schema_version != TRACE_EVENT_SCHEMA_VERSION:
            raise ValueError("TraceEvent schema_version is not supported.")
        risk_tier = payload.get("risk_tier")
        metadata = payload.get("metadata", {})
        if not isinstance(metadata, Mapping):
            raise ValueError("metadata must be a JSON object.")
        return cls(
            event_id=str(payload["event_id"]),
            cns_trace_id=str(payload["cns_trace_id"]),
            event_type=str(payload["event_type"]),
            occurred_at=str(payload["occurred_at"]),
            source_system=str(payload["source_system"]),
            source_ref=str(payload["source_ref"]),
            summary=str(payload["summary"]),
            mission_id=_optional_text(payload, "mission_id"),
            action_id=_optional_text(payload, "action_id"),
            evidence_id=_optional_text(payload, "evidence_id"),
            authority_ref=_optional_text(payload, "authority_ref"),
            status=_optional_text(payload, "status"),
            risk_tier=int(risk_tier) if risk_tier is not None else None,
            idempotency_key=_optional_text(payload, "idempotency_key"),
            duplicate_of_event_id=_optional_text(payload, "duplicate_of_event_id"),
            metadata=dict(metadata),
        )


class LocalTraceEventStore:
    """Small JSON-backed append-only event store."""

    def __init__(self, base_path: str | Path) -> None:
        self._base_path = Path(base_path)

    @property
    def base_path(self) -> Path:
        return self._base_path

    def path_for(self, event_id: str) -> Path:
        safe_id = event_id.strip()
        if not _safe_prefixed_id(safe_id, "event-"):
            raise ValueError("event_id is not safe for local storage.")
        return self._base_path / f"{safe_id}.json"

    def save(self, event: TraceEvent) -> Path:
        errors = validate_trace_event(event)
        if errors:
            raise ValueError(f"TraceEvent is invalid: {'; '.join(errors)}")
        self._base_path.mkdir(parents=True, exist_ok=True)
        path = self.path_for(event.event_id)
        path.write_text(json.dumps(event.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def read(self, event_id: str) -> TraceEvent:
        return TraceEvent.from_dict(json.loads(self.path_for(event_id).read_text(encoding="utf-8")))

    def list_recent(self, *, limit: int = 25) -> tuple[TraceEvent, ...]:
        events = self._load_all()
        events.sort(key=lambda event: event.occurred_at, reverse=True)
        return tuple(events[:limit])

    def find_by_trace(self, cns_trace_id: str) -> tuple[TraceEvent, ...]:
        _require_valid_cns_trace_id(cns_trace_id)
        events = [event for event in self._load_all() if event.cns_trace_id == cns_trace_id]
        events.sort(key=lambda event: (event.occurred_at, event.duplicate_detected, event.event_id))
        return tuple(events)

    def find_first_by_idempotency_key(self, idempotency_key: str | None) -> TraceEvent | None:
        if not idempotency_key:
            return None
        matches = [event for event in self._load_all() if event.idempotency_key == idempotency_key]
        if not matches:
            return None
        matches.sort(key=lambda event: event.occurred_at)
        return matches[0]

    def _load_all(self) -> list[TraceEvent]:
        if not self._base_path.exists():
            return []
        events: list[TraceEvent] = []
        for path in sorted(self._base_path.glob("event-*.json")):
            try:
                events.append(TraceEvent.from_dict(json.loads(path.read_text(encoding="utf-8"))))
            except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
                continue
        return events


def default_store_root() -> Path:
    return Path(os.environ.get("GAIL_OS_STORE_PATH", "./local_store"))


def default_trace_event_store_path(store_root: str | Path | None = None) -> Path:
    root = Path(store_root) if store_root is not None else default_store_root()
    return root / "trace-events"


def default_evidence_store_path(store_root: str | Path | None = None) -> Path:
    root = Path(store_root) if store_root is not None else default_store_root()
    return root / "evidence"


def create_trace_event(
    *,
    cns_trace_id: str,
    event_type: str,
    source_system: str,
    source_ref: str,
    summary: str,
    occurred_at: str | None = None,
    mission_id: str | None = None,
    action_id: str | None = None,
    evidence_id: str | None = None,
    authority_ref: str | None = None,
    status: str | None = None,
    risk_tier: int | None = None,
    idempotency_key: str | None = None,
    duplicate_of_event_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> TraceEvent:
    event = TraceEvent(
        event_id=f"event-{uuid4().hex[:12]}",
        cns_trace_id=ensure_cns_trace_id(cns_trace_id),
        event_type=event_type,
        occurred_at=occurred_at or utc_z_timestamp(),
        source_system=source_system,
        source_ref=source_ref,
        summary=summary,
        mission_id=mission_id,
        action_id=action_id,
        evidence_id=evidence_id,
        authority_ref=authority_ref,
        status=status,
        risk_tier=risk_tier,
        idempotency_key=idempotency_key,
        duplicate_of_event_id=duplicate_of_event_id,
        metadata=_safe_metadata(metadata or {}),
    )
    errors = validate_trace_event(event)
    if errors:
        raise ValueError("; ".join(errors))
    return event


def validate_trace_event(event: TraceEvent) -> list[str]:
    errors: list[str] = []
    if not _safe_prefixed_id(event.event_id, "event-"):
        errors.append("event_id must use the event- prefix and safe characters.")
    errors.extend(validate_cns_trace_id(event.cns_trace_id, required=True))
    if event.event_type not in ALLOWED_TRACE_EVENT_TYPES:
        errors.append("event_type is outside the approved trace event set.")
    if not _valid_timestamp(event.occurred_at):
        errors.append("occurred_at must be a timezone-aware ISO timestamp.")
    for field_name, value in {
        "source_system": event.source_system,
        "source_ref": event.source_ref,
        "summary": event.summary,
    }.items():
        if not value.strip():
            errors.append(f"{field_name} is required.")
        if _contains_secret_marker(value):
            errors.append(f"{field_name} must not contain secret markers.")
    errors.extend(_validate_optional_prefix("mission_id", event.mission_id, "mission-"))
    errors.extend(_validate_optional_prefix("action_id", event.action_id, "action-"))
    errors.extend(_validate_optional_prefix("evidence_id", event.evidence_id, "evidence-"))
    if event.authority_ref is not None and not (
        _safe_prefixed_id(event.authority_ref, "env-")
        or _safe_prefixed_id(event.authority_ref, "override-")
        or _safe_prefixed_id(event.authority_ref, "aprv-")
    ):
        errors.append("authority_ref must use env-, override-, or aprv- when present.")
    if event.risk_tier is not None and (
        isinstance(event.risk_tier, bool) or not isinstance(event.risk_tier, int) or not 0 <= event.risk_tier <= 5
    ):
        errors.append("risk_tier must be an integer between 0 and 5 when present.")
    if event.idempotency_key is not None and (
        not event.idempotency_key.strip() or _contains_secret_marker(event.idempotency_key)
    ):
        errors.append("idempotency_key must be non-empty and secret-free when present.")
    if event.duplicate_of_event_id is not None and not _safe_prefixed_id(event.duplicate_of_event_id, "event-"):
        errors.append("duplicate_of_event_id must use the event- prefix when present.")
    try:
        _safe_metadata(event.metadata)
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def recent_evidence_refs(
    *,
    limit: int = 25,
    store_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    packets = _load_evidence_packets(store_root=store_root)
    packets.sort(key=lambda packet: packet.created_at, reverse=True)
    return [_evidence_ref(packet) for packet in packets[:limit]]


def evidence_refs_for_mission(
    mission_id: str,
    *,
    store_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    packets = [packet for packet in _load_evidence_packets(store_root=store_root) if packet.mission_id == mission_id]
    packets.sort(key=lambda packet: packet.created_at)
    return [_evidence_ref(packet) for packet in packets]


def evidence_refs_for_trace(
    cns_trace_id: str,
    *,
    store_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    _require_valid_cns_trace_id(cns_trace_id)
    packets = [packet for packet in _load_evidence_packets(store_root=store_root) if packet.cns_trace_id == cns_trace_id]
    packets.sort(key=lambda packet: packet.created_at)
    return [_evidence_ref(packet) for packet in packets]


def mission_refs_for_trace(
    cns_trace_id: str,
    *,
    store_root: str | Path | None = None,
) -> list[dict[str, Any]]:
    _require_valid_cns_trace_id(cns_trace_id)
    root = Path(store_root) if store_root is not None else default_store_root()
    mission_path = root / "missions"
    if not mission_path.exists():
        return []
    refs: list[dict[str, Any]] = []
    for path in sorted(mission_path.glob("mission-*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if payload.get("cns_trace_id") != cns_trace_id:
            continue
        refs.append(
            {
                "mission_id": payload.get("mission_id"),
                "request_id": payload.get("request_id"),
                "domain": payload.get("domain"),
                "status": payload.get("status"),
                "created_at": payload.get("created_at"),
                "data_classification": payload.get("data_classification"),
            }
        )
    return refs


def build_trace_read_model(
    cns_trace_id: str,
    *,
    store_root: str | Path | None = None,
) -> dict[str, Any]:
    _require_valid_cns_trace_id(cns_trace_id)
    root = Path(store_root) if store_root is not None else default_store_root()
    store = LocalTraceEventStore(default_trace_event_store_path(root))
    events = store.find_by_trace(cns_trace_id)
    evidence_refs = evidence_refs_for_trace(cns_trace_id, store_root=root)
    mission_refs = mission_refs_for_trace(cns_trace_id, store_root=root)
    mission_ids = sorted(
        {
            str(value)
            for value in (
                [event.mission_id for event in events]
                + [ref.get("mission_id") for ref in evidence_refs]
                + [ref.get("mission_id") for ref in mission_refs]
            )
            if value
        }
    )
    action_ids = sorted({str(value) for value in [event.action_id for event in events] + [ref.get("action_id") for ref in evidence_refs] if value})
    evidence_ids = sorted({str(value) for value in [event.evidence_id for event in events] + [ref.get("evidence_id") for ref in evidence_refs] if value})
    authority_refs = sorted({str(event.authority_ref) for event in events if event.authority_ref})
    return {
        "schema_version": TRACE_READ_MODEL_SCHEMA_VERSION,
        "cns_trace_id": cns_trace_id,
        "found": bool(events or evidence_refs or mission_refs),
        "mission_ids": mission_ids,
        "action_ids": action_ids,
        "evidence_ids": evidence_ids,
        "authority_refs": authority_refs,
        "mission_refs": mission_refs,
        "evidence_refs": evidence_refs,
        "events": [event.to_dict() for event in events],
    }


def _load_evidence_packets(*, store_root: str | Path | None = None) -> list[EvidencePacket]:
    store = default_evidence_store_path(store_root)
    if not store.exists():
        return []
    packets: list[EvidencePacket] = []
    for path in sorted(store.glob("evidence-*.json")):
        try:
            packets.append(EvidencePacket.from_dict(json.loads(path.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
            continue
    return packets


def _require_valid_cns_trace_id(cns_trace_id: str) -> None:
    errors = validate_cns_trace_id(cns_trace_id, required=True)
    if errors:
        raise ValueError("; ".join(errors))


def _evidence_ref(packet: EvidencePacket) -> dict[str, Any]:
    return {
        "evidence_id": packet.evidence_id,
        "cns_trace_id": packet.cns_trace_id,
        "mission_id": packet.mission_id,
        "action_id": packet.action_id,
        "result": packet.result,
        "execution_mode": packet.execution_mode,
        "action_type": packet.action_type,
        "created_at": packet.created_at,
        "outcome_summary": packet.outcome_summary,
    }


def _safe_metadata(metadata: Mapping[str, Any]) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    for key, value in metadata.items():
        key_text = str(key).strip()
        if not key_text:
            raise ValueError("metadata keys must be non-empty.")
        if _contains_secret_marker(key_text):
            raise ValueError("metadata keys must not contain secret markers.")
        safe[key_text] = _safe_metadata_value(value)
    return safe


def _safe_metadata_value(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        if _contains_secret_marker(value):
            return "[redacted-sensitive-marker]"
        return value[:500]
    if isinstance(value, Mapping):
        return _safe_metadata(value)
    if isinstance(value, (list, tuple)):
        return [_safe_metadata_value(item) for item in value[:20]]
    return str(value)[:500]


def _optional_text(payload: Mapping[str, Any], key: str) -> str | None:
    value = payload.get(key)
    if value is None:
        return None
    return str(value)


def _valid_timestamp(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _validate_optional_prefix(field_name: str, value: str | None, prefix: str) -> list[str]:
    if value is None:
        return []
    if not _safe_prefixed_id(value, prefix):
        return [f"{field_name} must use the {prefix} prefix when present."]
    return []


def _safe_prefixed_id(value: str, prefix: str) -> bool:
    if not isinstance(value, str):
        return False
    normalized = value.strip()
    if not normalized.startswith(prefix):
        return False
    if any(part in normalized for part in ("/", "\\", "..")):
        return False
    return all(character.isalnum() or character in {"-", "_"} for character in normalized)


def _contains_secret_marker(value: str) -> bool:
    lowered = value.lower()
    return any(marker in lowered for marker in _SECRET_TEXT_MARKERS)


__all__ = [
    "ALLOWED_TRACE_EVENT_TYPES",
    "CNS_TRACE_ID_PATTERN",
    "SHARED_READ_MODEL_SCHEMA_VERSION",
    "TRACE_EVENT_SCHEMA_VERSION",
    "TRACE_READ_MODEL_SCHEMA_VERSION",
    "LocalTraceEventStore",
    "TraceEvent",
    "build_trace_read_model",
    "create_cns_trace_id",
    "create_trace_event",
    "default_evidence_store_path",
    "default_store_root",
    "default_trace_event_store_path",
    "ensure_cns_trace_id",
    "evidence_refs_for_mission",
    "evidence_refs_for_trace",
    "mission_refs_for_trace",
    "recent_evidence_refs",
    "utc_z_timestamp",
    "validate_cns_trace_id",
    "validate_trace_event",
]
