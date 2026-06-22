# Source Of Truth Map

Created: 2026-06-21T13:58:36-06:00
Last Updated: 2026-06-21T20:51:47-06:00
Status: active navigation
Owner: Adam Goodwin

## Purpose

This map identifies the active Rev 2 source-of-truth records, the copied v1
reference records, and the compact chunk route for moving from clean scaffold to
usable multi-device operating system.

Use this file when the question is "where should an agent look first?" or "what
is authoritative right now?"

## Core Rule

The source of truth is the governed Rev 2 record set, not a device.

The private GitHub repository `Adamgdwn/gail-ai-operating-system-rev-2`, its
`main` branch, and the active files listed below are the current durable spine.
Windows, Linux, Android, browser, Graphify, and future hosted relay surfaces are
access points, workers, viewers, or approval surfaces. They do not become
competing truth stores.

## Open First

| Order | Document | Use it for |
|---|---|---|
| 1 | `AGENTS.md` | Repo-local agent rules, material-work triggers, Graphify policy, and chunk close-out. |
| 2 | `START_HERE.md` | Current priorities, active pathway pointer, and stop triggers. |
| 3 | `docs/current-build-pathway.md` | Active chunk, validation ledger, compact future chunk map, and handoff. |
| 4 | `docs/context-map.md` | Task-specific context routing and files to avoid. |
| 5 | `project-control.yaml` | Use case, selected risk tier, selected governance level, required docs, and agent autonomy posture. |
| 6 | `docs/migration/source-inventory.md` | What was copied, what was excluded, and what remains reference-only. |
| 7 | `docs/migration/file-migration-decisions.md` | Which v1 files may be promoted, rewritten, archived, excluded, or held for later review. |
| 8 | `docs/decisions/freedom-phone-interface-business-partner-boundary.md` | Freedom phone-link, business-partner capability, neutral bridge record, and no-import boundary. |

## Active Rev 2 Controls

| Record | Current role |
|---|---|
| `project-control.yaml` | Selected project classification, risk tier, governance level, required controls, and A1 agent posture. |
| `AGENTS.md` | Working rules for agents in this repo. |
| `START_HERE.md` | Top-level active plan route and current stop triggers. |
| `docs/current-build-pathway.md` | Single active pathway, active chunk packet, validation log, and next handoff. |
| `docs/context-map.md` | Smallest-useful context routing by task. |
| `docs/source-of-truth-map.md` | Navigation map and compact build chunk route. |
| `docs/tool-permission-matrix.md` | Active tool, device, connector, and worker permission boundaries. |
| `docs/agent-runtime-instructions.md` | Active runtime scope, A1 autonomy, planning/execution separation, stale-state rules, and stop behavior. |
| `docs/agent-inventory.md` | Active agent-like roles, current statuses, autonomy posture, and non-approved future workers/surfaces. |
| `docs/model-registry.md` | Active model route posture and future model approval requirements. |
| `docs/prompt-register.md` | Active prompt and instruction register plus future runtime prompt approval requirements. |
| `docs/graphify-handoff-checkpoint.md` | Active read-only Graphify route, current graph/tool status, handoff payload contract, and stop boundaries. |
| `docs/architecture.md` | Active Rev 2 architecture for source spine, portal surfaces, workers, relay records, Graphify, connector boundaries, and verification ladder. |
| `docs/migration/source-inventory.md` | Migration source boundary and reference inventory. |
| `docs/migration/file-migration-decisions.md` | Active file-level migration queue, exclusions, and future migration stop triggers. |
| `docs/migration/freedom-engine-objective-review.md` | Objective external review of the downloaded Freedom Engine archive, Freedom phone-interface anchor posture, agentic business partner preservation track, and selective fold-in/fold-back boundaries. |
| `docs/decisions/freedom-phone-interface-business-partner-boundary.md` | Active Chunk Sixteen decision record defining what Freedom may feed into Rev 2, what Rev 2 may feed back, initial neutral bridge record shapes, and the no-import/no-runtime boundary. |
| `docs/standards/README.md` | Standards index. |
| `docs/policy/durable-development-engineering-policy.md` | Durable development policy. |
| `docs/standards/engineering-governance-by-use-case.md` | Use-case governance expectations. |
| `docs/standards/ship-ready-engineering-standard.md` | Completion labels and ship-readiness evidence gate. |

