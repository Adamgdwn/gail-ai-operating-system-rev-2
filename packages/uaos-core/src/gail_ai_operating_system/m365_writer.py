"""M365 Graph R2 internal write actions - governed writes with EvidencePacket.

Implements the first M365 internal write (Phase 4, task 4.4). In dry-run
mode (default and A1 boundary), no live Graph call is made - inputs and
auth config are validated and a planned EvidencePacket is produced.

Live mode is a dormant future app-only path. Current API routes force dry-run.

Current supported write targets:
  - planner-task: POST /v1.0/planner/tasks (Planner task in a known plan)

Current tenant state:
  - Delegated permission expansion exists for the local CLI app.
  - No client secret, certificate, or app-only grant exists.
  - Future app-only live calls require a separate owner-approved credential
    boundary, connector promotion, and allow_live=True from a governed caller.
"""
from __future__ import annotations

import httpx

from gail_ai_operating_system.evidence_packet import (
    EvidenceResult,
    EvidencePacket,
    ExecutionMode,
    create_evidence_packet,
)
from gail_ai_operating_system.m365_auth import GraphAuthProvider, GraphAuthError

_GRAPH_BASE = "https://graph.microsoft.com/v1.0"
ALLOWED_WRITE_TARGETS = frozenset({"planner-task"})
_MAX_TITLE_LEN = 255


def create_planner_task(
    auth: GraphAuthProvider,
    *,
    mission_id: str,
    action_id: str,
    actor: str,
    created_at: str,
    plan_id: str,
    bucket_id: str,
    task_title: str,
    dry_run: bool = True,
    allow_live: bool = False,
) -> EvidencePacket:
    """Execute an R2 internal write — create a Planner task under a known plan.

    Dry-run (default): validates inputs and auth config, produces a planned
    EvidencePacket without any live call - safe under A1 no-network boundary.

    Future live mode (dry_run=False, allow_live=True): may acquire an app-only
    token and call POST /v1.0/planner/tasks only after a later owner-approved
    app-only credential boundary. No current API route passes those flags.
    """
    if not plan_id.strip():
        return create_evidence_packet(
            mission_id=mission_id,
            action_id=action_id,
            actor=actor,
            action_type="m365.write.planner-task",
            authority_basis="R2_INTERNAL_WRITE — m365-graph-api-bridge — invalid input",
            result=EvidenceResult.STOPPED.value,
            created_at=created_at,
            execution_mode=ExecutionMode.DRY_RUN.value,
            rollback_note="No action taken; plan_id is required.",
            outcome_summary="plan_id must be a non-empty string.",
            allow_live=False,
        )

    if not bucket_id.strip():
        return create_evidence_packet(
            mission_id=mission_id,
            action_id=action_id,
            actor=actor,
            action_type="m365.write.planner-task",
            authority_basis="R2_INTERNAL_WRITE — m365-graph-api-bridge — invalid input",
            result=EvidenceResult.STOPPED.value,
            created_at=created_at,
            execution_mode=ExecutionMode.DRY_RUN.value,
            rollback_note="No action taken; bucket_id is required.",
            outcome_summary="bucket_id must be a non-empty string.",
            allow_live=False,
        )

    if not task_title.strip() or len(task_title) > _MAX_TITLE_LEN:
        return create_evidence_packet(
            mission_id=mission_id,
            action_id=action_id,
            actor=actor,
            action_type="m365.write.planner-task",
            authority_basis="R2_INTERNAL_WRITE — m365-graph-api-bridge — invalid input",
            result=EvidenceResult.STOPPED.value,
            created_at=created_at,
            execution_mode=ExecutionMode.DRY_RUN.value,
            rollback_note="No action taken; task_title is invalid.",
            outcome_summary=(
                f"task_title must be 1–{_MAX_TITLE_LEN} characters. "
                f"Got: {len(task_title)} chars."
            ),
            allow_live=False,
        )

    if not auth.is_configured():
        return create_evidence_packet(
            mission_id=mission_id,
            action_id=action_id,
            actor=actor,
            action_type="m365.write.planner-task",
            authority_basis="R2_INTERNAL_WRITE — m365-graph-api-bridge — not configured",
            result=EvidenceResult.STOPPED.value,
            created_at=created_at,
            execution_mode=ExecutionMode.DRY_RUN.value,
            rollback_note="No action taken; Graph auth credentials not configured.",
            outcome_summary=(
                "Future app-only Graph auth provider is not configured. "
                "Current approved Microsoft 365 state is delegated-only; "
                "no client secret, certificate, or app-only grant exists."
            ),
            allow_live=False,
        )

    if dry_run:
        return create_evidence_packet(
            mission_id=mission_id,
            action_id=action_id,
            actor=actor,
            action_type="m365.write.planner-task",
            authority_basis=(
                "R2_INTERNAL_WRITE — m365-graph-api-bridge (registry-only) "
                "— dry-run — target=planner-task"
            ),
            result=EvidenceResult.SUCCESS.value,
            created_at=created_at,
            execution_mode=ExecutionMode.DRY_RUN.value,
            rollback_note="Dry-run only; no Planner task created.",
            outcome_summary=(
                f"Dry-run Planner task planned: title={task_title!r}, "
                f"plan_id={plan_id!r}, bucket_id={bucket_id!r}. "
                "No live Graph call made."
            ),
            allow_live=False,
        )

    # Future live path. EvidencePacket validation rejects LIVE mode if allow_live is False.
    try:
        token = auth.get_token()
    except GraphAuthError as exc:
        return create_evidence_packet(
            mission_id=mission_id,
            action_id=action_id,
            actor=actor,
            action_type="m365.write.planner-task",
            authority_basis="R2_INTERNAL_WRITE — m365-graph-api-bridge — token acquisition failed",
            result=EvidenceResult.FAILURE.value,
            created_at=created_at,
            execution_mode=ExecutionMode.DRY_RUN.value,
            rollback_note="No task created; token acquisition failed before any Graph call.",
            outcome_summary=f"Token acquisition failed: {exc}",
            allow_live=False,
        )

    task_id = _post_planner_task(token, plan_id=plan_id, bucket_id=bucket_id, title=task_title)
    return create_evidence_packet(
        mission_id=mission_id,
        action_id=action_id,
        actor=actor,
        action_type="m365.write.planner-task",
        authority_basis=(
            "R2_INTERNAL_WRITE — m365-graph-api-bridge (registry-only) "
            "— live — target=planner-task"
        ),
        result=EvidenceResult.SUCCESS.value,
        created_at=created_at,
        execution_mode=ExecutionMode.LIVE.value,
        rollback_note=f"Undo: DELETE /v1.0/planner/tasks/{task_id}",
        outcome_summary=(
            f"Planner task created: task_id={task_id!r}, title={task_title!r}, "
            f"plan_id={plan_id!r}. No raw task content stored."
        ),
        allow_live=allow_live,
    )


def _post_planner_task(
    token: str,
    *,
    plan_id: str,
    bucket_id: str,
    title: str,
) -> str:
    """POST /v1.0/planner/tasks — returns the created task_id."""
    url = f"{_GRAPH_BASE}/planner/tasks"
    payload = {
        "planId": plan_id,
        "bucketId": bucket_id,
        "title": title,
    }
    with httpx.Client(timeout=10.0) as http:
        response = http.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        )
        response.raise_for_status()
    return response.json().get("id", "unknown")


__all__ = ["create_planner_task", "ALLOWED_WRITE_TARGETS"]
