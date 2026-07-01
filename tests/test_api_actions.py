"""Tests for POST /api/v1/actions."""
from __future__ import annotations

import sys
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "uaos-core" / "src"))
sys.path.insert(0, str(ROOT / "apps" / "gail-os-api"))

import os
os.environ.setdefault("GAIL_OS_API_KEY", "test-key-local")

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402

client = TestClient(app)
HEADERS = {"X-Api-Key": "test-key-local"}
TRACE_ID = "cns-20260701-a1b2c3d4e5f6"

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


def _create_traceable_mission(tmp_path, monkeypatch) -> dict:
    monkeypatch.setenv("GAIL_OS_STORE_PATH", str(tmp_path))
    resp = client.post(
        "/api/v1/missions",
        headers=HEADERS,
        json={
            "command": "Create a governed local action loop proof",
            "domain": "build",
            "request_id": "REQ-GLW-API-001",
            "cns_trace_id": TRACE_ID,
        },
    )
    assert resp.status_code == 200
    return resp.json()


def test_local_action_request_and_decision_records_evidence_trace_and_brief(tmp_path, monkeypatch):
    mission = _create_traceable_mission(tmp_path, monkeypatch)

    request_resp = client.post(
        "/api/v1/actions/local",
        headers=HEADERS,
        json={
            "mission_id": mission["mission_id"],
            "action_type": "local_repo_read",
            "title": "Inspect local evidence refs",
            "actor": "freedom",
            "authority_level": "R1",
            "risk_tier": 1,
            "arguments": {"scope": "local_store/evidence"},
            "idempotency_key": "glw-action-request-001",
            "cns_trace_id": TRACE_ID,
        },
    )

    assert request_resp.status_code == 201
    action_request = request_resp.json()
    assert action_request["schema_version"] == "rev2.local-action-request.v1"
    assert action_request["policy_decision"]["allowed"] is True
    assert action_request["action"]["status"] == "approval_requested"
    assert action_request["execution_authority"]["granted"] is False
    action_id = action_request["action"]["action_id"]
    assert (tmp_path / "actions" / f"{action_id}.json").exists()

    decision_resp = client.post(
        f"/api/v1/actions/local/{action_id}/decisions",
        headers=HEADERS,
        json={
            "decision_type": "approved",
            "decided_by": "Adam Goodwin",
            "rationale": "Approved local proof of the governed action loop.",
            "authority_basis": "R1 local governed write approved by Adam",
            "expected_status": "approval_requested",
            "idempotency_key": "glw-action-decision-001",
            "decided_at": "2026-07-01T12:35:00Z",
            "cns_trace_id": TRACE_ID,
        },
    )

    assert decision_resp.status_code == 201
    decision = decision_resp.json()
    assert decision["schema_version"] == "rev2.local-action-decision.v1"
    assert decision["action"]["status"] == "approved"
    assert decision["decision"]["decision_type"] == "approved"
    assert decision["evidence"]["action_type"] == "local_approval_decision"
    assert decision["evidence"]["execution_mode"] == "dry-run"
    assert decision["execution_authority"]["target_action_executed"] is False
    decision_id = decision["decision"]["decision_id"]
    evidence_id = decision["evidence"]["evidence_id"]
    assert (tmp_path / "approvals" / f"{decision_id}.json").exists()
    assert (tmp_path / "evidence" / f"{evidence_id}.json").exists()

    trace_resp = client.get(f"/api/v1/traces/{TRACE_ID}", headers=HEADERS)
    assert trace_resp.status_code == 200
    trace = trace_resp.json()
    assert action_id in trace["action_ids"]
    assert decision_id in trace["authority_refs"]
    assert trace["action_refs"][0]["status"] == "approved"
    assert trace["approval_refs"][0]["decision_type"] == "approved"
    event_types = {event["event_type"] for event in trace["events"]}
    assert {"mission.created", "action.validated", "approval.decided", "evidence.recorded"} <= event_types

    brief_resp = client.get(
        f"/api/v1/freedom/relationship-briefs/{TRACE_ID}?stale_after_seconds=86400",
        headers=HEADERS,
    )
    assert brief_resp.status_code == 200
    brief = brief_resp.json()
    assert brief["action_snapshot"]["by_status"] == {"approved": 1}
    assert brief["approval_snapshot"]["by_decision_type"] == {"approved": 1}
    assert brief["execution_authority"]["granted"] is False


