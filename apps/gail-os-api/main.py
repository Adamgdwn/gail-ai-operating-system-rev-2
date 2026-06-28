"""GAIL OS FastAPI HTTP API — Phase 1 local no-network surface.

Wraps the transport-independent Python spine with an HTTP layer so Freedom
(Linux) and Graphify can call GAIL OS remotely. No live connectors, no M365
writes, no secrets. A1 local boundary only.

Auth: GAIL_OS_API_KEY environment variable, passed as X-Api-Key header.
Never hardcode the key. Never commit a populated .env file.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add spine to path before importing routers
_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT / "packages" / "uaos-core" / "src"))

from fastapi import FastAPI  # noqa: E402
from routers import actions, authority, connectors, evidence, missions  # noqa: E402

app = FastAPI(
    title="GAIL OS API",
    version="0.1.0-phase1",
    description="Phase 1 local HTTP surface for GAIL AI Operating System Rev 2. A1 local no-network boundary.",
)

app.include_router(missions.router, prefix="/api/v1")
app.include_router(actions.router, prefix="/api/v1")
app.include_router(evidence.router, prefix="/api/v1")
app.include_router(connectors.router, prefix="/api/v1")
app.include_router(authority.router, prefix="/api/v1")


@app.get("/api/v1/health")
def health() -> dict:
    """Liveness check. No auth required."""
    return {
        "status": "ok",
        "boundary": "A1 local no-network",
        "phase": "1",
    }
