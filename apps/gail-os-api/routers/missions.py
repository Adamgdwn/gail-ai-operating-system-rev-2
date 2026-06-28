"""Mission creation endpoint — POST /api/v1/missions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from deps import verify_api_key
from gail_ai_operating_system.mission_spine import MissionValidationError, create_mission

router = APIRouter(dependencies=[Depends(verify_api_key)])


class CreateMissionRequest(BaseModel):
    command: str
    domain: str = "build"
    request_id: str = "REQ-LOCAL"
    requested_tools: List[str] = []
    data_classification: str = "internal"


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
        mission = create_mission(
            req.command,
            domain=req.domain,
            request_id=req.request_id,
            requested_tools=req.requested_tools,
            data_classification=req.data_classification,
        )
    except (ValueError, MissionValidationError) as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    payload = mission.to_dict()
    payload["created_at"] = _utc_z_timestamp(payload["created_at"])
    return payload
