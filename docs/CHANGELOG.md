# Changelog

## 2026-06-27

- Completed Graphify acceleration Phase B locally. Added sanitizer
  classification helpers, stricter safe-summary/reference/relationship guards,
  pure local graph-fact builders for `Action`, `AuthorityEnvelope`, and
  `EvidencePacket`, deterministic fingerprints for delta/cache workflows, and
  package-root exports for the stable local contract. No persistence, preview
  output, Graphify call, adapter, transport, HTTP API, cloud placement, live
  connector, client data, runtime hook, or execution authority was added.
- Started executing the Graphify acceleration path before Chunk Twenty by
  recording the GA-A3 owner promotion decision and completing GA-B1/GA-B2 to
  draft state. Added the local
  `packages/uaos-core/src/gail_ai_operating_system/graphify_acceleration.py`
  contract plus focused tests for strict `GraphifyAccelerationRecord`
  validation, unsafe reference rejection, JSON-safe serialization, required
  fingerprints, raw-payload blocking, and no package-root export before GA-B6.
  Also made the existing action schema tests runnable under the standard
  unittest command without an undeclared pytest dependency.
  No persistence, preview output, Graphify call, adapter, transport, HTTP API,
  cloud placement, live connector, client data, or execution authority was
  added.
- Expanded the Graphify acceleration readiness plan into plan-local GA-A
  through GA-E chunks covering owner promotion, local contract validation,
  local export preview, contract publication, and future adapter-boundary
  review. This remains planning only; it does not create source modules,
  schemas, export stores, Graphify adapters, transport, HTTP APIs, cloud
  placement, live connectors, or execution authority.
- Added the dated GAIL-side Graphify acceleration readiness plan at
  `docs/decisions/2026-06-27 - Graphify Acceleration Readiness Plan.md`.
  The plan defines future sanitized, delta-friendly graph facts emitted by Rev
  2 so an enhanced Graphify layer can move faster without changing Graphify,
  activating a live adapter, indexing raw payloads, exposing HTTP/cloud paths,
  or granting execution authority.
- Hardened the pre-Chunk Twenty CNS schema contracts for the Guided AI Labs
  operating system diagram: `Action` now validates R-levels, requires an
  `env-` AuthorityEnvelope reference for R4 actions, and blocks R5 records from
  entering agent approval/execution states; `AuthorityEnvelope` now rejects
  empty allowed-action and stop-condition charters; `EvidencePacket` now
  validates evidence/action IDs, execution mode, optional envelope IDs, and
  rejects live evidence by default under the current A1 local no-network
  boundary. Package-root exports now include the new CNS schema types and
  validators.
- Aligned `AGENTS.md` with the active pathway: Chunk Twenty remains local
  governed approval actions, Chunk Twenty-One remains evidence and handoff
  views, and HTTP API/cloud placement is deferred until the local approval,
  authority, and evidence contracts are firm. No approval action, HTTP API,
  Microsoft 365/QuickBooks adapter, Freedom runtime, live connector, client
  data, hosted authorization, or production behavior was added.

## 2026-06-25

- Clarified the document-control standard so dated document names cannot
  interfere with dependencies or tooling. Dependency manifests, lockfiles,
  importable source modules, schemas, generated files, CI workflows, runtime
  config, package identities, and tool-owned config files keep their required
  stable names; use dated companion notes instead.
- Added the active document-control standard at
  `docs/standards/2026-06-25 - Document Control Standard.md`. New durable documents and
  work-tracking records across GAIL AI Operating System Rev 2, Freedom, and AG
  Operations Workspace should use date-prefixed filenames based on first
  durable save or promotion date, with later edits tracked by internal metadata
  rather than repeated renames. Existing stable-route files are exempt unless a
  bounded rename plan updates references.
- Boxed the current change of direction into startup, routing, README, manual,
  roadmap, carry-forward, architecture, source-of-truth, and decision-process
  docs. Next startup should explicitly acknowledge that GAIL AI Operating
  System Rev 2, Freedom, and AG Operations Workspace are being coordinated as
  related builds while remaining separately owned. AG Operations should finish
  its current evolution, Freedom remains the core operator and agentic
  business-partner interface, and Rev 2 remains the governed technical spine
  until the build consolidation decision process records a later owner
  decision.

## 2026-06-24

- Added the active build consolidation decision process at
  `docs/decisions/2026-06-24 - Build Consolidation Decision Process.md`.
  Adam's direction is to let AG Operations finish its current evolution before
  deciding whether Rev 2, Freedom, and AG Operations should remain separate,
  bridge, fold under one build, fold back, stay in AG Operations, retire, or
  defer. The process includes weak-layer rejection rules and does not approve
  source merges, runtime coupling, live connectors, Freedom runtime access,
  Microsoft 365 tenant access, or production behavior.

