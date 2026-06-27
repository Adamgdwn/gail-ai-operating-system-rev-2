"""Tests for EvidencePacket schema — auditable record for governed actions."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

from gail_ai_operating_system.evidence_packet import (  # noqa: E402
    EvidencePacket,
    EvidenceResult,
    ExecutionMode,
    create_evidence_packet,
    validate_evidence_packet,
)


def _valid_packet(**overrides: object) -> EvidencePacket:
    defaults: dict = {
        "evidence_id": "evidence-test001234",
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
        "outcome_summary": "Mission record created and validated.",
    }
    defaults.update(overrides)
    return EvidencePacket(**defaults)


class EvidenceResultEnumTests(unittest.TestCase):
    def test_all_result_states_present(self) -> None:
        expected = {"success", "failure", "stopped", "partial"}
        self.assertEqual({r.value for r in EvidenceResult}, expected)

    def test_result_is_string_enum(self) -> None:
        self.assertIsInstance(EvidenceResult.SUCCESS, str)
        self.assertEqual(EvidenceResult.STOPPED, "stopped")


class ExecutionModeEnumTests(unittest.TestCase):
    def test_execution_modes_present(self) -> None:
        expected = {"dry-run", "live"}
        self.assertEqual({m.value for m in ExecutionMode}, expected)

    def test_dry_run_is_default(self) -> None:
        self.assertEqual(ExecutionMode.DRY_RUN.value, "dry-run")


class EvidencePacketSchemaTests(unittest.TestCase):
    def test_packet_has_all_required_fields(self) -> None:
        packet = _valid_packet()
        required_fields = {
            "evidence_id", "mission_id", "action_id", "actor",
            "action_type", "authority_basis", "result", "execution_mode",
            "created_at", "envelope_id", "rollback_note", "outcome_summary",
        }
        packet_dict = packet.to_dict()
        for f in required_fields:
            self.assertIn(f, packet_dict, f"Missing field: {f}")

    def test_packet_round_trips_via_dict(self) -> None:
        original = _valid_packet()
        restored = EvidencePacket.from_dict(original.to_dict())
        self.assertEqual(original, restored)

    def test_packet_with_envelope_id_round_trips(self) -> None:
        original = _valid_packet(envelope_id="env-test-001")
        restored = EvidencePacket.from_dict(original.to_dict())
        self.assertEqual(restored.envelope_id, "env-test-001")

    def test_packet_with_rollback_note_round_trips(self) -> None:
        original = _valid_packet(rollback_note="Revert by deleting the mission record.")
        restored = EvidencePacket.from_dict(original.to_dict())
        self.assertEqual(restored.rollback_note, "Revert by deleting the mission record.")

    def test_packet_without_optional_fields_round_trips(self) -> None:
        original = _valid_packet(envelope_id=None, rollback_note=None)
        restored = EvidencePacket.from_dict(original.to_dict())
        self.assertIsNone(restored.envelope_id)
        self.assertIsNone(restored.rollback_note)


class CreateEvidencePacketTests(unittest.TestCase):
    def test_create_generates_evidence_id_with_prefix(self) -> None:
        packet = create_evidence_packet(
            mission_id="mission-abc123",
            action_id="action-001",
            actor="Adam Goodwin",
            action_type="local_mission_record",
            authority_basis="A1 local no-network",
            result="success",
            created_at="2026-06-27T10:00:00-06:00",
        )
        self.assertTrue(packet.evidence_id.startswith("evidence-"))

    def test_create_defaults_to_dry_run_mode(self) -> None:
        packet = create_evidence_packet(
            mission_id="mission-abc123",
            action_id="action-001",
            actor="Adam Goodwin",
            action_type="local_mission_record",
            authority_basis="A1 local no-network",
            result="success",
            created_at="2026-06-27T10:00:00-06:00",
        )
        self.assertEqual(packet.execution_mode, "dry-run")

    def test_create_rejects_bad_mission_id_prefix(self) -> None:
        with self.assertRaises(ValueError):
            create_evidence_packet(
                mission_id="bad-id",
                action_id="action-001",
                actor="Adam Goodwin",
                action_type="local_mission_record",
                authority_basis="A1 local no-network",
                result="success",
                created_at="2026-06-27T10:00:00-06:00",
            )

    def test_create_rejects_invalid_result(self) -> None:
        with self.assertRaises(ValueError):
            create_evidence_packet(
                mission_id="mission-abc123",
                action_id="action-001",
                actor="Adam Goodwin",
                action_type="local_mission_record",
                authority_basis="A1 local no-network",
                result="unknown_result",
                created_at="2026-06-27T10:00:00-06:00",
            )


class ValidateEvidencePacketTests(unittest.TestCase):
    def test_valid_packet_returns_no_errors(self) -> None:
        errors = validate_evidence_packet(_valid_packet())
        self.assertEqual(errors, [])

    def test_invalid_mission_prefix_returns_error(self) -> None:
        packet = _valid_packet(mission_id="bad-id")
        errors = validate_evidence_packet(packet)
        self.assertTrue(any("mission-" in e for e in errors))

    def test_empty_actor_returns_error(self) -> None:
        packet = _valid_packet(actor="")
        errors = validate_evidence_packet(packet)
        self.assertTrue(any("actor" in e for e in errors))

    def test_invalid_result_returns_error(self) -> None:
        packet = _valid_packet(result="unknown")
        errors = validate_evidence_packet(packet)
        self.assertTrue(any("result" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
