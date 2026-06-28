"""Tests for m365_writer.create_planner_task and POST /api/v1/m365/write/planner-task."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "uaos-core" / "src"))
sys.path.insert(0, str(ROOT / "apps" / "gail-os-api"))

import os
os.environ.setdefault("GAIL_OS_API_KEY", "test-key-local")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from gail_ai_operating_system.evidence_packet import (  # noqa: E402
    EvidenceResult,
    ExecutionMode,
    validate_evidence_packet,
)
from gail_ai_operating_system.m365_auth import GraphAuthProvider  # noqa: E402
from gail_ai_operating_system.m365_writer import create_planner_task  # noqa: E402
from main import app  # noqa: E402

client = TestClient(app)
HEADERS = {"X-Api-Key": "test-key-local"}
NOW = "2026-06-28T12:00:00Z"

_CONFIGURED_AUTH = GraphAuthProvider(
    tenant_id="tenant-abc",
    client_id="client-xyz",
    client_secret="secret-123",
)
_UNCONFIGURED_AUTH = GraphAuthProvider(
    tenant_id="",
    client_id="",
    client_secret="",
)

VALID_BODY = {
    "mission_id": "mission-planner-001",
    "action_id": "action-create-task",
    "actor": "svc-gail-os-graph",
    "created_at": NOW,
    "plan_id": "plan-gail-ops-001",
    "bucket_id": "bucket-missions-001",
    "task_title": "GAIL OS mission tracking task",
}


# --- Service layer unit tests ---

def test_create_planner_task_dry_run_returns_success_when_configured():
    packet = create_planner_task(
        _CONFIGURED_AUTH,
        mission_id="mission-planner-001",
        action_id="action-create-task",
        actor="svc-gail-os-graph",
        created_at=NOW,
        plan_id="plan-gail-ops-001",
        bucket_id="bucket-missions-001",
        task_title="Test task",
        dry_run=True,
    )
    assert packet.result == EvidenceResult.SUCCESS.value


def test_create_planner_task_dry_run_stopped_when_not_configured():
    packet = create_planner_task(
        _UNCONFIGURED_AUTH,
        mission_id="mission-planner-002",
        action_id="action-create-task",
        actor="svc-gail-os-graph",
        created_at=NOW,
        plan_id="plan-gail-ops-001",
        bucket_id="bucket-missions-001",
        task_title="Test task",
        dry_run=True,
    )
    assert packet.result == EvidenceResult.STOPPED.value
    assert "not configured" in packet.outcome_summary.lower()


def test_create_planner_task_stopped_on_empty_task_title():
    packet = create_planner_task(
        _CONFIGURED_AUTH,
        mission_id="mission-planner-003",
        action_id="action-create-task",
        actor="svc-gail-os-graph",
        created_at=NOW,
        plan_id="plan-gail-ops-001",
        bucket_id="bucket-missions-001",
        task_title="",
        dry_run=True,
    )
    assert packet.result == EvidenceResult.STOPPED.value
    assert "task_title" in packet.outcome_summary


def test_create_planner_task_stopped_on_empty_plan_id():
    packet = create_planner_task(
        _CONFIGURED_AUTH,
        mission_id="mission-planner-004",
        action_id="action-create-task",
        actor="svc-gail-os-graph",
        created_at=NOW,
        plan_id="",
        bucket_id="bucket-missions-001",
        task_title="Test task",
        dry_run=True,
    )
    assert packet.result == EvidenceResult.STOPPED.value
    assert "plan_id" in packet.outcome_summary


def test_create_planner_task_evidence_has_r2_authority_basis():
    packet = create_planner_task(
        _CONFIGURED_AUTH,
        mission_id="mission-planner-005",
        action_id="action-create-task",
        actor="svc-gail-os-graph",
        created_at=NOW,
        plan_id="plan-gail-ops-001",
        bucket_id="bucket-missions-001",
        task_title="Test task",
        dry_run=True,
    )
    assert "R2_INTERNAL_WRITE" in packet.authority_basis


def test_create_planner_task_evidence_id_has_correct_prefix():
    packet = create_planner_task(
        _CONFIGURED_AUTH,
        mission_id="mission-planner-006",
        action_id="action-create-task",
        actor="svc-gail-os-graph",
        created_at=NOW,
        plan_id="plan-gail-ops-001",
        bucket_id="bucket-missions-001",
        task_title="Test task",
        dry_run=True,
    )
    assert packet.evidence_id.startswith("evidence-")


def test_create_planner_task_evidence_is_valid():
    packet = create_planner_task(
        _CONFIGURED_AUTH,
        mission_id="mission-planner-007",
        action_id="action-create-task",
        actor="svc-gail-os-graph",
        created_at=NOW,
        plan_id="plan-gail-ops-001",
        bucket_id="bucket-missions-001",
        task_title="Test task",
        dry_run=True,
    )
    errors = validate_evidence_packet(packet, allow_live=False)
    assert errors == []


def test_create_planner_task_dry_run_execution_mode():
    packet = create_planner_task(
        _CONFIGURED_AUTH,
        mission_id="mission-planner-008",
        action_id="action-create-task",
        actor="svc-gail-os-graph",
        created_at=NOW,
        plan_id="plan-gail-ops-001",
        bucket_id="bucket-missions-001",
        task_title="Test task",
        dry_run=True,
    )
    assert packet.execution_mode == ExecutionMode.DRY_RUN.value


def test_create_planner_task_dry_run_rollback_note():
    packet = create_planner_task(
        _CONFIGURED_AUTH,
        mission_id="mission-planner-009",
        action_id="action-create-task",
        actor="svc-gail-os-graph",
        created_at=NOW,
        plan_id="plan-gail-ops-001",
        bucket_id="bucket-missions-001",
        task_title="Test task",
        dry_run=True,
    )
    assert "dry-run" in (packet.rollback_note or "").lower()


# --- API endpoint tests ---

def test_api_m365_write_planner_task_returns_200_and_evidence(monkeypatch):
    monkeypatch.setenv("AZURE_TENANT_ID", "tenant-abc")
    monkeypatch.setenv("AZURE_CLIENT_ID", "client-xyz")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "secret-123")
    resp = client.post("/api/v1/m365/write/planner-task", headers=HEADERS, json=VALID_BODY)
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert "evidence" in data
    ev = data["evidence"]
    assert ev["evidence_id"].startswith("evidence-")
    assert ev["result"] == "success"
    assert ev["execution_mode"] == "dry-run"
    assert "R2_INTERNAL_WRITE" in ev["authority_basis"]


def test_api_m365_write_planner_task_not_configured_returns_stopped(monkeypatch):
    monkeypatch.delenv("AZURE_TENANT_ID", raising=False)
    monkeypatch.delenv("AZURE_CLIENT_ID", raising=False)
    monkeypatch.delenv("AZURE_CLIENT_SECRET", raising=False)
    resp = client.post("/api/v1/m365/write/planner-task", headers=HEADERS, json=VALID_BODY)
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert data["evidence"]["result"] == "stopped"


def test_api_m365_write_planner_task_missing_auth_returns_422():
    resp = client.post("/api/v1/m365/write/planner-task", json=VALID_BODY)
    assert resp.status_code == 422


def test_api_m365_write_planner_task_wrong_key_returns_401():
    resp = client.post(
        "/api/v1/m365/write/planner-task",
        headers={"X-Api-Key": "bad-key"},
        json=VALID_BODY,
    )
    assert resp.status_code == 401


def test_api_m365_write_planner_task_invalid_payload_returns_422():
    resp = client.post(
        "/api/v1/m365/write/planner-task",
        headers=HEADERS,
        json={"mission_id": "bad-id", "action_id": "bad-id", "actor": "a", "created_at": NOW,
              "plan_id": "p", "bucket_id": "b", "task_title": "t"},
    )
    assert resp.status_code == 422
