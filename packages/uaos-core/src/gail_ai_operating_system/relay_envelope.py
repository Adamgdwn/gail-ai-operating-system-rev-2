"""Local relay envelope validation for future Rev 2 cockpit records."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable, Mapping

from .connector_registry import initial_connector_profiles
from .mission_spine import MissionAction, STOP_ACTION_TYPES


PROJECT_ID = "gail-ai-operating-system-rev-2"
SCHEMA_VERSION = "rev2.relay-envelope.v1"

RECORD_TYPES = frozenset({"intent", "approval", "status", "evidence", "handoff"})
DEVICE_ROLES = frozenset(
    {
        "android_phone_cockpit",
        "android_tablet_cockpit",
        "browser_cockpit",
        "windows_operator_workspace",
        "windows_trusted_worker",
        "linux_trusted_worker",
        "graphify_knowledge_spoke",
        "viewer",
    }
)
APPROVAL_LEVELS = frozenset({"A0", "A1", "A2", "A3"})
SURFACE_APPROVAL_CEILINGS: Mapping[str, str] = {
    "android_phone_cockpit": "A2",
    "android_tablet_cockpit": "A2",
    "browser_cockpit": "A2",
    "viewer": "A0",
    "graphify_knowledge_spoke": "A1",
    "windows_trusted_worker": "A1",
    "linux_trusted_worker": "A1",
}

SAFE_RELAY_CAPABILITIES = frozenset(
    {
        "intent-capture",
        "approval",
        "status-read",
        "evidence-summary",
        "handoff-summary",
        "pause",
        "resume",
        "cancel",
        "redirect",
        "planning-only",
        "inventory-only",
        "metadata-only",
        "local-validation",
        "readiness-check",
    }
)
LIVE_RELAY_CAPABILITIES = frozenset(
    {
        "content-read",
        "summarize",
        "draft-only",
        "prepare-action",
        "execute-after-approval",
        "send-message",
        "write",
        "admin-change",
        "billing-action",
        "delete",
        "external-communication",
    }
)
ACTIVE_RELAY_STATUSES = frozenset({"draft", "proposed", "active", "approved", "paused"})
LOCAL_RELAY_TRANSPORTS = frozenset({"local-file"})
PLANNED_WORKER_MODES = frozenset({"not-started", "not-applicable", "outbound-planned", "outbound-pull-planned"})
SAFE_GRAPHIFY_CANDIDATE_STATUSES = frozenset({"", "none", "candidate", "proposed", "read-only", "needs-review", "read-only-candidate"})
SAFE_CLIENT_GATEWAY_STAGES = frozenset({"", "planning", "readiness-check"})

REQUIRED_RELAY_STOP_TRIGGERS = frozenset(
    {
        "portal_or_relay_live_action",
        "hosted_relay_or_worker_action",
        "secret_exposure",
        "client_data_access",
        "raw_payload_retention",
    }
)

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
class RelayEnvelope:
    """A future cockpit or worker relay record before hosted relay exists."""

    envelope_id: str
    record_type: str
    project_id: str
    request_id: str
    mission_id: str
    actor_id: str
    device_id: str
    device_role: str
    approval_level: str
    requested_capability: str
    connector_profile_ids: tuple[str, ...]
    stop_triggers: tuple[str, ...]
    observed_state_refs: Mapping[str, str]
    safe_summary: Mapping[str, Any]
    evidence_refs: tuple[str, ...]
    schema_version: str = SCHEMA_VERSION
    relay_status: str = "proposed"
    relay_transport: str = "local-file"
    worker_connection_mode: str = "not-started"
    graph_registry_id: str = ""
    graph_snapshot_ref: str = ""
    graph_observed_at: str = ""
    filesystem_scope_refs: tuple[str, ...] = ()
    approval_expires_at: str = ""
    graphify_handoff_candidate_status: str = ""
    client_gateway_lifecycle_stage: str = ""
    contains_client_data_full_payload: bool = False
    raw_audio_retained: bool = False
    live_action_requested: bool = False
    live_action_approved: bool = False
    conflict_markers: tuple[str, ...] = ()
    superseded_by_envelope_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "envelope_id": self.envelope_id,
            "record_type": self.record_type,
            "project_id": self.project_id,
            "request_id": self.request_id,
            "mission_id": self.mission_id,
            "actor_id": self.actor_id,
            "device_id": self.device_id,
            "device_role": self.device_role,
            "approval_level": self.approval_level,
            "requested_capability": self.requested_capability,
            "connector_profile_ids": list(self.connector_profile_ids),
            "stop_triggers": list(self.stop_triggers),
            "observed_state_refs": dict(self.observed_state_refs),
            "safe_summary": dict(self.safe_summary),
            "evidence_refs": list(self.evidence_refs),
            "relay_status": self.relay_status,
            "relay_transport": self.relay_transport,
            "worker_connection_mode": self.worker_connection_mode,
            "graph_registry_id": self.graph_registry_id,
            "graph_snapshot_ref": self.graph_snapshot_ref,
            "graph_observed_at": self.graph_observed_at,
            "filesystem_scope_refs": list(self.filesystem_scope_refs),
            "approval_expires_at": self.approval_expires_at,
            "graphify_handoff_candidate_status": self.graphify_handoff_candidate_status,
            "client_gateway_lifecycle_stage": self.client_gateway_lifecycle_stage,
            "contains_client_data_full_payload": self.contains_client_data_full_payload,
            "raw_audio_retained": self.raw_audio_retained,
            "live_action_requested": self.live_action_requested,
            "live_action_approved": self.live_action_approved,
            "conflict_markers": list(self.conflict_markers),
            "superseded_by_envelope_id": self.superseded_by_envelope_id,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "RelayEnvelope":
        return cls(
            schema_version=str(payload.get("schema_version", SCHEMA_VERSION)),
            envelope_id=str(payload["envelope_id"]),
            record_type=str(payload["record_type"]),
            project_id=str(payload["project_id"]),
            request_id=str(payload["request_id"]),
            mission_id=str(payload["mission_id"]),
            actor_id=str(payload["actor_id"]),
            device_id=str(payload["device_id"]),
            device_role=str(payload["device_role"]),
            approval_level=str(payload["approval_level"]),
            requested_capability=str(payload["requested_capability"]),
            connector_profile_ids=read_text_tuple(payload, "connector_profile_ids"),
            stop_triggers=read_text_tuple(payload, "stop_triggers"),
            observed_state_refs=read_text_mapping(payload, "observed_state_refs"),
            safe_summary=read_mapping(payload, "safe_summary"),
            evidence_refs=read_text_tuple(payload, "evidence_refs"),
            relay_status=str(payload.get("relay_status", "proposed")),
            relay_transport=str(payload.get("relay_transport", "local-file")),
            worker_connection_mode=str(payload.get("worker_connection_mode", "not-started")),
            graph_registry_id=str(payload.get("graph_registry_id", "")),
            graph_snapshot_ref=str(payload.get("graph_snapshot_ref", "")),
            graph_observed_at=str(payload.get("graph_observed_at", "")),
            filesystem_scope_refs=read_text_tuple(payload, "filesystem_scope_refs", default=()),
            approval_expires_at=str(payload.get("approval_expires_at", "")),
            graphify_handoff_candidate_status=str(payload.get("graphify_handoff_candidate_status", "")),
            client_gateway_lifecycle_stage=str(payload.get("client_gateway_lifecycle_stage", "")),
            contains_client_data_full_payload=read_json_bool(payload, "contains_client_data_full_payload", default=False),
            raw_audio_retained=read_json_bool(payload, "raw_audio_retained", default=False),
            live_action_requested=read_json_bool(payload, "live_action_requested", default=False),
            live_action_approved=read_json_bool(payload, "live_action_approved", default=False),
            conflict_markers=read_text_tuple(payload, "conflict_markers", default=()),
            superseded_by_envelope_id=str(payload.get("superseded_by_envelope_id", "")),
        )

    def to_mission_action(self) -> MissionAction:
        """Represent a valid relay envelope as a dry-run local policy action."""

        return MissionAction(
            action_id=f"relay-{self.envelope_id}",
            action_type="relay_envelope_validate",
            title=f"Validate relay envelope {self.envelope_id}",
            arguments={
                "schema_version": self.schema_version,
                "record_type": self.record_type,
                "project_id": self.project_id,
                "request_id": self.request_id,
                "mission_id": self.mission_id,
                "device_role": self.device_role,
                "approval_level": self.approval_level,
                "requested_capability": self.requested_capability,
                "relay_transport": self.relay_transport,
                "connector_profile_ids": list(self.connector_profile_ids),
                "evidence_refs": list(self.evidence_refs),
                "observed_state_refs": dict(self.observed_state_refs),
            },
            risk_tier=2,
        )


@dataclass(frozen=True)
class RelayValidationContext:
    """Known local state used to validate an envelope without network calls."""

    known_connector_profile_ids: tuple[str, ...] = field(
        default_factory=lambda: tuple(profile.connector_id for profile in initial_connector_profiles())
    )
    approved_device_ids: tuple[str, ...] = ()
    known_request_ids: tuple[str, ...] = ()
    known_mission_ids: tuple[str, ...] = ()
    current_state_refs: Mapping[str, str] = field(default_factory=dict)
    known_graph_snapshot_refs: tuple[str, ...] = ()
    validated_at: str = ""
    live_action_approved: bool = False


@dataclass(frozen=True)
class RelayValidationReport:
    """Validation result for one local relay envelope."""

    envelope_id: str
    valid: bool
    reasons: tuple[str, ...] = ()
    mission_action: MissionAction | None = None


def validate_relay_envelope(
    envelope: RelayEnvelope,
    *,
    context: RelayValidationContext | None = None,
) -> RelayValidationReport:
    """Validate a future relay/cockpit record before any network relay exists."""

    context = context or RelayValidationContext()
    reasons: list[str] = []

    _require_text(
        reasons,
        {
            "schema_version": envelope.schema_version,
            "envelope_id": envelope.envelope_id,
            "record_type": envelope.record_type,
            "project_id": envelope.project_id,
            "request_id": envelope.request_id,
            "mission_id": envelope.mission_id,
            "actor_id": envelope.actor_id,
            "device_id": envelope.device_id,
            "device_role": envelope.device_role,
            "approval_level": envelope.approval_level,
            "requested_capability": envelope.requested_capability,
            "relay_status": envelope.relay_status,
            "relay_transport": envelope.relay_transport,
            "worker_connection_mode": envelope.worker_connection_mode,
        },
    )

    if envelope.schema_version != SCHEMA_VERSION:
        reasons.append(f"schema_version must be {SCHEMA_VERSION}")
    if envelope.record_type not in RECORD_TYPES:
        reasons.append("record_type must be intent, approval, status, evidence, or handoff")
    if envelope.project_id != PROJECT_ID:
        reasons.append(f"project_id must be {PROJECT_ID}")
    if envelope.device_role not in DEVICE_ROLES:
        reasons.append("device_role is not approved for relay envelopes")
    if context.approved_device_ids and envelope.device_id not in context.approved_device_ids:
        reasons.append("device_id is not in the approved device list")

    if envelope.approval_level not in APPROVAL_LEVELS:
        reasons.append("approval_level must be A0, A1, A2, or A3")
    ceiling = SURFACE_APPROVAL_CEILINGS.get(envelope.device_role)
    if ceiling and _approval_rank(envelope.approval_level) > _approval_rank(ceiling):
        reasons.append(f"{envelope.device_role} cannot approve above {ceiling}")

    if envelope.relay_status not in ACTIVE_RELAY_STATUSES:
        reasons.append("relay_status must be active, proposed, approved, paused, or draft")
    if envelope.relay_transport not in LOCAL_RELAY_TRANSPORTS:
        reasons.append("relay_transport must remain local-file; hosted relay is not active")
    if envelope.worker_connection_mode not in PLANNED_WORKER_MODES:
        reasons.append("worker_connection_mode must remain planned-only and cannot start polling or inbound listeners")
    if envelope.superseded_by_envelope_id:
        reasons.append("superseded relay envelopes cannot authorize work")
    if envelope.conflict_markers:
        reasons.append("conflicting relay envelopes stop for human review")

    if not envelope.connector_profile_ids:
        reasons.append("connector_profile_ids must not be empty")
    unknown_connectors = sorted(set(envelope.connector_profile_ids) - set(context.known_connector_profile_ids))
    if unknown_connectors:
        reasons.append(f"unknown connector_profile_ids: {', '.join(unknown_connectors)}")

    if envelope.request_id and context.known_request_ids and envelope.request_id not in context.known_request_ids:
        reasons.append("request_id is not known in the current relay context")
    if envelope.mission_id and context.known_mission_ids and envelope.mission_id not in context.known_mission_ids:
        reasons.append("mission_id is not known in the current relay context")

    if not envelope.observed_state_refs:
        reasons.append("observed_state_refs must include the repo, request, mission, or graph state used")
    elif stale_refs := _stale_state_refs(envelope.observed_state_refs, context.current_state_refs):
        reasons.append(f"observed_state_refs are stale: {', '.join(stale_refs)}")

    if not envelope.graph_registry_id and not envelope.graph_snapshot_ref:
        reasons.append("graph_registry_id or graph_snapshot_ref is required")
    if (
        envelope.graph_snapshot_ref
        and context.known_graph_snapshot_refs
        and envelope.graph_snapshot_ref not in context.known_graph_snapshot_refs
    ):
        reasons.append("graph_snapshot_ref is not known in the current graph registry context")

    if not envelope.evidence_refs:
        reasons.append("evidence_refs must include at least one safe evidence reference")
    elif unsafe_refs := _unsafe_refs(envelope.evidence_refs):
        reasons.append(f"evidence_refs must be relative non-sensitive references: {', '.join(unsafe_refs)}")
    if unsafe_refs := _unsafe_refs(envelope.filesystem_scope_refs):
        reasons.append(f"filesystem_scope_refs must be relative scoped references: {', '.join(unsafe_refs)}")

    if not envelope.stop_triggers:
        reasons.append("stop_triggers must be shown to the approving surface")
    else:
        unknown_stop_triggers = sorted(set(envelope.stop_triggers) - set(STOP_ACTION_TYPES))
        missing_stop_triggers = sorted(REQUIRED_RELAY_STOP_TRIGGERS - set(envelope.stop_triggers))
        if unknown_stop_triggers:
            reasons.append(f"stop_triggers include unknown values: {', '.join(unknown_stop_triggers)}")
        if missing_stop_triggers:
            reasons.append(f"stop_triggers must include relay safety boundaries: {', '.join(missing_stop_triggers)}")
        if "graphify-enhanced-handoff" in envelope.connector_profile_ids and "graphify_action_execution" not in envelope.stop_triggers:
            reasons.append("Graphify relay envelopes must include graphify_action_execution")

    if not envelope.safe_summary:
        reasons.append("safe_summary is required and must contain references or summaries only")
    elif _contains_sensitive_summary(envelope.safe_summary):
        reasons.append("safe_summary must not include raw secrets, credentials, raw logs, raw audio, client payloads, or live sessions")

    requested = envelope.requested_capability
    if requested not in SAFE_RELAY_CAPABILITIES | LIVE_RELAY_CAPABILITIES:
        reasons.append("requested_capability is not approved for relay envelopes")
    if requested in LIVE_RELAY_CAPABILITIES or envelope.live_action_requested:
        if not (envelope.live_action_approved and context.live_action_approved):
            reasons.append("live relay actions require an explicit approved live-action boundary")

    if "m365-guided-ai-labs-business" in envelope.connector_profile_ids and requested not in {
        "planning-only",
        "inventory-only",
        "status-read",
        "handoff-summary",
    }:
        reasons.append("Microsoft 365 remains planning-only for relay envelopes")

    if "client-gateway-planning-template" in envelope.connector_profile_ids and envelope.client_gateway_lifecycle_stage not in SAFE_CLIENT_GATEWAY_STAGES:
        reasons.append("Client Gateway assessment stages require signed scope, roles, retention, approvals, and review")

    if envelope.contains_client_data_full_payload:
        reasons.append("relay envelopes must not carry client-data-full payloads")
    if envelope.raw_audio_retained:
        reasons.append("relay envelopes must not retain raw audio by default")

    graphify_status = envelope.graphify_handoff_candidate_status.lower()
    if graphify_status not in SAFE_GRAPHIFY_CANDIDATE_STATUSES:
        reasons.append("Graphify handoff status must remain read-only candidate state")

    if approval_expiry_issue := _approval_expiry_issue(envelope.approval_expires_at, context.validated_at):
        reasons.append(approval_expiry_issue)

    return RelayValidationReport(
        envelope_id=envelope.envelope_id or "unknown",
        valid=not reasons,
        reasons=tuple(reasons),
        mission_action=None if reasons else envelope.to_mission_action(),
    )


def read_text_tuple(payload: Mapping[str, Any], key: str, *, default: Iterable[str] | None = None) -> tuple[str, ...]:
    value = payload.get(key, default if default is not None else ())
    if isinstance(value, str):
        raise ValueError(f"{key} must be a JSON array of strings.")
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{key} must be a JSON array of strings.")
    return tuple(str(item).strip() for item in value if str(item).strip())


def read_text_mapping(payload: Mapping[str, Any], key: str) -> dict[str, str]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"{key} must be a JSON object.")
    return {str(item_key): str(item_value) for item_key, item_value in value.items()}


def read_mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ValueError(f"{key} must be a JSON object.")
    return dict(value)


def read_json_bool(payload: Mapping[str, Any], key: str, *, default: bool) -> bool:
    value = payload.get(key, default)
    if isinstance(value, bool):
        return value
    raise ValueError(f"{key} must be a JSON boolean.")


def _require_text(reasons: list[str], fields: Mapping[str, str]) -> None:
    for name, value in fields.items():
        if not isinstance(value, str) or not value.strip():
            reasons.append(f"{name} is required")


def _approval_rank(level: str) -> int:
    return {"A0": 0, "A1": 1, "A2": 2, "A3": 3}.get(level, 99)


def _stale_state_refs(observed: Mapping[str, str], current: Mapping[str, str]) -> list[str]:
    stale: list[str] = []
    for key, current_value in current.items():
        if observed.get(key) != current_value:
            stale.append(key)
    return stale


def _approval_expiry_issue(expires_at: str, validated_at: str) -> str | None:
    if not expires_at:
        return None
    if not validated_at:
        return "approval_expires_at cannot be evaluated without validation time"
    try:
        expiry = _parse_timestamp(expires_at)
        validation_time = _parse_timestamp(validated_at)
    except ValueError:
        return "approval_expires_at and validated_at must be valid ISO timestamps"
    if expiry <= validation_time:
        return "approval is stale or expired"
    return None


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


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
