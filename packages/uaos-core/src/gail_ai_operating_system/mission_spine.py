"""Local no-network mission spine for GAIL AI Operating System Rev 2."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Iterable, Mapping
from uuid import uuid4

from .trace_identity import ensure_cns_trace_id, validate_cns_trace_id


REV2_OWNER = "Adam Goodwin"
DEFAULT_APPROVAL_LEVEL = "A1 local no-network"

ALLOWED_DOMAINS = frozenset(
    {
        "build",
        "governance",
        "migration",
        "validation",
        "operations",
        "learning",
    }
)
ALLOWED_DATA_CLASSES = frozenset({"public", "internal", "synthetic"})
ALLOWED_LOCAL_TOOLS = frozenset({"local_repo", "local_validation", "policy_gate"})

LOCAL_ACTION_TYPES = frozenset(
    {
        "local_mission_record",
        "local_validation_command",
        "local_repo_read",
        "local_repo_update",
        "graphify_handoff_read",
        "relay_envelope_validate",
        "relay_worker_claim_validate",
        "policy_gate_review",
    }
)

STOP_ACTION_TYPES: Mapping[str, str] = {
    "secret_exposure": "Secret values must not be printed, copied, summarized, committed, stored, or exposed.",
    "client_data_access": "Client or customer data access is blocked until a later approved client-data boundary exists.",
    "external_message_send": "External messages, email, Teams posts, or customer communications require explicit approval.",
    "m365_live_content_read": "Microsoft 365 content reads are blocked until an approved connector boundary exists.",
    "m365_tenant_or_permission_change": "Microsoft 365 tenant, Entra, admin, permission, sharing, or billing changes require explicit approval.",
    "finance_or_billing_action": "QuickBooks, accounting, invoice, payment, billing, finance, and money actions require explicit approval.",
    "vendor_account_action": "Vendor account, subscription, license, contract, or paid-plan changes require explicit approval.",
    "destructive_git_operation": "Destructive Git operations require explicit approval and a rollback path.",
    "destructive_delete": "Deleting repositories, projects, remote resources, production data, or user work requires explicit approval.",
    "production_or_deployment_action": "Production launch, deployment, DNS, infrastructure, or public release actions require explicit approval.",
    "connector_profile_required": "Live connector or third-party account access requires an approved connector profile first.",
    "hosted_relay_or_worker_action": "Hosted relay, persistent worker, public ingress, or worker polling behavior is outside the local mission spine.",
    "portal_or_relay_live_action": "Phone, tablet, browser, or relay approvals cannot execute live connector actions until a later boundary exists.",
    "graphify_action_execution": "Graphify may provide read-only context later; it cannot approve or execute actions.",
    "raw_payload_retention": "Raw logs, raw audio, unredacted screenshots, and sensitive payload dumps must stay out of Rev 2 records.",
    "unreviewed_client_visibility": "Client-visible AI findings must remain internal until review and client-data boundaries are approved.",
    "external_tool_request": "Requested tools must stay inside the approved local no-network tool set.",
    "mission_validation_failed": "Mission records must pass local Rev 2 validation before planning.",
}

STOP_KEYWORD_MAP: tuple[tuple[tuple[str, ...], str], ...] = (
    (("secret", "token", "password", "api key", "credential", "private key"), "secret_exposure"),
    (
        (
            "client data",
            "client-data",
            "customer data",
            "client-controlled",
            "client gateway assessment",
            "client gateway workspace",
            "public prospect intake",
        ),
        "client_data_access",
    ),
    (("send email", "send message", "send outlook", "send teams", "post to teams", "sms"), "external_message_send"),
    (
        (
            "read outlook",
            "read microsoft 365",
            "read m365",
            "read sharepoint",
            "read onedrive",
            "read teams",
            "read calendar",
            "summarize sharepoint",
            "summarize onedrive",
            "summarize outlook",
            "index sharepoint",
            "sync sharepoint",
        ),
        "m365_live_content_read",
    ),
    (
        (
            "change entra",
            "tenant setting",
            "m365 admin",
            "microsoft 365 admin",
            "grant sharepoint",
            "change mailbox permission",
            "change m365 billing",
        ),
        "m365_tenant_or_permission_change",
    ),
    (
        (
            "quickbooks",
            "accounting",
            "invoice",
            "payment",
            "billing",
            "charge card",
            "bank data",
            "tax record",
        ),
        "finance_or_billing_action",
    ),
    (("subscription", "license", "contract", "vendor account", "paid plan"), "vendor_account_action"),
    (("git reset --hard", "git clean -fd", "force push", "delete branch"), "destructive_git_operation"),
    (("delete repo", "delete repository", "delete project", "delete production", "delete remote"), "destructive_delete"),
    (("production launch", "public launch", "deploy production", "change dns", "domain record"), "production_or_deployment_action"),
    (("connect m365", "connect microsoft 365", "connect quickbooks", "connect aws", "connect dropbox", "live connector"), "connector_profile_required"),
    (("hosted relay", "persistent worker", "worker polling", "public ingress"), "hosted_relay_or_worker_action"),
    (
        (
            "approve live m365 from phone",
            "phone and execute",
            "tablet and execute",
            "browser and execute",
            "relay approval",
            "execute the connector",
        ),
        "portal_or_relay_live_action",
    ),
    (("execute graphify", "run graphify recommendation", "mutate files from graphify"), "graphify_action_execution"),
    (("raw log", "raw audio", "voice recording", "unredacted screenshot", "sensitive payload"), "raw_payload_retention"),
    (
        (
            "publish ai findings",
            "client-visible",
            "client visible",
            "guided ai labs review",
            "unreviewed client",
        ),
        "unreviewed_client_visibility",
    ),
)


@dataclass(frozen=True)
class MissionValidationIssue:
    """One validation problem for a mission envelope."""

    field: str
    message: str


class MissionValidationError(ValueError):
    """Raised when a mission envelope is not valid for local use."""

    def __init__(self, issues: Iterable[MissionValidationIssue]) -> None:
        self.issues = tuple(issues)
        detail = "; ".join(f"{issue.field}: {issue.message}" for issue in self.issues)
        super().__init__(detail or "Mission envelope is not valid.")


@dataclass(frozen=True)
class MissionValidationResult:
    """Validation result for a mission envelope."""

    valid: bool
    issues: tuple[MissionValidationIssue, ...] = ()

    def require_valid(self) -> None:
        if not self.valid:
            raise MissionValidationError(self.issues)


@dataclass(frozen=True)
class MissionAction:
    """One proposed local action before policy evaluation."""

    action_id: str
    action_type: str
    title: str
    arguments: Mapping[str, Any] = field(default_factory=dict)
    risk_tier: int = 2

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "title": self.title,
            "arguments": dict(self.arguments),
            "risk_tier": self.risk_tier,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "MissionAction":
        return cls(
            action_id=str(payload["action_id"]),
            action_type=str(payload["action_type"]),
            title=str(payload["title"]),
            arguments=dict(payload.get("arguments", {})),
            risk_tier=int(payload.get("risk_tier", 2)),
        )


@dataclass(frozen=True)
class MissionEnvelope:
    """Structured local mission record created from operator intent."""

    mission_id: str
    request_id: str
    command: str
    domain: str
    created_at: str
    owner: str
    approval_level: str
    dry_run: bool
    requested_tools: tuple[str, ...] = ()
    data_classification: str = "internal"
    status: str = "draft"
    source_commit: str | None = None
    cns_trace_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "cns_trace_id": self.cns_trace_id,
            "request_id": self.request_id,
            "command": self.command,
            "domain": self.domain,
            "created_at": self.created_at,
            "owner": self.owner,
            "approval_level": self.approval_level,
            "dry_run": self.dry_run,
            "requested_tools": list(self.requested_tools),
            "data_classification": self.data_classification,
            "status": self.status,
            "source_commit": self.source_commit,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "MissionEnvelope":
        raw_source_commit = payload.get("source_commit")
        return cls(
            mission_id=str(payload["mission_id"]),
            request_id=str(payload["request_id"]),
            command=str(payload["command"]),
            domain=normalize_domain(str(payload["domain"])),
            created_at=str(payload["created_at"]),
            owner=str(payload["owner"]),
            approval_level=str(payload["approval_level"]),
            dry_run=read_json_bool(payload, "dry_run"),
            requested_tools=tuple(str(tool).strip().lower() for tool in payload.get("requested_tools", ())),
            data_classification=normalize_data_class(str(payload.get("data_classification", "internal"))),
            status=str(payload.get("status", "draft")),
            source_commit=str(raw_source_commit) if raw_source_commit is not None else None,
            cns_trace_id=str(payload["cns_trace_id"]) if payload.get("cns_trace_id") else None,
        )


@dataclass(frozen=True)
class MissionPlan:
    """Deterministic local plan for a mission envelope."""

    mission_id: str
    actions: tuple[MissionAction, ...]
    stop_trigger: str | None = None


@dataclass(frozen=True)
class PolicyDecision:
    """Permission decision for one proposed mission action."""

    action_id: str
    allowed: bool
    mode: str
    reason: str
    stop_reason: str | None = None


def current_timestamp(now: datetime | None = None) -> str:
    """Return a local ISO timestamp without sub-second noise."""

    value = now or datetime.now(timezone.utc).astimezone()
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone().replace(microsecond=0).isoformat()


def normalize_domain(domain: str) -> str:
    cleaned = (domain or "").strip().lower().replace(" ", "_").replace("-", "_")
    return cleaned if cleaned in ALLOWED_DOMAINS else "build"


def normalize_data_class(data_classification: str) -> str:
    cleaned = (data_classification or "").strip().lower().replace(" ", "_").replace("-", "_")
    return cleaned if cleaned in ALLOWED_DATA_CLASSES else cleaned


def read_json_bool(payload: Mapping[str, Any], key: str) -> bool:
    value = payload[key]
    if isinstance(value, bool):
        return value
    raise ValueError(f"{key} must be a JSON boolean.")


def create_mission(
    command: str,
    *,
    domain: str = "build",
    request_id: str = "REQ-LOCAL",
    requested_tools: Iterable[str] = (),
    data_classification: str = "internal",
    created_at: datetime | str | None = None,
    source_commit: str | None = None,
    cns_trace_id: str | None = None,
) -> MissionEnvelope:
    """Create a local mission envelope under the current Rev 2 A1 boundary."""

    cleaned_command = command.strip()
    if not cleaned_command:
        raise ValueError("Mission command is required.")

    if isinstance(created_at, datetime):
        timestamp = current_timestamp(created_at)
    elif isinstance(created_at, str):
        timestamp = created_at
    else:
        timestamp = current_timestamp()

    mission = MissionEnvelope(
        mission_id=f"mission-{uuid4().hex[:12]}",
        request_id=(request_id or "REQ-LOCAL").strip(),
        command=cleaned_command,
        domain=normalize_domain(domain),
        created_at=timestamp,
        owner=REV2_OWNER,
        approval_level=DEFAULT_APPROVAL_LEVEL,
        dry_run=True,
        requested_tools=tuple(str(tool).strip().lower() for tool in requested_tools if str(tool).strip()),
        data_classification=normalize_data_class(data_classification),
        source_commit=source_commit,
        cns_trace_id=ensure_cns_trace_id(cns_trace_id),
    )
    validate_mission(mission).require_valid()
    return mission


def validate_mission(mission: MissionEnvelope) -> MissionValidationResult:
    """Validate mission shape and current local-only governance boundaries."""

    issues: list[MissionValidationIssue] = []

    if not mission.mission_id.startswith("mission-"):
        issues.append(MissionValidationIssue("mission_id", "Mission IDs must use the mission- prefix."))
    if not mission.request_id.strip():
        issues.append(MissionValidationIssue("request_id", "Request ID is required."))
    if not mission.command.strip():
        issues.append(MissionValidationIssue("command", "Command is required."))
    if mission.domain not in ALLOWED_DOMAINS:
        issues.append(MissionValidationIssue("domain", "Domain is not approved for the local mission spine."))
    if mission.owner != REV2_OWNER:
        issues.append(MissionValidationIssue("owner", "Mission owner must remain Adam Goodwin."))
    if mission.approval_level != DEFAULT_APPROVAL_LEVEL:
        issues.append(MissionValidationIssue("approval_level", "Approval level must stay A1 local no-network."))
    if not mission.dry_run:
        issues.append(MissionValidationIssue("dry_run", "Chunk Nine missions must remain dry-run."))
    if mission.data_classification not in ALLOWED_DATA_CLASSES:
        issues.append(
            MissionValidationIssue(
                "data_classification",
                "Only public, internal, or synthetic data classes are allowed in the local mission spine.",
            )
        )
    for trace_error in validate_cns_trace_id(mission.cns_trace_id):
        issues.append(MissionValidationIssue("cns_trace_id", trace_error))
    unknown_tools = sorted(set(mission.requested_tools) - ALLOWED_LOCAL_TOOLS)
    if unknown_tools:
        issues.append(
            MissionValidationIssue(
                "requested_tools",
                f"Requested tools are outside the local no-network boundary: {', '.join(unknown_tools)}.",
            )
        )

    return MissionValidationResult(valid=not issues, issues=tuple(issues))


def detect_stop_trigger(command: str) -> str | None:
    """Return the first stop-trigger action type matched by command text."""

    lowered = command.lower()
    for keywords, action_type in STOP_KEYWORD_MAP:
        if any(keyword in lowered for keyword in keywords):
            return action_type
    return None


def build_local_plan(mission: MissionEnvelope) -> MissionPlan:
    """Build the smallest deterministic plan allowed before connectors exist."""

    validation = validate_mission(mission)
    if not validation.valid:
        stop_trigger = (
            "external_tool_request"
            if any(issue.field == "requested_tools" for issue in validation.issues)
            else "mission_validation_failed"
        )
        return MissionPlan(
            mission_id=mission.mission_id,
            stop_trigger=stop_trigger,
            actions=(
                MissionAction(
                    action_id="action-stop-001",
                    action_type=stop_trigger,
                    title="Stop for local mission validation",
                    arguments={"issues": [issue.message for issue in validation.issues]},
                    risk_tier=5,
                ),
            ),
        )

    stop_trigger = detect_stop_trigger(mission.command)
    if stop_trigger:
        return MissionPlan(
            mission_id=mission.mission_id,
            stop_trigger=stop_trigger,
            actions=(
                MissionAction(
                    action_id="action-stop-001",
                    action_type=stop_trigger,
                    title="Stop for Adam approval",
                    arguments={"stop_reason": STOP_ACTION_TYPES[stop_trigger]},
                    risk_tier=5,
                ),
            ),
        )

    return MissionPlan(
        mission_id=mission.mission_id,
        actions=(
            MissionAction(
                action_id="action-001",
                action_type="local_mission_record",
                title="Create local mission record",
                arguments={"mission_id": mission.mission_id, "request_id": mission.request_id},
                risk_tier=1,
            ),
            MissionAction(
                action_id="action-002",
                action_type="policy_gate_review",
                title="Evaluate local policy gate",
                arguments={"approval_level": mission.approval_level},
                risk_tier=1,
            ),
            MissionAction(
                action_id="action-003",
                action_type="local_validation_command",
                title="Queue local unit test validation",
                arguments={"command": "python -m unittest discover -s tests"},
                risk_tier=0,
            ),
        ),
    )


class PermissionGate:
    """Evaluate proposed mission actions against the Chunk Nine local boundary."""

    def evaluate(self, mission: MissionEnvelope, action: MissionAction) -> PolicyDecision:
        validation = validate_mission(mission)
        if not validation.valid:
            return PolicyDecision(
                action_id=action.action_id,
                allowed=False,
                mode="stop",
                reason="Mission envelope failed local validation.",
                stop_reason="; ".join(issue.message for issue in validation.issues),
            )

        if action.action_type in STOP_ACTION_TYPES:
            return PolicyDecision(
                action_id=action.action_id,
                allowed=False,
                mode="stop",
                reason="Action matches a Rev 2 stop trigger.",
                stop_reason=STOP_ACTION_TYPES[action.action_type],
            )

        if action.action_type not in LOCAL_ACTION_TYPES:
            return PolicyDecision(
                action_id=action.action_id,
                allowed=False,
                mode="stop",
                reason="Action type is not in the local no-network allowlist.",
                stop_reason="Default deny: unlisted mission actions stop for Adam approval.",
            )

        if action.risk_tier > 2:
            return PolicyDecision(
                action_id=action.action_id,
                allowed=False,
                mode="stop",
                reason="Action risk tier exceeds the current local mission boundary.",
                stop_reason="Only local Tier 0-2 actions are allowed in Chunk Nine.",
            )

        return PolicyDecision(
            action_id=action.action_id,
            allowed=True,
            mode="dry-run",
            reason="Action is inside the local no-network mission spine boundary.",
        )

    def evaluate_plan(self, mission: MissionEnvelope, plan: MissionPlan) -> tuple[PolicyDecision, ...]:
        return tuple(self.evaluate(mission, action) for action in plan.actions)


class LocalMissionStore:
    """Small JSON store for local synthetic mission records."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def path_for(self, mission_id: str) -> Path:
        safe_id = mission_id.strip()
        if not safe_id.startswith("mission-") or any(part in safe_id for part in ("/", "\\", "..")):
            raise ValueError("Mission ID is not safe for local storage.")
        return self.root / f"{safe_id}.json"

    def save(self, mission: MissionEnvelope) -> Path:
        validate_mission(mission).require_valid()
        self.root.mkdir(parents=True, exist_ok=True)
        path = self.path_for(mission.mission_id)
        path.write_text(json.dumps(mission.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def load(self, mission_id: str) -> MissionEnvelope:
        payload = json.loads(self.path_for(mission_id).read_text(encoding="utf-8"))
        mission = MissionEnvelope.from_dict(payload)
        validate_mission(mission).require_valid()
        return mission
