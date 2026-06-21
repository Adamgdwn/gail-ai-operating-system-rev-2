# Current Build Pathway

Last Updated: 2026-06-21T14:46:16-06:00
Status: draft
Owner: Adam Goodwin

> **Single active pathway document.** This is the one active pathway for this project.
> All prior pathway, deployment-plan, and build-plan documents in this repo must carry
> `Status: superseded` and reference this file.

## Purpose

This document is the live path from current plan to completed build. It keeps agent work small, timestamped, and easy to resume.

## Required Work Pattern

For ordinary scoped work, use lean startup:

1. Check `git status --short`.
2. Read the short repo-local agent instructions.
3. Use `docs/context-map.md` when context routing is unclear.
4. Inspect only the specific files, errors, or docs needed for the task.
5. Run targeted validation after the change.

For material or risk-triggering work sessions:

1. Start from `START_HERE.md`.
2. Run `bash scripts/governance-preflight.sh`.
3. Review `docs/standards/README.md`.
4. Review `docs/standards/engineering-governance-by-use-case.md`.
5. Review `docs/policy/durable-development-engineering-policy.md`.
6. Review `docs/standards/ship-ready-engineering-standard.md`.
7. Review `project-control.yaml` and open exceptions.
8. Capture a timestamp with `date -Iseconds`.
9. Define the next build chunk in this document.
10. Complete and validate that chunk before expanding scope.
11. Update this document with status, validation, and the next chunk.

Risk-triggering work includes production, deployment, authentication, authorization, payments, secrets, sensitive data, database migrations, customer communications, external side effects, infrastructure or provider settings, destructive actions, autonomous tool use, risk classification, governance policy changes, or release readiness.

After compaction or a context clear, restart from the latest handoff or active
work packet, then run `git status --short`, read short repo-local instructions,
and open only this plan plus the files needed for the next objective.

## Chunking Standard

Each build chunk should be small enough to fit comfortably in an agent context window.

A good chunk has:

- one objective
- a budget class: Tiny, Small, Medium, Large, or Strategic
- a target completion state
- clear acceptance criteria
- clear input files or documents
- clear output files or behavior
- explicit validation steps
- an explicit stop condition or escalation trigger
- a timestamped status note

When a chunk body is marked complete, put the completion timestamp on the same
line as the status, for example:

```md
Status: complete (2026-06-21T13:58:36-06:00)
```

Use second-level Markdown headings for active and planned chunks so they are easy to scan. Spell out the chunk number in the heading:

```md
## Chunk One - Short Objective
## Chunk Two - Short Objective
```

Continue the pattern for later chunks: `## Chunk Three - ...`, `## Chunk Four - ...`, and so on.

Avoid mixing unrelated code, governance, deployment, and product decisions in one chunk unless the change cannot be validated any other way.

## Active Path

| Step | Status | Timestamp | Owner | Notes |
|------|--------|-----------|-------|-------|
| Scaffold Rev 2 workspace | complete | 2026-06-21T12:45:36-06:00 | codex session | Governed workspace created at `C:\Users\adamg\01. Code Projects\GAIL AI Operating System Rev 2`; metadata tuned, reference docs copied, Git initialized. |
| Validate chunk | complete | 2026-06-21T12:53:00-06:00 | codex session | Governance preflight, schema validation, Tool Directory JSON parse, Git status, and strict secret-value scan completed. |
| Retire UAOS v1 active path | complete | 2026-06-21T13:09:23-06:00 | codex session | Linux Rev 1 root docs now mark the project as superseded-reference-only and route new work to Rev 2. |
| Archive Linux master env | complete | 2026-06-21T13:09:23-06:00 | codex session | `/home/adamgoodwin/code/.env.master` copied by `scp` to a Windows-only secure archive outside all repos. |
| Place shared master env | complete | 2026-06-21T13:22:58-06:00 | codex session | Secure archive copied to `C:\Users\adamg\01. Code Projects\.env.master` for parent-level local project access. |
| Publish private GitHub remote | complete | 2026-06-21T13:36:09-06:00 | codex session | Private repository target is `Adamgdwn/gail-ai-operating-system-rev-2`; initial scaffold commit and push are part of Chunk Three. |
| Promote Rev 2 source-of-truth map | complete | 2026-06-21T14:01:39-06:00 | codex session | Chunk Four promoted active navigation, status timestamp formatting, compact future chunk routing, and required-doc registration. |
| Promote Rev 2 tool permission matrix | complete | 2026-06-21T14:16:18-06:00 | codex session | Chunk Five promoted active tool, device, connector, and worker permission boundaries without activating live connectors. |
| Promote runtime and agent controls | complete | 2026-06-21T14:46:16-06:00 | codex session | Chunk Six promoted active runtime instructions, agent inventory, model registry, and prompt register without activating live runtime behavior. |
| Handoff next chunk | pending | 2026-06-21T14:46:16-06:00 | codex session | Next bounded task is promoting architecture specs before any UAOS code migration. |

## Current Completion Boundary

Rev 2 is not complete. Completed rows in the active path mean only that those
bounded chunks are done. The current project state is active control promotion:
source-of-truth, tool permission, runtime, agent, model, and prompt controls
are promoted; architecture specs and file migration decisions remain ahead. No
UAOS code migration, portal build, worker model, hosted relay, live connector
activation, client-data workflow, or production release has started. Project
completion remains a human decision after the release-decision chunk.

## Compact Future Chunk Map

Use these phase boundaries to keep future sessions token-friendly. Each future
chunk still needs its own packet, validation, commit, push, and handoff.

