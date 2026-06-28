# Graphify Acceleration Readiness Plan

Document type: architecture plan
Date: 2026-06-27
Saved: 2026-06-27T09:06:27-06:00
Last Updated: 2026-06-27T18:06:31-06:00
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

Owner context added 2026-06-27T17:41:51-06:00: Graphify should be treated as a
high-importance neuronal pathway layer for fast, reliable relationship
intelligence across the Guided AI Labs system. AG Operations Workspace Setup is
the likely first tactile Microsoft 365 environment that will eventually provide
real operating-system input and output surfaces, but it remains a future
governed boundary for Rev 2. Current Freedom inputs and outputs remain clear
and must not be compromised by Graphify acceleration work.

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

The chunks below are plan-local Graphify acceleration chunks. They do not
replace the main build pathway chunk numbers unless Adam later promotes one of
them into `docs/current-build-pathway.md`.

### Phase A - Plan Only

Status: complete (2026-06-27T09:39:31-06:00)

Capture the GAIL-side acceleration plan and route it through the active pathway.
No code, live connector, Graphify repo change, Graphify upload, HTTP API,
cloud placement, or production behavior.

#### GA-A1 - Record GAIL-Side Acceleration Boundary

Status: complete (2026-06-27T09:06:27-06:00)

Completion target: Task complete

Budget class: Small

Objective: define the GAIL-side speed lever for enhanced Graphify without
changing Graphify, activating an adapter, or granting authority.

Inputs: CNS diagram, owner direction, current Graphify handoff checkpoint,
architecture map, source-of-truth map, document-control standard, and active
pathway.

Outputs: this dated architecture plan, pathway routing notes, changelog entry,
and source/context map references.

Acceptance:

- the plan states that Rev 2 prepares itself for Graphify rather than modifying
  Graphify;
- the two lanes are distinct: Graphify-to-GAIL handoff candidates and
  GAIL-to-Graphify sanitized facts;
- future source file names remain dependency-safe and are not date-prefixed;
- stop boundaries block live adapters, graph upload, raw payload indexing,
  HTTP API exposure, cloud placement, connector activation, and execution
  authority.

Validation: governance preflight, Graphify orientation attempt, routing review,
`git diff --check`, Graphify incremental update, commit, and push.

Stop condition: stop before implementation, Graphify runtime changes, live
transport, or Chunk Twenty approval-action work.

#### GA-A2 - Detail Phase Chunks

Status: complete (2026-06-27T09:29:11-06:00)

Completion target: Task complete

Budget class: Small

Objective: turn the phase headings into executable work packets so a later
agent can advance the plan without guessing scope, boundaries, validation, or
completion state.

Inputs: this plan, active pathway, standards index, durable development
policy, ship-ready standard, use-case governance standard, project-control
classification, risk register, architecture key decisions, and Graphify
governance.

Outputs: detailed GA-A through GA-E chunk map in this plan, active pathway
status note, and changelog note.

Acceptance:

- each phase has small, named chunks with objective, inputs, outputs,
  acceptance, validation, and stop boundaries;
- implementation chunks are sequenced after a local contract and validator;
- transport, cloud, HTTP API, Graphify adapter, and publication work remain
  gated behind explicit owner decisions;
- Chunk Twenty remains the default Rev 2 implementation path unless Adam later
  promotes a Graphify acceleration slice.

Validation: governance preflight, repo-local Graphify query, document review,
`git diff --check`, Graphify incremental update, commit, and push.

Stop condition: stop before creating source modules, schemas, export stores,
adapters, or live integrations.

#### GA-A3 - Owner Promotion Checkpoint

Status: complete (2026-06-27T09:39:31-06:00)

Completion target: Draft complete

Budget class: Tiny

Objective: decide whether Graphify acceleration implementation should wait
until after Chunk Twenty or become the next pre-Chunk Twenty slice.

Inputs: this plan, current build pathway, Chunk Twenty readiness, CNS schema
hardening results, and owner priority.

Outputs: an owner decision recorded in the active pathway, either deferring
Graphify acceleration or promoting a specific GA-B chunk.

