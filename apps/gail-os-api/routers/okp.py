"""OKP endpoints — POST, list, get, and proof-chain for /api/v1/okp."""
from __future__ import annotations

import dataclasses
import os
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from deps import verify_api_key
from gail_ai_operating_system.operating_knowledge import (
    OkpRecordType,
    OperatingKnowledgePacket,
    create_operating_knowledge_packet,
)
from gail_ai_operating_system.operating_knowledge_store import OkpStore
from gail_ai_operating_system.signal_gravity import SignalGravityL1Calculator

router = APIRouter(dependencies=[Depends(verify_api_key)])


def _store() -> OkpStore:
    store_path = os.environ.get("GAIL_OS_STORE_PATH", "./local_store")
    return OkpStore(store_path=store_path)


def _gravity() -> SignalGravityL1Calculator:
    store_path = os.environ.get("GAIL_OS_STORE_PATH", "./local_store")
    return SignalGravityL1Calculator(store_path=store_path)


def _okp_to_dict(okp: OperatingKnowledgePacket) -> dict:
    d = dataclasses.asdict(okp)
    for key in ("created_at", "observed_at"):
        if isinstance(d[key], datetime):
            d[key] = d[key].isoformat()
    if hasattr(d["record_type"], "value"):
        d["record_type"] = d["record_type"].value
    return d


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class CreateOkpRequest(BaseModel):
    source_system: str
    source_ref: str
    record_type: str
    summary: str
    authority_level: str
    autonomy_level: str
    risk_tier: int = Field(..., ge=1, le=5)
    data_classification: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    status: str = "observed"
    observed_at: Optional[str] = None
    related_mission_id: Optional[str] = None
    related_action_id: Optional[str] = None
    related_evidence_id: Optional[str] = None
    related_connector_id: Optional[str] = None
    related_agent_id: Optional[str] = None


class CreateOkpResponse(BaseModel):
    okp_id: str
    gravity_score_l1: float
    fingerprint: str


# ---------------------------------------------------------------------------
# Routes — list before by-id; proof-chain before plain by-id to avoid shadowing
# ---------------------------------------------------------------------------

@router.post("/okp", status_code=status.HTTP_201_CREATED, response_model=CreateOkpResponse)
def create_okp(req: CreateOkpRequest) -> CreateOkpResponse:
    """Ingest a new OKP, score it at L1, persist it, and return key identifiers."""
    try:
        record_type = OkpRecordType(req.record_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown record_type: {req.record_type!r}",
        )

    observed_at: Optional[datetime] = None
    if req.observed_at:
        try:
            observed_at = datetime.fromisoformat(req.observed_at.replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid observed_at format: {req.observed_at!r}",
            )

    try:
        okp = create_operating_knowledge_packet(
            source_system=req.source_system,
            source_ref=req.source_ref,
            record_type=record_type,
            summary=req.summary,
            authority_level=req.authority_level,
            autonomy_level=req.autonomy_level,
            risk_tier=req.risk_tier,
            data_classification=req.data_classification,
            confidence=req.confidence,
            status=req.status,
            observed_at=observed_at,
            related_mission_id=req.related_mission_id,
            related_action_id=req.related_action_id,
            related_evidence_id=req.related_evidence_id,
            related_connector_id=req.related_connector_id,
            related_agent_id=req.related_agent_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )

    calc = _gravity()
    score = calc.calculate(okp)
    okp = dataclasses.replace(okp, gravity_score_l1=score)

    store = _store()
    store.save(okp)

    return CreateOkpResponse(
        okp_id=okp.okp_id,
        gravity_score_l1=score,
        fingerprint=okp.fingerprint,
    )


@router.get("/okp")
def list_okp_by_record_type(
    record_type: str = Query(..., description="OkpRecordType value string"),
) -> list[dict]:
    """List all OKPs with the given record_type. Returns [] if none found."""
    store = _store()
    okps = store.list_by_record_type(record_type)
    return [_okp_to_dict(o) for o in okps]


@router.get("/okp/{okp_id}/proof-chain")
def get_okp_proof_chain(okp_id: str) -> dict:
    """Return Synaptic Proof Chain stub (GAIL OS L1 layer) for this OKP.

    Full chain: this endpoint (L1) + GET /api/cns/okp/{id}/proof-chain (Graphify L2)
    + generateOperatingKnowledgeBrief() in Freedom (brief layer). CP-5 closed.
    """
    store = _store()
    okp = store.get(okp_id)
    if okp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"OKP not found: {okp_id!r}",
        )
    record_type_str = (
        okp.record_type.value
        if hasattr(okp.record_type, "value")
        else str(okp.record_type)
    )
    created_at_str = (
        okp.created_at.isoformat()
        if hasattr(okp.created_at, "isoformat")
        else str(okp.created_at)
    )
    observed_at_str = (
        okp.observed_at.isoformat()
        if hasattr(okp.observed_at, "isoformat")
        else str(okp.observed_at)
    )
    return {
        "okp_id": okp.okp_id,
        "source_system": okp.source_system,
        "source_ref": okp.source_ref,
        "record_type": record_type_str,
        "fingerprint": okp.fingerprint,
        "authority_level": okp.authority_level,
        "autonomy_level": okp.autonomy_level,
        "risk_tier": okp.risk_tier,
        "data_classification": okp.data_classification,
        "status": okp.status,
        "confidence": okp.confidence,
        "gravity_score_l1": okp.gravity_score_l1,
        "related_evidence_id": okp.related_evidence_id,
        "related_mission_id": okp.related_mission_id,
        "related_action_id": okp.related_action_id,
        "created_at": created_at_str,
        "observed_at": observed_at_str,
        "proof_chain_version": "stub-l1",
        "note": (
            "Graphify L2 enrichment: GET /api/cns/okp/{okp_id}/proof-chain. "
            "Freedom brief: generateOperatingKnowledgeBrief(). CP-5 closed."
        ),
    }


@router.get("/okp/{okp_id}")
def get_okp(okp_id: str) -> dict:
    """Retrieve a persisted OKP by id. Returns 404 if not found."""
    store = _store()
    okp = store.get(okp_id)
    if okp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"OKP not found: {okp_id!r}",
        )
    return _okp_to_dict(okp)
