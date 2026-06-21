from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

from gail_ai_operating_system import (  # noqa: E402
    PermissionGate,
    WORKSPACE_GRAPH_PATH,
    build_graphify_route_status,
    create_mission,
    validate_graphify_handoff_payload,
)


def valid_payload() -> dict:
    return {
        "schema_version": "rev2.graphify-handoff.v1",
        "graph": {
            "path": WORKSPACE_GRAPH_PATH,
            "generated_at": "2026-06-19T18:01:38-06:00",
        },
        "recommendations": [
            {
                "source_recommendation_id": "rec-graphify-001",
                "status": "candidate",
                "title": "Review selected Graphify handoff files",
                "summary": "Graphify points at a bounded routing and validation slice.",
                "evidence": [
                    "Applications/user-ai-operating-system/uaos_agent_spine/graphify_handoff.py",
                    {"source_file": "Applications/user-ai-operating-system/tests/test_graphify_handoff.py"},
                ],
                "confidence": 0.82,
                "risk": "medium",
                "data_classification": "internal",
                "mission_hint": {
                    "approval_level": "A1 local no-network",
                    "files_in_scope": [
                        "packages/uaos-core/src/gail_ai_operating_system/graphify_handoff.py",
                        "tests/test_graphify_handoff.py",
                    ],
                    "non_goals": ["graph upload", "source mutation", "live connector calls"],
                    "stop_triggers": ["graphify_action_execution", "secret_exposure", "client_data_access"],
                },
            }
        ],
    }


class GraphifyHandoffTests(unittest.TestCase):
    def test_route_status_uses_workspace_graph_when_repo_graph_is_missing(self) -> None:
        status = build_graphify_route_status(
            workspace_graph_available=True,
            repo_local_graph_available=False,
            graphify_cli_available=False,
            setup_cli_available=False,
        )

        self.assertEqual(status.status, "workspace-graph-ready")
        self.assertTrue(status.connector_decision.allowed)
        self.assertEqual(status.connector_decision.mode, "dry-run-local-validation")
        self.assertEqual(status.connector_id, "graphify-enhanced-handoff")
        self.assertIn("workspace graph", status.next_step)
        self.assertTrue(all("upload" not in command for command in status.allowed_commands))

    def test_accepts_valid_read_only_handoff_candidate(self) -> None:
        report = validate_graphify_handoff_payload(
            valid_payload(),
            existing_evidence_refs={
                "Applications/user-ai-operating-system/uaos_agent_spine/graphify_handoff.py",
                "Applications/user-ai-operating-system/tests/test_graphify_handoff.py",
            },
        )

        self.assertTrue(report.valid)
        self.assertEqual(report.accepted_count, 1)
        self.assertEqual(report.rejected_count, 0)
        candidate = report.accepted[0]
        self.assertEqual(candidate.source_recommendation_id, "rec-graphify-001")
        self.assertEqual(candidate.risk, "medium")
        self.assertIn("graphify_action_execution", candidate.stop_triggers)

    def test_candidate_becomes_policy_allowed_dry_run_read_action(self) -> None:
        report = validate_graphify_handoff_payload(valid_payload())
        action = report.accepted[0].to_mission_action()
        decision = PermissionGate().evaluate(
            create_mission("Review Graphify handoff candidate", request_id="REQ-GRAPHIFY"),
            action,
        )

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.mode, "dry-run")
        self.assertEqual(action.action_type, "graphify_handoff_read")

    def test_rejects_executed_or_mutating_recommendations(self) -> None:
        payload = valid_payload()
        recommendation = payload["recommendations"][0]
        recommendation["status"] = "executed"
        recommendation["executed_at"] = "2026-06-21T16:00:00-06:00"
        recommendation["proposed_action_text"] = "Run recommendation and mutate source files"

        report = validate_graphify_handoff_payload(payload)

        self.assertEqual(report.accepted_count, 0)
        reasons = " ".join(report.rejected[0].reasons)
        self.assertIn("not executed or approved", reasons)
        self.assertIn("execution, approval, result, or rollback", reasons)
        self.assertIn("implies execution", reasons)

    def test_rejects_missing_current_graph_evidence(self) -> None:
        report = validate_graphify_handoff_payload(
            valid_payload(),
            existing_evidence_refs={"Applications/user-ai-operating-system/uaos_agent_spine/graphify_handoff.py"},
        )

        self.assertEqual(report.accepted_count, 0)
        self.assertIn("evidence refs must exist", report.rejected[0].reasons[0])

    def test_rejects_sensitive_evidence_and_unsafe_scope(self) -> None:
        payload = valid_payload()
        recommendation = payload["recommendations"][0]
        recommendation["evidence"] = ["../.env.master"]
        recommendation["mission_hint"]["files_in_scope"] = ["C:/Users/adamg/.env.master"]

        report = validate_graphify_handoff_payload(payload)

        self.assertEqual(report.accepted_count, 0)
        reasons = " ".join(report.rejected[0].reasons)
        self.assertIn("evidence refs must not include secrets", reasons)
        self.assertIn("files_in_scope must use relative", reasons)

    def test_rejects_high_risk_client_or_live_connector_payload(self) -> None:
        payload = valid_payload()
        recommendation = payload["recommendations"][0]
        recommendation["risk"] = "high"
        recommendation["data_classification"] = "client-controlled"
        recommendation["summary"] = "Use live connector access for client data."

        report = validate_graphify_handoff_payload(payload)

        self.assertEqual(report.accepted_count, 0)
        reasons = " ".join(report.rejected[0].reasons)
        self.assertIn("risk is outside", reasons)
        self.assertIn("data classification", reasons)
        self.assertIn("live connector", reasons)

    def test_rejects_payload_without_recommendations_list(self) -> None:
        report = validate_graphify_handoff_payload(
            {
                "schema_version": "rev2.graphify-handoff.v1",
                "graph": {"path": WORKSPACE_GRAPH_PATH},
                "recommendations": {},
            }
        )

        self.assertEqual(report.accepted_count, 0)
        self.assertIn("recommendations must be a list", report.rejected[0].reasons)

    def test_rejects_graph_upload_or_unapproved_graph_reference(self) -> None:
        payload = valid_payload()
        payload["graph"]["path"] = "/tmp/graphify-upload/out/graph.json"

        report = validate_graphify_handoff_payload(payload)

        self.assertEqual(report.accepted_count, 0)
        self.assertIn("approved workspace graph", report.rejected[0].reasons[0])

    def test_rejects_missing_graphify_stop_trigger(self) -> None:
        payload = valid_payload()
        payload["recommendations"][0]["mission_hint"]["stop_triggers"] = ["secret_exposure"]

        report = validate_graphify_handoff_payload(payload)

        self.assertEqual(report.accepted_count, 0)
        self.assertIn("graphify_action_execution", report.rejected[0].reasons[0])


if __name__ == "__main__":
    unittest.main()
