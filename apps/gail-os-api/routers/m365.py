"""M365 Graph auth status + R0 observe endpoints.

- GET  /api/v1/m365/status  — auth config readiness (no live MSAL call)
- POST /api/v1/m365/observe — R0 dry-run observe action with EvidencePacket
"""
from __future__ import annotations

import os

from fastapi import APIRouter, Depends
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
    mission_id: str = Field(..., min_length=8, max_length=160, pattern=r"^mission-.+")
    action_id: str = Field(..., min_length=7, max_length=160, pattern=r"^action-.+")
    actor: str = Field(..., min_length=1, max_length=160)
    created_at: str = Field(..., min_length=1, max_length=64)
    observe_target: str = Field(default="organization", max_length=64)


@router.post("/m365/observe")
def m365_observe(req: ObserveRequest) -> dict:
    """Execute an R0 dry-run observe action. Returns an EvidencePacket. No live Graph call."""
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
