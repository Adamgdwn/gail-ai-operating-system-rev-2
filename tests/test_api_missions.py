"""Tests for POST /api/v1/missions."""
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


def test_create_mission_happy_path():
    resp = client.post("/api/v1/missions", json={
        "command": "Create a local mission record for build validation",
        "domain": "build",
        "request_id": "REQ-TEST-001",
    }, headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["mission_id"].startswith("mission-")
    assert data["command"] == "Create a local mission record for build validation"
    assert data["domain"] == "build"
    assert data["dry_run"] is True
    assert data["owner"] == "Adam Goodwin"


def test_create_mission_returns_full_envelope():
    resp = client.post("/api/v1/missions", json={
        "command": "Run local validation suite",
        "domain": "validation",
        "request_id": "REQ-VAL-001",
        "requested_tools": ["local_repo", "policy_gate"],
        "data_classification": "synthetic",
    }, headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["request_id"] == "REQ-VAL-001"
    assert data["domain"] == "validation"
    assert "local_repo" in data["requested_tools"]
    assert data["data_classification"] == "synthetic"
    assert data["approval_level"] == "A1 local no-network"


def test_create_mission_empty_command_returns_422():
    resp = client.post("/api/v1/missions", json={"command": "   "}, headers=HEADERS)
    assert resp.status_code == 422


def test_create_mission_stop_trigger_command_returns_200():
    resp = client.post("/api/v1/missions", json={
        "command": "Send email to the client",
    }, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["mission_id"].startswith("mission-")


def test_create_mission_missing_auth_returns_422():
    resp = client.post("/api/v1/missions", json={"command": "test"})
    assert resp.status_code == 422


def test_create_mission_wrong_api_key_returns_401():
    resp = client.post("/api/v1/missions", json={"command": "test"},
                       headers={"X-Api-Key": "wrong-key"})
    assert resp.status_code == 401


def test_create_mission_unknown_domain_normalizes_to_build():
    resp = client.post("/api/v1/missions", json={
        "command": "Some task",
        "domain": "not_a_real_domain",
    }, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["domain"] == "build"


def test_create_mission_dry_run_always_true():
    resp = client.post("/api/v1/missions", json={
        "command": "Build a local record",
    }, headers=HEADERS)
    assert resp.json()["dry_run"] is True


def test_create_mission_id_uses_mission_prefix():
    resp = client.post("/api/v1/missions", json={
        "command": "Validate local build artifacts",
    }, headers=HEADERS)
    assert resp.json()["mission_id"].startswith("mission-")
