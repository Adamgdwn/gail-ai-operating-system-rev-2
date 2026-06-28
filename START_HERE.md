# Start Here

Last Updated: 2026-06-27T22:23:45-06:00
Status: draft
Owner: Adam Goodwin

## Low-Token Restart

For the next session:

1. Run `git status --short`.
2. Read `AGENTS.md`.
3. Read this file.
4. Read `## Three-Repo Coordination Startup Flag`, Chunk Twenty, and
   `## Next Handoff` in `docs/current-build-pathway.md`.
5. Before building, explicitly acknowledge the current change of direction:
   GAIL AI Operating System Rev 2, Freedom, and AG Operations Workspace are
   being coordinated as three related builds, not folded together yet.
6. If creating or updating durable docs or work-tracking records, apply
   `docs/standards/2026-06-25 - Document Control Standard.md`.
7. Open the relay envelope/store, tool permission matrix, and command-center
   app files only when the user is ready to resume Rev 2 implementation.

Current direction: box the coordination pivot first. AG Operations Workspace
should finish and box its current evolution, Freedom remains the core operator
interface and high-level agentic business partner surface, and Rev 2 remains
the governed mission, policy, relay, approval-record, evidence, and worker
spine. The default Rev 2 build task remains Chunk Twenty - local governed
approval actions - but do not treat it as permission to merge repositories,
add bridge layers, or activate live systems.

Current CP-1 status: after the 2026-06-28 builder/Freedom handoff, the GAIL OS
FastAPI dev server proof is integration complete over DirectLink. Windows binds
the dev server to `10.77.77.1:8123`, Freedom on Linux reaches it, and the
Freedom `packages/gail-os-client/src/index.integration.ts` proof passed 4/4.
This remains an A1 local no-network dev proof only: no cloud placement, broad
firewall rule, live connector, Microsoft 365 access, production deployment, or
authority expansion is approved.

## Current Plan

For ordinary scoped work, agents should start with the lean startup checklist below. Read this file and follow the active plan named here for material work, unclear scope, handoffs, or changes that affect the active plan. Keep it short, current, and pointed at the active build path.

Current priorities:

- keep this repo as the clean Rev 2 workspace for GAIL AI Operating System work
- keep DirectLink as transport/status only, not the Rev 2 project home
- preserve the existing UAOS repo as superseded v1/reference material until migration is explicit
- keep the Linux master environment archive and shared parent-level working copy outside this repo; do not treat either as Rev 2 configuration or live connector approval
- use `gail-ai-operating-system-rev-2` as the canonical technical slug
- confirm copied references in `docs/migration/source-inventory.md` before code migration
- use the private GitHub repository `Adamgdwn/gail-ai-operating-system-rev-2` as the canonical remote after the initial scaffold push
- treat Microsoft 365, QuickBooks, finance, billing, and third-party systems as link-only/planning-only until approved connector boundaries exist
- apply `docs/policy/durable-development-engineering-policy.md` during implementation
- apply `docs/standards/ship-ready-engineering-standard.md` before declaring meaningful work complete
- use `docs/context-map.md` as the short routing map for task-specific context loads
- use `docs/source-of-truth-map.md` when deciding what is active Rev 2 source versus copied reference material
- keep startup lean: use short repo orientation first, then trigger governance, Graphify, plugins, MCP tools, and release checks by task risk or scope
- use Graphify before broad source exploration or architecture analysis, using workspace routing plus repo-local semantic graphs for heavy active repos
- fill in project commands in `AI_BOOTSTRAP.md`
- keep work in context-window-friendly chunks
- timestamp material work, decisions, validation, and handoffs
- preserve the completed Chunk Nineteen cockpit direction: a talk-first
  operator hub with observable governed spokes for Microsoft 365, Freedom,
  Graphify, QuickBooks, GitHub/build systems, evidence, and worker/device
  posture
- treat Freedom as the core operator interface and high-level agentic business
  partner surface; browser, hosted, desktop, and tablet command-center surfaces
  should augment or coordinate with Freedom rather than compete with it
- never build a competing native phone app for Rev 2; phone-side work should
  augment Freedom through governed bridge contracts, summaries, links, and
  fallback views unless Adam explicitly reverses this decision
- prefix newly authored durable documents and work-tracking records with a
  filename date stamp such as `YYYY-MM-DD - <title>.md`; also include an
  internal `Date: YYYY-MM-DD` marker where useful. Existing required repo files
  with stable routes may keep their current names unless a bounded rename plan
  updates all references.
