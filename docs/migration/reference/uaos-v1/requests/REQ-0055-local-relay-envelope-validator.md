# REQ-0055: Local Relay Envelope Validator

Created: 2026-06-14T17:27:10-06:00
Started: 2026-06-14T17:27:10-06:00
Completed: 2026-06-14T17:30:33-06:00
Status: complete
Owner: Adam Goodwin
Route owner: Codex

## Request Record

| Field | Value |
|---|---|
| Request ID | REQ-0055 |
| Created timestamp | 2026-06-14T17:27:10-06:00 |
| Started timestamp | 2026-06-14T17:27:10-06:00 |
| Completed timestamp | 2026-06-14T17:30:33-06:00 |
| Human owner | Adam Goodwin |
| Title | Local relay envelope validator |
| Intent | Turn the shared relay and phone/tablet cockpit architecture into a local no-network validation contract for Android, tablet, Windows, Linux, browser, and future relay records. |
| Desired output | Validator module, focused tests, policy/evaluation updates, active docs, and next implementation recommendation. |
| Domain | Build / Agent Architecture / Cross-Device Operations / Tool Governance |
| Risk tier | T3 safety foundation for future cross-device control plane |
| Data classification | Internal planning and local validation only; no client data, secrets, raw logs, raw audio, live relay, or live connector data |
| Source material | REQ-0054 shared relay architecture, connector registry boundary, Graphify handoff boundary, M365 boundary, cross-device source-of-truth foundation, Graphify Workspace Cockpit current pathway |
| Approval level | A3 mission envelope; A1/A2 runtime proposal/default validation |
| Expected artifact | `uaos_agent_spine/relay_envelope.py`, `tests/test_relay_envelope.py` |
| Status | Complete |

## Route Note

| Field | Value |
|---|---|
| Selected route | Codex local runtime/test/docs route |
| Why this route | The next safe step was to validate relay records locally before any hosted relay, phone UI, tunnel, worker poller, or persistent service exists. |
| Alternatives considered | Build the global cockpit UI now; rejected because device records need a tested contract first. Build a hosted relay now; rejected because identity, stale-state, approval, and source-of-truth rules should be proven locally first. Put source selection into UAOS; rejected because Graphify owns knowledge-source and cluster selection. |
| Human approval required | Required before any hosted relay, phone/tablet UI with write authority, persistent worker service, M365/Entra auth activation, live connector activation, public inbound worker access, client-data flow, destructive action, production action, or external communication. |
| Tool/model/agent boundary | Local validation only. No live connector, hosted relay, phone UI, M365 tenant, Client Gateway, or Graphify write capability was activated. |
| Context allowed | UAOS active control docs, REQ-0054 relay architecture, connector registry profiles, Graphify boundary docs, M365 boundary docs, local Graphify current pathway. |
| Context forbidden | Secrets, raw credentials, client data, raw Graphify state mutation, live M365/AWS/Dropbox/client-stack access, production deployment. |

## Task Brief

| Field | Value |
|---|---|
| Objective | Define and test a `RelayEnvelope` contract that keeps all future device/cockpit relay records reference-based, current, scoped, and policy-checkable. |
| Files, systems, or surfaces involved | `uaos_agent_spine/relay_envelope.py`, `tests/test_relay_envelope.py`, `uaos_agent_spine/policy.py`, `uaos_agent_spine/planner.py`, `tests/test_safety_evaluations.py`, active docs and request records. |
| Explicit non-goals | No hosted relay, no phone/tablet app, no global cockpit UI, no worker polling service, no Cloudflare Tunnel, no Tailscale dependency, no M365 access, no client workspace creation, no Graphify writes, no new runtime authority. |
| Acceptance criteria | Define relay shape with project, graph, request, mission, actor, device, approval, connector, stop-trigger, and state references; reject raw secrets/logs/audio/client payloads/live sessions; reject stale, superseded, conflicting, unknown-device, unknown-connector, inbound-worker, unapproved-live-action, Graphify-execution, M365-beyond-planning, and Client Gateway full-assessment records; keep validation no-network; add tests. |
| Test or QA plan | Run focused relay tests, focused safety tests, Python compile, full unit suite, governance preflight, central New Build Agent governance check, diff whitespace check, and secret-pattern scan. |
| Security and privacy notes | Relay payloads must carry references and safe summaries only. Secret values, raw credentials, unrestricted filesystem access, raw logs, raw audio, unscoped client data, and live connector sessions stay out of relay records. |
| Rollback or recovery plan | Revert `b9147a0` or apply a follow-up reverting REQ-0055 code, tests, and active-doc updates. No hosted relay, connector, client, M365, or production state was changed. |
| Expected handoff summary | REQ-0055 complete; next implementation chunk should prove local relay records and worker claim/reconciliation before any hosted relay or global cockpit UI. |

