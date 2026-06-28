"""Local planning-only connector registry for GAIL AI Operating System Rev 2."""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Iterable, Mapping

from .mission_spine import STOP_ACTION_TYPES


SYSTEM_FAMILIES = frozenset(
    {
        "GitHub",
        "Graphify",
        "Microsoft 365",
        "QuickBooks",
        "Local Device",
        "Client Gateway",
        "Vendor Or Deployment",
    }
)
CURRENT_STATES = frozenset({"planning-only", "registry-only", "inventory-only"})
PROFILE_CAPABILITIES = frozenset({"planning-only", "inventory-only", "metadata-only", "local-validation", "readiness-check"})
LIVE_CAPABILITIES = frozenset(
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
    }
)
DATA_CLASSES = frozenset({"public", "internal", "synthetic", "confidential", "client-controlled", "restricted"})
CURRENT_REQUEST_DATA_CLASSES = frozenset({"public", "internal", "synthetic"})
REQUIRED_AUDIT_FIELDS = frozenset({"mission_id", "connector_id", "capability", "result", "stop_reason"})
SAFE_ID_CHARS = frozenset("abcdefghijklmnopqrstuvwxyz0123456789-")

CAPABILITY_STOP_TRIGGERS: Mapping[str, str] = {
    "content-read": "m365_live_content_read",
    "summarize": "m365_live_content_read",
    "send-message": "external_message_send",
    "admin-change": "m365_tenant_or_permission_change",
    "billing-action": "finance_or_billing_action",
    "delete": "destructive_delete",
    "draft-only": "connector_profile_required",
    "prepare-action": "connector_profile_required",
    "execute-after-approval": "connector_profile_required",
    "write": "connector_profile_required",
}


@dataclass(frozen=True)
class ConnectorValidationIssue:
    """One connector profile validation problem."""

    field: str
    message: str


@dataclass(frozen=True)
class ConnectorValidationReport:
    """Validation result for one connector profile."""

    connector_id: str
    valid: bool
    issues: tuple[ConnectorValidationIssue, ...] = ()

    @property
    def reasons(self) -> tuple[str, ...]:
        return tuple(issue.message for issue in self.issues)


@dataclass(frozen=True)
class ConnectorRegistryReport:
    """Validation result for a connector profile set."""

    valid: bool
    profile_reports: tuple[ConnectorValidationReport, ...]
    issues: tuple[ConnectorValidationIssue, ...] = ()

    @property
    def reasons(self) -> tuple[str, ...]:
        return tuple(issue.message for issue in self.issues)


@dataclass(frozen=True)
class ConnectorProfile:
    """A local connector profile record, not credentials or a live adapter."""

    connector_id: str
    display_name: str
    system_family: str
    owner: str
    tenant_or_workspace: str
    current_state: str
    allowed_capabilities: tuple[str, ...]
    prohibited_capabilities: tuple[str, ...]
    data_classes: tuple[str, ...]
    approval_gate: str
    retention_rule: str
    audit_requirements: tuple[str, ...]
    stop_triggers: tuple[str, ...]
    failure_behavior: str
    live_access_enabled: bool = False
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "connector_id": self.connector_id,
            "display_name": self.display_name,
            "system_family": self.system_family,
            "owner": self.owner,
            "tenant_or_workspace": self.tenant_or_workspace,
            "current_state": self.current_state,
            "allowed_capabilities": list(self.allowed_capabilities),
            "prohibited_capabilities": list(self.prohibited_capabilities),
            "data_classes": list(self.data_classes),
            "approval_gate": self.approval_gate,
            "retention_rule": self.retention_rule,
            "audit_requirements": list(self.audit_requirements),
            "stop_triggers": list(self.stop_triggers),
            "failure_behavior": self.failure_behavior,
            "live_access_enabled": self.live_access_enabled,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ConnectorProfile":
        return cls(
            connector_id=str(payload["connector_id"]),
            display_name=str(payload["display_name"]),
            system_family=str(payload["system_family"]),
            owner=str(payload["owner"]),
            tenant_or_workspace=str(payload["tenant_or_workspace"]),
            current_state=str(payload["current_state"]),
            allowed_capabilities=read_text_tuple(payload, "allowed_capabilities"),
            prohibited_capabilities=read_text_tuple(payload, "prohibited_capabilities"),
            data_classes=read_text_tuple(payload, "data_classes"),
            approval_gate=str(payload["approval_gate"]),
            retention_rule=str(payload["retention_rule"]),
            audit_requirements=read_text_tuple(payload, "audit_requirements"),
            stop_triggers=read_text_tuple(payload, "stop_triggers"),
            failure_behavior=str(payload["failure_behavior"]),
            live_access_enabled=read_optional_json_bool(payload, "live_access_enabled", default=False),
            notes=str(payload.get("notes", "")),
        )


