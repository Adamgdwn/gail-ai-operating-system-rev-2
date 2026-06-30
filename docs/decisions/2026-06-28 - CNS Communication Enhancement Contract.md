# CNS Communication Enhancement Contract

Document type: coordination contract
Date: 2026-06-28
Saved: 2026-06-28T18:44:28-06:00
Last Updated: 2026-06-29T19:31:31-06:00
Status: draft complete for builder orchestration (2026-06-28T18:44:28-06:00)
Owner: Adam Goodwin

## Purpose

This contract gives the agentic multi-agent agent builder a compact target for
the communication layer between GAIL AI Operating System Rev 2, Freedom,
Graphify, Codex and future coding agents, and the future AG Operations
Workspace / Microsoft 365 environment.

The goal is not to modify Graphify or merge the systems. The goal is to shape
Rev 2 so an enhanced Graphify layer can move faster by receiving clean,
traceable, authority-aware facts and by returning compact relationship context
to Freedom, GAIL OS, and future application surfaces.

This contract is planning and coordination only. It does not approve live
Microsoft 365 access, tenant/admin consent, browser login, live Microsoft Graph
calls, Planner writes, Graphify ingest, cloud placement, production service
behavior, source-of-truth migration, runtime consolidation, R4 live execution,
or authority expansion.

## 2026-06-29 Boundary Addendum

Use
`docs/decisions/2026-06-29 - Graphify Boundary Transfer And GAIL OS Informing Plan.md`
as the active GAIL OS route for the Graphify boundary transfer.

This contract's "read-only relationship context" language means no Graphify
approval, execution, R-level escalation, source-system mutation, or canonical
evidence ownership. It does not forbid explicitly approved, bounded,
idempotent relationship-memory writes into Graphify. Any such write remains a
separate owner-gated learning lane.

## Current System Roles

| System | Communication role | Boundary |
|---|---|---|
| GAIL AI Operating System Rev 2 | Authority, evidence, mission/action state, connector posture, OKP records, and communication trace spine. | Owns policy and evidence, but does not become a raw data lake or live connector by implication. |
| Freedom | Operator continuity surface, executive cognition, business partner reasoning, approval briefing, and human-facing learning loop. | Must not bypass GAIL OS authority or receive hidden write authority. |
| Graphify | Fast relationship intelligence and neuronal pathway layer for entity, context, proof, and similarity traversal. | Not approval, not execution, not raw tenant-content ingestion, not source mutation, and not the canonical authority ledger. |
| AG Operations Workspace / Microsoft 365 | Future tactile business body for identity, records, collaboration, tasks, communications, forms, and action logs. | Planning-only in Rev 2 until a connector-promotion gate approves scopes, retention, audit, rollback, and human approval. |
| Codex, builder, and future coding agents | Governed construction workers and handoff producers. | Build authority is repo-scoped and evidence-bound; no live business authority or R5 delegation by implication. |

## Relationship To Existing Contracts

This contract sits above the existing lower-level graph-fact work:

- `docs/contracts/2026-06-28 - Graphify Fact Export Contract.md`
- `contracts/json-schema/graph-fact.schema.json`
- `packages/uaos-core/src/gail_ai_operating_system/graphify_acceleration.py`
- `packages/uaos-core/src/gail_ai_operating_system/operating_knowledge.py`

Those artifacts define current or proposed local shapes such as
`GraphifyAccelerationRecord`, `GraphFact`, and `OperatingKnowledgePacket`.
This document does not replace them. It defines the cross-system communication
rules that should decide when those records are created, how they are linked to
Freedom and application signals, and what Graphify is allowed to do with them.

Important reconciliation: Graphify-owned local CNS API routes may exist for
proof work, and the existing Graphify Fact Export Contract preserves an
extraction/write preference for GAIL OS graph facts. This communication
contract does not promote any Graphify HTTP write path. Any persistent Graphify
CNS store mutation remains owner-gated and should be handled as a connector-like
promotion step.

## Core Design Rule

Every meaningful cross-system message should be:

- traceable through a stable `cns_trace_id`;
- idempotent through a deterministic fingerprint or `idempotency_key`;
- tied to GAIL OS authority state;
- safe to summarize without raw payload retention;
- replayable from durable local records before any live adapter exists;
- readable by Freedom as a relationship brief;
- convertible into sanitized Graphify facts later;
- stoppable before live business-system action.

Graphify should accelerate recall, relationship ranking, route selection,
similar-mission lookup, evidence linkage, and learning feedback. It should not
approve, execute, mutate source systems, or override GAIL OS policy.

## Shared Identity Contract

`cns_trace_id` is the thread that binds the central nervous system loop.

