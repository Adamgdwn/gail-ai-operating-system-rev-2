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
    PROJECT_ID,
    SCHEMA_VERSION,
    PermissionGate,
    LocalRelayRecordStore,
    RelayEnvelope,
    RelayEvidenceRecord,
    RelayValidationContext,
    RelayWorkerClaim,
    create_mission,
)


NOW = "2026-06-21T18:32:47-06:00"


def relay_context() -> RelayValidationContext:
    return RelayValidationContext(
        approved_device_ids=(
            "android-phone-001",
            "android-tablet-001",
            "browser-cockpit-001",
            "linux-worker-001",
            "windows-worker-001",
        ),
        known_request_ids=("REQ-0056",),
        known_mission_ids=("mission-0056",),
        current_state_refs={
            "repo_commit": "commit-001",
            "github_issue": "issue-12",
            "graph_snapshot": "graph-etag-001",
        },
        known_graph_snapshot_refs=("graph-etag-001",),
        validated_at=NOW,
    )


def observed_state_refs(**overrides: str) -> dict[str, str]:
    refs = {
        "repo_commit": "commit-001",
        "github_issue": "issue-12",
        "graph_snapshot": "graph-etag-001",
    }
    refs.update(overrides)
    return refs


def valid_envelope(**overrides: object) -> RelayEnvelope:
    fields = {
        "schema_version": SCHEMA_VERSION,
        "envelope_id": "relay-056-android",
        "record_type": "approval",
        "project_id": PROJECT_ID,
        "request_id": "REQ-0056",
        "mission_id": "mission-0056",
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
        "observed_state_refs": observed_state_refs(),
        "safe_summary": {
            "intent": "Approve the local worker claim proof.",
            "source_refs": ["docs/current-build-pathway.md"],
        },
        "evidence_refs": ("docs/current-build-pathway.md", "docs/architecture.md"),
        "relay_status": "approved",
        "relay_transport": "local-file",
        "worker_connection_mode": "not-started",
        "graph_registry_id": "graphify-enhanced-handoff",
        "graph_snapshot_ref": "graph-etag-001",
        "graph_observed_at": NOW,
        "filesystem_scope_refs": ("packages/uaos-core/src/gail_ai_operating_system/relay_store.py",),
        "graphify_handoff_candidate_status": "read-only-candidate",
    }
    fields.update(overrides)
    return RelayEnvelope(**fields)


def worker_claim(**overrides: object) -> RelayWorkerClaim:
    fields = {
        "claim_id": "claim-linux-001",
        "envelope_id": "relay-056-android",
        "mission_id": "mission-0056",
        "worker_device_id": "linux-worker-001",
        "worker_role": "linux_trusted_worker",
        "observed_state_refs": observed_state_refs(),
        "connector_profile_ids": ("github-rev2-private-source",),
        "claimed_at": NOW,
        "requested_capability": "local-validation",
        "evidence_refs": ("docs/current-build-pathway.md",),
    }
    fields.update(overrides)
    return RelayWorkerClaim(**fields)


def evidence_record(**overrides: object) -> RelayEvidenceRecord:
    fields = {
        "evidence_id": "evidence-001",
        "envelope_id": "relay-056-android",
        "mission_id": "mission-0056",
        "recorder_device_id": "linux-worker-001",
        "recorder_role": "linux_trusted_worker",
        "recorded_at": NOW,
        "safe_summary": {"result": "Local claim proof passed.", "checks": ["unit tests"]},
        "evidence_refs": ("docs/current-build-pathway.md", "tests/test_relay_store.py"),
        "observed_state_refs": observed_state_refs(),
    }
    fields.update(overrides)
    return RelayEvidenceRecord(**fields)