@dataclass(frozen=True)
class ConnectorOperationRequest:
    """A local dry-run request to evaluate a connector profile boundary."""

    request_id: str
    connector_id: str
    capability: str
    data_classification: str = "internal"
    dry_run: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "connector_id": self.connector_id,
            "capability": self.capability,
            "data_classification": self.data_classification,
            "dry_run": self.dry_run,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ConnectorOperationRequest":
        return cls(
            request_id=str(payload["request_id"]),
            connector_id=str(payload["connector_id"]),
            capability=str(payload["capability"]),
            data_classification=str(payload.get("data_classification", "internal")),
            dry_run=read_optional_json_bool(payload, "dry_run", default=True),
        )


@dataclass(frozen=True)
class ConnectorPermissionDecision:
    """Local permission result for one connector operation request."""

    request_id: str
    connector_id: str
    capability: str
    allowed: bool
    mode: str
    reason: str
    stop_trigger: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "connector_id": self.connector_id,
            "capability": self.capability,
            "allowed": self.allowed,
            "mode": self.mode,
            "reason": self.reason,
            "stop_trigger": self.stop_trigger,
        }


def read_text_tuple(payload: Mapping[str, Any], key: str) -> tuple[str, ...]:
    value = payload.get(key, ())
    if isinstance(value, str):
        raise ValueError(f"{key} must be a JSON array of strings.")
    return tuple(str(item).strip() for item in value if str(item).strip())


def read_optional_json_bool(payload: Mapping[str, Any], key: str, *, default: bool) -> bool:
    value = payload.get(key, default)
    if isinstance(value, bool):
        return value
    raise ValueError(f"{key} must be a JSON boolean.")


