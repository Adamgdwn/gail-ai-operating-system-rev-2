"""Action policy-gate endpoint — POST /api/v1/actions."""
from __future__ import annotations

from typing import Any, Dict, Mapping

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from deps import verify_api_key
from gail_ai_operating_system.mission_spine import (
    DEFAULT_APPROVAL_LEVEL,
    REV2_OWNER,
    MissionAction,
    MissionEnvelope,
    PermissionGate,
)

router = APIRouter(dependencies=[Depends(verify_api_key)])


class ValidateActionRequest(BaseModel):
    mission: Dict[str, Any]
    action: Dict[str, Any]


def _canonicalize_bridge_mission(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Translate Freedom bridge mission metadata into the canonical GAIL owner."""
    data = dict(payload)
    if data.get("owner") in (None, "", "freedom", "gail_os"):
        data["owner"] = REV2_OWNER
    data.setdefault("approval_level", DEFAULT_APPROVAL_LEVEL)
    data.setdefault("dry_run", True)
    return data


def _canonicalize_bridge_action(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Map Freedom's low-risk generic system action into a local policy review."""
    data = dict(payload)
    risk_tier = int(data.get("risk_tier", 2))
    if data.get("action_type") == "system" and risk_tier <= 2:
        arguments = dict(data.get("arguments", {}))
        arguments.setdefault("freedom_action_type", "system")
        arguments.setdefault("freedom_action_title", str(data.get("title", "")))
        data["arguments"] = arguments
        data["action_type"] = "policy_gate_review"
    return data


@router.post("/actions")
def validate_action(req: ValidateActionRequest) -> dict:
    """Evaluate a proposed action against the local policy gate. Returns PolicyDecision."""
    try:
        mission = MissionEnvelope.from_dict(_canonicalize_bridge_mission(req.mission))
        action = MissionAction.from_dict(_canonicalize_bridge_action(req.action))
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
