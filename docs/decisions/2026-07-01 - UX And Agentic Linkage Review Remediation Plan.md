# UX And Agentic Linkage Review Remediation Plan

Document type: review packet and remediation plan
Date: 2026-07-01
Saved: 2026-07-01T09:32:16-06:00
Last Updated: 2026-07-01T11:41:25-06:00
Status: active remediation plan; EX-2 integration complete; EX-3 awaiting owner approval
Owner: Adam Goodwin
Prepared by: Codex

## Purpose

This document records a user-experience, quality-control, and agentic-linkage
review of GAIL AI Operating System Rev 2. It is intended to be the durable
report that future remediation work can build directly under.

The review looks at the repo from two perspectives:

- a user or operator jumping in and trying to understand, run, and use the
  system;
- the agentic linkage across Freedom, GAIL OS, Graphify, and future tactile
  tools such as Microsoft 365, local devices, and other governed connectors.

## Owner Direction Incorporated

Adam clarified the following direction on 2026-07-01:

- Keep this report and the remediation plan together in a separate durable
  document.
- Microsoft 365 and tactile-tool capability should support both delegated
  user/operator flows and app-only/service identities, as separate governed
  connector profiles.
- The target experience is fully agentic through any appropriate surface:
  laptop, tablet, phone, Freedom, command-center views, and future operator
  surfaces. The user should be able to ask Freedom to execute commands, pull
  information, build, refine, and operate integrated tools in controlled,
  governed ways.

This direction does not approve live Microsoft 365 business actions, Graphify
production ingest, R4 live execution, production readiness, or source-of-truth
migration. Those remain owner-gated promotion steps.

Phone access should follow the existing product boundary unless Adam reverses
it: use Freedom, responsive hosted surfaces, governed bridge contracts,
summaries, links, and fallback views rather than creating a competing native
Rev 2 phone app.

## Review Basis

The review used the current repo state, the active startup and stabilization
records, the command-center app, the FastAPI surface, the core UAOS package,
Graphify contract and handoff files, Microsoft 365 dry-run/auth code, and the
repo-local Graphify output available under `graphify-out/graph.json`.

Validation observed during the review:

- `npm --prefix apps/command-center run build` passed.
- `npm --prefix apps/command-center audit --audit-level=moderate` passed with
  zero reported vulnerabilities.
- `bash scripts/governance-preflight.sh` passed with zero warnings.
- `uv run --with-requirements requirements.txt python -m pytest -q` passed with
  563 tests, 55 subtests, and 4 warnings.
- `uv run --with-requirements requirements.txt python scripts/export-cp1-contracts.py --verbose`
  passed with 9 valid CP-1 schemas.
- Plain `python -m pytest -q`, plain schema export, and plain
  `python -m unittest discover -s tests` were not reliable first-run commands
  in the observed environment because dependencies were not installed in the
  base Python environment and unittest only exercised a partial suite.

## Executive Assessment

GAIL OS Rev 2 has a stronger governed spine than its onboarding experience
currently reveals. The core concepts are real in code: authority envelopes,
mission classification, connector registry records, action validation,
evidence packets, Graphify fact export, local proof runners, M365 dry-run
observe/write endpoints, and an operator cockpit. The strongest current trait
is that the repo already behaves like a control plane rather than a loose pile
of demos.

The biggest improvement need is productization of that spine into a trustworthy
operator system. A new user or future agent can see the intent, but the first
run path, live state visibility, API/UI persistence, auth-profile story,
Graphify replay path, and R4 naming boundaries need to become sharper before
the system should claim fully functional agentic operation.

## Findings Table

| Area | Strength | Area For Improvement | User Or Agentic Impact | Priority |
|---|---|---|---|---|
| First-run onboarding | `START_HERE.md`, the stabilization packet, and context routing make the current boundaries unusually explicit. | Quick Start guidance still points toward partial or stale commands. The observed reliable path is `uv run --with-requirements requirements.txt python -m pytest -q`, while plain Python commands fail without dependencies and unittest covers less than the full suite. | A new user or agent can waste time or trust the wrong validation result. This is the first user-experience gap to fix. | P0 |
| Command center | The React cockpit is coherent, responsive, and aligned with the governed-spoke model. Build and audit pass. | It is mostly static sample state. It needs live read-only API wiring, loading/empty/error/unauthorized states, and an operator path from signal to mission to action to evidence. | The visual experience is promising, but the user cannot yet rely on it as a real operating surface. | P0 |
| Governed core spine | Mission, action, approval, authority, connector, relay, evidence, M365 dry-run, Graphify handoff, and local proof code exist and are covered by a substantial test suite. | Some core concepts are not yet surfaced consistently through API/UI. Mission creation and authority override responses are not generally persisted, and approval actions exist in core before they are an operator-facing workflow. | Agents can validate proposals, but the operator story is not yet a complete loop. | P0 |
| Freedom linkage | FastAPI routes already provide the shape Freedom needs: health, missions, actions, authority, evidence, connectors, agents, and M365 dry-run probes. Local and Azure proof records exist. | The next layer needs a consistent `cns_trace_id`, `FreedomRelationshipBrief`, idempotency key, event ledger, and read model that lets Freedom reason across user intent, GAIL authority, Graphify context, and tactile-tool evidence. | Freedom can reach GAIL OS, but it needs a richer memory and trace contract to become the primary agentic business partner surface. | P1 |
| Graphify linkage | Sanitized fact export, fingerprints, preview/diff posture, and no-authority doctrine are strong. Graphify is treated as intelligence and context, not execution authority. | Persistent ingest remains owner-gated and not yet a normal replay path. The system needs a local replay/event-ledger proof and a synthetic fact-bundle proof before promotion. | Graphify can accelerate context, but the operator needs confidence that knowledge updates are traceable, reversible, and not authority-bearing. | P1 |
| Tactile tools and Microsoft 365 | Dry-run observe/write endpoints are guarded and evidence-producing. Delegated tenant permissions were approved separately, with no secret or certificate created. | Code currently includes client-credential expectations while the latest M365 approval is delegated-only. The target should explicitly support two connector profiles: delegated operator auth and app-only service auth, each with separate scopes, authority envelopes, and proof gates. | This is the most important integration mismatch before live tactile-tool work. Without reconciliation, agents may assume the wrong identity and authority model. | P0 |
| R4 execution semantics | R0-R5 doctrine is clear and the R4 simulator/test surface gives the repo a concrete autonomy vocabulary. | PH-2 corrected the old live-labeled proof wrapper by replacing it with `r4_synthetic_execution_record.py`, but full R4 AuthorityEnvelope execution remains future work. | For a fully agentic system, naming and feature gates must make real execution authority unambiguous. | P0 |
| Evidence and persistence | EvidencePacket and local evidence storage exist, and M365 dry-run writes produce retrievable evidence. | Persistence is not uniform across missions, approvals, overrides, Graphify handoff previews, and action lifecycle events. `local_store/` should be explicitly ignored or redirected if it is local runtime state. | Users need a dependable audit trail from request to result, especially when using phone/tablet/Freedom surfaces asynchronously. | P1 |
| Quality controls | Full pytest, schema export, frontend build, npm audit, and governance preflight are green when run with the right tooling. | Python dependencies are unpinned, there is no durable Python lock/pyproject path, governance-check does not yet enforce all controls named in `project-control.yaml`, and deprecation warnings remain. | The repo is testable, but repeatability needs to improve before release-ready claims. | P1 |
| Operations and release docs | Authority boundaries and current stabilization status are well documented. | Risk register, deployment guide, and runbook still contain placeholder sections. | A future operator or support agent lacks enough recovery, rollback, and escalation guidance. | P2 |