Suggested v0 format:

```text
cns-YYYYMMDD-<12-safe-lowercase-hex-or-base32-chars>
```

Rules:

- create one `cns_trace_id` when a new operator intent, application signal,
  builder task, or system observation enters GAIL OS;
- propagate it to the related `mission_id`, `action_id`, `evidence_id`,
  `okp_id`, `GraphifyAccelerationRecord`, Freedom brief, app event, builder
  handoff, commit reference, and validation record when present;
- never encode customer names, tenant IDs, file names, emails, phone numbers,
  secrets, raw payload hashes, or provider IDs directly inside it;
- do not use it as the only authorization check;
- do not replace canonical entity IDs with it.

Related identifiers:

| Field | Purpose | Durability |
|---|---|---|
| `cns_trace_id` | End-to-end CNS thread across systems. | Durable, safe to reference in docs and graph facts. |
| `correlation_id` | Per-request or per-process transport trace. | May rotate; useful for logs and HTTP/API probes. |
| `idempotency_key` | Prevents duplicate event/action processing. | Deterministic for retry-sensitive records. |
| `fingerprint` | Detects fact/content delta without raw payload recrawl. | Deterministic and safe; already used in Graphify acceleration and OKP work. |
| `source_ref` | Safe reference to canonical source record. | Must stay non-secret and non-absolute. |

## Message Envelopes

The builder should treat these as named communication shapes. They do not all
need to become code at once, but future chunks should avoid inventing new names
for the same concepts.

### SignalPacket

Inbound signal from Freedom, AG Operations Workspace, an application surface,
or a coding-agent handoff into GAIL OS.

Minimum fields:

| Field | Meaning |
|---|---|
| `schema_version` | Example: `rev2.signal-packet.v0`. |
| `cns_trace_id` | CNS thread. Created if absent and the source is allowed. |
| `source_system` | `freedom`, `ag-operations-workspace`, `gail-os`, `codex`, `builder`, or another approved profile. |
| `source_ref` | Safe non-secret reference to the source record. |
| `signal_type` | Closed set such as `operator_intent`, `workspace_event`, `build_handoff`, `evidence_observed`, `relationship_hint`. |
| `summary` | Sanitized short description, not raw content. |
| `observed_at` | Timestamp from source or GAIL OS observation time. |
| `authority_level` | Expected R-level classification before action. |
| `autonomy_level` | Expected A-level posture. |
| `risk_tier` | Risk tier before GAIL OS policy review. |
| `data_classification` | `public`, `internal`, `synthetic`, or approved restricted class. |
| `raw_payload_retained` | Must be `false` under the current boundary. |
| `links` | Optional safe entity IDs: mission, action, evidence, OKP, app item, commit, handoff. |

### FreedomRelationshipBrief

Read model from GAIL OS and Graphify context into Freedom. This is the operator
briefing surface, not an execution command.

Minimum fields:

| Field | Meaning |
|---|---|
| `cns_trace_id` | The CNS thread Freedom is being asked to reason about. |
| `mission_id` | Current or candidate GAIL OS mission. |
| `brief_type` | `mission_context`, `approval_request`, `learning_feedback`, `risk_warning`, or `similar_case`. |
| `operator_question` | The human-readable decision or attention point. |
| `relationship_map` | Compact links: entities, missions, evidence, prior outcomes, workspace items, and related commits. |
| `authority_snapshot` | Current R/A level, envelope status, human gate, and stop conditions. |
| `evidence_snapshot` | Safe summaries of evidence and proof state. |
| `options` | Candidate choices for Freedom/operator reasoning; not self-executing actions. |
| `confidence` | Confidence and source basis for the brief. |
| `graph_context_refs` | Optional Graphify references or query IDs, never raw graph dumps. |

### GraphifyFactBundle

Sanitized facts produced by GAIL OS for later Graphify acceleration. This
bundle should be compatible with the existing `GraphifyAccelerationRecord`,
`GraphFact`, and OKP direction rather than a competing model.

Minimum fields:

| Field | Meaning |
|---|---|
| `cns_trace_id` | CNS thread for the fact bundle. |
| `bundle_id` | Safe stable bundle ID. |
| `emitted_by` | GAIL OS module or approved builder/coding-agent handoff source. |
| `records` | One or more sanitized graph facts. |
| `fingerprint` | Deterministic bundle fingerprint for delta checks. |
| `authority_snapshot` | R/A level and envelope reference at emission time. |
| `contains_raw_payload` | Must be `false`. |
| `ingest_state` | `preview`, `queued`, `owner_gated`, `ingested`, or `rejected`. |

Rules:

- use existing `GraphifyAccelerationRecord` and `GraphFact` vocabulary where it
  fits;
