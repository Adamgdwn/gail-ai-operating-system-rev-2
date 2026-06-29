"""Tests for authority registry and POST /api/v1/authority/override."""
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

VALID_OVERRIDE_REQUEST = {
    "action_id": "action-blocked-001",
    "mission_id": "mission-test-abc",
    "summary": "Read M365 calendar for scheduling context",
    "action_kind": "calendar",
    "risk_tier": 3,
    "blocking_reason": "Restricted action requires live GAIL OS approval before execution.",
    "requested_by": "freedom",
    "request_id": "req-override-001",
}


def test_authority_registry_returns_200():
    resp = client.get("/api/v1/authority", headers=HEADERS)
    assert resp.status_code == 200


def test_authority_registry_is_read_only_local_boundary():
    resp = client.get("/api/v1/authority", headers=HEADERS)
    data = resp.json()
    assert data["registry_valid"] is True
    assert data["boundary"] == "A1 local no-network"
    assert data["live_execution_enabled"] is False


def test_authority_registry_includes_r_ladder_guardrails():
    resp = client.get("/api/v1/authority", headers=HEADERS)
    data = resp.json()
    levels = {item["level"]: item for item in data["authority_levels"]}
    assert set(levels) == {"R0", "R1", "R2", "R3", "R4", "R5"}
    assert data["r4_requires_authority_envelope"] is True
    assert data["r5_human_only"] is True
    assert "Human-only" in levels["R5"]["agent_boundary"]


def test_authority_registry_missing_auth_returns_422():
    resp = client.get("/api/v1/authority")
    assert resp.status_code == 422


def test_override_request_returns_201():
    resp = client.post("/api/v1/authority/override", json=VALID_OVERRIDE_REQUEST, headers=HEADERS)
    assert resp.status_code == 201


def test_override_request_returns_pending_status():
    resp = client.post("/api/v1/authority/override", json=VALID_OVERRIDE_REQUEST, headers=HEADERS)
    data = resp.json()
    assert data["status"] == "pending"


def test_override_request_echoes_action_and_mission_ids():
    resp = client.post("/api/v1/authority/override", json=VALID_OVERRIDE_REQUEST, headers=HEADERS)
    data = resp.json()
    assert data["action_id"] == "action-blocked-001"
    assert data["mission_id"] == "mission-test-abc"


def test_override_request_returns_override_request_id():
    resp = client.post("/api/v1/authority/override", json=VALID_OVERRIDE_REQUEST, headers=HEADERS)
    data = resp.json()
    assert "override_request_id" in data
    assert data["override_request_id"].startswith("override-")


def test_override_request_returns_recorded_at_utc():
    resp = client.post("/api/v1/authority/override", json=VALID_OVERRIDE_REQUEST, headers=HEADERS)
    data = resp.json()
    assert "recorded_at" in data
    assert data["recorded_at"].endswith("Z")


def test_override_request_ids_are_unique():
    resp1 = client.post("/api/v1/authority/override", json=VALID_OVERRIDE_REQUEST, headers=HEADERS)
    resp2 = client.post("/api/v1/authority/override", json=VALID_OVERRIDE_REQUEST, headers=HEADERS)
    assert resp1.json()["override_request_id"] != resp2.json()["override_request_id"]


def test_override_request_missing_auth_returns_422():
    resp = client.post("/api/v1/authority/override", json=VALID_OVERRIDE_REQUEST)
    assert resp.status_code == 422


def test_override_request_missing_required_fields_returns_422():
    resp = client.post("/api/v1/authority/override", json={
        "action_id": "action-001",
    }, headers=HEADERS)
    assert resp.status_code == 422


def test_override_request_minimum_valid_payload():
    minimal = {
        "action_id": "action-minimal-001",
        "mission_id": "mission-minimal-001",
        "summary": "Minimal override request",
        "blocking_reason": "Policy gate blocked this action.",
    }
    resp = client.post("/api/v1/authority/override", json=minimal, headers=HEADERS)
    assert resp.status_code == 201
    data = resp.json()
    assert data["action_kind"] == "general"
    assert data["risk_tier"] == 2
    assert data["requested_by"] == "freedom"
