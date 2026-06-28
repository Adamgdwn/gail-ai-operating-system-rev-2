"""Tests for the graph-fact.schema.json CP-1 contract (Chunk 20E).

Validates the GraphFact schema that defines the GAIL OS → Graphify extraction
lane. Extraction writes. API reads. No write path through the Graphify HTTP API.
"""
import json
from pathlib import Path

import jsonschema
import pytest

REPO_ROOT = Path(__file__).parent.parent
SCHEMA_DIR = REPO_ROOT / "contracts" / "json-schema"
GRAPH_FACT_SCHEMA_PATH = SCHEMA_DIR / "graph-fact.schema.json"

NOW = "2026-06-28T00:00:00-06:00"

VALID_GRAPH_FACT = {
    "fact_id": "gfact-abc123def456",
    "fact_type": "action_executed",
    "subject_entity_id": "action-abc123def456",
    "subject_entity_type": "Action",
    "emitted_by": "approval_actions",
    "emitted_at": NOW,
    "status": "emitted",
    "mission_id": "mission-abc123def456",
    "action_id": "action-abc123def456",
    "evidence_id": None,
    "source_ref_id": "src-abc123def456",
    "graph_ref_id": None,
    "sanitized_payload": {
        "action_kind": "local_mission_record",
        "risk_tier": 0,
        "outcome": "approved",
    },
    "ingestion_notes": None,
}


