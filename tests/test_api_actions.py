"""Tests for POST /api/v1/actions."""
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

VALID_MISSION = {
    "mission_id": "mission-testabcdef01",
    "request_id": "REQ-TEST",
    "command": "Create a local mission record",
    "domain": "build",
    "created_at": "2026-06-28T00:00:00-06:00",
    "owner": "Adam Goodwin",
    "approval_level": "A1 local no-network",
    "dry_run": True,
    "requested_tools": [],
    "data_classification": "internal",
    "status": "draft",
}

LOCAL_ACTION = {
    "action_id": "action-testabcdef01",
    "action_type": "local_mission_record",
    "title": "Create local mission record",
    "arguments": {},
    "risk_tier": 1,
}


def test_validate_action_allowed_returns_200():
    resp = client.post("/api/v1/actions", json={
        "mission": VALID_MISSION,
        "action": LOCAL_ACTION,
    }, headers=HEADERS)
    assert resp.status_code == 200


def test_validate_action_allowed_local():
    resp = client.post("/api/v1/actions", json={
        "mission": VALID_MISSION,
        "action": LOCAL_ACTION,
    }, headers=HEADERS)
    data = resp.json()
    assert data["allowed"] is True
    assert data["mode"] == "dry-run"


def test_validate_action_stop_trigger_blocked():
    stop_action = {
        "action_id": "action-stop-001",
        "action_type": "m365_live_content_read",
        "title": "Read M365",
        "arguments": {},
        "risk_tier": 3,
    }
    resp = client.post("/api/v1/actions", json={
        "mission": VALID_MISSION,
        "action": stop_action,
    }, headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["allowed"] is False
    assert data["mode"] == "stop"


def test_validate_action_high_risk_tier_blocked():
    risky = {
        "action_id": "action-risky-001",
        "action_type": "local_repo_read",
        "title": "Risky read",
        "arguments": {},
        "risk_tier": 5,
    }
    resp = client.post("/api/v1/actions", json={
        "mission": VALID_MISSION,
        "action": risky,
    }, headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["allowed"] is False
    assert data["stop_reason"] is not None
    assert "Tier" in data["stop_reason"]


def test_validate_action_missing_auth_returns_422():
    resp = client.post("/api/v1/actions", json={
        "mission": VALID_MISSION,
        "action": LOCAL_ACTION,
    })
    assert resp.status_code == 422


def test_validate_action_malformed_mission_returns_422():
    resp = client.post("/api/v1/actions", json={
        "mission": {"bad": "data"},
        "action": LOCAL_ACTION,
    }, headers=HEADERS)
    assert resp.status_code == 422


def test_validate_action_returns_all_fields():
    resp = client.post("/api/v1/actions", json={
        "mission": VALID_MISSION,
        "action": LOCAL_ACTION,
    }, headers=HEADERS)
    data = resp.json()
    assert "action_id" in data
    assert "allowed" in data
    assert "mode" in data
    assert "reason" in data
    assert "stop_reason" in data


def test_validate_action_default_deny_unlisted_type():
    unlisted = {
        "action_id": "action-unknown-001",
        "action_type": "send_external_email",
        "title": "Send email",
        "arguments": {},
        "risk_tier": 1,
    }
    resp = client.post("/api/v1/actions", json={
        "mission": VALID_MISSION,
        "action": unlisted,
    }, headers=HEADERS)
    data = resp.json()
    assert data["allowed"] is False
    assert "Default deny" in (data["stop_reason"] or "")


def test_validate_action_accepts_freedom_low_risk_system_bridge_payload():
    freedom_mission = {
        "mission_id": "mission-integration-1",
        "request_id": "req-integration-action-1",
        "command": "Read local evidence store",
        "domain": "build",
        "created_at": "2026-06-28T00:00:00.000Z",
        "owner": "freedom",
        "approval_level": "A1 local no-network",
        "dry_run": True,
    }
    freedom_action = {
        "action_id": "action-integration-1",
        "mission_id": "mission-integration-1",
        "action_type": "system",
        "title": "Read local evidence store",
        "actor": "freedom",
        "status": "proposed",
        "authority_level": "R1",
        "risk_tier": 1,
        "arguments": {},
        "created_at": "2026-06-28T00:00:00.000Z",
    }

    resp = client.post("/api/v1/actions", json={
        "mission": freedom_mission,
        "action": freedom_action,
    }, headers=HEADERS)

    assert resp.status_code == 200
    data = resp.json()
    assert data["action_id"] == "action-integration-1"
    assert data["allowed"] is True
    assert data["mode"] == "dry-run"
