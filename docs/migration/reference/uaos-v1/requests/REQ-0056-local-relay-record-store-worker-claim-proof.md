# REQ-0056: Local Relay Record Store And Worker Claim Proof

Created: 2026-06-14T18:43:22-06:00
Started: 2026-06-14T18:43:22-06:00
Completed: 2026-06-14T18:46:40-06:00
Status: complete
Owner: Adam Goodwin
Route owner: Codex

## Request Record

| Field | Value |
|---|---|
| Request ID | REQ-0056 |
| Created timestamp | 2026-06-14T18:43:22-06:00 |
| Started timestamp | 2026-06-14T18:43:22-06:00 |
| Completed timestamp | 2026-06-14T18:46:40-06:00 |
| Human owner | Adam Goodwin |
| Title | Local relay record store and worker claim proof |
| Intent | Prove the smallest no-network source-of-truth loop for relay approvals and trusted worker claims before hosted relay, phone UI, global cockpit UI, tunnel, or persistent worker service work. |
| Desired output | Local relay record store module, claim/reconciliation tests, active docs, and next implementation recommendation. |
| Domain | Build / Agent Architecture / Cross-Device Operations / Tool Governance |
| Risk tier | T3 safety foundation for future cross-device control plane |
| Data classification | Internal planning and local validation only; no client data, secrets, raw logs, raw audio, live relay, or live connector data |
| Source material | REQ-0055 relay envelope validator, REQ-0054 shared relay architecture, connector registry boundary, Graphify handoff boundary, cross-device source-of-truth foundation, Graphify Workspace Cockpit current pathway |
| Approval level | A3 mission envelope; A1/A2 local validation/default approval proof |
| Expected artifact | `uaos_agent_spine/relay_store.py`, `tests/test_relay_store.py` |
| Status | Complete |

## Route Note

| Field | Value |
|---|---|
| Selected route | Codex local runtime/test/docs route |
| Why this route | The relay envelope contract was validated; the next safe proof was local persistence and single trusted-worker claim behavior before adding infrastructure or UI. |
| Alternatives considered | Hosted relay now; rejected because local state, claim, stale-state, and conflict rules needed proof first. Phone UI now; rejected because phone/tablet approvals need durable record semantics first. Graphify source selection in UAOS; rejected because Graphify owns knowledge-source/cluster selection and chat. |
| Human approval required | Required before hosted relay, phone/tablet UI with write authority, persistent worker polling, live connector activation, M365 access, client-data flow, production action, external communication, destructive action, or Graphify write/action execution. |
| Tool/model/agent boundary | Local JSON-backed proof only. No network calls, hosted relay, phone UI, M365 tenant, Client Gateway, Graphify write, or worker daemon was activated. |
| Context allowed | UAOS active control docs, relay envelope module/tests, connector profiles, Graphify boundary docs, local Graphify current pathway. |
| Context forbidden | Secrets, raw credentials, client data, raw logs, raw audio, live M365/AWS/Dropbox/client-stack access, production deployment, Graphify mutation. |

## Task Brief

| Field | Value |
|---|---|
| Objective | Add a local record store that persists validated relay envelopes, records status changes and claim attempts, and allows exactly one trusted Linux/Windows worker claim for a mission when source-state references are current. |
| Files, systems, or surfaces involved | `uaos_agent_spine/relay_store.py`, `tests/test_relay_store.py`, active docs and request records. |
| Explicit non-goals | No hosted relay, no global cockpit UI, no phone/tablet app, no tunnel, no persistent worker service, no live connector session, no M365 access, no client workspace, no Graphify writes, no new runtime authority. |
| Acceptance criteria | Persist validated `RelayEnvelope` records; record status transitions and claim attempts; keep repo/workspace refs authoritative; require observed commit/issue/graph state before claim; allow one trusted worker claim per mission; reject conflicting, stale, superseded, unknown-device, unknown-connector, or unsafe claims; simulate Android/tablet/browser approvals and Windows/Linux workers locally; keep payloads reference-based. |
| Test or QA plan | Run focused relay store tests, relay envelope tests, full unit suite, Python compile, governance preflight, central New Build Agent governance check, diff whitespace check, and secret-pattern scan. |
| Security and privacy notes | The store records references, safe summaries, status history, and claim attempts only. Raw secrets, credentials, logs, audio, client-data-full payloads, live connector sessions, and Graphify writes remain prohibited. |
| Rollback or recovery plan | Revert the REQ-0056 code/docs commit or remove `uaos_agent_spine/relay_store.py`, `tests/test_relay_store.py`, and the related active-doc updates. No live service, connector, client, hosted relay, or production state was changed. |
| Expected handoff summary | REQ-0056 complete; next decision should choose the first product-facing surface: small relay proof runner, global cockpit shell, phone/tablet cockpit surface, or M365 inventory-only activation. |