## Remediation Improvement Plan

### Track A - Truthful Onboarding And First Run

Goal: make the first successful local run obvious and make partial validation
paths visibly partial.

Recommended work:

- Update `README.md` and `AI_BOOTSTRAP.md` so the primary validation path uses
  the known-good uv command.
- Label `python -m unittest discover -s tests` as partial, legacy, or remove it
  from the main path.
- Add a short "known local prerequisites" section covering uv, Node/npm, and
  the current Python dependency path.
- Decide whether to create `pyproject.toml` plus lockfile, or keep
  `requirements.txt` as the short-term path while pinning versions.
- Add `local_store/` to `.gitignore` if local runtime evidence should not be
  committed.

Acceptance:

- A new local agent can run one documented command and get the full Python
  validation result.
- The documented command count is small enough to be followed from a fresh
  clone.
- No doc suggests that a partial unittest run is the full quality gate.

### Track B - Command Center As A Real Operator Surface

Goal: make the command center a live, read-only operator view before adding
write controls.

Recommended work:

- Replace stale sample-only cockpit state with API-backed read models for
  health, connector registry, authority levels, agents, M365 dry-run status,
  and recent evidence.
- Add explicit loading, empty, API-key missing, unauthorized, offline, and
  stale-data states.
- Preserve the cockpit's role as a coordination surface that augments Freedom
  rather than competing with it.
- Add tests or screenshots for desktop, tablet, and phone-sized layouts.

Acceptance:

- The user can open the command center and tell whether GAIL OS is reachable,
  what authority posture is active, which connectors are live/planning-only,
  and whether evidence is fresh.
- No write or live connector action is exposed before the matching authority
  contract and evidence path exists.

### Track C - Governed Action Loop

Goal: close the loop from signal to mission to action to approval to evidence.

Recommended work:

- Surface approval actions through API endpoints that remain local, governed,
  auditable, stale-state protected, and non-executing until connector promotion
  is approved.
- Persist mission records, authority override requests, approval decisions,
  and action lifecycle transitions in one local event ledger or clearly related
  stores.
- Add idempotency keys for proposed actions and tactile-tool requests.
- Make evidence retrieval usable from Freedom and command-center views.

Acceptance:

- An operator can inspect the full lifecycle of a proposed action without
  reading raw local files.
- Replayed or duplicate requests are detectable and do not produce ambiguous
  state.
- Every approved local action has a corresponding evidence path.

### Track D - Freedom Relationship And Trace Contract

Goal: make Freedom the primary conversational operator surface while GAIL OS
remains the authority spine.

Recommended work:

- Introduce `cns_trace_id` across signal, mission, action, authority, evidence,
  Graphify fact bundle, and tactile-tool request/response records.
- Implement a `FreedomRelationshipBrief` read model that gives Freedom the
  current operator context, mission status, authority posture, connector
  state, and relevant Graphify facts without granting execution authority.
- Define retry and failure semantics so Freedom can explain what happened from
  phone, tablet, laptop, or desktop surfaces.
- Keep Freedom as the high-level business partner and request surface; keep
  GAIL OS as the policy/evidence layer.

Acceptance:

- A user can ask Freedom what happened to a request and receive a traceable
  answer grounded in GAIL OS evidence and Graphify context.
- The same trace can be inspected from command center without divergent state.

### Track E - Graphify Governed Intelligence Path

Goal: promote Graphify from preview contracts to a controlled knowledge update
path without making it an authority source.

Recommended work:

- Build a local replay proof that emits synthetic `GraphifyFactBundle` records
  from GAIL OS event/evidence state.
- Add a preview-to-acceptance flow with deterministic diff, cache, and rollback
  notes.
- Keep production/persistent Graphify ingest owner-gated until the local proof,
  schema, and evidence boundaries are accepted.
- Ensure Graphify facts reference authority/evidence IDs but cannot approve or
  execute actions.

Acceptance:

- The user can preview exactly what Graphify would learn from a governed
  action before any persistent ingest occurs.
- Graphify updates can be traced back to GAIL OS evidence.

### Track F - Tactile Tools And Microsoft 365 Connector Promotion

Goal: support real tactile-tool capability through separate, explicit identity
and authority profiles.

Recommended work:

- Define two Microsoft 365 connector profiles:
  - Delegated operator profile: uses user/operator delegated auth and is suited
    to owner-present or owner-approved action paths.
  - App-only service profile: uses a named service identity only after separate
    credential, scope, and authority-envelope approval.
- Reconcile `m365_auth.py`, reader, writer, docs, tests, and connector registry
  records with the two-profile model.
- Promote in stages: dry-run, read-only proof against owner-approved test
  surfaces, bounded write proof against safe test targets, then narrowly
  chartered live action.
- For every stage, define stop conditions, rollback path, token handling,
  evidence packet shape, and user-facing explanation.

Acceptance:

- No code path or doc implies app-only credentials exist when the approved
  tenant state is delegated-only.
- The user can see which identity will touch Microsoft 365 before any live
  read, write, send, or configuration action.
- Freedom and command center can explain whether a tactile-tool request is
  blocked, dry-run, read-only, pending approval, or executed.

### Track G - R4 And Live Execution Boundary

Goal: make fully agentic action possible without ambiguous live authority.

Recommended work:

- Rename, quarantine, or feature-gate the current R4 live executor so synthetic
  proof code cannot be mistaken for a live external-system adapter.
- Separate "simulated live lifecycle" evidence from actual tactile-tool live
  execution evidence.
- Require signed AuthorityEnvelope fields for R4: charter, actor, tools,
  scope, stop conditions, rollback path, review cadence, and expiry.
- Add a positive allowlist of executable adapters and a default-deny policy for
  all external effects.

Acceptance:

- Future agents cannot execute, import, or advertise R4 live behavior without
  an explicit owner-approved feature gate and authority envelope.
- The difference between simulation, dry-run, read-only, bounded write, and
  live execution is visible to users.

### Track H - Quality, Governance, And Release Readiness

Goal: make the repo's controls match the claims made in project-control docs.

Recommended work:

- Pin or lock Python dependencies.
- Make CI and local docs agree on the full test command.
- Expand governance check coverage or reduce `project-control.yaml` claims so
  they match actual enforcement.
- Add lint and secret-scan checks if they are intended release gates.
- Resolve or consciously accept FastAPI/Starlette deprecation warnings.
- Replace placeholder risk, deployment, and runbook content before any
  release-ready claim.

Acceptance:

- A future agent can tell which checks are advisory and which are enforced.
- Release readiness does not rely on placeholder operational documents.

## Experience-First Execution Packet

This section merges the 2026-07-01 experience-first execution packet into this
remediation plan. Keep it here until the file becomes too large to use as a
restart document; split only when doing so improves handoff clarity.

### Operating Cadence

Use plan, do, check, act.

- Plan: each chunk must have scope, acceptance, validation, stop-before lines,
  and a rollback path before implementation starts.
- Do: implement one approved chunk at a time.
- Check: run every validation command named in the chunk.
- Act: record the result in this file, update the chunk status, note any
  follow-on work, then stop for owner review before the next chunk unless Adam
  explicitly approves continuing.

No feature implementation starts from this packet until Adam approves the
specific chunk. Planning updates to this document are allowed when they improve
chunk clarity.

### Token-Friendly Continuity Model

For now, this document is the single execution status, handoff, and restart
record. Fresh sessions should read:

1. `AGENTS.md`;
2. this document's metadata, Operating Cadence, Execution Status, Shared
   Context, and the one assigned chunk;
3. the chunk's most recent handoff note in this document, if any;
4. only the files named in the chunk's context manifest.

Do not create a separate root-level `EXECUTION-STATUS.md` or handoff directory
yet. If this document becomes too large, split handoffs into dated companion
records under `docs/decisions/` and leave short links here.

### Shared Context

Iteration goal: make the system feel alive and usable for owner dogfooding in
read-only mode. Golden path v1 is: open Freedom or the command center, see true
live state, ask Freedom "what happened to X," and get a traceable answer
grounded in GAIL OS evidence and Graphify context. The same trace should be
visible from the cockpit.

Architecture invariant: one shared read/trace layer. Freedom and the command
center are thin views over it and must not show divergent state. Every newly
persisted lifecycle record should carry a `cns_trace_id`.

Hard boundary for this iteration:

- no live Microsoft 365 reads, writes, sends, or configuration changes;
- no app-only Microsoft 365 credentials, client secrets, or certificates;
- no OAuth, browser login, or consent surfaces;
- no Graphify production or persistent ingest;
- no R4 live execution;
- no new external-effect write/action endpoints;
- no cloud placement, production promotion, runtime consolidation, or
  source-of-truth migration.

Known-good validation commands:

```bash
uv run --with-requirements requirements.txt python -m pytest -q
uv run --with-requirements requirements.txt python scripts/export-cp1-contracts.py --verbose
npm --prefix apps/command-center run build
npm --prefix apps/command-center audit --audit-level=moderate
bash scripts/governance-preflight.sh
git diff --check
```

Plain `python -m pytest`, plain schema export, and
`python -m unittest discover -s tests` are not reliable full gates in the
observed owner environment.

### Execution Status

| Chunk | State | Depends On | Completion Target | Last Updated | Handoff |
|---|---|---|---|---|---|
| RMP-0 | owner approved; draft complete | none | Draft complete | 2026-07-01T10:43:19-06:00 | RMP-0 Handoff |
| PH-1 | task complete | RMP-0 owner approval | Task complete | 2026-07-01T10:44:03-06:00 | PH-1 Handoff |
| PH-2 | task complete | RMP-0 owner approval | Task complete | 2026-07-01T10:57:46-06:00 | PH-2 Handoff |
| EX-1 | integration complete | RMP-0 owner approval | Integration complete | 2026-07-01T11:23:53-06:00 | EX-1 Handoff |
| EX-2 | integration complete | EX-1 | Integration complete | 2026-07-01T11:41:25-06:00 | EX-2 Handoff |
| EX-3 | planned | EX-1 | Draft complete | 2026-07-01T10:11:09-06:00 | pending |

### Dependency Map