class RelayStoreTests(unittest.TestCase):
    def test_persists_validated_android_approval_record_and_reload(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "relay-records.json"
            store = LocalRelayRecordStore(path, context=relay_context())

            report = store.add_envelope(valid_envelope(), observed_at=NOW)

            self.assertTrue(report.accepted, report.reasons)
            reloaded = LocalRelayRecordStore(path, context=relay_context())
            record = reloaded.get_record("relay-056-android")
            self.assertIsNotNone(record)
            self.assertEqual(record.status, "approved")
            self.assertEqual(record.envelope.graph_snapshot_ref, "graph-etag-001")
            self.assertEqual(record.status_history[0].observed_state_refs["repo_commit"], "commit-001")

    def test_linux_worker_claims_mission_once_and_persists_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "relay-records.json"
            store = LocalRelayRecordStore(path, context=relay_context())
            store.add_envelope(valid_envelope(), observed_at=NOW)

            report = store.claim_worker(worker_claim())

            self.assertTrue(report.accepted, report.reasons)
            record = store.get_record("relay-056-android")
            self.assertEqual(record.status, "claimed")
            self.assertEqual(record.accepted_claim_id, "claim-linux-001")
            self.assertEqual(record.status_history[-1].status, "claimed")
            self.assertEqual(record.status_history[-1].observed_state_refs["repo_commit"], "commit-001")

            reloaded = LocalRelayRecordStore(path, context=relay_context())
            record = reloaded.get_record("relay-056-android")
            self.assertEqual(record.claim_attempts[0].worker_role, "linux_trusted_worker")

    def test_policy_gate_allows_worker_claim_validation_as_dry_run_only(self) -> None:
        mission = create_mission("Validate a relay worker claim", request_id="REQ-0056")

        decision = PermissionGate().evaluate(mission, worker_claim().to_mission_action())

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.mode, "dry-run")

    def test_rejects_second_trusted_worker_claim_for_same_mission(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = LocalRelayRecordStore(Path(tmpdir) / "relay-records.json", context=relay_context())
            store.add_envelope(valid_envelope(), observed_at=NOW)
            first = store.claim_worker(worker_claim())

            second = store.claim_worker(
                worker_claim(
                    claim_id="claim-windows-001",
                    worker_device_id="windows-worker-001",
                    worker_role="windows_trusted_worker",
                )
            )

            self.assertTrue(first.accepted, first.reasons)
            self.assertFalse(second.accepted)
            reasons = " ".join(second.reasons)
            self.assertIn("relay record is not claimable", reasons)
            self.assertIn("mission already has an accepted trusted-worker claim", reasons)
            record = store.get_record("relay-056-android")
            self.assertEqual(len(record.claim_attempts), 2)
            self.assertEqual(record.accepted_claim_id, "claim-linux-001")

    def test_tablet_and_browser_approvals_can_be_claimed_by_windows_or_linux_workers(self) -> None:
        scenarios = (
            (
                valid_envelope(
                    envelope_id="relay-tablet",
                    device_id="android-tablet-001",
                    device_role="android_tablet_cockpit",
                ),
                worker_claim(
                    claim_id="claim-windows-tablet",
                    envelope_id="relay-tablet",
                    worker_device_id="windows-worker-001",
                    worker_role="windows_trusted_worker",
                ),
            ),
            (
                valid_envelope(
                    envelope_id="relay-browser",
                    device_id="browser-cockpit-001",
                    device_role="browser_cockpit",
                ),
                worker_claim(claim_id="claim-linux-browser", envelope_id="relay-browser"),
            ),
        )

        for envelope, claim in scenarios:
            with self.subTest(envelope=envelope.envelope_id):
                with tempfile.TemporaryDirectory() as tmpdir:
                    store = LocalRelayRecordStore(Path(tmpdir) / "relay-records.json", context=relay_context())
                    add_report = store.add_envelope(envelope, observed_at=NOW)
                    claim_report = store.claim_worker(claim)

                    self.assertTrue(add_report.accepted, add_report.reasons)
                    self.assertTrue(claim_report.accepted, claim_report.reasons)

    def test_rejects_claim_when_envelope_state_is_stale_against_authoritative_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            context = relay_context()
            store = LocalRelayRecordStore(Path(tmpdir) / "relay-records.json", context=context)
            store.add_envelope(valid_envelope(), observed_at=NOW)

            new_context = RelayValidationContext(
                approved_device_ids=context.approved_device_ids,
                known_request_ids=context.known_request_ids,
                known_mission_ids=context.known_mission_ids,
                current_state_refs=observed_state_refs(repo_commit="commit-002"),
                known_graph_snapshot_refs=context.known_graph_snapshot_refs,
                validated_at=NOW,
            )
            report = store.claim_worker(worker_claim(), context=new_context)

            self.assertFalse(report.accepted)
            reasons = " ".join(report.reasons)
            self.assertIn("observed_state_refs are stale: repo_commit", reasons)
            self.assertIn("worker claim observed_state_refs are stale: repo_commit", reasons)

    def test_rejects_superseded_or_conflicted_record_before_worker_claim(self) -> None:
        for status in ("superseded", "conflicted"):
            with self.subTest(status=status):
                with tempfile.TemporaryDirectory() as tmpdir:
                    store = LocalRelayRecordStore(Path(tmpdir) / "relay-records.json", context=relay_context())
                    store.add_envelope(valid_envelope(), observed_at=NOW)
                    status_report = store.update_status(
                        "relay-056-android",
                        status,
                        changed_at=NOW,
                        reason=f"{status} local record exists",
                        observed_state_refs=observed_state_refs(),
                    )

                    claim_report = store.claim_worker(worker_claim())

                    self.assertTrue(status_report.accepted, status_report.reasons)
                    self.assertFalse(claim_report.accepted)
                    self.assertIn("relay record is not claimable", " ".join(claim_report.reasons))

    def test_rejects_unknown_worker_device_untrusted_role_unknown_connector_and_live_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = LocalRelayRecordStore(Path(tmpdir) / "relay-records.json", context=relay_context())
            store.add_envelope(valid_envelope(), observed_at=NOW)

            report = store.claim_worker(
                worker_claim(
                    worker_device_id="unapproved-worker",
                    worker_role="android_phone_cockpit",
                    connector_profile_ids=("unknown-connector",),
                    requested_capability="execute-after-approval",
                )
            )

            self.assertFalse(report.accepted)
            reasons = " ".join(report.reasons)
            self.assertIn("worker_role must be a trusted Linux or Windows worker", reasons)
            self.assertIn("worker_device_id is not in the approved device list", reasons)
            self.assertIn("worker claim connector_profile_ids exceed", reasons)
            self.assertIn("unknown connector_profile_ids: unknown-connector", reasons)
            self.assertIn("requested_capability must remain local validation", reasons)

    def test_rejects_unsafe_envelope_payloads_before_persistence(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "relay-records.json"
            store = LocalRelayRecordStore(path, context=relay_context())

            report = store.add_envelope(
                valid_envelope(
                    safe_summary={"intent": "approve", "raw_logs": ["synthetic redacted log"]},
                    raw_audio_retained=True,
                ),
                observed_at=NOW,
            )

            self.assertFalse(report.accepted)
            self.assertFalse(path.exists())
            self.assertIn("safe_summary must not include raw secrets", " ".join(report.reasons))

    def test_evidence_record_persists_safe_references_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "relay-records.json"
            store = LocalRelayRecordStore(path, context=relay_context())
            store.add_envelope(valid_envelope(), observed_at=NOW)
            store.claim_worker(worker_claim())

            report = store.add_evidence(evidence_record())

            self.assertTrue(report.accepted, report.reasons)
            reloaded = LocalRelayRecordStore(path, context=relay_context())
            record = reloaded.get_record("relay-056-android")
            self.assertEqual(record.evidence_records[0].evidence_id, "evidence-001")
            self.assertEqual(record.evidence_records[0].evidence_refs[-1], "tests/test_relay_store.py")

    def test_rejects_unsafe_or_stale_evidence_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            store = LocalRelayRecordStore(Path(tmpdir) / "relay-records.json", context=relay_context())
            store.add_envelope(valid_envelope(), observed_at=NOW)

            report = store.add_evidence(
                evidence_record(
                    recorder_device_id="unknown-worker",
                    safe_summary={"raw_log": "raw command output"},
                    evidence_refs=("C:/Users/adamg/.env.master",),
                    observed_state_refs=observed_state_refs(repo_commit="commit-000"),
                )
            )

            self.assertFalse(report.accepted)
            reasons = " ".join(report.reasons)
            self.assertIn("recorder_device_id is not in the approved device list", reasons)
            self.assertIn("evidence_refs must be relative", reasons)
            self.assertIn("safe_summary must not include raw secrets", reasons)
            self.assertIn("evidence observed_state_refs are stale: repo_commit", reasons)

    def test_relay_payload_file_stays_reference_based(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "relay-records.json"
            store = LocalRelayRecordStore(path, context=relay_context())
            store.add_envelope(valid_envelope(), observed_at=NOW)
            store.claim_worker(worker_claim())
            store.add_evidence(evidence_record())

            payload = json.loads(path.read_text(encoding="utf-8"))
            serialized = json.dumps(payload)

            self.assertIn("graph-etag-001", serialized)
            self.assertIn("docs/current-build-pathway.md", serialized)
            self.assertIn("tests/test_relay_store.py", serialized)
            self.assertNotIn("audio_blob", serialized)
            self.assertNotIn("raw audio bytes", serialized)
            self.assertNotIn("client_secret", serialized)
            self.assertNotIn("BEGIN PRIVATE KEY", serialized)


if __name__ == "__main__":
    unittest.main()