Execution note: Adam directed execution to start before Chunk Twenty, with the
boundary that this repository modifies GAIL OS only and does not modify
Graphify. GA-B1 and GA-B2 were promoted as the first pre-Chunk Twenty slice.

Acceptance:

- the next selected slice is named explicitly;
- the decision says whether Chunk Twenty remains next or a GA-B contract slice
  is inserted first;
- no code or transport work starts without the decision.

Validation: owner confirmation, pathway update, changelog note if the active
route changes, and `git diff --check` for any document edits.

Stop condition: stop if the priority is unclear, if the implementation would
touch live systems, or if it would require Graphify repo changes.

### Phase B - Local Contract And Validator

Status: integration complete (2026-06-27T17:03:09-06:00)

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

Execution note: As of 2026-06-27T17:03:09-06:00, Phase B is integration
complete. Rev 2 has sanitizer classification helpers, stricter reference and
relationship guards, pure local Action/AuthorityEnvelope/EvidencePacket record
builders, deterministic fingerprints, and package-root exports. This does not
add persistence, preview output, Graphify calls, adapters, transport, HTTP
APIs, cloud placement, live connectors, client data, runtime hooks, or
execution authority.

#### GA-B1 - Contract Work Packet And Fixture Inventory

Status: draft complete (2026-06-27T09:39:31-06:00)

Completion target: Draft complete

Budget class: Tiny

Objective: prepare the smallest implementation slice for the
`GraphifyAccelerationRecord` contract.

Inputs: `packages/uaos-core/src/gail_ai_operating_system/action.py`,
`packages/uaos-core/src/gail_ai_operating_system/authority_envelope.py`,
`packages/uaos-core/src/gail_ai_operating_system/evidence_packet.py`,
`packages/uaos-core/src/gail_ai_operating_system/mission_spine.py`,
`packages/uaos-core/src/gail_ai_operating_system/connector_registry.py`,
`packages/uaos-core/src/gail_ai_operating_system/graphify_handoff.py`,
existing tests, this plan, and active stop boundaries.

Outputs: pathway work packet that names the exact files, fixtures, non-goals,
test expectations, and rollback path for GA-B2 through GA-B4.

Acceptance:

- sample source objects are identified without reading secrets, live connector
  state, M365 content, QuickBooks data, client data, raw logs, or raw audio;
- contract vocabulary is aligned with existing CNS schema names;
- no source module is created yet unless this chunk is intentionally combined
  with GA-B2 by owner approval.

Fixture inventory:

- action fixture: synthetic `Action`-shaped records with `action-` IDs,
  `mission-` IDs, current `MissionStatus` values, R-level authority, risk
  tier, optional `env-` envelope reference, and relative source refs only;
- authority fixture: synthetic `AuthorityEnvelope`-shaped records with `env-`
  IDs, explicit allowed action types, stop conditions, rollback path, review
  cadence, and non-sensitive charter summaries only;
- evidence fixture: synthetic `EvidencePacket`-shaped records with
  `evidence-` IDs, `action-` refs, dry-run execution mode, safe outcome
  summaries, and relative evidence refs only;
- connector fixture: current planning-only connector profiles as metadata
  references only, never live connector state or external-system content.

Validation: targeted file review, governance preflight if the active pathway is
updated, and `git diff --check` for document edits.

Stop condition: stop if fixture selection would require live business data,
secret access, or Graphify repo changes.

#### GA-B2 - Define GraphifyAccelerationRecord Contract

Status: draft complete (2026-06-27T09:39:31-06:00)

Completion target: Draft complete

Budget class: Small

Objective: add the stable Python contract object in Rev 2 with strict field
validation and no transport behavior.

Inputs: current split CNS schema modules (`action.py`,
`authority_envelope.py`, `evidence_packet.py`), current package style,
existing validation patterns, this plan's required field list, and GA-B1
fixture decisions.

Outputs:
`packages/uaos-core/src/gail_ai_operating_system/graphify_acceleration.py`
with `GraphifyAccelerationRecord`, allowed enum values, serialization helpers,
and safe validation errors.

Acceptance:

- schema version must equal the approved v1 value;
- record IDs must use a stable `graphify-fact-` prefix;
- source system must identify Rev 2 unless a later bridge contract expands it;
- operation, entity type, authority level, risk tier, approval state, and data
  classification are closed sets;