## Approval Record

| Field | Value |
|---|---|
| Approval owner | Adam Goodwin |
| Approval level | A3 mission envelope; runtime A1/A2 validation proof |
| Action approved | Execute Chunk 20 with high diligence and shipping-ready practice. |
| Timestamp | 2026-06-14T18:43:22-06:00 |
| Conditions or limits | Keep Graphify as the knowledge-source selector/chat/map/recommendation spoke. UAOS may validate graph snapshot references and control mission approval/execution boundaries. |
| Related request/artifact | REQ-0055, REQ-0054, `docs/specs/shared-relay-phone-cockpit-architecture.md`, `uaos_agent_spine/relay_envelope.py` |

## Output Artifacts

- `uaos_agent_spine/relay_store.py`
- `tests/test_relay_store.py`
- Active control-document updates

## Validation Note

| Field | Value |
|---|---|
| What was checked | Repo governance and shipping standards, Graphify Workspace Cockpit boundary, local record persistence, Android/tablet/browser approval scenarios, Linux/Windows worker claim scenarios, stale-state rejection, superseded/conflicting status rejection, unknown device/role/connector rejection, unsafe payload rejection, and reference-only persistence. |
| Command or review performed | `bash scripts/governance-preflight.sh`; read-only Graphify Workspace Cockpit status/docs check; `python3 -m unittest tests.test_relay_store`; `python3 -m unittest tests.test_relay_store tests.test_relay_envelope`; `python3 -m py_compile uaos_agent_spine/relay_store.py uaos_agent_spine/relay_envelope.py uaos_agent_spine/policy.py uaos_agent_spine/planner.py`; `python3 -m unittest discover -s tests`; `git diff --check`; New Build Agent `governance_check.sh`; changed/untracked-file secret-pattern scan. |
| Result | Focused relay store tests passed: 9 tests. Focused relay store + relay envelope tests passed: 20 tests. Full suite passed: 70 tests. Compile and whitespace checks passed. Governance preflight passed with 0 warnings. Central governance check reported 0 required gaps and the known owner-decision warning. Changed-file secret-pattern scan found no matches. Graphify boundary check confirmed no overlap: Graphify owns help, chat, knowledge-source and cluster selection, map, decisions, recommendations, and read-only handoff; UAOS owns relay record validation, claims, policy, approvals, and execution boundaries. |
| Known gaps | No hosted relay, phone/tablet UI, global cockpit UI, worker polling daemon, M365 live access, Client Gateway live workspace, or production release exists yet. The store is a local proof, not a shared service. |
| Next action | Choose whether to implement a small local relay proof runner, global cockpit shell, phone/tablet cockpit surface, or M365 inventory-only activation chunk. |

## Learning Or Drift Note

| Field | Value |
|---|---|
| Learning classification | Product requirement / Safety control |
| What happened | The multi-device operating-system model needs a record store that distinguishes approval from worker claim, and current observed state from stale approval. |
| What worked | Keeping the store local and JSON-backed proved the core claim semantics without creating another source of truth or adding infrastructure. |
| What failed or drifted | Nothing material. The first reference-only payload assertion was tightened so safe guard fields such as `raw_audio_retained: false` are not mistaken for retained raw audio. |
| What rule/template/process should change | Future relay, phone, and worker chunks should require both a validated relay envelope and an accepted single-worker claim before execution work is considered. |
| Could this become OldSkoolAI content | Later |
