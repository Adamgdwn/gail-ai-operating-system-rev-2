# Current Main Stabilization Work Packet

Document type: work packet
Date: 2026-06-28
Saved: 2026-06-28T08:33:50-06:00
Last Updated: 2026-06-28T08:54:02-06:00
Status: in progress; CMS-A complete (2026-06-28T08:54:02-06:00)
Owner: Adam Goodwin

## Purpose

This packet keeps the current GitHub catch-up work small enough for low-token
startup. It is the active execution packet for current-main stabilization until
CMS-A through CMS-C are complete, superseded, or redirected by Adam.

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

## No-Fallback Boundaries

- Do not resume feature work or old Chunk Twenty implementation while current
  `main` remains red.
- Do not mask the failing tests by deleting the M365 bridge connector or
  weakening planning-only connector boundaries.
- Do not activate live Microsoft 365 reads, Outlook or Teams sends, Planner
  writes, tenant admin consent, Entra changes, or broad Graph scopes.
- Do not treat dry-run M365 endpoints as approved live connector activation.
- Do not treat the CP-1 DirectLink FastAPI proof as production service,
  cloud placement, broad network exposure, or schema publication.
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

## CMS-B - Reprove Runtime And Dry-Run Boundaries

Status: planned (2026-06-28T08:33:50-06:00)

Completion target: Integration complete

Budget class: Small

Inputs: greened current main, ignored local venv, FastAPI app, Freedom CP-1
client, M365 dry-run endpoints, and local evidence store path.

Outputs: a fresh local proof that GAIL OS still serves Freedom over DirectLink
and that the M365 endpoints remain dry-run/no-live-call surfaces.

Acceptance:

- health, missions, actions, connectors, agents, authority override, M365
  status, M365 observe dry-run, M365 Planner dry-run, and evidence retrieval
  behave as documented under local runtime constraints;
- generated evidence remains synthetic/local unless Adam explicitly approves a
  live connector promotion gate;
- DirectLink proof remains local development evidence only.

Validation:

- focused API tests;
- Windows HTTP probes;
- Linux Freedom CP-1 script where available;
- evidence store inspection with synthetic data only.

Stop before cloud placement, broad firewall changes, real Microsoft Graph
calls, tenant admin consent, live Planner writes, Graphify ingest, or
production service behavior.

## CMS-C - Reconcile Pathway, Handoff, And Builder Report

Status: planned (2026-06-28T08:33:50-06:00)

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

Stop before renumbering the whole roadmap, approving live M365 content access,
publishing schemas as a stable external package, moving to cloud, or altering
Freedom/Graphify source-of-truth boundaries.

## Recommended Execution Order

CMS-A is complete. CMS-B is the next stabilization chunk after Adam's go-ahead.
Do not continue feature work if a later CI run turns red; repair current `main`
before CMS-B or any new capability work.

CMS-B and CMS-C can be grouped into one execution chunk if CMS-A is small and
clean. Keep them separate if validation exposes runtime, DirectLink, or M365
dry-run drift.

After CMS-C, ask Adam whether to send the builder report, resume Graphify
acceleration Phase D/E design, continue CP-1 contract generation for
TypeScript consumers, or begin a formal M365 connector promotion design gate.

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

Next action after CMS-A: wait for Adam's go-ahead, then execute CMS-B to
reprove runtime and dry-run boundaries while preserving the no-live-access
boundary.
