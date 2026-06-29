# Current Main Stabilization Work Packet

Document type: work packet
Date: 2026-06-28
Saved: 2026-06-28T08:33:50-06:00
Last Updated: 2026-06-28T23:00:22-06:00
Status: boxed for night; current-main stabilization, CTP-2, CNS contract, H2/H3 ACA pilot, H4 Freedom-Azure connection, H5 Supabase RLS hosted apply, and M365 permission expansion are recorded; remaining live-action proofs stay gated (2026-06-28T23:00:22-06:00)
Owner: Adam Goodwin

## Purpose

This packet keeps the current GitHub catch-up work small enough for low-token
startup. It was the active execution packet for current-main stabilization
through CMS-A, CMS-B, and CMS-C. It now serves as the validation record and
handoff detail for that completed stabilization pass.

`docs/current-build-pathway.md` remains the historical master pathway and
ledger. Do not read the full pathway just to execute this packet unless a
specific question needs older chunk history.

## Current State

Feature-merge baseline: GitHub `main` advanced from the prior CP-1 bridge work
at `dab1883` to `2bcdeb7`.

Planning baseline: the later docs commit `30b12ad` added the first compact
CMS-A/CMS-B/CMS-C stabilization plan. This packet moves that plan out of the
large pathway without changing code or approving execution.

Known red check at packet creation: GitHub Actions was failing on two
connector-registry alignment tests:

- `tests/test_api_m365_bridge.py::test_m365_bridge_display_name`
- `tests/test_connector_registry.py::ConnectorRegistryTests::test_initial_connector_profiles_are_valid_and_not_live_enabled`

Observed failure shape: `m365-graph-api-bridge` exists as a new planning-only
connector, but two tests still assert the older connector registry shape. The
failure is not currently known to be a runtime failure or a live Microsoft 365
failure.

CMS-A closeout: as of 2026-06-28T08:54:02-06:00, the registry/test alignment
fix is locally green and GitHub Actions run `28326055021` passed. The fix keeps
`m365-graph-api-bridge` in the registry, preserves
`live_access_enabled=False`, preserves the profile's planning-only/registry-only
boundary, adds the `svc-gail-os-graph` identity to the bridge notes, and
updates the stale expected connector ID set in `tests/test_connector_registry.py`.

CMS-B local proof closeout: as of 2026-06-28T09:11:34-06:00, the local runtime,
M365 dry-run, evidence, and DirectLink/Freedom CP-1 proof paths are green. The
optional login edge is not executed yet; it is paused for Adam's explicit
"yes, go ahead" or "pause" decision after Codex explains the exact browser
login probe.

CMS-C closeout: as of 2026-06-28T09:57:53-06:00, the current-main
stabilization handoff is reconciled in
`docs/decisions/2026-06-28 - Current Main Stabilization Builder Report.md`.
The report records the actual CMS-A/CMS-B proof state, the remaining
no-live-connector boundaries, the roles of Freedom, Graphify, GAIL OS, AG
Operations Workspace / Microsoft 365, and the next owner decision before
further feature work.

Local CNS connection scout: as of 2026-06-28T17:55:25-06:00, the first
post-CMS connection proof across Freedom, GAIL OS, and Graphify is captured in
`docs/decisions/2026-06-28 - Local CNS Connection Proof Report.md`. Freedom can
reach GAIL OS over DirectLink and Graphify on Linux localhost; GAIL OS Graphify
fact and evidence contracts are locally green; Graphify CNS API route contracts
are green. The report was rebased onto `origin/main` at `5478b64`, after
another agent added GAIL OS OKP, Signal Gravity L1, CP-5 GAIL OS proof,
R4 doctrine/schema, R4 dry-run simulation, and R4 live-executor code. No
Microsoft 365 permission expansion, tenant/admin consent, live Graph call,
persistent Graphify CNS store ingest, cloud placement, production service
behavior, or R4 live execution was performed by this scout.

CTP-2 follow-on: as of 2026-06-28T18:19:59-06:00, Linux completed the local
triangle proof against the Windows GAIL OS server and Windows patched the two
small contract gaps exposed by the probe. The live dev server now exposes 14
routes including a read-only `/api/v1/authority` registry. The
`/api/v1/m365/observe` endpoint accepts a synthetic dry-run probe body and
rejects live-style `dry_run=false`; it still calls the service layer with
`dry_run=True, allow_live=False`. Focused API validation passed: 82 tests. No
Entra permission expansion, tenant/admin consent, live Microsoft Graph call,
Planner write, persistent Graphify CNS store ingest, cloud placement,
production service behavior, or R4 live execution was performed.