def initial_connector_profiles() -> tuple[ConnectorProfile, ...]:
    """Return the current Rev 2 planning-only connector registry entries."""

    return (
        ConnectorProfile(
            connector_id="github-rev2-private-source",
            display_name="Rev 2 private GitHub source",
            system_family="GitHub",
            owner="Adam Goodwin",
            tenant_or_workspace="Adamgdwn/gail-ai-operating-system-rev-2",
            current_state="registry-only",
            allowed_capabilities=("planning-only", "inventory-only", "metadata-only"),
            prohibited_capabilities=(
                "public repository exposure",
                "destructive repository settings",
                "secret exposure",
                "production release promotion",
            ),
            data_classes=("internal",),
            approval_gate="Chunk closeout may push scoped commits; issues, releases, settings, and destructive changes require explicit approval.",
            retention_rule="Keep commit metadata, validation summaries, and redacted evidence only.",
            audit_requirements=("mission_id", "connector_id", "capability", "result", "stop_reason"),
            stop_triggers=("secret_exposure", "destructive_git_operation", "destructive_delete", "production_or_deployment_action"),
            failure_behavior="Stop on auth, visibility, public exposure, destructive setting, secret, or remote mismatch ambiguity.",
            notes="This profile describes the source spine. It does not grant GitHub API execution authority.",
        ),
        ConnectorProfile(
            connector_id="graphify-enhanced-handoff",
            display_name="Enhanced Graphify handoff",
            system_family="Graphify",
            owner="Adam Goodwin",
            tenant_or_workspace="/home/adamgoodwin/code/Tools/graphify/workspace",
            current_state="planning-only",
            allowed_capabilities=("planning-only", "metadata-only", "readiness-check"),
            prohibited_capabilities=(
                "source mutation",
                "queued action execution",
                "secret indexing",
                "client-data ingestion",
                "graph upload",
            ),
            data_classes=("internal",),
            approval_gate="Chunk Twelve must approve graph-aware routing before broader source exploration or graph-dependent migration.",
            retention_rule="Keep source references, graph route IDs, confidence notes, and reviewed mission candidates only.",
            audit_requirements=("mission_id", "connector_id", "capability", "result", "stop_reason"),
            stop_triggers=("graphify_action_execution", "secret_exposure", "client_data_access", "raw_payload_retention"),
            failure_behavior="Stop on graph source, selected root, stale state, evidence sensitivity, or recommendation/action ambiguity.",
            notes="Graphify remains a knowledge spoke. Recommendations are not execution approval.",
        ),
        ConnectorProfile(
            connector_id="m365-guided-ai-labs-business",
            display_name="Microsoft 365 business environment",
            system_family="Microsoft 365",
            owner="Adam Goodwin",
            tenant_or_workspace="Guided AI Labs Microsoft 365 tenant; exact tenant to be recorded only in a later approved boundary",
            current_state="planning-only",
            allowed_capabilities=("planning-only", "inventory-only"),
            prohibited_capabilities=(
                "Outlook or Teams sending",
                "content reads",
                "tenant security changes",
                "permission changes",
                "billing changes",
                "unrestricted indexing",
                "automatic client workspace creation",
            ),
            data_classes=("internal",),
            approval_gate="Explicit Adam approval, connector profile update, data classification update, retention rule, and audit path are required before inventory or live access.",
            retention_rule="Registry metadata only; no raw Microsoft 365 content, emails, files, calendar records, tenant secrets, or payload dumps.",
            audit_requirements=("mission_id", "connector_id", "capability", "result", "stop_reason"),
            stop_triggers=(
                "m365_live_content_read",
                "external_message_send",
                "m365_tenant_or_permission_change",
                "connector_profile_required",
            ),
            failure_behavior="Stop on auth, identity, tenant, communication, content-read, retention, sharing, client-data, admin, or permission ambiguity.",
            notes="No live Microsoft 365 access is approved by this profile.",
        ),
        ConnectorProfile(
            connector_id="m365-graph-api-bridge",
            display_name="Microsoft Graph API bridge (svc-gail-os-graph)",
            system_family="Microsoft 365",
            owner="Adam Goodwin",
            tenant_or_workspace="guidedailabs.com Entra ID tenant — Graph API, client-credentials, least privilege",
            current_state="registry-only",
            allowed_capabilities=("planning-only", "inventory-only", "readiness-check"),
            prohibited_capabilities=(
                "Outlook or Teams sending",
                "SharePoint or OneDrive content reads",
                "tenant security or permission changes",
                "write or create operations",
                "admin consent or broad scope grants",
                "billing changes",
            ),
            data_classes=("internal",),
            approval_gate="Connector must be promoted to inventory-only with an explicit Graph scope list and Adam approval before any live Graph API call. Task 4.3 (R0 observe) is the next approval gate.",
            retention_rule="No raw Graph API payloads, email content, file content, user data, or tenant secrets. Structured metadata summaries only, after explicit scope approval.",
            audit_requirements=("mission_id", "connector_id", "capability", "result", "stop_reason"),
            stop_triggers=(
                "m365_live_content_read",
                "external_message_send",
                "m365_tenant_or_permission_change",
                "connector_profile_required",
            ),
            failure_behavior="Stop on auth failure, token exposure, scope creep, write attempt, live read without approved scope, or any deviation from the svc-gail-os-graph identity boundary.",
            live_access_enabled=False,
            notes="Graph auth provider is registered in gail_ai_operating_system.m365_auth (task 4.2). AZURE_TENANT_ID / AZURE_CLIENT_ID / AZURE_CLIENT_SECRET env vars required at runtime. Live access requires task 4.3 approval and connector state promotion.",
        ),
        ConnectorProfile(
            connector_id="quickbooks-finance-planning-boundary",
            display_name="QuickBooks and finance boundary",
            system_family="QuickBooks",
            owner="Adam Goodwin",
            tenant_or_workspace="No QuickBooks company, finance account, or billing workspace approved",
            current_state="planning-only",
            allowed_capabilities=("planning-only", "metadata-only"),
            prohibited_capabilities=(
                "accounting record reads",
                "invoice or payment actions",
                "billing exports",
                "bank data access",
                "tax record access",
                "money movement",
            ),
            data_classes=("internal",),
            approval_gate="Explicit finance connector boundary, least-privilege scope, audit path, and rollback/recovery notes are required before any live access.",
            retention_rule="Registry metadata only; no invoices, exports, bank data, tax records, payment details, or finance payloads.",
            audit_requirements=("mission_id", "connector_id", "capability", "result", "stop_reason"),
            stop_triggers=("finance_or_billing_action", "connector_profile_required", "raw_payload_retention"),
            failure_behavior="Stop on money, billing, account ownership, client/vendor data, compliance, or irreversible-action ambiguity.",
            notes="This is a planning guard, not an accounting connector.",
        ),
        ConnectorProfile(
            connector_id="local-device-worker-surfaces",
            display_name="Windows and Linux trusted worker surfaces",
            system_family="Local Device",
            owner="Adam Goodwin",
            tenant_or_workspace="Windows operator workspace, Linux reference host, and future approved worker clones",
            current_state="registry-only",
            allowed_capabilities=("planning-only", "inventory-only", "local-validation"),
            prohibited_capabilities=(
                "persistent worker polling",
                "system-wide changes",
                "credential extraction",
                "broad filesystem reads",
                "hosted relay operation",
            ),
            data_classes=("internal", "synthetic"),
            approval_gate="Worker bootstrap, persistent service behavior, privileged action, broad filesystem access, or live connector use requires a later explicit chunk.",
            retention_rule="Keep local temp state local unless promoted through governed non-sensitive artifacts.",
            audit_requirements=("mission_id", "connector_id", "capability", "result", "stop_reason"),
            stop_triggers=("hosted_relay_or_worker_action", "secret_exposure", "destructive_delete", "connector_profile_required"),
            failure_behavior="Stop on privilege, persistence, filesystem, device identity, worker claim, or credential ambiguity.",
            notes="DirectLink remains transport/status only and is not the project home.",
        ),
        ConnectorProfile(
            connector_id="client-gateway-planning-template",
            display_name="Client Gateway planning template",
            system_family="Client Gateway",
            owner="Future named client owner plus Guided AI Labs governance owner",
            tenant_or_workspace="Future isolated Client Gateway workspace; not created automatically",
            current_state="planning-only",
            allowed_capabilities=("planning-only", "readiness-check"),
            prohibited_capabilities=(
                "public-intake client-data collection",
                "automatic workspace creation",
                "unreviewed client-visible findings",
                "live connector access",
                "raw audio retention",
            ),
            data_classes=("client-controlled",),
            approval_gate="Signed scope, named roles, retention, connector approvals, and Guided AI Labs review are required before client data or client-visible output.",
            retention_rule="Archive/delete rules must be recorded per signed scope before assessment; no raw audio or client payload retention by default.",
            audit_requirements=("mission_id", "connector_id", "capability", "result", "stop_reason"),
            stop_triggers=(
                "client_data_access",
                "unreviewed_client_visibility",
                "raw_payload_retention",
                "connector_profile_required",
            ),
            failure_behavior="Stop on client identity, workspace isolation, signed scope, connector approval, retention, or visibility ambiguity.",
            notes="This profile describes future client-data prerequisites; current requests using client-controlled data still stop.",
        ),
        ConnectorProfile(
            connector_id="vendor-and-deployment-providers",
            display_name="Vendor, storage, infrastructure, and deployment providers",
            system_family="Vendor Or Deployment",
            owner="Adam Goodwin",
            tenant_or_workspace="No AWS, Dropbox, vendor, deployment, DNS, or production account approved",
            current_state="planning-only",
            allowed_capabilities=("planning-only", "metadata-only"),
            prohibited_capabilities=(
                "private account reads",
                "resource creation",
                "IAM or sharing changes",
                "billing changes",
                "file deletion",
                "production deployment",
                "DNS changes",
            ),
            data_classes=("internal",),
            approval_gate="Explicit connector activation, least-privilege scope, logging, cost review, and rollback plan are required before live access.",
            retention_rule="Registry metadata only until an approved internal or client use case exists.",
            audit_requirements=("mission_id", "connector_id", "capability", "result", "stop_reason"),
            stop_triggers=(
                "vendor_account_action",
                "production_or_deployment_action",
                "destructive_delete",
                "connector_profile_required",
            ),
            failure_behavior="Stop on cost, IAM, production, region, sharing, ownership, retention, data, or reversibility ambiguity.",
            notes="This profile groups future provider planning; it does not approve provider account access.",
        ),
    )