- prefer safe typed edges over prose-only descriptions;
- keep facts small enough for Graphify to traverse quickly;
- do not require Graphify to crawl raw documents to reconstruct mission,
  authority, evidence, or build relationships;
- do not mutate the persistent Graphify CNS store until Adam explicitly
  approves an ingest proof.

### AppSignalEnvelope

Inbound observation from AG Operations Workspace or a future product
application surface. Under the current boundary, this is synthetic or dry-run
only.

Minimum fields:

| Field | Meaning |
|---|---|
| `cns_trace_id` | Existing or newly created CNS thread. |
| `app_surface` | Planner, Lists, SharePoint, Teams, Exchange, Forms, CRM, dashboard, or another approved connector profile. |
| `workspace_ref` | Safe non-secret item reference, not raw content. |
| `event_kind` | `created`, `updated`, `commented`, `assigned`, `completed`, `exception_detected`, etc. |
| `summary` | Sanitized event summary. |
| `requested_outcome` | Optional outcome request for Freedom/GAIL OS reasoning. |
| `authority_level` | Usually R0/R1 until a connector promotion gate says otherwise. |
| `dry_run` | Must be `true` until live connector promotion. |
| `raw_payload_retained` | Must be `false`. |

### AppActionEnvelope

Future outbound action proposal from GAIL OS into AG Operations Workspace or
another application. This is not approved for live use yet.

Minimum fields:

| Field | Meaning |
|---|---|
| `cns_trace_id` | CNS thread. |
| `mission_id` / `action_id` | GAIL OS authority-controlled action identity. |
| `target_system` | Approved connector profile. |
| `target_ref` | Safe target reference, not raw provider payload. |
| `action_type` | Closed action type such as `draft_task`, `create_record`, `send_message`, `update_status`. |
| `authority_envelope_id` | Required for R4 and any future delegated action. |
| `dry_run` | Must be `true` until explicitly approved. |
| `idempotency_key` | Required before retryable writes. |
| `rollback_plan` | Required for any future live write where rollback is possible. |
| `stop_conditions` | Human-readable and machine-checkable stops. |

### BuildHandoffFact

Durable construction signal from Codex, the builder, or another coding agent
into the CNS layer.

Minimum fields:

| Field | Meaning |
|---|---|
| `cns_trace_id` | Thread for the build or proof chunk. |
| `chunk_id` | Work packet or chunk name. |
| `repo` | Repository slug. |
| `commit` | Commit SHA if available. |
| `ci_run` | CI run or validation reference if available. |
| `files_changed` | Safe relative file paths. |
| `checks_run` | Commands and pass/fail summaries. |
| `authority_boundary` | What was not approved or not executed. |
| `next_decision` | The next owner or builder decision. |

This gives Graphify and Freedom a compact memory of what changed without
recrawling full transcripts or treating chat as the source of truth.

## Communication Flow

### 1. Observe

Freedom, AG Operations Workspace, product apps, Graphify context, or coding
agents produce a `SignalPacket`. GAIL OS validates the source, assigns or
accepts a `cns_trace_id`, classifies authority/risk, and records a safe OKP or
mission candidate.

### 2. Reason

GAIL OS may request read-only Graphify context or existing OKP context, then
creates a `FreedomRelationshipBrief`. Freedom uses the brief to reason with
Adam, propose options, request clarification, or return operator intent.

### 3. Govern

GAIL OS validates the proposed mission/action, applies the R0-R5 authority
ladder, checks the A-level autonomy boundary, requires AuthorityEnvelope
coverage where needed, blocks R5 agent action, and records the decision.

### 4. Evidence

Completed, stopped, rejected, or dry-run actions create `EvidencePacket`
records and, where useful, `OperatingKnowledgePacket` records. These records
retain safe summaries and links, not raw payloads.

### 5. Learn

GAIL OS prepares `GraphifyFactBundle` records from missions, actions,
authority envelopes, evidence, OKP records, and build handoffs. Initially these
stay local as preview/replay data. Later, with Adam's approval, Graphify may
ingest sanitized facts through the approved Graphify write path and return
read-only relationship context.

### 6. Act

Future AG Operations Workspace or product-app actions use `AppActionEnvelope`
records. Live actions remain paused until a connector-promotion gate approves
identity, scopes, audit, retention, idempotency, rollback, human gates, and
stop conditions.

## Graphify Acceleration Requirements

To let enhanced Graphify work quickly, Rev 2 should prepare facts that are:

- pre-shaped: entity IDs, entity types, relationships, status, timestamps,
  authority, evidence links, and fingerprints are explicit;
- delta-friendly: Graphify can detect unchanged facts without reading the
  source record again;
