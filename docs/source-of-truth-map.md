# Source Of Truth Map

Created: 2026-06-21T13:58:36-06:00
Last Updated: 2026-06-21T15:03:45-06:00
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
| `docs/architecture.md` | Active Rev 2 architecture for source spine, portal surfaces, workers, relay records, Graphify, connector boundaries, and verification ladder. |
| `docs/migration/source-inventory.md` | Migration source boundary and reference inventory. |
| `docs/standards/README.md` | Standards index. |
| `docs/policy/durable-development-engineering-policy.md` | Durable development policy. |
| `docs/standards/engineering-governance-by-use-case.md` | Use-case governance expectations. |
| `docs/standards/ship-ready-engineering-standard.md` | Completion labels and ship-readiness evidence gate. |

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

## Device Roles

| Surface | Rev 2 role | Boundary |
|---|---|---|
| Windows | Current operator workspace and future trusted worker. | May edit/push Rev 2 repo and run local validation; live business connectors remain blocked until approved. |
| Linux | Superseded v1 reference host and future trusted worker clone. | Not the Rev 2 project home; future Linux work must pull from private GitHub and preserve Rev 2 controls. |
| Android phone | Future mobile operator cockpit. | Intent capture, approval, pause/resume, and safe evidence summaries only; no local execution or raw secrets/logs. |
| Android tablet | Future review cockpit. | Larger evidence and status review surface; no unrestricted connector or filesystem access. |
| Browser | Shared cockpit surface across desktop and mobile. | Reads/writes governed records through approved local or relay paths; must not become a second source of truth. |
| Private GitHub | Canonical durable spine. | Commits, request records, issues/PRs, relay references, and evidence links; no secrets or unredacted sensitive payloads. |
| Graphify | Knowledge spoke. | Read-only handoff and graph references; recommendations are not execution approval. |

## Compact Build Chunk Map

These are planning boundaries for future work. The active chunk and validation
ledger remain in `docs/current-build-pathway.md`.

| Phase | Chunk range | Purpose |
|---|---|---|
| Phase 1 - Active controls | Chunks Four to Eight | Promote Rev 2 navigation, permission, runtime, architecture, and migration-decision controls. |
| Phase 2 - File migration and initial build-out | Chunks Nine to Fifteen | Migrate/rewrite the no-network mission spine, connector registry, Graphify handoff, relay envelope, relay store, tests, and proof runner. |
| Phase 3 - First usable portal | Chunks Sixteen to Twenty | Build the browser command center, mobile-responsive views, approval actions, and evidence/handoff views. |
| Phase 4 - Multi-device worker model | Chunks Twenty-One to Twenty-Five | Add Windows/Linux worker bootstrap, role checks, GitHub-backed relay records, and conflict recovery. |
| Phase 5 - Full system build | Chunks Twenty-Six onward | Evaluate hosted relay, notifications, approved connector activation, Client Gateway boundaries, vendor intelligence, runbooks, pilot, and release decision. |

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

Record file migration decisions next. Do not migrate UAOS code until migration
decisions are explicit, bounded, and validated.
