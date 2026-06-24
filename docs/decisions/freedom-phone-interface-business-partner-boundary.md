# Freedom Phone Interface And Business Partner Boundary

Created: 2026-06-21T20:45:31-06:00
Last Updated: 2026-06-23T22:09:46-06:00
Status: active decision
Owner: Adam Goodwin

## Purpose

This decision defines the boundary between Freedom Engine and GAIL AI Operating
System Rev 2 before any portal, Android, worker, connector, hosted relay, or
runtime integration work proceeds.

Freedom is Adam's current operating partner OS. It is also the preferred
phone-side operator link and the strongest existing agentic business partner
surface. Rev 2 is the governed mission, policy, relay, worker-claim,
connector-boundary, and evidence spine.

The systems should converge through records and bridge contracts. They should
not converge through a wholesale source merge, generated config import, or live
runtime coupling.

## Decision

Freedom is the core operator interface and the phone-side anchor for Rev 2.
Rev 2 must not build a competing native phone app. Future phone-side work
should augment Freedom through governed bridge contracts, summaries, links,
signals, and fallback views unless Adam explicitly reverses this decision.

Freedom is also preserved and elevated as a high-level agentic business partner
capability source. Its self-learning, research, programming-request handling,
agent and tool calling, tool selection, business-memory feedback loops,
voice/mobile interaction, and operator-run judgment are product capabilities to
translate into governed records. They are not approved runtime behavior inside
Rev 2 yet.

Rev 2 remains the durable technical spine:

- mission intent and run state;
- policy and permission gates;
- connector profiles that are not credentials;
- relay envelopes and relay records;
- single-worker claim semantics;
- evidence truth and validation records;
- private GitHub-backed source and audit trail.

## Ownership Boundary

| Area | Freedom owns or informs | Rev 2 owns |
|---|---|---|
| Phone operator link | Intent capture, approval review, pause/resume, interruption, degraded-state truth, and mobile continuity. | The record contracts, policy decisions, relay state, evidence references, and approval requirements exposed to the phone link. |
| Agentic business partner UX | Business partner interaction model, voice/mobile experience, learning loops, research flows, and operator-run judgment. | Governed translation of those capabilities into mission candidates, evidence, learning, research, memory references, and action-intent records. |
| Runtime execution | Existing Freedom runtime remains outside Rev 2 until a later approved integration chunk. | Local no-network proof semantics, connector boundaries, trusted-worker claims, and evidence validation. |
| Data and memory | Existing Freedom stores remain Freedom-owned and out of Rev 2. | Safe summaries, references, redaction notes, policy outcomes, and evidence records. |
| Tool and agent calling | Freedom concepts may inform routing and tool-choice design. | Any future tool call requires a Rev 2 connector profile, policy gate, approval class, dry-run test, action log, and rollback note. |

## What Freedom May Feed Into Rev 2

Freedom may later feed Rev 2 through bounded bridge records only:

- safe operator intent summaries;
- phone-side approval, pause, resume, interruption, and hold-state signals;
- operator-run lifecycle summaries;
- safe evidence summaries and reference links;
- learning signals and memory references without raw memory payloads;
- research findings with source references and confidence notes;
- programming-request summaries as mission candidates;
- action-request candidates;
- agent/tool-calling intent candidates;
- device and environment capability summaries without secrets, tokens,
  generated config, provider state, raw logs, or local runtime dumps.

Every inbound Freedom record must be treated as untrusted input until Rev 2
validates its shape, data class, approval class, references, stale-state status,
and policy result.

## What Rev 2 May Feed Back To Freedom

Rev 2 may later expose to Freedom:

- mission and run status summaries;
- approval requests and denial reasons;
- hold, resume, cancel, and review prompts;
- safe evidence summaries and reference-only evidence links;
- policy decision summaries;
- worker claim status summaries;
- connector-profile names and capability classes, not credentials;
- next-review queue summaries;
- recovery or blocked-state notes.

Rev 2 must not feed Freedom raw secrets, connector credentials, raw client data,
raw logs, raw audio, unredacted memories, provider state, local relay files, or
unapproved execution authority.

## Neutral Bridge Record Envelope

All future Freedom bridge records should start from this common envelope before
any schema or code is created:

| Field | Meaning |
|---|---|
| `bridge_record_id` | Stable Rev 2-owned identifier for the bridge record. |
| `source_system` | `freedom-engine`, `gail-rev-2`, or a later approved source. |
| `target_system` | Intended receiving system. |
| `record_type` | One of the approved bridge record kinds below. |
| `summary` | Human-readable safe summary. No raw sensitive payloads. |
| `reference_uris` | Links or local references to approved evidence or source material. |
| `correlation_ids` | Mission, run, relay, evidence, or external IDs needed for traceability. |
| `data_class` | Public, internal, private, sensitive, or blocked. |
| `approval_class` | Planning-only, review-required, approved-internal, restricted-external, or blocked. |
| `policy_status` | Proposed, accepted, denied, expired, blocked, or superseded. |
| `redaction_notes` | What was removed or summarized. |
| `created_at` | Record creation timestamp. |
| `expires_at` | Required for approval, action, and agent/tool-intent records. |

