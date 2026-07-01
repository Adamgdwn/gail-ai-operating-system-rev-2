"""Tests for shared read-model and trace lookup API endpoints."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "uaos-core" / "src"))
sys.path.insert(0, str(ROOT / "apps" / "gail-os-api"))

os.environ.setdefault("GAIL_OS_API_KEY", "test-key-local")

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402

client = TestClient(app)
HEADERS = {"X-Api-Key": "test-key-local"}
TRACE_ID = "cns-20260701-feed1234abcd"
NOW = "2026-07-01T12:00:00Z"


def test_read_model_endpoint_returns_shared_status_surfaces(tmp_path, monkeypatch):
    monkeypatch.setenv("GAIL_OS_STORE_PATH", str(tmp_path))

    resp = client.get("/api/v1/read-model", headers=HEADERS)

    assert resp.status_code == 200
    data = resp.json()
    assert data["schema_version"] == "rev2.shared-read-model.v1"
    assert data["health"]["boundary"] == "A1 local no-network"
    assert data["authority"]["r5_human_only"] is True
    assert data["connectors"]["live_access_enabled"] is False
    assert data["agents"]["live_access_enabled"] is False
    assert data["m365"]["boundary"] == "A1 local no-network"
    assert "recent_events" in data
    assert "recent_evidence" in data


def test_mission_creation_persists_trace_event_and_mission_record(tmp_path, monkeypatch):
    monkeypatch.setenv("GAIL_OS_STORE_PATH", str(tmp_path))

    resp = client.post(
        "/api/v1/missions",
        headers=HEADERS,
        json={
            "command": "Create a traceable mission record",
            "domain": "build",
            "request_id": "REQ-TRACE-API-001",
            "cns_trace_id": TRACE_ID,
        },
    )

    assert resp.status_code == 200
    mission = resp.json()
    assert mission["cns_trace_id"] == TRACE_ID
    mission_path = tmp_path / "missions" / f"{mission['mission_id']}.json"
    assert mission_path.exists()
    assert json.loads(mission_path.read_text(encoding="utf-8"))["cns_trace_id"] == TRACE_ID

    read_model = client.get("/api/v1/read-model", headers=HEADERS).json()
    matching_events = [event for event in read_model["recent_events"] if event["cns_trace_id"] == TRACE_ID]
    assert len(matching_events) == 1
    assert matching_events[0]["event_type"] == "mission.created"
    assert matching_events[0]["mission_id"] == mission["mission_id"]


def test_trace_lookup_unifies_mission_and_m365_dry_run_evidence(tmp_path, monkeypatch):
    monkeypatch.setenv("GAIL_OS_STORE_PATH", str(tmp_path))
    monkeypatch.setenv("AZURE_TENANT_ID", "tenant-abc")
    monkeypatch.setenv("AZURE_CLIENT_ID", "client-xyz")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "secret-123")
    mission_resp = client.post(
        "/api/v1/missions",
        headers=HEADERS,
        json={
            "command": "Create a mission for dry-run Planner trace",
            "domain": "operations",
            "request_id": "REQ-TRACE-M365-001",
            "cns_trace_id": TRACE_ID,
        },
    )
    mission_id = mission_resp.json()["mission_id"]

    write_resp = client.post(
        "/api/v1/m365/write/planner-task",
        headers=HEADERS,
        json={
            "mission_id": mission_id,
            "action_id": "action-trace-planner",
            "actor": "gail-os-m365-dry-run-actor",
            "created_at": NOW,
            "plan_id": "plan-001",
            "bucket_id": "bucket-001",
            "task_title": "Traceable dry-run task",
            "cns_trace_id": TRACE_ID,
        },
    )

    assert write_resp.status_code == 200
    assert write_resp.json()["evidence"]["cns_trace_id"] == TRACE_ID

    trace_resp = client.get(f"/api/v1/traces/{TRACE_ID}", headers=HEADERS)
    assert trace_resp.status_code == 200
    trace = trace_resp.json()
    assert trace["found"] is True
    assert mission_id in trace["mission_ids"]
    assert "action-trace-planner" in trace["action_ids"]
    assert write_resp.json()["evidence"]["evidence_id"] in trace["evidence_ids"]
    event_types = {event["event_type"] for event in trace["events"]}
    assert {"mission.created", "evidence.recorded"} <= event_types


def test_duplicate_request_is_visible_in_trace_events(tmp_path, monkeypatch):
    monkeypatch.setenv("GAIL_OS_STORE_PATH", str(tmp_path))
    body = {
        "command": "Create a duplicate-detection mission record",
        "domain": "build",
        "request_id": "REQ-DUPE-TRACE",
        "cns_trace_id": TRACE_ID,
    }

    first = client.post("/api/v1/missions", headers=HEADERS, json=body)
    second = client.post("/api/v1/missions", headers=HEADERS, json=body)

    assert first.status_code == 200
    assert second.status_code == 200
    trace = client.get(f"/api/v1/traces/{TRACE_ID}", headers=HEADERS).json()
    mission_events = [event for event in trace["events"] if event["event_type"] == "mission.created"]
    assert len(mission_events) == 2
    assert mission_events[0]["duplicate_detected"] is False
    assert mission_events[1]["duplicate_detected"] is True
    assert mission_events[1]["duplicate_of_event_id"] == mission_events[0]["event_id"]


def test_trace_lookup_rejects_bad_trace_id(tmp_path, monkeypatch):
    monkeypatch.setenv("GAIL_OS_STORE_PATH", str(tmp_path))

    resp = client.get("/api/v1/traces/not-a-trace", headers=HEADERS)

    assert resp.status_code == 422
