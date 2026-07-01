# Agent Instructions

## CNS Role (Guided AI Labs Agentic OS - updated 2026-07-01)

**Layer:** GAIL OS - Deep-brain / Mid-brain / Brain-stem governed control layer
**Function:** Authority envelopes, evidence ledger, action state machine, connector/agent registries, R0–R5 policy gate, trace continuity, and safe execution coordination
**In the CNS loop:** `Signal → GAIL OS classifies → Freedom reasons → OS validates authority → Motor system executes → Evidence returned to OS → Graphify updates → Freedom learns`

GAIL OS is the governed spine - the authority and evidence layer beneath all
other systems. No restricted action may execute without passing through the
GAIL OS policy gate.

**Critical CNS role:** Treat GAIL OS as the mid-brain and brain-stem of the
agentic operating system, not as a presentation layer. It coordinates intent,
authority, connector identity, action state, evidence, traceability, and stop
conditions. UI, read models, briefs, and docs are useful only when they are
tethered to real governed contracts and tested integration paths.

**Enabler, not a hand brake:** GAIL OS is what makes autonomy *safe and
legible*. By classifying actions, issuing authority envelopes, and recording
evidence, it is the layer that lets the system operate at higher autonomy
(R4 charter-based action) with accountability. Governance here is the enabler
of action, not a brake on it.

**Current state:** Rev 2 has moved past the older Chunk 1-19 framing. Current
`main` includes the Python spine, FastAPI HTTP surface, connector and agent
registries, authority override, dry-run M365 observe/write surfaces, evidence
store, OKP and Signal Gravity work, R4 charter/dry-run/synthetic
execution-record code, and Azure Container Apps pilot deployment records. The
current 2026-06-29 active
informing lane is
`docs/decisions/2026-06-29 - Graphify Boundary Transfer And GAIL OS Informing Plan.md`.

**Implemented core surfaces:**
- `mission_spine.py` — MissionEnvelope, MissionPlan, PermissionGate, LocalMissionStore
- `connector_registry.py` — planning-only connector profiles, including the M365 graph bridge
- `relay_envelope.py` — RelayEnvelope, RelayValidationContext, validate_relay_envelope
- `relay_store.py` — Local JSON-backed proof store for relay records, status transitions, worker claims
- `graphify_handoff.py` — Graphify handoff candidate validation with no authority transfer
- `local_proof_runner.py` — Complete no-network mission → policy → relay → evidence proof path
- `graphify_acceleration.py` — local sanitized relationship-fact contract for later Graphify learning
- `operating_knowledge.py` and `signal_gravity.py` — OKP records and local signal ranking
- `charter_profile.py`, `r4_dry_run_simulator.py`, `r4_synthetic_execution_record.py` — R4 charter and synthetic proof-record surfaces; no live external adapter is exported

**Current planning route:** Stay away from Freedom implementation work unless
Adam explicitly routes the session there. For GAIL OS work, import the
Graphify boundary revelation into authority, evidence, GraphFact, and
communication plans. Graphify is the high-speed relationship-transfer layer,
not authority and not execution.

**Current API surface (upstream - produces governed records):**
- `GET /api/v1/health` — Liveness and boundary check
- `POST /api/v1/missions` — Classify and create mission records
- `POST /api/v1/actions` — Validate proposed actions against policy
- `GET /api/v1/authority` — Return read-only R0-R5 authority registry
- `POST /api/v1/authority/override` — Record override requests
- `GET /api/v1/evidence/{mission_id}` — Retrieve mission evidence summaries
- `GET /api/v1/connectors` — Return connector registry status
- `GET /api/v1/agents` — Return agent registry status
- `GET /api/v1/m365/status` — Dry-run M365 bridge readiness
- `POST /api/v1/m365/observe` — Synthetic dry-run observe proof
- `POST /api/v1/m365/write/planner-task` — Dry-run Planner-task proof
- `POST /api/v1/okp`, `GET /api/v1/okp`, `GET /api/v1/okp/{okp_id}`,
  `GET /api/v1/okp/{okp_id}/proof-chain` — Operating knowledge packet routes

**Integration contracts (downstream - consumes):**
- Receives safe `SignalPacket`/mission/action candidates from approved surfaces.
- May request bounded relationship context from Graphify when relationships
  matter.
