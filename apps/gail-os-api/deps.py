"""Shared FastAPI dependencies for GAIL OS API."""
from __future__ import annotations

import os

from fastapi import Header, HTTPException, status


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
