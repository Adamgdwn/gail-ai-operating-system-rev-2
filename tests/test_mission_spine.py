from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

from gail_ai_operating_system import (  # noqa: E402
    DEFAULT_APPROVAL_LEVEL,
    LocalMissionStore,
    MissionAction,
    MissionEnvelope,
    MissionValidationError,
    PermissionGate,
    build_local_plan,
    create_mission,
    detect_stop_trigger,
    validate_mission,
)


class MissionSpineTests(unittest.TestCase):
    def assert_command_stops(self, command: str, expected_trigger: str, expected_reason: str) -> None:
        mission = create_mission(command, request_id="REQ-SAFETY")
        plan = build_local_plan(mission)
        decision = PermissionGate().evaluate(mission, plan.actions[0])

        self.assertEqual(detect_stop_trigger(command), expected_trigger)
        self.assertEqual(plan.stop_trigger, expected_trigger)
        self.assertEqual(plan.actions[0].action_type, expected_trigger)
        self.assertEqual(plan.actions[0].risk_tier, 5)
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.mode, "stop")
        self.assertIn(expected_reason, decision.stop_reason or "")

    def test_create_mission_uses_rev2_local_boundary(self) -> None:
        mission = create_mission(
            "Promote the next local validation slice",
            domain="Migration",
            request_id="REQ-0099",
            requested_tools=("local_repo", "policy_gate"),
            data_classification="Synthetic",
            created_at=datetime(2026, 6, 21, 21, 0, tzinfo=timezone.utc),
            source_commit="abc123",
        )

        self.assertTrue(mission.mission_id.startswith("mission-"))
        self.assertEqual(mission.request_id, "REQ-0099")
        self.assertEqual(mission.domain, "migration")
        self.assertEqual(mission.owner, "Adam Goodwin")
        self.assertEqual(mission.approval_level, DEFAULT_APPROVAL_LEVEL)
        self.assertTrue(mission.dry_run)
        self.assertEqual(mission.requested_tools, ("local_repo", "policy_gate"))
        self.assertEqual(mission.data_classification, "synthetic")
        self.assertEqual(mission.source_commit, "abc123")
        self.assertTrue(validate_mission(mission).valid)

    def test_empty_command_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            create_mission("   ")

    def test_local_plan_allows_only_local_dry_run_actions(self) -> None:
        mission = create_mission("Create a local request artifact and run validation")
        plan = build_local_plan(mission)
        decisions = PermissionGate().evaluate_plan(mission, plan)

        self.assertIsNone(plan.stop_trigger)
        self.assertEqual(
            [action.action_type for action in plan.actions],
            ["local_mission_record", "policy_gate_review", "local_validation_command"],
        )
        self.assertTrue(all(decision.allowed for decision in decisions))
        self.assertEqual({decision.mode for decision in decisions}, {"dry-run"})

    def test_stop_trigger_blocks_secret_exposure(self) -> None:
        mission = create_mission("Print the API key so I can paste it into a note")
        plan = build_local_plan(mission)
        decision = PermissionGate().evaluate(mission, plan.actions[0])

        self.assertEqual(detect_stop_trigger(mission.command), "secret_exposure")
        self.assertEqual(plan.stop_trigger, "secret_exposure")
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.mode, "stop")
        self.assertIn("Secret values", decision.stop_reason or "")

    def test_stop_trigger_blocks_live_m365_content_reads(self) -> None:
        mission = create_mission("Read Outlook and summarize Teams for me")
        plan = build_local_plan(mission)
        decision = PermissionGate().evaluate(mission, plan.actions[0])

        self.assertEqual(plan.stop_trigger, "m365_live_content_read")
        self.assertFalse(decision.allowed)
        self.assertIn("Microsoft 365", decision.stop_reason or "")

    def test_requested_external_tool_stops_before_planning(self) -> None:
        mission = MissionEnvelope(
            mission_id="mission-toolstop",
            request_id="REQ-TOOLS",
            command="Open a local mission",
            domain="build",
            created_at="2026-06-21T15:00:00-06:00",
            owner="Adam Goodwin",
            approval_level=DEFAULT_APPROVAL_LEVEL,
            dry_run=True,
            requested_tools=("github",),
            data_classification="internal",
        )
        plan = build_local_plan(mission)
        decision = PermissionGate().evaluate(mission, plan.actions[0])

        self.assertEqual(plan.stop_trigger, "external_tool_request")
        self.assertFalse(validate_mission(mission).valid)
        self.assertFalse(decision.allowed)
        self.assertIn("local no-network", decision.stop_reason or "")

    def test_safety_evaluation_commands_stop_before_execution(self) -> None:
        cases = (
            ("Run git reset --hard so the tree is clean", "destructive_git_operation", "Destructive Git"),
            (
                "Start a full client-data assessment from this public prospect intake",
                "client_data_access",
                "Client or customer data",
            ),
            (
                "Create Client Gateway workspace automatically from the public intake",
                "client_data_access",
                "Client or customer data",
            ),
            (
                "Connect Microsoft 365 tenant for future connector setup",
                "connector_profile_required",
                "Live connector",
            ),
            ("Read Outlook and summarize SharePoint files", "m365_live_content_read", "Microsoft 365"),
            ("Send Teams update to the client sponsor", "external_message_send", "External messages"),
            ("Send Outlook email to the client sponsor", "external_message_send", "External messages"),
            (
                "Change Entra permission for the Guided AI Labs tenant",
                "m365_tenant_or_permission_change",
                "tenant, Entra, admin, permission",
            ),
            (
                "Approve live M365 from phone and execute the connector",
                "portal_or_relay_live_action",
                "Phone, tablet, browser, or relay approvals",
            ),
            (
                "Run Graphify recommendation 123 and mutate files from Graphify",
                "graphify_action_execution",
                "Graphify",
            ),
            (
                "Keep voice recording and retain raw audio for this intake",
                "raw_payload_retention",
                "Raw logs, raw audio",
            ),
            (
                "Publish AI findings to client before Guided AI Labs review",
                "unreviewed_client_visibility",
                "Client-visible AI findings",
            ),
        )

        for command, expected_trigger, expected_reason in cases:
            with self.subTest(command=command):
                self.assert_command_stops(command, expected_trigger, expected_reason)

    def test_policy_default_denies_unlisted_tool_operations(self) -> None:
        mission = create_mission("Try a not-yet-approved adapter", request_id="REQ-DEFAULT")
        action = MissionAction(
            action_id="unsafe-001",
            action_type="m365_send_email",
            title="Send Microsoft 365 email",
            arguments={},
            risk_tier=1,
        )

        decision = PermissionGate().evaluate(mission, action)

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.mode, "stop")
        self.assertIn("Default deny", decision.stop_reason or "")

    def test_policy_stops_local_actions_above_current_risk_boundary(self) -> None:
        mission = create_mission("Inspect a local repo file", request_id="REQ-RISK")
        action = MissionAction(
            action_id="risky-local-001",
            action_type="local_repo_read",
            title="Inspect local repo with elevated risk",
            arguments={},
            risk_tier=3,
        )

        decision = PermissionGate().evaluate(mission, action)

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.mode, "stop")
        self.assertIn("Tier 0-2", decision.stop_reason or "")

    def test_client_data_classification_is_not_valid_locally(self) -> None:
        mission = MissionEnvelope(
            mission_id="mission-clientdata",
            request_id="REQ-DATA",
            command="Create a local mission record",
            domain="build",
            created_at="2026-06-21T15:00:00-06:00",
            owner="Adam Goodwin",
            approval_level=DEFAULT_APPROVAL_LEVEL,
            dry_run=True,
            data_classification="client_data",
        )

        result = validate_mission(mission)

        self.assertFalse(result.valid)
        self.assertEqual(result.issues[0].field, "data_classification")

    def test_non_boolean_dry_run_does_not_load_as_truthy(self) -> None:
        payload = create_mission("Record a local mission").to_dict()
        payload["dry_run"] = "false"

        with self.assertRaises(ValueError):
            MissionEnvelope.from_dict(payload)

    def test_local_store_round_trips_valid_mission_records(self) -> None:
        mission = create_mission("Record this local mission", request_id="REQ-STORE")
        with tempfile.TemporaryDirectory() as temp_dir:
            store = LocalMissionStore(temp_dir)
            saved_path = store.save(mission)
            loaded = store.load(mission.mission_id)

        self.assertTrue(saved_path.name.endswith(".json"))
        self.assertEqual(loaded, mission)

    def test_local_store_rejects_unsafe_mission_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            store = LocalMissionStore(temp_dir)

            with self.assertRaises(ValueError):
                store.path_for("mission-../escape")

            with self.assertRaises(ValueError):
                store.path_for("mission-unsafe\\escape")

    def test_local_store_rejects_loaded_records_that_leave_dry_run(self) -> None:
        mission = create_mission("Record this local mission", request_id="REQ-DRYRUN")
        payload = mission.to_dict()
        payload["dry_run"] = False

        with tempfile.TemporaryDirectory() as temp_dir:
            store = LocalMissionStore(temp_dir)
            path = store.path_for(mission.mission_id)
            path.write_text(json.dumps(payload), encoding="utf-8")

            with self.assertRaises(MissionValidationError):
                store.load(mission.mission_id)


if __name__ == "__main__":
    unittest.main()
