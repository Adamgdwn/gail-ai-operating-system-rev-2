"""M365 Graph R2 internal write endpoints.

- POST /api/v1/m365/write/planner-task — R2 dry-run create a Planner task
  and persist the EvidencePacket to local_store.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from deps import verify_api_key
from gail_ai_operating_system.evidence_store import save_evidence_packet
from gail_ai_operating_system.m365_auth import GraphAuthProvider
from gail_ai_operating_system.m365_writer import create_planner_task

router = APIRouter(dependencies=[Depends(verify_api_key)])


class PlannerTaskRequest(BaseModel):
    mission_id: str = Field(..., min_length=8, max_length=160, pattern=r"^mission-.+")
    action_id: str = Field(..., min_length=7, max_length=160, pattern=r"^action-.+")
    actor: str = Field(..., min_length=1, max_length=160)
    created_at: str = Field(..., min_length=1, max_length=64)
    plan_id: str = Field(..., min_length=1, max_length=255)
    bucket_id: str = Field(..., min_length=1, max_length=255)
    task_title: str = Field(..., min_length=1, max_length=255)


@router.post("/m365/write/planner-task")
def m365_write_planner_task(req: PlannerTaskRequest) -> dict:
    """Create a Planner task (R2 dry-run). Stores and returns EvidencePacket. No live Graph call."""
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
    )
    save_evidence_packet(packet)
    return {"ok": True, "evidence": packet.to_dict()}
