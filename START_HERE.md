# Start Here

Last Updated: 2026-06-28T22:14:09-06:00
Status: draft
Owner: Adam Goodwin

## Low-Token Restart

For the next session:

1. Run `git status --short`.
2. Read `AGENTS.md`.
3. Read this file.
4. Read
   `docs/decisions/2026-06-28 - Current Main Stabilization Work Packet.md`.
   Open `docs/current-build-pathway.md` only when older chunk history or a
   specific historical pathway section is needed.
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
spine. Chunk Twenty - local governed approval actions - remains the historical
next Rev 2 build task after current-main stabilization closes or Adam
explicitly redirects. Do not treat it as permission to merge repositories, add
bridge layers, or activate live systems.

Current CP-1 status: after the 2026-06-28 builder/Freedom handoff, the GAIL OS
FastAPI dev server proof is integration complete over DirectLink. Windows binds
the dev server to `10.77.77.1:8123`, Freedom on Linux reaches it, and the
Freedom `packages/gail-os-client/src/index.integration.ts` proof passed 4/4.
This remains an A1 local no-network dev proof only: no cloud placement, broad
firewall rule, live connector, Microsoft 365 access, production deployment, or
authority expansion is approved.

Current GitHub stabilization status: as of 2026-06-28T09:57:53-06:00, the
feature-merge baseline is `2bcdeb7`, adding agent registry, authority override,
M365 dry-run observe/write, and local evidence persistence work. CMS-A is
complete and GitHub Actions run `28326055021` passed. CMS-B local proof is
complete: focused API/M365 tests, full Python tests, Windows HTTP probes, and
the Linux Freedom CP-1 script passed against a temporary local server with
synthetic M365 env values and dry-run evidence only. CMS-C is complete and the
compact builder-facing handoff is
`docs/decisions/2026-06-28 - Current Main Stabilization Builder Report.md`.
The compact stabilization packet remains
`docs/decisions/2026-06-28 - Current Main Stabilization Work Packet.md` for
validation detail. The next owner decision is whether to send the CMS-C report
to the agentic multi-agent builder, resume Chunk Twenty local governed
approval actions, explicitly run or continue pausing the optional CMS-B
browser-login edge, or open a formal Microsoft 365 connector-promotion design
gate. The agent must pause for Adam to say "yes, go ahead" before opening any
browser login, OAuth, or consent surface. Do not proceed into live Microsoft
365 access, cloud placement, Graphify ingest, schema publication, browser
login, OAuth consent, tenant admin consent, or further authority expansion
without an explicit owner decision.

Current local CNS connection status: as of 2026-06-28T17:49:02-06:00, the
first post-CMS connection scout is captured in
`docs/decisions/2026-06-28 - Local CNS Connection Proof Report.md`. Freedom can
reach GAIL OS over DirectLink and Graphify on Linux localhost; GAIL OS Graphify
fact/evidence contracts and Graphify CNS API route contracts are green. The
report was rebased onto `origin/main` at `5478b64`, after another agent added
GAIL OS OKP, Signal Gravity L1, CP-5 GAIL OS proof, R4 doctrine/schema,
R4 dry-run simulation, and R4 live-executor code. The next safe lane is a
bounded local CNS connection-test proof. The Linux request to expand Entra
permissions remains a separate Microsoft 365 connector-promotion decision and
is not approved by this connection scout. R4 live-executor code being present
on `main` is not approval to run R4 live mutations.

Follow-on CTP-2 status: as of 2026-06-28T18:19:59-06:00, the local triangle
proof is integration complete. Linux proved Freedom to GAIL OS, Freedom to
Graphify, GAIL OS M365 dry-run status/observe, authority override, and agents
registry probes. Windows refreshed the GAIL OS dev server and patched two
small API contract gaps: `GET /api/v1/authority` now returns a read-only R0-R5
authority registry, and `POST /api/v1/m365/observe` accepts a synthetic
`{"dry_run": true}` probe body while rejecting `dry_run=false` and still
forcing dry-run/no-live behavior internally. The live dev API is bound to
`10.77.77.1:8123` and exposes 14 routes. This does not approve Entra scope
expansion, live Microsoft Graph calls, persistent Graphify ingest, cloud
placement, production service behavior, or R4 live execution.

