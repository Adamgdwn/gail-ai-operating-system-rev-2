# UX And Agentic Linkage Review Remediation Plan

Document type: review packet and remediation plan
Date: 2026-07-01
Saved: 2026-07-01T09:32:16-06:00
Last Updated: 2026-07-01T09:32:16-06:00
Status: draft
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
| R4 execution semantics | R0-R5 doctrine is clear and the R4 simulator/test surface gives the repo a concrete autonomy vocabulary. | `r4_live_executor.py` is publicly exported and creates live-labeled evidence even though it does not call external systems. The naming can be misunderstood by future agents. | For a fully agentic system, naming and feature gates must make real execution authority unambiguous. | P0 |
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
  - App-only service profile: uses service identity such as `svc-gail-os-graph`
    only after separate credential, scope, and authority-envelope approval.
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

## Recommended Execution Order

1. Track A: truthful onboarding and local validation.
2. Track G: R4/live-execution naming and feature-gate clarity.
3. Track F: Microsoft 365 dual-profile connector design and auth-code
   reconciliation.
4. Track B and Track C: live read-only command center plus governed local
   action loop.
5. Track D and Track E: `cns_trace_id`, Freedom relationship brief, event
   ledger, and Graphify synthetic fact-bundle replay.
6. Track H: harden quality gates and replace placeholder ops docs before
   declaring release readiness.

This order fixes trust and safety language before adding more capability. It
also lets the user experience become real in read-only form before the system
promotes controlled writes.

## Suggested Next Chunk

Start with a small remediation chunk:

**RMP-A - Truthful First Run And Local Runtime State Hygiene**

Scope:

- update first-run docs to the reliable uv-based validation path;
- mark unittest as partial or remove it from the main path;
- add `local_store/` to `.gitignore` if local evidence remains runtime-only;
- optionally add a short note that command center is currently static/sample
  state until Track B begins.

Completion target: Task complete

Validation:

- run the documented uv pytest command;
- run CP-1 schema export through uv;
- run command-center build if docs mention the frontend;
- run `git diff --check`.

Stop before changing Microsoft 365 auth behavior, opening OAuth/login surfaces,
promoting Graphify ingest, changing live execution code, or exposing new
write/action endpoints.

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

