# 2026-06-28 — R4 Charter Doctrine and First Internal Autonomy Candidate

**Status:** Draft — pending Adam approval signature (see §6)
**Phase:** Phase 6 — R4 Autonomy
**Chunk:** 6.0 (docs-only, cloud-safe)
**Unblocks:** Chunk 6.1 (CharterProfile Schema)

---

## 1. Authority Level Ladder Summary

The CNS uses a six-level authority ladder (R0–R5) to classify every action, connector, and decision by who or what may initiate it.

| Level | Name | Who may act | Examples |
|---|---|---|---|
| R0 | Read / Observe | Any agent, any connector | Read graph, read OKPs, read M365 tasks |
| R1 | Internal Read (trusted) | Credentialed CNS agents | Read restricted OKP fields, read internal missions |
| R2 | Internal Write | GAIL OS (dry-run or scoped) | Create Planner task (dry-run), save EvidencePacket |
| R3 | External Write (approval required) | GAIL OS with per-action confirmation | Send email, post Teams message |
| R4 | Delegated Autonomous Action | GAIL OS under a pre-approved charter | Stale-claim review, calendar maintenance |
| R5 | Human-Only Decision | Adam Goodwin only | Entra app registration, charter grant, authority escalation |

R0–R3 require evidence but not a charter. **R4 requires a charter.** R5 cannot be executed by any agent under any charter.

---

## 2. R4 — Delegated Autonomous Action

**R4 is the authority level at which GAIL OS may initiate and complete a class of actions autonomously, without a per-action human approval, as long as all of the following hold:**

1. A valid `CharterProfile` exists that covers the action class.
2. The action falls within the charter's `allowed_action_types` and `target_resources`.
3. The charter has not expired.
4. No stop condition has been triggered.
5. The agent has not exceeded `max_actions` for the charter session.
6. A rollback path exists and has been verified pre-execution.
7. Every action is evidenced at the time it executes — evidence is not deferred.
8. The charter was granted by Adam Goodwin (R5) in writing before execution.

R4 is **not** a general-purpose autonomous mode. It is a narrow pre-authorization for a specific, bounded action class on named resources. Each R4 charter must be auditable: at any point Adam can read the evidence log and understand exactly what the CNS did, why, and how to reverse it.

### 2.1 R4 Requirements Checklist (per charter)

Every R4 charter must define all of the following before it may be activated:

| Field | Requirement |
|---|---|
| `charter_id` | Unique identifier, `charter-` prefix |
| `title` | Human-readable name |
| `authority_level` | Must be exactly `R4` — cannot exceed R4 |
| `autonomy_level` | A-level classification for the action class |
| `allowed_action_types` | Closed list of permitted operations |
| `target_resources` | Named specific resources (not wildcard) |
| `connector_scope` | Which connectors may be invoked |
| `agent_scope` | Which agents may act under this charter |
| `max_actions` | Hard ceiling on actions per session (no unbounded charters) |
| `expiry` | Datetime; cannot be in the past; required for R4 |
| `stop_conditions` | Non-empty list; any triggered condition halts execution immediately |
| `rollback_path` | Non-empty string describing exactly how to reverse actions taken |
| `review_cadence` | How often Adam reviews the charter and its evidence log |
| `evidence_requirements` | What must be logged per action (evidence is mandatory) |

A charter missing any required R4 field is invalid and must not be activated.

---

## 3. R5 — Human-Only Decision

R5 actions cannot be delegated to any agent, model, or charter. No `CharterProfile` may grant R5 authority. Attempting to create a charter with `authority_level == R5` is a validation error.

R5 actions include:
- Granting, modifying, or revoking charters
- Changing authority or autonomy levels on any record
- Entra app registration and permission changes
- Any action affecting tenant-level identity, authentication, or secrets
- Production deployments to customer-facing services
- Approving actions that were flagged by a stop condition

R5 is always and only: Adam Goodwin acting directly.

---

## 4. First R4 Candidate — R4-001: Graphify Stale Claim Review Charter

### 4.1 Purpose

The Graphify CNS graph accumulates OKP nodes over time. Some of those nodes represent claims about the state of systems (active connectors, open missions, pending actions) that may have become stale — the underlying reality has changed but the graph node has not been updated. The Stale Claim Review Charter authorizes GAIL OS to identify and flag these nodes for human review, without deleting them or taking write action against external systems.

This is the **minimum viable first R4 action**: internal only, reversible, evidenced, and scoped to the Graphify graph.

