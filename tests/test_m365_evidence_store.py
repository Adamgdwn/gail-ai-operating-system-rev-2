"""Tests for evidence_store.save_evidence_packet and evidence persistence after M365 write."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "uaos-core" / "src"))
sys.path.insert(0, str(ROOT / "apps" / "gail-os-api"))

import os
os.environ.setdefault("GAIL_OS_API_KEY", "test-key-local")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from gail_ai_operating_system.evidence_packet import EvidencePacket, create_evidence_packet  # noqa: E402
from gail_ai_operating_system.evidence_store import save_evidence_packet  # noqa: E402
from main import app  # noqa: E402

client = TestClient(app)
HEADERS = {"X-Api-Key": "test-key-local"}
NOW = "2026-06-28T12:00:00Z"

VALID_BODY = {
    "mission_id": "mission-persist-001",
    "action_id": "action-store-task",
    "actor": "svc-gail-os-graph",
    "created_at": NOW,
    "plan_id": "plan-gail-ops-001",
    "bucket_id": "bucket-missions-001",
    "task_title": "Evidence persistence test task",
}


def _make_packet(mission_id: str, action_id: str) -> EvidencePacket:
    return create_evidence_packet(
        mission_id=mission_id,
        action_id=action_id,
        actor="test-actor",
        action_type="m365.write.planner-task",
        authority_basis="R2_INTERNAL_WRITE — test",
        result="success",
        created_at=NOW,
        execution_mode="dry-run",
        rollback_note="Dry-run only; no task created.",
        outcome_summary="Test evidence packet.",
        allow_live=False,
    )


# --- Service layer unit tests ---

def test_save_creates_file(tmp_path):
    store = tmp_path / "evidence"
    packet = _make_packet("mission-persist-001", "action-store-001")
    save_evidence_packet(packet, store_path=store)
    assert (store / f"{packet.evidence_id}.json").exists()


def test_save_content_matches_packet(tmp_path):
    store = tmp_path / "evidence"
    packet = _make_packet("mission-persist-002", "action-store-002")
    path = save_evidence_packet(packet, store_path=store)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["evidence_id"] == packet.evidence_id
    assert data["mission_id"] == packet.mission_id
    assert data["result"] == packet.result
    assert data["execution_mode"] == packet.execution_mode


def test_save_creates_directory_if_absent(tmp_path):
    store = tmp_path / "nested" / "evidence"
    assert not store.exists()
    packet = _make_packet("mission-persist-003", "action-store-003")
    save_evidence_packet(packet, store_path=store)
    assert store.exists()


def test_save_returns_correct_path(tmp_path):
    store = tmp_path / "evidence"
    packet = _make_packet("mission-persist-004", "action-store-004")
    path = save_evidence_packet(packet, store_path=store)
    assert path == store / f"{packet.evidence_id}.json"


def test_save_file_name_matches_evidence_id(tmp_path):
    store = tmp_path / "evidence"
    packet = _make_packet("mission-persist-005", "action-store-005")
    path = save_evidence_packet(packet, store_path=store)
    assert path.stem == packet.evidence_id


def test_save_uses_env_store_path(tmp_path, monkeypatch):
    monkeypatch.setenv("GAIL_OS_STORE_PATH", str(tmp_path))
    packet = _make_packet("mission-persist-006", "action-store-006")
    path = save_evidence_packet(packet)
    assert path.parent == tmp_path / "evidence"
    assert path.exists()


# --- API integration tests ---

def test_api_write_stores_evidence_file(tmp_path, monkeypatch):
    monkeypatch.setenv("GAIL_OS_STORE_PATH", str(tmp_path))
    monkeypatch.setenv("AZURE_TENANT_ID", "tenant-abc")
    monkeypatch.setenv("AZURE_CLIENT_ID", "client-xyz")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "secret-123")
    resp = client.post("/api/v1/m365/write/planner-task", headers=HEADERS, json=VALID_BODY)
    assert resp.status_code == 200
    evidence_id = resp.json()["evidence"]["evidence_id"]
    assert (tmp_path / "evidence" / f"{evidence_id}.json").exists()


def test_evidence_retrievable_after_write(tmp_path, monkeypatch):
    monkeypatch.setenv("GAIL_OS_STORE_PATH", str(tmp_path))
    monkeypatch.setenv("AZURE_TENANT_ID", "tenant-abc")
    monkeypatch.setenv("AZURE_CLIENT_ID", "client-xyz")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "secret-123")
    mission_id = VALID_BODY["mission_id"]
    client.post("/api/v1/m365/write/planner-task", headers=HEADERS, json=VALID_BODY)
    get_resp = client.get(f"/api/v1/evidence/{mission_id}", headers=HEADERS)
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["mission_id"] == mission_id
    assert len(data["evidence_refs"]) == 1
    assert data["evidence_refs"][0]["result"] == "success"


def test_evidence_ref_has_correct_fields(tmp_path, monkeypatch):
    monkeypatch.setenv("GAIL_OS_STORE_PATH", str(tmp_path))
    monkeypatch.setenv("AZURE_TENANT_ID", "tenant-abc")
    monkeypatch.setenv("AZURE_CLIENT_ID", "client-xyz")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "secret-123")
    mission_id = VALID_BODY["mission_id"]
    write_resp = client.post("/api/v1/m365/write/planner-task", headers=HEADERS, json=VALID_BODY)
    written_id = write_resp.json()["evidence"]["evidence_id"]
    get_resp = client.get(f"/api/v1/evidence/{mission_id}", headers=HEADERS)
    ref = get_resp.json()["evidence_refs"][0]
    assert ref["evidence_id"] == written_id
    assert ref["mission_id"] == mission_id
    assert ref["action_id"] == VALID_BODY["action_id"]
    assert ref["created_at"] == NOW


def test_multiple_writes_both_stored(tmp_path, monkeypatch):
    monkeypatch.setenv("GAIL_OS_STORE_PATH", str(tmp_path))
    monkeypatch.setenv("AZURE_TENANT_ID", "tenant-abc")
    monkeypatch.setenv("AZURE_CLIENT_ID", "client-xyz")
    monkeypatch.setenv("AZURE_CLIENT_SECRET", "secret-123")
    mission_id = VALID_BODY["mission_id"]
    body1 = {**VALID_BODY, "action_id": "action-task-alpha"}
    body2 = {**VALID_BODY, "action_id": "action-task-beta"}
    client.post("/api/v1/m365/write/planner-task", headers=HEADERS, json=body1)
    client.post("/api/v1/m365/write/planner-task", headers=HEADERS, json=body2)
    get_resp = client.get(f"/api/v1/evidence/{mission_id}", headers=HEADERS)
    refs = get_resp.json()["evidence_refs"]
    assert len(refs) == 2
    action_ids = {r["action_id"] for r in refs}
    assert "action-task-alpha" in action_ids
    assert "action-task-beta" in action_ids
