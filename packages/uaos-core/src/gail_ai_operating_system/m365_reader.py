"""M365 Graph R0 observe action - read-only structured metadata, no raw content.

Implements the first M365 read action (Phase 4, task 4.3). In dry-run mode
(default and A1 boundary), no live Graph call is made - auth config is
checked and a planned EvidencePacket is produced. Live mode (allow_live=True)
is a dormant future app-only path. Current API routes force dry-run.

Current tenant state:
  - Delegated permission expansion exists for the local CLI app.
  - No client secret, certificate, or app-only grant exists.
  - Future app-only live calls require a separate owner-approved credential
    boundary before AZURE_* app-only env vars are real.
"""
from __future__ import annotations

from typing import Any

import httpx

from gail_ai_operating_system.evidence_packet import (
    EvidenceResult,
    EvidencePacket,
    ExecutionMode,
    create_evidence_packet,
)
from gail_ai_operating_system.m365_auth import GraphAuthProvider, GraphAuthError

_GRAPH_BASE = "https://graph.microsoft.com/v1.0"
ALLOWED_OBSERVE_TARGETS = frozenset({"organization"})


def observe_graph_metadata(
    auth: GraphAuthProvider,
    *,
    mission_id: str,
    action_id: str,
    actor: str,
    created_at: str,
    observe_target: str = "organization",
    dry_run: bool = True,
    allow_live: bool = False,
    cns_trace_id: str | None = None,
) -> EvidencePacket:
    """Execute an R0 observe action against Microsoft Graph.

    Dry-run (default): validates auth config, produces a planned EvidencePacket
    without any live call - safe under the A1 local no-network boundary.

    Future live mode (dry_run=False, allow_live=True): may acquire an app-only
    token and call Graph API only after a later owner-approved app-only
    credential boundary. No current API route passes those flags.
    """
    if observe_target not in ALLOWED_OBSERVE_TARGETS:
        return create_evidence_packet(
            mission_id=mission_id,
            action_id=action_id,
            actor=actor,
            action_type=f"m365.observe.{observe_target}",
            authority_basis="R0_OBSERVE — m365-graph-api-bridge — invalid target",
            result=EvidenceResult.STOPPED.value,
            created_at=created_at,
            execution_mode=ExecutionMode.DRY_RUN.value,
            rollback_note="No action taken; observe target is not in the allowed list.",
            outcome_summary=(
                f"observe_target '{observe_target}' is not allowed. "
                f"Allowed: {sorted(ALLOWED_OBSERVE_TARGETS)}."
            ),
            cns_trace_id=cns_trace_id,
            allow_live=False,
        )

    if not auth.is_configured():
        return create_evidence_packet(
            mission_id=mission_id,
            action_id=action_id,
            actor=actor,
            action_type=f"m365.observe.{observe_target}",
            authority_basis="R0_OBSERVE — m365-graph-api-bridge — not configured",
            result=EvidenceResult.STOPPED.value,
            created_at=created_at,
            execution_mode=ExecutionMode.DRY_RUN.value,
            rollback_note="No action taken; Graph auth credentials not configured.",
            outcome_summary=(
                "Future app-only Graph auth provider is not configured. "
                "Current approved Microsoft 365 state is delegated-only; "
                "no client secret, certificate, or app-only grant exists."
            ),
            cns_trace_id=cns_trace_id,
            allow_live=False,
        )

    if dry_run:
        return create_evidence_packet(
            mission_id=mission_id,
            action_id=action_id,
            actor=actor,
            action_type=f"m365.observe.{observe_target}",
            authority_basis=(
                f"R0_OBSERVE — m365-graph-api-bridge (registry-only) "
                f"— dry-run — target={observe_target}"
            ),
            result=EvidenceResult.SUCCESS.value,
            created_at=created_at,
            execution_mode=ExecutionMode.DRY_RUN.value,
            rollback_note="Dry-run only; no external call made.",
            outcome_summary=(
                f"Dry-run observe planned for target '{observe_target}'. "
                "Auth provider is configured. No live Graph call made."
            ),
            cns_trace_id=cns_trace_id,
            allow_live=False,
        )

    # Future live path. EvidencePacket validation rejects LIVE when allow_live is False.
    try:
        token = auth.get_token()
    except GraphAuthError as exc:
        return create_evidence_packet(
            mission_id=mission_id,
            action_id=action_id,
            actor=actor,
            action_type=f"m365.observe.{observe_target}",
            authority_basis="R0_OBSERVE — m365-graph-api-bridge — token acquisition failed",
            result=EvidenceResult.FAILURE.value,
            created_at=created_at,
            execution_mode=ExecutionMode.DRY_RUN.value,
            rollback_note="No data read; token acquisition failed before any Graph call.",
            outcome_summary=f"Token acquisition failed: {exc}",
            cns_trace_id=cns_trace_id,
            allow_live=False,
        )

    metadata = _fetch_org_metadata(token)
    return create_evidence_packet(
        mission_id=mission_id,
        action_id=action_id,
        actor=actor,
        action_type=f"m365.observe.{observe_target}",
        authority_basis=(
            f"R0_OBSERVE — m365-graph-api-bridge (registry-only) "
            f"— live — target={observe_target}"
        ),
        result=EvidenceResult.SUCCESS.value,
        created_at=created_at,
        execution_mode=ExecutionMode.LIVE.value,
        rollback_note="R0 observe — read-only, no state mutation, no rollback needed.",
        outcome_summary=_summarize_org(metadata),
        cns_trace_id=cns_trace_id,
        allow_live=allow_live,
    )


def _fetch_org_metadata(token: str) -> dict[str, Any]:
    """GET /v1.0/organization — minimal org metadata, no raw content."""
    url = f"{_GRAPH_BASE}/organization?$select=id,displayName,verifiedDomains"
    with httpx.Client(timeout=10.0) as http:
        response = http.get(url, headers={"Authorization": f"Bearer {token}"})
        response.raise_for_status()
    data = response.json()
    orgs = data.get("value", [])
    return orgs[0] if orgs else {}


def _summarize_org(metadata: dict[str, Any]) -> str:
    org_id = metadata.get("id", "unknown")
    display_name = metadata.get("displayName", "unknown")
    domains = [
        d.get("name", "")
        for d in metadata.get("verifiedDomains", [])
        if d.get("isDefault")
    ]
    primary_domain = domains[0] if domains else "unknown"
    return (
        f"Organization observed: displayName={display_name!r}, "
        f"id={org_id!r}, primaryDomain={primary_domain!r}. "
        "No raw content stored."
    )


__all__ = ["observe_graph_metadata", "ALLOWED_OBSERVE_TARGETS"]
