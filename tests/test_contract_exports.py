"""Tests for 20C CP-1 JSON Schema contract files.

Validates that:
- All 9 schema files exist and parse as valid JSON Schema
- Synthetic valid records pass each schema
- Invalid records fail with clear errors
- Transport-neutral: no FastAPI, HTTP, or live-connector references
- R-level and A-level enums are closed (only valid values accepted)
- MissionStatus 12-stage lifecycle is closed (only valid values accepted)
"""

import json
import sys
import os
from pathlib import Path
from contextlib import contextmanager
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "packages", "uaos-core", "src"))

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

SCHEMA_DIR = Path(__file__).parent.parent / "contracts" / "json-schema"

SCHEMA_FILES = [
    "mission.schema.json",
    "action.schema.json",
    "policy-decision.schema.json",
    "authority-envelope.schema.json",
    "evidence-packet.schema.json",
    "connector-status.schema.json",
    "source-ref.schema.json",
    "graph-context-ref.schema.json",
    "approval-decision.schema.json",
]


@contextmanager
def raises(exc_type, match=None):
    try:
        yield
    except exc_type as e:
        if match is not None and not re.search(match, str(e)):
            raise AssertionError(f"{match!r} not in {e!r}") from e
        return
    raise AssertionError(f"{exc_type.__name__} not raised")


def load_schema(name: str) -> dict:
    path = SCHEMA_DIR / name
    return json.loads(path.read_text(encoding="utf-8"))


def validate(record: dict, schema: dict) -> list[str]:
    if not HAS_JSONSCHEMA:
        return []
    validator_cls = jsonschema.validators.validator_for(schema)
    v = validator_cls(schema)
    return [e.message for e in v.iter_errors(record)]


def assert_valid(record: dict, schema: dict) -> None:
    errors = validate(record, schema)
    assert not errors, f"Expected valid, got errors: {errors}"


def assert_invalid(record: dict, schema: dict) -> None:
    if not HAS_JSONSCHEMA:
        return
    errors = validate(record, schema)
    assert errors, f"Expected invalid but schema accepted the record"


# ── Schema existence and parseability ────────────────────────────────────────

def test_all_schema_files_exist():
    missing = [f for f in SCHEMA_FILES if not (SCHEMA_DIR / f).exists()]
    assert not missing, f"Missing schema files: {missing}"


def test_all_schema_files_are_valid_json():
    for name in SCHEMA_FILES:
        data = load_schema(name)
        assert isinstance(data, dict), f"{name} must be a JSON object"


def test_all_schemas_have_required_meta_fields():
    for name in SCHEMA_FILES:
        schema = load_schema(name)
        assert "$schema" in schema, f"{name} missing $schema"
        assert "$id" in schema, f"{name} missing $id"
        assert "title" in schema, f"{name} missing title"
        assert "description" in schema, f"{name} missing description"


def test_all_schemas_are_valid_jsonschema():
    if not HAS_JSONSCHEMA:
        return
    for name in SCHEMA_FILES:
        schema = load_schema(name)
        validator_cls = jsonschema.validators.validator_for(schema)
        validator_cls.check_schema(schema)


def test_all_schema_ids_use_gail_os_local_prefix():
    for name in SCHEMA_FILES:
        schema = load_schema(name)
        assert schema["$id"].startswith("https://gail-os.local/"), f"{name} $id must use gail-os.local"


# ── mission.schema.json ───────────────────────────────────────────────────────

def test_mission_valid_record():
    schema = load_schema("mission.schema.json")
    record = {
        "mission_id": "mission-abc123def456",
        "request_id": "req-abc123def456",
        "command": "Validate schemas",
        "domain": "validation",
        "created_at": "2026-06-28T00:00:00-06:00",
        "owner": "Adam Goodwin",
        "approval_level": "A1 local no-network",
        "dry_run": True,
    }
    assert_valid(record, schema)


def test_mission_invalid_mission_id_prefix():
    schema = load_schema("mission.schema.json")
    record = {
        "mission_id": "bad-prefix-123",
        "request_id": "req-abc123def456",
        "command": "Test",
        "domain": "validation",
        "created_at": "2026-06-28T00:00:00-06:00",
        "owner": "Adam Goodwin",
        "approval_level": "A1 local no-network",
        "dry_run": True,
    }
    assert_invalid(record, schema)


