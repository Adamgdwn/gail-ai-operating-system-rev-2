# Source Inventory

Created: 2026-06-21T12:45:36-06:00
Last Updated: 2026-06-21T15:39:29-06:00
Status: active separation inventory
Owner: Adam Goodwin

## Purpose

This inventory records the first copied reference material for GAIL AI Operating
System Rev 2.

The copied files are reference inputs only. They are not active Rev 2 controls
until a later chunk promotes, rewrites, or supersedes them.

## Source Roots

| Source | Role | Migration posture |
|---|---|---|
| `C:\Users\adamg\DirectLink` | Windows/Linux transport, status, and shared skill tooling | Do not migrate operational files into Rev 2. |
| `L:\Applications\user-ai-operating-system` | Existing UAOS v1 proof, docs, mission spine, relay, connector registry, and cockpit proof | Copy selected docs first; migrate code only after separation is clean. |
| `L:\agents\New Build Agent` | Governance scaffold and control standards | Used to scaffold this workspace; do not vendor-copy the full governance repo. |
| `C:\Users\adamg\.gail-secure\linux-env-master` | Windows-only operator archive of the Linux master environment file | Not a project source. Never commit, migrate, or copy into Rev 2. Use only as an explicit owner-approved local operator reference. |
| `C:\Users\adamg\01. Code Projects\.env.master` | Shared Windows working copy of the Linux master environment file | Parent-level operator config for local projects. Do not commit, copy into repo folders, or treat as an approved live connector boundary by itself. |

## Superseded Source Status

As of 2026-06-21, the Linux UAOS v1 workspace at
`L:\Applications\user-ai-operating-system` is marked
`superseded-reference-only`. Its top-level `README.md`, `START_HERE.md`,
`AGENTS.md`, `project-control.yaml`, and
`SUPERSEDED_BY_GAIL_AI_OPERATING_SYSTEM_REV_2.md` now direct agents away from
new Rev 1 implementation work and toward this Rev 2 workspace.

## Secure Operator Archives

The Linux master environment file was copied from
`/home/adamgoodwin/code/.env.master` to a Windows-only secure archive outside
all repos:

`C:\Users\adamg\.gail-secure\linux-env-master\.env.master.pop-os.20260621-130834`

The archive folder has restricted Windows ACLs for the current Windows user,
SYSTEM, and Administrators. A metadata-only `archive-manifest.tsv` sits beside
the archived file. Secret contents were not inspected, summarized, or copied
into Rev 2.

## Shared Working Environment Copy

For project-wide local access, the same Linux master environment file is also
available outside all individual repos at:

`C:\Users\adamg\01. Code Projects\.env.master`

This file is hidden and ACL-restricted to the current Windows user, SYSTEM, and
Administrators. It is a parent-level operator config file so future projects can
reference one shared Windows path. It is not Rev 2 source, is not committed, and
does not approve any live Microsoft 365, QuickBooks, finance, billing, client,
vendor, or third-party integration by itself.

## Copied UAOS v1 References

