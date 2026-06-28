"""Tests for GET /api/v1/agents."""
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


def test_agents_returns_200():
    resp = client.get("/api/v1/agents", headers=HEADERS)
    assert resp.status_code == 200


def test_agents_has_agents_list():
    resp = client.get("/api/v1/agents", headers=HEADERS)
    data = resp.json()
    assert "agents" in data
    assert data["agent_count"] > 0
    assert len(data["agents"]) == data["agent_count"]


def test_agents_all_no_live_access():
    resp = client.get("/api/v1/agents", headers=HEADERS)
    for a in resp.json()["agents"]:
        assert a["live_access_enabled"] is False


def test_agents_known_cns_layers():
    resp = client.get("/api/v1/agents", headers=HEADERS)
    layers = {a["cns_layer"] for a in resp.json()["agents"]}
    assert "freedom" in layers
    assert "gail_os" in layers
    assert "graphify" in layers


def test_agents_known_maturities():
    resp = client.get("/api/v1/agents", headers=HEADERS)
    for a in resp.json()["agents"]:
        assert a["maturity"] in ("prototype", "active", "production")


def test_agents_registry_valid():
    resp = client.get("/api/v1/agents", headers=HEADERS)
    assert resp.json()["registry_valid"] is True


def test_agents_expected_agents_present():
    resp = client.get("/api/v1/agents", headers=HEADERS)
    ids = {a["agent_id"] for a in resp.json()["agents"]}
    assert "freedom-executive" in ids
    assert "gail-os-policy" in ids
    assert "graphify-cockpit" in ids


def test_agents_missing_auth_returns_422():
    resp = client.get("/api/v1/agents")
    assert resp.status_code == 422


def test_agents_wrong_api_key_returns_401():
    resp = client.get("/api/v1/agents", headers={"X-Api-Key": "wrong"})
    assert resp.status_code == 401


def test_agents_response_has_required_fields():
    resp = client.get("/api/v1/agents", headers=HEADERS)
    a = resp.json()["agents"][0]
    assert "agent_id" in a
    assert "display_name" in a
    assert "purpose" in a
    assert "cns_layer" in a
    assert "maturity" in a
    assert "max_authority_level" in a
    assert "action_kinds" in a
    assert isinstance(a["action_kinds"], list)
