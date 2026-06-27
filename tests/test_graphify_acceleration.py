"""Tests for the local Graphify acceleration fact contract."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

import gail_ai_operating_system as gail  # noqa: E402
from gail_ai_operating_system.graphify_acceleration import (  # noqa: E402
    GRAPHIFY_ACCELERATION_SCHEMA_VERSION,
    GRAPHIFY_ACCELERATION_SOURCE_SYSTEM,
    GraphifyAccelerationRecord,
    GraphifyAccelerationValidationError,
    GraphifyRelatedEntity,
    validate_graphify_acceleration_record,
)


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

    def test_rejects_wrong_entity_prefixes(self) -> None:
        record = _valid_record(entity_type="authority_envelope", entity_id="action-001")

        reasons = validate_graphify_acceleration_record(record)

        self.assertTrue(any("env-" in reason for reason in reasons))

    def test_rejects_bad_authority_envelope_reference(self) -> None:
        record = _valid_record(authority_envelope_id="bad-envelope")

        reasons = validate_graphify_acceleration_record(record)

        self.assertTrue(any("authority_envelope_id" in reason for reason in reasons))

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

    def test_contract_is_not_exported_from_package_root_before_ga_b6(self) -> None:
        self.assertFalse(hasattr(gail, "GraphifyAccelerationRecord"))


if __name__ == "__main__":
    unittest.main()
