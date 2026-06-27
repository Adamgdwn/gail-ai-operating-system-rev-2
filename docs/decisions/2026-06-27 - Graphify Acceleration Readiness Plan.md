# Graphify Acceleration Readiness Plan

Document type: architecture plan
Date: 2026-06-27
Saved: 2026-06-27T09:06:27-06:00
Last Updated: 2026-06-27T09:06:27-06:00
Status: active planning record
Owner: Adam Goodwin

## Purpose

This plan defines what GAIL AI Operating System Rev 2 should do to help a
faster, more agile Graphify layer interact with the governed operating system.

The scope is GAIL-side readiness only. This record does not modify Graphify,
activate a Graphify connector, upload a graph, start a live adapter, or grant
Graphify execution authority.

## Owner Direction

Graphify is expected to become faster and able to reach more corners of the
interconnected Guided AI Labs system. Rev 2 should prepare for that by making
its own governed state easier for Graphify to consume, not by changing Graphify
itself inside this repository.

New durable reading documents should use date-prefixed filenames. Dependency
files, importable source modules, schemas, generated files, runtime configs,
and tool-owned files must keep their stable names.

## Design Concept

GAIL OS should support two separate lanes:

1. Graphify to GAIL OS: read-only recommendations and graph context become
   mission candidates through the existing Graphify handoff validator.
2. GAIL OS to Graphify: sanitized authority, action, evidence, connector, and
   system-state facts become small delta records that Graphify can ingest or
   index later.

The second lane is the speed lever. Graphify should not have to rediscover
every governed relationship by crawling raw source or parsing long documents
when GAIL OS can emit compact, policy-aware graph facts.

## CNS Fit

In the CNS model:

```text
Signal -> GAIL OS classifies -> Freedom reasons -> OS validates authority
  -> motor system executes -> evidence returns to OS
  -> Graphify updates -> Freedom learns
```

This plan strengthens the `evidence returns to OS -> Graphify updates` segment.
The graph layer can become much faster at relationship intelligence while GAIL
OS remains the authority and evidence boundary.

## Planned Contract Shape

Future local implementation should introduce a stable importable contract with
dependency-safe names, for example:

- `packages/uaos-core/src/gail_ai_operating_system/graphify_acceleration.py`
- `tests/test_graphify_acceleration.py`

The reading document is dated. The importable source files are not.

Candidate record name: `GraphifyAccelerationRecord`.

Required fields:

| Field | Purpose |
|---|---|
| `schema_version` | Stable contract marker, for example `rev2.graphify-acceleration.v1`. |
| `record_id` | Stable `graphify-fact-...` identifier. |
| `source_system` | Always this Rev 2 system unless a later bridge contract says otherwise. |
| `generated_at` | Timestamp from the GAIL-side emitter. |
| `operation` | `created`, `transitioned`, `evidenced`, `reviewed`, `learned`, `linked`, or `superseded`. |
| `entity_type` | `mission`, `action`, `authority_envelope`, `evidence_packet`, `connector`, `system`, or later approved type. |
| `entity_id` | Stable GAIL OS entity ID. |
| `entity_version` | Local version or revision when available. |
| `title` | Short safe label. |
| `summary` | Safe summary only, never raw payload. |
| `authority_level` | R0 to R5. |
| `risk_tier` | Integer 0 to 5. |
| `authority_envelope_id` | Optional `env-...` reference where required. |
| `approval_state` | Local action or relay approval state where applicable. |
| `data_classification` | `public`, `internal`, `synthetic`, or later approved safe-summary class. |
| `source_refs` | Relative non-sensitive repo or record references. |
| `evidence_refs` | Existing evidence or graph node references. |
| `related_entities` | Typed edges to other GAIL OS entities. |
| `stop_triggers` | Explicit stop triggers preserved for Graphify routing. |
| `non_goals` | Boundaries Graphify and future agents must not cross. |
| `contains_raw_payload` | Must be `false` for current A1 local no-network posture. |
| `fingerprint` | Deterministic value for cache and delta detection. |

## GAIL-Side Emitters

Future implementation should keep emitters close to the governed boundaries:

