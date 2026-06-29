"""M365 Graph auth status + R0 observe endpoints.

- GET  /api/v1/m365/status  — auth config readiness (no live MSAL call)
- POST /api/v1/m365/observe — R0 dry-run observe action with EvidencePacket
"""
from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from deps import verify_api_key
from gail_ai_operating_system.m365_auth import GRAPH_SCOPE, GraphAuthProvider
from gail_ai_operating_system.m365_reader import observe_graph_metadata

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("/m365/status")
def m365_status() -> dict:
    """Return Graph auth configuration readiness. No live MSAL call, no token in response."""
    tenant_id_present = bool(os.environ.get("AZURE_TENANT_ID", ""))
    client_id_present = bool(os.environ.get("AZURE_CLIENT_ID", ""))
    client_secret_present = bool(os.environ.get("AZURE_CLIENT_SECRET", ""))
    configured = tenant_id_present and client_id_present and client_secret_present
    return {
        "configured": configured,
        "tenant_id_present": tenant_id_present,
        "client_id_present": client_id_present,
        "client_secret_present": client_secret_present,
        "scope": GRAPH_SCOPE,
        "boundary": "A1 local no-network",
        "note": "Live token acquisition requires Azure app registration and env vars set at runtime.",
    }


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


@router.post("/m365/observe")
def m365_observe(req: Optional[ObserveRequest] = None) -> dict:
    """Execute an R0 dry-run observe action. Returns an EvidencePacket. No live Graph call."""
    req = req or ObserveRequest()
    if req.dry_run is not True:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="m365/observe is dry-run only in the A1 local boundary.",
        )
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
    )
    return {"ok": True, "evidence": packet.to_dict()}
