# Local CNS Connection Proof Report

Document type: connection proof report
Date: 2026-06-28
Saved: 2026-06-28T17:49:02-06:00
Last Updated: 2026-06-28T18:19:59-06:00
Status: integration complete; CTP-2 local triangle proof complete, server refreshed, and contract gaps patched (2026-06-28T18:19:59-06:00)
Owner: Adam Goodwin

## Purpose

This report captures the first post-CMS connection scout across Freedom,
GAIL AI Operating System Rev 2, and Graphify after the Linux-side request to
expand Microsoft Entra permissions.

The proof deliberately stays outside live Microsoft 365, tenant/admin consent,
persistent Graphify ingest, cloud placement, production service behavior, and
authority expansion. It tests the current local CNS connection surfaces so the
next chunk can be chosen deliberately.

During closeout, `origin/main` advanced through GAIL OS Phase 5/6 commits up
to `5478b64`, adding OKP, Signal Gravity L1, a GAIL OS CP-5 proof segment,
R4 doctrine, CharterProfile, R4 dry-run simulation, and R4 live-executor code.
This report was rebased onto that current main state. Code presence is not
owner approval to execute R4 actions, expand Microsoft 365 permissions, run
live Graph calls, or mutate the persistent Graphify CNS store.

## Current Endpoint State

| Surface | Observed state |
|---|---|
| GAIL OS dev API | `http://10.77.77.1:8123/api/v1/health` returns `status=ok`, `boundary=A1 local no-network`, `phase=1`. |
| Graphify CNS API | `http://127.0.0.1:8001/api/cns/health` on Linux returns `status=ok`, `store=connected`, `node_count=0`. |
| Graphify DirectLink exposure | `http://10.77.77.2:8001` is not reachable because the running Graphify CNS API is bound to Linux loopback only. |
| Freedom runtime clients | Freedom can reach GAIL OS over DirectLink and Graphify over Linux localhost through existing integration clients. |

Follow-on CTP-2 server refresh: Windows restarted the GAIL OS dev server from
current code and then patched two small contract gaps that surfaced from the
Linux probe. The live server is now bound to `10.77.77.1:8123`, owned by a
fresh uvicorn process, and exposes 14 routes including `/api/v1/authority`,
`/api/v1/m365/status`, `/api/v1/m365/observe`, `/api/v1/authority/override`,
`/api/v1/agents`, and `/api/v1/okp`.

## Validation Evidence

Freedom to GAIL OS:

```text
cd /home/adamgoodwin/code/agents/the-freedom-engine-os
PATH=/home/adamgoodwin/.nvm/versions/node/v24.14.0/bin:$PATH \
GAIL_OS_API_URL=http://10.77.77.1:8123 \
GAIL_OS_API_KEY=dev-key \
npx tsx packages/gail-os-client/src/index.integration.ts
```

Result: 4 passed. Health, mission proposal, action validation, and
planning-only connector registry all passed.

Linux CTP-2 proof against the Windows GAIL OS server:

```text
X:\LINUX_TO_WINDOWS__2026-06-28-ctp2-complete-full-proof.md
```

Result: pass. Linux confirmed Freedom to GAIL OS CP-1 still passed 4/4,
`GET /api/v1/m365/status` returned the expected A1/not-configured readiness
shape, `POST /api/v1/m365/observe` returned an EvidencePacket with
`execution_mode=dry-run`, `POST /api/v1/authority/override` returned a pending
override record, and `GET /api/v1/agents` returned the six-agent registry. The
Linux proof used the 13-route contract already present before the extra
read-only `/api/v1/authority` registry endpoint was added.

Windows post-patch API contract probes:

```text
GET http://10.77.77.1:8123/openapi.json
GET http://10.77.77.1:8123/api/v1/authority
POST http://10.77.77.1:8123/api/v1/m365/observe {"dry_run": true}
```

Result: pass. Route count is 14; `/api/v1/authority` returns the read-only
R0-R5 authority ladder with `live_execution_enabled=false`,
`r4_requires_authority_envelope=true`, and `r5_human_only=true`;
`/api/v1/m365/observe` accepts a synthetic dry-run probe body and returns an
EvidencePacket with `execution_mode=dry-run`. With Azure env vars absent from
the dev server process, the observe result is correctly `stopped` and no live
Microsoft Graph call is made.

Focused Windows regression tests for the CTP-2 contract alignment:

```text
PYTHONPATH=packages/uaos-core/src
GAIL_OS_API_KEY=test-key-local
uv run --with-requirements requirements.txt python -m pytest \
  tests/test_api_authority.py \
  tests/test_m365_observe.py \
  tests/test_api_m365_bridge.py \
  tests/test_api_agents.py \
  tests/test_api_connectors.py \
  tests/test_api_evidence.py \
  tests/test_api_actions.py \
  tests/test_api_missions.py -q
```

Result: 82 passed, 3 warnings. The remaining warnings are existing Starlette
deprecation warnings in FastAPI/TestClient and unrelated older 422 constants.

Freedom to Graphify:

```text
cd /home/adamgoodwin/code/agents/the-freedom-engine-os
PATH=/home/adamgoodwin/.nvm/versions/node/v24.14.0/bin:$PATH \
GRAPHIFY_CNS_API_URL=http://127.0.0.1:8001 \
npx tsx packages/graphify-client/src/index.integration.ts
```

Result: 4 passed. Mission history, entity context, domain info, and fake CNS
mode behaved as expected.

GAIL OS Graphify and graph-fact contracts:

```text
uv run --with-requirements requirements.txt python -m pytest \
  tests/test_graphify_acceleration.py \
  tests/test_graphify_acceleration_preview.py \
  tests/test_graphify_handoff.py \
  tests/test_graph_fact_schema.py -q
```

Result: 72 passed, 26 subtests passed.

GAIL OS local evidence and M365 dry-run route contracts:

```text
uv run --with-requirements requirements.txt python -m pytest \
  tests/test_api_evidence.py \
  tests/test_api_m365_bridge.py \
  tests/test_m365_write.py \
  tests/test_m365_evidence_store.py -q
```

Result: 41 passed, 1 warning.

Graphify CNS API route contracts:

```text
cd /home/adamgoodwin/code/agents/graphify-workspace-cockpit
backend/.venv/bin/python -m pytest \
  tests/test_cns_evidence_route.py \
  tests/test_cns_api_freedom.py \
  tests/test_cns_api_gail_os.py -q
```

Result: 41 passed.

Current-main GAIL OS Phase 5/6 focused validation after rebasing onto
`5478b64`:

```text
PYTHONPATH=packages/uaos-core/src
uv run --with-requirements requirements.txt python -m pytest \
  tests/test_operating_knowledge.py \
  tests/test_operating_knowledge_store.py \
  tests/test_signal_gravity.py \
  tests/test_cp5_proof.py \
  tests/test_charter_profile.py \
  tests/test_r4_dry_run_simulation.py \
  tests/test_r4_live_executor.py -q
```

Result: 138 passed, 2 warnings.

Validation caveat: a combined single-process run of the new Phase 5/6 tests
plus older API tests produced 230 passes and 21 API failures caused by
`GAIL_OS_API_KEY` environment state in the shared test process. The same older
API/M365/evidence group passes when run isolated with
`GAIL_OS_API_KEY=test-key-local`. Treat this as a test-isolation fragility to
clean up before broad all-in-one API validation claims.

## What This Proves

- Freedom can reach GAIL OS over the private DirectLink path.
- Freedom can reach Graphify CNS API on Linux localhost.
- The CTP-2 local triangle proof is green for Freedom to GAIL OS, Freedom to
  Graphify, GAIL OS dry-run M365 readiness/observe, authority override, and
  agent registry probes.
- GAIL OS now exposes a read-only `/api/v1/authority` registry for local
  connection probes without granting execution authority.
- `/api/v1/m365/observe` now accepts a synthetic dry-run probe body for seam
  tests while rejecting live-style `dry_run=false` requests and still forcing
  `dry_run=True, allow_live=False` internally.
- GAIL OS can still produce sanitized Graphify-ready facts locally.
- GAIL OS evidence and M365 dry-run contracts remain healthy.
- Current `main` includes GAIL OS OKP, Signal Gravity L1, a GAIL OS CP-5 proof
  segment, R4 schema/simulation, and R4 live-executor code with focused tests
  green when run in scoped groups.
- Graphify has a tested local EvidencePacket ingest route and read/query
  routes, but this proof did not persistently ingest into the running Graphify
  CNS store.

## What This Does Not Prove

- It does not prove GAIL OS can directly call Graphify over DirectLink because
  the running Graphify CNS API is bound to `127.0.0.1`.
- It does not prove live Microsoft 365 access or writes.
- It does not approve the Linux request to expand Entra delegated scopes.
- It does not perform tenant/admin consent.
- It does not mutate the persistent running Graphify CNS store.
- It does not approve or run the R4 live executor now present on `main`.
- It does not close the full cross-repo CP-5 operating knowledge proof. The
  GAIL OS segment now exists, but Graphify L2 enrichment, Freedom OKP briefing,
  and a coordinated proof artifact still need their own validation.

## Recommended Next Chunk

CTP-1 and CTP-2 are now complete for the local connection lane. The next
bounded choices are:

1. Keep the Entra permission expansion paused.
2. Treat CTP-0, CTP-1, and CTP-2 as local proof only, not production service
   readiness.
3. Review the new GAIL OS Phase 5/6 commits now on `main` before executing
   any R4 or CP-5 follow-on. In particular, R4 doctrine remains an approval
   gate even though R4 live-executor code exists.
4. Decide whether to hand this CTP-2 proof back to the agentic multi-agent
   agent builder for revised orchestration, or continue locally into the next
   connection proof.
5. Define any next Graphify ingest proof as owner-gated:
   a synthetic dry-run EvidencePacket is posted to the local Graphify CNS API,
   read back, and recorded with rollback/delete instructions. This is the first
   point that should explicitly say "Graphify ingest" because it mutates the
   local Graphify CNS store.
6. Treat full CP-5 as a cross-repo proof, not just a GAIL OS unit proof:
   Graphify L2 enrichment, Freedom OKP briefing, and one durable proof artifact
   still need to be reconciled before calling the loop closed.

## Boundary Reply For Linux

Windows has received the request to expand Entra permissions, but the immediate
need Adam named is to test the local connections between Freedom, GAIL OS, and
Graphify. The safe collaborative path is to pause Entra permission expansion
and run the no-M365 local CNS connection lane first.

Linux should not treat this report as approval for Microsoft 365 delegated
write scopes, tenant/admin consent, live Graph calls, Planner writes, Teams
sends, SharePoint writes, Flow mutation, or app permission expansion.

Linux should also not treat the R4 live-executor code now present on GAIL OS
`main` as approval to run live R4 mutations. R4 execution remains owner-gated.
