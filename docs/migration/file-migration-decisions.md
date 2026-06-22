# File Migration Decisions

Created: 2026-06-21T15:13:19-06:00
Last Updated: 2026-06-21T20:51:47-06:00
Status: active migration decision record
Owner: Adam Goodwin

## Purpose

This record decides what may move from the superseded UAOS v1 workspace into
GAIL AI Operating System Rev 2.

It exists so future chunks can migrate or rewrite code without reopening the
whole Linux source tree, treating v1 as active source, or accidentally bringing
secrets, logs, generated artifacts, client data, raw audio, live connector
state, or local runtime state into the private Rev 2 repository.

## Core Rule

No UAOS v1 file may be copied into active Rev 2 source until it is listed here
and the active chunk revalidates the relevant source, target path, data class,
tests, and stop triggers.

Do not bulk-copy the v1 package, app, scripts, tests, logs, generated outputs,
or local state. Future chunks may inspect and migrate only the selected files
needed for that chunk.

## Decision Vocabulary

| Decision | Meaning |
|---|---|
| `promote` | Move or rewrite into active Rev 2 source with current controls and validation. |
| `rewrite` | Use the v1 file as design and test reference, then create Rev 2 code under current naming, permissions, and tests. |
| `archive` | Keep as copied reference or historical source only. Do not make active behavior. |
| `exclude` | Do not copy, migrate, summarize, or commit into Rev 2. |
| `later review` | Defer until a future chunk has a narrower boundary and approval path. |

## Current Migration Queue

The first safe code queue is:

1. Chunk Nine: rewrite the local no-network mission spine from selected v1
   mission and policy modules. Complete as of
   2026-06-21T15:39:29-06:00.
2. Chunk Ten: migrate or rewrite focused mission-spine tests. Complete as of
   2026-06-21T16:14:14-06:00.
3. Chunk Eleven: rewrite the connector registry foundation as local schema and
   validation only. Complete as of 2026-06-21T16:29:12-06:00.
4. Chunk Twelve: activate the enhanced Graphify handoff checkpoint as
   read-only routing and candidate validation only. Complete as of
   2026-06-21T16:48:17-06:00.
5. Chunk Thirteen: rewrite the relay envelope validator. Complete as of
   2026-06-21T17:09:24-06:00.
6. Chunk Fourteen: rewrite the relay record store and single-worker claim
   proof. Complete as of 2026-06-21T18:38:23-06:00.
7. Chunk Fifteen: build a local no-network proof runner. Complete as of
   2026-06-21T20:01:42-06:00.
8. Chunk Sixteen: define the Freedom phone-interface and agentic business
   partner boundary. Complete as of 2026-06-21T20:51:47-06:00 with
   `docs/decisions/freedom-phone-interface-business-partner-boundary.md`.

Portal source, Android-specific behavior, Windows/Linux worker bootstrap,
hosted relay, notifications, live connectors, and production release remain
outside this queue.

## Implemented Rewrites

