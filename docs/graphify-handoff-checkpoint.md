# Graphify Handoff Checkpoint

Created: 2026-06-21T16:48:17-06:00
Last Updated: 2026-06-29T19:31:31-06:00
Status: active checkpoint
Owner: Adam Goodwin

## Purpose

This checkpoint defines how GAIL AI Operating System Rev 2 may use Graphify
during the current file migration and build-out phase.

Graphify is a relationship-intelligence spoke. It may reduce raw source reads
and help route architecture or migration work, but its recommendations remain
mission candidates until Rev 2 validation, policy, and owner approval accept
them.

2026-06-29 boundary clarification: "read-only Graphify" means read-only with
respect to GAIL OS authority, approval, execution, source-system mutation, and
evidence truth. It does not mean Graphify can never receive approved learning
facts. Bounded, sanitized, idempotent graph-memory writes may exist only through
explicit owner-gated lanes. Graphify may remember relationships; it may not
approve, deny, execute, escalate authority, or become the canonical evidence
ledger.

Related outbound-readiness plan:
`docs/decisions/2026-06-27 - Graphify Acceleration Readiness Plan.md` defines
how Rev 2 should later emit sanitized, delta-friendly authority, action,
evidence, connector, and system-state facts so an enhanced Graphify layer can
move faster without gaining execution authority.

Current boundary transfer packet:
`docs/decisions/2026-06-29 - Graphify Boundary Transfer And GAIL OS Informing Plan.md`
is the active route for applying the refined Graphify boundary inside this
repo.

## Current Route

| Item | Current state |
|---|---|
| Canonical governance file | `/home/adamgoodwin/code/Tools/graphify/docs/agent-governance.md` |
| Windows access path | `L:\Tools\graphify\docs\agent-governance.md` |
| Workspace graph | `/home/adamgoodwin/code/Tools/graphify/workspace/out/graph.json` |
| Windows workspace graph path | `L:\Tools\graphify\workspace\out\graph.json` |
| Repo-local graph | `graphify-out/graph.json` is not present yet in Rev 2 |
| Windows CLI probe | `graphify` and `graphify-setup-project` were not on the Windows PATH |
| Linux CLI probe | `graphify` and `graphify-setup-project` were present under `/home/adamgoodwin/.local/bin` |

The workspace graph exists and was last observed as a local file of
177,549,876 bytes with 41,881 nodes. A first broad query returned noisy
cross-workspace CMake nodes, so agents should treat Graphify output as routing
context, not proof or authority.

## Allowed Current Use

Agents may:

- read the canonical Graphify governance file;
- query the existing workspace graph before broad source exploration,
  architecture routing, dependency tracing, or graph-dependent migration work;
- inspect only the files selected by the active Rev 2 work packet after graph
  routing;
- validate Graphify handoff payloads with
  `gail_ai_operating_system.validate_graphify_handoff_payload`;
- build local route status records with
  `gail_ai_operating_system.build_graphify_route_status`.
- prepare sanitized GraphifyAccelerationRecord/GraphFact candidates for
  preview, reconciliation, or owner-gated learning-lane design.

Current allowed command shapes, when the CLI is available in the active shell:

```bash
graphify query "<question>" --graph /home/adamgoodwin/code/Tools/graphify/workspace/out/graph.json
graphify-setup-project .
graphify update . --no-cluster
```

The repo-local setup and update commands are instructions for an approved
active shell or future worker clone. They do not approve graph upload, source
mutation, or a full semantic rebuild.

## Handoff Payload Contract

Valid Graphify handoff payloads must:

- include a schema version and approved graph reference;
- use a `recommendations` list;
- keep recommendation status as `candidate`, `proposed`, `read-only`, or
  `needs-review`;
- include a source recommendation ID, title, summary, evidence refs, confidence,
  risk, data classification, files in scope, non-goals, and stop triggers;
- keep confidence at or above `0.6`;
- keep risk to `low` or `medium`;
- keep data classification to `public`, `internal`, or `synthetic`;
- include only relative non-sensitive file references;
- include the `graphify_action_execution` stop trigger;
- convert only to dry-run `graphify_handoff_read` mission actions.

Invalid payloads include:

- `executed`, `approved`, `completed`, or `applied` recommendations;
- `executed_at`, `approved_at`, `result`, or `rollback_note` fields;
- graph upload paths, temporary graph outputs, or unapproved graph references;
- source mutation, delete, commit, push, send, tenant, billing, payment,
  live connector, client-data, raw payload, production, secret, token, or
  credential hints;
- absolute paths, parent traversal, `.env`, raw log, raw audio, invoice,
  accounting, or client-data references.

## Stop Boundary

Stop before:

- graph upload;
- source mutation through Graphify;
- treating a Graphify fact preview as evidence or ingest;
- treating a Graphify learning write as approval, denial, execution, or
  authority escalation;
- a full `/graphify` semantic rebuild outside an explicit chunk;
- treating a Graphify recommendation as execution approval;
- indexing, printing, summarizing, or committing secrets, environment files,
  raw logs, raw audio, client data, Microsoft 365 content, QuickBooks or
  accounting records, or production state.

## Chunk Twelve Result

Chunk Twelve added local validation only:

- `packages/uaos-core/src/gail_ai_operating_system/graphify_handoff.py`
- `tests/test_graphify_handoff.py`

No live Graphify adapter, HTTP fetch, graph upload, source mutation, portal,
worker, hosted relay, client-data flow, live connector, or production behavior
was activated.