- authority-aware: every fact carries R/A level context and envelope links when
  relevant;
- safe-summary only: no raw provider content, raw logs, raw transcripts, raw
  audio, secrets, tokens, or client payloads;
- edge-rich: facts carry typed relationships such as `belongs_to`,
  `authorized_by`, `evidenced_by`, `references`, `derived_from`, `blocks`,
  `supersedes`, and `related_to`;
- replayable: local preview/replay should prove ordering, stale-state
  protection, and idempotency before live ingest;
- briefable: Freedom can receive small relationship briefs instead of long
  graph dumps;
- builder-readable: the agentic builder can inspect clear chunk boundaries,
  validation evidence, and next decisions.

## No-Fallback Boundaries

- Do not use this contract to approve live Microsoft 365 access.
- Do not open browser login, OAuth, tenant/admin consent, or scope expansion.
- Do not call live Microsoft Graph, write Planner, send Teams/Outlook, or read
  tenant content.
- Do not mutate the persistent Graphify CNS store without a specific owner
  approval for an ingest proof.
- Do not use Graphify as an authority, approval, execution, or source mutation
  engine.
- Do not let Freedom, Graphify, Codex, the builder, or AG Operations bypass
  GAIL OS policy.
- Do not treat R4 live-executor code on `main` as approval to run live R4.
- Do not retain raw payloads, secrets, logs, transcripts, audio, provider
  exports, or client data in cross-system communication records.
- Do not consolidate Rev 2, Freedom, Graphify, and AG Operations into one
  runtime without the build consolidation decision process.

## Builder Chunk Request

The builder should convert this contract into bounded chunks. A safe sequence
would be:

1. CE-1 - Trace identity and envelope glossary

   Define `cns_trace_id`, `correlation_id`, `idempotency_key`, and the named
   envelopes above as documentation or local schemas. Stop before runtime
   adapters, schema publication, or live connectors.

2. CE-2 - Local communication event ledger and replay proof

   Add a local append-only communication event record that can store synthetic
   `SignalPacket`, `FreedomRelationshipBrief`, `GraphifyFactBundle`, and
   `BuildHandoffFact` examples. Prove replay, stale-state checks, and
   idempotency locally. Stop before Graphify ingest or cloud placement.

3. CE-3 - Freedom relationship brief read model

   Shape a compact read-only brief that Freedom can consume for mission
   context, approvals, risk warnings, and learning feedback. Stop before
   Freedom runtime changes unless a separate Freedom-side owner task approves
   them.

4. CE-4 - Graphify fact-bundle preview and delta cache alignment

   Tie the communication ledger to the existing Graphify acceleration preview
   and fingerprint work. Keep output ignored/local and prove deterministic
   deltas. Stop before persistent Graphify CNS store mutation.

5. CE-5 - AG Operations Workspace dry-run signal mapping

   Map future Microsoft 365 surfaces to `AppSignalEnvelope` examples using
   synthetic records only. Keep current M365 endpoints dry-run/no-live and stop
   before tenant consent, scope expansion, or provider calls.

6. CE-6 - Owner-gated Graphify ingest proof

   Only after CE-1 through CE-4 are green, Adam may approve a bounded local
   ingest proof using synthetic data, read-back validation, and rollback/delete
   notes. This is the first chunk that should explicitly say "Graphify ingest."

## Acceptance For Future Implementation

Future implementation chunks should satisfy these checks:

- every cross-system record has a `cns_trace_id`;
- every retryable event has an idempotency key or deterministic fingerprint;
- every action-like record carries authority/risk/autonomy context;
- all external application records remain dry-run until promoted;
- all Graphify-bound data is sanitized and raw-payload-free;
- Freedom receives relationship briefs, not hidden execution commands;
- Graphify returns context, not approval;
- local replay can prove ordering and stale-state behavior;
- validation evidence is recorded in the active work packet;
- CI or focused tests pass before commit/push.

## Current Status

This document is draft complete for builder orchestration as of
2026-06-28T18:44:28-06:00. It is ready to be sent to the agentic multi-agent
agent builder alongside:

- `docs/decisions/2026-06-28 - Local CNS Connection Proof Report.md`
- `docs/decisions/2026-06-28 - Current Main Stabilization Builder Report.md`
- `docs/decisions/2026-06-27 - Builder Graphify Freedom AG Operations Integration Summary.md`
- `docs/decisions/2026-06-27 - Graphify Acceleration Readiness Plan.md`

The next owner decision is whether the builder should produce a revised
orchestrated plan from this contract, or whether Rev 2 should resume local
implementation at Chunk Twenty / CE-1 style trace-envelope work.
