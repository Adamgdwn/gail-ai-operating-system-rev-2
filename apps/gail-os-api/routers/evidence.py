"""Evidence retrieval endpoint — GET /api/v1/evidence/{mission_id}."""
from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import APIRouter, Depends

from deps import verify_api_key

router = APIRouter(dependencies=[Depends(verify_api_key)])


def _evidence_store() -> Path:
    """Return the evidence store path from env, defaulting to ./local_store/evidence."""
    return Path(os.environ.get("GAIL_OS_STORE_PATH", "./local_store")) / "evidence"


@router.get("/evidence/{mission_id}")
def get_evidence(mission_id: str) -> dict:
    """Return evidence packet refs for a mission from the local JSON store."""
    store = _evidence_store()
    if not store.exists():
        return {"mission_id": mission_id, "evidence_refs": []}

    refs = []
    for f in sorted(store.glob("evidence-*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if data.get("mission_id") == mission_id:
                refs.append({
                    "evidence_id": data["evidence_id"],
                    "mission_id": data["mission_id"],
                    "action_id": data.get("action_id"),
                    "result": data.get("result"),
                    "created_at": data.get("created_at"),
                })
        except (json.JSONDecodeError, KeyError):
            continue

    return {"mission_id": mission_id, "evidence_refs": refs}