def validate_connector_profile(profile: ConnectorProfile) -> ConnectorValidationReport:
    """Validate a connector profile before registry routing can trust it."""

    issues: list[ConnectorValidationIssue] = []
    required_text = {
        "connector_id": profile.connector_id,
        "display_name": profile.display_name,
        "system_family": profile.system_family,
        "owner": profile.owner,
        "tenant_or_workspace": profile.tenant_or_workspace,
        "current_state": profile.current_state,
        "approval_gate": profile.approval_gate,
        "retention_rule": profile.retention_rule,
        "failure_behavior": profile.failure_behavior,
    }

    for field_name, value in required_text.items():
        if not value.strip():
            issues.append(ConnectorValidationIssue(field_name, "Field is required."))

    if not is_safe_connector_id(profile.connector_id):
        issues.append(
            ConnectorValidationIssue(
                "connector_id",
                "Connector ID must use lowercase letters, numbers, and hyphens only.",
            )
        )
    if profile.system_family not in SYSTEM_FAMILIES:
        issues.append(ConnectorValidationIssue("system_family", "System family is not approved for the Rev 2 registry."))
    if profile.current_state not in CURRENT_STATES:
        issues.append(ConnectorValidationIssue("current_state", "Current state must remain planning-only, registry-only, or inventory-only."))
    if profile.live_access_enabled:
        issues.append(ConnectorValidationIssue("live_access_enabled", "Live connector access is blocked in Chunk Eleven."))
    if not profile.allowed_capabilities:
        issues.append(ConnectorValidationIssue("allowed_capabilities", "At least one local planning capability is required."))
    unsupported_capabilities = sorted(set(profile.allowed_capabilities) - PROFILE_CAPABILITIES)
    if unsupported_capabilities:
        issues.append(
            ConnectorValidationIssue(
                "allowed_capabilities",
                f"Unsupported or live capabilities are not allowed: {', '.join(unsupported_capabilities)}.",
            )
        )
    live_capabilities = sorted(set(profile.allowed_capabilities) & LIVE_CAPABILITIES)
    if live_capabilities:
        issues.append(
            ConnectorValidationIssue(
                "allowed_capabilities",
                f"Live capabilities are not allowed in the current registry: {', '.join(live_capabilities)}.",
            )
        )
    if not profile.prohibited_capabilities:
        issues.append(ConnectorValidationIssue("prohibited_capabilities", "Profiles must explicitly name prohibited capabilities."))
    if not profile.data_classes:
        issues.append(ConnectorValidationIssue("data_classes", "At least one described data class is required."))
    unsupported_data = sorted(set(profile.data_classes) - DATA_CLASSES)
    if unsupported_data:
        issues.append(ConnectorValidationIssue("data_classes", f"Unsupported data classes: {', '.join(unsupported_data)}."))
    missing_audit = sorted(REQUIRED_AUDIT_FIELDS - set(profile.audit_requirements))
    if missing_audit:
        issues.append(
            ConnectorValidationIssue(
                "audit_requirements",
                f"Missing required audit fields: {', '.join(missing_audit)}.",
            )
        )
    if not profile.stop_triggers:
        issues.append(ConnectorValidationIssue("stop_triggers", "At least one stop trigger is required."))
    unknown_stop_triggers = sorted(set(profile.stop_triggers) - set(STOP_ACTION_TYPES))
    if unknown_stop_triggers:
        issues.append(
            ConnectorValidationIssue(
                "stop_triggers",
                f"Unknown stop triggers: {', '.join(unknown_stop_triggers)}.",
            )
        )
    if "client-controlled" in profile.data_classes:
        gate = profile.approval_gate.lower()
        if "signed scope" not in gate:
            issues.append(
                ConnectorValidationIssue(
                    "approval_gate",
                    "Client-controlled profiles must require signed scope in the approval gate.",
                )
            )
        if "review" not in gate:
            issues.append(
                ConnectorValidationIssue(
                    "approval_gate",
                    "Client-controlled profiles must require review before client-visible output.",
                )
            )
        if "client_data_access" not in profile.stop_triggers:
            issues.append(
                ConnectorValidationIssue(
                    "stop_triggers",
                    "Client-controlled profiles must include the client_data_access stop trigger.",
                )
            )
    if "restricted" in profile.data_classes and "human" not in profile.approval_gate.lower():
        issues.append(
            ConnectorValidationIssue(
                "approval_gate",
                "Restricted profiles must include an explicit human approval gate.",
            )
        )
    if "stop" not in profile.failure_behavior.lower():
        issues.append(ConnectorValidationIssue("failure_behavior", "Failure behavior must state a stop condition."))

    return ConnectorValidationReport(
        connector_id=profile.connector_id or "unknown",
        valid=not issues,
        issues=tuple(issues),
    )