## 2026-06-23

- Boxed up the post-Chunk Nineteen state for a low-token restart at Chunk
  Twenty, refreshing the repo handoff docs and the external AG Operations
  `01 Work Tracking` folder. Strengthened the document convention so newly
  authored durable documents and work-tracking records should use
  date-stamped filenames such as `YYYY-MM-DD - <title>.md`, with stable
  required repo paths exempted unless a bounded rename plan updates all
  references.
- Captured the owner decision that Freedom is the core operator interface and
  high-level agentic business partner surface, not merely a phone anchor. Rev 2
  must not build a competing native phone app; hosted, desktop, browser, and
  tablet command-center surfaces should augment Freedom through governed bridge
  records, summaries, links, and fallback views. Also recorded the preference
  that newly authored durable documents and records begin with a clear date
  marker unless a required schema/template prevents it.
- Added a user-approved local Windows Desktop shortcut for the command center,
  backed by repo-owned PowerShell launch/install scripts and a symbol-only
  `.ico`. The launcher starts the existing local browser command center only;
  desktop wrappers, service installs, service workers, live connectors, Freedom
  runtime access, hosted relay, and production behavior remain blocked.
- Built the Chunk Nineteen multi-viewport command-center cockpit under
  `apps/command-center`, adding a talk-first operator hub, local/static
  governed spokes for Microsoft 365, Freedom, Graphify, QuickBooks,
  GitHub/build systems, evidence, and worker/device posture, desktop and
  larger-tablet arc layout, and hub-first phone-browser fallback. Approval
  mutations, live relay writes, Freedom runtime access, M365/QuickBooks
  adapters, worker bootstrap, live connectors, client data, hosted
  authorization, and production behavior remain blocked.

## 2026-06-21

- Created the governed `GAIL AI Operating System Rev 2` workspace from the New
  Build Agent scaffold.
- Set canonical slug to `gail-ai-operating-system-rev-2`.
- Kept owner-selected `governance_level: 1` while setting runtime autonomy to
  `A1`.
- Added initial migration, Tool Directory, command-center, core package, and
  test folders.
- Copied selected UAOS v1 reference docs into `docs/migration/reference/uaos-v1`.
- Added link-only Tool Directory seed records for Microsoft 365, QuickBooks,
  GitHub, and Graphify.
- Marked the Linux UAOS v1 workspace as superseded-reference-only so new work
  routes to Rev 2.
- Archived `/home/adamgoodwin/code/.env.master` to a Windows-only secure local
  folder outside all repos; no secret values were copied into Rev 2 docs.
- Created the private GitHub repository
  `Adamgdwn/gail-ai-operating-system-rev-2` for the Rev 2 scaffold and initial
  source-of-truth push.
- Promoted the active Rev 2 `docs/source-of-truth-map.md` from copied v1
  reference material, including device roles and compact future chunk phases.
- Promoted the active Rev 2 `docs/tool-permission-matrix.md` from copied v1
  reference material, keeping live business connectors, client data, hosted
  relay, and production actions blocked until later explicit approval.
- Expanded `docs/current-build-pathway.md` with an explicit current completion
  boundary and planned chunk headings from Chunk Six through the release
  decision so completed chunks cannot be mistaken for project completion.
- Promoted Rev 2 runtime, agent, model, and prompt controls with active
  `docs/agent-runtime-instructions.md`, `docs/agent-inventory.md`,
  `docs/model-registry.md`, and `docs/prompt-register.md`; no live runtime,
  worker, connector, client-data, hosted relay, or production authority was
  activated.
- Promoted active Rev 2 architecture in `docs/architecture.md`, defining the
  private GitHub source spine, portal, worker, relay, Graphify, connector, data,
  and verification boundaries without migrating code or activating runtime
  behavior.
- Added active file migration decisions in
  `docs/migration/file-migration-decisions.md`, classifying the first v1 code
  migration queue as rewrite-focused while keeping secrets, logs, generated
  artifacts, live connector state, client data, raw audio, bulk v1 package
  copying, and production behavior out of Rev 2.
- Rewrote the approved v1 mission, planner, and policy references as the Rev 2
  local no-network mission spine in
  `packages/uaos-core/src/gail_ai_operating_system/mission_spine.py`, with
  focused unit tests in `tests/test_mission_spine.py`.
- Scheduled Chunk Twelve as the explicit enhanced Graphify checkpoint for
  graph-aware routing, repo-local graph setup checks, and read-only handoff
  validation before broader migration exploration.
- Expanded the Rev 2 mission-spine safety tests from the approved v1
  `test_safety_evaluations.py` reference, adding stop-trigger, default-deny,
  risk-tier, validation, and local store file-boundary coverage without
  activating live connectors or runtime behavior.
