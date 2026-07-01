"""Future app-only Microsoft Graph authentication provider for GAIL OS.

Current approved Microsoft 365 tenant state is delegated-only: the local CLI
app has delegated permissions and admin consent, but no client secret,
certificate, or app-only grant exists. This provider is a dormant
client-credentials path for isolated tests and a later owner-gated app-only
promotion.

Future app-only env vars, if owner-approved later:
  AZURE_TENANT_ID      - Entra ID tenant identifier
  AZURE_CLIENT_ID      - Future app-only app registration client ID
  AZURE_CLIENT_SECRET  - Future app-only client secret

A1 local no-network boundary: get_token() makes a live MSAL call. Do not call
it inside tests without mocking. Use is_configured() to check readiness first.
"""
from __future__ import annotations

import os
from typing import Optional

import msal

GRAPH_SCOPE = "https://graph.microsoft.com/.default"
_AUTHORITY_BASE = "https://login.microsoftonline.com/"
CURRENT_M365_IDENTITY_BOUNDARY = (
    "delegated-permissions-approved; app-only-secret-certificate-not-created"
)
APP_ONLY_AUTH_PROFILE_STATE = "future-only-unprovisioned"


class GraphAuthError(RuntimeError):
    """Raised when Graph auth fails — missing config, MSAL error, or network fault."""


class GraphAuthProvider:
    """Future app-only client-credentials Graph auth provider backed by MSAL.

    This does not represent the current approved Microsoft 365 identity
    boundary. It is available only for synthetic tests and a later explicit
    app-only promotion gate.
    """

    def __init__(self, tenant_id: str, client_id: str, client_secret: str) -> None:
        self._tenant_id = tenant_id
        self._client_id = client_id
        self._client_secret = client_secret

    @classmethod
    def from_env(cls) -> "GraphAuthProvider":
        """Construct from AZURE_* environment variables."""
        return cls(
            tenant_id=os.environ.get("AZURE_TENANT_ID", ""),
            client_id=os.environ.get("AZURE_CLIENT_ID", ""),
            client_secret=os.environ.get("AZURE_CLIENT_SECRET", ""),
        )

    def is_configured(self) -> bool:
        """Return True if all three credentials are non-empty."""
        return bool(self._tenant_id and self._client_id and self._client_secret)

    def get_token(self) -> str:
        """Acquire a Graph access token via MSAL client credentials flow.

        Raises GraphAuthError if credentials are missing or MSAL returns an
        error. Never logs or returns the raw secret.
        """
        if not self.is_configured():
            raise GraphAuthError(
                "Future app-only Graph auth is not configured. "
                "Current approved Microsoft 365 state is delegated-only. "
                "Set AZURE_TENANT_ID, AZURE_CLIENT_ID, and AZURE_CLIENT_SECRET "
                "only after an owner-approved app-only credential boundary exists."
            )
        authority = f"{_AUTHORITY_BASE}{self._tenant_id}"
        app = msal.ConfidentialClientApplication(
            client_id=self._client_id,
            client_credential=self._client_secret,
            authority=authority,
        )
        result = app.acquire_token_for_client(scopes=[GRAPH_SCOPE])
        if "access_token" not in result:
            error = result.get("error", "unknown")
            description = result.get("error_description", "no description")
            raise GraphAuthError(
                f"MSAL token acquisition failed: {error} — {description}"
            )
        token: str = result["access_token"]
        return token
