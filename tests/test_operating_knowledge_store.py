"""Tests for OkpStore (Phase 5.3)."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure uaos-core is importable
sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "packages" / "uaos-core" / "src"),
)

from gail_ai_operating_system.operating_knowledge import (
    OkpRecordType,
    create_operating_knowledge_packet,
)
from gail_ai_operating_system.operating_knowledge_store import OkpStore


def _make_okp(**kwargs):
    defaults = dict(
        source_system="test",
        source_ref="test-ref-001",
        record_type=OkpRecordType.EVIDENCE_CREATED,
        summary="Test OKP summary",
        authority_level="R1",
        autonomy_level="A1",
        risk_tier=2,
        data_classification="internal",
        confidence=0.8,
    )
    defaults.update(kwargs)
    return create_operating_knowledge_packet(**defaults)


# ---------------------------------------------------------------------------
# Test 1: save and retrieve roundtrip
# ---------------------------------------------------------------------------

def test_save_and_get_roundtrip(tmp_path):
    store = OkpStore(store_path=str(tmp_path))
    okp = _make_okp()
    okp_id = store.save(okp)
    retrieved = store.get(okp_id)
    assert retrieved is not None
    assert retrieved.okp_id == okp.okp_id
    assert retrieved.summary == okp.summary
    assert retrieved.fingerprint == okp.fingerprint
    assert retrieved.record_type == OkpRecordType.EVIDENCE_CREATED


# ---------------------------------------------------------------------------
# Test 2: list_by_record_type filters correctly
# ---------------------------------------------------------------------------

def test_list_by_record_type(tmp_path):
    store = OkpStore(store_path=str(tmp_path))
    okp1 = _make_okp(source_ref="ref-list-1", summary="Evidence A")
    okp2 = _make_okp(
        source_ref="ref-list-2",
        summary="Build blocker B",
        record_type=OkpRecordType.BUILD_BLOCKER_DETECTED,
    )
    okp3 = _make_okp(source_ref="ref-list-3", summary="Evidence C")
    store.save(okp1)
    store.save(okp2)
    store.save(okp3)
    evidence_okps = store.list_by_record_type("evidence.created")
    assert len(evidence_okps) == 2
    ids = {o.okp_id for o in evidence_okps}
    assert okp1.okp_id in ids
    assert okp3.okp_id in ids
    assert okp2.okp_id not in ids


# ---------------------------------------------------------------------------
# Test 3: fingerprint deduplication marks old OKP as "superseded"
# ---------------------------------------------------------------------------

def test_fingerprint_deduplication(tmp_path):
    store = OkpStore(store_path=str(tmp_path))
    # Two OKPs with identical source_ref + record_type + summary share a fingerprint
    okp1 = _make_okp(source_ref="dup-ref", summary="Duplicate summary")
    okp2 = _make_okp(source_ref="dup-ref", summary="Duplicate summary")
    assert okp1.fingerprint == okp2.fingerprint
    assert okp1.okp_id != okp2.okp_id
    store.save(okp1)
    store.save(okp2)
    # okp1 should now be superseded
    retrieved1 = store.get(okp1.okp_id)
    assert retrieved1 is not None
    assert retrieved1.status == "superseded"
    # okp2 should remain with its original status
    retrieved2 = store.get(okp2.okp_id)
    assert retrieved2 is not None
    assert retrieved2.status == "observed"


# ---------------------------------------------------------------------------
# Test 4: missing ID returns None
# ---------------------------------------------------------------------------

def test_get_missing_returns_none(tmp_path):
    store = OkpStore(store_path=str(tmp_path))
    result = store.get("okp-does-not-exist")
    assert result is None


# ---------------------------------------------------------------------------
# Test 5: store path isolation
# ---------------------------------------------------------------------------

def test_store_path_isolation(tmp_path):
    store_a = OkpStore(store_path=str(tmp_path / "store_a"))
    store_b = OkpStore(store_path=str(tmp_path / "store_b"))
    okp = _make_okp()
    store_a.save(okp)
    # Store B should not see the OKP from Store A
    assert store_b.get(okp.okp_id) is None
    # Store A should still have it
    assert store_a.get(okp.okp_id) is not None