- `contains_raw_payload` must be false;
- source and evidence refs must be relative, non-sensitive references;
- absolute paths, parent traversal, `.env`, raw logs, raw audio, client-data
  labels, live connector hints, and likely secret markers are rejected;
- fingerprints are required but generated in a later chunk unless GA-B5 is
  promoted in the same implementation session.

Validation: focused unit tests for valid records, invalid enum values,
sensitive references, missing required fields, and JSON-safe serialization.

Stop condition: stop before package-root exports, persistence, preview files,
Graphify calls, HTTP APIs, or TypeScript schema publication.

#### GA-B3 - Add Sanitization And Reference Guards

Status: task complete (2026-06-27T17:03:09-06:00)

Completion target: Task complete

Budget class: Small

Objective: make the validator hard to misuse before any emitter depends on it.

Inputs: GA-B2 contract module, existing Graphify handoff sensitive-boundary
tests, file-boundary tests in the mission and relay store areas, and security
rules from project standards.

Outputs: validator helpers that classify safe summaries, safe refs, safe edge
labels, blocked raw payload hints, and blocked sensitive source indicators.

Acceptance:

- summary text cannot contain raw payload markers, secret-like markers, or
  blocked sensitive-data labels;
- refs cannot point outside the repo, to absolute local paths, to `.env`
  material, to logs/audio dumps, or to generated graph output;
- related entity edges must have typed relationship names and stable target
  IDs;
- validation errors are explicit enough for tests and future operators without
  leaking sensitive content.

Validation: focused unit tests for accepted safe refs/summaries and rejected
unsafe refs/summaries/edges.

Stop condition: stop before adding emitters if sanitization is incomplete or
ambiguous.

#### GA-B4 - Add Local Sample Emitters

Status: task complete (2026-06-27T17:03:09-06:00)

Completion target: Task complete

Budget class: Medium

Objective: prove the contract can be produced from current local governed
objects without changing those objects' behavior.

Inputs: `Action`, `AuthorityEnvelope`, `EvidencePacket`, safe local fixtures,
and GA-B2/GA-B3 validation helpers.

Outputs: deterministic local emitter functions for sample action, authority
envelope, and evidence packet facts.

Acceptance:

- emitters are pure local functions with no network, file writes, Graphify
  calls, or live connector access;
- action facts include action ID, approval state, authority level, risk tier,
  envelope reference when required, stop triggers, and non-goals;
- authority facts include envelope ID, charter boundaries, stop conditions,
  risk tier, and human-only limits where applicable;
- evidence facts include evidence packet ID, execution mode, referenced action
  ID, safe summary, and evidence refs only;
- invalid source objects fail clearly instead of producing partial graph facts.

Validation: unit tests that build facts from safe fixtures and reject unsafe or
incomplete source objects.

Stop condition: stop before persistence, export preview, package-root exports,
or connecting the emitters to runtime state transitions.

#### GA-B5 - Add Deterministic Fingerprints And Delta Identity

Status: task complete (2026-06-27T17:03:09-06:00)

Completion target: Task complete

Budget class: Small

Objective: give Graphify future cache and delta workflows a stable comparison
surface without requiring whole-state recrawls.

Inputs: GA-B2 through GA-B4 records, JSON-safe serialization, existing
deterministic ID patterns, and test fixtures.

Outputs: canonical payload normalization and fingerprint generation for
acceleration records.

Acceptance:

- fingerprints are deterministic across repeated runs with identical input;
- volatile fields that should not invalidate graph cache are excluded only when
  explicitly documented;
- changes to entity ID, operation, entity type, relationships, authority,
  approval state, risk, summary, refs, stop triggers, or non-goals change the
  fingerprint;
- fingerprint generation does not include raw payloads or local absolute paths.

Validation: unit tests for stable repeat generation, expected changes, and
blocked unsafe fields.

Stop condition: stop before export preview if deterministic identity cannot be
proven.

#### GA-B6 - Package Export And Local Consumer Gate

Status: integration complete (2026-06-27T17:03:09-06:00)

Completion target: Integration complete

Budget class: Small

