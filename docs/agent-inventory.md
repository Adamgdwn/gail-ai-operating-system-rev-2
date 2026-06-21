# Agent Inventory

Created: 2026-06-21T14:42:00-06:00
Last Updated: 2026-06-21T14:46:16-06:00
Status: active control
Owner: Adam Goodwin

## Purpose

This inventory records the agent-like roles currently recognized by GAIL AI
Operating System Rev 2 and their allowed autonomy.

It does not activate a production agent, a background worker, a hosted relay, a
live connector, or any client-data workflow. Any role not listed here is not
approved.

## Current Rule

The only active autonomy level is `A1`: human-directed planning, drafting,
local repository work, and validation inside the active chunk.

Agents may assist with local docs, code, validation, and chunk closeout under
the tool permission matrix. They may not independently execute business-system
actions, connector calls, production changes, account changes, money movement,
client-data handling, or destructive operations.

## Agent Roles

| Agent ID | Name | Role | Status | Autonomy | Allowed now | Blocked until later approval |
|---|---|---|---|---|---|---|
| AG-001 | Codex repo collaborator | Human-directed coding and documentation agent for this Rev 2 repository. | Active for this workspace | A1 | Inspect scoped repo files, edit active docs/code in approved chunks, run local validation, commit and push chunk work under `AGENTS.md`. | Autonomous runtime loops, live connectors, secrets, client data, production operations, destructive actions, or work outside the active chunk. |
| AG-002 | Rev 2 local runtime agent | Future deterministic local mission runtime. | Not active | A1 design target | Planning and control documentation only. | Code migration, mission execution, worker polling, connector calls, and persistent services. |
| AG-003 | Windows worker | Future trusted worker on the Windows operator workspace. | Not active | A1/A2 future review | Architecture and bootstrap planning only. | Background service, local tool execution from relay records, persistent polling, or live connector use. |
| AG-004 | Linux worker | Future trusted worker clone that pulls from the private GitHub source of truth. | Not active | A1/A2 future review | Architecture and bootstrap planning only; copied v1 references may inform design. | Treating Linux as source of truth, tunnel-dependent operation, background service, or Rev 1 implementation. |
| AG-005 | Android cockpit | Future phone/tablet operator surface for intent, approval, status, and evidence. | Not active | Human approval surface, not an autonomous agent | Planning only. | Local execution, raw secret/log/audio display, stale approval reuse, or direct connector access. |
| AG-006 | Browser command center | Future shared browser portal across desktop and mobile. | Not active | Human approval surface, not an autonomous agent | Planning only. | Becoming a second source of truth, bypassing worker permissions, hosted auth, or production deployment. |
| AG-007 | Graphify knowledge spoke | Future graph-backed context and routing aid. | Not active in Rev 2 runtime | Read-only knowledge spoke | Use only when available and when policy calls for graph-aided orientation. | Treating recommendations as execution approval, indexing secrets, or mutating source. |

## Explicit Non-Approvals

- No active production agent exists.
- No active live connector agent exists.
- No active client-data agent exists.
- No active Microsoft 365, QuickBooks, billing, payment, vendor, deployment, or
  hosted-relay agent exists.
- No agent may raise its own autonomy level.

## Promotion Notes

This inventory replaces the scaffold example row and aligns with
`project-control.yaml`, `docs/tool-permission-matrix.md`, and
`docs/agent-runtime-instructions.md`.
