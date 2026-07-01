"""Action policy-gate endpoint — POST /api/v1/actions."""
from __future__ import annotations

from typing import Any, Dict, Literal, Mapping, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, Field

from deps import get_store_root, get_trace_event_store, record_api_trace_event, verify_api_key
from gail_ai_operating_system.action import LocalActionStore
from gail_ai_operating_system.approval_actions import ApprovalDecisionType, ApprovalStore
from gail_ai_operating_system.local_action_loop import (
    LocalActionConflictError,
    LocalActionLoopError,
    LocalActionNotFoundError,
    LocalActionPolicyBlockedError,
    create_local_action_request,
    record_local_action_decision,
)
from gail_ai_operating_system.mission_spine import (
    DEFAULT_APPROVAL_LEVEL,
    LocalMissionStore,
    REV2_OWNER,
    MissionAction,
    MissionEnvelope,
    PermissionGate,
)
from gail_ai_operating_system.read_model import utc_z_timestamp
from gail_ai_operating_system.trace_identity import CNS_TRACE_ID_PATTERN, ensure_cns_trace_id

router = APIRouter(dependencies=[Depends(verify_api_key)])


class ValidateActionRequest(BaseModel):
    mission: Dict[str, Any]
    action: Dict[str, Any]
    cns_trace_id: Optional[str] = Field(default=None, pattern=CNS_TRACE_ID_PATTERN)


class CreateLocalActionRequest(BaseModel):
    mission_id: str = Field(pattern=r"^mission-[A-Za-z0-9_-]+$")
    action_type: str
    title: str
    actor: str = "freedom"
    authority_level: Literal["R0", "R1"] = "R1"
    risk_tier: int = Field(default=1, ge=0, le=5)
    arguments: Dict[str, Any] = Field(default_factory=dict)
    envelope_id: Optional[str] = Field(default=None, pattern=r"^env-[A-Za-z0-9_-]+$")
    idempotency_key: str = Field(min_length=1, max_length=160)
    cns_trace_id: Optional[str] = Field(default=None, pattern=CNS_TRACE_ID_PATTERN)


class DecideLocalActionRequest(BaseModel):
    decision_type: ApprovalDecisionType
    decided_by: str = "Adam Goodwin"
    rationale: str
    authority_basis: str = "R1 local governed write approved by operator"
    expected_status: str = "approval_requested"
    idempotency_key: str = Field(min_length=1, max_length=160)
    decided_at: Optional[str] = None
    hold_until: Optional[str] = None
    info_requested: Optional[str] = None
    info_from: Optional[str] = None
    envelope_id: Optional[str] = Field(default=None, pattern=r"^env-[A-Za-z0-9_-]+$")
    cns_trace_id: Optional[str] = Field(default=None, pattern=CNS_TRACE_ID_PATTERN)


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
        cns_trace_id = ensure_cns_trace_id(req.cns_trace_id or mission.cns_trace_id)
    except (KeyError, ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid mission or action payload: {exc}",
        )
    decision = PermissionGate().evaluate(mission, action)
    record_api_trace_event(
        cns_trace_id=cns_trace_id,
        event_type="action.validated",
        source_ref=f"api/v1/actions/{decision.action_id}",
        summary="Action proposal evaluated by the GAIL OS policy gate.",
        mission_id=mission.mission_id,
        action_id=decision.action_id,
        status="allowed" if decision.allowed else "blocked",
        risk_tier=action.risk_tier,
        idempotency_key=f"action-validation:{mission.mission_id}:{decision.action_id}",
        metadata={
            "allowed": decision.allowed,
            "mode": decision.mode,
            "action_type": action.action_type,
            "stop_reason_present": decision.stop_reason is not None,
        },
    )
    return {
        "action_id": decision.action_id,
        "cns_trace_id": cns_trace_id,
        "allowed": decision.allowed,
        "mode": decision.mode,
        "reason": decision.reason,
        "stop_reason": decision.stop_reason,
    }


@router.post("/actions/local", status_code=status.HTTP_201_CREATED)
def create_local_action(req: CreateLocalActionRequest, response: Response) -> dict[str, Any]:
    """Persist a governed local action request in approval_requested state."""

    store_root = get_store_root()
    try:
        mission = LocalMissionStore(store_root / "missions").load(req.mission_id)
        result = create_local_action_request(
            mission=mission,
            action_type=req.action_type,
            title=req.title,
            actor=req.actor,
            authority_level=req.authority_level,
            risk_tier=req.risk_tier,
            arguments=req.arguments,
            envelope_id=req.envelope_id,
            idempotency_key=req.idempotency_key,
            cns_trace_id=req.cns_trace_id,
            action_store=LocalActionStore(store_root / "actions"),
            trace_event_store=get_trace_event_store(),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission record was not found.") from exc
    except LocalActionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except LocalActionPolicyBlockedError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "reason": "Local action request is outside the current governed boundary.",
                "policy_decision": {
                    "action_id": exc.decision.action_id,
                    "allowed": exc.decision.allowed,
                    "mode": exc.decision.mode,
                    "reason": exc.decision.reason,
                    "stop_reason": exc.decision.stop_reason,
                },
            },
        ) from exc
    except LocalActionConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except (KeyError, ValueError, TypeError, LocalActionLoopError) as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    if result["duplicate_detected"]:
        response.status_code = status.HTTP_200_OK
    return result


@router.post("/actions/local/{action_id}/decisions", status_code=status.HTTP_201_CREATED)
def decide_local_action(
    action_id: str,
    req: DecideLocalActionRequest,
    response: Response,
) -> dict[str, Any]:
    """Record a governed local approval decision and evidence for one action."""

    store_root = get_store_root()
    try:
        result = record_local_action_decision(
            action_id=action_id,
            decision_type=req.decision_type.value,
            decided_by=req.decided_by,
            rationale=req.rationale,
            authority_basis=req.authority_basis,
            expected_status=req.expected_status,
            idempotency_key=req.idempotency_key,
            decided_at=req.decided_at or utc_z_timestamp(),
            hold_until=req.hold_until,
            info_requested=req.info_requested,
            info_from=req.info_from,
            envelope_id=req.envelope_id,
            cns_trace_id=req.cns_trace_id,
            action_store=LocalActionStore(store_root / "actions"),
            approval_store=ApprovalStore(store_root / "approvals"),
            evidence_store_path=store_root / "evidence",
            trace_event_store=get_trace_event_store(),
        )
    except LocalActionNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except LocalActionConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    except (ValueError, TypeError, LocalActionLoopError) as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    if result["duplicate_detected"]:
        response.status_code = status.HTTP_200_OK
    return result
