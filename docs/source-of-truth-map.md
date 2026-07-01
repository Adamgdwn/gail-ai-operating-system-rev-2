# Source Of Truth Map

Created: 2026-06-21T13:58:36-06:00
Last Updated: 2026-07-01T12:43:18-06:00
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

New durable documents and work-tracking records should use date-stamped
filenames going forward, such as `YYYY-MM-DD - <title>.md`, unless an existing
required repo route, schema, or template requires a stable path. The controlling
rule is `docs/standards/2026-06-25 - Document Control Standard.md`: use the first durable
save/promote date in the filename, then update internal metadata on later
edits.

## Open First

| Order | Document | Use it for |
|---|---|---|
| 1 | `AGENTS.md` | Repo-local agent rules, material-work triggers, Graphify policy, and chunk close-out. |
| 2 | `START_HERE.md` | Current priorities, active pathway pointer, and stop triggers. |
| 3 | `docs/decisions/2026-06-29 - Graphify Boundary Transfer And GAIL OS Informing Plan.md` | Current GAIL OS informing packet while Freedom work is parked; Graphify boundary transfer, learning-lane rules, and next GI chunks. |
| 4 | `docs/decisions/2026-06-28 - Current Main Stabilization Work Packet.md` | Prior compact CMS-A/CMS-B/CMS-C GitHub catch-up packet, no-fallback boundaries, and validation record. |
| 5 | `docs/current-build-pathway.md` | Historical master pathway, validation ledger, compact future chunk map, and older handoff history. |
| 6 | `docs/context-map.md` | Task-specific context routing and files to avoid. |
| 7 | `project-control.yaml` | Use case, selected risk tier, selected governance level, required docs, and agent autonomy posture. |
| 8 | `docs/migration/source-inventory.md` | What was copied, what was excluded, and what remains reference-only. |
| 9 | `docs/migration/file-migration-decisions.md` | Which v1 files may be promoted, rewritten, archived, excluded, or held for later review. |
| 10 | `docs/decisions/freedom-phone-interface-business-partner-boundary.md` | Freedom phone-link, business-partner capability, neutral bridge record, and no-import boundary. |
| 11 | `docs/decisions/app-shell-command-center.md` | Browser-first command-center shell choice, options reviewed, dependency boundary, and multi-device posture. |
| 12 | `docs/decisions/2026-06-24 - Build Consolidation Decision Process.md` | Deciding whether Rev 2, Freedom, and AG Operations should remain separate, bridge, fold, or defer after AG Operations completes its current evolution. |
| 13 | `docs/decisions/2026-06-27 - Graphify Acceleration Readiness Plan.md` | GAIL-side plan for future sanitized graph-fact exports that let enhanced Graphify move faster without becoming an authority or execution layer. |
| 14 | `docs/decisions/2026-06-27 - Graphify Preview Retention Decision.md` | GA-C1 decision that local Graphify acceleration preview output is ignored disposable developer artifact output under `tmp/graphify-acceleration-preview/` by default. |
| 15 | `docs/decisions/2026-06-28 - Current Main Stabilization Builder Report.md` | Current compact builder-facing report after CMS-A/CMS-B/CMS-C, with current-main proof state, boundaries, path-forward impact, and next owner decision. |
| 16 | `docs/decisions/2026-06-28 - Local CNS Connection Proof Report.md` | First post-CMS local connection scout across Freedom, GAIL OS, and Graphify, including validation evidence and the next no-M365 connection-test lane. |
| 17 | `docs/decisions/2026-06-28 - CNS Communication Enhancement Contract.md` | Current builder-facing communication target for `cns_trace_id`, signal packets, Freedom relationship briefs, Graphify fact bundles, application envelopes, and build handoff facts. |
| 18 | `docs/decisions/2026-06-27 - Builder Graphify Freedom AG Operations Integration Summary.md` | Handoff summary for the agentic multi-agent builder, connecting builder CNS schema work, Rev 2 Graphify readiness, Freedom, Codex/future coding agents, and AG Operations Workspace / Microsoft 365 integration wishes. |
| 19 | `docs/decisions/2026-07-01 - UX And Agentic Linkage Review Remediation Plan.md` | Active PDCA remediation packet for UX, agentic linkage, feature-integrity doctrine, EX chunks, validation evidence, and handoffs. |

Startup direction as of 2026-06-29T19:31:31-06:00: the current active lane is
GAIL OS informing and Graphify boundary transfer. Freedom implementation work
is parked unless Adam explicitly routes the session there. This is not a
consolidation approval. Rev 2 remains the governed technical spine, Graphify is
relationship intelligence and graph memory, and GAIL OS authority/evidence do
not move into Graphify.

## Active Rev 2 Controls

