"""Tests for Mission schema types — data model shape and MissionStatus enum."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

from gail_ai_operating_system.mission import (  # noqa: E402
    MissionAction,
    MissionEnvelope,
    MissionPlan,
    MissionStatus,
    PolicyDecision,
    create_mission,
    validate_mission,
)


class MissionStatusEnumTests(unittest.TestCase):
    def test_all_state_machine_stages_present(self) -> None:
        expected = {
            "observed", "proposed", "classified", "approval_requested",
            "approved", "rejected", "claimed", "executed", "stopped",
            "evidenced", "reviewed", "learned",
        }
        actual = {s.value for s in MissionStatus}
        self.assertEqual(actual, expected)

    def test_status_is_string_enum(self) -> None:
        self.assertIsInstance(MissionStatus.PROPOSED, str)
        self.assertEqual(MissionStatus.APPROVED, "approved")

    def test_terminal_states_are_distinct_from_active_states(self) -> None:
        terminal = {MissionStatus.APPROVED, MissionStatus.REJECTED, MissionStatus.STOPPED, MissionStatus.LEARNED}
        active = {MissionStatus.PROPOSED, MissionStatus.CLASSIFIED, MissionStatus.CLAIMED, MissionStatus.EXECUTED}
        self.assertFalse(terminal & active)


class MissionEnvelopeSchemaTests(unittest.TestCase):
    def test_mission_envelope_has_required_fields(self) -> None:
        mission = create_mission("Validate schema field coverage", request_id="REQ-SCHEMA-001")
        required_fields = {
            "mission_id", "request_id", "command", "domain",
            "created_at", "owner", "approval_level", "dry_run",
            "data_classification", "status",
        }
        envelope_dict = mission.to_dict()
        for field in required_fields:
            self.assertIn(field, envelope_dict, f"Missing field: {field}")

    def test_mission_envelope_round_trips_via_dict(self) -> None:
        original = create_mission("Round-trip schema test", request_id="REQ-SCHEMA-002")
        restored = MissionEnvelope.from_dict(original.to_dict())
        self.assertEqual(original, restored)

    def test_mission_id_uses_mission_prefix(self) -> None:
        mission = create_mission("Check mission ID prefix", request_id="REQ-SCHEMA-003")
        self.assertTrue(mission.mission_id.startswith("mission-"))

    def test_validate_mission_returns_valid_for_well_formed_envelope(self) -> None:
        mission = create_mission("Valid envelope check", request_id="REQ-SCHEMA-004")
        result = validate_mission(mission)
        self.assertTrue(result.valid)
        self.assertEqual(len(result.issues), 0)


class MissionActionSchemaTests(unittest.TestCase):
    def test_mission_action_has_required_fields(self) -> None:
        action = MissionAction(
            action_id="action-schema-001",
            action_type="local_mission_record",
            title="Schema field test",
        )
        action_dict = action.to_dict()
        for field in {"action_id", "action_type", "title", "arguments", "risk_tier"}:
            self.assertIn(field, action_dict, f"Missing field: {field}")

    def test_mission_action_round_trips_via_dict(self) -> None:
        action = MissionAction(
            action_id="action-schema-002",
            action_type="local_validation_command",
            title="Round-trip action",
            arguments={"command": "pytest"},
            risk_tier=1,
        )
        restored = MissionAction.from_dict(action.to_dict())
        self.assertEqual(action, restored)


class PolicyDecisionSchemaTests(unittest.TestCase):
    def test_policy_decision_has_required_fields(self) -> None:
        decision = PolicyDecision(
            action_id="action-schema-001",
            allowed=True,
            mode="dry-run",
            reason="Schema field coverage test",
        )
        self.assertEqual(decision.action_id, "action-schema-001")
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.mode, "dry-run")
        self.assertIsNone(decision.stop_reason)


if __name__ == "__main__":
    unittest.main()
