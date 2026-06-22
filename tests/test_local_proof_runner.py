from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

from gail_ai_operating_system import (  # noqa: E402
    LocalProofError,
    LocalRelayRecordStore,
    run_local_proof,
)


NOW = "2026-06-21T19:57:56-06:00"


class LocalProofRunnerTests(unittest.TestCase):
    def test_runs_complete_local_path_and_persists_validated_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            relay_store_path = Path(tmpdir) / "relay-records.json"

            report = run_local_proof(
                relay_store_path,
                request_id="REQ-PROOF-001",
                observed_at=NOW,
                repo_state_ref="commit-proof-001",
                graph_snapshot_ref="graph-proof-001",
            )

            self.assertTrue(report.completed)
            self.assertEqual(report.request_id, "REQ-PROOF-001")
            self.assertEqual(report.relay_status, "completed")
            self.assertEqual(report.connector_id, "local-device-worker-surfaces")
            self.assertEqual(report.connector_mode, "dry-run-local-validation")
            self.assertEqual(
                [step.name for step in report.steps],
                [
                    "mission_intent",
                    "mission_plan_policy",
                    "connector_registry_dry_run",
                    "relay_record_persistence",
                    "trusted_worker_claim",
                    "validated_evidence_record",
                ],
            )

            store = LocalRelayRecordStore(relay_store_path)
            record = store.get_record(report.envelope_id)
            self.assertIsNotNone(record)
            self.assertEqual(record.status, "completed")
            self.assertEqual(record.accepted_claim_id, report.claim_id)
            self.assertEqual(record.evidence_records[0].evidence_id, report.evidence_id)
            self.assertEqual(record.envelope.relay_transport, "local-file")
            self.assertEqual(record.envelope.worker_connection_mode, "not-started")
            self.assertFalse(record.envelope.live_action_requested)

    def test_report_and_store_payload_stay_reference_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            relay_store_path = Path(tmpdir) / "relay-records.json"

            report = run_local_proof(
                relay_store_path,
                request_id="REQ-PROOF-JSON",
                observed_at=NOW,
            )

            report_json = json.dumps(report.to_dict(), sort_keys=True)
            store_json = relay_store_path.read_text(encoding="utf-8")

            self.assertIn("tests/test_local_proof_runner.py", store_json)
            self.assertIn("local-device-worker-surfaces", report_json)
            for blocked in ("BEGIN PRIVATE KEY", "client_secret", "raw audio", "password=", "api_key="):
                self.assertNotIn(blocked, report_json)
                self.assertNotIn(blocked, store_json)

    def test_stop_triggered_mission_fails_before_relay_record_is_written(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            relay_store_path = Path(tmpdir) / "relay-records.json"

            with self.assertRaises(LocalProofError) as error:
                run_local_proof(
                    relay_store_path,
                    command="Send email after reading Microsoft 365 content.",
                    request_id="REQ-PROOF-STOP",
                    observed_at=NOW,
                )

            self.assertEqual(error.exception.step, "mission_plan_policy")
            self.assertIn("Action matches a Rev 2 stop trigger", " ".join(error.exception.reasons))
            self.assertFalse(relay_store_path.exists())


if __name__ == "__main__":
    unittest.main()