Current CNS communication contract status: as of 2026-06-28T18:44:28-06:00,
`docs/decisions/2026-06-28 - CNS Communication Enhancement Contract.md` is
draft complete for the agentic multi-agent agent builder. It defines the
builder-facing `cns_trace_id`, `SignalPacket`, `FreedomRelationshipBrief`,
`GraphifyFactBundle`, `AppSignalEnvelope`, `AppActionEnvelope`, and
`BuildHandoffFact` direction so enhanced Graphify can accelerate context
without becoming authority or execution. This is a coordination contract only;
it does not approve live Microsoft 365 access, Graphify ingest, cloud
placement, source-of-truth migration, runtime consolidation, R4 live execution,
or authority expansion.

Current Azure Container Apps pilot status: as of 2026-06-28T20:22:25-06:00,
Adam approved cloud placement for the narrow H2/H3 pilot deployment. GAIL OS
API and Graphify CNS API are deployed in Azure Container Apps under the
personal credit-bearing Azure subscription, with public health endpoints green
and fresh pilot API keys stored in Key Vault. The durable deployment report is
`docs/decisions/2026-06-28 - Azure Container Apps Pilot Deployment Report.md`.
Graphify CNS API initially used the documented ephemeral SQLite fallback, then
the pre-registered Azure Files share was mounted by YAML update and verified
healthy. This does not approve Microsoft 365 live access, tenant consent,
persistent Graphify production ingest, source-of-truth migration, runtime
consolidation, R4 live execution, or production service readiness.

Current Freedom to Azure H4 status: as of 2026-06-28T22:00:30-06:00, Adam
approved completing the bounded H4 connection. Windows retrieved the two pilot
API keys from `kv-gail-cns-pilot` and applied them directly to Freedom's
git-ignored local `.env.local` on Linux without printing, committing, or
writing secret values into DirectLink/docs/logs/chat. Linux smoke-tested
Freedom to Azure successfully: Freedom health, GAIL OS ACA direct health,
Graphify ACA direct health, bearer-key auth, Freedom to GAIL OS proxy, Freedom
to Graphify proxy, and all five local env vars passed. Windows also ran the
existing Freedom GAIL OS client integration against Azure, passing 4/4, and a
Graphify health probe returned HTTP 200 with `status=ok`, `store=connected`,
and `node_count=0`. H4 is complete.

Current Freedom Supabase H5 status: as of 2026-06-28T22:14:09-06:00, Adam
approved the H5 audit/remediation package. Freedom now has a dated security
plan, forward RLS migration, explicit rollback SQL, and changelog entry for the
legacy public Supabase tables. Source migrations plus a read-only service-role
REST existence probe found 21 legacy public tables present, not the 20 named in
the builder handoff, so H5 covers all 21. The package enables RLS without
adding anon/authenticated policies, preserving the server-side-only
service-role posture. No hosted Supabase migration was applied, no row data or
secret values were printed, and applying the migration remains a separate Adam
approval gate.

Current Microsoft 365 permission-expansion status: as of
2026-06-28T20:55:36-06:00, Adam approved the Entra delegated permission
expansion for `Guided AI Labs - CLI for Microsoft 365 Local Agent`, including
the previously paused Microsoft 365 read/write scopes plus mail, calendar, and
Exchange Online delegated management scopes. Admin consent for A.G. Operations
Ltd is complete, with no client secret or certificate created. The durable
non-secret report is
`docs/decisions/2026-06-28 - M365 Entra Permission Expansion Report.md`. This
does not approve live business-system writes, Outlook sends, Teams sends,
Planner writes, SharePoint mutations, Power Automate changes, Exchange
configuration changes, Graphify production ingest, R4 live execution, or
production readiness without a separate owner-gated proof/action boundary.

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
- use `docs/decisions/2026-06-28 - CNS Communication Enhancement Contract.md`
  as the current builder-facing communication target for enhancing the
  Freedom/GAIL OS/Graphify/AG Operations loop with shared trace identity,
  relationship briefs, application signal envelopes, build handoff facts, and
  owner-gated Graphify ingest boundaries
- use `docs/decisions/2026-06-28 - Azure Container Apps Pilot Deployment Report.md`
  as the current non-secret record of the owner-approved H2/H3 Azure Container
  Apps pilot endpoints, health checks, Key Vault secret handling, and the
  Graphify Azure Files volume mount follow-on
- use `docs/decisions/2026-06-28 - M365 Entra Permission Expansion Report.md`
  as the current non-secret record of the owner-approved A.G. Operations tenant
  delegated permission expansion and admin-consent boundary

## Current Build Pathway

Current execution packet:
[docs/decisions/2026-06-28 - Current Main Stabilization Work Packet.md](docs/decisions/2026-06-28%20-%20Current%20Main%20Stabilization%20Work%20Packet.md).

Historical master pathway:
[docs/current-build-pathway.md](docs/current-build-pathway.md).

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