- `Action` creation and transition emit action state facts.
- `AuthorityEnvelope` creation or status changes emit authority-boundary facts.
- `EvidencePacket` creation emits safe evidence summary facts.
- Connector registry evaluation emits capability and stop-boundary facts.
- Pathway validation and chunk closeout emit build-state facts.

Each emitter should be local and deterministic first. It should produce records
that can be inspected in tests before any Graphify adapter, API, or cloud path
exists.

## Speed Benefits

This plan should let future Graphify improvements move faster because Rev 2
will provide:

- stable entity IDs instead of fuzzy document-only discovery;
- delta records instead of repeated whole-repo crawling;
- deterministic fingerprints for cache invalidation;
- explicit typed relationships between missions, actions, authority envelopes,
  evidence, connectors, and chunks;
- safe summaries that exclude secrets, raw logs, raw audio, live business
  content, client data, and unredacted payloads;
- authority and risk metadata that Graphify can use for routing without
  becoming an approval source.

## Phased Path

### Phase A - Plan Only

Status: active with this record.

Capture the GAIL-side acceleration plan and route it through the active pathway.
No code, live connector, Graphify repo change, Graphify upload, HTTP API,
cloud placement, or production behavior.

### Phase B - Local Contract And Validator

After Chunk Twenty is ready or when Adam explicitly chooses this work, add the
stable local contract and tests in Rev 2 only.

Acceptance:

- create acceleration records from safe sample Action, AuthorityEnvelope, and
  EvidencePacket data;
- reject absolute paths, parent traversal, `.env`, raw logs, raw audio, client
  data, live connector hints, secrets, missing fingerprints, invalid R-levels,
  invalid risk tiers, and `contains_raw_payload: true`;
- expose package-root exports only when the contract is stable enough for
  local consumers.

### Phase C - Local Export Preview

Add a local export preview or store only after the contract is validated.

Acceptance:

- produce deterministic JSONL or JSON records from local governed sample data;
- keep output ignored or explicitly controlled until retention is decided;
- show what Graphify would receive without sending it anywhere.

### Phase D - Contract Publication

After local approval, authority, evidence, API/cloud placement, and TypeScript
consumer decisions are firm, publish the contract through the future
`@gail/contracts` or equivalent typed contract package.

Acceptance:

- schema is versioned;
- Python and TypeScript examples agree;
- backward-compatible change policy is documented.

### Phase E - Future Graphify Adapter Boundary

Only after explicit approval, define a read/write boundary for Graphify ingest.

Acceptance:

- Graphify may ingest safe acceleration records;
- Graphify still cannot approve execution;
- graph updates cannot mutate Rev 2 source;
- live adapter calls require connector profile, auth, retention, audit, and
  stop rules.

## Stop Boundaries

Stop before:

- modifying the Graphify repository or runtime;
- creating a live Graphify adapter;
- uploading graph data;
- changing Graphify roots or performing a full semantic rebuild outside an
  approved chunk;
- exposing HTTP APIs or selecting cloud placement;
- indexing Microsoft 365, QuickBooks, client, finance, billing, raw logs, raw
  audio, or secrets;
- letting Graphify recommendations approve, execute, mutate, send, deploy, or
  change permissions;
- treating this plan as approval for Chunk Twenty implementation.

## Open Decisions

- Whether acceleration records should be event-only, snapshot-only, or both.
  Initial recommendation: event-first deltas with optional compact snapshots.
- Whether local preview output should live in a relay store, a dedicated local
  export store, or an ignored developer artifact. Initial recommendation:
  no persistent export store until the contract validator exists.
- Whether Graphify should consume acceleration facts from GitHub records, a
  future API, local files, or a cloud event path. Initial recommendation:
  defer transport until after local approval, authority, and evidence
  contracts are stable.

## Next Safe Slice

The next GAIL-side slice, when selected, should be:

```text
Pre-Graphify implementation slice:
Add local GraphifyAccelerationRecord validation and sample emitters from
Action, AuthorityEnvelope, and EvidencePacket, with tests only.
```

That slice remains outside live Graphify modification and outside Chunk Twenty
unless Adam explicitly folds it into the active build path.