Objective: expose the contract from the package root only after the validator,
emitters, and fingerprint behavior are stable enough for local use.

Inputs: package `__init__.py`, GA-B2 through GA-B5 tests, and existing package
export style.

Outputs: package-root exports for the record, emitter helpers, and validation
errors.

Acceptance:

- exports are deliberate and documented in tests;
- local import examples work without circular imports;
- public names match the domain vocabulary in this plan;
- no transport, persistence, Graphify adapter, TypeScript publication, or
  runtime hook is added.

Validation: focused package import tests, full Python test suite, governance
preflight, `git diff --check`, Graphify incremental update, commit, and push.

Stop condition: stop before moving to Phase C unless all Phase B focused tests
pass.

### Phase C - Local Export Preview

Status: task complete (2026-06-27T18:06:31-06:00)

Add a local export preview or store only after the contract is validated.

Acceptance:

- produce deterministic JSONL or JSON records from local governed sample data;
- keep output ignored or explicitly controlled until retention is decided;
- show what Graphify would receive without sending it anywhere.

#### GA-C1 - Preview Retention Decision

Status: draft complete (2026-06-27T17:15:09-06:00)

Completion target: Draft complete

Budget class: Tiny

Objective: choose whether preview output is ignored developer artifact,
controlled test fixture, relay-store-adjacent record, or a dedicated local
export store.

Inputs: GA-B outputs, current `.gitignore`, relay store behavior, evidence
ledger direction, and retention/security standards.

Outputs: documented preview-retention decision in the active pathway and
`docs/decisions/2026-06-27 - Graphify Preview Retention Decision.md`.

Decision: preview output defaults to ignored local developer artifact retention
under `tmp/graphify-acceleration-preview/`. Generated preview output is not
committed by default and is not a relay record, evidence record, approval
record, source-of-truth record, or Graphify ingest path.

Acceptance:

- default recommendation remains ignored local preview output unless Adam
  approves controlled retention;
- decision names cleanup expectations and what may be committed;
- no Graphify ingest path is implied by the preview location.

Validation: document review and `git diff --check`.

Stop condition: stop if preview retention could accidentally store sensitive
business data, secrets, raw logs, raw audio, or client content.

Execution note: GA-C1 chose the ignored local preview lane because `.gitignore`
already excludes `tmp/` and `graphify-out/`, while the relay store remains a
governed proof lane with approval/evidence semantics. No preview writer,
preview output, persistent export store, Graphify call, adapter, transport,
HTTP API, cloud placement, live connector, live business-system read, client
data, or execution authority was added.

#### GA-C2 - Build Local Export Preview Command

Status: task complete (2026-06-27T17:41:51-06:00)

Completion target: Task complete

Budget class: Medium

Objective: generate deterministic preview output from local safe records so
operators can inspect what Graphify would later receive.

Inputs: GA-B contract and emitters, safe local fixtures, selected preview
location from GA-C1, and existing project command conventions.

Outputs: a local command or callable function that writes JSONL or JSON preview
records from safe sample data only.

Acceptance:

- [x] preview records validate before write;
- [x] output ordering is deterministic;
- [x] output includes fingerprints and schema version;
- [x] command has a print-only mode;
- [x] output path is ignored and controlled according to GA-C1;
- [x] command cannot read live M365, QuickBooks, client, finance, billing, raw
  audio, raw logs, secrets, or Graphify runtime state.

Validation: focused tests for deterministic output, invalid output rejection,
safe path checks, and no-network behavior.

Stop condition: stop before scheduling, background execution, Graphify ingest,
or live data sources.

Execution note: GA-C2 added
`packages/uaos-core/src/gail_ai_operating_system/graphify_acceleration_preview.py`,
`tests/test_graphify_acceleration_preview.py`, and
`scripts/write-graphify-acceleration-preview.ps1`. The command writes
deterministic synthetic JSONL records under
`tmp/graphify-acceleration-preview/graphify-acceleration-preview.jsonl` by
default, or prints the same JSONL without writing when `-PrintOnly` is used.
It validates every `GraphifyAccelerationRecord` before write, rejects output
paths outside the approved ignored preview directory, and creates no Graphify
call, adapter, transport, HTTP API, cloud placement, live connector, business
system read, retained evidence lane, or execution authority.

