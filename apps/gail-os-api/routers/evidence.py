"""Evidence retrieval endpoint — GET /api/v1/evidence/{mission_id}."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from deps import get_store_root, verify_api_key
from gail_ai_operating_system.read_model import evidence_refs_for_mission

router = APIRouter(dependencies=[Depends(verify_api_key)])


@router.get("/evidence/{mission_id}")
def get_evidence(mission_id: str) -> dict:
    """Return evidence packet refs for a mission from the local JSON store."""
    return {"mission_id": mission_id, "evidence_refs": evidence_refs_for_mission(mission_id, store_root=get_store_root())}