def test_mission_invalid_domain():
    schema = load_schema("mission.schema.json")
    record = {
        "mission_id": "mission-abc123def456",
        "request_id": "req-abc123def456",
        "command": "Test",
        "domain": "invalid_domain",
        "created_at": "2026-06-28T00:00:00-06:00",
        "owner": "Adam Goodwin",
        "approval_level": "A1 local no-network",
        "dry_run": True,
    }
    assert_invalid(record, schema)


def test_mission_status_enum_has_all_12_stages():
    schema = load_schema("mission.schema.json")
    mission_status_enum = schema["$defs"]["MissionStatus"]["enum"]
    expected = {
        "observed", "proposed", "classified", "approval_requested",
        "approved", "rejected", "claimed", "executed", "stopped",
        "evidenced", "reviewed", "learned",
    }
    assert set(mission_status_enum) == expected


def test_mission_status_enum_is_closed():
    schema = load_schema("mission.schema.json")
    status_schema = schema["$defs"]["MissionStatus"]
    assert_invalid({"$ref": "MissionStatus", "value": "unknown_stage"}, status_schema)


# ── action.schema.json ───────────────────────────────────────────────────────

def test_action_valid_record():
    schema = load_schema("action.schema.json")
    record = {
        "action_id": "action-abc123def456",
        "mission_id": "mission-abc123def456",
        "action_type": "local_mission_record",
        "title": "Test action",
        "actor": "Adam Goodwin",
        "status": "approval_requested",
        "authority_level": "R0",
        "risk_tier": 1,
        "arguments": {},
        "created_at": "2026-06-28T00:00:00-06:00",
        "claimed_at": None,
        "executed_at": None,
        "envelope_id": None,
    }
    assert_valid(record, schema)


def test_action_invalid_authority_level():
    schema = load_schema("action.schema.json")
    record = {
        "action_id": "action-abc123def456",
        "mission_id": "mission-abc123def456",
        "action_type": "test",
        "title": "Test",
        "actor": "Adam",
        "status": "observed",
        "authority_level": "R9",
        "risk_tier": 1,
        "arguments": {},
        "created_at": "2026-06-28T00:00:00-06:00",
    }
    assert_invalid(record, schema)


def test_action_risk_tier_out_of_range():
    schema = load_schema("action.schema.json")
    record = {
        "action_id": "action-abc123def456",
        "mission_id": "mission-abc123def456",
        "action_type": "test",
        "title": "Test",
        "actor": "Adam",
        "status": "observed",
        "authority_level": "R0",
        "risk_tier": 9,
        "arguments": {},
        "created_at": "2026-06-28T00:00:00-06:00",
    }
    assert_invalid(record, schema)


def test_action_authority_level_enum_complete():
    schema = load_schema("action.schema.json")
    r_levels = schema["$defs"]["AuthorityLevel"]["enum"]
    assert set(r_levels) == {"R0", "R1", "R2", "R3", "R4", "R5"}


def test_action_invalid_status():
    schema = load_schema("action.schema.json")
    record = {
        "action_id": "action-abc123def456",
        "mission_id": "mission-abc123def456",
        "action_type": "test",
        "title": "Test",
        "actor": "Adam",
        "status": "unknown_status",
        "authority_level": "R0",
        "risk_tier": 1,
        "arguments": {},
        "created_at": "2026-06-28T00:00:00-06:00",
    }
    assert_invalid(record, schema)


# ── authority-envelope.schema.json ───────────────────────────────────────────

def test_authority_envelope_valid_record():
    schema = load_schema("authority-envelope.schema.json")
    record = {
        "envelope_id": "env-abc123def456",
        "mission_id": "mission-abc123def456",
        "authority_level": "R4",
        "autonomy_level": "A1",
        "domain": "governance",
        "granted_by": "Adam Goodwin",
        "granted_at": "2026-06-28T00:00:00-06:00",
        "allowed_action_types": ["local_validation_command"],
        "max_risk_tier": 3,
        "stop_conditions": ["Any live connector access"],
        "rollback_path": "Delete local record",
        "review_cadence": "Weekly",
        "status": "active",
    }
    assert_valid(record, schema)


