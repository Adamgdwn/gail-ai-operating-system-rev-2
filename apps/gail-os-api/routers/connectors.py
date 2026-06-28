"""Connector registry endpoint — GET /api/v1/connectors."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from deps import verify_api_key
from gail_ai_operating_system.connector_registry import ConnectorRegistry

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("/connectors")
def list_connectors() -> dict:
    """Return connector registry status — all planning-only profiles, no live access."""
    registry = ConnectorRegistry()
    report = registry.validate()
    return {
        "registry_valid": report.valid,
        "connector_count": len(registry.profiles),
        "connectors": [
            {
                "connector_id": p.connector_id,
                "display_name": p.display_name,
                "system_family": p.system_family,
                "current_state": p.current_state,
                "allowed_capabilities": list(p.allowed_capabilities),
                "live_access_enabled": p.live_access_enabled,
            }
            for p in registry.profiles
        ],
    }