- apply `docs/standards/2026-06-25 - Document Control Standard.md` for new durable documents
  across GAIL AI Operating System Rev 2, Freedom, and AG Operations Workspace:
  use the first durable saved/promoted date in the filename, and update
  internal `Last Updated` metadata for later edits instead of renaming files
  repeatedly; do not date-prefix dependency manifests, lockfiles, importable
  source modules, schemas, generated files, CI workflows, or tool-owned config
  files
- keep Chunk Twenty approval actions local, governed, auditable, stale-state
  protected, and non-executing until later connector and runtime boundaries are
  explicitly approved
- let AG Operations finish and box its current agentic-assistance evolution
  before deciding whether Rev 2, Freedom, and AG Operations should remain
  separate, bridge, fold, or defer; use
  `docs/decisions/2026-06-24 - Build Consolidation Decision Process.md` for
  that review and do not add weak pass-through layers or runtime coupling first
- treat the current owner direction as a three-repo coordination change:
  coordinate GAIL AI Operating System Rev 2, Freedom, and AG Operations
  Workspace deliberately, keep their ownership boundaries visible at startup,
  and require an explicit decision-process review before any consolidation,
  shared runtime, or source-of-truth change
- the promoted Graphify acceleration GA-B/GA-C local readiness package is now
  ready for the agentic multi-agent agent builder to consider in a revised
  orchestration plan: Rev 2 has the local contract, sanitized emitters,
  deterministic preview JSONL, safe preview diff/cache checks, and operator
  preview handoff under the ignored preview boundary; do not retain generated
  preview output, imply Graphify ingest, add adapters, expose HTTP/cloud
  paths, read live business systems, or grant execution authority
- treat Graphify acceleration as a high-importance neuronal pathway track for
  future fast relationship intelligence, while keeping AG Operations Workspace
  Setup as a later governed Microsoft 365 tactile input/output boundary and
  preserving the current Freedom input/output boundary
- use `docs/decisions/2026-06-27 - Builder Graphify Freedom AG Operations Integration Summary.md`
  as the current coordination summary to send to the agentic multi-agent agent
  builder with the GA-B/GA-C readiness package; it records the builder schema
  foundation, the Rev 2 hardening/Graphify preview work, and the wish list for
  integrating Freedom, Codex and future coding agents, AG Operations Workspace
  / Microsoft 365, and Graphify without promoting live connectors or authority

## Current Build Pathway

Default live build route: [docs/current-build-pathway.md](docs/current-build-pathway.md).

If this project later promotes a different active plan, name it here and route
agents there instead of rereading archived pathway history.

For ordinary scoped work:

1. Run `git status --short`.
2. Read the repo-local agent instructions.
3. Use `docs/context-map.md` when context routing is unclear.
4. Inspect the specific files, errors, or docs needed for the task.
5. Run targeted validation after the change.

For material or risk-triggering changes:

1. Run `bash scripts/governance-preflight.sh`.
2. Review `docs/standards/README.md`.
3. Review `docs/standards/engineering-governance-by-use-case.md`.
4. Review `docs/policy/durable-development-engineering-policy.md`.
5. Review `docs/standards/ship-ready-engineering-standard.md`.
6. Review `project-control.yaml`.
7. Check `exceptions` in `project-control.yaml` and any exception records.
8. For broad source exploration, architecture analysis, dependency tracing, or cross-repo planning, use the Graphify policy at `/home/adamgoodwin/code/Tools/graphify/docs/agent-governance.md` before reading raw source broadly. Reference `/home/adamgoodwin/code/Tools/graphify/workspace/out/graph.json` for cross-repo routing, set up repo-local Graphify when a new repo becomes active, run `/graphify /path/to/repo` from Claude Code for full semantic repo graphs on heavy active repos, and update the relevant graph after code changes.
9. Capture the work timestamp with `date -Iseconds`.
10. Work in the smallest complete chunk that can be reviewed safely.

Risk-triggering work includes production, deployment, authentication, authorization, payments, secrets, sensitive data, database migrations, customer communications, external side effects, infrastructure or provider settings, destructive actions, autonomous tool use, risk classification, governance policy changes, or release readiness.

Rev 2 stop triggers also include live Microsoft 365 content reads, Outlook or
Teams sends, Entra/admin/permission changes, QuickBooks or accounting reads,
invoice/payment/billing actions, vendor account changes, and client-data access.

## Agent Handoff

Update this file only when the top-level plan or handoff point changes. Put detailed step-by-step progress in the active plan named above.

After compaction or a context clear, restart from the latest handoff/work packet,
then run `git status --short`, read the short repo-local instructions, and open
only the active plan and files needed for the next objective. Use
`docs/source-of-truth-map.md` when the next objective needs source routing,
device-role context, or migration boundary context.