#### GA-C3 - Add Preview Diff And Cache Checks

Status: task complete (2026-06-27T18:06:31-06:00)

Completion target: Task complete

Budget class: Small

Objective: make the preview useful for speed by showing changed facts without
requiring the operator to inspect the entire file manually.

Inputs: GA-C2 output, fingerprints, and local preview fixtures.

Outputs: local comparison helper or test-supported behavior that reports added,
changed, unchanged, and removed fact IDs.

Acceptance:

- [x] comparison is deterministic;
- [x] removed facts are reported as preview information only and do not mutate
  source or Graphify state;
- [x] diff output is safe to read in logs and excludes raw payloads;
- [x] comparison handles empty previous output and invalid previous output clearly.

Validation: focused tests for added, changed, unchanged, removed, empty, and
invalid preview cases.

Stop condition: stop before treating preview diffs as authority, approvals, or
live graph mutations.

Execution note: GA-C3 extended the local preview module with a validated cache
loader, deterministic diff entries, safe JSON diff rendering, and wrapper
support for `-Diff` / `--diff`. The diff compares safe fact IDs and
fingerprints only, reports `added`, `changed`, `unchanged`, and `removed`
facts, treats missing or empty prior preview output as an empty cache, and
raises a clear local error for invalid prior JSONL. The diff never writes,
calls Graphify, mutates source, changes approvals, edits evidence, updates
relay records, reads live business systems, or grants execution authority.

#### GA-C4 - Operator Preview Handoff

Status: task complete (2026-06-27T18:06:31-06:00)

Completion target: Task complete

Budget class: Small

Objective: document how Adam or a future agent can inspect local acceleration
facts safely.

Inputs: GA-C2/GA-C3 behavior, command output examples, stop boundaries, and
current runbook conventions.

Outputs: short operator note in the plan, runbook, or dated companion document
that explains preview generation, safe cleanup, and non-goals.

Acceptance:

- [x] note states that preview output is not sent to Graphify;
- [x] note states that preview output is not an approval record;
- [x] cleanup and ignored-output expectations are clear;
- [x] validation commands are listed.

Validation: document review, command smoke check if command exists, and
`git diff --check`.

Stop condition: stop before publishing schemas or defining a live adapter.

Operator note:

- Generate or refresh the ignored local preview cache:
  `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\write-graphify-acceleration-preview.ps1`
- Print the deterministic preview JSONL without writing:
  `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\write-graphify-acceleration-preview.ps1 -PrintOnly`
- Compare current synthetic preview records against the existing ignored cache:
  `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\write-graphify-acceleration-preview.ps1 -Diff`
- Generated preview output remains disposable under
  `tmp/graphify-acceleration-preview/` and may be deleted during cleanup.
- Preview JSONL and preview diffs are not sent to Graphify, are not approval
  records, are not evidence records, are not relay records, are not
  source-of-truth records, and are not authority to execute.

### Phase D - Contract Publication

After local approval, authority, evidence, API/cloud placement, and TypeScript
consumer decisions are firm, publish the contract through the future
`@gail/contracts` or equivalent typed contract package.

Acceptance:

- schema is versioned;
- Python and TypeScript examples agree;
- backward-compatible change policy is documented.

#### GA-D1 - Publication Readiness Gate

Status: planned

Completion target: Draft complete

Budget class: Tiny

Objective: confirm the prerequisites for publishing a cross-language contract
are actually firm.

Inputs: Chunk Twenty approval-action implementation, evidence and handoff view
direction, API/cloud placement decision, TypeScript contract package decision,
and GA-B/GA-C validation evidence.

Outputs: owner-approved go/no-go note for publication.

Acceptance:

- approval, authority, evidence, transport, and consumer boundaries are named;
- publication is held if HTTP API, cloud placement, or TypeScript package shape
  is still unsettled;
- no schema package is created as a placeholder.

Validation: owner decision, pathway update, and `git diff --check`.

Stop condition: stop if publication would freeze unstable local semantics.

#### GA-D2 - Create Versioned Schema Artifact

Status: planned

Completion target: Task complete

Budget class: Medium