| Phase | Chunk range | Purpose |
|---|---|---|
| Phase 1 - Active controls | Chunks Four to Eight | Promote Rev 2 source-of-truth, tool permissions, runtime controls, architecture specs, and file migration decisions. |
| Phase 2 - File migration and initial build-out | Chunks Nine to Fifteen | Migrate or rewrite the no-network mission spine, connector registry, Graphify handoff, relay envelope, relay store, tests, and proof runner. |
| Phase 3 - First usable portal | Chunks Sixteen to Twenty | Build the browser command center, mobile-responsive Android/tablet views, approval actions, and evidence/handoff views. |
| Phase 4 - Multi-device worker model | Chunks Twenty-One to Twenty-Five | Add Windows/Linux worker bootstrap, role checks, GitHub-backed relay records, and conflict recovery. |
| Phase 5 - Full system build | Chunks Twenty-Six onward | Evaluate hosted relay, notifications, approved connector activation, Client Gateway boundaries, vendor intelligence, runbooks, pilot, and release decision. |

The compact chunk packets below are the planned runway. A future chunk may be
expanded when activated, but it should not absorb unrelated chunks just because
the plan is visible here.

## Chunk One - Governed Workspace Separation

Status: complete (2026-06-21T12:53:00-06:00)

Completion target: Task complete

Budget class: Small

Objective:

Create the clean Rev 2 governed workspace, keep DirectLink separate, copy only
selected UAOS v1 reference docs, and prepare the project for a fresh VS Code
session.

Acceptance criteria:

- [x] New folder exists at `C:\Users\adamg\01. Code Projects\GAIL AI Operating System Rev 2`.
- [x] New Build Agent scaffold files exist and `project-control.yaml` uses slug `gail-ai-operating-system-rev-2`.
- [x] Runtime autonomy is `A1` even though owner-selected governance level is `1`.
- [x] Rev 2 folders exist for specs, decisions, requests, migration, tool directory, command center, core package, and tests.
- [x] Selected UAOS v1 docs are copied into `docs/migration/reference/uaos-v1`.
- [x] `docs/migration/source-inventory.md` records copied and intentionally excluded sources.
- [x] Local Git repo is initialized with no remote.
- [x] Schema validation, Git status, and secret-pattern scan complete.

Inputs:

- `START_HERE.md`
- `docs/context-map.md`
- `docs/current-build-pathway.md`
- `L:\agents\New Build Agent\automation\scaffold_project.py`
- `L:\Applications\user-ai-operating-system`

Outputs:

- Governed Rev 2 workspace scaffold.
- Initial link-only Tool Directory seed.
- Migration source inventory.
- Copied UAOS v1 reference docs.
- Fresh VS Code window at the Rev 2 root.

Validation:

- `python "L:\agents\New Build Agent\automation\schema_validation.py" --project .`
- `git status --short`
- changed-tree secret-pattern scan for common secret file names and token markers

Stop condition:

- Stop after scaffold, inventory, validation, and VS Code handoff are complete.

Known gaps:

- UAOS core code is not migrated yet.
- No live Microsoft 365, QuickBooks, finance, billing, client, or third-party connector is active.
- Tool Directory entries are link-only seed records, not automation permission.
- The repository is initialized locally but the scaffold files are not committed yet.

Next action:

- In the new VS Code window, promote the active Rev 2 command-center plan into
  `docs/specs` and decide the first code migration chunk.

## Chunk Two - Retire Rev 1 And Archive Master Env

Status: complete (2026-06-21T13:09:23-06:00)

Completion target: Task complete

Budget class: Tiny

Objective:

Make the Linux UAOS Rev 1 folder visibly superseded so agents do not
accidentally run it, and keep a Windows-side copy of the Linux master
environment file outside all repos.

Acceptance criteria:

- [x] Rev 1 top-level docs warn that the folder is superseded-reference-only.
- [x] Rev 1 `project-control.yaml` no longer says `status: active`.
- [x] Rev 1 guidance points new work to `GAIL AI Operating System Rev 2`.
- [x] Linux master environment file is archived on Windows outside DirectLink,
  Rev 2, Git, and shared handoff paths.
- [x] A shared working copy exists at the Windows Code Projects root for
  parent-level local project access.
- [x] Rev 2 inventory records the archive posture without copying secret
  values into project docs.

Inputs:

- `L:\Applications\user-ai-operating-system`
- `/home/adamgoodwin/code/.env.master`
- `C:\Users\adamg\01. Code Projects\GAIL AI Operating System Rev 2`

Outputs:

- Rev 1 `SUPERSEDED_BY_GAIL_AI_OPERATING_SYSTEM_REV_2.md`.
- Rev 1 top-level README, START_HERE, AGENTS, and project control updates.
- Windows-only secure environment archive under
  `C:\Users\adamg\.gail-secure\linux-env-master`.
- Shared parent-level working copy at
  `C:\Users\adamg\01. Code Projects\.env.master`.
- Rev 2 migration inventory update.

Validation:

- `scp linux-direct:/home/adamgoodwin/code/.env.master <secure archive path>`
- `Get-FileHash -Algorithm SHA256 <secure archive path>`
- `Copy-Item <secure archive path> C:\Users\adamg\01. Code Projects\.env.master`
- `ssh linux-direct "cd /home/adamgoodwin/code/Applications/user-ai-operating-system && bash scripts/governance-preflight.sh && git status --short"`
- `git status --short`

Stop condition:

- Stop after the archive exists, Rev 1 warning docs are in place, and Rev 2
  records the control posture.

## Chunk Three - Publish Private GitHub Remote

Status: complete (2026-06-21T13:39:01-06:00)

Completion target: Task complete

Budget class: Tiny

Objective:

Create the private GitHub repository for Rev 2, commit the current scaffold,
and push `main` so the governed workspace has a private remote source.

Acceptance criteria:

- [x] GitHub CLI is installed and authenticated as `Adamgdwn`.
- [x] No existing `Adamgdwn/gail-ai-operating-system-rev-2` repository blocks creation.
- [x] Governance preflight and schema validation pass before publication.
- [x] Strict secret-value scan and forbidden filename scan pass before publication.
- [x] Private GitHub repository exists at `Adamgdwn/gail-ai-operating-system-rev-2`.
- [x] Local `origin` points to the private repository.
- [x] Initial scaffold commit is pushed to `main`.

Inputs:

- `START_HERE.md`
- `docs/current-build-pathway.md`
- `project-control.yaml`
- current scaffold files

Outputs:

- Private GitHub repository `Adamgdwn/gail-ai-operating-system-rev-2`.
- Initial scaffold commit on `main`.
- Updated pathway and changelog notes.

Validation:

- `bash scripts/governance-preflight.sh`
- `python "L:\agents\New Build Agent\automation\schema_validation.py" --project .`
- strict secret-value scan and forbidden filename scan
- `gh repo view Adamgdwn/gail-ai-operating-system-rev-2 --json nameWithOwner,visibility,url,defaultBranchRef`
- `git status --short`

Stop condition:

- Stop after the private remote is created, the scaffold commit is pushed, and
  the next migration task is still clearly recorded.

## Chunk Four - Promote Rev 2 Source Of Truth Map

Status: complete (2026-06-21T14:01:39-06:00)

Completion target: Task complete

Budget class: Tiny

Objective:

Promote the source-of-truth navigation map into active Rev 2 controls, record
the user-requested complete-status timestamp format, and preserve the approved
future chunk route in a token-friendly form.

Acceptance criteria:

- [x] `docs/source-of-truth-map.md` exists as an active Rev 2 navigation map.
- [x] Active source-of-truth docs are distinguished from copied v1 reference
  material.
- [x] Device roles for Windows, Linux, Android, browser, GitHub, and Graphify
  are recorded without granting new live connector authority.
- [x] Future compact chunk phases cover active controls, file migration and
  initial build-out, first portal, multi-device workers, and full system build.
- [x] Existing completed chunk body status lines include completion timestamps.
- [x] Next bounded task points to active tool permission matrix promotion.

Inputs:

- `START_HERE.md`
- `docs/current-build-pathway.md`
- `docs/context-map.md`
- `docs/migration/source-inventory.md`
- `docs/migration/reference/uaos-v1/controls/source-of-truth-map.md`
- copied v1 cross-device and relay references

Outputs:

- Active Rev 2 `docs/source-of-truth-map.md`.
- Updated source routing in `START_HERE.md`, `docs/context-map.md`, and
  `README.md`.
- Updated migration inventory, changelog, and active pathway.

Validation:

- `bash scripts/governance-preflight.sh`
- `python "L:\agents\New Build Agent\automation\schema_validation.py" --project .`
- `git diff --check`
- targeted search for stale references to missing active `docs/source-of-truth-map.md`
- `git status --short`

Stop condition:

- Stop after active navigation is promoted, the process timestamp format is
  recorded, validation passes, and the next active-controls chunk is clear.

## Chunk Five - Promote Rev 2 Tool Permission Matrix

Status: complete (2026-06-21T14:16:18-06:00)

Completion target: Task complete

Budget class: Tiny

Objective:

Promote the copied v1 tool permission controls into the active Rev 2
permission matrix, scoped to the new private GitHub source of truth, local
validation, DirectLink-as-transport, Windows/Linux worker posture, Android and
browser portal posture, relay planning, connector planning, and current stop
triggers.

Acceptance criteria:

- [x] `docs/tool-permission-matrix.md` no longer contains the scaffold example.
- [x] The matrix states the current Rev 2 posture, default deny rule, approval
  gates, and action risk tiers.
- [x] Local repo, shell, Git, GitHub, DirectLink, Windows, Linux, Android,
  browser, relay, connector registry, Graphify, model-provider, M365,
  QuickBooks/accounting, Client Gateway, vendor/deployment, and voice surfaces
  have explicit current boundaries.
- [x] Live connectors, client data, hosted relay, production, billing, finance,
  payment, account, tenant, and destructive actions remain blocked until later
  explicit approval.
- [x] Source map and source inventory record the matrix as promoted active Rev
  2 source.
- [x] Next bounded task points to runtime, agent, model, and prompt control
  promotion.

Inputs:

- `docs/tool-permission-matrix.md`
- `docs/migration/reference/uaos-v1/controls/tool-permission-matrix.md`
- `docs/source-of-truth-map.md`
- `docs/migration/source-inventory.md`
- `docs/current-build-pathway.md`

Outputs:

- Active Rev 2 `docs/tool-permission-matrix.md`.
- Updated source map, migration inventory, changelog, and active pathway.

Validation:

- `bash scripts/governance-preflight.sh`
- `python "L:\agents\New Build Agent\automation\schema_validation.py" --project .`
- `git diff --check`
- targeted search for scaffold placeholder text and complete-status formatting
- forbidden filename scan
- strict secret-pattern scan
- `git status --short`

Stop condition:

- Stop after active tool permissions are promoted, validation passes, the
  runtime/agent-controls handoff is clear, and the chunk is committed and
  pushed.

## Chunk Six - Promote Runtime And Agent Controls

Status: complete (2026-06-21T14:46:16-06:00)

Completion target: Task complete

Budget class: Tiny

Objective:

Promote runtime, agent, model, and prompt controls into active Rev 2 source so
the next architecture and migration chunks can proceed without relying on
scaffold placeholders or v1 runtime authority.

Acceptance criteria:

- [x] `docs/agent-runtime-instructions.md` exists as an active Rev 2 runtime
  control.
- [x] `docs/agent-inventory.md` replaces the scaffold example row with active
  and future inactive Rev 2 agent roles.
