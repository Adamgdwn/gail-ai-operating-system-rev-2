"""Tests for SignalGravityL1Calculator and the OKP API endpoints (Phase 5.3)."""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

# Ensure uaos-core is importable
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "packages" / "uaos-core" / "src"),
)
# Ensure routers (FastAPI app) are importable
_API_DIR = str(Path(__file__).resolve().parent.parent / "apps" / "gail-os-api")
if _API_DIR not in sys.path:
    sys.path.insert(0, _API_DIR)

from gail_ai_operating_system.operating_knowledge import (
    OkpRecordType,
    create_operating_knowledge_packet,
)
from gail_ai_operating_system.signal_gravity import (
    DEFAULT_WEIGHTS,
    SignalGravityL1Calculator,
)


def _make_okp(*, observed_at=None, risk_tier=2, confidence=0.8,
              status="observed", authority_level="R1", source_ref="sg-test-ref",
              summary="Signal gravity test", record_type=OkpRecordType.EVIDENCE_CREATED):
    return create_operating_knowledge_packet(
        source_system="test",
        source_ref=source_ref,
        record_type=record_type,
        summary=summary,
        authority_level=authority_level,
        autonomy_level="A1",
        risk_tier=risk_tier,
        data_classification="internal",
        confidence=confidence,
        status=status,
        observed_at=observed_at,
    )


# ---------------------------------------------------------------------------
# Test 1: L1 score is in range [0.0, 1.0]
# ---------------------------------------------------------------------------

def test_score_in_range(tmp_path):
    calc = SignalGravityL1Calculator(store_path=str(tmp_path))
    okp = _make_okp()
    score = calc.calculate(okp)
    assert 0.0 <= score <= 1.0


# ---------------------------------------------------------------------------
# Test 2: Factor 1 — recent signal scores higher than old signal
# ---------------------------------------------------------------------------

def test_factor1_recent_vs_old(tmp_path):
    calc = SignalGravityL1Calculator(store_path=str(tmp_path))
    now = datetime.now(timezone.utc)
    recent_okp = _make_okp(observed_at=now - timedelta(hours=1),
                            source_ref="f1-recent", summary="Recent")
    old_okp = _make_okp(observed_at=now - timedelta(hours=200),
                         source_ref="f1-old", summary="Old")
    recent_score = calc.calculate(recent_okp)
    old_score = calc.calculate(old_okp)
    assert recent_score > old_score


# ---------------------------------------------------------------------------
# Test 3: Factor 2 — risk_tier 5 scores higher than risk_tier 1
# ---------------------------------------------------------------------------

def test_factor2_risk_tier(tmp_path):
    calc = SignalGravityL1Calculator(store_path=str(tmp_path))
    high_risk = _make_okp(risk_tier=5, source_ref="f2-high", summary="High risk")
    low_risk = _make_okp(risk_tier=1, source_ref="f2-low", summary="Low risk")
    assert calc.calculate(high_risk) > calc.calculate(low_risk)


# ---------------------------------------------------------------------------
# Test 4: Factor 3 — high confidence scores higher
# ---------------------------------------------------------------------------

def test_factor3_confidence(tmp_path):
    calc = SignalGravityL1Calculator(store_path=str(tmp_path))
    high_conf = _make_okp(confidence=1.0, source_ref="f3-hi", summary="High conf")
    low_conf = _make_okp(confidence=0.1, source_ref="f3-lo", summary="Low conf")
    assert calc.calculate(high_conf) > calc.calculate(low_conf)


# ---------------------------------------------------------------------------
# Test 5: Factor 5 — review_required status = high score
# ---------------------------------------------------------------------------

def test_factor5_review_required(tmp_path):
    calc = SignalGravityL1Calculator(store_path=str(tmp_path))
    review_okp = _make_okp(status="review_required",
                            source_ref="f5-rev", summary="Needs review")
    observed_okp = _make_okp(status="observed",
                              source_ref="f5-obs", summary="Observed")
    assert calc.calculate(review_okp) > calc.calculate(observed_okp)


# ---------------------------------------------------------------------------
# Test 6: Factor 5 — R4 authority level = high score
# ---------------------------------------------------------------------------

