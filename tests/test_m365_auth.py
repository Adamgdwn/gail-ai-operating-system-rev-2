"""Tests for GraphAuthProvider and GET /api/v1/m365/status."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "uaos-core" / "src"))
sys.path.insert(0, str(ROOT / "apps" / "gail-os-api"))

import os
os.environ.setdefault("GAIL_OS_API_KEY", "test-key-local")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from gail_ai_operating_system.m365_auth import (  # noqa: E402
    APP_ONLY_AUTH_PROFILE_STATE,
    CURRENT_M365_IDENTITY_BOUNDARY,
    GraphAuthError,
    GraphAuthProvider,
)
from main import app  # noqa: E402

client = TestClient(app)
HEADERS = {"X-Api-Key": "test-key-local"}


# --- GraphAuthProvider unit tests ---

def test_is_configured_true_when_all_env_set(monkeypatch):
    monkeypatch.setenv("AZURE_TENANT_ID", "tenant-abc")
    monkeypatch.setenv("AZURE_CLIENT_ID", "client-xyz")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "secret-123")
    provider = GraphAuthProvider.from_env()
    assert provider.is_configured() is True


def test_is_configured_false_when_missing_tenant(monkeypatch):
    monkeypatch.delenv("AZURE_TENANT_ID", raising=False)
    monkeypatch.setenv("AZURE_CLIENT_ID", "client-xyz")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "secret-123")
    provider = GraphAuthProvider.from_env()
    assert provider.is_configured() is False


def test_is_configured_false_when_missing_client_id(monkeypatch):
    monkeypatch.setenv("AZURE_TENANT_ID", "tenant-abc")
    monkeypatch.delenv("AZURE_CLIENT_ID", raising=False)
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "secret-123")
    provider = GraphAuthProvider.from_env()
    assert provider.is_configured() is False


def test_is_configured_false_when_missing_secret(monkeypatch):
    monkeypatch.setenv("AZURE_TENANT_ID", "tenant-abc")
    monkeypatch.setenv("AZURE_CLIENT_ID", "client-xyz")
    monkeypatch.delenv("AZURE_CLIENT_SECRET", raising=False)
    provider = GraphAuthProvider.from_env()
    assert provider.is_configured() is False


def test_get_token_calls_msal_with_correct_params():
    provider = GraphAuthProvider(
        tenant_id="tenant-abc",
        client_id="client-xyz",
        client_secret="secret-123",
    )
    mock_app = MagicMock()
    mock_app.acquire_token_for_client.return_value = {"access_token": "tok-fake-001"}

    with patch("gail_ai_operating_system.m365_auth.msal.ConfidentialClientApplication", return_value=mock_app) as mock_cls:
        token = provider.get_token()

    assert token == "tok-fake-001"
    mock_cls.assert_called_once_with(
        client_id="client-xyz",
        client_credential="secret-123",
        authority="https://login.microsoftonline.com/tenant-abc",
    )
    mock_app.acquire_token_for_client.assert_called_once_with(
        scopes=["https://graph.microsoft.com/.default"]
    )


def test_get_token_raises_when_not_configured():
    provider = GraphAuthProvider(tenant_id="", client_id="", client_secret="")
    with pytest.raises(GraphAuthError, match="not configured"):
        provider.get_token()


def test_get_token_raises_on_msal_error():
    provider = GraphAuthProvider(
        tenant_id="tenant-abc",
        client_id="client-xyz",
        client_secret="secret-123",
    )
    mock_app = MagicMock()
    mock_app.acquire_token_for_client.return_value = {
        "error": "invalid_client",
        "error_description": "AADSTS70011: The provided request must include a 'scope' input parameter.",
    }
    with patch("gail_ai_operating_system.m365_auth.msal.ConfidentialClientApplication", return_value=mock_app):
        with pytest.raises(GraphAuthError, match="MSAL token acquisition failed"):
            provider.get_token()


# --- API endpoint tests ---

def test_m365_status_returns_200_when_configured(monkeypatch):
    monkeypatch.setenv("AZURE_TENANT_ID", "tenant-abc")
    monkeypatch.setenv("AZURE_CLIENT_ID", "client-xyz")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "secret-123")
    resp = client.get("/api/v1/m365/status", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["configured"] is True
    assert data["tenant_id_present"] is True
    assert data["client_id_present"] is True
    assert data["client_secret_present"] is True


def test_m365_status_not_configured_when_no_env(monkeypatch):
    monkeypatch.delenv("AZURE_TENANT_ID", raising=False)
    monkeypatch.delenv("AZURE_CLIENT_ID", raising=False)
    monkeypatch.delenv("AZURE_CLIENT_SECRET", raising=False)
    resp = client.get("/api/v1/m365/status", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["configured"] is False
    assert data["tenant_id_present"] is False
    assert data["client_id_present"] is False
    assert data["client_secret_present"] is False


def test_m365_status_returns_scope_and_boundary(monkeypatch):
    monkeypatch.delenv("AZURE_TENANT_ID", raising=False)
    resp = client.get("/api/v1/m365/status", headers=HEADERS)
    data = resp.json()
    assert data["scope"] == "https://graph.microsoft.com/.default"
    assert "A1" in data["boundary"]
    assert data["identity_boundary"] == CURRENT_M365_IDENTITY_BOUNDARY
    assert data["app_only_profile_state"] == APP_ONLY_AUTH_PROFILE_STATE
    assert "delegated-only" in data["note"]
    assert "No client secret" in data["note"]


def test_m365_status_missing_auth_returns_422():
    resp = client.get("/api/v1/m365/status")
    assert resp.status_code == 422


def test_m365_status_wrong_key_returns_401():
    resp = client.get("/api/v1/m365/status", headers={"X-Api-Key": "bad-key"})
    assert resp.status_code == 401