Objective: create a versioned contract artifact for acceleration records after
the local Python contract is stable.

Inputs: GA-D1 approval, GA-B Python contract, GA-C preview examples, and future
contract package conventions.

Outputs: JSON Schema or equivalent typed schema artifact in the approved
contract location.

Acceptance:

- schema version matches the Python contract;
- required fields, enums, reference rules, and raw-payload prohibition are
  represented;
- schema is dependency-safe and uses stable tool-facing filenames;
- examples validate against the schema;
- backward compatibility expectations are documented.

Validation: schema validation tests, Python example generation, TypeScript
example validation if tooling exists, and `git diff --check`.

Stop condition: stop before publishing to external consumers or packaging if
schema and examples disagree.

#### GA-D3 - Add Python And TypeScript Agreement Examples

Status: planned

Completion target: Integration complete

Budget class: Medium

Objective: prove that Python-generated acceleration records and TypeScript
consumers interpret the same contract.

Inputs: GA-D2 schema artifact, Python fixtures, future TypeScript contract
package or command-center consumer test harness.

Outputs: paired Python/TypeScript examples or tests using the same sample
records.

Acceptance:

- Python emits records that TypeScript accepts;
- TypeScript rejects records Python rejects, especially unsafe refs, invalid
  R-levels, invalid risk tiers, and raw-payload flags;
- examples avoid live data and do not imply Graphify transport.

Validation: Python tests, TypeScript tests or build checks, schema validation,
and command-center build if TypeScript code changes.

Stop condition: stop before adapter design if contract agreement is not proven.

#### GA-D4 - Document Versioning And Compatibility Policy

Status: planned

Completion target: Task complete

Budget class: Small

Objective: make future contract evolution safe for Graphify, Freedom, and GAIL
OS consumers.

Inputs: GA-D2/GA-D3 artifacts, existing document-control standard, and contract
package decision.

Outputs: compatibility note covering additive fields, breaking changes,
deprecation, schema version bumps, and minimum consumer behavior.

Acceptance:

- additive changes are distinguished from breaking changes;
- consumers are told how to handle unknown fields;
- old schema handling, deprecation, and migration notes are explicit;
- Graphify still does not become an authority or execution layer.

Validation: document review and `git diff --check`.

Stop condition: stop before public or cross-repo publication if compatibility
rules are not agreed.

### Phase E - Future Graphify Adapter Boundary

Only after explicit approval, define a read/write boundary for Graphify ingest.

Acceptance:

- Graphify may ingest safe acceleration records;
- Graphify still cannot approve execution;
- graph updates cannot mutate Rev 2 source;
- live adapter calls require connector profile, auth, retention, audit, and
  stop rules.

#### GA-E1 - Adapter Approval And Connector Profile Gate

Status: planned

Completion target: Draft complete

Budget class: Small

Objective: require explicit owner approval and connector profiling before any
Graphify ingest or write boundary exists.

Inputs: GA-D publication evidence, connector registry policy, tool permission
matrix, Graphify governance, auth and retention decisions, and owner approval.

Outputs: connector profile or decision record describing Graphify ingest
permissions, auth, retention, audit, rate limits, stop triggers, and rollback.

Acceptance:

- Graphify ingest is named as a connector-like boundary, not an implicit local
  file side effect;
- allowed operations are limited to consuming approved acceleration records;
- denied operations include approval, execution, source mutation, permissions,
  deployment, live business-system reads, and secret handling;
- human approval and rollback expectations are explicit.

Validation: connector profile tests if code changes, document review,
governance preflight, and `git diff --check`.

Stop condition: stop without explicit owner approval.

#### GA-E2 - Adapter Design Note

Status: planned

Completion target: Draft complete

Budget class: Medium

Objective: design the future adapter before implementation so transport,
failure modes, and authority boundaries are reviewable.

Inputs: GA-E1 gate, GA-D schema, Graphify current runtime home, transport
decision, cloud/API placement decision, and security/privacy review.

Outputs: dated adapter design record with data flow, trust boundary, retry
policy, idempotency, audit records, error handling, retention, and rollback.

Acceptance:

- design states exactly where records originate, where they are sent, and what
  acknowledgements mean;
