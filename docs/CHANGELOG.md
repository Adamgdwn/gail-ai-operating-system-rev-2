# Changelog

## 2026-06-23

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
