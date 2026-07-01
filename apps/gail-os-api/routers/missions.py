"""Mission creation endpoint — POST /api/v1/missions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from deps import get_store_root, record_api_trace_event, verify_api_key
from gail_ai_operating_system.mission_spine import LocalMissionStore, MissionValidationError, create_mission
from gail_ai_operating_system.trace_identity import CNS_TRACE_ID_PATTERN, ensure_cns_trace_id

router = APIRouter(dependencies=[Depends(verify_api_key)])


class CreateMissionRequest(BaseModel):
    command: str
    domain: str = "build"
    request_id: str = "REQ-LOCAL"
    requested_tools: List[str] = []
    data_classification: str = "internal"
    cns_trace_id: Optional[str] = Field(default=None, pattern=CNS_TRACE_ID_PATTERN)


def _utc_z_timestamp(value: str) -> str:
    """Return a UTC `Z` timestamp for TypeScript runtime schema compatibility."""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    return parsed.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@router.post("/missions")
def create_mission_endpoint(req: CreateMissionRequest) -> dict:
    """Create and validate a mission envelope. Returns the mission_id and full envelope."""
    try:
        cns_trace_id = ensure_cns_trace_id(req.cns_trace_id)
        mission = create_mission(
            req.command,
            domain=req.domain,
            request_id=req.request_id,
            requested_tools=req.requested_tools,
            data_classification=req.data_classification,
            cns_trace_id=cns_trace_id,
        )
        LocalMissionStore(get_store_root() / "missions").save(mission)
        record_api_trace_event(
            cns_trace_id=cns_trace_id,
            event_type="mission.created",
            source_ref=f"api/v1/missions/{mission.mission_id}",
            summary="Mission record created and persisted.",
            mission_id=mission.mission_id,
            status=mission.status,
            idempotency_key=f"mission:{req.request_id}",
            metadata={
                "domain": mission.domain,
                "data_classification": mission.data_classification,
                "requested_tools": list(mission.requested_tools),
            },
        )
    except (ValueError, MissionValidationError) as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    payload = mission.to_dict()
    payload["created_at"] = _utc_z_timestamp(payload["created_at"])
    return payload