```text
RMP-0  Plan adoption and chunk detail
  ├─ PH-1  Truthful first run and runtime hygiene
  ├─ PH-2  Truth-in-naming, cheap safety clarity
  └─ EX-1  Shared read model and trace spine
        ├─ EX-2  Command center live read-only
        └─ EX-3  Freedom relationship brief
```

PH-1 and PH-2 may run before EX-1. EX-2 and EX-3 must wait for EX-1's
handoff. No chunk may begin until Adam approves it after reviewing this
execution packet.

### RMP-0 - Adopt Experience-First Execution Plan

Intent: merge the uploaded execution packet into this remediation plan and
create an owner-reviewable chunk sequence before feature work starts.

Depends on: none

Size: Small

Preconditions:

- Working tree is clean before the planning edit.
- Uploaded execution packet is available for review.
- No feature implementation begins during this chunk.

Context manifest:

- Known files:
  - `AGENTS.md`
  - `docs/decisions/2026-07-01 - UX And Agentic Linkage Review Remediation Plan.md`
  - `C:\Users\adamg\Downloads\2026-07-01_-_Experience_First_Agent_Execution_Packet.md`
- Discovery scope: only planning/status/handoff conventions already present in
  this repo.
- Do not read: application code, frontend internals, M365 auth internals, or
  Graphify internals.

Scope:

- Merge the packet's PDCA cadence into this plan.
- Keep status and handoffs in this document for now.
- Detail PH-1, PH-2, EX-1, EX-2, and EX-3 enough for owner approval.
- Preserve all non-approval boundaries.

Out of scope / stop before:

- No README, bootstrap, code, test, API, frontend, auth, Graphify, M365, R4, or
  runtime behavior changes.
- No separate status file unless Adam asks for it.

Deliverables:

- Updated remediation plan with detailed chunks and execution status.

Acceptance:

- Adam can review the chunk plan and decide whether to approve PH-1, request
  revisions, or choose a different first implementation chunk.
- The plan is token-friendly for restarts.
- No implementation work is started.

Validation:

```bash
bash scripts/governance-preflight.sh
git diff --check
```

Handoff:

- Record the final status of RMP-0 in this document after owner review or
  commit.

Rollback:

- Revert the planning-doc commit.

### PH-1 - Truthful First Run And Runtime Hygiene

Intent: stop the owner or any future agent from trusting the wrong validation
result.

Depends on: RMP-0 owner approval

Size: Small

Preconditions:

- Adam approves PH-1 after reviewing this plan.
- Working tree is clean.

Context manifest:

- Known files:
  - `README.md`
  - `AI_BOOTSTRAP.md`
  - `START_HERE.md`
  - `requirements.txt`
  - `.gitignore`
  - this remediation plan
- Discovery scope:
  - find active doc references to `python -m unittest discover`;
  - confirm whether `local_store/` is currently ignored;
  - inspect only documentation and ignore rules needed for first-run guidance.
- Do not read: application code, M365 internals, Graphify internals, command
  center implementation files, or old archived pathway sections except when a
  direct search result must be classified as historical.

Scope:

- Update first-run guidance so the primary full Python validation command is:

  ```bash
  uv run --with-requirements requirements.txt python -m pytest -q
  ```

- Update CP-1 schema validation guidance to use:

  ```bash
  uv run --with-requirements requirements.txt python scripts/export-cp1-contracts.py --verbose
  ```

- Mark `python -m unittest discover -s tests` as historical, partial, or
  legacy wherever it appears in active first-run guidance.
- Add a short prerequisites note covering uv, Node/npm, and current Python
  dependency handling.
- Add `local_store/` to `.gitignore` if local runtime evidence and OKP stores
  are intended to remain untracked.
- Optionally add one sentence saying command center live data is planned in
  EX-2 if a first-run doc currently implies it is already live.
- Update this document's PH-1 handoff/status section after validation.

Out of scope / stop before:

- No M365 auth behavior changes.
- No OAuth, browser login, or tenant consent surfaces.
- No Graphify ingest.
- No R4 naming or execution changes.
- No new API endpoints.
- No frontend behavior changes.
- No dependency pinning or lockfile work; note it for Track H instead.

Deliverables:

- Updated first-run docs.
- Updated `.gitignore` if `local_store/` is runtime-only.
- PH-1 handoff note in this document.

Acceptance:

- A fresh local agent can find one documented full Python validation path.
- Active docs no longer imply unittest discovery is the full quality gate.
- Runtime local store output will not be accidentally committed if it is meant
  to remain local state.

Validation:

```bash
uv run --with-requirements requirements.txt python -m pytest -q
uv run --with-requirements requirements.txt python scripts/export-cp1-contracts.py --verbose
git diff --check
```

Rollback:

- Revert the PH-1 commit.

### PH-2 - Truth-In-Naming And Identity Boundary

Intent: remove false signals around R4 "live" naming and app-only M365
identity without changing runtime behavior.

Depends on: RMP-0 owner approval

Size: Small to Medium

Preconditions:

- Adam approves PH-2 after reviewing this plan.
- Working tree is clean.
- Full Python suite passes before edits.

Context manifest:

- Known files:
  - `AGENTS.md`
  - `packages/uaos-core/src/gail_ai_operating_system/r4_synthetic_execution_record.py`
  - `packages/uaos-core/src/gail_ai_operating_system/__init__.py`
  - `tests/test_r4_synthetic_execution_record.py`
  - `packages/uaos-core/src/gail_ai_operating_system/m365_auth.py`
  - `packages/uaos-core/src/gail_ai_operating_system/m365_reader.py`
  - `packages/uaos-core/src/gail_ai_operating_system/m365_writer.py`
  - `packages/uaos-core/src/gail_ai_operating_system/connector_registry.py`
  - `tests/test_m365_auth.py`
  - `tests/test_m365_observe.py`
  - `tests/test_m365_write.py`
  - `docs/decisions/2026-06-28 - M365 Entra Permission Expansion Report.md`
