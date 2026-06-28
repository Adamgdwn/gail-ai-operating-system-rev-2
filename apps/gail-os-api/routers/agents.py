"""Agent registry endpoint — GET /api/v1/agents."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from deps import verify_api_key
from gail_ai_operating_system.agent_registry import AgentRegistry

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("/agents")
def list_agents() -> dict:
    """Return registered CNS agents — purpose, layer, authority level, and action kinds."""
    registry = AgentRegistry()
    report = registry.validate()
    return {
        "registry_valid": report.valid,
        "agent_count": len(registry.profiles),
        "agents": [
            {
                "agent_id": p.agent_id,
                "display_name": p.display_name,
                "purpose": p.purpose,
                "cns_layer": p.cns_layer,
                "owner": p.owner,
                "maturity": p.maturity,
                "max_authority_level": p.max_authority_level,
                "action_kinds": p.action_kinds,
                "live_access_enabled": p.live_access_enabled,
            }
            for p in registry.profiles
        ],
    }