## Active Rev 2 Code

| Record | Current role |
|---|---|
| `packages/uaos-core/src/gail_ai_operating_system/mission_spine.py` | Local no-network mission envelopes, validation, deterministic planning, policy decisions, stop triggers, and JSON record store. |
| `tests/test_mission_spine.py` | Expanded local mission-spine behavior tests for stop triggers, policy gates, validation failures, and file boundaries. |
| `packages/uaos-core/src/gail_ai_operating_system/connector_registry.py` | Local planning-only connector profile schema, validation, JSON-safe serialization, dry-run request evaluation, and default-deny stop decisions. |
| `tests/test_connector_registry.py` | Local connector registry tests for planning-only profiles, live-capability rejection, client-controlled gates, dry-run-only decisions, JSON round trips, and duplicate IDs. |
| `packages/uaos-core/src/gail_ai_operating_system/graphify_handoff.py` | Local read-only Graphify route status and handoff candidate validation for approved graph references. |
| `tests/test_graphify_handoff.py` | Local Graphify handoff tests for route readiness, candidate validation, policy-gated dry-run actions, denied execution/mutation, evidence checks, and sensitive-boundary rejection. |
| `packages/uaos-core/src/gail_ai_operating_system/relay_envelope.py` | Local no-network relay envelope schema validation for intent, approval, status, evidence, and handoff records. |
| `tests/test_relay_envelope.py` | Local relay envelope tests for safe references, dry-run policy gates, malformed JSON shapes, stale or expired approvals, denied hosted relay or worker polling, and unsafe payload rejection. |
| `packages/uaos-core/src/gail_ai_operating_system/relay_store.py` | Local no-network relay record store proof for validated envelopes, status transitions, reference-only evidence records, and single trusted-worker claim attempts. |
| `tests/test_relay_store.py` | Local relay store tests for persistence, reload, policy-gated claim validation, stale state rejection, duplicate worker claim rejection, trusted worker boundaries, evidence safety, and reference-only payloads. |
| `packages/uaos-core/src/gail_ai_operating_system/local_proof_runner.py` | Local no-network proof runner that exercises one mission path from intent through policy, connector registry, relay envelope, relay store, trusted-worker claim, reference-only evidence, and completed relay status. |
| `tests/test_local_proof_runner.py` | Local proof-runner tests for complete mission-to-evidence proof, reference-only payload safety, and stop-trigger failure before relay records are written. |

## Active Placeholders To Promote

These files exist in Rev 2 but still need promotion or rewrite before code
migration:

| File | Needed promotion |
|---|---|
| `docs/risks/risk-register.md` | Replace example risk row with current Rev 2 risks and stop triggers. |

## Reference-Only Material

Copied v1 records under `docs/migration/reference/uaos-v1` are local evidence
and design input. They are not active Rev 2 controls until a later chunk
promotes, rewrites, or supersedes them.

Open these references only when the active chunk calls for them:

| Reference | Use before |
|---|---|
| `docs/migration/reference/uaos-v1/specs/uaos-final-shippable-plan.md` | Historical source for promoted Rev 2 architecture and future acceptance-test planning. |
| `docs/migration/reference/uaos-v1/specs/cross-device-source-of-truth-foundation.md` | Historical source for promoted Rev 2 multi-device source-of-truth architecture. |
| `docs/migration/reference/uaos-v1/specs/shared-relay-phone-cockpit-architecture.md` | Historical source for promoted Rev 2 relay, phone/tablet cockpit, worker polling, hosted relay, and no-tunnel architecture. |
| `docs/migration/reference/uaos-v1/controls/tool-permission-matrix.md` | Historical source for promoted Rev 2 tool permission controls. |
| `docs/migration/reference/uaos-v1/controls/agent-runtime-instructions.md` | Historical source for promoted Rev 2 runtime controls. |
| `docs/migration/reference/uaos-v1/specs/connector-registry-client-gateway-boundary.md` | Historical source for promoted Rev 2 connector boundary architecture and future connector registry migration. |
| `docs/migration/reference/uaos-v1/specs/microsoft-365-business-environment-boundary.md` | Historical source for promoted Rev 2 M365 planning-only architecture and future inventory-only activation decision. |
| `docs/migration/reference/uaos-v1/requests/REQ-0055-local-relay-envelope-validator.md` | Relay envelope code/test migration. |
| `docs/migration/reference/uaos-v1/requests/REQ-0056-local-relay-record-store-worker-claim-proof.md` | Relay store and single-worker claim migration. |

## External Local Reference Material

The AG Operations Microsoft 365 setup repo is a local orientation source for
future bridge design, not an active Rev 2 source of truth:

`C:\Users\adamg\01. Code Projects\AG Operations Workspace Setup`

Open these files only for approved M365 bridge, connector, cockpit, or
cross-workspace architecture work:

| Reference | Use before |
|---|---|
| `M365_STAGE_9_AGENTIC_OS_BRIDGE_READINESS.md` | Future M365 adapter or bridge posture decisions. |
| `M365_GRAPHIFY_UAOS_ALIGNMENT.md` | Deciding the M365, Graphify, and Rev 2 split. |
| `docs/AGENTIC_M365_READINESS.md` | Mapping M365 G0-G4 readiness to Rev 2 connector and approval levels. |
| `config/M365_STAGE_9_AGENT_CAPABILITY_MODEL.json` | Candidate M365 Coordinator and Support Agent capability boundaries. |
| `config/M365_STAGE_9_BRIDGE_READINESS_CONTROL.json` | Adapter contracts, risk controls, app posture options, and graduation gates. |
| `docs/CARD_PLAN_AGENT_CONTROL_PLANE.md` | Agent Action Log, Decision Register, Tool Permission Review, and approval-control surface design. |
| `docs/WORKSPACE_CHUNK_7_FINAL_USABILITY_WALKTHROUGH.md` | Current M365 workspace handoff state and carried-forward blockers. |

Do not read or copy `M365_ENVIRONMENT.local.env`, live Microsoft 365 tenant
content, OneDrive content, raw logs, client data, secrets, permission payloads,
or setup-helper credentials into Rev 2.

The downloaded Freedom Engine archive is an external orientation source for
operating-partner runtime, the preferred future phone-interface anchor,
self-learning, research, agent/tool calling, business memory,
mobile/gateway/desktop-host, Action Fabric, Device Mesh, storage-map, and
operator-run design:

`C:\Users\adamg\Downloads\the-freedom-engine-os-main.zip`

Open the active review first:

| Reference | Use before |
|---|---|
| `docs/migration/freedom-engine-objective-review.md` | Deciding whether a Freedom concept should be translated into Rev 2, held in Freedom, or bridged later. |
| `docs/decisions/freedom-phone-interface-business-partner-boundary.md` | Deciding what may cross between Freedom and Rev 2 before app-shell, Android, bridge, connector, worker, or runtime work. |

Do not bulk-copy Freedom source into Rev 2. Do not read, copy, summarize, or
commit Freedom secret values, generated mobile runtime config, `.local-data`,
build outputs, APKs, provider state, Supabase runtime data, contacts, email
data, memories, raw transcripts, logs, or release artifacts. Freedom remains
Adam's current operating partner OS, high-level agentic business partner, and
preferred future phone-side operator link; Rev 2 remains the clean governed
mission, relay, policy, and worker spine until a later bridge chunk changes
that boundary explicitly.

## Device Roles