- [x] `docs/model-registry.md` replaces the scaffold example row with current
  model-route posture and explicit no-production-runtime approval.
- [x] `docs/prompt-register.md` replaces the scaffold example row with active
  instruction sources and future prompt approval requirements.
- [x] Current autonomy remains `A1`.
- [x] Live connectors, client data, hosted relay, persistent workers,
  production runtime behavior, and code migration remain blocked.
- [x] Source map, source inventory, project control, context routing, changelog,
  and handoff records point to the promoted controls.

Inputs:

- `docs/agent-inventory.md`
- `docs/model-registry.md`
- `docs/prompt-register.md`
- `docs/tool-permission-matrix.md`
- `docs/source-of-truth-map.md`
- `docs/migration/source-inventory.md`
- `docs/migration/reference/uaos-v1/controls/agent-runtime-instructions.md`

Outputs:

- Active Rev 2 `docs/agent-runtime-instructions.md`.
- Active Rev 2 `docs/agent-inventory.md`.
- Active Rev 2 `docs/model-registry.md`.
- Active Rev 2 `docs/prompt-register.md`.
- Updated project control, context routing, source map, migration inventory,
  changelog, and active pathway.

Validation:

- `bash scripts/governance-preflight.sh`
- `python "L:\agents\New Build Agent\automation\schema_validation.py" --project .`
- `git diff --check`
- targeted search for scaffold placeholder text, active control routing, and
  complete-status formatting
- forbidden filename scan
- strict secret-pattern scan
- `git status --short`

Stop condition:

- Stop after controls are promoted, validation passes, the architecture-spec
  handoff is clear, and the chunk is committed and pushed.

## Chunk Seven - Promote Architecture Specs

Status: planned

Completion target: Task complete

Budget class: Small

Plan packet:

Inputs: copied v1 architecture, DirectLink, relay, cockpit, and cross-device
references plus active source-of-truth controls. Outputs: active Rev 2
architecture specs for source of truth, portal surfaces, workers, relay
records, and connector boundaries. Acceptance: Windows, Linux, Android,
browser, GitHub, and future hosted surfaces have clear roles. Validation:
governance preflight, schema validation, link/path checks, targeted search for
stale v1 authority language, diff check, commit, push. Stop: before any app or
worker code migration.

## Chunk Eight - Record File Migration Decisions

Status: planned

Completion target: Task complete

Budget class: Small

Plan packet:

Inputs: source inventory, copied v1 references, active control docs, and
candidate v1 code folders. Outputs: migration decision record marking each
candidate source as promote, rewrite, archive, exclude, or later review.
Acceptance: no secrets, logs, client data, raw audio, generated artifacts, or
live connector state enter the repo. Validation: inventory reconciliation,
forbidden filename scan, strict secret-pattern scan, diff check, commit, push.
Stop: when the first code migration queue is safe and bounded.

## Chunk Nine - Migrate Local Mission Spine

Status: planned

Completion target: Task complete

Budget class: Medium

Plan packet:

Inputs: approved migration decision record and selected v1 mission-spine code.
Outputs: Rev 2 local-only mission spine with no network side effects.
Acceptance: mission records can be created, read, and validated locally under
Rev 2 naming and governance. Validation: unit tests, type or syntax checks,
secret scan, diff check, commit, push. Stop: before connector, portal, or
worker behavior.

## Chunk Ten - Migrate Mission Spine Tests

Status: planned

Completion target: Task complete

Budget class: Small

Plan packet:

Inputs: migrated mission spine and selected v1 test references. Outputs:
focused Rev 2 tests for mission state, validation, failure cases, and file
boundaries. Acceptance: tests prove local behavior without external services.
Validation: targeted test run, governance preflight if controls changed,
secret scan, diff check, commit, push. Stop: once the local mission spine has a
repeatable safety loop.

## Chunk Eleven - Migrate Connector Registry Foundation

Status: planned

Completion target: Task complete

Budget class: Medium

Plan packet:

Inputs: tool permission matrix, source-of-truth map, migration decisions, and
selected v1 connector registry references. Outputs: Rev 2 connector registry
schema and local validation only. Acceptance: registry entries describe
permissions and stop triggers but do not activate live services. Validation:
schema tests, JSON/YAML parse checks, forbidden live-secret scan, diff check,
commit, push. Stop: before any live connector credentials or API calls.

## Chunk Twelve - Migrate Graphify Handoff Validator

Status: planned

Completion target: Task complete

Budget class: Small

Plan packet:

Inputs: Graphify policy, active context hygiene standard, and selected v1
handoff references. Outputs: local validation for graph-aware handoff records
without broad graph rebuilds. Acceptance: validator supports context routing
and compaction handoffs while preserving secret exclusions. Validation:
targeted tests, sample handoff validation, diff check, commit, push. Stop:
before broad source exploration or full semantic graph work.

## Chunk Thirteen - Migrate Relay Envelope Validator

Status: planned

Completion target: Task complete

Budget class: Medium

Plan packet:

Inputs: relay references, tool permissions, architecture specs, and migration
decisions. Outputs: Rev 2 relay envelope schema and validator for intent,
approval, status, evidence, and handoff records. Acceptance: envelopes are
local files only and contain no secrets or client data. Validation: schema
tests, malformed-envelope tests, secret scan, diff check, commit, push. Stop:
before any persistent hosted relay or cross-device execution loop.

## Chunk Fourteen - Build Relay Store And Worker Claim Proof

Status: planned

Completion target: Task complete

Budget class: Medium

Plan packet:

Inputs: relay envelope validator, architecture specs, and worker role
boundaries. Outputs: local Git-backed relay store proof with claim, status, and
evidence records. Acceptance: worker claim behavior is deterministic, stale
state is rejected, and no device receives more authority than documented.
Validation: local tests, conflict-case tests, diff check, commit, push. Stop:
before Windows/Linux worker bootstrap scripts.