def test_authority_envelope_bad_prefix():
    schema = load_schema("authority-envelope.schema.json")
    record = {
        "envelope_id": "bad-prefix",
        "mission_id": "mission-abc123def456",
        "authority_level": "R4",
        "autonomy_level": "A1",
        "domain": "governance",
        "granted_by": "Adam",
        "granted_at": "2026-06-28T00:00:00-06:00",
        "allowed_action_types": ["test"],
        "max_risk_tier": 1,
        "stop_conditions": ["stop"],
        "rollback_path": "delete",
        "review_cadence": "weekly",
        "status": "active",
    }
    assert_invalid(record, schema)


def test_authority_envelope_invalid_autonomy_level():
    schema = load_schema("authority-envelope.schema.json")
    record = {
        "envelope_id": "env-abc123def456",
        "mission_id": "mission-abc123def456",
        "authority_level": "R4",
        "autonomy_level": "A9",
        "domain": "governance",
        "granted_by": "Adam",
        "granted_at": "2026-06-28T00:00:00-06:00",
        "allowed_action_types": ["test"],
        "max_risk_tier": 1,
        "stop_conditions": ["stop"],
        "rollback_path": "delete",
        "review_cadence": "weekly",
        "status": "active",
    }
    assert_invalid(record, schema)


def test_authority_envelope_autonomy_enum_complete():
    schema = load_schema("authority-envelope.schema.json")
    a_levels = schema["$defs"]["AutonomyLevel"]["enum"]
    assert set(a_levels) == {"A0", "A1", "A2", "A3", "A4", "A5", "A6"}


def test_authority_envelope_empty_stop_conditions_invalid():
    schema = load_schema("authority-envelope.schema.json")
    record = {
        "envelope_id": "env-abc123def456",
        "mission_id": "mission-abc123def456",
        "authority_level": "R4",
        "autonomy_level": "A1",
        "domain": "governance",
        "granted_by": "Adam",
        "granted_at": "2026-06-28T00:00:00-06:00",
        "allowed_action_types": ["test"],
        "max_risk_tier": 1,
        "stop_conditions": [],
        "rollback_path": "delete",
        "review_cadence": "weekly",
        "status": "active",
    }
    assert_invalid(record, schema)


# ── evidence-packet.schema.json ──────────────────────────────────────────────

def test_evidence_packet_valid_record():
    schema = load_schema("evidence-packet.schema.json")
    record = {
        "evidence_id": "evidence-abc123def456",
        "mission_id": "mission-abc123def456",
        "action_id": "action-abc123def456",
        "actor": "Adam Goodwin",
        "action_type": "local_mission_record",
        "authority_basis": "R0 — local dry-run",
        "result": "success",
        "execution_mode": "dry-run",
        "created_at": "2026-06-28T00:00:00-06:00",
        "envelope_id": None,
        "rollback_note": None,
        "outcome_summary": "All good",
    }
    assert_valid(record, schema)


def test_evidence_packet_invalid_result():
    schema = load_schema("evidence-packet.schema.json")
    record = {
        "evidence_id": "evidence-abc123def456",
        "mission_id": "mission-abc123def456",
        "action_id": "action-abc123def456",
        "actor": "Adam",
        "action_type": "test",
        "authority_basis": "R0",
        "result": "unknown_result",
        "execution_mode": "dry-run",
        "created_at": "2026-06-28T00:00:00-06:00",
        "outcome_summary": "",
    }
    assert_invalid(record, schema)


def test_evidence_packet_invalid_execution_mode():
    schema = load_schema("evidence-packet.schema.json")
    record = {
        "evidence_id": "evidence-abc123def456",
        "mission_id": "mission-abc123def456",
        "action_id": "action-abc123def456",
        "actor": "Adam",
        "action_type": "test",
        "authority_basis": "R0",
        "result": "success",
        "execution_mode": "production",
        "created_at": "2026-06-28T00:00:00-06:00",
        "outcome_summary": "",
    }
    assert_invalid(record, schema)


def test_evidence_result_enum_complete():
    schema = load_schema("evidence-packet.schema.json")
    results = schema["$defs"]["EvidenceResult"]["enum"]
    assert set(results) == {"success", "failure", "stopped", "partial"}