CNS communication contract follow-on: as of 2026-06-28T18:44:28-06:00,
`docs/decisions/2026-06-28 - CNS Communication Enhancement Contract.md` is
draft complete for builder orchestration. It defines the next communication
target around `cns_trace_id`, signal packets, Freedom relationship briefs,
Graphify fact bundles, application signal/action envelopes, build handoff
facts, and owner-gated Graphify ingest. This remains documentation only and
does not approve live Microsoft 365 access, Graphify ingest, cloud placement,
runtime consolidation, source-of-truth migration, R4 live execution, or
authority expansion.

Azure Container Apps pilot follow-on: as of 2026-06-28T20:22:25-06:00, Adam
approved the narrow H2/H3 cloud placement step requested by the Linux builder.
Windows deployed `aca-gail-os-api` and `aca-graphify-cns-api`, verified both
public health endpoints, generated fresh pilot API keys into Key Vault, and
wrote the Linux handoff
`X:\WINDOWS_TO_LINUX__2026-06-28-aca-apps-deployed.md`. The durable non-secret
record is
`docs/decisions/2026-06-28 - Azure Container Apps Pilot Deployment Report.md`.
Graphify CNS API initially used the documented ephemeral SQLite fallback
because the installed `az containerapp create` surface did not expose the
requested volume mount flags. The pre-registered Azure Files share was then
mounted by YAML update and verified healthy in
`X:\WINDOWS_TO_LINUX__2026-06-28-graphify-volume-mounted.md`. This pilot
deployment does not approve Microsoft 365 live access, tenant/admin consent,
live Graph calls, persistent Graphify production ingest, R4 live execution,
source-of-truth migration, runtime consolidation, or production service
readiness.

M365 permission expansion follow-on: as of 2026-06-28T20:55:36-06:00, Adam
approved the previously paused Entra delegated permission expansion for
`Guided AI Labs - CLI for Microsoft 365 Local Agent`, including Microsoft 365
read/write scopes plus mail, calendar, and Exchange Online delegated
management scopes. Windows added the delegated scopes, granted admin consent
for A.G. Operations Ltd, verified tenant-wide delegated grants, verified that
no client secret or certificate exists, and wrote the Linux handoff
`X:\WINDOWS_TO_LINUX__2026-06-28-entra-permissions-expanded.md`. The durable
non-secret record is
`docs/decisions/2026-06-28 - M365 Entra Permission Expansion Report.md`. This
permission change does not itself approve live SharePoint mutations, Teams
sends, Outlook sends, Planner writes, Power Automate changes, Exchange
configuration changes, business-system actions, Graphify production ingest,
R4 live execution, source-of-truth migration, runtime consolidation, or
production service readiness.

H4 Freedom to Azure connection follow-on: as of 2026-06-28T22:00:30-06:00,
Adam approved completing the bounded H4 connection step. Windows retrieved the
GAIL OS and Graphify pilot API keys from `kv-gail-cns-pilot` and applied them
directly to Freedom's git-ignored local `.env.local` on Linux without
printing, committing, or writing secret values into DirectLink/docs/logs/chat.
Linux smoke-tested Freedom to Azure successfully: Freedom health, GAIL OS ACA
direct health, Graphify ACA direct health, bearer-key auth, Freedom to GAIL OS
proxy, Freedom to Graphify proxy, and all five local env vars passed. Windows
also ran the existing Freedom GAIL OS client integration against Azure, passing
4/4, and verified Graphify health HTTP 200 with `status=ok`,
`store=connected`, and `node_count=0`. H4 is complete.

H5 Supabase RLS audit/apply follow-on: as of 2026-06-28T22:50:00-06:00, Adam
approved hosted application of the H5 RLS migration after the audit/remediation
package was drafted. The work belongs in Freedom, not Rev 2. Freedom now has
`docs/security/2026-06-28 - Supabase RLS Remediation Plan.md`,
`supabase/migrations/202606280001_enable_rls_for_legacy_public_tables.sql`,
`supabase/rollbacks/202606280001_disable_rls_for_legacy_public_tables.sql`,
and changelog entries for the package and hosted apply. The package reconciles
the builder's 20-table note with source migration and read-only REST evidence
showing 21 legacy public tables present, covers all 21, and keeps them
server-side-only by enabling RLS without adding anon/authenticated policies.
The hosted apply returned HTTP 201 through the Supabase Management API database
query endpoint. Post-apply metadata confirmed 21/21 target tables present,
21/21 with `relrowsecurity=true`, 0 target policies, and 21/21 service-role
HEAD probes passing without row-data reads. No secret values, tokens, database
passwords, or `.env` values were printed, copied, or committed.