## Approval Record

| Field | Value |
|---|---|
| Approval owner | Adam Goodwin |
| Approval level | A3 mission envelope; runtime A1/A2 validation |
| Action approved | Verify coding/shipping/completion practices and execute the next chunk. |
| Timestamp | 2026-06-14T17:27:10-06:00 |
| Conditions or limits | Keep Graphify as the knowledge-source selector/chat/instructions surface; UAOS validates references to Graphify snapshots and controls mission approval/execution boundaries. |
| Related request/artifact | REQ-0054, `docs/specs/shared-relay-phone-cockpit-architecture.md`, Graphify Workspace Cockpit Chunks 15-17 planning |

## Output Artifacts

- `uaos_agent_spine/relay_envelope.py`
- `tests/test_relay_envelope.py`
- Policy/evaluation updates for relay validation and phone/relay live-action stop triggers
- Active control-document updates

## Validation Note

| Field | Value |
|---|---|
| What was checked | Repo governance and shipping standards, Graphify Workspace Cockpit boundary, relay-envelope acceptance scenarios, policy gate behavior, safety stop trigger, Python compile, and source-of-truth docs. |
| Command or review performed | `bash scripts/governance-preflight.sh`; read-only Graphify Workspace Cockpit status/docs check; `python3 -m unittest tests.test_relay_envelope`; `python3 -m unittest tests.test_safety_evaluations`; `python3 -m py_compile uaos_agent_spine/relay_envelope.py uaos_agent_spine/policy.py uaos_agent_spine/planner.py`; `python3 -m unittest discover -s tests`; `git diff --check`; New Build Agent `governance_check.sh`; changed/untracked-file secret-pattern scan. |
| Result | Focused relay tests passed: 11 tests. Focused safety evaluations passed: 13 tests. Full suite passed: 61 tests. Compile and whitespace checks passed. Governance preflight passed with 0 warnings. Central governance check reported 0 required gaps and the known owner-decision warning. Secret-pattern scan matched policy words and deliberately fake redaction-test strings only. Graphify boundary check confirmed Graphify owns help, chat, knowledge-source selection, graph maps, decisions, recommendations, and handoff; UAOS owns relay validation, mission control, policy, and execution. Commit `b9147a0` was pushed to `origin/main`. |
| Known gaps | No relay record store, worker claim flow, hosted relay, phone/tablet UI, global cockpit UI, M365 live access, Client Gateway live workspace, or production release exists yet. |
| Next action | Build a local no-network relay record store and worker-claim proof that uses `RelayEnvelope` records before any hosted relay or global cockpit UI. |

## Learning Or Drift Note

| Field | Value |
|---|---|
| Learning classification | Product requirement / Safety control |
| What happened | The multi-device operating-system concept needs one governed source of truth with many surfaces, not multiple independent operating systems. |
| What worked | Validating relay envelopes locally creates the first enforceable contract for phone/tablet/Windows/Linux/browser records without adding infrastructure or duplicating Graphify. |
| What failed or drifted | The previous handoff still said REQ-0054 was pending commit/push even though it was already pushed. This chunk cleans that handoff drift. |
| What rule/template/process should change | Future device/cockpit chunks must validate project ID, graph snapshot, actor, device role, approval level, stop triggers, connector profile, and observed state before execution. |
| Could this become OldSkoolAI content | Later |
