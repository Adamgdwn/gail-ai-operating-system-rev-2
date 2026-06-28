"""Tests for GET /api/v1/evidence/{mission_id}."""
from __future__ import annotations

import json
import sys
import tempfile
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
NOW = "2026-06-28T00:00:00-06:00"


def _write_evidence(store: Path, mission_id: str, evidence_id: str, result: str = "success") -> None:
    store.mkdir(parents=True, exist_ok=True)
    data = {
        "evidence_id": evidence_id,
        "mission_id": mission_id,
        "action_id": "action-test001",
        "actor": "Adam Goodwin",
        "action_type": "local_mission_record",
        "authority_basis": "A1 local no-network",
        "result": result,
        "execution_mode": "dry-run",
        "created_at": NOW,
        "envelope_id": None,
        "rollback_note": None,
        "outcome_summary": "Test evidence record",
    }
    (store / f"{evidence_id}.json").write_text(json.dumps(data), encoding="utf-8")


def test_evidence_no_store_returns_empty_list():
    os.environ["GAIL_OS_STORE_PATH"] = "/tmp/gail_os_nonexistent_test_xyz_abc"
    resp = client.get("/api/v1/evidence/mission-doesnotexist", headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["mission_id"] == "mission-doesnotexist"
    assert data["evidence_refs"] == []


def test_evidence_empty_store_returns_empty_list():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["GAIL_OS_STORE_PATH"] = tmpdir
        resp = client.get("/api/v1/evidence/mission-empty001", headers=HEADERS)
        assert resp.status_code == 200
        assert resp.json()["evidence_refs"] == []


def test_evidence_returns_matching_refs():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = Path(tmpdir) / "evidence"
        _write_evidence(store, "mission-abc001", "evidence-e001")
        _write_evidence(store, "mission-abc001", "evidence-e002")
        _write_evidence(store, "mission-other", "evidence-e003")
        os.environ["GAIL_OS_STORE_PATH"] = tmpdir
        resp = client.get("/api/v1/evidence/mission-abc001", headers=HEADERS)
        assert resp.status_code == 200
        refs = resp.json()["evidence_refs"]
        assert len(refs) == 2
        ids = {r["evidence_id"] for r in refs}
        assert "evidence-e001" in ids
        assert "evidence-e002" in ids
        assert "evidence-e003" not in ids


def test_evidence_ref_has_expected_fields():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = Path(tmpdir) / "evidence"
        _write_evidence(store, "mission-fields001", "evidence-f001", result="success")
        os.environ["GAIL_OS_STORE_PATH"] = tmpdir
        resp = client.get("/api/v1/evidence/mission-fields001", headers=HEADERS)
        ref = resp.json()["evidence_refs"][0]
        assert ref["evidence_id"] == "evidence-f001"
        assert ref["mission_id"] == "mission-fields001"
        assert ref["result"] == "success"
        assert ref["created_at"] == NOW


def test_evidence_mission_not_in_store_returns_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = Path(tmpdir) / "evidence"
        _write_evidence(store, "mission-abc001", "evidence-e001")
        os.environ["GAIL_OS_STORE_PATH"] = tmpdir
        resp = client.get("/api/v1/evidence/mission-other999", headers=HEADERS)
        assert resp.json()["evidence_refs"] == []


def test_evidence_missing_auth_returns_422():
    resp = client.get("/api/v1/evidence/mission-abc001")
    assert resp.status_code == 422


def test_evidence_wrong_api_key_returns_401():
    resp = client.get("/api/v1/evidence/mission-abc001",
                      headers={"X-Api-Key": "bad-key"})
    assert resp.status_code == 401