Night closeout follow-on: as of 2026-06-28T23:00:22-06:00, the compact resume
record is
`docs/decisions/2026-06-28 - Nightly Turnover And Token-Friendly Startup.md`.
It is the preferred first read after `AGENTS.md` for the next session. Rev 2 is
clean and synced to `origin/main`; Freedom is synced to `origin/main` with only
unrelated generated APK artifacts modified locally; DirectLink shows Linux
ACKed H5-apply and the ball is back with Windows/Adam for the next lane.

## No-Fallback Boundaries

- Do not resume feature work or old Chunk Twenty implementation while current
  `main` remains red.
- Do not mask the failing tests by deleting the M365 bridge connector or
  weakening planning-only connector boundaries.
- Do not activate live Microsoft 365 reads, Outlook or Teams sends, Planner
  writes, SharePoint mutations, Power Automate changes, Exchange configuration
  changes, or business-system actions merely because the delegated permissions
  now exist.
- Do not open another interactive browser login, complete another OAuth flow,
  approve further consent, retain token-bearing artifacts, or broaden Entra
  scopes unless Adam explicitly approves that specific owner-gated edge step
  after an in-chat explanation.
- The 2026-06-28 owner-approved Entra delegated permission expansion is now
  complete. Do not treat that permission availability as approval for live
  content reads, writes, sends, flow changes, Exchange configuration changes,
  production operation, or R4 execution without a separate owner-gated
  proof/action boundary.
- Do not treat dry-run M365 endpoints as approved live connector activation.
- Do not treat the CP-1 DirectLink FastAPI proof as production service,
  cloud placement, broad network exposure, or schema publication.
- Do not treat the H2/H3 ACA pilot deployment as production service readiness,
  live connector activation, Microsoft 365 access approval, persistent
  Graphify ingest approval, source-of-truth migration, runtime consolidation,
  or R4 live execution approval.
- Do not treat the H4 Freedom to Azure smoke pass as production service
  readiness, Vercel environment promotion, live Microsoft 365 business-action
  approval, persistent Graphify production ingest approval, source-of-truth
  migration, runtime consolidation, or R4 live execution approval.
- Do not treat the completed H5 Supabase RLS hosted apply as approval for any
  further Supabase schema, policy, data, credential, or production workflow
  change. Rolling back or applying follow-on migrations requires a separate Adam
  approval gate and fresh backup/rollback posture confirmation unless immediate
  recovery is required.
- Do not treat Graphify preview/diff output as Graphify ingest, evidence,
  approval, relay, source-of-truth, or execution authority.
- Do not rename stable-route files or pre-standard documents without a bounded
  rename plan that updates references and validates links.

## CMS-A - Green Current Main And Align Tests

Status: task complete (2026-06-28T08:54:02-06:00)

Completion target: Task complete

Budget class: Small

Inputs: `origin/main`, GitHub Actions run `28313436058`, connector registry,
M365 bridge tests, and the existing full pytest suite.

Outputs: the smallest registry/test alignment fix that makes CI green without
changing connector authority.

Acceptance:

- local full pytest passes;
- connector registry still contains `m365-graph-api-bridge`;
- `live_access_enabled` remains false for planning-only connectors;
- CI is expected to pass after push.

Validation:

- focused connector registry tests;
- focused M365 bridge/API tests;
- full Python test suite;
- `git diff --check`;
- governance preflight if the fix touches policy or connector authority.

Validation evidence:

- `.\.venv\Scripts\python.exe -m pytest tests/test_connector_registry.py tests/test_api_m365_bridge.py -q` passed: 21 passed, 1 warning.
- `.\.venv\Scripts\python.exe -m pytest tests/test_connector_registry.py tests/test_api_connectors.py tests/test_api_m365_bridge.py tests/test_m365_auth.py tests/test_m365_observe.py tests/test_m365_write.py tests/test_m365_evidence_store.py -q` passed: 78 passed, 1 warning.
- `.\.venv\Scripts\python.exe -m pytest -q` passed: 419 passed, 3 warnings, 55 subtests passed.
- `bash scripts/governance-preflight.sh` passed with 0 warnings.
- GitHub Actions CI run `28326055021` passed after push.

Stop before adding endpoints, broadening M365 scope, changing live access,
changing secrets handling, or masking a real registry regression.

## CMS-B - Reprove Runtime, Dry-Run Boundaries, And Login Edge Gate

Status: local proof complete; owner-gated login edge paused (2026-06-28T09:11:34-06:00)

Completion target: Integration complete

Budget class: Small

Inputs: greened current main, ignored local venv, FastAPI app, Freedom CP-1
client, M365 dry-run endpoints, and local evidence store path.

