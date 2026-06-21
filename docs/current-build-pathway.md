# Current Build Pathway

Last Updated: 2026-06-21T14:18:18-06:00
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
| Handoff next chunk | pending | 2026-06-21T14:16:18-06:00 | codex session | Next bounded task is promoting runtime, agent, model, and prompt controls. |

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

## Next Handoff

Next agent should use lean startup for ordinary scoped work: check `git status --short`, read short repo-local instructions, use `docs/context-map.md` when routing is unclear, inspect targeted files, and run targeted validation. After compaction or a context clear, resume from this handoff: the Rev 2 workspace scaffold is complete, reference docs live under `docs/migration/reference/uaos-v1`, Linux UAOS v1 is superseded-reference-only, the Linux master env has a Windows-only secure archive outside all repos plus a shared parent-level working copy at `C:\Users\adamg\01. Code Projects\.env.master`, the private GitHub remote is `Adamgdwn/gail-ai-operating-system-rev-2`, active navigation now includes `docs/source-of-truth-map.md`, active tool permissions now live in `docs/tool-permission-matrix.md`, the next bounded task is to promote runtime, agent, model, and prompt controls, and no UAOS code migration has started yet.