- Discovery scope:
  - find imports/exports and tests for the old R4 live-labeled proof wrapper;
  - find code/docs implying app-only M365 credentials, client secrets, or
    runtime service-identity availability.
- Do not read: command center internals, EX read-model code, Graphify internals,
  or unrelated M365 tenant/provider docs.

Scope:

- Replace the old R4 live-labeled proof wrapper so synthetic proof code cannot
  be mistaken for a real external-system adapter.
- Preserve tests by updating names/imports/expected language only as needed.
- Reconcile M365 identity language so current approved tenant state is clear:
  delegated permission expansion exists; app-only secret/certificate does not.
- Keep existing dry-run behavior unchanged.
- Update this document's PH-2 handoff/status section after validation.

Out of scope / stop before:

- Do not create credentials, secrets, certificates, OAuth flows, or consent
  surfaces.
- Do not implement dual-profile M365 promotion.
- Do not change live/dry-run behavior.
- Do not add R4 authority-envelope functionality.
- Do not add executable adapters or external effects.

Deliverables:

- R4 naming/export posture that does not advertise live external execution.
- M365 code/docs/tests/registry language aligned with delegated-only current
  approval.
- PH-2 handoff note in this document.

Acceptance:

- No active code or doc path implies R4 live external-system execution is
  approved or available.
- No active code or doc path implies app-only M365 credentials currently exist.
- Full Python behavior remains green.

Validation:

```bash
uv run --with-requirements requirements.txt python -m pytest -q
bash scripts/governance-preflight.sh
git diff --check
```

Rollback:

- Revert the PH-2 commit.

### EX-1 - Shared Read Model And Trace Spine

Intent: give GAIL OS one persisted read/trace layer that the API serves
read-only, so Freedom and the command center can render the same live state.

Depends on: RMP-0 owner approval

Size: Large

Preconditions:

- Adam approves EX-1 after reviewing this plan.
- Working tree is clean.
- Governance preflight passes.
- Full Python suite passes before edits.

Context manifest:

- Known files:
  - `apps/gail-os-api/main.py`
  - `apps/gail-os-api/deps.py`
  - `apps/gail-os-api/routers/`
  - `packages/uaos-core/src/gail_ai_operating_system/mission_spine.py`
  - `packages/uaos-core/src/gail_ai_operating_system/action.py`
  - `packages/uaos-core/src/gail_ai_operating_system/approval_actions.py`
  - `packages/uaos-core/src/gail_ai_operating_system/authority_envelope.py`
  - `packages/uaos-core/src/gail_ai_operating_system/evidence_packet.py`
  - `packages/uaos-core/src/gail_ai_operating_system/evidence_store.py`
  - `packages/uaos-core/src/gail_ai_operating_system/connector_registry.py`
  - `packages/uaos-core/src/gail_ai_operating_system/agent_registry.py`
  - `packages/uaos-core/src/gail_ai_operating_system/graphify_acceleration.py`
  - relevant API tests under `tests/`
- Discovery scope:
  - locate existing mission/action/authority/evidence persistence paths;
  - locate current route tests for health, missions, actions, authority,
    evidence, connectors, agents, and M365 dry-run status;
  - locate existing `cns_trace_id` references in docs/contracts/code.
- Do not read: command center frontend internals, M365 auth internals beyond
  dry-run status shape, Freedom repo implementation, Graphify internals beyond
  local fact-bundle/reference contracts.

Scope:

- Add or standardize `cns_trace_id` on newly persisted signal, mission, action,
  authority, approval, evidence, Graphify fact-bundle candidate, and tactile
  request/response records where those records already exist in this repo.
- Persist mission records, authority override requests, approval decisions, and
  action lifecycle transitions to one local event ledger or clearly related
  local stores.
- Expose a read-only API read model covering:
  - health and boundary;
  - authority posture;
  - connector registry live/planning-only posture;
  - agent registry posture;
  - M365 dry-run status;
  - recent evidence/events;
  - trace lookup by `cns_trace_id`, if feasible inside this chunk.
- Add focused tests for persistence, trace IDs, and read-model response shapes.
- Update this document's EX-1 handoff/status section after validation.

Out of scope / stop before:

- No new external-effect write/action endpoints.
- No live M365 read/write/send/config.
- No OAuth or browser login.
- No Graphify persistent ingest.
- No R4 live execution.
- No frontend changes.
- No cloud placement or production-readiness claims.

Deliverables:

- Trace-aware local event/read store.
- Read-only API endpoint or endpoints for shared live state.
- Focused API/core tests.
- EX-1 handoff note in this document with endpoint paths and response shapes.

Acceptance:

- API returns live read-model data, not sample data, for the agreed state list.
- Every newly persisted lifecycle record carries a `cns_trace_id`.
- Duplicate or replayed requests are at least detectable, or explicitly noted
  as the next follow-up if full idempotency is too large for this chunk.
- Full Python suite and CP-1 schema export remain green.
- No external-effect endpoint or live connector path is added.

Validation:

```bash
uv run --with-requirements requirements.txt python -m pytest -q
uv run --with-requirements requirements.txt python scripts/export-cp1-contracts.py --verbose
bash scripts/governance-preflight.sh
git diff --check
```

Rollback:

- Revert the EX-1 commit.
- If a new local store file shape is introduced, delete only generated local
  runtime data under ignored local-store paths after confirming it is untracked.

### EX-2 - Command Center Live Read-Only

Intent: make the cockpit a real read-only operator surface over the EX-1 shared
read model.

Depends on: EX-1

Size: Medium

Preconditions:

- EX-1 handoff in this document is marked PASS.
- Adam approves EX-2 after reviewing the EX-1 handoff.
- Working tree is clean.
- Command center build passes before edits.

Context manifest:

- Known files:
  - EX-1 handoff section in this document;
  - `apps/command-center/src/App.tsx`
  - `apps/command-center/src/cockpitData.ts`
  - `apps/command-center/src/appShellDecision.ts`
  - `apps/command-center/src/styles.css`
  - `apps/command-center/package.json`