Outputs: a fresh local proof that GAIL OS still serves Freedom over DirectLink
and that the M365 endpoints remain dry-run/no-live-call surfaces, followed by
a separate owner-gated login edge briefing if the local proof is green.

Acceptance:

- health, missions, actions, connectors, agents, authority override, M365
  status, M365 observe dry-run, M365 Planner dry-run, and evidence retrieval
  behave as documented under local runtime constraints;
- generated evidence remains synthetic/local unless Adam explicitly approves a
  live connector promotion gate;
- DirectLink proof remains local development evidence only;
- the interactive login edge is not started until Codex explains the target
  account context, requested scopes or login surface, expected evidence,
  persistence/token handling risk, stop conditions, and rollback/cleanup path;
- Adam gives an explicit in-the-moment "yes, go ahead" before any browser
  window, login prompt, OAuth flow, or tenant consent surface is opened.

Validation:

- focused API tests;
- Windows HTTP probes;
- Linux Freedom CP-1 script where available;
- evidence store inspection with synthetic data only;
- only after the local proof passes, an owner-gated browser/login reachability
  probe may be prepared, explained, and paused for Adam's decision.

Validation evidence:

- `.\.venv\Scripts\python.exe -m pytest tests/test_api_health.py tests/test_api_missions.py tests/test_api_actions.py tests/test_api_connectors.py tests/test_api_agents.py tests/test_api_authority.py tests/test_api_evidence.py tests/test_api_m365_bridge.py tests/test_m365_auth.py tests/test_m365_observe.py tests/test_m365_write.py tests/test_m365_evidence_store.py -q` passed: 118 passed, 3 warnings.
- DirectLink status probe passed at 2026-06-28T09:06:20-06:00: Windows `10.77.77.1`, Linux `10.77.77.2`, SSH, and `L:`/`X:` shared workspace were healthy with no gateway/DNS change.
- Existing `10.77.77.1:8123` server was already running before CMS-B. Windows and Linux health probes returned `status=ok`, `boundary=A1 local no-network`, `phase=1`; protected endpoints were not reused because the runtime key was unknown.
- Temporary CMS-B server on `10.77.77.1:8124` used synthetic env values and ignored `tmp/cms-b-local-store/` evidence output. Windows HTTP probes passed for health, mission creation, allowed local action, blocked `m365_live_content_read`, authority override pending record, connector list, agent list, M365 status, M365 observe dry-run, Planner dry-run, and evidence lookup.
- The Windows probe confirmed `connector_count=8`, connector live-enabled count `0`, `m365-graph-api-bridge.current_state=registry-only`, `agent_count=6`, agent live-enabled count `0`, M365 observe evidence `execution_mode=dry-run` with `R0_OBSERVE`, and Planner evidence `execution_mode=dry-run` with `R2_INTERNAL_WRITE`.
- The first Windows mission probe intentionally hit a guardrail: `requested_tools` values outside the local no-network allowlist were rejected before mission creation.
- Linux Freedom CP-1 script passed 4/4 over DirectLink against the temporary server: health, mission proposal, action validation, and planning-only connector registry.
- `.\.venv\Scripts\python.exe -m pytest -q` passed: 419 passed, 3 warnings, 55 subtests passed.
- The temporary `8124` server was stopped after the proof; the pre-existing `8123` server was left untouched. The temporary evidence store and local `.venv` were removed before closeout.

Normal CMS-B proof stops before cloud placement, broad firewall changes, real
Microsoft Graph calls, tenant admin consent, live Planner writes, Graphify
ingest, or production service behavior.

Optional CMS-B login edge gate: if the normal proof is green, Codex may explain
and prepare an interactive browser-login probe. That probe still stops before
broad scopes, tenant-wide/admin consent approval, live Microsoft Graph content
reads, Outlook or Teams sends, Planner writes, Graphify ingest, production
service behavior, or any retained/printed/committed secret, token, or auth
code. If a consent screen, code, token, or unexpected permission request
appears, pause and ask Adam before continuing.

## CMS-C - Reconcile Pathway, Handoff, And Builder Report

Status: task complete (2026-06-28T09:57:53-06:00)

Completion target: Task complete

Budget class: Small

Inputs: CMS-A/CMS-B validation results, this work packet, START_HERE,
changelog, and the builder/Graphify/Freedom/AG Operations integration summary.

Outputs: updated handoff notes describing the actual post-merge state, a
concise report for the agentic multi-agent agent builder, and a next-decision
recommendation.

Acceptance:

- handoff clearly distinguishes dry-run M365 capability from approved live
  connector activation;
