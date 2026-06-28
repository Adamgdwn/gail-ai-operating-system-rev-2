"""Tests for GET /api/v1/connectors."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "uaos-core" / "src"))
sys.path.insert(0, str(ROOT / "apps" / "gail-os-api"))

import os
os.environ.setdefault("GAIL_OS_API_KEY", "test-key-local")

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402

client = TestClient(app)
HEADERS = {"X-Api-Key": "test-key-local"}


def test_connectors_returns_200():
    resp = client.get("/api/v1/connectors", headers=HEADERS)
    assert resp.status_code == 200


def test_connectors_has_connectors_list():
    resp = client.get("/api/v1/connectors", headers=HEADERS)
    data = resp.json()
    assert "connectors" in data
    assert data["connector_count"] > 0
    assert len(data["connectors"]) == data["connector_count"]


def test_connectors_all_no_live_access():
    resp = client.get("/api/v1/connectors", headers=HEADERS)
    for c in resp.json()["connectors"]:
        assert c["live_access_enabled"] is False


def test_connectors_all_planning_only_states():
    resp = client.get("/api/v1/connectors", headers=HEADERS)
    for c in resp.json()["connectors"]:
        assert c["current_state"] in ("planning-only", "registry-only", "inventory-only")


def test_connectors_expected_system_families():
    resp = client.get("/api/v1/connectors", headers=HEADERS)
    families = {c["system_family"] for c in resp.json()["connectors"]}
    assert "GitHub" in families
    assert "Microsoft 365" in families
    assert "Graphify" in families


def test_connectors_registry_valid():
    resp = client.get("/api/v1/connectors", headers=HEADERS)
    assert resp.json()["registry_valid"] is True


def test_connectors_missing_auth_returns_422():
    resp = client.get("/api/v1/connectors")
    assert resp.status_code == 422


def test_connectors_wrong_api_key_returns_401():
    resp = client.get("/api/v1/connectors", headers={"X-Api-Key": "wrong"})
    assert resp.status_code == 401


def test_connectors_response_has_required_fields():
    resp = client.get("/api/v1/connectors", headers=HEADERS)
    c = resp.json()["connectors"][0]
    assert "connector_id" in c
    assert "display_name" in c
    assert "system_family" in c
    assert "current_state" in c
    assert "allowed_capabilities" in c
