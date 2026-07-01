"""M365 Graph auth status + R0 observe endpoints.

- GET  /api/v1/m365/status  — auth config readiness (no live MSAL call)
- POST /api/v1/m365/observe — R0 dry-run observe action with EvidencePacket
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from deps import record_api_trace_event, verify_api_key
from gail_ai_operating_system.evidence_store import save_evidence_packet
from gail_ai_operating_system.m365_auth import (
    GraphAuthProvider,
    graph_auth_status_from_env,
)
from gail_ai_operating_system.m365_reader import observe_graph_metadata
from gail_ai_operating_system.trace_identity import CNS_TRACE_ID_PATTERN, ensure_cns_trace_id

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("/m365/status")
def m365_status() -> dict:
    """Return Graph auth configuration readiness. No live MSAL call, no token in response."""
    return graph_auth_status_from_env()


class ObserveRequest(BaseModel):
    mission_id: str = Field("mission-ctp2-probe", min_length=8, max_length=160, pattern=r"^mission-.+")
    action_id: str = Field("action-ctp2-m365-observe", min_length=7, max_length=160, pattern=r"^action-.+")
    actor: str = Field("linux-ctp2-probe", min_length=1, max_length=160)
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        min_length=1,
        max_length=64,
    )
    observe_target: str = Field(default="organization", max_length=64)
    dry_run: bool = Field(default=True)
    cns_trace_id: Optional[str] = Field(default=None, pattern=CNS_TRACE_ID_PATTERN)


@router.post("/m365/observe")
def m365_observe(req: Optional[ObserveRequest] = None) -> dict:
    """Execute an R0 dry-run observe action. Returns an EvidencePacket. No live Graph call."""
    req = req or ObserveRequest()
    if req.dry_run is not True:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="m365/observe is dry-run only in the A1 local boundary.",
        )
    cns_trace_id = ensure_cns_trace_id(req.cns_trace_id)
    auth = GraphAuthProvider.from_env()
    packet = observe_graph_metadata(
        auth,
        mission_id=req.mission_id,
        action_id=req.action_id,
        actor=req.actor,
        created_at=req.created_at,
        observe_target=req.observe_target,
        dry_run=True,
        allow_live=False,
        cns_trace_id=cns_trace_id,
    )
    save_evidence_packet(packet)
    record_api_trace_event(
        cns_trace_id=cns_trace_id,
        event_type="evidence.recorded",
        source_ref=f"api/v1/m365/observe/{packet.evidence_id}",
        summary="Microsoft 365 dry-run observe evidence recorded.",
        mission_id=packet.mission_id,
        action_id=packet.action_id,
        evidence_id=packet.evidence_id,
        status=packet.result,
        risk_tier=0,
        idempotency_key=f"m365-observe:{packet.mission_id}:{packet.action_id}",
        metadata={
            "action_type": packet.action_type,
            "execution_mode": packet.execution_mode,
            "observe_target": req.observe_target,
        },
    )
    return {"ok": True, "cns_trace_id": cns_trace_id, "evidence": packet.to_dict()}
