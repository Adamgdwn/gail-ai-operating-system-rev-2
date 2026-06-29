"""Authority registry and override request endpoints."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from deps import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])


AUTHORITY_LEVELS = [
    {
        "level": "R0",
        "name": "Observe",
        "meaning": "Read-only, no external effect",
        "agent_boundary": "Allowed for local dry-run observation.",
    },
    {
        "level": "R1",
        "name": "Propose",
        "meaning": "Draft, recommend, prepare - no external effect",
        "agent_boundary": "Allowed for proposal work only.",
    },
    {
        "level": "R2",
        "name": "Internal approved action",
        "meaning": "Reversible internal write with named approval",
        "agent_boundary": "Requires GAIL OS policy validation and evidence.",
    },
    {
        "level": "R3",
        "name": "Restricted action",
        "meaning": "External send, production release, irreversible change",
        "agent_boundary": "Requires explicit approval before execution.",
    },
    {
        "level": "R4",
        "name": "Delegated autonomous restricted action",
        "meaning": "Inside a valid pre-approved authority charter",
        "agent_boundary": "Owner-gated; requires a signed AuthorityEnvelope.",
    },
    {
        "level": "R5",
        "name": "Blocked / human-only",
        "meaning": "Agent may analyze only; human decides",
        "agent_boundary": "Human-only. No agent execution.",
    },
]


@router.get("/authority")
def authority_registry() -> dict:
    """Return the read-only authority ladder used by local integration probes."""
    return {
        "registry_valid": True,
        "source": "docs/governance/authority-ladders.md",
        "boundary": "A1 local no-network",
        "autonomy_level": "A1",
        "live_execution_enabled": False,
        "r4_requires_authority_envelope": True,
        "r5_human_only": True,
        "authority_levels": AUTHORITY_LEVELS,
    }


class OverrideRequest(BaseModel):
    action_id: str
    mission_id: str
    summary: str
    action_kind: str = "general"
    risk_tier: int = 2
    blocking_reason: str
    requested_by: str = "freedom"
    request_id: Optional[str] = None


@router.post("/authority/override", status_code=201)
def request_authority_override(req: OverrideRequest) -> dict:
    """Record a Freedom authority override request. Returns a pending override record.

    Freedom calls this when validateAction returns a blocked decision and the
    executive layer needs to escalate to a human authority for approval.
    No live connectors, no M365 writes. Records the request and returns pending.
    """
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    override_id = f"override-{req.mission_id}-{req.action_id}-{uuid.uuid4().hex[:8]}"

    return {
        "override_request_id": override_id,
        "status": "pending",
        "action_id": req.action_id,
        "mission_id": req.mission_id,
        "summary": req.summary,
        "action_kind": req.action_kind,
        "risk_tier": req.risk_tier,
        "blocking_reason": req.blocking_reason,
        "requested_by": req.requested_by,
        "recorded_at": now,
    }
