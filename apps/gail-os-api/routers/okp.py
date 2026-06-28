"""OKP ingest endpoint — POST /api/v1/okp and GET /api/v1/okp/{okp_id}."""
from __future__ import annotations

import dataclasses
import os
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
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


# ---------------------------------------------------------------------------
# Pydantic request / response models
# ---------------------------------------------------------------------------

class CreateOkpRequest(BaseModel):
    source_system: str
    source_ref: str
    record_type: str  # OkpRecordType value string, e.g. "evidence.created"
    summary: str
    authority_level: str
    autonomy_level: str
    risk_tier: int = Field(..., ge=1, le=5)
    data_classification: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    status: str = "observed"
    observed_at: Optional[str] = None  # ISO string; defaults to now
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
# Routes
# ---------------------------------------------------------------------------

@router.post("/okp", status_code=status.HTTP_201_CREATED, response_model=CreateOkpResponse)
def create_okp(req: CreateOkpRequest) -> CreateOkpResponse:
    """Ingest a new OKP, score it at L1, persist it, and return key identifiers."""
    # Resolve record_type enum
    try:
        record_type = OkpRecordType(req.record_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown record_type: {req.record_type!r}",
        )

    # Resolve observed_at
    observed_at: Optional[datetime] = None
    if req.observed_at:
        try:
            observed_at = datetime.fromisoformat(req.observed_at.replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid observed_at format: {req.observed_at!r}",
            )

    # Build the OKP
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

    # L1 gravity score
    calc = _gravity()
    score = calc.calculate(okp)

    # Attach score (frozen dataclass — use replace)
    okp = dataclasses.replace(okp, gravity_score_l1=score)

    # Persist
    store = _store()
    store.save(okp)

    return CreateOkpResponse(
        okp_id=okp.okp_id,
        gravity_score_l1=score,
        fingerprint=okp.fingerprint,
    )


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
    d = dataclasses.asdict(okp)
    # Normalise datetime and enum to strings for JSON serialisation
    for key in ("created_at", "observed_at"):
        if isinstance(d[key], datetime):
            d[key] = d[key].isoformat()
    if hasattr(d["record_type"], "value"):
        d["record_type"] = d["record_type"].value
    return d