- Discovery scope:
  - locate sample-state source and any existing API/client/env handling inside
    `apps/command-center`;
  - inspect only frontend files needed to consume EX-1 read-model fields.
- Do not read: Python internals beyond the EX-1 read-model contract; M365 auth
  internals; Graphify internals; Freedom repo implementation.

Scope:

- Replace or clearly subordinate sample cockpit state with EX-1 live read-model
  data.
- Add explicit UI states:
  - loading;
  - empty;
  - API key missing or config missing;
  - unauthorized;
  - offline/unreachable;
  - stale data.
- Preserve the cockpit's role as a read-only operator view that augments
  Freedom.
- Add or update lightweight frontend tests if the repo already has a frontend
  test harness; otherwise use build plus documented screenshot/manual viewport
  evidence.
- Verify desktop, tablet, and phone-sized layouts.
- Update this document's EX-2 handoff/status section after validation.

Out of scope / stop before:

- No write controls.
- No live connector actions.
- No Python read-model shape changes. If the EX-1 contract is insufficient,
  stop and record an EX-1 follow-up.
- No new native phone app.

Deliverables:

- Command center wired to live read-model data.
- Six explicit state treatments.
- Layout evidence for desktop/tablet/phone.
- EX-2 handoff note in this document.

Acceptance:

- The owner can open the cockpit and tell whether GAIL OS is reachable.
- The cockpit shows authority posture, connector posture, agent posture, M365
  dry-run posture, and evidence/event freshness from live API data.
- No write or live connector action is exposed.
- Text and controls fit at desktop, tablet, and phone widths.

Validation:

```bash
npm --prefix apps/command-center run build
npm --prefix apps/command-center audit --audit-level=moderate
bash scripts/governance-preflight.sh
git diff --check
```

Rollback:

- Revert the EX-2 commit.

### EX-3 - Freedom Relationship Brief

Intent: let Freedom answer "what is the posture?" and "what happened to X?"
from the same read/trace layer, with no execution authority.

Depends on: EX-1

Size: Medium

Preconditions:

- EX-1 handoff in this document is marked PASS.
- Adam approves EX-3 after reviewing the EX-1 handoff.
- Working tree is clean.
- Full Python suite passes before edits.

Context manifest:

- Known files:
  - EX-1 handoff section in this document;
  - `apps/gail-os-api/routers/`
  - `docs/decisions/2026-06-28 - CNS Communication Enhancement Contract.md`
  - `docs/contracts/2026-06-28 - Graphify Fact Export Contract.md`
  - `packages/uaos-core/src/gail_ai_operating_system/graphify_acceleration.py`
  - shared read-model files introduced by EX-1
- Discovery scope:
  - locate Freedom-facing route or client-contract conventions in this repo;
  - locate current `FreedomRelationshipBrief` mentions in docs/contracts;
  - locate Graphify fact reference fields available without Graphify ingest.
- Do not read: command center frontend internals beyond EX-1 trace contract;
  Freedom repo implementation; live Graphify services; M365 auth internals.

Scope:

- Implement or document a `FreedomRelationshipBrief` read model over EX-1.
- Include current operator context, mission status, authority posture,
  connector state, recent evidence/event state, and relevant Graphify fact
  references where available.
- Define retry/failure semantics so Freedom can explain stale, degraded,
  unavailable, unauthorized, and not-found states.
- Ensure the same `cns_trace_id` resolves to the same underlying GAIL OS trace
  records that command center uses.
- Update this document's EX-3 handoff/status section after validation.

Out of scope / stop before:

- No execution authority for Freedom.
- No live M365.
- No Graphify persistent ingest.
- No R4 live.
- No write/action endpoints.
- No Freedom repo implementation unless Adam explicitly routes the session
  there later.

Deliverables:

- `FreedomRelationshipBrief` endpoint, schema, or contract record in this repo.
- Retry/failure semantics.
- Focused tests or contract validation.
- EX-3 handoff note in this document.

Acceptance:

- Freedom can ask GAIL OS for a traceable relationship/posture brief without
  receiving execution authority.
- The same `cns_trace_id` maps to the same source records visible to command
  center.
- Degraded or missing data is explicit rather than silently omitted.

Validation:

```bash
uv run --with-requirements requirements.txt python -m pytest -q
bash scripts/governance-preflight.sh
git diff --check
```

Rollback:

- Revert the EX-3 commit.

### Deferred Owner-Gated Work

Do not start these without a separate owner greenlight:

- one governed local write action after EX-1 through EX-3;
- Graphify synthetic fact-bundle replay, then persistent ingest;
- Microsoft 365 dual-profile promotion and any live read/write/send/config
  proof;
- full R4 authority-envelope, stop conditions, and adapter allowlist;
- dependency pinning, placeholder ops-doc replacement, lint, and secret-scan
  gates before any release-ready claim.

### Handoff Log

Use this section for short handoff notes until this document becomes too large.
Each completed chunk should add:

- result;
- files changed;
- exact endpoint/schema/UI shape introduced;
- validation commands and pass/fail result;
- open risks or next-chunk notes.

#### RMP-0 Handoff

Status: owner approved; draft complete.

What changed:

- Merged the experience-first execution packet into this remediation plan.
- Added the PDCA operating cadence.
- Chose this document as the token-friendly status and handoff record for now.
- Added detailed chunk definitions for PH-1, PH-2, EX-1, EX-2, and EX-3.
- Preserved the hard non-approval boundary against live M365, OAuth/login,
  Graphify persistent ingest, R4 live execution, cloud changes, and source of
  truth migration.

Validation:

- `git diff --check` passed.
- `bash scripts/governance-preflight.sh` passed with 0 warnings.

Owner decision:

- Adam approved RMP-0 and PH-1 on 2026-07-01.

#### PH-1 Handoff

Status: task complete.

Completed: 2026-07-01T10:43:19-06:00

What changed:

- Updated `README.md` Quick Start to use the observed reliable full Python
  validation command and CP-1 schema export command:
  `uv run --with-requirements requirements.txt python -m pytest -q` and
  `uv run --with-requirements requirements.txt python scripts/export-cp1-contracts.py --verbose`.
