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
            "MissionStatus",
            "create_action",
            "create_evidence_packet",
            "validate_action",
            "validate_authority_envelope",
            "validate_evidence_packet",
        ]

        for export_name in expected_exports:
            with self.subTest(export_name=export_name):
                self.assertTrue(hasattr(gail, export_name))


if __name__ == "__main__":
    unittest.main()