- Graphify failure cannot block GAIL OS authority decisions;
- duplicate delivery is idempotent by fingerprint and record ID;
- adapter logs are safe and do not include raw payloads;
- adapter cannot mutate Rev 2 source or approve actions.

Validation: architecture review, security/privacy review appropriate to the
risk, and document routing update.

Stop condition: stop if cloud/API/auth/retention choices are unresolved.

#### GA-E3 - Local Dry-Run Adapter Proof

Status: planned

Completion target: Task complete

Budget class: Medium

Objective: prove the adapter boundary locally without sending data to Graphify
or any cloud system.

Inputs: GA-E2 design, GA-C preview output, connector profile, and safe mock
transport.

Outputs: dry-run adapter that validates, batches, logs safe summaries, and
produces an audit record without network calls.

Acceptance:

- dry run reads only approved preview records;
- every outgoing item is schema-validated immediately before the simulated
  send;
- audit output records record IDs, fingerprints, counts, and simulated outcome
  without raw payloads;
- failure modes include invalid records, duplicate records, unavailable
  transport, partial batches, and stop-trigger activation;
- no Graphify process, API, cloud endpoint, M365, QuickBooks, client data, or
  live connector is contacted.

Validation: focused adapter tests, no-network test, audit safety tests,
governance preflight, `git diff --check`, Graphify incremental update, commit,
and push.

Stop condition: stop before live adapter credentials, scheduled execution, or
background worker behavior.

#### GA-E4 - Live Adapter Readiness Review

Status: planned

Completion target: Integration complete

Budget class: Strategic

Objective: decide whether a live adapter is safe to enable after the dry-run
proof, contract publication, and transport decisions are mature.

Inputs: GA-E3 evidence, connector profile, auth model, retention decision,
cloud/API placement, monitoring and rollback plan, Graphify runtime readiness,
and owner approval.

Outputs: live-adapter readiness packet with ship/hold recommendation.

Acceptance:

- security, privacy, retention, auth, monitoring, rollback, and audit evidence
  are attached;
- live enablement remains a separate human decision;
- first live scope is constrained to synthetic or non-sensitive internal facts
  unless Adam explicitly approves more;
- kill switch and rollback are documented;
- Graphify still cannot approve, execute, mutate, deploy, change permissions,
  or read live business systems.

Validation: ship-readiness review, security review, connector tests,
integration dry-run, and owner approval.

Stop condition: stop if any live-adapter control is missing or if the owner
has not explicitly approved live enablement.

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
- Whether Graphify should consume acceleration facts from GitHub records, a
  future API, local files, or a cloud event path. Initial recommendation:
  defer transport until after local approval, authority, and evidence
  contracts are stable.

## Closed Decisions And Completed Gates

- 2026-06-27T17:15:09-06:00: GA-C1 selected ignored local developer artifact
  retention for preview output under `tmp/graphify-acceleration-preview/`.
  Generated preview output must not be committed by default and does not imply
  Graphify ingest.
- 2026-06-27T17:41:51-06:00: GA-C2 implemented the ignored local preview
  command using synthetic local records only. The preview command is an
  operator inspection surface, not a retained evidence, relay, approval,
  source-of-truth, or Graphify ingest path.
- 2026-06-27T18:06:31-06:00: GA-C3 and GA-C4 completed local preview
  diff/cache checks plus the operator preview handoff. The safe diff reports
  fact IDs and fingerprints only and remains non-authoritative, non-ingest,
  non-evidence, non-relay, and non-mutating.

## Next Safe Slice

The next GAIL-side slice, when selected, should be:

```text
Post-Graphify preview slice:
Report the GA-B/GA-C local readiness package back to the agentic multi-agent
agent builder for a revised orchestrated plan, or return to Chunk Twenty local
governed approval actions if Adam resumes the default Rev 2 build path.
```

That handoff should treat the GA-C preview and diff tools as local inspection
surfaces only. Do not proceed into Phase D contract publication, Phase E
adapter boundary design, live Graphify ingest, HTTP/cloud placement, live
connectors, live business-system reads, AG Operations Workspace / Microsoft
365 content access, Freedom runtime changes, or execution authority without an
explicit owner decision.