| Record | Current role |
|---|---|
| `project-control.yaml` | Selected project classification, risk tier, governance level, required controls, and A1 agent posture. |
| `AGENTS.md` | Working rules for agents in this repo. |
| `START_HERE.md` | Top-level active plan route and current stop triggers. |
| `docs/decisions/2026-06-29 - Graphify Boundary Transfer And GAIL OS Informing Plan.md` | Active GAIL OS informing route for the refined Graphify boundary: no Graphify authority/execution transfer, but explicit owner-gated relationship-memory writes may exist. |
| `docs/decisions/2026-06-28 - Current Main Stabilization Work Packet.md` | Compact GitHub catch-up work packet and validation record for completed CMS-A/CMS-B/CMS-C stabilization. Read this before the large pathway when stabilization detail is needed. |
| `docs/decisions/2026-06-28 - Current Main Stabilization Builder Report.md` | Compact builder-facing closeout for CMS-C. Read this before asking the builder to revise orchestration after the current-main stabilization pass. |
| `docs/current-build-pathway.md` | Historical master pathway, active routing index, validation log, and older handoff history. |
| `docs/context-map.md` | Smallest-useful context routing by task. |
| `docs/source-of-truth-map.md` | Navigation map and compact build chunk route. |
| `docs/tool-permission-matrix.md` | Active tool, device, connector, and worker permission boundaries. |
| `docs/agent-runtime-instructions.md` | Active runtime scope, A1 autonomy, planning/execution separation, stale-state rules, and stop behavior. |
| `docs/agent-inventory.md` | Active agent-like roles, current statuses, autonomy posture, and non-approved future workers/surfaces. |
| `docs/model-registry.md` | Active model route posture and future model approval requirements. |
| `docs/prompt-register.md` | Active prompt and instruction register plus future runtime prompt approval requirements. |
| `docs/graphify-handoff-checkpoint.md` | Active Graphify route, current graph/tool status, handoff payload contract, and stop boundaries. Read-only means no authority, approval, execution, source mutation, or evidence-truth transfer. |
| `docs/architecture.md` | Active Rev 2 architecture for source spine, portal surfaces, workers, relay records, Graphify, connector boundaries, and verification ladder. |
| `docs/migration/source-inventory.md` | Migration source boundary and reference inventory. |
| `docs/migration/file-migration-decisions.md` | Active file-level migration queue, exclusions, and future migration stop triggers. |
| `docs/migration/freedom-engine-objective-review.md` | Objective external review of the downloaded Freedom Engine archive, Freedom core interface posture, agentic business partner preservation track, and selective fold-in/fold-back boundaries. |
| `docs/decisions/freedom-phone-interface-business-partner-boundary.md` | Active Chunk Sixteen decision record defining what Freedom may feed into Rev 2, what Rev 2 may feed back, initial neutral bridge record shapes, and the no-import/no-runtime boundary. |
| `docs/decisions/app-shell-command-center.md` | Active shell decision record selecting the Vite React TypeScript browser shell, now noting the later EX-2 read-only read-model proxy while still deferring service worker, command-center session auth, hosted relay, worker bootstrap, live connectors, desktop wrapper, and competing native phone app work. |
| `docs/decisions/2026-06-24 - Build Consolidation Decision Process.md` | Active decision process for reviewing whether Rev 2, Freedom, and AG Operations should stay separate, bridge, fold under one build, fold back, stay in AG Operations, retire, or defer after AG Operations boxes its current evolution. |
| `docs/decisions/2026-06-27 - Graphify Acceleration Readiness Plan.md` | Active GAIL-side plan for future Graphify acceleration readiness: Rev 2 should emit sanitized authority, action, evidence, connector, and system-state facts later, while Graphify remains relationship intelligence and never an execution authority. |
| `docs/decisions/2026-06-27 - Graphify Preview Retention Decision.md` | Active GA-C1 retention decision: local preview output stays ignored under `tmp/graphify-acceleration-preview/` and is not committed, retained as evidence, or treated as Graphify ingest. |
| `docs/decisions/2026-06-27 - Builder Graphify Freedom AG Operations Integration Summary.md` | Active coordination summary for the next builder handoff: describes what the agentic multi-agent builder added, what this Rev 2 pass added, and the desired integration between GAIL OS, Freedom, Codex/future coding agents, AG Operations Workspace / Microsoft 365, and Graphify. |
| `docs/decisions/2026-06-28 - Current Main Stabilization Builder Report.md` | Current-main addendum for the builder handoff: records green CMS-A/CMS-B proof state, CMS-C closeout, dry-run M365 boundary, paused login edge, and next owner decision lanes. |
| `docs/decisions/2026-06-28 - Local CNS Connection Proof Report.md` | First post-CMS local connection scout across Freedom, GAIL OS, and Graphify. Read this before rerunning connection proofs or deciding whether to move into a bounded local Graphify evidence-ingest proof. |
| `docs/decisions/2026-06-28 - CNS Communication Enhancement Contract.md` | Active communication contract for enhancing the Freedom/GAIL OS/Graphify/AG Operations loop through shared trace IDs, safe signal envelopes, Freedom relationship briefs, Graphify fact bundles, application action envelopes, and build handoff facts without approving live connectors or Graphify ingest. |
| `docs/decisions/2026-07-01 - UX And Agentic Linkage Review Remediation Plan.md` | Active PDCA remediation and handoff packet for UX, cross-surface agentic linkage, feature-integrity doctrine, EX-1 through EX-3 evidence, GLW-1 governed local write loop, and next-chunk selection. |
| `docs/standards/README.md` | Standards index. |
| `docs/standards/2026-06-25 - Document Control Standard.md` | Active document naming, dated filename, stable-path exception, and cross-build work-tracking rule for Rev 2, Freedom, and AG Operations Workspace. |
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
| `packages/uaos-core/src/gail_ai_operating_system/graphify_acceleration.py` | Local sanitized `GraphifyAccelerationRecord` contract, safety classifiers, pure Action/AuthorityEnvelope/EvidencePacket graph-fact builders, and deterministic fingerprints for future Graphify acceleration. No persistence, transport, adapter, ingest, or execution authority. |
| `tests/test_graphify_acceleration.py` | Local contract, sanitizer, emitter, fingerprint, and package-root export tests for Graphify acceleration records. |
| `packages/uaos-core/src/gail_ai_operating_system/graphify_acceleration_preview.py` | Local synthetic JSONL preview generator plus safe preview diff/cache inspector for GA-C2 through GA-C4. Writes only under the ignored preview boundary by default, supports print-only and diff modes, validates records before write or compare, and does not call Graphify or live systems. |
| `tests/test_graphify_acceleration_preview.py` | Local preview tests for deterministic output, path safety, invalid-record rejection before write, print-only mode, JSONL structure, and safe added/changed/unchanged/removed diff behavior against missing, empty, invalid, or duplicate previous preview caches. |
| `scripts/write-graphify-acceleration-preview.ps1` | Windows wrapper for the local preview command. It sets `PYTHONPATH` to the repo source folder and supports preview write, print-only, diff, and diff-against modes; it does not install services, schedule jobs, call Graphify, or read live systems. |
| `packages/uaos-core/src/gail_ai_operating_system/relay_envelope.py` | Local no-network relay envelope schema validation for intent, approval, status, evidence, and handoff records. |
| `tests/test_relay_envelope.py` | Local relay envelope tests for safe references, dry-run policy gates, malformed JSON shapes, stale or expired approvals, denied hosted relay or worker polling, and unsafe payload rejection. |
| `packages/uaos-core/src/gail_ai_operating_system/relay_store.py` | Local no-network relay record store proof for validated envelopes, status transitions, reference-only evidence records, and single trusted-worker claim attempts. |
| `tests/test_relay_store.py` | Local relay store tests for persistence, reload, policy-gated claim validation, stale state rejection, duplicate worker claim rejection, trusted worker boundaries, evidence safety, and reference-only payloads. |
| `packages/uaos-core/src/gail_ai_operating_system/local_proof_runner.py` | Local no-network proof runner that exercises one mission path from intent through policy, connector registry, relay envelope, relay store, trusted-worker claim, reference-only evidence, and completed relay status. |
| `tests/test_local_proof_runner.py` | Local proof-runner tests for complete mission-to-evidence proof, reference-only payload safety, and stop-trigger failure before relay records are written. |
| `packages/uaos-core/src/gail_ai_operating_system/action.py` | Governed action schema, state machine, validation, and local JSON action store used by the GLW-1 local action request/decision loop. |
| `packages/uaos-core/src/gail_ai_operating_system/approval_actions.py` | Transport-independent approval decision functions and local approval decision store for approve/reject/hold/more-info records. |
| `packages/uaos-core/src/gail_ai_operating_system/local_action_loop.py` | GLW-1 local orchestration path from persisted mission to policy-gated action request, stale-protected approval decision, dry-run evidence packet, idempotency handling, and trace events. No live connector execution. |
| `packages/uaos-core/src/gail_ai_operating_system/read_model.py` | Shared trace, event, read-model, and Freedom relationship brief spine. It builds `GET /api/v1/read-model`, `GET /api/v1/traces/{cns_trace_id}`, and `GET /api/v1/freedom/relationship-briefs/{cns_trace_id}` payloads from local mission, action, approval, evidence, authority, connector, event, and Graphify-context refs without external calls or execution authority. |
| `tests/test_read_model.py` and `tests/test_api_read_model.py` | Core and authenticated API tests for shared read models, trace lookup, duplicate visibility, and read-only Freedom relationship briefs. |
| `apps/command-center` | Browser-first Vite React TypeScript command-center cockpit shell with a read-only multi-viewport operator hub over `GET /api/v1/read-model`, including governed spokes, mission, approval-boundary, agent/device, evidence, and connector-posture areas plus loading, empty, missing local API key, unauthorized, offline, stale-data, and protocol-error states. No approval mutation, service worker, relay write, Freedom runtime, Microsoft 365 live read/write, Graphify ingest, R4 live execution, worker bootstrap, live connector, client data, or production behavior. |

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

