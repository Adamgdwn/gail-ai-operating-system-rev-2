"""Shared read-only state and trace lookup endpoints."""

from __future__ import annotations

from collections import Counter
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from deps import get_store_root, get_trace_event_store, verify_api_key
from gail_ai_operating_system.agent_registry import AgentRegistry
from gail_ai_operating_system.authority_registry import authority_registry_payload
from gail_ai_operating_system.connector_registry import ConnectorRegistry
from gail_ai_operating_system.m365_auth import graph_auth_status_from_env
from gail_ai_operating_system.read_model import (
    SHARED_READ_MODEL_SCHEMA_VERSION,
    build_trace_read_model,
    recent_evidence_refs,
    utc_z_timestamp,
)

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("/read-model")
def shared_read_model(limit: int = Query(default=25, ge=1, le=100)) -> dict[str, Any]:
    """Return the read-only operator state shared by Freedom and command center."""

    store_root = get_store_root()
    trace_events = [event.to_dict() for event in get_trace_event_store().list_recent(limit=limit)]
    evidence_refs = recent_evidence_refs(limit=limit, store_root=store_root)
    return {
        "schema_version": SHARED_READ_MODEL_SCHEMA_VERSION,
        "generated_at": utc_z_timestamp(),
        "health": {
            "status": "ok",
            "boundary": "A1 local no-network",
            "phase": "1",
            "live_execution_enabled": False,
        },
        "authority": authority_registry_payload(),
        "connectors": _connector_read_model(),
        "agents": _agent_read_model(),
        "m365": graph_auth_status_from_env(),
        "recent_events": trace_events,
        "recent_evidence": evidence_refs,
    }


@router.get("/traces/{cns_trace_id}")
def trace_lookup(cns_trace_id: str) -> dict[str, Any]:
    """Return persisted events and evidence refs for one CNS trace."""

    try:
        return build_trace_read_model(cns_trace_id, store_root=get_store_root())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))


def _connector_read_model() -> dict[str, Any]:
    registry = ConnectorRegistry()
    report = registry.validate()
    by_state = Counter(profile.current_state for profile in registry.profiles)
    by_family = Counter(profile.system_family for profile in registry.profiles)
    return {
        "registry_valid": report.valid,
        "connector_count": len(registry.profiles),
        "live_access_enabled": any(profile.live_access_enabled for profile in registry.profiles),
        "by_state": dict(sorted(by_state.items())),
        "by_system_family": dict(sorted(by_family.items())),
        "connectors": [
            {
                "connector_id": profile.connector_id,
                "display_name": profile.display_name,
                "system_family": profile.system_family,
                "current_state": profile.current_state,
                "allowed_capabilities": list(profile.allowed_capabilities),
                "live_access_enabled": profile.live_access_enabled,
            }
            for profile in registry.profiles
        ],
    }


def _agent_read_model() -> dict[str, Any]:
    registry = AgentRegistry()
    report = registry.validate()
    by_layer = Counter(profile.cns_layer for profile in registry.profiles)
    by_maturity = Counter(profile.maturity for profile in registry.profiles)
    return {
        "registry_valid": report.valid,
        "agent_count": len(registry.profiles),
        "live_access_enabled": any(profile.live_access_enabled for profile in registry.profiles),
        "by_cns_layer": dict(sorted(by_layer.items())),
        "by_maturity": dict(sorted(by_maturity.items())),
        "agents": [
            {
                "agent_id": profile.agent_id,
                "display_name": profile.display_name,
                "cns_layer": profile.cns_layer,
                "maturity": profile.maturity,
                "max_authority_level": profile.max_authority_level,
                "live_access_enabled": profile.live_access_enabled,
            }
            for profile in registry.profiles
        ],
    }
