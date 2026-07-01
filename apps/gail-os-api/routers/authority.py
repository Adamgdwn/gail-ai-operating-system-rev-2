"""Authority registry and override request endpoints."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from deps import record_api_trace_event, verify_api_key
from gail_ai_operating_system.authority_registry import authority_registry_payload
from gail_ai_operating_system.trace_identity import CNS_TRACE_ID_PATTERN, ensure_cns_trace_id

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("/authority")
def authority_registry() -> dict:
    """Return the read-only authority ladder used by local integration probes."""
    return authority_registry_payload()


class OverrideRequest(BaseModel):
    action_id: str
    mission_id: str
    summary: str
    action_kind: str = "general"
    risk_tier: int = 2
    blocking_reason: str
    requested_by: str = "freedom"
    request_id: Optional[str] = None
    cns_trace_id: Optional[str] = Field(default=None, pattern=CNS_TRACE_ID_PATTERN)


@router.post("/authority/override", status_code=201)
def request_authority_override(req: OverrideRequest) -> dict:
    """Record a Freedom authority override request. Returns a pending override record.

    Freedom calls this when validateAction returns a blocked decision and the
    executive layer needs to escalate to a human authority for approval.
    No live connectors, no M365 writes. Records the request and returns pending.
    """
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    override_id = f"override-{req.mission_id}-{req.action_id}-{uuid.uuid4().hex[:8]}"
    cns_trace_id = ensure_cns_trace_id(req.cns_trace_id)
    record_api_trace_event(
        cns_trace_id=cns_trace_id,
        event_type="authority.override_requested",
        source_ref=f"api/v1/authority/override/{override_id}",
        summary="Authority override request recorded as pending.",
        mission_id=req.mission_id,
        action_id=req.action_id,
        authority_ref=override_id,
        status="pending",
        risk_tier=req.risk_tier,
        idempotency_key=(
            f"authority-override:{req.request_id}"
            if req.request_id
            else f"authority-override:{req.mission_id}:{req.action_id}"
        ),
        metadata={
            "action_kind": req.action_kind,
            "requested_by": req.requested_by,
            "request_id": req.request_id,
        },
    )

    return {
        "override_request_id": override_id,
        "cns_trace_id": cns_trace_id,
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