def validate_connector_registry(profiles: Iterable[ConnectorProfile]) -> ConnectorRegistryReport:
    """Validate a full local connector registry profile set."""

    profile_list = tuple(profiles)
    profile_reports = tuple(validate_connector_profile(profile) for profile in profile_list)
    issues: list[ConnectorValidationIssue] = []
    seen: set[str] = set()

    for profile in profile_list:
        if profile.connector_id in seen:
            issues.append(ConnectorValidationIssue("connector_id", f"Duplicate connector ID: {profile.connector_id}."))
        seen.add(profile.connector_id)

    if not profile_list:
        issues.append(ConnectorValidationIssue("profiles", "Connector registry must contain at least one profile."))

    return ConnectorRegistryReport(
        valid=not issues and all(report.valid for report in profile_reports),
        profile_reports=profile_reports,
        issues=tuple(issues),
    )


def is_safe_connector_id(connector_id: str) -> bool:
    return bool(connector_id) and connector_id.strip() == connector_id and all(character in SAFE_ID_CHARS for character in connector_id)


def profiles_to_json(profiles: Iterable[ConnectorProfile]) -> str:
    """Serialize profile records as deterministic JSON for local validation."""

    return json.dumps([profile.to_dict() for profile in profiles], indent=2, sort_keys=True) + "\n"


