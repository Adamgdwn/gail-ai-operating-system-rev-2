"""Tests for the shared read model and CNS trace spine."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

from gail_ai_operating_system.evidence_packet import create_evidence_packet  # noqa: E402
from gail_ai_operating_system.evidence_store import save_evidence_packet  # noqa: E402
from gail_ai_operating_system.mission_spine import LocalMissionStore, create_mission  # noqa: E402
from gail_ai_operating_system.read_model import (  # noqa: E402
    FREEDOM_RELATIONSHIP_BRIEF_SCHEMA_VERSION,
    LocalTraceEventStore,
    build_freedom_relationship_brief,
    build_trace_read_model,
    create_trace_event,
    validate_trace_event,
)
from gail_ai_operating_system.trace_identity import create_cns_trace_id, validate_cns_trace_id  # noqa: E402


TRACE_ID = "cns-20260701-abc123def456"
NOW = "2026-07-01T12:00:00Z"


def test_create_cns_trace_id_uses_safe_contract():
    trace_id = create_cns_trace_id()
    assert trace_id.startswith("cns-")
    assert validate_cns_trace_id(trace_id, required=True) == []


def test_trace_event_store_round_trips_event(tmp_path):
    store = LocalTraceEventStore(tmp_path / "trace-events")
    event = create_trace_event(
        cns_trace_id=TRACE_ID,
        event_type="mission.created",
        occurred_at=NOW,
        source_system="gail-os-api",
        source_ref="api/v1/missions/mission-test001",
        summary="Mission record created and persisted.",
        mission_id="mission-test001",
        status="draft",
        idempotency_key="mission:REQ-TRACE-001",
    )

    store.save(event)

    loaded = store.read(event.event_id)
    assert loaded == event
    assert validate_trace_event(loaded) == []


def test_trace_event_duplicate_marker_is_detectable(tmp_path):
    store = LocalTraceEventStore(tmp_path / "trace-events")
    first = create_trace_event(
        cns_trace_id=TRACE_ID,
        event_type="mission.created",
        occurred_at="2026-07-01T12:00:00Z",
        source_system="gail-os-api",
        source_ref="api/v1/missions/mission-first001",
        summary="Mission record created and persisted.",
        mission_id="mission-first001",
        idempotency_key="mission:REQ-DUPE",
    )
    store.save(first)
    duplicate_of = store.find_first_by_idempotency_key("mission:REQ-DUPE")
    assert duplicate_of is not None
    second = create_trace_event(
        cns_trace_id=TRACE_ID,
        event_type="mission.created",
        occurred_at="2026-07-01T12:01:00Z",
        source_system="gail-os-api",
        source_ref="api/v1/missions/mission-second001",
        summary="Mission record created and persisted.",
        mission_id="mission-second001",
        idempotency_key="mission:REQ-DUPE",
        duplicate_of_event_id=duplicate_of.event_id,
    )
    store.save(second)

    events = store.find_by_trace(TRACE_ID)
    assert [event.duplicate_detected for event in events] == [False, True]
    assert events[1].duplicate_of_event_id == first.event_id


def test_trace_read_model_collects_events_missions_and_evidence(tmp_path):
    mission = create_mission("Trace a local mission", request_id="REQ-TRACE-READ", cns_trace_id=TRACE_ID)
    LocalMissionStore(tmp_path / "missions").save(mission)
    packet = create_evidence_packet(
        mission_id=mission.mission_id,
        action_id="action-trace-read",
        actor="test-actor",
        action_type="local_mission_record",
        authority_basis="R0 local dry-run",
        result="success",
        created_at=NOW,
        cns_trace_id=TRACE_ID,
    )
    save_evidence_packet(packet, store_path=tmp_path / "evidence")
    store = LocalTraceEventStore(tmp_path / "trace-events")
    store.save(
        create_trace_event(
            cns_trace_id=TRACE_ID,
            event_type="evidence.recorded",
            occurred_at=NOW,
            source_system="gail-os-api",
            source_ref=f"api/v1/evidence/{packet.evidence_id}",
            summary="Evidence packet recorded.",
            mission_id=mission.mission_id,
            action_id=packet.action_id,
            evidence_id=packet.evidence_id,
            status=packet.result,
        )
    )

    read_model = build_trace_read_model(TRACE_ID, store_root=tmp_path)

    assert read_model["found"] is True
    assert mission.mission_id in read_model["mission_ids"]
    assert packet.action_id in read_model["action_ids"]
    assert packet.evidence_id in read_model["evidence_ids"]
    assert read_model["mission_refs"][0]["request_id"] == "REQ-TRACE-READ"
    assert read_model["evidence_refs"][0]["cns_trace_id"] == TRACE_ID


def test_freedom_relationship_brief_summarizes_trace_without_execution_authority(tmp_path, monkeypatch):
    monkeypatch.delenv("AZURE_CLIENT_SECRET", raising=False)
    mission = create_mission("Brief a local mission", request_id="REQ-FREEDOM-BRIEF", cns_trace_id=TRACE_ID)
    LocalMissionStore(tmp_path / "missions").save(mission)
    packet = create_evidence_packet(
        mission_id=mission.mission_id,
        action_id="action-freedom-brief",
        actor="test-actor",
        action_type="local_mission_record",
        authority_basis="R0 local dry-run",
        result="success",
        created_at=NOW,
        cns_trace_id=TRACE_ID,
    )
    save_evidence_packet(packet, store_path=tmp_path / "evidence")
    store = LocalTraceEventStore(tmp_path / "trace-events")
    store.save(
        create_trace_event(
            cns_trace_id=TRACE_ID,
            event_type="evidence.recorded",
            occurred_at=NOW,
            source_system="gail-os-api",
            source_ref=f"api/v1/evidence/{packet.evidence_id}",
            summary="Evidence packet recorded.",
            mission_id=mission.mission_id,
            action_id=packet.action_id,
            evidence_id=packet.evidence_id,
            status=packet.result,
            risk_tier=1,
        )
    )
    store.save(
        create_trace_event(
            cns_trace_id=TRACE_ID,
            event_type="graphify.fact_candidate_prepared",
            occurred_at="2026-07-01T12:01:00Z",
            source_system="gail-os-api",
            source_ref=f"graphify-preview/{packet.evidence_id}",
            summary="Local Graphify fact candidate prepared.",
            mission_id=mission.mission_id,
            evidence_id=packet.evidence_id,
            status="preview",
            metadata={"graphify_record_id": f"graphify-fact-{packet.evidence_id}"},
        )
    )

    brief = build_freedom_relationship_brief(
        TRACE_ID,
        store_root=tmp_path,
        generated_at="2026-07-01T12:05:00Z",
    )

    assert brief["schema_version"] == FREEDOM_RELATIONSHIP_BRIEF_SCHEMA_VERSION
    assert brief["found"] is True
    assert brief["data_state"] == "ready"
    assert brief["mission_snapshot"]["current_mission_id"] == mission.mission_id
    assert brief["evidence_snapshot"]["evidence_count"] == 1
    assert brief["event_snapshot"]["by_event_type"]["graphify.fact_candidate_prepared"] == 1
    assert brief["authority_snapshot"]["highest_observed_risk_tier"] == 1
    assert brief["connector_state"]["live_access_enabled"] is False
    assert brief["connector_state"]["m365"]["app_only_profile_state"] == "future-only-unprovisioned"
    assert brief["graph_context_state"] == "local_fact_candidates"
    assert brief["graph_context_refs"][0]["authority"] == "non_authoritative_context_only"
    assert brief["execution_authority"]["granted"] is False


def test_freedom_relationship_brief_reports_not_found_explicitly(tmp_path):
    brief = build_freedom_relationship_brief(
        TRACE_ID,
        store_root=tmp_path,
        generated_at="2026-07-01T12:05:00Z",
    )

    assert brief["found"] is False
    assert brief["data_state"] == "not_found"
    assert brief["failure_semantics"]["not_found"]["found"] is False
    assert brief["failure_semantics"]["retry"]["recommended"] is True
    assert brief["relationship_map"]["mission_ids"] == []