@pytest.fixture(scope="module")
def graph_fact_schema():
    assert GRAPH_FACT_SCHEMA_PATH.exists(), f"graph-fact.schema.json not found at {GRAPH_FACT_SCHEMA_PATH}"
    with open(GRAPH_FACT_SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def validator(graph_fact_schema):
    cls = jsonschema.validators.validator_for(graph_fact_schema)
    cls.check_schema(graph_fact_schema)
    return cls(graph_fact_schema)


# ---------------------------------------------------------------------------
# Schema file existence and structure
# ---------------------------------------------------------------------------

def test_graph_fact_schema_file_exists():
    assert GRAPH_FACT_SCHEMA_PATH.exists()


def test_graph_fact_schema_is_valid_json(graph_fact_schema):
    assert isinstance(graph_fact_schema, dict)


def test_graph_fact_schema_is_valid_json_schema(graph_fact_schema):
    cls = jsonschema.validators.validator_for(graph_fact_schema)
    cls.check_schema(graph_fact_schema)


def test_graph_fact_schema_id_uses_gail_os_local_namespace(graph_fact_schema):
    schema_id = graph_fact_schema.get("$id", "")
    assert schema_id.startswith("https://gail-os.local/"), f"$id must use gail-os.local namespace, got: {schema_id}"


def test_graph_fact_schema_uses_draft_2020_12(graph_fact_schema):
    assert graph_fact_schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"


def test_graph_fact_schema_has_no_transport_references(graph_fact_schema):
    schema_str = json.dumps(graph_fact_schema).lower()
    forbidden = ["localhost", "fastapi", "8001", "httpx", "requests"]
    for term in forbidden:
        assert term not in schema_str, f"graph-fact schema must not reference '{term}'"


def test_graph_fact_schema_has_additional_properties_false(graph_fact_schema):
    assert graph_fact_schema.get("additionalProperties") is False


# ---------------------------------------------------------------------------
# Required fields
# ---------------------------------------------------------------------------

def test_graph_fact_required_fields(graph_fact_schema):
    required = set(graph_fact_schema.get("required", []))
    expected_required = {"fact_id", "fact_type", "subject_entity_id", "subject_entity_type", "emitted_by", "emitted_at", "status"}
    assert expected_required == required


# ---------------------------------------------------------------------------
# Valid synthetic record
# ---------------------------------------------------------------------------

def test_valid_graph_fact_passes(validator):
    errors = list(validator.iter_errors(VALID_GRAPH_FACT))
    assert not errors, f"Valid GraphFact should pass: {errors}"


def test_graph_fact_entity_observed_passes(validator):
    fact = {
        **VALID_GRAPH_FACT,
        "fact_id": "gfact-entity-obs",
        "fact_type": "entity_observed",
        "subject_entity_type": "Repository",
        "emitted_by": "mission_lifecycle",
    }
    errors = list(validator.iter_errors(fact))
    assert not errors


def test_graph_fact_relationship_observed_passes(validator):
    fact = {
        **VALID_GRAPH_FACT,
        "fact_id": "gfact-rel-obs",
        "fact_type": "relationship_observed",
        "object_entity_id": "connector-graphify-local",
        "relationship_kind": "GOVERNS",
        "emitted_by": "connector_registry",
    }
    errors = list(validator.iter_errors(fact))
    assert not errors


def test_graph_fact_connector_registered_passes(validator):
    fact = {
        **VALID_GRAPH_FACT,
        "fact_id": "gfact-connector-reg",
        "fact_type": "connector_registered",
        "subject_entity_id": "connector-graphify-local",
        "subject_entity_type": "Connector",
        "emitted_by": "connector_registry",
    }
    errors = list(validator.iter_errors(fact))
    assert not errors


def test_graph_fact_all_optional_fields_null_passes(validator):
    minimal = {
        "fact_id": "gfact-minimal-001",
        "fact_type": "entity_observed",
        "subject_entity_id": "action-minimal",
        "subject_entity_type": "Action",
        "emitted_by": "mission_lifecycle",
        "emitted_at": NOW,
        "status": "emitted",
    }
    errors = list(validator.iter_errors(minimal))
    assert not errors


# ---------------------------------------------------------------------------
# Closed enum enforcement
# ---------------------------------------------------------------------------

def test_invalid_fact_type_rejected(validator):
    bad = {**VALID_GRAPH_FACT, "fact_id": "gfact-bad-type", "fact_type": "INVALID_FACT_TYPE"}
    errors = list(validator.iter_errors(bad))
    assert errors, "Invalid fact_type should be rejected"


def test_invalid_emitted_by_rejected(validator):
    bad = {**VALID_GRAPH_FACT, "fact_id": "gfact-bad-emitter", "emitted_by": "freedom"}
    errors = list(validator.iter_errors(bad))
    assert errors, "Freedom is not a valid emitted_by value — GAIL OS modules only"


def test_invalid_status_rejected(validator):
    bad = {**VALID_GRAPH_FACT, "fact_id": "gfact-bad-status", "status": "ACTIVE"}
    errors = list(validator.iter_errors(bad))
    assert errors, "Invalid status should be rejected"


def test_all_valid_fact_types_accepted(validator):
    valid_types = [
        "entity_observed", "relationship_observed", "mission_completed",
        "action_executed", "evidence_recorded", "connector_registered", "authority_granted"
    ]
    for i, fact_type in enumerate(valid_types):
        fact = {**VALID_GRAPH_FACT, "fact_id": f"gfact-type-{i}", "fact_type": fact_type}
        errors = list(validator.iter_errors(fact))
        assert not errors, f"Valid fact_type '{fact_type}' should be accepted: {errors}"


def test_all_valid_statuses_accepted(validator):
    valid_statuses = ["emitted", "queued", "ingested", "rejected"]
    for i, status in enumerate(valid_statuses):
        fact = {**VALID_GRAPH_FACT, "fact_id": f"gfact-status-{i}", "status": status}
        errors = list(validator.iter_errors(fact))
        assert not errors, f"Valid status '{status}' should be accepted: {errors}"


# ---------------------------------------------------------------------------
# Prefix validation
# ---------------------------------------------------------------------------

def test_fact_id_must_use_gfact_prefix(validator):
    bad = {**VALID_GRAPH_FACT, "fact_id": "wrong-prefix-abc123"}
    errors = list(validator.iter_errors(bad))
    assert errors, "fact_id without 'gfact-' prefix should be rejected"


# ---------------------------------------------------------------------------
# Missing required fields
# ---------------------------------------------------------------------------

def test_missing_fact_id_rejected(validator):
    bad = {k: v for k, v in VALID_GRAPH_FACT.items() if k != "fact_id"}
    errors = list(validator.iter_errors(bad))
    assert errors


def test_missing_fact_type_rejected(validator):
    bad = {k: v for k, v in VALID_GRAPH_FACT.items() if k != "fact_type"}
    errors = list(validator.iter_errors(bad))
    assert errors


def test_missing_subject_entity_id_rejected(validator):
    bad = {k: v for k, v in VALID_GRAPH_FACT.items() if k != "subject_entity_id"}
    errors = list(validator.iter_errors(bad))
    assert errors


def test_missing_emitted_by_rejected(validator):
    bad = {k: v for k, v in VALID_GRAPH_FACT.items() if k != "emitted_by"}
    errors = list(validator.iter_errors(bad))
    assert errors


def test_missing_status_rejected(validator):
    bad = {k: v for k, v in VALID_GRAPH_FACT.items() if k != "status"}
    errors = list(validator.iter_errors(bad))
    assert errors


# ---------------------------------------------------------------------------
# Extraction-write / API-read rule: no HTTP import in this test module
# ---------------------------------------------------------------------------

def test_no_http_transport_imports():
    import ast
    source = open(__file__).read()
    tree = ast.parse(source)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split(".")[0])
    http_libs = {"fastapi", "httpx", "requests", "aiohttp", "flask", "starlette"}
    found = http_libs & set(imports)
    assert not found, f"HTTP transport imports found in test module: {found}"
