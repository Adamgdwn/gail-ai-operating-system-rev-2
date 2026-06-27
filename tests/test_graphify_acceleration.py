"""Tests for the local Graphify acceleration fact contract."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

import gail_ai_operating_system as gail  # noqa: E402
from gail_ai_operating_system.action import Action  # noqa: E402
from gail_ai_operating_system.authority_envelope import AuthorityEnvelope  # noqa: E402
from gail_ai_operating_system.evidence_packet import EvidencePacket  # noqa: E402
from gail_ai_operating_system.graphify_acceleration import (  # noqa: E402
    GRAPHIFY_ACCELERATION_SCHEMA_VERSION,
    GRAPHIFY_ACCELERATION_SOURCE_SYSTEM,
    GraphifyAccelerationSafetyCheck,
    GraphifyAccelerationRecord,
    GraphifyAccelerationValidationError,
    GraphifyRelatedEntity,
    build_graphify_action_record,
    build_graphify_authority_envelope_record,
    build_graphify_evidence_record,
    classify_graphify_reference,
    classify_graphify_relationship,
    classify_graphify_summary,
    generate_graphify_acceleration_fingerprint,
    validate_graphify_acceleration_record,
    with_graphify_acceleration_fingerprint,
)
from gail_ai_operating_system.mission import MissionStatus  # noqa: E402


def _valid_record(**overrides: object) -> GraphifyAccelerationRecord:
    defaults: dict[str, object] = {
        "schema_version": GRAPHIFY_ACCELERATION_SCHEMA_VERSION,
        "record_id": "graphify-fact-action-001",
        "source_system": GRAPHIFY_ACCELERATION_SOURCE_SYSTEM,
        "generated_at": "2026-06-27T09:39:31-06:00",
        "operation": "created",
        "entity_type": "action",
        "entity_id": "action-001",
        "entity_version": "1",
        "title": "Create local mission record",
        "summary": "Safe local action fact for future Graphify routing.",
        "authority_level": "R1",
        "risk_tier": 1,
        "authority_envelope_id": None,
        "approval_state": "observed",
        "data_classification": "internal",
        "source_refs": ("packages/uaos-core/src/gail_ai_operating_system/action.py",),
        "evidence_refs": ("tests/test_action.py",),
        "related_entities": (
            GraphifyRelatedEntity(
                relationship="belongs_to",
                entity_type="mission",
                entity_id="mission-abc123",
            ),
        ),
        "stop_triggers": ("graphify_action_execution",),
        "non_goals": ("No Graphify runtime modification", "No live connector access"),
        "contains_raw_payload": False,
        "fingerprint": "sha256-local-action-001",
    }
    defaults.update(overrides)
    return GraphifyAccelerationRecord(**defaults)


def _valid_action(**overrides: object) -> Action:
    defaults: dict[str, object] = {
        "action_id": "action-001",
        "mission_id": "mission-abc123",
        "action_type": "local_mission_record",
        "title": "Create local mission record",
        "actor": "Adam Goodwin",
        "status": MissionStatus.PROPOSED,
        "authority_level": "R1",
        "risk_tier": 1,
        "arguments": {"mode": "dry-run"},
        "created_at": "2026-06-27T10:00:00-06:00",
        "claimed_at": None,
        "executed_at": None,
        "envelope_id": None,
    }
    defaults.update(overrides)
    return Action(**defaults)


def _valid_envelope(**overrides: object) -> AuthorityEnvelope:
    defaults: dict[str, object] = {
        "envelope_id": "env-test-001",
        "mission_id": "mission-abc123",
        "authority_level": "R2",
        "autonomy_level": "A1",
        "domain": "build",
        "granted_by": "Adam Goodwin",
        "granted_at": "2026-06-27T10:00:00-06:00",
        "expires_at": None,
        "allowed_action_types": ("local_mission_record",),
        "max_risk_tier": 2,
        "stop_conditions": ("Scope boundary breach", "Any R3+ action attempt"),
        "rollback_path": "Revert local mission state.",
        "review_cadence": "After each local mission cycle",
        "status": "active",
    }
    defaults.update(overrides)
    return AuthorityEnvelope(**defaults)


def _valid_packet(**overrides: object) -> EvidencePacket:
    defaults: dict[str, object] = {
        "evidence_id": "evidence-test-001",
        "mission_id": "mission-abc123",
        "action_id": "action-001",
        "actor": "Adam Goodwin",
        "action_type": "local_mission_record",
        "authority_basis": "A1 local no-network",
        "result": "success",
        "execution_mode": "dry-run",
        "created_at": "2026-06-27T10:00:00-06:00",
        "envelope_id": None,
        "rollback_note": None,
        "outcome_summary": "Mission record validated with safe local evidence.",
    }
    defaults.update(overrides)
    return EvidencePacket(**defaults)


class GraphifyAccelerationRecordTests(unittest.TestCase):
    def test_valid_record_round_trips_through_dict_and_json(self) -> None:
        record = _valid_record()

        self.assertEqual(validate_graphify_acceleration_record(record), [])

        restored = GraphifyAccelerationRecord.from_dict(record.to_dict())
        self.assertEqual(restored, record)

        restored_from_json = GraphifyAccelerationRecord.from_json(record.to_json())
        self.assertEqual(restored_from_json, record)

    def test_require_valid_raises_safe_validation_error(self) -> None:
        record = _valid_record(record_id="bad-id")

        with self.assertRaises(GraphifyAccelerationValidationError) as context:
            record.require_valid()

        self.assertIn("record_id", " ".join(context.exception.issues))

    def test_rejects_contract_identity_drift(self) -> None:
        record = _valid_record(
            schema_version="rev2.graphify-acceleration.v2",
            source_system="graphify-runtime",
            operation="uploaded",
            entity_type="runtime_adapter",
        )

        reasons = " ".join(validate_graphify_acceleration_record(record))

        self.assertIn("schema_version", reasons)
        self.assertIn("source_system", reasons)
        self.assertIn("operation", reasons)
        self.assertIn("entity_type", reasons)

    def test_rejects_invalid_authority_risk_and_approval_state(self) -> None:
        record = _valid_record(
            authority_level="R9",
            risk_tier=6,
            approval_state="executed_by_graphify",
            data_classification="restricted",
        )

        reasons = " ".join(validate_graphify_acceleration_record(record))

        self.assertIn("authority_level", reasons)
        self.assertIn("risk_tier", reasons)
        self.assertIn("approval_state", reasons)
        self.assertIn("data_classification", reasons)

    def test_rejects_boolean_risk_tier(self) -> None:
        record = _valid_record(risk_tier=True)

        reasons = validate_graphify_acceleration_record(record)

        self.assertTrue(any("risk_tier" in reason for reason in reasons))

    def test_rejects_raw_payload_and_missing_fingerprint(self) -> None:
        record = _valid_record(contains_raw_payload=True, fingerprint="")

        reasons = " ".join(validate_graphify_acceleration_record(record))

        self.assertIn("contains_raw_payload", reasons)
        self.assertIn("fingerprint", reasons)

    def test_rejects_absolute_parent_and_sensitive_refs(self) -> None:
        record = _valid_record(
            source_refs=(
                "C:/Users/adamg/.env.master",
                "../logs/raw-audio/session.wav",
            ),
            evidence_refs=("tmp/live-connector/client-data.json",),
        )

        reasons = " ".join(validate_graphify_acceleration_record(record))

        self.assertIn("source_refs", reasons)
        self.assertIn("evidence_refs", reasons)

    def test_rejects_summary_raw_payload_markers_without_echoing_payload(self) -> None:
        record = _valid_record(summary="raw log marker should never appear")

        reasons = validate_graphify_acceleration_record(record)

        self.assertTrue(any("summary" in reason for reason in reasons))
        self.assertFalse(any("should never appear" in reason for reason in reasons))

    def test_classifies_safe_and_unsafe_summary_text(self) -> None:
        safe = classify_graphify_summary("Safe local fact for routing only.")
        unsafe = classify_graphify_summary("Authorization: Bearer should-never-leak")

        self.assertIsInstance(safe, GraphifyAccelerationSafetyCheck)
        self.assertTrue(safe.accepted)
        self.assertFalse(unsafe.accepted)
        self.assertIn("secret_marker", unsafe.indicators)
        self.assertFalse(any("should-never-leak" in reason for reason in unsafe.reasons))

    def test_rejects_invalid_related_entity_edges(self) -> None:
        record = _valid_record(
            related_entities=(
                GraphifyRelatedEntity(
                    relationship="mutates_source",
                    entity_type="graphify_runtime",
                    entity_id="../graphify-runtime",
                ),
            )
        )

        reasons = " ".join(validate_graphify_acceleration_record(record))

        self.assertIn("relationships", reasons)
        self.assertIn("entity_type", reasons)
        self.assertIn("entity_id", reasons)

    def test_classifies_reference_guard_categories(self) -> None:
        safe = classify_graphify_reference("docs/current-build-pathway.md")
        unsafe_cases = {
            "drive": "C:/Users/adamg/.env.master",
            "parent": "../outside-repo.md",
            "url": "https://example.com/graph.json",
            "generated_graph": "graphify-out/graph.json",
            "log_dump": "tmp/logs/session.log",
            "raw_audio": "recordings/session.wav",
        }

        self.assertTrue(safe.accepted)
        for name, ref in unsafe_cases.items():
            with self.subTest(name=name):
                check = classify_graphify_reference(ref)
                self.assertFalse(check.accepted)
                self.assertTrue(check.reasons)

    def test_classifies_relationship_edges(self) -> None:
        safe = classify_graphify_relationship(
            GraphifyRelatedEntity("belongs_to", "mission", "mission-abc123")
        )
        unsafe = classify_graphify_relationship(
            GraphifyRelatedEntity("mutates_source", "graphify_runtime", "../runtime")
        )

        self.assertTrue(safe.accepted)
        self.assertFalse(unsafe.accepted)
        self.assertIn("unknown_relationship", unsafe.indicators)
        self.assertIn("unknown_entity_type", unsafe.indicators)
        self.assertIn("invalid_entity_id", unsafe.indicators)

    def test_rejects_wrong_entity_prefixes(self) -> None:
        record = _valid_record(entity_type="authority_envelope", entity_id="action-001")

        reasons = validate_graphify_acceleration_record(record)

        self.assertTrue(any("env-" in reason for reason in reasons))

    def test_rejects_bad_authority_envelope_reference(self) -> None:
        record = _valid_record(authority_envelope_id="bad-envelope")

        reasons = validate_graphify_acceleration_record(record)

        self.assertTrue(any("authority_envelope_id" in reason for reason in reasons))

    def test_rejects_generated_graph_logs_and_audio_refs(self) -> None:
        record = _valid_record(
            source_refs=("graphify-out/graph.json", "tmp/logs/session.log"),
            evidence_refs=("recordings/session.wav",),
        )

        reasons = " ".join(validate_graphify_acceleration_record(record))

        self.assertIn("generated graph output", reasons)
        self.assertIn("raw logs", reasons)
        self.assertIn("raw audio", reasons)

    def test_rejects_missing_required_field_from_dict(self) -> None:
        payload = _valid_record().to_dict()
        del payload["fingerprint"]

        with self.assertRaisesRegex(ValueError, "fingerprint"):
            GraphifyAccelerationRecord.from_dict(payload)

    def test_rejects_non_boolean_raw_payload_flag_from_dict(self) -> None:
        payload = _valid_record().to_dict()
        payload["contains_raw_payload"] = "false"

        with self.assertRaisesRegex(ValueError, "contains_raw_payload"):
            GraphifyAccelerationRecord.from_dict(payload)

    def test_rejects_non_string_refs_from_dict(self) -> None:
        payload = _valid_record().to_dict()
        payload["source_refs"] = ["docs/current-build-pathway.md", 123]

        with self.assertRaisesRegex(ValueError, "source_refs"):
            GraphifyAccelerationRecord.from_dict(payload)

    def test_direct_validation_rejects_non_string_values_without_crashing(self) -> None:
        record = _valid_record(
            generated_at=object(),
            title=123,
            source_refs=(object(),),
            related_entities=(
                GraphifyRelatedEntity(
                    relationship=object(),
                    entity_type="mission",
                    entity_id=object(),
                ),
            ),
        )

        reasons = " ".join(validate_graphify_acceleration_record(record))

        self.assertIn("generated_at", reasons)
        self.assertIn("title", reasons)
        self.assertIn("source_refs", reasons)
        self.assertIn("entity_id", reasons)

    def test_fingerprint_generation_is_deterministic_and_excludes_generated_at(self) -> None:
        first = with_graphify_acceleration_fingerprint(
            _valid_record(fingerprint="", generated_at="2026-06-27T10:00:00-06:00")
        )
        second = with_graphify_acceleration_fingerprint(
            _valid_record(fingerprint="", generated_at="2026-06-27T11:00:00-06:00")
        )
        changed = with_graphify_acceleration_fingerprint(
            _valid_record(fingerprint="", summary="Changed safe local summary.")
        )

        self.assertEqual(first.fingerprint, second.fingerprint)
        self.assertNotEqual(first.fingerprint, changed.fingerprint)
        self.assertEqual(generate_graphify_acceleration_fingerprint(first), first.fingerprint)

    def test_fingerprint_changes_for_material_contract_fields(self) -> None:
        baseline = with_graphify_acceleration_fingerprint(_valid_record(fingerprint=""))
        mutations = {
            "entity_id": {"entity_id": "action-002", "record_id": "graphify-fact-action-002"},
            "operation": {"operation": "transitioned"},
            "authority_level": {"authority_level": "R2"},
            "risk_tier": {"risk_tier": 2},
            "approval_state": {"approval_state": "proposed"},
            "source_refs": {"source_refs": ("docs/current-build-pathway.md",)},
            "related_entities": {
                "related_entities": (
                    GraphifyRelatedEntity("depends_on", "mission", "mission-abc123"),
                )
            },
            "non_goals": {"non_goals": ("No transport exposure",)},
        }

        for name, overrides in mutations.items():
            with self.subTest(name=name):
                changed = with_graphify_acceleration_fingerprint(
                    _valid_record(fingerprint="", **overrides)
                )
                self.assertNotEqual(baseline.fingerprint, changed.fingerprint)

    def test_builds_action_authority_and_evidence_records_from_safe_fixtures(self) -> None:
        action_record = build_graphify_action_record(
            _valid_action(),
            source_refs=("tests/test_action.py",),
        )
        authority_record = build_graphify_authority_envelope_record(
            _valid_envelope(),
            source_refs=("tests/test_authority_envelope.py",),
        )
        evidence_record = build_graphify_evidence_record(
            _valid_packet(),
            source_refs=("tests/test_evidence_packet.py",),
            authority_level="R1",
            risk_tier=1,
        )

        for record in (action_record, authority_record, evidence_record):
            with self.subTest(record=record.record_id):
                self.assertEqual(validate_graphify_acceleration_record(record), [])
                self.assertTrue(record.fingerprint.startswith("sha256-"))
                self.assertFalse(record.contains_raw_payload)

        self.assertEqual(action_record.entity_type, "action")
        self.assertEqual(authority_record.entity_type, "authority_envelope")
        self.assertEqual(evidence_record.entity_type, "evidence_packet")
        self.assertEqual(evidence_record.evidence_refs, ("records/evidence/evidence-test-001",))

    def test_emitters_reject_invalid_or_unsafe_source_objects(self) -> None:
        with self.assertRaises(GraphifyAccelerationValidationError):
            build_graphify_action_record(_valid_action(title="password=not-for-graph"))

        with self.assertRaises(GraphifyAccelerationValidationError):
            build_graphify_authority_envelope_record(_valid_envelope(stop_conditions=()))

        with self.assertRaises(GraphifyAccelerationValidationError):
            build_graphify_evidence_record(_valid_packet(execution_mode="live"))

    def test_contract_is_exported_from_package_root_after_ga_b6(self) -> None:
        self.assertIs(gail.GraphifyAccelerationRecord, GraphifyAccelerationRecord)
        self.assertIs(gail.GraphifyAccelerationValidationError, GraphifyAccelerationValidationError)
        self.assertIs(gail.build_graphify_action_record, build_graphify_action_record)
        self.assertIs(gail.with_graphify_acceleration_fingerprint, with_graphify_acceleration_fingerprint)


if __name__ == "__main__":
    unittest.main()