def profiles_from_json(document: str) -> tuple[ConnectorProfile, ...]:
    """Load connector profiles from a local JSON string."""

    payload = json.loads(document)
    if not isinstance(payload, list):
        raise ValueError("Connector profile JSON must be a list.")
    return tuple(ConnectorProfile.from_dict(item) for item in payload)


def stop_trigger_for_capability(capability: str) -> str:
    return CAPABILITY_STOP_TRIGGERS.get(capability, "connector_profile_required")


class ConnectorRegistry:
    """Evaluate connector profile metadata without calling external systems."""

    def __init__(self, profiles: Iterable[ConnectorProfile] | None = None) -> None:
        profile_list = tuple(initial_connector_profiles() if profiles is None else profiles)
        self._profile_list = profile_list
        self._profiles_by_id = {profile.connector_id: profile for profile in profile_list}

    @property
    def profiles(self) -> tuple[ConnectorProfile, ...]:
        return self._profile_list

    def validate(self) -> ConnectorRegistryReport:
        return validate_connector_registry(self.profiles)

    def get_profile(self, connector_id: str) -> ConnectorProfile | None:
        return self._profiles_by_id.get(connector_id)

    def evaluate(self, request: ConnectorOperationRequest) -> ConnectorPermissionDecision:
        profile = self.get_profile(request.connector_id)
        if profile is None:
            return stopped_connector_decision(
                request,
                "connector_profile_required",
                "Connector profile is not registered under the Rev 2 local registry.",
            )

        report = validate_connector_profile(profile)
        if not report.valid:
            return stopped_connector_decision(
                request,
                "mission_validation_failed",
                "Connector profile failed local validation: " + "; ".join(report.reasons),
            )

        if not request.dry_run:
            return stopped_connector_decision(
                request,
                "connector_profile_required",
                "Live connector requests are blocked; only local dry-run registry evaluation is allowed.",
            )

        if request.data_classification not in CURRENT_REQUEST_DATA_CLASSES:
            return stopped_connector_decision(
                request,
                "client_data_access",
                "Current Rev 2 connector requests may use only public, internal, or synthetic data classes.",
            )

        if request.capability in LIVE_CAPABILITIES:
            return stopped_connector_decision(
                request,
                stop_trigger_for_capability(request.capability),
                "Requested capability is a live or external-action capability and is blocked.",
            )

        if request.capability not in PROFILE_CAPABILITIES:
            return stopped_connector_decision(
                request,
                "connector_profile_required",
                "Requested capability is outside the local connector registry capability set.",
            )

        if request.capability not in profile.allowed_capabilities:
            return stopped_connector_decision(
                request,
                "connector_profile_required",
                "Default deny: this connector profile does not allow the requested local capability.",
            )

        return ConnectorPermissionDecision(
            request_id=request.request_id,
            connector_id=request.connector_id,
            capability=request.capability,
            allowed=True,
            mode="dry-run-local-validation",
            reason="Request is limited to local connector registry validation; no external system is called.",
        )


def stopped_connector_decision(
    request: ConnectorOperationRequest,
    stop_trigger: str,
    reason: str,
) -> ConnectorPermissionDecision:
    return ConnectorPermissionDecision(
        request_id=request.request_id,
        connector_id=request.connector_id,
        capability=request.capability,
        allowed=False,
        mode="stop",
        reason=reason,
        stop_trigger=stop_trigger,
    )