# ── policy-decision.schema.json ──────────────────────────────────────────────

def test_policy_decision_valid_allow():
    schema = load_schema("policy-decision.schema.json")
    record = {
        "action_id": "action-abc123def456",
        "allowed": True,
        "mode": "dry-run",
        "reason": "Within A1 boundary.",
        "stop_reason": None,
    }
    assert_valid(record, schema)


def test_policy_decision_valid_deny():
    schema = load_schema("policy-decision.schema.json")
    record = {
        "action_id": "action-abc123def456",
        "allowed": False,
        "mode": "dry-run",
        "reason": "Action type is blocked.",
        "stop_reason": "external_message_send",
    }
    assert_valid(record, schema)


def test_policy_decision_invalid_mode():
    schema = load_schema("policy-decision.schema.json")
    record = {
        "action_id": "action-abc123def456",
        "allowed": True,
        "mode": "production",
        "reason": "Test",
    }
    assert_invalid(record, schema)


# ── connector-status.schema.json ─────────────────────────────────────────────

def test_connector_status_valid_record():
    schema = load_schema("connector-status.schema.json")
    record = {
        "connector_id": "graphify-local",
        "display_name": "Graphify Local CNS API",
        "system_family": "Graphify",
        "owner": "Adam Goodwin",
        "tenant_or_workspace": "local-linux",
        "current_state": "planning-only",
        "allowed_capabilities": ["planning-only"],
        "prohibited_capabilities": ["execute-after-approval"],
        "data_classes": ["internal"],
        "approval_gate": "A2 required",
        "retention_rule": "Local only",
        "audit_requirements": ["mission_id"],
        "stop_triggers": ["graphify_action_execution"],
        "failure_behavior": "Halt and log",
        "live_access_enabled": False,
        "notes": "",
    }
    assert_valid(record, schema)


def test_connector_status_invalid_system_family():
    schema = load_schema("connector-status.schema.json")
    record = {
        "connector_id": "unknown",
        "display_name": "Unknown",
        "system_family": "UnknownFamily",
        "owner": "Adam",
        "tenant_or_workspace": "local",
        "current_state": "planning-only",
        "allowed_capabilities": [],
        "prohibited_capabilities": [],
        "data_classes": [],
        "approval_gate": "none",
        "retention_rule": "local",
        "audit_requirements": [],
        "stop_triggers": [],
        "failure_behavior": "halt",
    }
    assert_invalid(record, schema)


def test_connector_status_system_family_enum_complete():
    schema = load_schema("connector-status.schema.json")
    families = schema["$defs"]["SystemFamily"]["enum"]
    assert "GitHub" in families
    assert "Microsoft 365" in families
    assert "Graphify" in families


# ── source-ref.schema.json ───────────────────────────────────────────────────

def test_source_ref_valid_record():
    schema = load_schema("source-ref.schema.json")
    record = {
        "source_id": "src-abc123def456",
        "source_system": "gail-os",
        "entity_id": "action-abc123def456",
        "ref_type": "action",
        "created_at": "2026-06-28T00:00:00-06:00",
    }
    assert_valid(record, schema)


def test_source_ref_invalid_source_system():
    schema = load_schema("source-ref.schema.json")
    record = {
        "source_id": "src-abc123def456",
        "source_system": "twitter",
        "entity_id": "some-entity",
        "ref_type": "entity",
        "created_at": "2026-06-28T00:00:00-06:00",
    }
    assert_invalid(record, schema)


def test_source_ref_bad_id_prefix():
    schema = load_schema("source-ref.schema.json")
    record = {
        "source_id": "bad-prefix",
        "source_system": "gail-os",
        "entity_id": "some-entity",
        "ref_type": "entity",
        "created_at": "2026-06-28T00:00:00-06:00",
    }
    assert_invalid(record, schema)


# ── graph-context-ref.schema.json ────────────────────────────────────────────

def test_graph_context_ref_valid_record():
    schema = load_schema("graph-context-ref.schema.json")
    record = {
        "graph_ref_id": "gref-abc123def456",
        "entity_id": "connector-graphify",
        "entity_type": "connector",
        "query_context": "connector scope validation",
        "graph_timestamp": "2026-06-28T00:00:00-06:00",
        "confidence": 0.97,
    }
    assert_valid(record, schema)


