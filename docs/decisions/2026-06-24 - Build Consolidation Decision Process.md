# Build Consolidation Decision Process

Date: 2026-06-24
Recorded: 2026-06-24T12:22:39-06:00
Status: active decision process
Owner: Adam Goodwin

## Purpose

This record defines how to decide whether GAIL AI Operating System Rev 2,
Freedom Engine, and AG Operations should stay as separate builds, connect
through governed bridge records, or consolidate under one build.

The immediate owner direction is to let AG Operations finish its current
evolution before consolidation decisions are made. Rev 2 should not absorb
partially moving AG Operations work just to reduce the number of projects. The
decision must be based on system responsibility, evidence, and weak-layer risk.

## Current Decision

Do not fold AG Operations, Freedom, or Rev 2 into one build yet.

For now:

- AG Operations continues evolving as the live Microsoft 365 business substrate
  and operating workflow environment.
- Freedom remains the core operator interface and high-level agentic business
  partner surface.
- Rev 2 remains the clean governed mission, policy, relay, connector-boundary,
  approval-record, evidence, and worker spine.

A future consolidation decision must pass through this process before any repo
merge, runtime merge, connector activation, shared app shell, or source-of-truth
change.

## Decision Trigger

Run this decision process after AG Operations completes its current agentic
assistance and approval-loop evolution, or sooner only if continued separation
creates an obvious design failure.

The trigger should include evidence that AG Operations has a stable current
shape, such as:

- a named current agent lane, for example `M365 Coordinator Agent`;
- stable source surfaces, write surfaces, approval gates, and blocked actions;
- clear Agent Action Log and Decision Register roles;
- a tested local-only, G1, or approved supervised proof;
- explicit unresolved blockers, permission gaps, and rollback or pause notes;
- no unboxed in-progress repo state that would make the review stale.

## Options

| Option | Meaning | Use when |
|---|---|---|
| Keep separate | Each build owns a distinct product/system boundary. | Responsibilities are clear and integration is not yet worth the coupling cost. |
| Governed bridge | Systems stay separate but exchange safe summaries, links, action candidates, and evidence records. | The interaction is valuable but runtime and source ownership should remain isolated. |
| Fold under Rev 2 | Rev 2 becomes the primary technical build for the shared capability. | Rev 2 owns the durable contract and the other build has become a surface, adapter, or implementation detail. |
| Fold back into Freedom | Freedom owns the operator-facing capability and Rev 2 exposes only records or policy contracts. | The capability is mainly operator experience, phone continuity, voice/mobile, learning, or business-partner behavior. |
| Keep in AG Operations | AG Operations owns the capability as a business-system workflow. | The capability depends on live M365 records, human operating cadence, or tenant-native governance surfaces. |
| Retire or archive | Stop building a duplicate surface or bridge. | It only adds routing, ambiguity, or maintenance cost. |

## Evaluation Tests

A consolidation proposal must answer these tests before implementation:

| Test | Question |
|---|---|
| User job | Which user job does the capability serve: operator interface, governed execution spine, or business substrate? |
| Source of truth | Which system owns the canonical record after the change? |
| Runtime authority | Which system may execute, write, send, approve, or deny? |
| Data boundary | Does the change move secrets, raw logs, client data, M365 content, Freedom memory, or generated runtime config? |
| Approval boundary | Where is approval recorded, and how are suggested, approved, rejected, held, and executed states kept distinct? |
| Evidence boundary | Where does evidence live, and can later agents verify it without the chat thread? |
| Weak-layer risk | Does the proposal create a pass-through layer that owns no validation, policy, persistence, UX, or operational responsibility? |
| Feedback loop | Are tests, read-back proof, UI checks, or manual validation available at the boundary being changed? |
| Reversibility | Can the consolidation be backed out without breaking the live operating workflow? |
| Governance fit | Does the proposal change risk tier, autonomy, live connector access, production posture, or data classification? |

## Weak-Layer Rejection Rules

Reject or redesign a consolidation proposal if it creates any of these shapes:

- a bridge that only copies fields from one system to another without owning
  validation, redaction, stale-state checks, or evidence;
- duplicate approval states across AG Operations, Freedom, and Rev 2 with no
  single authoritative state;
- two operator cockpits competing for the same phone or daily workflow role;
- a browser surface that bypasses Freedom while claiming to be only a fallback;
- an adapter that depends on broad setup-helper grants or inherited runtime
  power instead of a purpose-built permission model;
- a source import that carries generated config, secrets, local state, raw logs,
  provider state, or client data;
- a shared model where failures cannot be traced to one owning system;
- a layer that exists because the projects are separate, not because it protects
  a real boundary.

## Preferred Review Process

1. Let AG Operations complete and box the current evolution.
2. Gather read-only evidence from the current Rev 2, Freedom, and AG Operations
   decision records and handoffs.
3. Create a small comparison packet with the options above.
4. Pick one narrow capability to test the decision, not the whole system.
5. Apply the evaluation tests and weak-layer rejection rules.
6. Record the owner decision as keep separate, bridge, fold, fold back, keep in
   AG Operations, retire, or defer.
7. Implement only the smallest reversible slice needed to prove the chosen
   direction.

## Current Non-Goals

This decision process does not approve:

- merging repositories;
- moving AG Operations source or live tenant content into Rev 2;
- importing Freedom source, generated runtime config, memory, local state, or
  provider data;
- activating Freedom runtime, gateway, voice, mobile, Supabase, email, or
  desktop-host behavior;
- activating Microsoft 365, QuickBooks, finance, billing, vendor, client-data,
  or production connectors;
- changing `project-control.yaml` risk tier, governance level, autonomy level,
  or repository model;
- building a competing native Rev 2 phone app.

## Stop Triggers

Stop for explicit owner approval before any consolidation work that would:

- change the durable source of truth;
- create or modify live connector credentials, app registrations, permissions,
  tenant settings, or hosted runtime infrastructure;
- read live M365 content, Freedom runtime data, secrets, raw logs, raw audio, or
  client data;
- change AG Operations, Freedom, or Rev 2 runtime behavior;
- replace Freedom as the core operator interface;
- move from planning-only records to external, destructive, sensitive, or
  production-like action.

## Completion Criteria

The decision process is complete only when a later review records:

- the AG Operations state being reviewed;
- the Rev 2 and Freedom state being reviewed;
- the selected option;
- rejected options and why;
- weak-layer findings;
- governance or risk changes, if any;
- the smallest reversible implementation slice;
- validation evidence;
- owner acceptance or deferral.

Until then, the standing decision is to keep the builds separate with no new
runtime coupling and no source consolidation.
