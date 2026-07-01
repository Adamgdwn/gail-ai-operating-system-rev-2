"""Tests for package-level public schema exports."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

import gail_ai_operating_system as gail  # noqa: E402


class PublicApiExportTests(unittest.TestCase):
    def test_cns_schema_exports_are_available_from_package_root(self) -> None:
        expected_exports = [
            "Action",
            "AuthorityEnvelope",
            "AuthorityLevel",
            "AutonomyLevel",
            "EvidencePacket",
            "EvidenceResult",
            "ExecutionMode",
            "FREEDOM_RELATIONSHIP_BRIEF_SCHEMA_VERSION",
            "LOCAL_ACTION_DECISION_SCHEMA_VERSION",
            "LOCAL_ACTION_REQUEST_SCHEMA_VERSION",
            "LocalActionStore",
            "LocalTraceEventStore",
            "MissionStatus",
            "TraceEvent",
            "action_refs_for_trace",
            "approval_refs_for_trace",
            "create_action",
            "create_cns_trace_id",
            "create_evidence_packet",
            "create_local_action_request",
            "create_trace_event",
            "build_freedom_relationship_brief",
            "default_action_store_path",
            "default_approval_store_path",
            "ensure_cns_trace_id",
            "record_local_action_decision",
            "validate_action",
            "validate_authority_envelope",
            "validate_cns_trace_id",
            "validate_evidence_packet",
            "validate_trace_event",
        ]

        for export_name in expected_exports:
            with self.subTest(export_name=export_name):
                self.assertTrue(hasattr(gail, export_name))


if __name__ == "__main__":
    unittest.main()