def test_factor5_r4_authority(tmp_path):
    calc = SignalGravityL1Calculator(store_path=str(tmp_path))
    r4_okp = _make_okp(authority_level="R4", source_ref="f5-r4", summary="R4 authority")
    r1_okp = _make_okp(authority_level="R1", source_ref="f5-r1", summary="R1 authority")
    assert calc.calculate(r4_okp) > calc.calculate(r1_okp)


# ---------------------------------------------------------------------------
# Test 7: Weight config loads from file
# ---------------------------------------------------------------------------

def test_weights_load_from_file(tmp_path):
    config_path = tmp_path / "signal_gravity_config.json"
    custom_weights = dict(DEFAULT_WEIGHTS)
    custom_weights["operational_value"] = 0.20
    # Adjust another to keep sum=1 (not strictly required for load test)
    config_path.write_text(json.dumps(custom_weights), encoding="utf-8")
    calc = SignalGravityL1Calculator(store_path=str(tmp_path))
    loaded = calc.load_weights()
    assert loaded["operational_value"] == 0.20


# ---------------------------------------------------------------------------
# Test 8: Default config is created when missing
# ---------------------------------------------------------------------------

def test_default_config_created(tmp_path):
    calc = SignalGravityL1Calculator(store_path=str(tmp_path))
    config_path = tmp_path / "signal_gravity_config.json"
    assert not config_path.exists()
    weights = calc.load_weights()
    assert config_path.exists()
    assert weights == DEFAULT_WEIGHTS


# ---------------------------------------------------------------------------
# Test 9: Calibration proposal writes to file
# ---------------------------------------------------------------------------

def test_calibration_proposal_writes_to_file(tmp_path):
    calc = SignalGravityL1Calculator(store_path=str(tmp_path))
    proposal = calc.propose_calibration(
        factor_name="operational_value",
        proposed_weight=0.20,
        rationale="Increase weight based on recent feedback",
    )
    proposals_path = tmp_path / "signal_gravity_calibration_proposals.json"
    assert proposals_path.exists()
    data = json.loads(proposals_path.read_text(encoding="utf-8"))
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["factor_name"] == "operational_value"
    assert data[0]["proposed_weight"] == 0.20
    assert data[0]["proposal_id"].startswith("proposal-")
    assert proposal.factor_name == "operational_value"


# ---------------------------------------------------------------------------
# Tests 10-12: API endpoint tests
# ---------------------------------------------------------------------------

@pytest.fixture()
def api_client(tmp_path):
    """FastAPI test client with API key set and store isolated to tmp_path."""
    os.environ["GAIL_OS_API_KEY"] = "test-key-5.3"
    os.environ["GAIL_OS_STORE_PATH"] = str(tmp_path)
    from fastapi.testclient import TestClient
    # Import the app after env vars are set
    import importlib
    import apps.gail_os_api.main as _main_mod  # may fail; use direct import
    # Use direct path approach
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "apps" / "gail-os-api"))
    # Force reimport to pick up env
    import main as main_mod
    importlib.reload(main_mod)
    client = TestClient(main_mod.app)
    yield client
    del os.environ["GAIL_OS_API_KEY"]


_VALID_OKP_PAYLOAD = {
    "source_system": "test-api",
    "source_ref": "api-test-ref-001",
    "record_type": "evidence.created",
    "summary": "API test OKP summary",
    "authority_level": "R1",
    "autonomy_level": "A1",
    "risk_tier": 2,
    "data_classification": "internal",
    "confidence": 0.75,
}


@pytest.fixture()
def simple_client(tmp_path):
    """Simpler test client using TestClient directly."""
    os.environ["GAIL_OS_API_KEY"] = "test-key-5.3"
    os.environ["GAIL_OS_STORE_PATH"] = str(tmp_path)
    api_path = str(Path(__file__).resolve().parent.parent / "apps" / "gail-os-api")
    if api_path not in sys.path:
        sys.path.insert(0, api_path)
    from fastapi.testclient import TestClient
    import importlib
    import main as main_mod
    importlib.reload(main_mod)
    yield TestClient(main_mod.app)
    del os.environ["GAIL_OS_API_KEY"]


