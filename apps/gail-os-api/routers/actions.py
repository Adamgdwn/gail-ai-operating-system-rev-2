"""Action policy-gate endpoint — POST /api/v1/actions."""
from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from deps import verify_api_key
from gail_ai_operating_system.mission_spine import MissionAction, MissionEnvelope, PermissionGate

router = APIRouter(dependencies=[Depends(verify_api_key)])


class ValidateActionRequest(BaseModel):
    mission: Dict[str, Any]
    action: Dict[str, Any]


@router.post("/actions")
def validate_action(req: ValidateActionRequest) -> dict:
    """Evaluate a proposed action against the local policy gate. Returns PolicyDecision."""
    try:
        mission = MissionEnvelope.from_dict(req.mission)
        action = MissionAction.from_dict(req.action)
    except (KeyError, ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid mission or action payload: {exc}",
        )
    decision = PermissionGate().evaluate(mission, action)
    return {
        "action_id": decision.action_id,
        "allowed": decision.allowed,
        "mode": decision.mode,
        "reason": decision.reason,
        "stop_reason": decision.stop_reason,
    }