- May emit sanitized `GraphifyAccelerationRecord` or `GraphFact` candidates
  into an owner-gated Graphify learning lane.

**Graphify boundary:** "Read-only Graphify" means read-only with respect to
GAIL OS authority, approval, execution, and source-system mutation. It does not
forbid approved graph-memory writes. GAIL OS may prepare or emit sanitized,
idempotent, source-referenced relationship facts through an explicit
owner-gated lane. Graphify may inform and remember relationships; it may not
approve, deny, execute, escalate authority, mutate business systems, or become
the canonical evidence ledger.

**Authority boundary:** This repo is the R0-R5 authority source. R5 is
human-only - no agent may bypass this. R4 requires a signed AuthorityEnvelope
with explicit charter, stop conditions, rollback path, and review cadence.

**Cross-machine note:** GAIL OS runs on Windows and has also been deployed to
the narrow Azure Container Apps pilot. Freedom and Graphify work may be on
Linux or hosted surfaces. DirectLink is approved for local proof transport, but
it is not a production service boundary or a reason to broaden live connector
authority.

For cross-repo coordination state, see `agentic-multi-agent-agent-builder/docs/build-control/` (Linux control plane repo).

---

## Normal Startup

For ordinary scoped work:

1. run `git status --short`
2. read this file
3. use `docs/context-map.md` when context routing is unclear
4. inspect the specific files, errors, or docs needed for the task
5. run targeted validation after the change

Do not turn `START_HERE.md`, pathway docs, governance standards, Graphify, plugins, MCP servers, or provider tools into an automatic startup chain for every small edit.

## Governance Triggers

Before making material or risk-triggering code or configuration changes in this repository:

1. read `START_HERE.md`
2. review the active plan named in `START_HERE.md` (default `docs/current-build-pathway.md`)
3. review `docs/standards/README.md`
4. review `docs/standards/engineering-governance-by-use-case.md`
5. review `docs/policy/durable-development-engineering-policy.md`
6. review `docs/standards/ship-ready-engineering-standard.md`
7. run the governance preflight check
8. review `project-control.yaml`
9. note any open exceptions relevant to the work
10. capture a timestamp with `date -Iseconds`
11. proceed only after the project passes preflight or any gaps are explicitly accepted

Risk-triggering work includes production, deployment, authentication, authorization, payments, secrets, sensitive data, database migrations, customer communications, external side effects, infrastructure or provider settings, destructive actions, autonomous tool use, risk classification, governance policy changes, or release readiness.

## Preflight

```bash
bash scripts/governance-preflight.sh
```

## Working Rules

- Follow the repository standards by default.
- Use `docs/standards/README.md` as the standards map for coding and release work.
- Confirm the requested work matches the project's `use_case.primary` classification.
- Apply the durable development standard: build the smallest useful thing in the safest durable way.
- Treat Definition of Shipped as a separate evidence gate before declaring meaningful work complete.
- Use `docs/standards/context-hygiene-standard.md` for long sessions, scoped repository reads, compaction, and handoffs.
- Apply lean startup: keep always-on checks short, and trigger heavy governance, Graphify, plugin, MCP, and release checks by task risk or scope.
- Use `docs/context-map.md` to route task-specific context before loading broad docs or source trees.
- Do not silently skip required documentation or controls.
- Record justified deviations as exceptions.
- Reassess governance when risk, autonomy, data sensitivity, or money movement changes.
- Keep work in context-window-friendly chunks with one objective, clear files, validation, and handoff notes.
- Plan before writing for meaningful changes: each feature chunk must name the
  user/operator outcome, source-of-truth path, integration seam, acceptance
  tests, stop-before lines, and rollback/recovery posture.
- Build the feature and test the feature. A chunk that adds only UI, sample
  data, a pass-through wrapper, or a disconnected read model is not a complete
  user capability unless it is explicitly scoped and reported as groundwork.
- Favor deep, tested connections across intent, authority, connector identity,
  action state, evidence, trace, and operator surfaces over weak layers stapled
  on top of the system.
