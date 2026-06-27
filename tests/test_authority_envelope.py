"""Tests for AuthorityEnvelope schema — the governance charter for R4 actions."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

from gail_ai_operating_system.authority_envelope import (  # noqa: E402
    AuthorityEnvelope,
    AuthorityLevel,
    AutonomyLevel,
    EnvelopeStatus,
    validate_authority_envelope,
)


def _valid_envelope(**overrides: object) -> AuthorityEnvelope:
    defaults: dict = {
        "envelope_id": "env-test-001",
        "mission_id": "mission-abc123",
        "authority_level": "R2",
        "autonomy_level": "A1",
        "domain": "build",
        "granted_by": "Adam Goodwin",
        "granted_at": "2026-06-27T10:00:00-06:00",
        "expires_at": None,
        "allowed_action_types": ("local_mission_record", "policy_gate_review"),
        "max_risk_tier": 2,
        "stop_conditions": ("Any R3+ action attempt", "Scope boundary breach"),
        "rollback_path": "Revert to prior mission state; review evidence log.",
        "review_cadence": "After each mission cycle",
        "status": "active",
    }
    defaults.update(overrides)
    return AuthorityEnvelope(**defaults)


class AuthorityLevelEnumTests(unittest.TestCase):
    def test_all_r_levels_present(self) -> None:
        expected = {"R0", "R1", "R2", "R3", "R4", "R5"}
        self.assertEqual({l.value for l in AuthorityLevel}, expected)

    def test_r_levels_are_string_enum(self) -> None:
        self.assertIsInstance(AuthorityLevel.R4, str)
        self.assertEqual(AuthorityLevel.R0, "R0")


class AutonomyLevelEnumTests(unittest.TestCase):
    def test_all_a_levels_present(self) -> None:
        expected = {"A0", "A1", "A2", "A3", "A4", "A5", "A6"}
        self.assertEqual({l.value for l in AutonomyLevel}, expected)

    def test_current_operating_boundary_is_a1(self) -> None:
        self.assertIn(AutonomyLevel.A1, AutonomyLevel)
        self.assertEqual(AutonomyLevel.A1.value, "A1")


class EnvelopeStatusEnumTests(unittest.TestCase):
    def test_lifecycle_statuses_present(self) -> None:
        expected = {"active", "revoked", "expired", "pending"}
        self.assertEqual({s.value for s in EnvelopeStatus}, expected)


class AuthorityEnvelopeSchemaTests(unittest.TestCase):
    def test_envelope_has_fourteen_charter_fields(self) -> None:
        envelope = _valid_envelope()
        charter_fields = [
            "envelope_id", "mission_id", "authority_level", "autonomy_level",
            "domain", "granted_by", "granted_at", "expires_at",
            "allowed_action_types", "max_risk_tier", "stop_conditions",
            "rollback_path", "review_cadence", "status",
        ]
        envelope_dict = envelope.to_dict()
        self.assertEqual(len(charter_fields), 14)
        for f in charter_fields:
            self.assertIn(f, envelope_dict, f"Missing charter field: {f}")

    def test_envelope_round_trips_via_dict(self) -> None:
        original = _valid_envelope()
        restored = AuthorityEnvelope.from_dict(original.to_dict())
        self.assertEqual(original, restored)

    def test_envelope_with_expiry_round_trips(self) -> None:
        original = _valid_envelope(expires_at="2027-01-01T00:00:00+00:00")
        restored = AuthorityEnvelope.from_dict(original.to_dict())
        self.assertEqual(restored.expires_at, "2027-01-01T00:00:00+00:00")

    def test_envelope_without_expiry_round_trips(self) -> None:
        original = _valid_envelope(expires_at=None)
        restored = AuthorityEnvelope.from_dict(original.to_dict())
        self.assertIsNone(restored.expires_at)


class ValidateAuthorityEnvelopeTests(unittest.TestCase):
    def test_valid_envelope_returns_no_errors(self) -> None:
        errors = validate_authority_envelope(_valid_envelope())
        self.assertEqual(errors, [])

    def test_missing_env_prefix_is_rejected(self) -> None:
        envelope = _valid_envelope(envelope_id="bad-id-001")
        errors = validate_authority_envelope(envelope)
        self.assertTrue(any("env-" in e for e in errors))

    def test_missing_mission_prefix_is_rejected(self) -> None:
        envelope = _valid_envelope(mission_id="bad-mission")
        errors = validate_authority_envelope(envelope)
        self.assertTrue(any("mission-" in e for e in errors))

    def test_invalid_authority_level_is_rejected(self) -> None:
        envelope = _valid_envelope(authority_level="R9")
        errors = validate_authority_envelope(envelope)
        self.assertTrue(any("authority_level" in e for e in errors))

    def test_invalid_autonomy_level_is_rejected(self) -> None:
        envelope = _valid_envelope(autonomy_level="A9")
        errors = validate_authority_envelope(envelope)
        self.assertTrue(any("autonomy_level" in e for e in errors))

    def test_risk_tier_above_five_is_rejected(self) -> None:
        envelope = _valid_envelope(max_risk_tier=6)
        errors = validate_authority_envelope(envelope)
        self.assertTrue(any("max_risk_tier" in e for e in errors))

    def test_empty_rollback_path_is_rejected(self) -> None:
        envelope = _valid_envelope(rollback_path="")
        errors = validate_authority_envelope(envelope)
        self.assertTrue(any("rollback_path" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
