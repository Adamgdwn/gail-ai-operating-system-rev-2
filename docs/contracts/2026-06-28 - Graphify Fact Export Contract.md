# Graphify Fact Export Contract

**Date:** 2026-06-28
**Last Updated:** 2026-06-29T19:31:31-06:00
**Chunk:** 20E — GAIL OS + Graphify Safe Graph-Fact Extraction Lane
**Status:** Contract complete — extraction lane defined, not active as GAIL OS ingest approval
**Schema:** `contracts/json-schema/graph-fact.schema.json`
**Transport:** GAIL OS learning transport remains owner-gated; this contract does not approve any live Graphify write call

---

## Purpose

This contract defines the lane through which GAIL OS emits sanitized graph facts into the Graphify CNS store. It is the "Learn" step in the CNS cognitive cycle: after an action completes and an EvidencePacket is written, GAIL OS packages the sanitized outcome as a `GraphFact` and Graphify ingests it to update relationship weights, entity attributes, and mission history in the store.

---

## 2026-06-29 Boundary Reconciliation

This contract predates the 2026-06-29 Graphify boundary transfer. Its local
GAIL OS safety intent still stands: GAIL OS has not been approved to mutate the
persistent Graphify CNS store from this repo.

The older wording below should no longer be read as a universal Graphify
platform invariant. Graphify may own guarded relationship-memory write lanes in
its own repo. For GAIL OS, any persistent Graphify learning write remains a
connector-like promotion gate that must define source refs, idempotency,
payload limits, rejection behavior, failure handling, and owner approval before
runtime use.

Active rule:

- Graphify may remember approved relationships.
- Graphify may not approve, deny, execute, escalate R-levels, mutate business
  systems, or become the canonical GAIL OS evidence ledger.
- This contract defines fact shape and safety posture, not active ingest
  authorization.

## Original Extraction-Write / API-Read Preference

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

For this GAIL OS contract, the HTTP API is not approved as a write path. The
original preference was an extraction pipeline writer. This contract adds GAIL
OS as a future extraction or learning source; it does not add an active API
write path from this repo.

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

**Current status:** Contract and schema defined. Local acceleration/preview
helpers exist elsewhere in this repo, but no persistent GAIL OS Graphify ingest
lane is active from this contract.

---

## What Is NOT Included

Per 20E stop condition:
- No live M365 data ingested
- No secrets in sanitized_payload
- No Graphify HTTP/API write path added from GAIL OS
- No Phase 3 emission code (future implementation)
- No EvidencePacket content stored in Graphify (sanitized attributes only)

---

*Contract status: Task complete. Fact shape and safety posture defined. No live
GAIL OS Graphify ingest or write transport active.*
