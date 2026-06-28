# Context Map

Document type: project context routing map
Last Updated: 2026-06-28T08:33:50-06:00
Status: draft
Owner: Technical Lead
Audience: coding agents, human coders, reviewers, and project owners

## Purpose

This file keeps agent context loads small, deliberate, and recoverable.

The repository remembers. Agents rent context. Use this map to decide what to
load first, what to load by task type, and what to avoid unless the task needs
it.

## Always Load

- `AGENTS.md` or the active agent instruction file
- `START_HERE.md` for material work, unclear scope, or changes to the active plan
- `project-control.yaml` when risk, governance level, controls, or required docs matter

Keep these files compact. They should route to durable docs, not duplicate them.

## Load By Task

| Task | Load First |
|---|---|
| Current plan, chunking, validation, or handoff | Active execution packet named by `START_HERE.md`; for the current GitHub catch-up, read `docs/decisions/2026-06-28 - Current Main Stabilization Work Packet.md` before opening the large historical pathway |
| Current-main stabilization, GitHub catch-up, red CI after M365 dry-run merge, CMS-A/CMS-B/CMS-C | `docs/decisions/2026-06-28 - Current Main Stabilization Work Packet.md`, then only the targeted connector registry, M365 API, evidence, or handoff files needed for the selected CMS chunk |
| Source-of-truth routing, active versus reference docs, device roles, or compact future chunk map | `docs/source-of-truth-map.md` |
| Engineering standards map | `docs/standards/README.md` |
| Document naming, dated filenames, document control, work-tracking records, pathway logs, handoffs, ADRs, audits, or runbooks | `docs/standards/2026-06-25 - Document Control Standard.md`, then `docs/source-of-truth-map.md` for stable-route exceptions |
| Context windows, token budgets, compaction, scoped reads, or handoffs | `docs/standards/context-hygiene-standard.md` |
| Durable implementation, design quality, testing discipline, or AI coding fundamentals | `docs/policy/durable-development-engineering-policy.md` |
| Use-case controls, risk tier, governance level, or owner decisions | `docs/standards/engineering-governance-by-use-case.md` |
| Completion labels, Definition of Shipped, release evidence, or finish reports | `docs/standards/ship-ready-engineering-standard.md` |
| Architecture decisions or system shape | `docs/architecture.md` and relevant ADRs |
| Three-repo coordination, startup direction change, build consolidation, weak-layer review, or deciding whether GAIL AI Operating System Rev 2, Freedom, and AG Operations Workspace should become one build | `START_HERE.md`, `docs/decisions/2026-06-28 - Current Main Stabilization Work Packet.md` for the current no-fallback boundary, `docs/decisions/2026-06-24 - Build Consolidation Decision Process.md`, `docs/architecture.md`, `docs/source-of-truth-map.md`, and the current AG Operations handoff after its active evolution is boxed; open the large pathway only for older chunk history |
| Agentic multi-agent builder handoff, Graphify acceleration package summary, or integration wish list across Freedom, Codex/future coding agents, AG Operations Workspace / Microsoft 365, and Graphify | `docs/decisions/2026-06-27 - Builder Graphify Freedom AG Operations Integration Summary.md`, `docs/decisions/2026-06-27 - Graphify Acceleration Readiness Plan.md`, `docs/decisions/2026-06-28 - Current Main Stabilization Work Packet.md` when CMS-C is in scope, and `docs/source-of-truth-map.md` |
| Freedom phone interface, business-partner capability preservation, or Freedom bridge boundaries | `docs/decisions/freedom-phone-interface-business-partner-boundary.md`, `docs/migration/freedom-engine-objective-review.md`, `docs/architecture.md`, and `docs/migration/file-migration-decisions.md` |
| App shell, command center, portal stack, browser cockpit, or multi-device review surface | `docs/decisions/app-shell-command-center.md`, `docs/decisions/freedom-phone-interface-business-partner-boundary.md`, `docs/architecture.md`, and `apps/command-center/README.md` |
| File migration, source promotion, rewrite decisions, or exclusion checks | `docs/migration/source-inventory.md`, `docs/migration/file-migration-decisions.md`, and the relevant copied v1 reference records |
| Graphify routing, graph-aware handoffs, repo-local graph setup, Graphify acceleration readiness, preview retention, preview command behavior, preview diff/cache behavior, or Graphify stop boundaries | `docs/graphify-handoff-checkpoint.md`, `docs/decisions/2026-06-27 - Graphify Acceleration Readiness Plan.md`, `docs/decisions/2026-06-27 - Graphify Preview Retention Decision.md`, `packages/uaos-core/src/gail_ai_operating_system/graphify_acceleration.py`, `packages/uaos-core/src/gail_ai_operating_system/graphify_acceleration_preview.py`, then the Graphify policy named there when broad exploration is in scope |
| Domain terms or naming | `docs/domain-language.md` |
| Deployment, release, rollback, or environment changes | `docs/deployment-guide.md`, `docs/runbook.md`, and release standards |
| Agent autonomy, runtime behavior, tools, prompts, models, or permissions | `docs/agent-runtime-instructions.md`, `docs/agent-inventory.md`, `docs/model-registry.md`, `docs/prompt-register.md`, and `docs/tool-permission-matrix.md` |

## Search Before Loading

- long audit reports
- old pathway history below the current active chunk
- logs, generated reports, and command output
- exported manifests
- archived plans or superseded briefs

Use `rg` or targeted file excerpts before opening long files.

## Avoid Unless Needed

- `.git/`
- `.venv/`, `venv/`, `node_modules/`, and dependency caches
- build output, coverage, and generated artifacts
- ignored Graphify output
- secrets and environment files
- large transcripts or pasted chat histories

Do not print, summarize, index, or commit secrets.

## Work Packet Reminder

For meaningful work, define:

- goal
- budget class: Tiny, Small, Medium, Large, or Strategic
- context to load first
- files or folders to avoid unless needed
- constraints and non-goals
- done-when checks
- handoff location

Tiny edits may use an inline version of this packet. Large or strategic work
should record the packet in the active execution packet named by
`START_HERE.md`, an ADR, or a short handoff note.

## Document Naming

Use `docs/standards/2026-06-25 - Document Control Standard.md` for document naming. New
durable documents and work-tracking records saved after 2026-06-25 should use a
date-stamped filename prefix, such as `YYYY-MM-DD - <title>.md`, based on the
first durable save or promotion date. Later edits update internal metadata
rather than renaming the file. Existing required repo files with stable routing
paths may keep their current names unless a bounded rename plan updates all
references.

## Maintenance

Update this file when the repo's routing paths change or when agents repeatedly
load the wrong material. Keep it short enough to read at startup when context
routing is unclear.