| Destination | Source | Why copied |
|---|---|---|
| `docs/migration/reference/uaos-v1/specs/uaos-final-shippable-plan.md` | `L:\Applications\user-ai-operating-system\docs\specs\uaos-final-shippable-plan.md` | Baseline v1 finish-line and stage order. |
| `docs/migration/reference/uaos-v1/specs/microsoft-365-business-environment-boundary.md` | `L:\Applications\user-ai-operating-system\docs\specs\microsoft-365-business-environment-boundary.md` | M365 boundary and stop triggers. |
| `docs/migration/reference/uaos-v1/specs/connector-registry-client-gateway-boundary.md` | `L:\Applications\user-ai-operating-system\docs\specs\connector-registry-client-gateway-boundary.md` | Connector registry and Client Gateway controls. |
| `docs/migration/reference/uaos-v1/specs/shared-relay-phone-cockpit-architecture.md` | `L:\Applications\user-ai-operating-system\docs\specs\shared-relay-phone-cockpit-architecture.md` | Cross-device relay architecture reference. |
| `docs/migration/reference/uaos-v1/specs/cross-device-source-of-truth-foundation.md` | `L:\Applications\user-ai-operating-system\docs\specs\cross-device-source-of-truth-foundation.md` | Source-of-truth and authorized surface model. |
| `docs/migration/reference/uaos-v1/specs/graphify-workspace-cockpit-uaos-integration.md` | `L:\Applications\user-ai-operating-system\docs\specs\graphify-workspace-cockpit-uaos-integration.md` | Graphify/UAOS boundary. |
| `docs/migration/reference/uaos-v1/specs/subscription-vendor-intelligence.md` | `L:\Applications\user-ai-operating-system\docs\specs\subscription-vendor-intelligence.md` | Vendor and subscription intelligence requirement. |
| `docs/migration/reference/uaos-v1/specs/manual-subscription-vendor-register.md` | `L:\Applications\user-ai-operating-system\docs\specs\manual-subscription-vendor-register.md` | Manual vendor register fields. |
| `docs/migration/reference/uaos-v1/specs/manual-vendor-register-learning-test.md` | `L:\Applications\user-ai-operating-system\docs\specs\manual-vendor-register-learning-test.md` | First safe vendor-register learning sample. |
| `docs/migration/reference/uaos-v1/controls/tool-permission-matrix.md` | `L:\Applications\user-ai-operating-system\docs\tool-permission-matrix.md` | Existing tool permission controls. |
| `docs/migration/reference/uaos-v1/controls/source-of-truth-map.md` | `L:\Applications\user-ai-operating-system\docs\source-of-truth-map.md` | Current v1 source map. |
| `docs/migration/reference/uaos-v1/controls/agent-runtime-instructions.md` | `L:\Applications\user-ai-operating-system\docs\agent-runtime-instructions.md` | Existing runtime stop rules and allowed posture. |
| `docs/migration/reference/uaos-v1/requests/REQ-0055-local-relay-envelope-validator.md` | `L:\Applications\user-ai-operating-system\docs\requests\REQ-0055-local-relay-envelope-validator.md` | Relay envelope validator evidence. |
| `docs/migration/reference/uaos-v1/requests/REQ-0056-local-relay-record-store-worker-claim-proof.md` | `L:\Applications\user-ai-operating-system\docs\requests\REQ-0056-local-relay-record-store-worker-claim-proof.md` | Relay store and worker claim evidence. |
| `docs/migration/reference/uaos-v1/requests/REQ-0057-uaos-final-shippable-plan.md` | `L:\Applications\user-ai-operating-system\docs\requests\REQ-0057-uaos-final-shippable-plan.md` | Final plan request record. |
| `docs/migration/reference/uaos-v1/requests/REQ-0058-closeout-turnover-and-work-tracking.md` | `L:\Applications\user-ai-operating-system\docs\requests\REQ-0058-closeout-turnover-and-work-tracking.md` | Turnover and work tracking closeout. |
| `docs/migration/reference/uaos-v1/apps/cockpit-command-proof-README.md` | `L:\Applications\user-ai-operating-system\apps\cockpit-command-proof\README.md` | Static cockpit proof notes. |

## Promoted Into Active Rev 2 Controls