The AG Operations work tracking folder also holds a human-facing restart note
for this Rev 2 build. The current date-stamped tracker is:

`C:\Users\adamg\AG Operations\01. Strategy and Planning\01. Work Tracking\2026-06-23 - GAIL AI Operating System Rev 2 - Work Tracking.md`

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
operating-partner runtime, the core phone-side operator interface,
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
core phone-side operator link; Rev 2 remains the clean governed mission, relay,
policy, and worker spine. Rev 2 must not build a competing native phone app
unless Adam explicitly reverses that decision.

## Device Roles

| Surface | Rev 2 role | Boundary |
|---|---|---|
| Windows | Current operator workspace and future trusted worker. | May edit/push Rev 2 repo and run local validation; live business connectors remain blocked until approved. |
| Linux | Superseded v1 reference host and future trusted worker clone. | Not the Rev 2 project home; future Linux work must pull from private GitHub and preserve Rev 2 controls. |
| Android phone | Freedom-owned operator link. | Freedom is the core phone-side interface for intent capture, approval, pause/resume, safe evidence summaries, and business-partner continuity; Rev 2 must not build a competing native phone app. No local execution, raw secrets/logs, generated config import, direct connector access, or runtime activation without a bounded later chunk. |
| Android tablet | Future review cockpit. | Larger evidence and status review surface; no unrestricted connector or filesystem access. |
| Browser | Shared cockpit surface across desktop and mobile, now anchored by the `apps/command-center` Vite React TypeScript shell with the read-only hub-and-spoke operating cockpit view over the shared GAIL OS read model. | Reads governed records through approved read-only local paths today; writes require later approved local or relay paths and must not become a second source of truth or replace Freedom's core operator role. |
| Private GitHub | Canonical durable spine. | Commits, request records, issues/PRs, relay references, and evidence links; no secrets or unredacted sensitive payloads. |
| Graphify | Knowledge spoke and high-importance neuronal pathway layer for relationship intelligence. | Read-only handoff and graph references; recommendations are not execution approval. Current acceleration work emits local sanitized preview facts only. Future ingest still requires an approved connector-like boundary. |
| Microsoft 365 / AG Operations | Future business substrate, identity/records/signals spoke, and likely first tactile input/output environment. | Planning-only in Rev 2; feed cockpit through approved metadata, safe summaries, action logs, decision records, and links only after connector boundaries exist. No tenant content, live actions, or physical operating outputs are active in this repo. |
| Freedom Engine | Current operating partner OS, high-level agentic business partner, and core operator interface. | Reference and bridge-planning only; self-learning, research, agent/tool calling, business memory, voice/mobile, and operator-run capabilities must be preserved and elevated through later safe contracts; no runtime merge, generated config, live provider access, code import, or Freedom modification without a bounded later chunk. |
| Build consolidation review | Future architecture decision process and current startup flag. | Do not fold AG Operations, Freedom, or Rev 2 into one build until `docs/decisions/2026-06-24 - Build Consolidation Decision Process.md` is run after AG Operations finishes its current evolution. Next startup should acknowledge the three-repo coordination direction before resuming implementation. |

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

First acknowledge the three-repo coordination direction: GAIL AI Operating
System Rev 2, Freedom, and AG Operations Workspace are coordinated but not
consolidated. The promoted Graphify acceleration GA-B/GA-C local readiness
package plus
`docs/decisions/2026-06-28 - Current Main Stabilization Builder Report.md`,
`docs/decisions/2026-06-28 - Local CNS Connection Proof Report.md`,
`docs/decisions/2026-06-28 - CNS Communication Enhancement Contract.md`, and
`docs/decisions/2026-06-27 - Builder Graphify Freedom AG Operations Integration Summary.md`
are ready to report back to the agentic multi-agent agent builder for a revised
orchestrated plan. If Adam resumes the default Rev 2 implementation route
instead, begin Chunk Twenty: add local governed approval actions for approve,
reject, hold, and request-more-info. Stop before live tool execution, live
relay or hosted authorization, Freedom runtime access, M365 or QuickBooks
adapter work, worker bootstrap scripts, client data, live connectors, live
business systems, retained preview records, Graphify ingest, Phase D contract
publication, Phase E adapter-boundary design, cross-system source-of-truth
changes, or production.
