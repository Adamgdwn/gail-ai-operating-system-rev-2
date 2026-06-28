"""Local evidence store — write EvidencePacket JSON files to disk.

Files are stored as {store_path}/evidence-{evidence_id}.json and are
readable by the evidence retrieval router (GET /api/v1/evidence/{mission_id}).
The store path is controlled by the GAIL_OS_STORE_PATH environment variable
(default: ./local_store).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from gail_ai_operating_system.evidence_packet import EvidencePacket


def _default_store_path() -> Path:
    return Path(os.environ.get("GAIL_OS_STORE_PATH", "./local_store")) / "evidence"


def save_evidence_packet(
    packet: EvidencePacket,
    *,
    store_path: Path | None = None,
) -> Path:
    """Write an EvidencePacket to the local JSON store.

    Returns the path of the written file. Creates the store directory if
    it does not exist.
    """
    base = store_path if store_path is not None else _default_store_path()
    base.mkdir(parents=True, exist_ok=True)
    file_path = base / f"{packet.evidence_id}.json"
    file_path.write_text(
        json.dumps(packet.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return file_path


__all__ = ["save_evidence_packet"]