## Chunk Fifteen - Build Local Proof Runner

Status: planned

Completion target: Integration complete

Budget class: Medium

Plan packet:

Inputs: mission spine, connector registry foundation, relay envelope validator,
and relay store proof. Outputs: local proof runner that exercises one complete
no-network mission path. Acceptance: a mission can move from intent to
validated evidence locally. Validation: full local proof run, test suite,
governance preflight, secret scan, diff check, commit, push. Stop: before UI
or live connector work.

## Chunk Sixteen - Choose App Shell

Status: planned

Completion target: Task complete

Budget class: Small

Plan packet:

Inputs: architecture specs, portal requirements, current repo tooling, and
local proof runner behavior. Outputs: app-shell decision record and initial
project structure for the browser command center. Acceptance: selected shell
supports Windows, Linux, Android phone, Android tablet, and browser workflows.
Validation: dependency review, minimal build check, diff check, commit, push.
Stop: before feature UI implementation.

## Chunk Seventeen - Build Operating Cockpit Shell

Status: planned

Completion target: Task complete

Budget class: Medium

Plan packet:

Inputs: app-shell decision and relay/mission proof data. Outputs: first
browser cockpit shell showing missions, approvals, worker status, and evidence
areas from local sample data. Acceptance: first screen is the usable cockpit,
not a landing page. Validation: build, lint or equivalent checks, responsive
smoke test, screenshot review if available, commit, push. Stop: before
approval mutation behavior.

## Chunk Eighteen - Build Mobile-Responsive Cockpit

Status: planned

Completion target: Task complete

Budget class: Medium

Plan packet:

Inputs: cockpit shell and device role specs. Outputs: Android phone, Android
tablet, desktop Windows, and desktop Linux responsive layouts. Acceptance:
operators can review status, approvals, and evidence cleanly on each target
viewport. Validation: responsive browser checks, screenshot review, build, diff
check, commit, push. Stop: before adding real approval actions.

## Chunk Nineteen - Add Approval Actions

Status: planned

Completion target: Integration complete

Budget class: Medium

Plan packet:

Inputs: mobile cockpit, relay envelope validator, relay store, and tool
permission matrix. Outputs: local approval, reject, hold, and request-more-info
actions writing governed relay records. Acceptance: actions are auditable,
stale-state protected, and do not execute live tools. Validation: UI tests or
manual proof, relay record tests, diff check, commit, push. Stop: before
production or hosted authorization.

## Chunk Twenty - Build Evidence And Handoff Views

Status: planned

Completion target: Integration complete

Budget class: Medium

Plan packet:

Inputs: cockpit shell, approval actions, relay records, and context hygiene
standard. Outputs: evidence viewer and chunk handoff view for compact resume
across devices. Acceptance: a future agent can resume from durable records
without needing chat history. Validation: sample mission proof, responsive
checks, handoff validation, commit, push. Stop: before multi-worker bootstrap.

## Chunk Twenty-One - Build Windows Worker Bootstrap

Status: planned

Completion target: Task complete

Budget class: Medium

Plan packet:

Inputs: worker architecture, relay store, local proof runner, and Windows
operator workspace constraints. Outputs: Windows worker bootstrap for local
claim, run, evidence write, and stop behavior. Acceptance: worker runs only
approved local no-network tasks. Validation: local bootstrap test, stale claim
test, secret scan, diff check, commit, push. Stop: before Linux worker
bootstrap.

## Chunk Twenty-Two - Build Linux Worker Bootstrap

Status: planned

Completion target: Task complete

Budget class: Medium

Plan packet:

Inputs: worker architecture, relay store, local proof runner, and Linux
reference/worker boundaries. Outputs: Linux worker bootstrap that clones or
pulls the private repo and claims approved work without tunnel dependence.
Acceptance: Linux acts as a worker, not as Rev 2 source of truth. Validation:
local or DirectLink-assisted dry run, claim/evidence tests, diff check, commit,
push. Stop: before cross-worker identity enforcement.

## Chunk Twenty-Three - Add Worker Identity And Role Checks

Status: planned

Completion target: Integration complete

Budget class: Medium

Plan packet:

Inputs: Windows worker, Linux worker, tool permission matrix, and relay
records. Outputs: explicit worker identity, role, and capability checks.
Acceptance: worker permissions are enforced before claim or execution.
Validation: allowed and denied role tests, stale-state tests, diff check,
commit, push. Stop: before GitHub-backed relay synchronization.

## Chunk Twenty-Four - Add GitHub-Backed Relay Records

Status: planned

Completion target: Integration complete

Budget class: Medium

Plan packet:

Inputs: private GitHub remote, relay store, worker checks, and portal views.
Outputs: GitHub-backed relay record flow for device-independent status,
approval, claim, and evidence records. Acceptance: devices coordinate through
private GitHub records, not through persistent tunneling. Validation: local
branch/commit proof, conflict tests, push/pull proof, diff check, commit, push.
Stop: before hosted relay services.

## Chunk Twenty-Five - Add Conflict And Recovery Behavior

Status: planned

Completion target: Integration complete

Budget class: Medium

Plan packet:

Inputs: GitHub-backed relay records, worker identity checks, and portal
approval flows. Outputs: conflict detection, retry, stale claim cleanup,
operator override, and recovery records. Acceptance: failed or competing work
can be recovered without silent state loss. Validation: conflict scenario
tests, manual proof, diff check, commit, push. Stop: before auth or hosted
relay design.

## Chunk Twenty-Six - Design Auth And Session Boundaries

Status: planned

Completion target: Draft complete

Budget class: Medium

Plan packet:

