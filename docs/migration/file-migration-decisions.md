# File Migration Decisions

Created: 2026-06-21T15:13:19-06:00
Last Updated: 2026-06-21T16:00:50-06:00
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
2. Chunk Ten: migrate or rewrite focused mission-spine tests.
3. Chunk Eleven: rewrite the connector registry foundation as local schema and
   validation only.
4. Chunk Twelve: activate the enhanced Graphify handoff checkpoint as
   read-only routing and candidate validation only.
5. Chunk Thirteen: rewrite the relay envelope validator.
6. Chunk Fourteen: rewrite the relay record store and single-worker claim
   proof.
7. Chunk Fifteen: build a local no-network proof runner.

Portal source, Android-specific behavior, Windows/Linux worker bootstrap,
hosted relay, notifications, live connectors, and production release remain
outside this queue.

## Implemented Rewrites

| Active Rev 2 file | Source references | Completed | Boundary |
|---|---|---:|---|
| `packages/uaos-core/src/gail_ai_operating_system/mission_spine.py` | `mission.py`, `planner.py`, `policy.py` | 2026-06-21T15:39:29-06:00 | Local no-network mission envelopes, deterministic local plans, permission decisions, validation results, and JSON store only. |
| `packages/uaos-core/src/gail_ai_operating_system/__init__.py` | Rev 2 package interface | 2026-06-21T15:39:29-06:00 | Public local package exports only. |
| `tests/test_mission_spine.py` | Selected mission-spine behavior from v1 references | 2026-06-21T15:39:29-06:00 | Focused Chunk Nine behavior tests; broader safety-evaluation test migration remains Chunk Ten. |

## Candidate Decisions

| Source | Exists checked | Decision | Earliest chunk | Boundary |
|---|---:|---|---|---|
| `docs/migration/reference/uaos-v1/**` | yes | `archive` | already copied | Keep as local reference material unless a later chunk promotes a specific record. |
| `L:\Applications\user-ai-operating-system` | yes | `later review` | none | Do not bulk-copy the v1 root. Inspect only named files needed for an active chunk. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine` | yes | `later review` | none | Do not bulk-copy the package. File-level selection is required. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\policy.py` | yes | `rewrite` | Chunk Nine | Use as a policy-gate reference for local no-network mission validation only. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\planner.py` | yes | `rewrite` | Chunk Nine | Use as planning-flow reference; remove v1 path assumptions and any external action assumptions. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\mission.py` | yes | `rewrite` | Chunk Nine | Use as mission-record reference; Rev 2 target must be local, deterministic, and no-network. |
| `L:\Applications\user-ai-operating-system\tests\test_safety_evaluations.py` | yes | `rewrite` | Chunk Ten | Convert into Rev 2 behavior tests around stop triggers and permission gates. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\connector_registry.py` | yes | `rewrite` | Chunk Eleven | Rewrite as connector profile schema and validation only; no live connector access. |
| `L:\Applications\user-ai-operating-system\tests\test_connector_registry.py` | yes | `rewrite` | Chunk Eleven | Rewrite tests for planning-only connector profiles, data classes, approval gates, and denied live actions. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\graphify_handoff.py` | yes | `rewrite` | Chunk Twelve | Rewrite as enhanced read-only handoff validation; Graphify remains a knowledge spoke, not execution approval. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\graphify_adapter.py` | yes | `rewrite` | Chunk Twelve | Rewrite only if the active checkpoint needs adapter shape; no Graphify mutation, graph upload, or unapproved source indexing. |
| `L:\Applications\user-ai-operating-system\tests\test_graphify_handoff.py` | yes | `rewrite` | Chunk Twelve | Rewrite tests for candidate validation, denied execution authority, and enhanced Graphify routing boundaries. |
| `L:\Applications\user-ai-operating-system\uaos_agent_spine\relay_envelope.py` | yes | `rewrite` | Chunk Thirteen | Rewrite with Rev 2 source spine, device roles, stale-state checks, and unsafe-payload rejection. |
| `L:\Applications\user-ai-operating-system\tests\test_relay_envelope.py` | yes | `rewrite` | Chunk Thirteen | Rewrite tests for no-network relay envelopes and denied unsafe payloads. |
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
into the first active local Rev 2 code slice.

This record still blocks bulk copying and all files outside the approved queue.
Rev 2 remains a private governed repository with local no-network validation
and Git/GitHub closeout only. No connector, portal, worker, hosted relay,
client-data, live business-system, or production behavior is active.
