"""M365 Graph R2 internal write endpoints.

- POST /api/v1/m365/write/planner-task — R2 dry-run create a Planner task
  and persist the EvidencePacket to local_store.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from deps import record_api_trace_event, verify_api_key
from gail_ai_operating_system.evidence_store import save_evidence_packet
from gail_ai_operating_system.m365_auth import GraphAuthProvider
from gail_ai_operating_system.m365_writer import create_planner_task
from gail_ai_operating_system.trace_identity import CNS_TRACE_ID_PATTERN, ensure_cns_trace_id

router = APIRouter(dependencies=[Depends(verify_api_key)])


class PlannerTaskRequest(BaseModel):
    mission_id: str = Field(..., min_length=8, max_length=160, pattern=r"^mission-.+")
    action_id: str = Field(..., min_length=7, max_length=160, pattern=r"^action-.+")
    actor: str = Field(..., min_length=1, max_length=160)
    created_at: str = Field(..., min_length=1, max_length=64)
    plan_id: str = Field(..., min_length=1, max_length=255)
    bucket_id: str = Field(..., min_length=1, max_length=255)
    task_title: str = Field(..., min_length=1, max_length=255)
    cns_trace_id: str | None = Field(default=None, pattern=CNS_TRACE_ID_PATTERN)


@router.post("/m365/write/planner-task")
def m365_write_planner_task(req: PlannerTaskRequest) -> dict:
    """Create a Planner task (R2 dry-run). Stores and returns EvidencePacket. No live Graph call."""
    cns_trace_id = ensure_cns_trace_id(req.cns_trace_id)
    auth = GraphAuthProvider.from_env()
    packet = create_planner_task(
        auth,
        mission_id=req.mission_id,
        action_id=req.action_id,
        actor=req.actor,
        created_at=req.created_at,
        plan_id=req.plan_id,
        bucket_id=req.bucket_id,
        task_title=req.task_title,
        dry_run=True,
        allow_live=False,
        cns_trace_id=cns_trace_id,
    )
    save_evidence_packet(packet)
    record_api_trace_event(
        cns_trace_id=cns_trace_id,
        event_type="evidence.recorded",
        source_ref=f"api/v1/m365/write/planner-task/{packet.evidence_id}",
        summary="Microsoft 365 Planner-task dry-run evidence recorded.",
        mission_id=packet.mission_id,
        action_id=packet.action_id,
        evidence_id=packet.evidence_id,
        status=packet.result,
        risk_tier=2,
        idempotency_key=f"m365-write-planner-task:{packet.mission_id}:{packet.action_id}",
        metadata={
            "action_type": packet.action_type,
            "execution_mode": packet.execution_mode,
            "target": "planner-task",
        },
    )
    return {"ok": True, "cns_trace_id": cns_trace_id, "evidence": packet.to_dict()}