Inputs: portal, relay, worker model, tool permissions, and future hosted relay
needs. Outputs: auth/session design for local, private GitHub, and potential
hosted surfaces. Acceptance: no production auth is activated; data classes,
roles, tokens, and session expiry are specified. Validation: governance review,
threat-model checklist, diff check, commit, push. Stop: before implementation
or provider configuration.

## Chunk Twenty-Seven - Evaluate Hosted Relay

Status: planned

Completion target: Draft complete

Budget class: Medium

Plan packet:

Inputs: local relay proof, GitHub-backed relay behavior, auth design, and
device requirements. Outputs: hosted relay decision record with options,
risks, costs, and approval gates. Acceptance: hosting is evaluated without
creating infrastructure or public ingress. Validation: decision review,
security/risk checklist, diff check, commit, push. Stop: before provisioning.

## Chunk Twenty-Eight - Prototype Hosted Relay

Status: planned

Completion target: Integration complete

Budget class: Large

Plan packet:

Inputs: approved hosted relay decision, auth/session design, relay schema, and
worker model. Outputs: minimal hosted relay prototype behind approved controls.
Acceptance: prototype has disable path, logs only safe metadata, and excludes
client data and live connector execution unless separately approved.
Validation: local and hosted smoke tests, security checks, rollback runbook,
commit, push. Stop: on any unresolved auth, secret, public ingress, or data
classification issue.

## Chunk Twenty-Nine - Add Notification Layer

Status: planned

Completion target: Integration complete

Budget class: Medium

Plan packet:

Inputs: approval flows, hosted or GitHub-backed relay posture, and device role
specs. Outputs: notification design and minimal approved status notifications.
Acceptance: notifications are opt-in, auditable, and do not leak sensitive
content. Validation: notification dry run, safe payload review, diff check,
commit, push. Stop: before customer or business-system communications.

## Chunk Thirty - Activate Microsoft 365 Inventory If Approved

Status: planned

Completion target: Task complete

Budget class: Large

Plan packet:

Inputs: explicit Adam approval, tool permission matrix update, auth/session
design, connector registry, and M365 boundary docs. Outputs: inventory-only
M365 connector posture, if approved. Acceptance: no mail send, Teams send,
tenant/admin mutation, or content extraction beyond approved inventory scope.
Validation: dry run, permission review, safe-log review, governance preflight,
commit, push. Stop: unless explicit approval and credentials boundary are in
place.

## Chunk Thirty-One - Activate GitHub Adapter

Status: planned

Completion target: Integration complete

Budget class: Medium

Plan packet:

Inputs: connector registry, relay records, private GitHub remote, and tool
permission matrix. Outputs: governed GitHub adapter for repo metadata, issues,
PRs, and approved workflow support. Acceptance: adapter follows risk tiers,
dry-run where practical, and never mutates outside approved repos or branches.
Validation: adapter tests, dry-run proof, safe-log review, commit, push. Stop:
before broader vendor account access.

## Chunk Thirty-Two - Define Client Gateway Boundary

Status: planned

Completion target: Draft complete

Budget class: Medium

Plan packet:

Inputs: portal, relay, auth design, connector registry, and client-data stop
triggers. Outputs: Client Gateway boundary spec and activation checklist.
Acceptance: client data remains blocked until classification, consent, storage,
retention, and deletion controls are approved. Validation: governance review,
data-boundary checklist, diff check, commit, push. Stop: before any real
client data enters the system.

## Chunk Thirty-Three - Add Vendor And Subscription Intelligence

Status: planned

Completion target: Task complete

Budget class: Large

Plan packet:

Inputs: connector registry, vendor/account stop triggers, approval flows, and
safe evidence views. Outputs: local or approved-read vendor/subscription
intelligence workflow. Acceptance: no billing mutation, payment movement,
account change, or vendor communication occurs. Validation: dry run, safe-log
review, governance preflight, tests, commit, push. Stop: before finance,
payment, or account-change authority.

## Chunk Thirty-Four - Write Runbooks And Disable Procedures

Status: planned

Completion target: Task complete

Budget class: Medium

Plan packet:

Inputs: all active architecture, portal, relay, worker, auth, connector, and
notification controls. Outputs: operator runbooks, emergency stop, credential
rotation notes, disable procedures, and recovery procedures. Acceptance:
operator can stop or roll back every active surface. Validation: runbook
walkthrough, link checks, governance preflight, commit, push. Stop: before
pilot mission.

## Chunk Thirty-Five - Run Pilot Mission

Status: planned

Completion target: Integration complete

Budget class: Large

Plan packet:

Inputs: local/hosted relay posture, portal, workers, runbooks, and approved
connector boundaries. Outputs: one documented pilot mission from intent through
approval, execution, evidence, handoff, and recovery. Acceptance: pilot stays
inside approved data and tool boundaries and produces durable evidence.
Validation: pilot transcript, test suite, runbook checks, governance preflight,
commit, push. Stop: on any boundary breach or unapproved connector need.

## Chunk Thirty-Six - Perform Ship-Readiness Hardening

Status: planned

Completion target: Release ready

Budget class: Strategic

Plan packet:

Inputs: pilot results, active code, controls, runbooks, tests, and standards.
Outputs: release-readiness evidence package, resolved high-risk gaps, and
known residual risks. Acceptance: Definition of Shipped evidence supports a
human release decision. Validation: full test suite, security and secret
checks, governance preflight, runbook proof, commit, push. Stop: before
declaring project completion.

## Chunk Thirty-Seven - Make Release Decision

Status: planned

Completion target: Release ready

Budget class: Strategic

Plan packet:

Inputs: ship-readiness evidence, pilot results, risk register, runbooks,
release checklist, and Adam's decision. Outputs: release decision record:
ship, hold, limited pilot, or redesign. Acceptance: only Adam decides project
completion; agents may report evidence and bounded completion states.
Validation: decision record, final status update, tagged release only if
approved, commit, push. Stop: at human release decision.