| Active Rev 2 file | Source references | Completed | Boundary |
|---|---|---:|---|
| `packages/uaos-core/src/gail_ai_operating_system/mission_spine.py` | `mission.py`, `planner.py`, `policy.py` | 2026-06-21T15:39:29-06:00 | Local no-network mission envelopes, deterministic local plans, permission decisions, validation results, and JSON store only. |
| `packages/uaos-core/src/gail_ai_operating_system/__init__.py` | Rev 2 package interface | 2026-06-21T15:39:29-06:00 | Public local package exports only. |
| `tests/test_mission_spine.py` | Selected mission-spine behavior plus `test_safety_evaluations.py` | 2026-06-21T16:14:14-06:00 | Focused Chunk Nine behavior tests plus Chunk Ten local no-network safety stop-trigger, permission-gate, validation, and file-boundary tests. |
| `packages/uaos-core/src/gail_ai_operating_system/connector_registry.py` | `connector_registry.py` | 2026-06-21T16:29:12-06:00 | Local planning-only connector profile schema, validation, JSON-safe serialization, dry-run operation evaluation, duplicate-ID checks, and default-deny stop decisions only. |
| `tests/test_connector_registry.py` | `test_connector_registry.py` | 2026-06-21T16:29:12-06:00 | Tests for planning-only profile validity, JSON round trips, denied live capabilities, client-controlled approval gates, local dry-run decisions, unknown connector denial, and duplicate IDs. |
| `packages/uaos-core/src/gail_ai_operating_system/graphify_handoff.py` | `graphify_handoff.py` plus route shape from `graphify_adapter.py` | 2026-06-21T16:48:17-06:00 | Local read-only Graphify route status and handoff candidate validation only. No live adapter, HTTP fetch, graph upload, source mutation, full semantic rebuild, or execution approval. |
| `tests/test_graphify_handoff.py` | `test_graphify_handoff.py` | 2026-06-21T16:48:17-06:00 | Tests for route readiness, accepted read-only candidates, policy-gated dry-run mission actions, denied executed/mutating recommendations, evidence checks, sensitive-path rejection, live/client-data rejection, unapproved graph references, and required Graphify stop triggers. |
| `packages/uaos-core/src/gail_ai_operating_system/relay_envelope.py` | `relay_envelope.py` | 2026-06-21T17:09:24-06:00 | Local-file-only relay envelope schema validation for intent, approval, status, evidence, and handoff records. No hosted relay, worker polling, portal behavior, live connector action, client data, raw payload, or production behavior. |
| `tests/test_relay_envelope.py` | `test_relay_envelope.py` | 2026-06-21T17:09:24-06:00 | Tests for safe references, malformed JSON shapes, stale or expired approvals, hosted relay denial, worker polling denial, live connector denial, Graphify execution denial, and unsafe payload rejection. |
| `packages/uaos-core/src/gail_ai_operating_system/relay_store.py` | `relay_store.py` | 2026-06-21T18:38:23-06:00 | Local no-network relay record store proof for validated envelopes, status transitions, reference-only evidence records, and single trusted-worker claim attempts. No hosted relay, worker bootstrap, polling daemon, portal behavior, live connector action, client data, raw payload, or production behavior. |
| `tests/test_relay_store.py` | `test_relay_store.py` | 2026-06-21T18:38:23-06:00 | Tests for local persistence, reload, policy-gated claim validation, stale state rejection, duplicate trusted-worker claim rejection, trusted worker boundaries, evidence safety, and reference-only payload serialization. |

## Candidate Decisions

