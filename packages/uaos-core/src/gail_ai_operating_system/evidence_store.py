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

from gail_ai_operating_system.evidence_packet import EvidencePacket, validate_evidence_packet


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


def load_evidence_packet(
    evidence_id: str,
    *,
    store_path: Path | None = None,
) -> EvidencePacket:
    """Read one EvidencePacket from the local JSON store."""
    if not _safe_evidence_id(evidence_id):
        raise ValueError("Evidence ID is not safe for local storage.")
    base = store_path if store_path is not None else _default_store_path()
    file_path = base / f"{evidence_id}.json"
    packet = EvidencePacket.from_dict(json.loads(file_path.read_text(encoding="utf-8")))
    errors = validate_evidence_packet(packet)
    if errors:
        raise ValueError(f"EvidencePacket is invalid: {'; '.join(errors)}")
    return packet


def _safe_evidence_id(value: str) -> bool:
    if not value.startswith("evidence-"):
        return False
    if any(part in value for part in ("/", "\\", "..")):
        return False
    return all(character.isalnum() or character in {"-", "_"} for character in value)


__all__ = ["load_evidence_packet", "save_evidence_packet"]