| Active file | Source material | Promoted | Notes |
|---|---|---|---|
| `docs/source-of-truth-map.md` | `docs/migration/reference/uaos-v1/controls/source-of-truth-map.md` plus Rev 2 scaffold state | 2026-06-21T13:58:36-06:00 | Rewritten for Rev 2. It now distinguishes active controls from copied reference material and records the compact future chunk map. |
| `docs/tool-permission-matrix.md` | `docs/migration/reference/uaos-v1/controls/tool-permission-matrix.md` plus Rev 2 source-of-truth and device-role controls | 2026-06-21T14:16:18-06:00 | Rewritten for Rev 2. It defines current local, Git/GitHub, DirectLink, Windows/Linux, Android/browser, relay, connector, Graphify, M365, QuickBooks, client-data, vendor, deployment, voice, and model-provider boundaries without activating live connectors. |
| `docs/agent-runtime-instructions.md` | `docs/migration/reference/uaos-v1/controls/agent-runtime-instructions.md` plus Rev 2 tool permissions and current A1 posture | 2026-06-21T14:46:16-06:00 | Rewritten for Rev 2. It defines current local-only runtime scope, planning/execution separation, stale-state checks, stop behavior, evidence rules, and future runtime prerequisites without migrating v1 code. |
| `docs/agent-inventory.md` | Rev 2 scaffold placeholder plus current Rev 2 source-of-truth and device-role controls | 2026-06-21T14:46:16-06:00 | Rewritten for Rev 2. It lists the current Codex repo collaborator and future inactive runtime, worker, portal, and Graphify roles. |
| `docs/model-registry.md` | Rev 2 scaffold placeholder plus current model-provider boundary in the tool permission matrix | 2026-06-21T14:46:16-06:00 | Rewritten for Rev 2. It records that only the current coding-session model route is active for repo collaboration and no production runtime or BYOK model route is approved. |
| `docs/prompt-register.md` | Rev 2 scaffold placeholder plus active repo instruction files | 2026-06-21T14:46:16-06:00 | Rewritten for Rev 2. It records active instruction sources and the approval requirements for future runtime prompts. |
| `docs/architecture.md` | Copied v1 cross-device, relay, final shippable, connector, M365, Graphify, and cockpit proof references plus active Rev 2 controls | 2026-06-21T15:03:45-06:00 | Rewritten for Rev 2. It defines the active source spine, device roles, portal, worker, relay, connector, Graphify, data, and verification boundaries without migrating code or activating runtime behavior. |
| `docs/migration/file-migration-decisions.md` | Source inventory, active controls, copied v1 request records, and targeted existence checks for named v1 source candidates | 2026-06-21T15:20:04-06:00 | Created for Rev 2. It classifies the first code migration queue as rewrite-focused and excludes secrets, logs, generated artifacts, live connector state, client data, raw audio, and bulk v1 package copying. |

## Rewritten Into Active Rev 2 Code

| Active file | Source material | Rewritten | Notes |
|---|---|---|---|
| `packages/uaos-core/src/gail_ai_operating_system/mission_spine.py` | `L:\Applications\user-ai-operating-system\uaos_agent_spine\mission.py`, `planner.py`, and `policy.py` | 2026-06-21T15:39:29-06:00 | Rewritten for Rev 2 as local no-network mission envelopes, deterministic local plans, validation results, permission decisions, and local JSON store. No v1 file was bulk-copied. |
| `tests/test_mission_spine.py` | Selected behavior from the same mission-spine references | 2026-06-21T15:39:29-06:00 | Focused behavior tests for Chunk Nine. Broader safety-evaluation test migration remains Chunk Ten. |

## Not Copied Yet

- DirectLink operational scripts, indicators, runbooks, and skill files.
- Remaining UAOS Python code, selected v1 safety tests, static cockpit source,
  action logs, generated files, or local runtime artifacts. Candidate code
  paths are classified in `docs/migration/file-migration-decisions.md`; only
  the Chunk Nine mission spine has been rewritten into active Rev 2 source.
- Any `.env`, credentials, tenant secrets, tokens, private keys, invoices,
  accounting exports, QuickBooks data, Microsoft 365 content, client data, raw
  logs, or raw audio.
- The Linux master environment archive. It exists outside this repo as an
  operator-held secure copy and is not Rev 2 configuration.
- The shared parent-level `.env.master` working copy. It remains outside Rev 2
  and should be referenced by path only when explicitly needed.

## Next Migration Chunk

Use `docs/migration/file-migration-decisions.md` to begin Chunk Ten. The next
bounded task is to expand mission-spine tests from the approved v1
`tests\test_safety_evaluations.py` reference. Do not migrate any file that is
not listed in the decision record.
