"""Tests for m365-graph-api-bridge connector registration — task 4.1."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "uaos-core" / "src"))
sys.path.insert(0, str(ROOT / "apps" / "gail-os-api"))

import os
os.environ.setdefault("GAIL_OS_API_KEY", "test-key-local")

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402
from gail_ai_operating_system.connector_registry import ConnectorRegistry  # noqa: E402

client = TestClient(app)
HEADERS = {"X-Api-Key": "test-key-local"}

BRIDGE_ID = "m365-graph-api-bridge"


def _get_bridge():
    resp = client.get("/api/v1/connectors", headers=HEADERS)
    assert resp.status_code == 200
    connectors = resp.json()["connectors"]
    matches = [c for c in connectors if c["connector_id"] == BRIDGE_ID]
    assert len(matches) == 1, f"{BRIDGE_ID} not found in connector registry"
    return matches[0]


def test_m365_bridge_present_in_registry():
    bridge = _get_bridge()
    assert bridge["connector_id"] == BRIDGE_ID


def test_m365_bridge_system_family():
    bridge = _get_bridge()
    assert bridge["system_family"] == "Microsoft 365"


def test_m365_bridge_current_state_registry_only():
    bridge = _get_bridge()
    assert bridge["current_state"] == "registry-only"


def test_m365_bridge_live_access_disabled():
    bridge = _get_bridge()
    assert bridge["live_access_enabled"] is False


def test_m365_bridge_allowed_capabilities_include_readiness_check():
    bridge = _get_bridge()
    assert "readiness-check" in bridge["allowed_capabilities"]
    assert "planning-only" in bridge["allowed_capabilities"]


def test_m365_bridge_full_registry_valid():
    resp = client.get("/api/v1/connectors", headers=HEADERS)
    assert resp.json()["registry_valid"] is True


def test_m365_bridge_unit_validation_passes():
    registry = ConnectorRegistry()
    bridge_profile = registry.get_profile(BRIDGE_ID)
    assert bridge_profile is not None
    from gail_ai_operating_system.connector_registry import validate_connector_profile
    report = validate_connector_profile(bridge_profile)
    assert report.valid, f"Validation failed: {report.reasons}"


def test_m365_bridge_display_name():
    registry = ConnectorRegistry()
    bridge = registry.get_profile(BRIDGE_ID)
    assert bridge is not None
    assert "Graph" in bridge.display_name
    assert "svc-gail-os-graph" in bridge.notes


def test_m365_status_missing_auth_returns_422():
    resp = client.get("/api/v1/connectors")
    assert resp.status_code == 422


def test_m365_bridge_wrong_key_returns_401():
    resp = client.get("/api/v1/connectors", headers={"X-Api-Key": "bad"})
    assert resp.status_code == 401