- Rewrote the selected v1 connector registry reference as the Rev 2 local
  planning-only connector registry, adding profile validation, JSON-safe
  serialization, dry-run request evaluation, default-deny stop decisions, and
  focused tests without activating live connector credentials or API calls.
- Added the active Rev 2 Graphify handoff checkpoint in
  `docs/graphify-handoff-checkpoint.md` and rewrote the selected v1 Graphify
  handoff references as local read-only route/candidate validation with focused
  tests, without graph upload, source mutation, live adapter calls, or full
  semantic rebuild behavior.
- Rewrote the selected v1 relay envelope references as Rev 2 local-file-only
  relay envelope schema validation with focused tests for stale approvals,
  malformed JSON shapes, unsafe payloads, denied hosted relay or worker
  polling, and blocked live connector/client-data behavior.
- Recorded an inter-chunk Microsoft 365 / AG Operations bridge orientation in
  the active architecture and source-of-truth docs: M365 is the future governed
  business substrate feeding the cockpit through approved records, safe
  summaries, action logs, decisions, task/list state, and links, while Rev 2
  retains mission policy, approvals, relay, workers, evidence, and stop rules.
- Rewrote the selected v1 relay store references as a Rev 2 local no-network
  relay record store with status transitions, reference-only evidence records,
  deterministic single trusted-worker claim attempts, stale-state rejection,
  and focused tests, without activating hosted relay, worker bootstrap,
  persistent polling, portal behavior, live connectors, client data, or
  production behavior.
- Recorded an inter-chunk objective review of the downloaded Freedom Engine
  archive in `docs/migration/freedom-engine-objective-review.md`, classifying
  Freedom as Adam's current operating partner OS and Rev 2 as the clean
  governed mission, relay, policy, evidence, connector, and worker spine. The
  review keeps Freedom as a future contract, UX, gateway/desktop-host, and
  bridge reference only, with no source import, secret capture, runtime
  activation, provider access, or production behavior.
- Updated the active pathway, architecture, source-of-truth map, and migration
  decisions to treat Freedom as the substantial future phone-interface anchor
  candidate after the local proof runner. Added a dedicated Chunk Sixteen
  planning boundary before app-shell work and preserved the no-code, no-merge,
  no-import, no-generated-config, no-secret-read, and no-runtime-activation
  boundary until a later approved integration chunk.
- Updated the Freedom planning boundary to preserve and elevate Freedom as a
  high-level agentic business partner, including self-learning, research,
  programming-request handling, agent/tool calling, tool selection, business
  memory, voice/mobile interaction, and operator-run judgment, while still
  blocking code import, generated config, secret reads, runtime activation, and
  Freedom modification until later bounded chunks.
- Added the Chunk Fifteen local no-network proof runner in
  `packages/uaos-core/src/gail_ai_operating_system/local_proof_runner.py`,
  exercising one mission from dry-run intent through policy, connector registry,
  relay envelope validation, relay store persistence, trusted-worker claim,
  reference-only evidence, and completed relay status with focused tests in
  `tests/test_local_proof_runner.py`.
- Added the Chunk Sixteen Freedom phone-interface and business-partner boundary
  decision record in
  `docs/decisions/freedom-phone-interface-business-partner-boundary.md`,
  defining Freedom as the phone anchor and high-level agentic business partner
  source, Rev 2 as the governed mission/relay/evidence spine, initial neutral
  bridge record shapes, safe summary rules, feed-forward/feed-back boundaries,
  approval gates, and no-import/no-runtime stop triggers.
- Added the Chunk Seventeen app-shell decision record in
  `docs/decisions/app-shell-command-center.md` and created the initial
  buildable Vite React TypeScript browser shell under `apps/command-center`.
  The shell supports the Windows/Linux/browser/Android-tablet path while
  preserving Freedom as the phone anchor and deferring service workers, auth,
  hosted relay, worker bootstrap, live connectors, M365, Freedom runtime
  access, native Android, and production behavior.
- Built the Chunk Eighteen read-only operating cockpit shell under
  `apps/command-center`, showing local sample mission, approval boundary,
  worker/device, evidence, and connector-posture areas shaped by the local
  proof runner. Approval mutations, live relay writes, Freedom runtime access,
  M365/QuickBooks adapters, worker bootstrap, live connectors, client data,
  and production behavior remain blocked.
- Recorded the hub-and-spoke command-center direction for Chunk Nineteen and
  boxed up the session with low-token restart guidance in `START_HERE.md`, the
  active pathway handoff, `CARRY_FORWARD.md`, and the AG Operations work
  tracking folder.
