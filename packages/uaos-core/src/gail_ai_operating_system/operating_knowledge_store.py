"""OKP Store — filesystem persistence for OperatingKnowledgePackets (Phase 5)."""
from __future__ import annotations

import dataclasses
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from gail_ai_operating_system.operating_knowledge import (
    OkpRecordType,
    OperatingKnowledgePacket,
)


def _okp_to_dict(okp: OperatingKnowledgePacket) -> dict:
    """Serialize OKP to a JSON-safe dict."""
    d = dataclasses.asdict(okp)
    # Convert datetime fields to ISO strings
    for key in ("created_at", "observed_at"):
        if isinstance(d[key], datetime):
            d[key] = d[key].isoformat()
    # Convert OkpRecordType enum to string value
    if isinstance(d["record_type"], str) and d["record_type"].startswith("OkpRecordType."):
        # already a name; convert via value
        d["record_type"] = OkpRecordType[d["record_type"].split(".", 1)[1]].value
    elif hasattr(d["record_type"], "value"):
        d["record_type"] = d["record_type"].value
    return d


def _okp_from_dict(d: dict) -> OperatingKnowledgePacket:
    """Deserialize an OKP from a JSON-loaded dict."""
    d = dict(d)
    # Convert datetime strings back to datetime objects
    for key in ("created_at", "observed_at"):
        if isinstance(d[key], str):
            d[key] = datetime.fromisoformat(d[key])
    # Convert record_type string back to enum
    if isinstance(d["record_type"], str):
        d["record_type"] = OkpRecordType(d["record_type"])
    return OperatingKnowledgePacket(**d)


class OkpStore:
    """Filesystem-backed store for OperatingKnowledgePackets.

    Each OKP is persisted as a JSON file at
    ``{store_path}/okp/{okp_id}.json``.

    Duplicate fingerprint handling: if an OKP with the same fingerprint
    already exists in the store, the old OKP is updated to status
    ``"superseded"`` before the new one is written.
    """

    def __init__(self, store_path: str = "local_store") -> None:
        self.store_path = store_path
        self._okp_dir = Path(store_path) / "okp"

    def _ensure_dir(self) -> None:
        self._okp_dir.mkdir(parents=True, exist_ok=True)

    def save(self, okp: OperatingKnowledgePacket) -> str:
        """Persist *okp* and return its okp_id.

        If another OKP with the same fingerprint exists it is first marked as
        ``"superseded"`` in-place.
        """
        self._ensure_dir()
        # Fingerprint deduplication
        existing = self._find_by_fingerprint(okp.fingerprint)
        if existing is not None and existing.okp_id != okp.okp_id:
            superseded = dataclasses.replace(existing, status="superseded")
            superseded_path = self._okp_dir / f"{existing.okp_id}.json"
            superseded_path.write_text(
                json.dumps(_okp_to_dict(superseded), indent=2),
                encoding="utf-8",
            )
        # Write new OKP
        okp_path = self._okp_dir / f"{okp.okp_id}.json"
        okp_path.write_text(json.dumps(_okp_to_dict(okp), indent=2), encoding="utf-8")
        return okp.okp_id

    def get(self, okp_id: str) -> Optional[OperatingKnowledgePacket]:
        """Read OKP by id; return ``None`` if not found."""
        okp_path = self._okp_dir / f"{okp_id}.json"
        if not okp_path.exists():
            return None
        try:
            d = json.loads(okp_path.read_text(encoding="utf-8"))
            return _okp_from_dict(d)
        except (json.JSONDecodeError, (TypeError, KeyError, ValueError)):
            return None

    def list_by_record_type(self, record_type: str) -> list[OperatingKnowledgePacket]:
        """Return all OKPs whose record_type matches *record_type* (string value)."""
        if not self._okp_dir.exists():
            return []
        results = []
        for f in sorted(self._okp_dir.glob("*.json")):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
                if d.get("record_type") == record_type:
                    results.append(_okp_from_dict(d))
            except (json.JSONDecodeError, TypeError, KeyError, ValueError):
                continue
        return results

    def _find_by_fingerprint(self, fingerprint: str) -> Optional[OperatingKnowledgePacket]:
        """Scan store for an OKP with the given fingerprint; return ``None`` if absent."""
        if not self._okp_dir.exists():
            return None
        for f in self._okp_dir.glob("*.json"):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
                if d.get("fingerprint") == fingerprint:
                    return _okp_from_dict(d)
            except (json.JSONDecodeError, TypeError, KeyError, ValueError):
                continue
        return None


__all__ = ["OkpStore"]
