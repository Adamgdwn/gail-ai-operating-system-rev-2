"""Tests for m365_reader.observe_graph_metadata and POST /api/v1/m365/observe."""
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
from gail_ai_operating_system.m365_reader import observe_graph_metadata  # noqa: E402
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
    "mission_id": "mission-observe-001",
    "action_id": "action-observe-org",
    "actor": "svc-gail-os-graph",
    "created_at": NOW,
    "observe_target": "organization",
}


# --- Service layer unit tests ---

def test_observe_dry_run_returns_success_when_configured():
    packet = observe_graph_metadata(
        _CONFIGURED_AUTH,
        mission_id="mission-observe-001",
        action_id="action-observe-org",
        actor="svc-gail-os-graph",
        created_at=NOW,
        dry_run=True,
    )
    assert packet.result == EvidenceResult.SUCCESS.value


def test_observe_dry_run_stopped_when_not_configured():
    packet = observe_graph_metadata(
        _UNCONFIGURED_AUTH,
        mission_id="mission-observe-002",
        action_id="action-observe-org",
        actor="svc-gail-os-graph",
        created_at=NOW,
        dry_run=True,
    )
    assert packet.result == EvidenceResult.STOPPED.value
    assert "not configured" in packet.outcome_summary.lower()


def test_observe_invalid_target_returns_stopped():
    packet = observe_graph_metadata(
        _CONFIGURED_AUTH,
        mission_id="mission-observe-003",
        action_id="action-observe-org",
        actor="svc-gail-os-graph",
        created_at=NOW,
        observe_target="calendar",
        dry_run=True,
    )
    assert packet.result == EvidenceResult.STOPPED.value
    assert "not allowed" in packet.outcome_summary.lower()


def test_observe_evidence_has_r0_authority_basis():
    packet = observe_graph_metadata(
        _CONFIGURED_AUTH,
        mission_id="mission-observe-004",
        action_id="action-observe-org",
        actor="svc-gail-os-graph",
        created_at=NOW,
        dry_run=True,
    )
    assert "R0_OBSERVE" in packet.authority_basis


def test_observe_evidence_id_has_correct_prefix():
    packet = observe_graph_metadata(
        _CONFIGURED_AUTH,
        mission_id="mission-observe-005",
        action_id="action-observe-org",
        actor="svc-gail-os-graph",
        created_at=NOW,
        dry_run=True,
    )
    assert packet.evidence_id.startswith("evidence-")


def test_observe_evidence_is_valid():
    packet = observe_graph_metadata(
        _CONFIGURED_AUTH,
        mission_id="mission-observe-006",
        action_id="action-observe-org",
        actor="svc-gail-os-graph",
        created_at=NOW,
        dry_run=True,
    )
    errors = validate_evidence_packet(packet, allow_live=False)
    assert errors == []


def test_observe_dry_run_execution_mode():
    packet = observe_graph_metadata(
        _CONFIGURED_AUTH,
        mission_id="mission-observe-007",
        action_id="action-observe-org",
        actor="svc-gail-os-graph",
        created_at=NOW,
        dry_run=True,
    )
    assert packet.execution_mode == ExecutionMode.DRY_RUN.value


# --- API endpoint tests ---

def test_api_m365_observe_returns_200_and_evidence(monkeypatch):
    monkeypatch.setenv("AZURE_TENANT_ID", "tenant-abc")
    monkeypatch.setenv("AZURE_CLIENT_ID", "client-xyz")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "secret-123")
    resp = client.post("/api/v1/m365/observe", headers=HEADERS, json=VALID_BODY)
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert "evidence" in data
    ev = data["evidence"]
    assert ev["evidence_id"].startswith("evidence-")
    assert ev["result"] == "success"
    assert ev["execution_mode"] == "dry-run"
    assert "R0_OBSERVE" in ev["authority_basis"]


def test_api_m365_observe_accepts_synthetic_probe_body(monkeypatch):
    monkeypatch.setenv("AZURE_TENANT_ID", "tenant-abc")
    monkeypatch.setenv("AZURE_CLIENT_ID", "client-xyz")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "secret-123")
    resp = client.post("/api/v1/m365/observe", headers=HEADERS, json={"dry_run": True})
    assert resp.status_code == 200
    data = resp.json()
    ev = data["evidence"]
    assert ev["mission_id"] == "mission-ctp2-probe"
    assert ev["action_id"] == "action-ctp2-m365-observe"
    assert ev["execution_mode"] == "dry-run"


def test_api_m365_observe_rejects_live_probe_request():
    resp = client.post("/api/v1/m365/observe", headers=HEADERS, json={"dry_run": False})
    assert resp.status_code == 422


def test_api_m365_observe_not_configured_returns_stopped(monkeypatch):
    monkeypatch.delenv("AZURE_TENANT_ID", raising=False)
    monkeypatch.delenv("AZURE_CLIENT_ID", raising=False)
    monkeypatch.delenv("AZURE_CLIENT_SECRET", raising=False)
    resp = client.post("/api/v1/m365/observe", headers=HEADERS, json=VALID_BODY)
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert data["evidence"]["result"] == "stopped"


def test_api_m365_observe_missing_auth_returns_422():
    resp = client.post("/api/v1/m365/observe", json=VALID_BODY)
    assert resp.status_code == 422


def test_api_m365_observe_wrong_key_returns_401():
    resp = client.post("/api/v1/m365/observe", headers={"X-Api-Key": "bad-key"}, json=VALID_BODY)
    assert resp.status_code == 401


def test_api_m365_observe_invalid_payload_returns_422():
    resp = client.post(
        "/api/v1/m365/observe",
        headers=HEADERS,
        json={"mission_id": "bad-id", "action_id": "bad-id", "actor": "a", "created_at": NOW},
    )
    assert resp.status_code == 422