def test_local_action_decision_idempotency_returns_existing_records(tmp_path, monkeypatch):
    mission = _create_traceable_mission(tmp_path, monkeypatch)
    action_resp = client.post(
        "/api/v1/actions/local",
        headers=HEADERS,
        json={
            "mission_id": mission["mission_id"],
            "action_type": "policy_gate_review",
            "title": "Review local policy gate",
            "idempotency_key": "glw-action-request-dupe",
            "cns_trace_id": TRACE_ID,
        },
    )
    action_id = action_resp.json()["action"]["action_id"]
    body = {
        "decision_type": "held",
        "decided_by": "Adam Goodwin",
        "rationale": "Hold until the next owner check.",
        "authority_basis": "R1 local governed hold",
        "expected_status": "approval_requested",
        "idempotency_key": "glw-action-decision-dupe",
        "decided_at": "2026-07-01T12:36:00Z",
        "hold_until": "2026-07-01T13:00:00Z",
        "cns_trace_id": TRACE_ID,
    }

    first = client.post(f"/api/v1/actions/local/{action_id}/decisions", headers=HEADERS, json=body)
    second = client.post(f"/api/v1/actions/local/{action_id}/decisions", headers=HEADERS, json=body)

    assert first.status_code == 201
    assert second.status_code == 200
    assert second.json()["duplicate_detected"] is True
    assert second.json()["decision"]["decision_id"] == first.json()["decision"]["decision_id"]
    assert second.json()["evidence"]["evidence_id"] == first.json()["evidence"]["evidence_id"]
    assert len(list((tmp_path / "approvals").glob("aprv-*.json"))) == 1
    assert len(list((tmp_path / "evidence").glob("evidence-*.json"))) == 1


def test_local_action_decision_rejects_stale_expected_status(tmp_path, monkeypatch):
    mission = _create_traceable_mission(tmp_path, monkeypatch)
    action_resp = client.post(
        "/api/v1/actions/local",
        headers=HEADERS,
        json={
            "mission_id": mission["mission_id"],
            "action_type": "policy_gate_review",
            "title": "Review local policy gate",
            "idempotency_key": "glw-action-request-stale",
            "cns_trace_id": TRACE_ID,
        },
    )
    action_id = action_resp.json()["action"]["action_id"]

    resp = client.post(
        f"/api/v1/actions/local/{action_id}/decisions",
        headers=HEADERS,
        json={
            "decision_type": "approved",
            "decided_by": "Adam Goodwin",
            "rationale": "Approval should not apply against stale state.",
            "authority_basis": "R1 local governed write",
            "expected_status": "classified",
            "idempotency_key": "glw-action-decision-stale",
            "cns_trace_id": TRACE_ID,
        },
    )

    assert resp.status_code == 409
    assert "expected 'classified'" in json.dumps(resp.json())


def test_local_action_request_blocks_live_connector_action(tmp_path, monkeypatch):
    mission = _create_traceable_mission(tmp_path, monkeypatch)

    resp = client.post(
        "/api/v1/actions/local",
        headers=HEADERS,
        json={
            "mission_id": mission["mission_id"],
            "action_type": "m365_live_content_read",
            "title": "Read Microsoft 365 live content",
            "actor": "freedom",
            "risk_tier": 1,
            "idempotency_key": "glw-action-request-blocked",
            "cns_trace_id": TRACE_ID,
        },
    )

    assert resp.status_code == 409
    detail = resp.json()["detail"]
    assert detail["policy_decision"]["allowed"] is False
    assert "Microsoft 365 content reads are blocked" in detail["policy_decision"]["stop_reason"]
