"""Tests for GET /api/v1/health — no auth required."""
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


def test_health_returns_200():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200


def test_health_status_ok():
    resp = client.get("/api/v1/health")
    assert resp.json()["status"] == "ok"


def test_health_boundary_is_a1_local():
    resp = client.get("/api/v1/health")
    assert "A1" in resp.json()["boundary"]


def test_health_no_auth_header_required():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200


def test_health_has_phase_field():
    resp = client.get("/api/v1/health")
    assert "phase" in resp.json()


def test_health_content_type_json():
    resp = client.get("/api/v1/health")
    assert "application/json" in resp.headers["content-type"]