| Surface | Rev 2 role | Boundary |
|---|---|---|
| Windows | Current operator workspace and future trusted worker. | May edit/push Rev 2 repo and run local validation; live business connectors remain blocked until approved. |
| Linux | Superseded v1 reference host and future trusted worker clone. | Not the Rev 2 project home; future Linux work must pull from private GitHub and preserve Rev 2 controls. |
| Android phone | Freedom-anchored future operator link. | Freedom is the preferred phone-interface anchor candidate for intent capture, approval, pause/resume, safe evidence summaries, and business-partner continuity; no local execution, raw secrets/logs, generated config import, direct connector access, or runtime activation without a bounded later chunk. |
| Android tablet | Future review cockpit. | Larger evidence and status review surface; no unrestricted connector or filesystem access. |
| Browser | Shared cockpit surface across desktop and mobile. | Reads/writes governed records through approved local or relay paths; must not become a second source of truth. |
| Private GitHub | Canonical durable spine. | Commits, request records, issues/PRs, relay references, and evidence links; no secrets or unredacted sensitive payloads. |
| Graphify | Knowledge spoke. | Read-only handoff and graph references; recommendations are not execution approval. |
| Microsoft 365 / AG Operations | Future business substrate and identity/records/signals spoke. | Planning-only in Rev 2; feed cockpit through approved metadata, safe summaries, action logs, decision records, and links only after connector boundaries exist. |
| Freedom Engine | Current operating partner OS, high-level agentic business partner, and preferred future phone-interface anchor candidate. | Reference and bridge-planning only; self-learning, research, agent/tool calling, business memory, voice/mobile, and operator-run capabilities must be preserved and elevated through later safe contracts; no runtime merge, generated config, live provider access, code import, or Freedom modification without a bounded later chunk. |

## Compact Build Chunk Map

These are planning boundaries for future work. The active chunk and validation
ledger remain in `docs/current-build-pathway.md`.

| Phase | Chunk range | Purpose |
|---|---|---|
| Phase 1 - Active controls | Chunks Four to Eight | Promote Rev 2 navigation, permission, runtime, architecture, and migration-decision controls. |
| Phase 2 - File migration and initial build-out | Chunks Nine to Fifteen | Migrate/rewrite the no-network mission spine, connector registry, enhanced Graphify handoff checkpoint, relay envelope, relay store, tests, and proof runner. |
| Phase 3 - First usable portal | Chunks Sixteen to Twenty-One | Define the Freedom phone-interface and agentic business partner preservation boundary, choose the browser/app shell around that anchor, then build approval, evidence, and handoff views. |
| Phase 4 - Multi-device worker model | Chunks Twenty-Two to Twenty-Six | Add Windows/Linux worker bootstrap, role checks, GitHub-backed relay records, and conflict recovery. |
| Phase 5 - Full system build | Chunks Twenty-Seven onward | Evaluate hosted relay, notifications, approved connector activation, Client Gateway boundaries, vendor intelligence, runbooks, pilot, and release decision. |

## Stop Triggers

Stop and require explicit owner approval before:

- live Microsoft 365 content reads, Outlook or Teams sends, Entra/admin/security
  changes, permission changes, or tenant changes;
- QuickBooks, accounting, invoice, payment, billing, finance, vendor-account, or
  money movement actions;
- client data access, client workspace creation, or client-visible AI findings;
- secrets, raw credentials, raw logs, raw audio, or unredacted sensitive payloads
  leaving the trusted worker boundary;
- hosted relay, persistent worker service, public inbound worker access, or
  production deployment;
- destructive filesystem, Git, account, infrastructure, or provider changes.

## Next Action

Begin Chunk Seventeen: choose the app shell around the Freedom phone anchor and
Rev 2 local proof runner. Keep the next chunk bounded to shell choice and
initial structure only. Do not broaden into Freedom code import, generated
config reads, Freedom modification, Freedom runtime/provider activation, a
competing native Android phone surface, M365 adapter work, hosted relay, worker
bootstrap scripts, client data, live connectors, live business systems, or
production.