### 4.2 Charter Profile — R4-001

```
charter_id:           charter-r4-001
title:                Graphify Stale Claim Review
authority_level:      R4
autonomy_level:       A3
allowed_action_types:
  - graphify.node.read
  - graphify.node.status_update (review_required only)
  - evidence.create
  - okp.create (type=review_required)
  - freedom.report (read-only summary)
target_resources:
  - graphify-workspace-cockpit CNS SQLite store
  - OKP nodes where status == "observed" and age > 7 days
  - OKP nodes where status == "accepted" and confidence < 0.4
connector_scope:
  - graphify-http-api (internal, read + status update only)
  - gail-os-evidence-store (write)
  - freedom-briefing-api (write)
agent_scope:
  - GAIL OS (gail-ai-operating-system-rev-2)
max_actions:          25 per session
expiry:               2026-07-12T23:59:59Z (14-day initial authorization)
stop_conditions:
  - Any action would delete a graph node (halt immediately)
  - Any action would modify a client record (halt immediately)
  - Any live M365 call is attempted (halt immediately)
  - Any product repo is accessed (halt immediately)
  - Error rate exceeds 2 consecutive failures (halt and report)
  - Rollback data cannot be written before the action executes (halt)
rollback_path: >
  For each OKP node marked review_required: revert status to its prior value
  using PATCH /api/v1/okp/{okp_id} with the original status field. The original
  status is captured in the evidence packet before the update executes.
  Rollback does not require M365 access. Graphify node deletions are not
  performed under this charter — nothing is irreversible.
review_cadence:       Adam reviews evidence log before charter renewal (before 2026-07-12)
evidence_requirements:
  - okp_id of every node examined
  - original_status before update
  - reason for stale classification (age, confidence, or both)
  - timestamp of action
  - rollback_ref pointing to the evidence packet that contains original_status
```

### 4.3 What R4-001 Is Allowed to Do

- Read OKP nodes from the Graphify CNS store
- Identify nodes that are likely stale by age (> 7 days since observed) or low confidence (< 0.4)
- Set `status = review_required` on those nodes
- Create an EvidencePacket and OKP for each flagged node, capturing the original status
- Produce a Freedom briefing summarizing what was found and flagged
- Produce a rollback manifest so Adam can undo any or all flags in one step

### 4.4 What R4-001 Is Not Allowed to Do

- Delete any graph node or edge
- Modify any client record, CRM entry, or SharePoint list row
- Make any live M365 API call (Graph, Power Automate, SharePoint, Exchange, Teams)
- Alter authority levels or autonomy levels on any record
- Approve, auto-resolve, or close any flagged item
- Suppress, skip, or defer evidence for any action
- Access or modify any product repo (GAI Journey, OldSkoolAI, Bowtie, Change Leadership, EasyDraft, websites)
- Act on any record outside the Graphify CNS store
- Grant, extend, or modify any charter

### 4.5 Execution Gate

R4-001 may not execute until:

1. This doctrine is approved by Adam (§6).
2. Chunk 6.1 (CharterProfile schema and validation) is merged and tests pass.
3. Chunk 6.2 (Graphify charter node type) is merged.
4. Chunk 6.4 (dry-run simulation) completes and produces evidence without errors.
5. Adam explicitly approves transition from simulation to limited execution for Chunk 6.5.

Chunk 6.4 is the mandatory simulation gate. No real mutations may occur until the simulation proves the scope is correct.

---

## 5. Exclusions — Live M365

Live Microsoft 365 writes are excluded from the first R4 charter (R4-001) and from all R4 charters until:

- BLK-005 (Entra app registration) is resolved and `m365 login` is authenticated on Linux.
- A named M365 write scope is selected and approved by Adam.
- An M365-specific charter is defined and simulation passes.

The M365 authority ladder state is currently:

```
pending → proven (CP-4 dry-run complete) → approved (pending) → active (pending)
```

A proven state (dry-run) is not permission for live writes. M365 live writes require `approved` status plus a named charter.

---

## 6. Approval

This document represents the R4 Charter Doctrine for the Guided AI Labs Agentic OS CNS as of 2026-06-28.

**Document approved by:** ________________________________

**Date:** ________________

**Notes / modifications:**

```
(Adam to complete before Chunk 6.1 begins)
```

---

*Built by Linux Claude Code build agent — agentic-multi-agent-agent-builder — Chunk 6.0.*
