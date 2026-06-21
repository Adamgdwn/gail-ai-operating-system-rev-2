from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

from gail_ai_operating_system import (  # noqa: E402
    PROJECT_ID,
    SCHEMA_VERSION,
    PermissionGate,
    RelayEnvelope,
    RelayValidationContext,
    create_mission,
    validate_relay_envelope,
)


def valid_envelope(**overrides: object) -> RelayEnvelope:
    fields = {
        "schema_version": SCHEMA_VERSION,
        "envelope_id": "relay-001",
        "record_type": "approval",
        "project_id": PROJECT_ID,
        "request_id": "REQ-RELAY-001",
        "mission_id": "mission-relay-001",
        "actor_id": "adam",
        "device_id": "android-phone-001",
        "device_role": "android_phone_cockpit",
        "approval_level": "A2",
        "requested_capability": "approval",
        "connector_profile_ids": ("github-rev2-private-source", "graphify-enhanced-handoff"),
        "stop_triggers": (
            "portal_or_relay_live_action",
            "hosted_relay_or_worker_action",
            "secret_exposure",
            "client_data_access",
            "raw_payload_retention",
            "graphify_action_execution",
        ),
        "observed_state_refs": {
            "repo_commit": "abc123",
            "request": "REQ-RELAY-001",
            "mission": "mission-relay-001",
            "graph_snapshot": "graph-etag-001",
        },
        "safe_summary": {
            "intent": "Approve the next local validation step.",
            "evidence_refs": ["docs/architecture.md"],
        },
        "evidence_refs": ("docs/architecture.md", "docs/tool-permission-matrix.md"),
        "relay_transport": "local-file",
        "worker_connection_mode": "not-started",
        "graph_registry_id": "graphify-enhanced-handoff",
        "graph_snapshot_ref": "graph-etag-001",
        "graph_observed_at": "2026-06-21T17:04:13-06:00",
        "filesystem_scope_refs": ("packages/uaos-core/src/gail_ai_operating_system/relay_envelope.py",),
        "graphify_handoff_candidate_status": "read-only-candidate",
    }
    fields.update(overrides)
    return RelayEnvelope(**fields)


