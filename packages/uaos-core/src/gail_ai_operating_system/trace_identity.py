"""Shared CNS trace identity helpers."""

from __future__ import annotations

from datetime import datetime, timezone
import re
from uuid import uuid4


CNS_TRACE_ID_PATTERN = r"^cns-[0-9]{8}-[a-z0-9]{12}$"
CNS_TRACE_ID_RE = re.compile(CNS_TRACE_ID_PATTERN)


def utc_z_timestamp(now: datetime | None = None) -> str:
    value = now or datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create_cns_trace_id(now: datetime | None = None) -> str:
    value = now or datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    stamp = value.astimezone(timezone.utc).strftime("%Y%m%d")
    return f"cns-{stamp}-{uuid4().hex[:12]}"


def ensure_cns_trace_id(cns_trace_id: str | None = None, *, now: datetime | None = None) -> str:
    if cns_trace_id is None or not cns_trace_id.strip():
        return create_cns_trace_id(now=now)
    errors = validate_cns_trace_id(cns_trace_id, required=True)
    if errors:
        raise ValueError("; ".join(errors))
    return cns_trace_id.strip()


def validate_cns_trace_id(cns_trace_id: str | None, *, required: bool = False) -> list[str]:
    if cns_trace_id is None or not str(cns_trace_id).strip():
        return ["cns_trace_id is required."] if required else []
    if not CNS_TRACE_ID_RE.match(str(cns_trace_id).strip()):
        return ["cns_trace_id must match cns-YYYYMMDD-12safechars."]
    return []


__all__ = [
    "CNS_TRACE_ID_PATTERN",
    "create_cns_trace_id",
    "ensure_cns_trace_id",
    "utc_z_timestamp",
    "validate_cns_trace_id",
]
