#!/usr/bin/env python3
"""CP-1 JSON Schema contract export and validation script.

Validates all CP-1 JSON Schema files against synthetic records.
Transport-neutral. No HTTP, no live connectors, no FastAPI.

Usage:
    python scripts/export-cp1-contracts.py [--schema-dir contracts/json-schema] [--verbose]
"""

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_SCHEMA_DIR = REPO_ROOT / "contracts" / "json-schema"

CP1_SCHEMA_FILES = [
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

SYNTHETIC_RECORDS = {
    "mission.schema.json": {
        "mission_id": "mission-abc123def456",
        "cns_trace_id": "cns-20260628-abc123def456",
        "request_id": "req-abc123def456",
        "command": "Validate local proof runner output against schema",
        "domain": "validation",
        "created_at": "2026-06-28T00:00:00-06:00",
        "owner": "Adam Goodwin",
        "approval_level": "A1 local no-network",
        "dry_run": True,
        "requested_tools": ["local_validation"],
        "data_classification": "internal",
        "status": "draft",
        "source_commit": None,
    },
    "action.schema.json": {
        "action_id": "action-abc123def456",
        "cns_trace_id": "cns-20260628-abc123def456",
        "mission_id": "mission-abc123def456",
        "action_type": "local_mission_record",
        "title": "Record local validation result",
        "actor": "Adam Goodwin",
        "status": "approval_requested",
        "authority_level": "R0",
        "risk_tier": 1,
        "arguments": {"target": "validation-suite"},
        "created_at": "2026-06-28T00:00:00-06:00",
        "claimed_at": None,
        "executed_at": None,
        "envelope_id": None,
    },
    "policy-decision.schema.json": {
        "action_id": "action-abc123def456",
        "cns_trace_id": "cns-20260628-abc123def456",
        "allowed": True,
        "mode": "dry-run",
        "reason": "Action is within A1 local no-network boundary.",
        "stop_reason": None,
    },
    "authority-envelope.schema.json": {
        "envelope_id": "env-abc123def456",
        "mission_id": "mission-abc123def456",
        "authority_level": "R4",
        "autonomy_level": "A1",
        "domain": "governance",
        "granted_by": "Adam Goodwin",
        "granted_at": "2026-06-28T00:00:00-06:00",
        "expires_at": None,
        "allowed_action_types": ["local_mission_record", "local_validation_command"],
        "max_risk_tier": 3,
        "stop_conditions": ["Any live connector access", "Any network call"],
        "rollback_path": "Delete local record file",
        "review_cadence": "Weekly during active build",
        "status": "active",
    },
    "evidence-packet.schema.json": {
        "evidence_id": "evidence-abc123def456",
        "cns_trace_id": "cns-20260628-abc123def456",
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
        "outcome_summary": "Validation record written locally.",
    },
    "connector-status.schema.json": {
        "connector_id": "graphify-local",
        "display_name": "Graphify Local CNS API",
        "system_family": "Graphify",
        "owner": "Adam Goodwin",
        "tenant_or_workspace": "local-linux",
        "current_state": "planning-only",
        "allowed_capabilities": ["planning-only", "inventory-only"],
        "prohibited_capabilities": ["execute-after-approval", "write", "admin-change"],
        "data_classes": ["public", "internal", "synthetic"],
        "approval_gate": "A2 approval required for live read",
        "retention_rule": "Local records only, no cloud persistence at A1",
        "audit_requirements": ["mission_id", "connector_id", "capability", "result"],
        "stop_triggers": ["graphify_action_execution"],
        "failure_behavior": "Log stop trigger and halt; no retry without governance review",
        "live_access_enabled": False,
        "notes": "Graphify HTTP API is read-only at port 8001",
    },
    "source-ref.schema.json": {
        "source_id": "src-abc123def456",
        "source_system": "gail-os",
        "entity_id": "action-abc123def456",
        "ref_type": "action",
        "repo_path": "packages/uaos-core/src/gail_ai_operating_system/action.py",
        "ref_value": "8e56b8a582483965e646cba510c5448c95aa1849",
        "created_at": "2026-06-28T00:00:00-06:00",
    },
    "graph-context-ref.schema.json": {
        "graph_ref_id": "gref-abc123def456",
        "entity_id": "connector-graphify-local",
        "entity_type": "connector",
        "relationship_type": "GOVERNS",
        "target_entity_id": "repo-gail-ai-operating-system-rev-2",
        "query_context": "connector scope validation",
        "confidence": 0.97,
        "graph_timestamp": "2026-06-28T00:00:00-06:00",
        "source_ref_id": None,
    },
    "approval-decision.schema.json": {
        "decision_id": "aprv-abc123def456",
        "cns_trace_id": "cns-20260628-abc123def456",
        "action_id": "action-abc123def456",
        "mission_id": "mission-abc123def456",
        "decision_type": "approved",
        "decided_by": "Adam Goodwin",
        "decided_at": "2026-06-28T00:00:00-06:00",
        "rationale": "Mission is low-risk local validation. R0 boundary preserved.",
        "authority_basis": "R0 — local dry-run",
        "envelope_id": None,
        "hold_until": None,
        "info_requested": None,
        "info_from": None,
    },
}


def load_schema(schema_path: Path) -> dict:
    with open(schema_path, encoding="utf-8") as f:
        return json.load(f)


def validate_record(record: dict, schema: dict) -> list[str]:
    try:
        import jsonschema
    except ImportError:
        return ["jsonschema library not installed — run: pip install jsonschema"]

    validator_cls = jsonschema.validators.validator_for(schema)
    validator = validator_cls(schema)
    errors = list(validator.iter_errors(record))
    return [f"{'.'.join(str(p) for p in e.absolute_path) or '(root)'}: {e.message}" for e in errors]


def run_export(schema_dir: Path, verbose: bool = False) -> int:
    """Validate all CP-1 schemas and synthetic records. Returns 0 on success."""

    errors_found = 0

    print(f"CP-1 Contract Export — schema dir: {schema_dir}")
    print("=" * 60)

    for schema_file in CP1_SCHEMA_FILES:
        schema_path = schema_dir / schema_file

        if not schema_path.exists():
            print(f"  MISSING  {schema_file}")
            errors_found += 1
            continue

        try:
            schema = load_schema(schema_path)
        except json.JSONDecodeError as e:
            print(f"  INVALID JSON  {schema_file}: {e}")
            errors_found += 1
            continue

        # Validate schema is valid JSON Schema
        try:
            import jsonschema
            jsonschema.validators.validator_for(schema).check_schema(schema)
        except Exception as e:
            print(f"  INVALID SCHEMA  {schema_file}: {e}")
            errors_found += 1
            continue

        # Validate synthetic record against schema
        synthetic = SYNTHETIC_RECORDS.get(schema_file)
        if synthetic:
            record_errors = validate_record(synthetic, schema)
            if record_errors:
                print(f"  FAIL  {schema_file}")
                for err in record_errors:
                    print(f"         {err}")
                errors_found += 1
            else:
                print(f"  OK    {schema_file}")
                if verbose:
                    title = schema.get("title", schema_file)
                    print(f"        title: {title}")
                    print(f"        required: {schema.get('required', [])}")
        else:
            print(f"  OK    {schema_file} (no synthetic record — schema parse only)")

    print("=" * 60)
    if errors_found:
        print(f"FAILED — {errors_found} error(s) found")
        return 1
    else:
        print(f"OK — all {len(CP1_SCHEMA_FILES)} CP-1 schemas valid")
        return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Export and validate CP-1 JSON Schema contracts.")
    parser.add_argument(
        "--schema-dir",
        type=Path,
        default=DEFAULT_SCHEMA_DIR,
        help="Path to the json-schema directory (default: contracts/json-schema)",
    )
    parser.add_argument("--verbose", action="store_true", help="Show schema titles and required fields")
    args = parser.parse_args()

    sys.exit(run_export(args.schema_dir, verbose=args.verbose))


if __name__ == "__main__":
    main()