def test_graph_context_ref_bad_prefix():
    schema = load_schema("graph-context-ref.schema.json")
    record = {
        "graph_ref_id": "bad-prefix",
        "entity_id": "connector-graphify",
        "entity_type": "connector",
        "query_context": "test",
        "graph_timestamp": "2026-06-28T00:00:00-06:00",
    }
    assert_invalid(record, schema)


def test_graph_context_ref_confidence_out_of_range():
    schema = load_schema("graph-context-ref.schema.json")
    record = {
        "graph_ref_id": "gref-abc123def456",
        "entity_id": "connector-graphify",
        "entity_type": "connector",
        "query_context": "test",
        "graph_timestamp": "2026-06-28T00:00:00-06:00",
        "confidence": 1.5,
    }
    assert_invalid(record, schema)


# ── approval-decision.schema.json ────────────────────────────────────────────

def test_approval_decision_valid_approved():
    schema = load_schema("approval-decision.schema.json")
    record = {
        "decision_id": "aprv-abc123def456",
        "action_id": "action-abc123def456",
        "mission_id": "mission-abc123def456",
        "decision_type": "approved",
        "decided_by": "Adam Goodwin",
        "decided_at": "2026-06-28T00:00:00-06:00",
        "rationale": "Mission is within A1 boundary.",
        "authority_basis": "R0 — local dry-run",
        "envelope_id": None,
        "hold_until": None,
        "info_requested": None,
        "info_from": None,
    }
    assert_valid(record, schema)


def test_approval_decision_valid_held():
    schema = load_schema("approval-decision.schema.json")
    record = {
        "decision_id": "aprv-abc123def456",
        "action_id": "action-abc123def456",
        "mission_id": "mission-abc123def456",
        "decision_type": "held",
        "decided_by": "Adam Goodwin",
        "decided_at": "2026-06-28T00:00:00-06:00",
        "rationale": "Awaiting policy review.",
        "authority_basis": "R0",
        "hold_until": "2026-06-29T00:00:00-06:00",
    }
    assert_valid(record, schema)


def test_approval_decision_invalid_type():
    schema = load_schema("approval-decision.schema.json")
    record = {
        "decision_id": "aprv-abc123def456",
        "action_id": "action-abc123def456",
        "mission_id": "mission-abc123def456",
        "decision_type": "skipped",
        "decided_by": "Adam",
        "decided_at": "2026-06-28T00:00:00-06:00",
        "rationale": "Test",
        "authority_basis": "R0",
    }
    assert_invalid(record, schema)


def test_approval_decision_bad_decision_id_prefix():
    schema = load_schema("approval-decision.schema.json")
    record = {
        "decision_id": "bad-prefix",
        "action_id": "action-abc123def456",
        "mission_id": "mission-abc123def456",
        "decision_type": "approved",
        "decided_by": "Adam",
        "decided_at": "2026-06-28T00:00:00-06:00",
        "rationale": "Test",
        "authority_basis": "R0",
    }
    assert_invalid(record, schema)


def test_approval_decision_type_enum_complete():
    schema = load_schema("approval-decision.schema.json")
    types = schema["$defs"]["ApprovalDecisionType"]["enum"]
    assert set(types) == {"approved", "rejected", "held", "more_info_requested"}


# ── Export script integration ─────────────────────────────────────────────────

def test_export_script_runs_clean():
    """Verify the export script exits 0 with all schemas in place."""
    import subprocess
    script = Path(__file__).parent.parent / "scripts" / "export-cp1-contracts.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Export script failed:\n{result.stdout}\n{result.stderr}"


# ── No transport/HTTP references in schemas ───────────────────────────────────

def test_no_fastapi_references_in_schemas():
    for name in SCHEMA_FILES:
        schema_text = (SCHEMA_DIR / name).read_text(encoding="utf-8").lower()
        assert "fastapi" not in schema_text, f"{name} contains 'fastapi'"
        assert "localhost" not in schema_text, f"{name} contains 'localhost'"
        assert "127.0.0.1" not in schema_text, f"{name} contains hardcoded IP"