class RelayEnvelopeTests(unittest.TestCase):
    def test_valid_phone_envelope_accepts_safe_references_only(self) -> None:
        context = RelayValidationContext(
            approved_device_ids=("android-phone-001",),
            known_request_ids=("REQ-RELAY-001",),
            known_mission_ids=("mission-relay-001",),
            current_state_refs={
                "repo_commit": "abc123",
                "request": "REQ-RELAY-001",
                "mission": "mission-relay-001",
                "graph_snapshot": "graph-etag-001",
            },
            known_graph_snapshot_refs=("graph-etag-001",),
            validated_at="2026-06-21T17:04:13-06:00",
        )

        report = validate_relay_envelope(valid_envelope(), context=context)

        self.assertTrue(report.valid, report.reasons)
        self.assertEqual(report.reasons, ())
        self.assertIsNotNone(report.mission_action)
        self.assertEqual(report.mission_action.action_type, "relay_envelope_validate")
        self.assertEqual(report.mission_action.arguments["relay_transport"], "local-file")

    def test_policy_allows_relay_envelope_validation_as_dry_run_only(self) -> None:
        report = validate_relay_envelope(valid_envelope())
        mission = create_mission("Validate a local relay envelope", request_id="REQ-RELAY-001")

        decision = PermissionGate().evaluate(mission, report.mission_action)

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.mode, "dry-run")

    def test_round_trips_schema_without_enabling_live_transport(self) -> None:
        payload = valid_envelope().to_dict()
        parsed = RelayEnvelope.from_dict(payload)

        self.assertEqual(parsed.to_dict(), payload)
        report = validate_relay_envelope(parsed)
        self.assertTrue(report.valid, report.reasons)

    def test_rejects_malformed_json_shapes(self) -> None:
        payload = valid_envelope().to_dict()
        payload["connector_profile_ids"] = "github-rev2-private-source"

        with self.assertRaises(ValueError):
            RelayEnvelope.from_dict(payload)

        payload = valid_envelope().to_dict()
        payload["live_action_requested"] = "false"

        with self.assertRaises(ValueError):
            RelayEnvelope.from_dict(payload)

    def test_rejects_raw_secret_log_audio_client_payloads_and_absolute_filesystem_refs(self) -> None:
        report = validate_relay_envelope(
            valid_envelope(
                safe_summary={
                    "intent": "Approve step",
                    "secret_value": "token: do-not-store-this",
                    "raw_log": "raw command output",
                },
                raw_audio_retained=True,
                contains_client_data_full_payload=True,
                evidence_refs=("docs/architecture.md", "C:/Users/adamg/.env.master"),
                filesystem_scope_refs=("/home/adamgoodwin/code/private", "../outside"),
            )
        )

        self.assertFalse(report.valid)
        reasons = " ".join(report.reasons)
        self.assertIn("safe_summary must not include raw secrets", reasons)
        self.assertIn("must not retain raw audio", reasons)
        self.assertIn("must not carry client-data-full", reasons)
        self.assertIn("evidence_refs must be relative", reasons)
        self.assertIn("filesystem_scope_refs must be relative", reasons)

    def test_rejects_stale_superseded_conflicting_and_unknown_device_records(self) -> None:
        report = validate_relay_envelope(
            valid_envelope(
                device_id="unknown-phone",
                device_role="random_device",
                relay_status="superseded",
                superseded_by_envelope_id="relay-002",
                conflict_markers=("android-phone-001 approved a different state",),
                approval_expires_at="2026-06-21T16:00:00-06:00",
            ),
            context=RelayValidationContext(
                approved_device_ids=("android-phone-001",),
                current_state_refs={"repo_commit": "newer-commit", "graph_snapshot": "graph-etag-001"},
                validated_at="2026-06-21T17:04:13-06:00",
            ),
        )

        self.assertFalse(report.valid)
        reasons = " ".join(report.reasons)
        self.assertIn("device_role is not approved", reasons)
        self.assertIn("device_id is not in the approved device list", reasons)
        self.assertIn("relay_status must be active", reasons)
        self.assertIn("superseded relay envelopes", reasons)
        self.assertIn("conflicting relay envelopes", reasons)
        self.assertIn("observed_state_refs are stale: repo_commit", reasons)
        self.assertIn("approval is stale or expired", reasons)

    def test_rejects_unknown_connector_and_unapproved_live_actions(self) -> None:
        report = validate_relay_envelope(
            valid_envelope(
                connector_profile_ids=("github-rev2-private-source", "unknown-stack"),
                requested_capability="execute-after-approval",
                live_action_requested=True,
            )
        )

        self.assertFalse(report.valid)
        reasons = " ".join(report.reasons)
        self.assertIn("unknown connector_profile_ids: unknown-stack", reasons)
        self.assertIn("live relay actions require", reasons)

    def test_rejects_phone_approval_above_boundary(self) -> None:
        report = validate_relay_envelope(valid_envelope(approval_level="A3"))

        self.assertFalse(report.valid)
        self.assertIn("android_phone_cockpit cannot approve above A2", " ".join(report.reasons))

    def test_rejects_hosted_relay_or_active_worker_polling(self) -> None:
        report = validate_relay_envelope(
            valid_envelope(
                relay_transport="hosted-relay",
                worker_connection_mode="outbound-poll",
            )
        )

        self.assertFalse(report.valid)
        reasons = " ".join(report.reasons)
        self.assertIn("relay_transport must remain local-file", reasons)
        self.assertIn("cannot start polling", reasons)

    def test_rejects_graphify_execution_status_and_missing_stop_trigger(self) -> None:
        triggers = tuple(
            trigger for trigger in valid_envelope().stop_triggers if trigger != "graphify_action_execution"
        )
        report = validate_relay_envelope(
            valid_envelope(
                graphify_handoff_candidate_status="execute-queued-action",
                stop_triggers=triggers,
            )
        )

        self.assertFalse(report.valid)
        reasons = " ".join(report.reasons)
        self.assertIn("Graphify relay envelopes must include graphify_action_execution", reasons)
        self.assertIn("Graphify handoff status must remain read-only", reasons)

    def test_rejects_m365_beyond_planning_only(self) -> None:
        report = validate_relay_envelope(
            valid_envelope(
                connector_profile_ids=("m365-guided-ai-labs-business",),
                requested_capability="content-read",
                live_action_requested=True,
                stop_triggers=(
                    "portal_or_relay_live_action",
                    "hosted_relay_or_worker_action",
                    "secret_exposure",
                    "client_data_access",
                    "raw_payload_retention",
                ),
            )
        )

        self.assertFalse(report.valid)
        reasons = " ".join(report.reasons)
        self.assertIn("Microsoft 365 remains planning-only", reasons)
        self.assertIn("live relay actions require", reasons)

    def test_rejects_client_gateway_full_assessment_stage(self) -> None:
        report = validate_relay_envelope(
            valid_envelope(
                connector_profile_ids=("client-gateway-planning-template",),
                client_gateway_lifecycle_stage="full_assessment",
                stop_triggers=(
                    "portal_or_relay_live_action",
                    "hosted_relay_or_worker_action",
                    "secret_exposure",
                    "client_data_access",
                    "raw_payload_retention",
                ),
            )
        )

        self.assertFalse(report.valid)
        self.assertIn("Client Gateway assessment stages require", " ".join(report.reasons))

    def test_requires_graph_reference_evidence_and_stop_triggers(self) -> None:
        report = validate_relay_envelope(
            valid_envelope(
                graph_registry_id="",
                graph_snapshot_ref="",
                evidence_refs=(),
                stop_triggers=(),
            )
        )

        self.assertFalse(report.valid)
        reasons = " ".join(report.reasons)
        self.assertIn("graph_registry_id or graph_snapshot_ref is required", reasons)
        self.assertIn("evidence_refs must include", reasons)
        self.assertIn("stop_triggers must be shown", reasons)

    def test_rejects_wrong_project_or_record_type(self) -> None:
        report = validate_relay_envelope(
            valid_envelope(
                project_id="uaos-v1",
                record_type="worker-command",
                schema_version="rev1.relay-envelope.v1",
            )
        )

        self.assertFalse(report.valid)
        reasons = " ".join(report.reasons)
        self.assertIn("schema_version must be", reasons)
        self.assertIn("record_type must be", reasons)
        self.assertIn("project_id must be", reasons)


if __name__ == "__main__":
    unittest.main()
