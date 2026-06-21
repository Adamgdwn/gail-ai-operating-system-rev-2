"""Read-only Graphify handoff checkpoint for GAIL AI Operating System Rev 2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from .connector_registry import ConnectorOperationRequest, ConnectorPermissionDecision, ConnectorRegistry
from .mission_spine import MissionAction, STOP_ACTION_TYPES


GRAPHIFY_CONNECTOR_ID = "graphify-enhanced-handoff"
GRAPHIFY_GOVERNANCE_PATH = "/home/adamgoodwin/code/Tools/graphify/docs/agent-governance.md"
WORKSPACE_GRAPH_PATH = "/home/adamgoodwin/code/Tools/graphify/workspace/out/graph.json"
WORKSPACE_GRAPH_WINDOWS_PATH = "L:\\Tools\\graphify\\workspace\\out\\graph.json"
REPO_LOCAL_GRAPH_PATH = "graphify-out/graph.json"

MIN_CONFIDENCE = 0.6
ALLOWED_RISKS = frozenset({"low", "medium"})
ALLOWED_APPROVAL_LEVELS = frozenset({"A1", "A1 local no-network", "A1 dry-run", "A2 review"})
ALLOWED_DATA_CLASSES = frozenset({"public", "internal", "synthetic"})
ALLOWED_RECOMMENDATION_STATUSES = frozenset({"candidate", "proposed", "read-only", "needs-review"})
PROHIBITED_RECOMMENDATION_STATUSES = frozenset({"executed", "approved", "completed", "applied"})

APPROVED_GRAPH_REFERENCES = frozenset(
    {
        WORKSPACE_GRAPH_PATH,
        WORKSPACE_GRAPH_WINDOWS_PATH,
        REPO_LOCAL_GRAPH_PATH,
        f"./{REPO_LOCAL_GRAPH_PATH}",
    }
)

PROHIBITED_ACTION_HINTS = (
    "/graphify",
    "full semantic rebuild",
    "source mutation",
    "mutate",
    "graph upload",
    "upload graph",
    "execute",
    "run recommendation",
    "delete",
    "remove",
    "commit",
    "push",
    "send",
    "email",
    "message",
    "permission",
    "tenant",
    "billing",
    "payment",
    "quickbooks",
    "microsoft 365",
    "m365",
    "live connector",
    "client data",
    "client-controlled",
    "raw audio",
    "raw log",
    "production",
    "deploy",
    "secret",
    "token",
    "credential",
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
    "invoice-export",
    "accounting-export",
)


@dataclass(frozen=True)
class GraphifyRouteStatus:
    """Current safe route for consuming Graphify as orientation only."""

    connector_id: str
    status: str
    workspace_graph_path: str
    repo_local_graph_path: str
    governance_path: str
    workspace_graph_available: bool
    repo_local_graph_available: bool
    graphify_cli_available: bool
    setup_cli_available: bool
    allowed_commands: tuple[str, ...]
    next_step: str
    connector_decision: ConnectorPermissionDecision

    def to_dict(self) -> dict[str, Any]:
        return {
            "connector_id": self.connector_id,
            "status": self.status,
            "workspace_graph_path": self.workspace_graph_path,
            "repo_local_graph_path": self.repo_local_graph_path,
            "governance_path": self.governance_path,
            "workspace_graph_available": self.workspace_graph_available,
            "repo_local_graph_available": self.repo_local_graph_available,
            "graphify_cli_available": self.graphify_cli_available,
            "setup_cli_available": self.setup_cli_available,
            "allowed_commands": list(self.allowed_commands),
            "next_step": self.next_step,
            "connector_decision": self.connector_decision.to_dict(),
        }


@dataclass(frozen=True)
class GraphifyHandoffCandidate:
    """A read-only Graphify recommendation that may become a Rev 2 mission candidate."""

    candidate_id: str
    source_recommendation_id: str
    title: str
    summary: str
    graph_reference: str
    evidence_refs: tuple[str, ...]
    confidence: float
    risk: str
    approval_level: str
    files_in_scope: tuple[str, ...]
    non_goals: tuple[str, ...]
    stop_triggers: tuple[str, ...]

    def to_mission_action(self) -> MissionAction:
        """Convert a candidate to a dry-run local action for the Rev 2 policy gate."""

        risk_tier = {"low": 1, "medium": 2}.get(self.risk, 3)
        return MissionAction(
            action_id=f"graphify-{self.source_recommendation_id}",
            action_type="graphify_handoff_read",
            title=f"Review Graphify handoff candidate: {self.title}",
            arguments={
                "source": "graphify",
                "source_recommendation_id": self.source_recommendation_id,
                "title": self.title,
                "summary": self.summary,
                "graph_reference": self.graph_reference,
                "evidence_refs": list(self.evidence_refs),
                "confidence": self.confidence,
                "risk": self.risk,
                "approval_level": self.approval_level,
                "files_in_scope": list(self.files_in_scope),
                "non_goals": list(self.non_goals),
                "stop_triggers": list(self.stop_triggers),
            },
            risk_tier=risk_tier,
        )


@dataclass(frozen=True)
class GraphifyHandoffRejection:
    """One rejected Graphify handoff record."""

    source_recommendation_id: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class GraphifyHandoffValidationReport:
    """Validation result for a Graphify handoff payload."""

    schema_version: str | None
    graph_reference: str | None
    accepted: tuple[GraphifyHandoffCandidate, ...] = ()
    rejected: tuple[GraphifyHandoffRejection, ...] = ()

    @property
    def accepted_count(self) -> int:
        return len(self.accepted)

    @property
    def rejected_count(self) -> int:
        return len(self.rejected)

    @property
    def valid(self) -> bool:
        return bool(self.accepted) and not self.rejected


def build_graphify_route_status(
    *,
    workspace_graph_available: bool,
    repo_local_graph_available: bool,
    graphify_cli_available: bool,
    setup_cli_available: bool,
    registry: ConnectorRegistry | None = None,
    workspace_graph_path: str = WORKSPACE_GRAPH_PATH,
    repo_local_graph_path: str = REPO_LOCAL_GRAPH_PATH,
) -> GraphifyRouteStatus:
    """Build a local, no-network status record for the current Graphify route."""

    connector_decision = (registry or ConnectorRegistry()).evaluate(
        ConnectorOperationRequest(
            request_id="REQ-GRAPHIFY-ROUTE",
            connector_id=GRAPHIFY_CONNECTOR_ID,
            capability="readiness-check",
            data_classification="internal",
            dry_run=True,
        )
    )

    if not connector_decision.allowed:
        status = "stopped"
        next_step = connector_decision.reason
        allowed_commands: tuple[str, ...] = ()
    elif repo_local_graph_available and graphify_cli_available:
        status = "repo-local-graph-ready"
        next_step = "Use the repo-local graph for focused Rev 2 routing and update it with the cheap incremental command after code changes."
        allowed_commands = ("graphify query <question> --graph graphify-out/graph.json", "graphify update . --no-cluster")
    elif workspace_graph_available:
        status = "workspace-graph-ready"
        next_step = "Use the existing workspace graph for routing, then inspect only selected files. Set up a repo-local graph when the tool is available in the active shell."
        allowed_commands = ("graphify query <question> --graph /home/adamgoodwin/code/Tools/graphify/workspace/out/graph.json",)
        if setup_cli_available:
            allowed_commands = allowed_commands + ("graphify-setup-project .",)
    else:
        status = "blocked"
        next_step = "Graphify handoff is blocked until an approved workspace or repo-local graph is available."
        allowed_commands = ()

    return GraphifyRouteStatus(
        connector_id=GRAPHIFY_CONNECTOR_ID,
        status=status,
        workspace_graph_path=workspace_graph_path,
        repo_local_graph_path=repo_local_graph_path,
        governance_path=GRAPHIFY_GOVERNANCE_PATH,
        workspace_graph_available=workspace_graph_available,
        repo_local_graph_available=repo_local_graph_available,
        graphify_cli_available=graphify_cli_available,
        setup_cli_available=setup_cli_available,
        allowed_commands=allowed_commands,
        next_step=next_step,
        connector_decision=connector_decision,
    )


def validate_graphify_handoff_payload(
    payload: Mapping[str, Any],
    *,
    existing_evidence_refs: Iterable[str] | None = None,
    route_status: GraphifyRouteStatus | None = None,
    min_confidence: float = MIN_CONFIDENCE,
    allowed_risks: Iterable[str] = ALLOWED_RISKS,
) -> GraphifyHandoffValidationReport:
    """Validate Graphify output as read-only mission candidates, never actions."""

    schema_version = _string_or_none(payload.get("schema_version"))
    graph_reference = _graph_reference(payload)
    recommendations = payload.get("recommendations", payload.get("actions"))
    known_evidence = _normalized_set(existing_evidence_refs)
    allowed_risk_set = {risk.lower() for risk in allowed_risks}
    global_reasons = _validate_graph_context(graph_reference, route_status)

    if not isinstance(recommendations, list):
        return GraphifyHandoffValidationReport(
            schema_version=schema_version,
            graph_reference=graph_reference,
            rejected=(
                GraphifyHandoffRejection(
                    source_recommendation_id="payload",
                    reasons=tuple(global_reasons + ["recommendations must be a list"]),
                ),
            ),
        )

    accepted: list[GraphifyHandoffCandidate] = []
    rejected: list[GraphifyHandoffRejection] = []

    for index, recommendation in enumerate(recommendations):
        source_recommendation_id = _field_as_text(recommendation, "source_recommendation_id", fallback=f"recommendation-{index}")
        candidate, reasons = _validate_recommendation(
            recommendation,
            source_recommendation_id=source_recommendation_id,
            graph_reference=graph_reference,
            global_reasons=global_reasons,
            known_evidence=known_evidence,
            min_confidence=min_confidence,
            allowed_risks=allowed_risk_set,
        )
        if reasons:
            rejected.append(GraphifyHandoffRejection(source_recommendation_id=source_recommendation_id, reasons=tuple(reasons)))
        elif candidate is not None:
            accepted.append(candidate)

    return GraphifyHandoffValidationReport(
        schema_version=schema_version,
        graph_reference=graph_reference,
        accepted=tuple(accepted),
        rejected=tuple(rejected),
    )


def _validate_graph_context(graph_reference: str | None, route_status: GraphifyRouteStatus | None) -> list[str]:
    reasons: list[str] = []
    if not graph_reference:
        reasons.append("graph reference is required")
    elif _normalize_ref(graph_reference) not in _normalized_set(APPROVED_GRAPH_REFERENCES):
        reasons.append("graph reference must point to the approved workspace graph or repo-local graph")
    elif _contains_sensitive_reference(graph_reference):
        reasons.append("graph reference must not point at secrets, raw payloads, or client data")

    if route_status is not None:
        if not route_status.connector_decision.allowed:
            reasons.append("Graphify connector readiness-check is not allowed")
        if route_status.status in {"blocked", "stopped"}:
            reasons.append("Graphify route is not currently usable")

    return reasons


def _validate_recommendation(
    recommendation: Any,
    *,
    source_recommendation_id: str,
    graph_reference: str | None,
    global_reasons: list[str],
    known_evidence: set[str] | None,
    min_confidence: float,
    allowed_risks: set[str],
) -> tuple[GraphifyHandoffCandidate | None, list[str]]:
    reasons = list(global_reasons)
    if not isinstance(recommendation, dict):
        return None, reasons + ["recommendation must be an object"]

    status = _field_as_text(recommendation, "status", fallback="candidate").lower()
    if status in PROHIBITED_RECOMMENDATION_STATUSES:
        reasons.append("recommendation status must remain candidate/read-only, not executed or approved")
    elif status not in ALLOWED_RECOMMENDATION_STATUSES:
        reasons.append("recommendation status is outside the read-only handoff envelope")

    if any(key in recommendation for key in ("executed_at", "approved_at", "result", "rollback_note")):
        reasons.append("handoff payload must not include execution, approval, result, or rollback fields")

    if not _field_as_text(recommendation, "source_recommendation_id"):
        reasons.append("source_recommendation_id is required")

    title = _field_as_text(recommendation, "title") or _field_as_text(recommendation, "rec_title")
    summary = _field_as_text(recommendation, "summary") or _field_as_text(recommendation, "rec_summary")
    if not title:
        reasons.append("title is required")
    if not summary:
        reasons.append("summary is required")

    checked_action_text = " ".join(
        part
        for part in (
            _field_as_text(recommendation, "action_type"),
            _field_as_text(recommendation, "proposed_action_text"),
            title,
            summary,
        )
        if part
    )
    if _contains_prohibited_action_hint(checked_action_text):
        reasons.append("recommendation implies execution, mutation, live connector use, or sensitive access")

    confidence = _number_or_none(recommendation.get("confidence"))
    if confidence is None:
        reasons.append("confidence must be a number")
        confidence = 0.0
    elif confidence < min_confidence:
        reasons.append(f"confidence must be >= {min_confidence}")

    risk = _field_as_text(recommendation, "risk").lower()
    if risk not in allowed_risks:
        reasons.append("risk is outside the approved read-only Graphify handoff envelope")

    data_classification = _field_as_text(recommendation, "data_classification", fallback="internal").lower()
    if data_classification not in ALLOWED_DATA_CLASSES:
        reasons.append("data classification must remain public, internal, or synthetic")

    evidence_refs = tuple(_evidence_refs(recommendation.get("evidence")))
    if not evidence_refs:
        reasons.append("evidence must include at least one graph node or source reference")
    elif known_evidence is not None:
        missing = [ref for ref in evidence_refs if _normalize_ref(ref) not in known_evidence]
        if missing:
            reasons.append("evidence refs must exist in the current approved graph evidence set")
    if any(_contains_sensitive_reference(ref) or _unsafe_ref(ref) for ref in evidence_refs):
        reasons.append("evidence refs must not include secrets, raw payloads, client data, absolute paths, or parent traversal")

    hint = recommendation.get("mission_hint", recommendation.get("uaos_mission_hint", {}))
    if not isinstance(hint, dict):
        reasons.append("mission_hint must be an object")
        hint = {}

    approval_level = _field_as_text(hint, "approval_level", fallback="A1 local no-network")
    if approval_level not in ALLOWED_APPROVAL_LEVELS:
        reasons.append("approval level must remain A1/A2 review only")

    files_in_scope = tuple(_text_list(hint.get("files_in_scope", recommendation.get("files_in_scope"))))
    if not files_in_scope:
        reasons.append("files_in_scope must include at least one relative Rev 2 file path")
    elif any(_unsafe_ref(path) or _contains_sensitive_reference(path) for path in files_in_scope):
        reasons.append("files_in_scope must use relative non-sensitive repo references")

    stop_triggers = tuple(_text_list(hint.get("stop_triggers", recommendation.get("stop_triggers"))))
    unknown_stop_triggers = sorted(set(stop_triggers) - set(STOP_ACTION_TYPES))
    if not stop_triggers:
        reasons.append("stop_triggers must include Graphify execution boundaries")
    elif unknown_stop_triggers:
        reasons.append(f"stop_triggers include unknown values: {', '.join(unknown_stop_triggers)}")
    elif "graphify_action_execution" not in stop_triggers:
        reasons.append("stop_triggers must include graphify_action_execution")

    non_goals = tuple(_text_list(hint.get("non_goals", recommendation.get("non_goals"))))

    if reasons:
        return None, reasons

    return (
        GraphifyHandoffCandidate(
            candidate_id=f"graphify-candidate-{source_recommendation_id}",
            source_recommendation_id=source_recommendation_id,
            title=title,
            summary=summary,
            graph_reference=graph_reference or "",
            evidence_refs=evidence_refs,
            confidence=confidence,
            risk=risk,
            approval_level=approval_level,
            files_in_scope=files_in_scope,
            non_goals=non_goals,
            stop_triggers=stop_triggers,
        ),
        [],
    )


def _graph_reference(payload: Mapping[str, Any]) -> str | None:
    graph = payload.get("graph")
    if isinstance(graph, Mapping):
        return _field_as_text(graph, "path") or _field_as_text(graph, "graph_path")
    return _field_as_text(payload, "graph_path") or None


def _field_as_text(container: Any, key: str, *, fallback: str = "") -> str:
    if not isinstance(container, Mapping):
        return fallback
    value = container.get(key, fallback)
    return value.strip() if isinstance(value, str) else fallback


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _number_or_none(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _text_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _evidence_refs(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    refs: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            refs.append(item.strip())
        elif isinstance(item, Mapping):
            ref = _field_as_text(item, "ref") or _field_as_text(item, "node_id") or _field_as_text(item, "source_file")
            if ref:
                refs.append(ref)
    return refs


def _normalized_set(values: Iterable[str] | None) -> set[str] | None:
    if values is None:
        return None
    return {_normalize_ref(value) for value in values}


def _normalize_ref(value: str) -> str:
    return value.strip().replace("\\", "/").removeprefix("./").rstrip("/").lower()


def _contains_prohibited_action_hint(value: str) -> bool:
    lowered = value.lower()
    return any(hint in lowered for hint in PROHIBITED_ACTION_HINTS)


def _contains_sensitive_reference(value: str) -> bool:
    lowered = value.lower().replace("\\", "/")
    return any(hint in lowered for hint in SENSITIVE_REFERENCE_HINTS)


def _unsafe_ref(value: str) -> bool:
    normalized = value.strip().replace("\\", "/")
    if not normalized:
        return True
    if normalized.startswith("/") or normalized.startswith("//"):
        return True
    if ":" in normalized.split("/", 1)[0]:
        return True
    return ".." in normalized.split("/")
