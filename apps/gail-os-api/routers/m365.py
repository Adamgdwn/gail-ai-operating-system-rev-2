"""M365 Graph auth status endpoint — GET /api/v1/m365/status.

Returns configuration readiness without making live Graph calls or
exposing credentials. Actual token acquisition (get_token) is deferred
to the Phase 4 read/write action routers once connectors are registered.
"""
from __future__ import annotations

import os

from fastapi import APIRouter, Depends

from deps import verify_api_key
from gail_ai_operating_system.m365_auth import GRAPH_SCOPE

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