- Define the target completion state for each meaningful chunk: `Draft complete`, `Task complete`, `Integration complete`, `Release ready`, or `Blocked`.
- Project completion is a human decision. Agents may report only bounded completion states when the documented criteria and verification evidence support that label.
- Stop when the chunk's definition of done is met, when its stop condition is reached, or when repeated attempts stop producing new evidence.
- In the active plan document, label active and planned chunks clearly and keep the document's existing heading pattern.
- Timestamp material work, decisions, validation, and handoffs.
- Update the active plan named by `START_HERE.md` when the active plan, status, or next chunk changes.

## Fundamentals-First AI Coding

Build fundamentals-first software. AI speed does not make bad code cheap.

Before meaningful coding, reach shared understanding. Use consistent domain language. Prefer deep modules with simple interfaces over shallow pass-through layers.

Let feedback loops set the pace: types, tests, linting, runtime checks, and user-visible validation.

Design interfaces deliberately, then implement in small vertical slices.

Avoid flimsy pass-through layers, generic helpers, premature abstractions, swallowed errors, untyped blobs, duplicated business rules, hidden production assumptions, and fake validation claims.

When you see weak design, flag it and propose the smallest safe improvement instead of rewriting the project.

Every change should make the next correct change easier.

## Context Hygiene

Operate with strict context hygiene. Keep active context minimal, relevant, current, and recoverable.

Work in clear phases. Summarize at phase boundaries. Compact or reset before quality degrades. Re-state critical constraints after compaction.

Narrow file scope before reading. Prefer targeted diffs and specific files over whole-repo exploration.

Treat tokens as a budget, but do not skip required governance, security, architecture, or task-critical reading.

The repository remembers. Agents rent context. Keep work packets, scout summaries, validation, and handoffs durable enough that the next agent does not need the chat thread.

Keep read-only scout outputs summary-only.

After a compaction, context clear, or fresh restart, treat the latest handoff or active work packet as the resume point. Then check `git status --short`, read the short repo-local instructions, read the active plan named by `START_HERE.md` only when the task needs it, and avoid archived logs or broad scans unless the current objective requires them.

## Graphify Policy

Use the canonical Graphify governance file:

`/home/adamgoodwin/code/Tools/graphify/docs/agent-governance.md`

Before broad source exploration, architecture analysis, dependency tracing, unfamiliar large-surface work, or cross-repo planning, use Graphify first and reference the workspace graph at:

`/home/adamgoodwin/code/Tools/graphify/workspace/out/graph.json`

Use the workspace graph for cross-repo routing. When a new repo becomes active, set up repo-local Graphify with:

```bash
graphify-setup-project /path/to/repo
```

For full semantic repo graphs in heavy active repos, run `/graphify /path/to/repo` from Claude Code. Current Graphify skills can use Claude Code subagents when no Gemini key is set, so policy should constrain token burn through per-repo scope, caching, strict ignores, and cheap updates rather than hard-coding a provider or extraction backend.

Use Graphify to orient, then inspect only the files needed for the actual change. Do not require Graphify for known files, build or test errors, small scoped edits, or routine docs checks. After code changes, update the relevant graph with `graphify update . --no-cluster`, or update the workspace graph for cross-repo work. Do not trigger a full `/graphify` rebuild to answer a question, at session start, or after a context clear; query the existing graph instead. A full semantic pass is a deliberate, once-per-major-change act, roughly 1M subagent tokens. Routine refreshes use the cheap incremental `graphify update . --no-cluster`. Preserve existing secret-handling rules: do not index, print, summarize, or commit secrets or environment files.

## Chunk Close-Out Protocol

At the end of every chunk of work:

1. Check `CARRY_FORWARD.md` — if it has any open items, surface them to the
   user before proceeding. If there are open flags that must survive the context
   reset, read them aloud and wait for confirmation.
2. Stage the relevant files, commit with a clear message, and push. Do this
   automatically — do not ask unless a carry-forward flag or blocker requires
   a decision first.
3. Confirm the push succeeded, then suggest `/compact` to compress the context
   window. Do not suggest `/clear` — compact preserves the summary of what was
   done, which is cheaper to resume from than a cold start.
4. `/clear` is an explicit user override only: use it when prior context had
   persistent wrong assumptions, or the next chunk is in a completely unrelated
   domain.
5. Do not auto-compact. Do not skip the commit step without flagging why.

A chunk ends when:
- the current definition-of-done in `docs/current-build-pathway.md` is met, or
- a stop condition is reached (blocker, repeated failure, scope boundary), or
- the user signals done.