| Source | Exists checked | Decision | Earliest chunk | Boundary |
|---|---:|---|---|---|
| `docs/migration/reference/uaos-v1/**` | yes | `archive` | already copied | Keep as local reference material unless a later chunk promotes a specific record. |
| `L:\Applications\user-ai-operating-system` | yes | `later review` | none | Do not bulk-copy the v1 root. Inspect only named files needed for an active chunk. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine` | yes | `later review` | none | Do not bulk-copy the package. File-level selection is required. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\policy.py` | yes | `rewrite` | Chunk Nine | Use as a policy-gate reference for local no-network mission validation only. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\planner.py` | yes | `rewrite` | Chunk Nine | Use as planning-flow reference; remove v1 path assumptions and any external action assumptions. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\mission.py` | yes | `rewrite` | Chunk Nine | Use as mission-record reference; Rev 2 target must be local, deterministic, and no-network. |
| `L:\Applications\user-ai-operating-system\tests\test_safety_evaluations.py` | yes | `rewrite` | Chunk Ten | Converted into Rev 2 behavior tests around stop triggers, permission gates, risk-tier blocking, and local file boundaries without external services. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\connector_registry.py` | yes | `rewrite` | Chunk Eleven | Converted into Rev 2 local planning-only connector profile schema and validation with no live connector access. |
| `L:\Applications\user-ai-operating-system\tests\test_connector_registry.py` | yes | `rewrite` | Chunk Eleven | Converted into Rev 2 behavior tests for planning-only profiles, data classes, approval gates, local dry-run decisions, and denied live actions. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\graphify_handoff.py` | yes | `rewrite` | Chunk Twelve | Converted into Rev 2 local read-only handoff validation; Graphify remains a knowledge spoke, not execution approval. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\graphify_adapter.py` | yes | `rewrite` | Chunk Twelve | Inspected for route shape only. No live adapter, HTTP fetch, Graphify mutation, graph upload, or unapproved source indexing was copied. |
| `L:\Applications\user-ai-operating-system\tests\test_graphify_handoff.py` | yes | `rewrite` | Chunk Twelve | Converted into Rev 2 tests for candidate validation, denied execution authority, evidence checks, and enhanced Graphify routing boundaries. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\relay_envelope.py` | yes | `rewrite` | Chunk Thirteen | Converted into Rev 2 local-file-only relay envelope validation with Rev 2 source spine, device roles, stale-state checks, and unsafe-payload rejection. |
| `L:\Applications\user-ai-operating-system\tests\test_relay_envelope.py` | yes | `rewrite` | Chunk Thirteen | Converted into Rev 2 tests for no-network relay envelopes, stale approval/state rejection, hosted relay denial, worker polling denial, and unsafe payload rejection. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\relay_store.py` | yes | `rewrite` | Chunk Fourteen | Rewrite local record store and single-worker claim proof only; no hosted relay or polling daemon. |
| `L:\Applications\user-ai-operating-system\tests\test_relay_store.py` | yes | `rewrite` | Chunk Fourteen | Rewrite tests for local persistence, stale-state rejection, and claim conflict behavior. |
| `L:\Applications\user-ai-operating-system\apps\cockpit-command-proof\README.md` | yes | `archive` | already copied | Keep the README as reference for future portal UX and validation. |
| `L:\Applications\user-ai-operating-system\apps\cockpit-command-proof\index.html` | yes | `later review` | Chunk Sixteen | Use as UX reference only; do not copy before the portal stack and target app structure are chosen. |
| `L:\Applications\user-ai-operating-system\apps\cockpit-command-proof\app.js` | yes | `later review` | Chunk Sixteen | Use as behavior reference only; rewrite in the future portal stack. |
| `L:\Applications\user-ai-operating-system\apps\cockpit-command-proof\styles.css` | yes | `later review` | Chunk Sixteen | Use as visual reference only; rewrite to the Rev 2 design system when portal work starts. |
| `L:\Applications\user-ai-operating-system\scripts\validate-cockpit-proof.py` | yes | `later review` | Chunk Sixteen | May inform future portal checks, but not part of first code migration. |
| `L:\Applications\user-ai-operating-system\scripts\launch-cockpit.*` | yes | `later review` | Chunk Sixteen | May inform developer ergonomics only after portal app structure exists. |
| `L:\Applications\user-ai-operating-system\scripts\governance-check.sh` | yes | `exclude` | none | Rev 2 uses its own governed scaffold scripts. Do not vendor-copy v1 governance scripts. |
| `L:\Applications\user-ai-operating-system\scripts\governance-preflight.sh` | yes | `exclude` | none | Rev 2 uses its own governed scaffold scripts. Do not replace them with v1 scripts. |
| DirectLink operational scripts, indicators, runbooks, and skills | not inspected | `later review` | worker chunks | DirectLink remains transport/status only, not Rev 2 project source. |
| UAOS action logs, generated files, local runtime artifacts, caches, and temporary output | not inspected | `exclude` | none | Never commit runtime state or generated evidence dumps into Rev 2. |
| `.env` files, credentials, tenant secrets, tokens, private keys, and local master environment files | not inspected | `exclude` | none | Never inspect, summarize, copy, or commit secret values into Rev 2. |
| QuickBooks, accounting, invoice, payment, billing, finance, vendor-account, Microsoft 365, client, raw audio, raw log, or unredacted screenshot payloads | not inspected | `exclude` | none | Blocked until later explicit data and connector boundaries exist; real sensitive payloads do not belong in the repo. |

## External Freedom Engine Review Boundary

The downloaded Freedom Engine archive was reviewed on 2026-06-21 as an
external operating-partner OS reference and later recorded as the preferred
future phone-interface anchor candidate and high-level agentic business partner
capability source, not as active Rev 2 source.

Active review record:

- `docs/migration/freedom-engine-objective-review.md`

Decision summary:

| Source or concept | Decision | Earliest chunk | Boundary |
|---|---|---|---|
| Freedom monorepo root | `later review` | none | Do not bulk-copy or merge into Rev 2. Freedom remains Adam's current operating partner OS and likely phone-side operator link. |
| Freedom operator-run lifecycle and evidence vocabulary | `rewrite` | after Chunk Fifteen | Translate into Rev 2 mission/run/evidence records after the local proof runner exists. |
| Freedom self-learning, learning reviews, and business-memory loops | `rewrite` | after Chunk Sixteen | Preserve and elevate as governed learning, evidence, and memory-reference records. Do not import raw memories, logs, contacts, email data, provider state, or Supabase runtime data. |
| Freedom research and programming-request workflows | `rewrite` | after Chunk Sixteen | Translate into Rev 2 mission candidates, research/evidence records, and approval gates. Do not activate live web, provider, or tool-calling behavior without later connector boundaries. |
| Freedom agent/tool calling and tool-selection concepts | `later review` | connector/runtime activation chunks | Treat as core agentic business partner capability input. Requires connector profiles, capability gates, dry-run tests, explicit approval, rollback, and secret containment before runtime use. |
| Freedom consequence review model | `rewrite` | approval/connector chunks | Use as design input for higher-risk approval gates, not active runtime behavior. |
| Freedom Device Mesh and environment capability contracts | `rewrite` | portal/worker chunks | Translate as planning-only device and capability schemas before worker bootstrap or portal execution. |
| Freedom Action Fabric request/plan/result/evidence concepts | `rewrite` | action-classification chunks | Use after Rev 2 has proof-runner semantics; do not activate low-risk execution routes yet. |
| Freedom storage persistence map | `promote` | future data/evidence control chunk | Promote principles into Rev 2 docs; do not adopt Supabase runtime by implication. |
| Freedom phone-interface boundary | `complete decision` | Chunk Sixteen | Defined in `docs/decisions/freedom-phone-interface-business-partner-boundary.md`; Freedom is the substantial phone-interface anchor candidate and business-partner capability source, with bridge record shapes, permitted safe summaries, and no-import/no-runtime boundaries before app-shell or Android decisions. |
| Freedom Android/mobile UX | `anchor candidate` | after Chunk Sixteen | Use as the likely phone-side operator link for pairing, approval, hold/resume, offline import, and degraded-state truth; do not copy generated config, import app code, or modify Freedom until a later bounded integration chunk. |
| Freedom gateway and desktop-host runtime | `later review` | worker chunks | Use pairing, heartbeat, bounded body, approved-root, polling, and evidence patterns as references only. No service activation. |
| Freedom Supabase migrations and runtime tables | `later review` | hosted-runtime/data chunks | Reference schema ideas only. No active hosted store or data import. |
| Freedom voice, LiveKit, OpenAI, relay, wake, email, Vercel, and provider integrations | `later review` | connector/runtime activation chunks | Planning-only until connector profiles, tests, approvals, rollback, and secret containment exist. |
| Freedom `.env*`, generated mobile runtime config, `.local-data`, APKs, build outputs, binary assets, logs, provider state, contacts, email data, memories, raw transcripts, and secret-shaped material | `exclude` | none | Do not read values, summarize sensitive payloads, copy, commit, or treat as Rev 2 configuration. |

## Future Code Migration Rules

Each future code migration chunk must:

- start from this decision record, the source inventory, the source-of-truth
  map, the tool permission matrix, runtime instructions, and the active
  pathway;
- inspect only the selected v1 source files for the active chunk;
- create Rev 2 source under a deliberate Rev 2 package or app path chosen by
  that chunk;
- remove v1 absolute paths, Linux-source assumptions, tunnel dependencies, and
  stale authority language;
- keep behavior local and no-network until a later chunk explicitly approves a
  connector, relay, worker, or hosted surface;
- use synthetic fixtures only;
- add or rewrite tests near the migrated behavior;
- run governance preflight, schema validation when controls change, targeted
  tests or syntax checks, diff check, forbidden filename scan, strict
  secret-pattern scan, and Git/GitHub closeout;
- update this record if a new source file must join the queue.

## Stop Triggers

Stop before migration when:

- the source file is not listed here;
- a source file references secrets, live credentials, raw logs, raw audio,
  client data, accounting, billing, vendor, Microsoft 365 content, or
  production state;
- the migration would require a live connector, hosted relay, persistent
  worker, public ingress, production deployment, or external side effect;
- the target path, package name, tests, data class, approval gate, or rollback
  path is unclear;
- the source contradicts active Rev 2 controls.

## Current Boundary

Chunk Nine has rewritten the approved mission, planner, and policy references
into the first active local Rev 2 code slice. Chunk Ten has expanded its local
mission-spine safety tests from the approved v1 safety-evaluation reference.
Chunk Eleven has rewritten the connector registry foundation from the selected
v1 connector registry references as local schema, validation, JSON-safe
serialization, and dry-run/default-deny request evaluation only. Chunk Twelve
has rewritten the selected Graphify handoff references as local read-only route
status and candidate validation only. Chunk Thirteen has rewritten the selected
relay envelope references as local-file-only schema validation and safety tests
only. Chunk Fourteen has rewritten the selected relay store references as local
record persistence, status/evidence records, and single trusted-worker claim
proof only. Chunk Fifteen has built the local proof runner across the mission,
connector, relay-envelope, relay-store, trusted-worker-claim, and evidence
path. Chunk Sixteen has defined the Freedom phone-interface and business
partner boundary as a decision record, without importing Freedom source,
generated config, runtime state, or live behavior.

This record still blocks bulk copying and all files outside the approved queue.
Rev 2 remains a private governed repository with local no-network validation
and Git/GitHub closeout only. No live connector, portal, worker bootstrap,
persistent worker service, hosted relay, Graphify source mutation, graph
upload, full semantic rebuild, Freedom runtime activation, client-data, live
business-system, or production behavior is active.
