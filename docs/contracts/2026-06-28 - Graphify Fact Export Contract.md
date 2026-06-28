# Graphify Fact Export Contract

**Date:** 2026-06-28
**Chunk:** 20E — GAIL OS + Graphify Safe Graph-Fact Extraction Lane
**Status:** Contract complete — extraction lane defined, not yet active (Phase 3)
**Schema:** `contracts/json-schema/graph-fact.schema.json`
**Transport:** Extraction pipeline write only — never the Graphify HTTP API

---

## Purpose

This contract defines the lane through which GAIL OS emits sanitized graph facts into the Graphify CNS store. It is the "Learn" step in the CNS cognitive cycle: after an action completes and an EvidencePacket is written, GAIL OS packages the sanitized outcome as a `GraphFact` and Graphify ingests it to update relationship weights, entity attributes, and mission history in the store.

---

## Extraction-Write / API-Read Rule (Reinforced)

```
GAIL OS (approval_actions, evidence_recorder, mission_lifecycle)
    │
    │  emits GraphFact records
    ▼
GraphFact extraction pipeline
    │
    │  writes to CNS store (SQLite)
    ▼
CNS store (entities + relationships)
    │
    │  reads only
    ▼
Graphify HTTP API (port 8001) ← queried by Freedom and GAIL OS
```

**The HTTP API is never a write path.** This is the fundamental Graphify design rule. The extraction pipeline is the only writer. This contract adds GAIL OS as an extraction source — it does not add an API write path.

---

## What GAIL OS Emits

GAIL OS emits `GraphFact` records from four modules:

| Module | Fact Types Emitted | When |
|---|---|---|
| `approval_actions` | `action_executed`, `authority_granted` | After `approve_action()` completes |
| `evidence_recorder` | `evidence_recorded`, `mission_completed` | After `EvidencePacket` is written |
| `mission_lifecycle` | `entity_observed`, `relationship_observed` | When missions target entities |
| `connector_registry` | `connector_registered` | When a new `ConnectorProfile` is registered |

---

## Schema Summary (`graph-fact.schema.json`)

| Field | Type | Required | Description |
|---|---|---|---|
| `fact_id` | string (`gfact-` prefix) | Yes | Unique fact identifier |
| `fact_type` | closed enum | Yes | Classification (7 types) |
| `subject_entity_id` | string | Yes | Primary entity this fact describes |
| `subject_entity_type` | string | Yes | Entity type (Action, Mission, Connector, etc.) |
| `object_entity_id` | string or null | No | Secondary entity for relationship facts |
| `relationship_kind` | string or null | No | Relationship type for `relationship_observed` facts |
| `emitted_by` | closed enum (6 modules) | Yes | GAIL OS module that emitted this |
| `emitted_at` | ISO 8601 string | Yes | When GAIL OS emitted the fact |
| `status` | closed enum (4 states) | Yes | `emitted` → `queued` → `ingested` / `rejected` |
| `mission_id` | string or null | No | Parent mission (`mission-` prefix) |
| `action_id` | string or null | No | Parent action (`action-` prefix) |
| `evidence_id` | string or null | No | Parent evidence packet (`evidence-` prefix) |
| `source_ref_id` | string or null | No | Source-of-truth reference (`src-` prefix) — links to `source-ref.schema.json` |
| `graph_ref_id` | string or null | No | Existing Graphify entity reference (`gref-` prefix) — links to `graph-context-ref.schema.json` |
| `sanitized_payload` | object or null | No | Sanitized GAIL OS data for Graphify to ingest |
| `ingestion_notes` | string or null | No | Graphify pipeline notes (populated post-ingestion) |

---

## Closed Enums

| Enum | Values |
|---|---|
| `GraphFactType` | `entity_observed`, `relationship_observed`, `mission_completed`, `action_executed`, `evidence_recorded`, `connector_registered`, `authority_granted` |
| `GraphFactStatus` | `emitted`, `queued`, `ingested`, `rejected` |
| `emitted_by` | `approval_actions`, `evidence_recorder`, `mission_lifecycle`, `connector_registry`, `policy_gate`, `authority_engine` |

---

## Sanitization Rules

The `sanitized_payload` field must:
- Contain only structured key-value data safe for indexing in a graph store
- Never contain secrets, credentials, API keys, or raw provider content
- Never contain PII beyond what is already in the entity's public GAIL OS record
- Be validated against a per-fact-type allowlist before emission (future Phase 3 implementation)

---

## Connection to 20C Schemas

The `GraphFact` schema references two schemas from 20C:

| Field | References | Schema |
|---|---|---|
| `source_ref_id` | A `source-ref` record in GAIL OS | `source-ref.schema.json` (`src-` prefix) |
| `graph_ref_id` | A `graph-context-ref` in Graphify | `graph-context-ref.schema.json` (`gref-` prefix) |

These fields are optional — a `GraphFact` can be emitted without an existing Graphify entity to corroborate.

---

## Phase Gate

The extraction lane defined here is an architecture contract, not a live implementation. It becomes active in Phase 3 (after CP-1 closes). Phase 3 requires:

1. GAIL OS HTTP API live (Chunk 21) — so GAIL OS can signal the extraction pipeline
2. Graphify CNS store accessible (Phase 2 complete — G1-GPHY open)
3. An extraction pipeline trigger in GAIL OS that emits `GraphFact` records post-evidence
4. Graphify extraction pipeline accepts `GraphFact` as an input format (Graphify Phase 3)

**Current status:** Contract and schema defined. No emission code active. No Graphify ingestion code active.

---

## What Is NOT Included

Per 20E stop condition:
- No live M365 data ingested
- No secrets in sanitized_payload
- No Graphify HTTP API write path added
- No Phase 3 emission code (future implementation)
- No EvidencePacket content stored in Graphify (sanitized attributes only)

---

*Contract status: Task complete. Extraction lane defined. Extraction-write / API-read rule preserved. No live emission active.*
