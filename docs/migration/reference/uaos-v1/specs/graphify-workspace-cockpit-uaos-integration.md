# Graphify Workspace Cockpit UAOS Integration

Created: 2026-06-14T10:19:48-06:00
Last Updated: 2026-06-14T16:55:15-06:00
Status: active architecture note; updated with REQ-0054 relay boundary and transcript learning
Owner: Adam Goodwin

## Purpose

This note captures how the separate Graphify Workspace Cockpit changes the User
AI Operating System build.

Graphify Workspace Cockpit is not just another execution tool. It is the likely
workspace knowledge lookup and optimization layer: the place where UAOS can ask
what exists, why things are connected, which repo or document matters, what
should be archived, and what should become the next bounded mission.

## Current Understanding

Graphify Workspace Cockpit is a local-first app at:

```text
/home/adamgoodwin/code/agents/graphify-workspace-cockpit
```

Its current design:

- reads Graphify `graph.json` from the workspace;
- exposes Ask, Map, Decisions, Recommendations, and Work Queue tabs;
- uses Graphify CLI for `query`, `path`, and `explain`;
- keeps decisions, recommendations, actions, sessions, and settings in local
  JSON state under `workspace/state/`;
- stays read-only by default;
- delays approved action execution until later chunks with dry-run and explicit
  approval.

That makes it a knowledge cockpit, not an autonomous executor.

## Architectural Role

UAOS should treat Graphify Workspace Cockpit as a governed knowledge spoke that
sits before mission execution.

```text
Workspace files and repos
  -> Graphify graph extraction
    -> Graphify Workspace Cockpit
      -> Ask / Map / Decisions / Recommendations / Work Queue
        -> UAOS mission envelope
          -> Local Mission Agent
            -> policy gate
            -> tool adapter
            -> validation
            -> action log
```

The practical division:

| Layer | Owns |
|---|---|
| Graphify Workspace Cockpit | Workspace map, graph-backed Q&A, relationship explanation, human decision ledger, recommendation cards, queued proposed actions. |
| UAOS | Mission envelope, approval boundary, policy gate, execution adapters, validation evidence, request records, learning promotion. |
| Microsoft 365 business environment | Future business document, email, calendar, Teams, SharePoint, and operational workspace surfaces. |
| Shared relay / phone cockpit | Future mission coordination, approval prompts, pause/resume, status, and evidence-summary surfaces that reference durable UAOS records without owning graph knowledge or local execution. |

## Build Consequences

### 0. Check This Boundary Before Major UAOS Turns

Before any major UAOS architecture, connector, source-of-truth, tool-adapter,
or planning turn, do a quick check against this document and the current
Graphify Workspace Cockpit state.

The check should ask:

- is UAOS trying to rebuild graph lookup, workspace map, recommendation, or
  queued-action behavior that belongs in Graphify Workspace Cockpit?
- is Graphify output being treated as execution approval rather than
  read-only knowledge input?
- does the proposed UAOS change consume a stable handoff record, source
  reference, or evidence node instead of reaching into Graphify internals?
- is the durable source-of-truth path still clear across UAOS, Graphify, and
  the private GitHub spine?

### 1. Do Not Fold Graphify Cockpit Into UAOS Runtime

Keep Graphify Workspace Cockpit as a separate local app/repo for now. UAOS
should reference it as a knowledge source and future spoke, not import its code
or runtime state prematurely.

REQ-0054 confirms the same boundary for relay work: Graphify owns shared
knowledge state, decisions, recommendations, actions, and handoff records.
UAOS relay work owns mission coordination and approval records. Do not put
Graphify graph/recommendation behavior into the relay.

An external video transcript review on 2026-06-14 reinforced one product rule:
when multiple agents, devices, or operating-system surfaces coordinate through
UAOS, they should reference the same project registry and graph snapshot before
approval or execution. That supports the "shared brain" benefit without moving
Graphify's map, Ask, recommendation, or queue responsibilities into UAOS.

### 2. Add A Read-Only Knowledge Adapter Before Broad Execution

UAOS should eventually gain a Graphify knowledge adapter that can:

- read approved graph summaries or exported recommendation records;
- ask graph-backed questions about the workspace;
- link evidence nodes back to files, repos, or docs;
- propose a mission route or request record;
- stop before mutating workspace files.

This adapter should be read-only at first.

### 3. Keep Chunk 16 GitHub Narrow

The next GitHub adapter still makes sense as the first execution spoke because
GitHub readiness has already been proven. But it should not become the general
workspace intelligence layer.

Chunk 16 should stay narrow:

- private repo metadata;
- issues or draft PR records;
- dry-run support;
- policy-gated execution;
- action logging.

Graphify should inform which GitHub work matters later, after a handoff
contract exists.

### 4. Add A Graphify Handoff Contract Before Recommendations Trigger Missions

Before UAOS consumes Graphify recommendations, define the shape of a handoff:

- source graph path or graph snapshot;
- question asked;
- evidence nodes and source locations;
- decision or recommendation ID;
- confidence and risk;
- proposed mission title;
- proposed approval level;
- files/repos in scope;
- explicit non-goals;
- validation hints;
- stop triggers.

### 5. Treat Microsoft 365 As A Future Business Spoke

Adam is building the Microsoft 365 business environment on Windows. UAOS should
expect eventual access to that environment, but it should not assume access now.

Future Microsoft 365 integration should be planned as its own governed spoke:

- SharePoint and OneDrive document libraries;
- Teams channels and conversations;
- Outlook email and calendar;
- Microsoft Lists or Planner;
- business identity, permissions, and data boundaries.

This is higher-risk than local graph reading because it can touch business
documents, external communications, account permissions, and private data. It
needs a separate mission envelope, tool permission matrix update, data
classification review, and likely stronger governance before live access.

## Cockpit Build Timeline And UAOS Integration Gates

The cockpit has completed Chunks 1–8 (local tool, fully functional). The next
three cockpit chunks directly enable UAOS integration:

### Cockpit Chunk 9 — GitHub Packaging + Network Wiring (Active)

What it delivers for UAOS:

- The cockpit becomes installable on any machine in under 15 minutes
- Env-var layer removes hardcoded Linux paths — Windows and hosted installs work
- Docker image means UAOS can reference a stable, runnable cockpit without
  depending on Adam's local machine being on

UAOS dependency: none yet. Continue Chunk 17 evaluation work independently.

### Cockpit Chunk 10 — Network-Ready Deployment (Next)

What it delivers for UAOS:

- API key auth gate — UAOS agents can authenticate to the cockpit API
- HTTPS via Caddy — cockpit API is reachable over a secure channel
- Graph upload API — UAOS can push an updated graph.json to the cockpit
  without SSH access (future: automated graph refresh after graphify update)
- The cockpit becomes a genuine "knowledge spoke" per the device-roles table in
  `cross-device-source-of-truth-foundation.md`

UAOS dependency: after Chunk 10, begin designing the Graphify read-only
knowledge adapter — the first UAOS component that calls the cockpit API.

### Cockpit Chunk 11 — Shared State + Handoff Contract (Appears Complete In Local Graphify Repo)

What it delivers for UAOS:

- The handoff endpoint: `GET /actions?status=executed&format=uaos` — exports
  executed cockpit actions in UAOS mission envelope format; read-only; no
  execution authority
- Shared state backend means decisions made anywhere are visible everywhere —
  a UAOS agent on any machine reads current, consistent decision state
- `created_by` identity on all records — UAOS can filter by who made a decision

UAOS dependency: the Graphify handoff contract appears live in the local
Graphify repo as of the REQ-0052 boundary check. Plan the UAOS knowledge
adapter consumption as a read-only adapter chunk that wraps the REQ-0050
validator and the REQ-0052 `graphify-workspace-cockpit-handoff` connector
profile.

## Handoff Contract Schema

When the cockpit Chunk 11 handoff endpoint is live, the payload shape is:

```json
{
  "schema_version": "1.0",
  "exported_at": "2026-06-14T...",
  "actions": [
    {
      "id": "uuid",
      "source_recommendation_id": "uuid",
      "action_type": "create_note | tag_for_archive",
      "description": "human-readable action description",
      "rec_title": "recommendation title",
      "rec_summary": "2-3 sentence summary from the recommendation card",
      "evidence": ["project-area-id", "..."],
      "confidence": 0.75,
      "risk": "low | medium | high",
      "proposed_action_text": "concrete proposed action from the recommendation",
      "result": {
        "success": true,
        "file_created": "workspace/state/notes/...",
        "message": "Created ..."
      },
      "rollback_note": "To undo: delete ...",
      "approved_at": "iso timestamp",
      "executed_at": "iso timestamp",
      "uaos_mission_hint": {
        "proposed_mission_title": "derived from action description",
        "stop_triggers": [
          "stop before deleting files",
          "stop before external commits",
          "stop before mutating source outside workspace/state/"
        ],
        "approval_level": "A2",
        "files_in_scope": ["evidence nodes that are file paths"],
        "non_goals": ["destructive action", "external service calls"]
      }
    }
  ]
}
```

### UAOS Consumer Validation Requirements

Before a UAOS agent proposes a mission from a handoff record, it must validate:

1. `result.success` is true — only executed actions, not failed ones
2. `confidence` meets the minimum threshold for the mission type (suggest >= 0.6)
3. `risk` is within the current approved mission envelope
4. No `stop_trigger` in `uaos_mission_hint.stop_triggers` would be crossed
5. The `evidence` nodes still exist in the current graph (graph may have changed
   since the recommendation was generated)
6. Adam has not made a conflicting decision about the same target area since
   the action was executed (check `GET /decisions?target_id=<evidence node>`)

A UAOS agent must not propose a mission for a handoff record if any of these
validations fail. It logs the failure reason and stops.

REQ-0050 added the UAOS-side local validator for this shape at
`uaos_agent_spine/graphify_handoff.py`. It accepts safe handoff-shaped records
as dry-run-only `graphify_handoff_read` mission proposals and rejects failed,
low-confidence, stale-evidence, high-risk, execution-shaped, unsafe-scope, or
malformed records with explicit reasons.

REQ-0053 added the UAOS-side live read-only adapter at
`uaos_agent_spine/graphify_adapter.py`. It consumes
`GET /actions?status=executed&format=uaos`, handles optional API-key and ETag
headers, validates the REQ-0052 Graphify connector profile, and delegates every
payload to the REQ-0050 validator. It does not execute Graphify actions,
upload graphs, mutate files, or create UAOS missions automatically.

## Near-Term Build Sequence Change

The active next execution chunk remains Chunk 17: evaluation and safety tests.

Add these planning chunks after Chunk 17:

1. **Cockpit Chunk 10 monitoring** — when cockpit Chunk 10 ships, begin
   designing the Graphify read-only knowledge adapter for UAOS.
2. **Graphify handoff validation prep** — complete in REQ-0050; UAOS can
   validate handoff-shaped records locally before live endpoint access exists.
3. **Graphify handoff contract** (align with cockpit Chunk 11) — define how
   UAOS consumes the handoff endpoint and wire the live payload through the
   REQ-0050 validator.
4. **Graphify read-only knowledge adapter** — UAOS component that reads
   approved graph summaries and evidence; read-only, no file mutation.
5. **Microsoft 365 business environment boundary** — complete in REQ-0051.
   Future M365 access still requires a connector-profile activation chunk
   before live inventory, metadata reads, content reads, communications, writes,
   or admin actions.

## Stop Triggers

Stop for Adam approval before:

- indexing or exposing secret/environment files;
- reading private repos outside an approved graph or selected root;
- mutating files based on a Graphify recommendation;
- executing queued Graphify actions;
- connecting to Microsoft 365 accounts;
- reading email, calendar, Teams, SharePoint, OneDrive, task, List, or tenant
  content;
- sending messages, invites, emails, or external notifications;
- changing Microsoft tenant, Entra, identity, permission, sharing, billing,
  admin, app, or security settings;
- using client or sensitive business data.

## Decision

Graphify Workspace Cockpit becomes the likely knowledge lookup and optimization
spoke for UAOS.

Microsoft 365 becomes a future governed business-environment spoke.

UAOS remains the mission, approval, execution, validation, and learning system
that consumes those spokes only through explicit boundaries.