# Test 10: POST /api/v1/okp returns 201 with okp_id and gravity_score_l1
def test_api_post_okp_returns_201(simple_client):
    response = simple_client.post(
        "/api/v1/okp",
        json=_VALID_OKP_PAYLOAD,
        headers={"X-Api-Key": "test-key-5.3"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "okp_id" in data
    assert data["okp_id"].startswith("okp-")
    assert "gravity_score_l1" in data
    assert 0.0 <= data["gravity_score_l1"] <= 1.0
    assert "fingerprint" in data


# Test 11: GET /api/v1/okp/{id} returns 200
def test_api_get_okp_returns_200(simple_client):
    post_resp = simple_client.post(
        "/api/v1/okp",
        json=_VALID_OKP_PAYLOAD,
        headers={"X-Api-Key": "test-key-5.3"},
    )
    assert post_resp.status_code == 201
    okp_id = post_resp.json()["okp_id"]
    get_resp = simple_client.get(
        f"/api/v1/okp/{okp_id}",
        headers={"X-Api-Key": "test-key-5.3"},
    )
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["okp_id"] == okp_id
    assert data["source_system"] == "test-api"


# Test 12: GET /api/v1/okp/missing-id returns 404
def test_api_get_missing_okp_returns_404(simple_client):
    get_resp = simple_client.get(
        "/api/v1/okp/okp-does-not-exist",
        headers={"X-Api-Key": "test-key-5.3"},
    )
    assert get_resp.status_code == 404


# ---------------------------------------------------------------------------
# Test 13: L1 factors 1/2/3/5 produce expected relative scores
# ---------------------------------------------------------------------------

def test_relative_factor_scores(tmp_path):
    """All four L1 factors individually produce a higher score when their
    input is at the high end vs the low end, using fixed weights."""
    calc = SignalGravityL1Calculator(store_path=str(tmp_path))
    now = datetime.now(timezone.utc)

    # Factor 1: recent vs very old
    f1_high = _make_okp(observed_at=now, source_ref="rel-f1h", summary="F1 high")
    f1_low = _make_okp(observed_at=now - timedelta(days=30),
                        source_ref="rel-f1l", summary="F1 low")
    assert calc.calculate(f1_high) > calc.calculate(f1_low)

    # Factor 2: risk_tier 5 vs 1
    f2_high = _make_okp(risk_tier=5, source_ref="rel-f2h", summary="F2 high")
    f2_low = _make_okp(risk_tier=1, source_ref="rel-f2l", summary="F2 low")
    assert calc.calculate(f2_high) > calc.calculate(f2_low)

    # Factor 3: confidence 1.0 vs 0.0
    f3_high = _make_okp(confidence=1.0, source_ref="rel-f3h", summary="F3 high")
    f3_low = _make_okp(confidence=0.0, source_ref="rel-f3l", summary="F3 low")
    assert calc.calculate(f3_high) > calc.calculate(f3_low)

    # Factor 5: review_required vs accepted
    f5_high = _make_okp(status="review_required",
                         source_ref="rel-f5h", summary="F5 high")
    f5_low = _make_okp(status="accepted",
                        source_ref="rel-f5l", summary="F5 low")
    assert calc.calculate(f5_high) > calc.calculate(f5_low)


# ---------------------------------------------------------------------------
# Tests 14-15: invalid calibration + invalid record type via API
# ---------------------------------------------------------------------------

def test_calibration_invalid_factor(tmp_path):
    calc = SignalGravityL1Calculator(store_path=str(tmp_path))
    with pytest.raises(ValueError, match="not a recognised factor"):
        calc.propose_calibration(
            factor_name="nonexistent_factor",
            proposed_weight=0.5,
            rationale="Should fail",
        )


def test_api_invalid_record_type_returns_422(simple_client):
    bad_payload = dict(_VALID_OKP_PAYLOAD)
    bad_payload["record_type"] = "totally.invalid.type"
    resp = simple_client.post(
        "/api/v1/okp",
        json=bad_payload,
        headers={"X-Api-Key": "test-key-5.3"},
    )
    assert resp.status_code == 422