- Graphify remains the binding knowledge layer rather than an execution
  authority;
- Freedom remains the operator interface and current input/output boundary;
- AG Operations Workspace / Microsoft 365 remains the future governed tactile
  environment, not an approved live connector;
- the next owner decision is named before further feature work.

Validation:

- doc review;
- timestamped status entries;
- `git diff --check`;
- any required handoff note review.

Validation evidence:

- Added
  `docs/decisions/2026-06-28 - Current Main Stabilization Builder Report.md`
  as the compact builder-facing report.
- Updated this active packet, `START_HERE.md`, `docs/CHANGELOG.md`,
  `docs/context-map.md`, `docs/source-of-truth-map.md`,
  `docs/current-build-pathway.md`, and the 2026-06-27 builder integration
  summary so future agents route to the compact CMS-C report.
- Confirmed recent GitHub Actions runs are green after CMS-A/CMS-B:
  `28326055021`, `28326108489`, `28326324992`, and `28326642983` passed.
- `git diff --check` passed, with only the existing `START_HERE.md` CRLF
  normalization warning from Git.
- The optional browser-login edge remains paused. No browser login, OAuth
  consent, tenant/admin consent, live Microsoft Graph call, Planner write,
  Graphify ingest, cloud placement, broad firewall change, production service
  behavior, schema publication, or authority expansion was executed.

Stop before renumbering the whole roadmap, approving live M365 content access,
publishing schemas as a stable external package, moving to cloud, or altering
Freedom/Graphify source-of-truth boundaries.

## Recommended Execution Order

CMS-A, CMS-B local proof, and CMS-C are complete. Do not open an interactive
login automatically; explain the edge probe and wait for Adam to say "yes, go
ahead" or "pause." Do not continue feature work if a later CI run turns red;
repair current `main` before login-edge work or any new capability work.

Next owner decision: run a bounded Microsoft 365 re-authenticated test proof
against an owner-approved test surface, send the CMS-C builder report, CTP-2
proof, CNS communication contract, ACA pilot report, M365 permission report,
H4 smoke result, and H5 applied RLS result to the agentic multi-agent agent
builder, resume Chunk Twenty local governed approval actions, or open a formal
Microsoft 365 connector-promotion design gate.

## Documentation Sweep Notes

Sweep timestamp: 2026-06-28T08:33:50-06:00

This packet follows the date-prefixed document-control standard for new
durable records.

Stable-route files intentionally keep stable names, including:

- `AGENTS.md`
- `START_HERE.md`
- `CARRY_FORWARD.md`
- `docs/current-build-pathway.md`
- `docs/context-map.md`
- `docs/source-of-truth-map.md`
- `docs/CHANGELOG.md`

Existing non-date-prefixed decision records remain in place because they
pre-date the 2026-06-25 document-control standard or are already widely
referenced:

- `docs/decisions/app-shell-command-center.md`
- `docs/decisions/freedom-phone-interface-business-partner-boundary.md`

Do not rename those files casually. If Adam wants them date-prefixed later,
perform a bounded rename chunk that updates all references and validates the
links.

New durable reading documents, work packets, handoffs, review packets, and
decision records should continue to use `YYYY-MM-DD - <clear-title>.md` unless
the file is a stable route, dependency file, importable source module, schema,
generated file, CI workflow, runtime config, or tool-owned config.

## Next Handoff

Current-main stabilization is task complete as of 2026-06-28T09:57:53-06:00
and boxed for night as of 2026-06-28T23:00:22-06:00. The compact startup
handoff is
`docs/decisions/2026-06-28 - Nightly Turnover And Token-Friendly Startup.md`.
The compact builder handoff lives at
`docs/decisions/2026-06-28 - Current Main Stabilization Builder Report.md`.
The local CNS connection scout lives at
`docs/decisions/2026-06-28 - Local CNS Connection Proof Report.md`.

Next owner decision: send the updated local CNS/CTP-2 proof, CNS communication
contract, ACA pilot deployment report, M365 permission report, H4 smoke result,
and H5 applied RLS result back to the agentic multi-agent agent builder for
revised orchestration, continue into a bounded Microsoft 365 re-authenticated
test proof, continue into an owner-gated Graphify ingest proof, resume Chunk
Twenty local governed approval actions, or open a formal Microsoft 365
connector-promotion design gate. The delegated permission expansion, H4 smoke
pass, and H5 hosted RLS apply are complete, but no live Microsoft 365 business
action, Graphify CNS store ingest, broad firewall change, production service
behavior, schema publication, R4 live execution, rollback, follow-on Supabase
migration, or source-of-truth migration is approved by this stabilization pass.