## Initial Bridge Record Shapes

| Record type | Purpose | Minimum extra fields | Blocked content |
|---|---|---|---|
| `freedom_safe_summary` | Carry a phone or business-partner summary into Rev 2. | `topic`, `source_ref`, `operator_context`, `confidence_note` | Raw transcripts, contacts, emails, memories, logs, screenshots, or secrets. |
| `freedom_run_signal` | Translate Freedom operator-run state into Rev 2 mission/run context. | `freedom_run_ref`, `run_state`, `requested_next_state`, `checkpoint_ref` | Direct execution instruction or hidden runtime state. |
| `freedom_evidence_reference` | Reference evidence without importing payloads. | `evidence_kind`, `evidence_ref`, `observed_at`, `validation_hint` | Embedded files, raw log bodies, provider traces, or binary artifacts. |
| `freedom_learning_signal` | Preserve self-learning and business-memory value as governed learning input. | `learning_topic`, `memory_ref`, `lesson_summary`, `review_needed` | Raw memory records, contact data, email content, Supabase rows, or unredacted personal data. |
| `freedom_research_finding` | Convert research work into mission evidence or follow-up candidates. | `research_question`, `finding_summary`, `source_refs`, `uncertainty_note` | Live web-session state, credentials, browser cookies, or private-source payloads. |
| `freedom_action_request_candidate` | Carry a proposed action into Rev 2 for policy review. | `requested_outcome`, `action_class`, `connector_profile_ref`, `approval_needed`, `rollback_hint` | Live connector arguments, payment or send authority, destructive commands, or production changes. |
| `freedom_agent_tool_intent` | Preserve agent/tool-calling intent without granting execution. | `intent_summary`, `candidate_tool`, `required_capability`, `risk_tier`, `dry_run_expected` | Tool credentials, raw prompts that override policy, direct tool invocation payloads, or autonomous execution approval. |

## Phone Interface Rules

Freedom may be the first phone-side experience for:

- intent capture;
- approval review;
- interruption and hold/resume;
- mission status summaries;
- safe evidence review;
- degraded or offline truth statements;
- business-partner continuity.

Freedom must not become:

- the sole durable truth store for Rev 2;
- a direct local execution surface for Rev 2 workers;
- a place where Rev 2 sends credentials, raw logs, or raw sensitive payloads;
- an implied approval to import generated mobile runtime config;
- an implied approval to activate Freedom gateway, relay, voice, Supabase,
  desktop-host, email, or provider integrations.

The future browser/app shell should support Windows, Linux, Android tablet, and
ordinary browsers while treating Freedom as the core phone-side interface.
Browser work can provide review and fallback capability, but it must not
duplicate or replace Freedom's phone investment.

## Capability Preservation Track

Freedom's high-level business partner capabilities should be preserved this
way:

| Freedom capability | Rev 2 preservation path |
|---|---|
| Self-learning and learning reviews | Governed learning-signal records, evidence references, review queues, and memory-reference policy. |
| Research workflows | Research-finding records that can become mission evidence or follow-up mission candidates. |
| Programming-request handling | Mission candidates with acceptance criteria, evidence, and approval state. |
| Agent and tool calling | Agent/tool-intent candidates that remain planning-only until connector profiles and approval gates exist. |
| Tool selection | Planner input and capability matching, never direct execution approval. |
| Business-memory feedback loops | Memory references and safe summaries, not raw memory import. |
| Voice/mobile interaction | Capture and review surfaces only until voice/runtime activation is explicitly approved. |
| Operator-run judgment | Approval checkpoints, consequence review, policy reasons, and evidence quality gates. |

## Approval Gates Before Runtime Work

Before any Freedom runtime, code, or live bridge integration is allowed, a
future chunk must define and validate:

- the exact source files or API surfaces under review;
- the target Rev 2 record schema;
- secret and generated-config exclusion checks;
- connector profiles and least-privilege capability scopes;
- dry-run and stale-state tests;
- approval classes and denial behavior;
- action logging and evidence writeback;
- rollback or hold behavior;
- owner approval for any external, destructive, sensitive, or production-like
  action.

## Stop Triggers

Stop and require explicit owner approval before:

- copying Freedom source into active Rev 2 source;
- reading or recording secret values from Freedom env, generated config, local
  state, provider setup, or runtime files;
- modifying Freedom code;
- importing Freedom generated mobile runtime config;
- importing `.local-data`, APKs, build outputs, logs, provider state, contacts,
  email data, memories, raw transcripts, Supabase data, or release artifacts;
- activating Freedom gateway, relay, voice, desktop-host, Supabase, email,
  Vercel, OpenAI, LiveKit, or mobile runtime behavior from Rev 2;
- treating Freedom's A3 autonomy posture as approved for Rev 2;
- building a competing native phone app for Rev 2.

## Current Result

Chunk Sixteen is documentation and architecture boundary work only. It creates
no source import, no runtime bridge, no portal scaffold, no Android build, no
M365 adapter, no hosted relay, no worker bootstrap, no live connector, no client
data workflow, and no production behavior.
