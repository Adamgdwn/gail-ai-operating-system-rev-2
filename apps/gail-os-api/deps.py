"""Shared FastAPI dependencies for GAIL OS API."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Mapping

from fastapi import Header, HTTPException, status

from gail_ai_operating_system.read_model import (
    LocalTraceEventStore,
    TraceEvent,
    create_trace_event,
    default_trace_event_store_path,
)


def verify_api_key(x_api_key: str = Header(...)) -> None:
    """Validate the X-Api-Key header against GAIL_OS_API_KEY env var.

    The key is read at request time so it can be rotated without restart.
    Never hardcode. Never commit.
    """
    expected = os.environ.get("GAIL_OS_API_KEY", "")
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GAIL_OS_API_KEY is not configured on this server.",
        )
    if x_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )


def get_store_root() -> Path:
    return Path(os.environ.get("GAIL_OS_STORE_PATH", "./local_store"))


def get_trace_event_store() -> LocalTraceEventStore:
    return LocalTraceEventStore(default_trace_event_store_path(get_store_root()))


def record_api_trace_event(
    *,
    cns_trace_id: str,
    event_type: str,
    source_ref: str,
    summary: str,
    mission_id: str | None = None,
    action_id: str | None = None,
    evidence_id: str | None = None,
    authority_ref: str | None = None,
    status: str | None = None,
    risk_tier: int | None = None,
    idempotency_key: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> TraceEvent:
    store = get_trace_event_store()
    duplicate = store.find_first_by_idempotency_key(idempotency_key)
    event = create_trace_event(
        cns_trace_id=cns_trace_id,
        event_type=event_type,
        source_system="gail-os-api",
        source_ref=source_ref,
        summary=summary,
        mission_id=mission_id,
        action_id=action_id,
        evidence_id=evidence_id,
        authority_ref=authority_ref,
        status=status,
        risk_tier=risk_tier,
        idempotency_key=idempotency_key,
        duplicate_of_event_id=duplicate.event_id if duplicate else None,
        metadata=metadata or {},
    )
    store.save(event)
    return event