- Added a short first-run prerequisite note for `uv`, Node/npm, and current
  requirements-based Python dependency handling.
- Marked `python -m unittest discover -s tests` as a historical partial check
  rather than the full Python validation gate.
- Clarified that command-center live read-only data is planned for EX-2 and is
  not present in the first-run static app shell.
- Updated `AI_BOOTSTRAP.md` commands so future agents see the same full Python
  and CP-1 validation path.
- Added `local_store/` to `.gitignore` after confirming it is default local
  runtime persistence for evidence and OKP stores.

Endpoint/schema/UI shape introduced:

- None. PH-1 changed only onboarding, bootstrap guidance, and ignore rules.

Validation:

- `uv run --with-requirements requirements.txt python -m pytest -q` passed:
  563 tests, 55 subtests, 4 existing Starlette deprecation warnings.
- `uv run --with-requirements requirements.txt python scripts/export-cp1-contracts.py --verbose`
  passed: all 9 CP-1 schemas valid.
- `git diff --check` passed.
- `bash scripts/governance-preflight.sh` passed with 0 warnings.

Open risks / next-chunk notes:

- Python dependencies are still requirements-based and not pinned by a durable
  lockfile; this remains Track H work, not PH-1 scope.
- The existing Starlette deprecation warnings remain open Track H cleanup.
- Next approved implementation chunk remains owner-gated.

#### PH-2 Handoff

Status: task complete (2026-07-01T10:57:46-06:00).

Completed:

- Replaced the exported R4 live-labeled module with
  `packages/uaos-core/src/gail_ai_operating_system/r4_synthetic_execution_record.py`.
- Removed the old top-level R4 live-named result/function exports; exported
  `R4SyntheticExecutionRecord` and
  `run_r4_synthetic_execution_record` instead.
- Updated R4 focused tests to assert dry-run evidence, synthetic OKP record
  language, and `no_live_mutations=True`.
- Reconciled M365 auth, reader, writer, status API, connector registry, and
  focused tests so the current state is delegated-only and app-only credentials
  are explicitly future-only/unprovisioned.
- Updated `AGENTS.md`, `START_HERE.md`, and `docs/CHANGELOG.md` so active
  startup and history do not advertise a live executor or current app-only
  credential.

Validation:

- Baseline before edits:
  `uv run --with-requirements requirements.txt python -m pytest -q` passed:
  563 passed, 4 warnings, 55 subtests.
- Focused after edits:
  `uv run --with-requirements requirements.txt python -m pytest tests/test_r4_synthetic_execution_record.py tests/test_m365_auth.py tests/test_api_m365_bridge.py tests/test_m365_observe.py tests/test_m365_write.py tests/test_m365_evidence_store.py -q`
  passed: 79 passed, 1 warning.
- Full after edits:
  `uv run --with-requirements requirements.txt python -m pytest -q` passed:
  564 passed, 4 warnings, 55 subtests.
- `bash scripts/governance-preflight.sh` passed with 0 warnings.
- `git diff --check` passed after the final handoff edit.
- Targeted scan passed with no hits in active code/tests/startup/remediation
  docs for the old R4 live module/symbol names or service-placeholder identity.

Open risks / next-chunk notes:

- Historical June reports still mention the old R4 live-executor name as
  history. Active startup/docs now route to the synthetic record surface.
- The dormant future app-only code path still exists for tests and later
  promotion planning, but no credential, secret, certificate, OAuth/consent, or
  live Microsoft 365 behavior was added.
- Next planned implementation chunk is EX-2, pending owner approval.

#### EX-1 Handoff

Status: integration complete.

Completion target: Integration complete.

Files / surfaces changed:

- Added a shared trace identity helper:
  `packages/uaos-core/src/gail_ai_operating_system/trace_identity.py`.
- Added a local trace/event/read-model spine:
  `packages/uaos-core/src/gail_ai_operating_system/read_model.py`.
- Added a core authority posture payload:
  `packages/uaos-core/src/gail_ai_operating_system/authority_registry.py`.
- Added read-only API endpoints:
  - `GET /api/v1/read-model`
  - `GET /api/v1/traces/{cns_trace_id}`
- Wired trace-aware persistence into:
  - `POST /api/v1/missions`
  - `POST /api/v1/actions`
  - `POST /api/v1/authority/override`
  - `POST /api/v1/m365/observe`
  - `POST /api/v1/m365/write/planner-task`
  - `GET /api/v1/evidence/{mission_id}`
- Added optional `cns_trace_id` to CP-1 mission, action, policy-decision,
  evidence-packet, and approval-decision schemas.

Response shapes now available:

- `GET /api/v1/read-model` returns:
  - `schema_version`
  - `generated_at`
  - `health`
  - `authority`
  - `connectors`
  - `agents`
  - `m365`
  - `recent_events`
  - `recent_evidence`
- `GET /api/v1/traces/{cns_trace_id}` returns:
  - `schema_version`
  - `cns_trace_id`
  - `found`
  - `mission_ids`
  - `action_ids`
  - `evidence_ids`
  - `authority_refs`
  - `mission_refs`
  - `evidence_refs`
  - `events`

Core behavior:

- New `cns_trace_id` values use `cns-YYYYMMDD-12safechars`.
- New mission, action, approval, and evidence factory paths generate or
  preserve a valid trace ID.
- Legacy records can still load when `cns_trace_id` is absent.
- API-created mission records persist under `GAIL_OS_STORE_PATH/missions`.
- Trace events persist under `GAIL_OS_STORE_PATH/trace-events`.
- Evidence remains under `GAIL_OS_STORE_PATH/evidence`.
- M365 observe now persists dry-run/stopped evidence, matching the existing
  dry-run write evidence posture.
- Duplicate/replay detection is visible through trace events via
  `idempotency_key`, `duplicate_detected`, and `duplicate_of_event_id`.

Validation:

- Baseline before edits:
  `uv run --with-requirements requirements.txt python -m pytest -q` passed:
  564 passed, 4 warnings, 55 subtests.
- Focused EX-1 subset:
  `uv run --with-requirements requirements.txt python -m pytest tests/test_read_model.py tests/test_api_read_model.py tests/test_api_missions.py tests/test_api_actions.py tests/test_api_authority.py tests/test_api_evidence.py tests/test_m365_observe.py tests/test_m365_evidence_store.py tests/test_m365_write.py tests/test_mission.py tests/test_action.py tests/test_approval_actions.py tests/test_evidence_packet.py tests/test_public_api.py -q`
  passed: 201 passed, 4 warnings, 20 subtests.
- CP-1 schema export:
  `uv run --with-requirements requirements.txt python scripts/export-cp1-contracts.py --verbose`
  passed: all 9 CP-1 schemas valid.
- Full after edits:
  `uv run --with-requirements requirements.txt python -m pytest -q` passed:
  577 passed, 5 warnings, 62 subtests.
- `bash scripts/governance-preflight.sh` passed with 0 warnings.
- `git diff --check` passed.

Open risks / next-chunk notes:

- This is still a local JSON persistence layer, not a production datastore.
- `cns_trace_id` remains optional for legacy/manual records, but API-created
  and factory-created records now get one.
- EX-2 should consume `GET /api/v1/read-model` in the command center without
  changing Python response shapes unless a gap is explicitly recorded.
- EX-3 should build the Freedom relationship/posture brief over the same trace
  layer.
- No live connector route, OAuth flow, Microsoft 365 live read/write/send,
  Graphify ingest, R4 live execution, frontend change, cloud placement, or
  source-of-truth migration was added.

#### EX-2 Handoff

Status: integration complete.

Completion target: Integration complete.

Files / surfaces changed:

- Added `apps/command-center/src/readModelClient.ts` as the typed frontend
  boundary for `GET /api/v1/read-model`, including runtime response validation,
  timeout handling, stale-data detection, and explicit HTTP/protocol/offline
  errors.
- Replaced the static cockpit snapshot in
  `apps/command-center/src/cockpitData.ts` with a read-model-to-operator-view
  mapper plus a non-fake waiting snapshot.
- Updated `apps/command-center/src/App.tsx` to render live read-model state and
  explicit loading, empty, local API-key missing/config missing,
  unauthorized, offline/unreachable, stale-data, and protocol-error states.
- Updated `apps/command-center/vite.config.ts` with a local same-origin proxy:
  `/gail-os-api/*` rewrites to `/api/v1/*` on the GAIL OS API target and
  injects `X-Api-Key` from the shell environment. The browser receives only a
  configured/not-configured flag, not the key value.
- Updated command-center styling for the status banner, refresh button, empty
  spoke state, responsive mission metadata, and mobile wrapping.
- Updated `README.md`, `AI_BOOTSTRAP.md`, `apps/command-center/README.md`,
  `docs/architecture.md`, `docs/source-of-truth-map.md`, and
  `docs/decisions/app-shell-command-center.md` to stop describing the cockpit
  as static-only.

Endpoint/UI shape introduced:

- Command center now consumes `GET /api/v1/read-model?limit=25`.
- Default frontend API base is `/gail-os-api`, with
  `GAIL_OS_API_PROXY_TARGET` defaulting to `http://127.0.0.1:8123`.
- Local run requires `GAIL_OS_API_KEY` in the shell running Vite/preview so the
  proxy can authenticate to GAIL OS without exposing the key to browser code.
- The cockpit shows:
  - GAIL OS reachability and freshness;
  - authority posture;
  - connector posture;
  - agent posture;
  - Microsoft 365 delegated/current app-only-future posture;
  - recent trace/evidence freshness.

Validation:

- Baseline before edits:
  `npm --prefix apps/command-center run build` passed.
- Final frontend build:
  `npm --prefix apps/command-center run build` passed.
- Frontend audit:
  `npm --prefix apps/command-center audit --audit-level=moderate` passed with
  0 vulnerabilities.
- Live read-only smoke:
  temporary local GAIL OS API on `127.0.0.1:8125` plus Vite on
  `127.0.0.1:5177` passed. The command center proxy returned
  `rev2.shared-read-model.v1` and 1 synthetic trace event for
  `cns-20260701-facefeedcafe`.
- Viewport evidence:
  Playwright using system Edge captured screenshots:
  - `tmp/screenshots/command-center-ex2-desktop.png` at 1366x900;
  - `tmp/screenshots/command-center-ex2-tablet.png` at 900x900;
  - `tmp/screenshots/command-center-ex2-phone.png` at 390x844.
  Visual review found no obvious overlap, clipped controls, or broken wrapping.
- `bash scripts/governance-preflight.sh` passed with 0 warnings.
- `git diff --check` passed.

Open risks / next-chunk notes:

- No Python read-model shape changed during EX-2.
- No write controls, live connector actions, OAuth/login, Microsoft 365 live
  reads/writes/sends/configuration, Graphify ingest, R4 live execution, cloud
  placement, source-of-truth migration, or native phone app was added.
- Frontend has no dedicated unit/component test harness yet; EX-2 uses
  TypeScript build, live proxy smoke, npm audit, governance preflight, and
  screenshot/manual viewport review as the risk-appropriate evidence.
- The Vite proxy is a local dev/preview convenience. A hosted command-center
  path would need a separate approved auth/reverse-proxy boundary.
- Next planned implementation chunk is EX-3, pending owner approval.

#### EX-3 Handoff

Status: not started.

## Non-Approval Boundary

This review and plan do not approve:

- live Microsoft 365 reads, writes, sends, Planner changes, Exchange changes,
  or Power Automate changes;
- app-only Microsoft 365 credentials or client secrets;
- Graphify production/persistent ingest;
- R4 live execution;
- production service readiness;
- cloud placement changes;
- source-of-truth migration;
- runtime consolidation across Rev 2, Freedom, Graphify, or AG Operations
  Workspace.
