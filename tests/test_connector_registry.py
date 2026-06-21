from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

from gail_ai_operating_system import (  # noqa: E402
    ConnectorOperationRequest,
    ConnectorProfile,
    ConnectorRegistry,
    initial_connector_profiles,
    profiles_from_json,
    profiles_to_json,
    validate_connector_profile,
    validate_connector_registry,
)


class ConnectorRegistryTests(unittest.TestCase):
    def test_initial_connector_profiles_are_valid_and_not_live_enabled(self) -> None:
        profiles = initial_connector_profiles()

        self.assertEqual(
            {profile.connector_id for profile in profiles},
            {
                "github-rev2-private-source",
                "graphify-enhanced-handoff",
                "m365-guided-ai-labs-business",
                "quickbooks-finance-planning-boundary",
                "local-device-worker-surfaces",
                "client-gateway-planning-template",
                "vendor-and-deployment-providers",
            },
        )

        report = validate_connector_registry(profiles)

        self.assertTrue(report.valid, [profile_report.reasons for profile_report in report.profile_reports])
        self.assertFalse(any(profile.live_access_enabled for profile in profiles))
        self.assertLessEqual(
            {capability for profile in profiles for capability in profile.allowed_capabilities},
            {"planning-only", "inventory-only", "metadata-only", "local-validation", "readiness-check"},
        )

    def test_profiles_round_trip_through_json_without_enabling_live_access(self) -> None:
        document = profiles_to_json(initial_connector_profiles())
        parsed = profiles_from_json(document)

        self.assertEqual(json.loads(document), [profile.to_dict() for profile in parsed])
        self.assertTrue(validate_connector_registry(parsed).valid)
        self.assertFalse(any(profile.live_access_enabled for profile in parsed))

    def test_profile_rejects_live_access_and_runtime_capability(self) -> None:
        profile = ConnectorProfile(
            connector_id="m365-live-too-soon",
            display_name="M365 live too soon",
            system_family="Microsoft 365",
            owner="Adam Goodwin",
            tenant_or_workspace="Guided AI Labs tenant",
            current_state="planning-only",
            allowed_capabilities=("content-read",),
            prohibited_capabilities=("send mail",),
            data_classes=("internal",),
            approval_gate="Adam approval required before live access.",
            retention_rule="No raw content retention.",
            audit_requirements=("mission_id", "connector_id", "capability", "result", "stop_reason"),
            stop_triggers=("m365_live_content_read",),
            failure_behavior="Stop on ambiguity.",
            live_access_enabled=True,
        )

        report = validate_connector_profile(profile)
        reasons = " ".join(report.reasons)

        self.assertFalse(report.valid)
        self.assertIn("Live connector access is blocked", reasons)
        self.assertIn("Unsupported or live capabilities", reasons)

    def test_client_controlled_profile_requires_signed_scope_review_and_stop_trigger(self) -> None:
        profile = ConnectorProfile(
            connector_id="client-gateway-too-loose",
            display_name="Loose client gateway",
            system_family="Client Gateway",
            owner="Future client",
            tenant_or_workspace="Future workspace",
            current_state="planning-only",
            allowed_capabilities=("planning-only",),
            prohibited_capabilities=("live access",),
            data_classes=("client-controlled",),
            approval_gate="Client sponsor says yes later.",
            retention_rule="Retention to be decided.",
            audit_requirements=("mission_id", "connector_id", "capability", "result", "stop_reason"),
            stop_triggers=("connector_profile_required",),
            failure_behavior="Stop on ambiguity.",
        )

        report = validate_connector_profile(profile)
        reasons = " ".join(report.reasons)

        self.assertFalse(report.valid)
        self.assertIn("signed scope", reasons)
        self.assertIn("review", reasons)
        self.assertIn("client_data_access", reasons)

    def test_registry_allows_only_local_dry_run_profile_validation(self) -> None:
        registry = ConnectorRegistry()
        request = ConnectorOperationRequest(
            request_id="REQ-CONNECTOR-LOCAL",
            connector_id="local-device-worker-surfaces",
            capability="local-validation",
            data_classification="synthetic",
            dry_run=True,
        )

        decision = registry.evaluate(request)

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.mode, "dry-run-local-validation")
        self.assertIsNone(decision.stop_trigger)
        self.assertIn("no external system", decision.reason)

    def test_registry_denies_live_m365_content_read(self) -> None:
        registry = ConnectorRegistry()
        request = ConnectorOperationRequest(
            request_id="REQ-M365-LIVE",
            connector_id="m365-guided-ai-labs-business",
            capability="content-read",
            data_classification="internal",
            dry_run=True,
        )

        decision = registry.evaluate(request)

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.mode, "stop")
        self.assertEqual(decision.stop_trigger, "m365_live_content_read")

    def test_registry_denies_non_dry_run_requests(self) -> None:
        registry = ConnectorRegistry()
        request = ConnectorOperationRequest(
            request_id="REQ-LIVE",
            connector_id="github-rev2-private-source",
            capability="metadata-only",
            data_classification="internal",
            dry_run=False,
        )

        decision = registry.evaluate(request)

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.mode, "stop")
        self.assertEqual(decision.stop_trigger, "connector_profile_required")
        self.assertIn("Live connector requests are blocked", decision.reason)

    def test_registry_denies_client_controlled_operation_requests_even_when_profile_describes_future_template(self) -> None:
        registry = ConnectorRegistry()
        request = ConnectorOperationRequest(
            request_id="REQ-CLIENT-DATA",
            connector_id="client-gateway-planning-template",
            capability="readiness-check",
            data_classification="client-controlled",
            dry_run=True,
        )

        decision = registry.evaluate(request)

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.mode, "stop")
        self.assertEqual(decision.stop_trigger, "client_data_access")

    def test_registry_denies_unknown_connector_and_default_disallowed_capability(self) -> None:
        registry = ConnectorRegistry()

        unknown = registry.evaluate(
            ConnectorOperationRequest(
                request_id="REQ-UNKNOWN",
                connector_id="m365-not-registered",
                capability="planning-only",
            )
        )
        disallowed = registry.evaluate(
            ConnectorOperationRequest(
                request_id="REQ-DISALLOWED",
                connector_id="quickbooks-finance-planning-boundary",
                capability="local-validation",
            )
        )

        self.assertFalse(unknown.allowed)
        self.assertEqual(unknown.stop_trigger, "connector_profile_required")
        self.assertFalse(disallowed.allowed)
        self.assertEqual(disallowed.stop_trigger, "connector_profile_required")
        self.assertIn("Default deny", disallowed.reason)

    def test_registry_validation_reports_duplicate_connector_ids(self) -> None:
        profile = initial_connector_profiles()[0]
        report = validate_connector_registry((profile, profile))

        self.assertFalse(report.valid)
        self.assertIn("Duplicate connector ID", " ".join(report.reasons))

    def test_non_boolean_json_request_dry_run_is_rejected(self) -> None:
        payload = ConnectorOperationRequest(
            request_id="REQ-BOOL",
            connector_id="github-rev2-private-source",
            capability="metadata-only",
        ).to_dict()
        payload["dry_run"] = "false"

        with self.assertRaises(ValueError):
            ConnectorOperationRequest.from_dict(payload)


if __name__ == "__main__":
    unittest.main()