## Timestamp Rule

Use ISO-style timestamps for work notes, handoffs, decisions, exceptions, release notes, and validation records. Prefer the local command:

```bash
date -Iseconds
```

## Validation Log

| Timestamp | Command | Result | Notes |
|-----------|---------|--------|-------|
| 2026-06-21T12:42:52-06:00 | `python "L:\agents\New Build Agent\automation\scaffold_project.py" "C:\Users\adamg\01. Code Projects\GAIL AI Operating System Rev 2" agent 1` | pass | New governed agent scaffold created. |
| 2026-06-21T12:48:00-06:00 | `bash scripts/governance-preflight.sh` | failed, then fixed | Initial failure was hidden CRLF in `project-control.yaml`; normalized file line endings. |
| 2026-06-21T12:53:00-06:00 | `bash scripts/governance-preflight.sh` | pass | Governance check passed with 0 warnings. |
| 2026-06-21T12:53:00-06:00 | `python "L:\agents\New Build Agent\automation\schema_validation.py" --project .` | pass | `project-control.yaml` schema passed. |
| 2026-06-21T12:53:00-06:00 | `python -m json.tool data\tool-directory\link-only-tools.json` | pass | Tool Directory seed JSON parsed. |
| 2026-06-21T12:53:00-06:00 | `git status --short` | pass | Local repo initialized; scaffold files are untracked as expected. |
| 2026-06-21T12:53:00-06:00 | strict secret-value scan and forbidden filename scan | pass | No strict secret-pattern matches and no `.env`, key, tenant secret, invoice/export, or credential files found. |
| 2026-06-21T13:08:34-06:00 | `scp linux-direct:/home/adamgoodwin/code/.env.master C:\Users\adamg\.gail-secure\linux-env-master\.env.master.pop-os.20260621-130834` | pass | Master env archived outside all repos; metadata recorded in a secure local manifest. |
| 2026-06-21T13:09:23-06:00 | Rev 1 top-level doc/control update | pass | Rev 1 now has superseded-reference-only notices in README, START_HERE, AGENTS, project control, and a dedicated superseded notice. |
| 2026-06-21T13:14:00-06:00 | `bash scripts/governance-preflight.sh` | pass | Rev 2 governance check still passes with 0 warnings after doc updates. |
| 2026-06-21T13:14:00-06:00 | Rev 2 strict secret-value scan and forbidden filename scan | pass | No actual `.env`, key, tenant secret, invoice/export, credential, or strict secret-value files were found in Rev 2. |
| 2026-06-21T13:14:30-06:00 | `ssh linux-direct "cd /home/adamgoodwin/code/Applications/user-ai-operating-system && bash scripts/governance-preflight.sh && git status --short"` | pass | Linux Rev 1 governance passes; Git shows only intended superseded-marker changes. |
| 2026-06-21T13:22:58-06:00 | `Copy-Item C:\Users\adamg\.gail-secure\linux-env-master\.env.master.pop-os.20260621-130834 C:\Users\adamg\01. Code Projects\.env.master` | pass | Shared parent-level working copy created; file is hidden, ACL-restricted, 23,952 bytes, and SHA-256 matches the secure archive. |
| 2026-06-21T13:36:09-06:00 | `bash scripts/governance-preflight.sh` | pass | Governance check passed with 0 warnings before private GitHub publication. |
| 2026-06-21T13:36:09-06:00 | `python "L:\agents\New Build Agent\automation\schema_validation.py" --project .` | pass | `project-control.yaml` schema passed before private GitHub publication. |
| 2026-06-21T13:36:09-06:00 | `gh auth status` | pass | GitHub CLI authenticated as `Adamgdwn`; token value was not printed beyond `gh` masked status output. |
| 2026-06-21T13:36:09-06:00 | private repository existence check and pre-push scans | pass | Target repo did not already exist; no forbidden filenames or strict secret-value patterns found. |
| 2026-06-21T13:39:01-06:00 | `gh repo create Adamgdwn/gail-ai-operating-system-rev-2 --private --source . --remote origin --push` | pass | Private repository created, `origin` set, and `main` pushed with commit `12fa8c3`. |
| 2026-06-21T13:39:01-06:00 | `gh repo view Adamgdwn/gail-ai-operating-system-rev-2 --json nameWithOwner,visibility,url,defaultBranchRef` | pass | GitHub reports `visibility: PRIVATE` and default branch `main`. |
| 2026-06-21T13:39:01-06:00 | `git status -sb` | pass | Local `main` is tracking `origin/main` with no uncommitted changes after initial push. |
| 2026-06-21T13:58:36-06:00 | `bash scripts/governance-preflight.sh` | pass | Governance check passed with 0 warnings before Chunk Four edits. |
| 2026-06-21T14:01:39-06:00 | `bash scripts/governance-preflight.sh` | pass | Governance check passed with 0 warnings after source-of-truth promotion. |
| 2026-06-21T14:01:39-06:00 | `python "L:\agents\New Build Agent\automation\schema_validation.py" --project .` | pass | `project-control.yaml` schema passed after adding `docs/source-of-truth-map.md` to required docs. |
| 2026-06-21T14:01:39-06:00 | `git diff --check` | pass | No whitespace errors; Git reported expected line-ending normalization warnings for previously CRLF files. |
| 2026-06-21T14:01:39-06:00 | targeted source map and complete-status search | pass | Active Rev 2 docs route to `docs/source-of-truth-map.md`; bare `Status: complete` matches remain only in copied v1 reference request records. |
| 2026-06-21T14:01:39-06:00 | forbidden filename scan | pass | No `.env`, key, credential, secret, invoice, or export filenames found in tracked or untracked non-ignored files. |
| 2026-06-21T14:01:39-06:00 | strict secret-pattern scan | pass | No strict secret-looking assignments found outside copied v1 reference records. |
| 2026-06-21T14:12:35-06:00 | `bash scripts/governance-preflight.sh` | pass | Governance check passed with 0 warnings before Chunk Five edits. |
| 2026-06-21T14:16:18-06:00 | `bash scripts/governance-preflight.sh` | pass | Governance check passed with 0 warnings after tool permission matrix promotion. |
| 2026-06-21T14:16:18-06:00 | `python "L:\agents\New Build Agent\automation\schema_validation.py" --project .` | pass | `project-control.yaml` schema passed after tool permission matrix promotion. |
| 2026-06-21T14:16:18-06:00 | `git diff --check` | pass | No whitespace errors; Git reported expected line-ending normalization warning for the pathway file. |
| 2026-06-21T14:16:18-06:00 | targeted matrix placeholder and complete-status search | pass | No scaffold placeholder and no bare completed-status lines in active chunk docs. |
| 2026-06-21T14:16:18-06:00 | forbidden filename scan | pass | No `.env`, key, credential, secret, invoice, QuickBooks, token, or export filenames found in tracked or untracked non-ignored files. |
| 2026-06-21T14:16:18-06:00 | strict secret-pattern scan | pass | No strict secret-looking assignments found outside copied v1 reference records. |
| 2026-06-21T14:17:39-06:00 | targeted matrix placeholder and complete-status search | failed, then fixed | The check caught its own validation-log wording; the wording was changed to avoid self-referential placeholder text. |
| 2026-06-21T14:18:18-06:00 | targeted matrix placeholder and complete-status search | pass | Final rerun passed after validation-log wording fix. |
| 2026-06-21T14:33:43-06:00 | pathway planned-chunk correction | pass | Added a current completion boundary and planned chunk headings from Chunk Six through Chunk Thirty-Seven so the pathway does not imply project completion after Chunk Five. |
| 2026-06-21T14:33:43-06:00 | `bash scripts/governance-preflight.sh` | pass | Governance check passed with 0 warnings after pathway roadmap correction. |
| 2026-06-21T14:33:43-06:00 | `python "L:\agents\New Build Agent\automation\schema_validation.py" --project .` | pass | `project-control.yaml` schema still passes. |
| 2026-06-21T14:33:43-06:00 | `git diff --check` | pass | No whitespace errors; Git reported expected line-ending normalization warning for the pathway file. |
| 2026-06-21T14:33:43-06:00 | targeted planned-chunk and complete-status search | failed, then fixed | First heading count included instructional code-block examples; rerun checked required future chunk headings and no bare completed-status lines. |
| 2026-06-21T14:33:43-06:00 | forbidden filename scan | pass | No `.env`, key, credential, secret, invoice, QuickBooks, token, or export filenames found in tracked or untracked non-ignored files. |
| 2026-06-21T14:33:43-06:00 | strict secret-pattern scan | pass | No strict secret-looking assignments found outside copied v1 reference records. |
| 2026-06-21T14:41:16-06:00 | `bash scripts/governance-preflight.sh` | pass | Governance check passed with 0 warnings before Chunk Six edits. |
| 2026-06-21T14:46:16-06:00 | runtime, agent, model, and prompt control promotion | pass | Added active runtime instructions and promoted registries; no live runtime, worker, connector, client-data, hosted relay, production, or code migration authority was activated. |
| 2026-06-21T14:46:16-06:00 | `bash scripts/governance-preflight.sh` | pass | Governance check passed with 0 warnings after Chunk Six promotion. |
| 2026-06-21T14:46:16-06:00 | `python "L:\agents\New Build Agent\automation\schema_validation.py" --project .` | pass | `project-control.yaml` schema passed after registering runtime, model, and prompt controls. |
| 2026-06-21T14:46:16-06:00 | `git diff --check` | pass | No whitespace errors; Git reported expected line-ending normalization warning for the pathway file. |
| 2026-06-21T14:46:16-06:00 | targeted control placeholder, routing, and complete-status search | pass | No scaffold placeholder examples or bare completed-status lines in active Chunk Six docs; promoted controls are routed from project control, context map, source map, inventory, and pathway. |
| 2026-06-21T14:46:16-06:00 | forbidden filename scan | pass | No `.env`, key, credential, secret, invoice, QuickBooks, token, or export filenames found in tracked or untracked non-ignored files. |
| 2026-06-21T14:46:16-06:00 | strict secret-pattern scan | failed, then fixed | First run failed from PowerShell regex quoting; rerun with a pattern variable passed with no strict secret-looking assignments outside copied v1 references. |

## Next Handoff

Next agent should use lean startup for ordinary scoped work: check `git status --short`, read short repo-local instructions, use `docs/context-map.md` when routing is unclear, inspect targeted files, and run targeted validation. After compaction or a context clear, resume from this handoff: the Rev 2 workspace scaffold is complete, reference docs live under `docs/migration/reference/uaos-v1`, Linux UAOS v1 is superseded-reference-only, the Linux master env has a Windows-only secure archive outside all repos plus a shared parent-level working copy at `C:\Users\adamg\01. Code Projects\.env.master`, the private GitHub remote is `Adamgdwn/gail-ai-operating-system-rev-2`, active navigation now includes `docs/source-of-truth-map.md`, active tool permissions now live in `docs/tool-permission-matrix.md`, active runtime and agent controls now live in `docs/agent-runtime-instructions.md`, `docs/agent-inventory.md`, `docs/model-registry.md`, and `docs/prompt-register.md`, the next bounded task is to promote architecture specs, and no UAOS code migration has started yet.
