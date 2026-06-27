# Authority and Autonomy Ladders

**Last Updated:** 2026-06-26
**Status:** Canonical within the Guided AI Labs Agentic OS (CNS)
**Layer:** GAIL OS — authority and evidence layer

This document is the canonical, in-repo statement of the two governance ladders
for the entire Guided AI Labs Agentic OS CNS: the **R0–R5 authority ladder** and
the **A0–A6 autonomy maturity ladder**. They live here because `gail-ai-operating-system-rev-2`
is the CNS authority and evidence layer — the OS owns authority classification.

> **Source of truth:** These definitions are copied verbatim from
> `agentic-multi-agent-agent-builder/docs/build-control/master-plan-summary.md §4`
> (the master CNS architecture). Do not redefine the levels here; if the master
> architecture changes, update it there first, then mirror the change into this
> file. This file is the in-repo mirror, not a competing definition.

---

## Authority Ladder — R0 to R5

The R-ladder classifies **how much external effect an action may have** and what
approval it requires. Every action is classified to an R-level before it can move
through the action state machine.

| Level | Name | Meaning |
|---:|---|---|
| R0 | Observe | Read-only, no external effect |
| R1 | Propose | Draft, recommend, prepare — no external effect |
| R2 | Internal approved action | Reversible internal write with named approval |
| R3 | Restricted action | External send, production release, irreversible change |
| R4 | Delegated autonomous restricted action | Inside a valid pre-approved authority charter |
| R5 | Blocked / human-only | Agent may analyze only; human decides |

**Boundary rules:**

- No restricted action (R3+) executes without passing through the GAIL OS policy gate.
- **R4 requires a signed AuthorityEnvelope** with an explicit charter, stop conditions,
  rollback path, and review cadence. No R4 without a charter.
- **R5 is human-only.** No agent code may execute an R5 action or bypass this boundary.

---

## Autonomy Maturity Ladder — A0 to A6

The A-ladder describes **how much standing autonomy the system operates with** as a
maturity progression. It is orthogonal to the R-ladder: the R-level classifies a
single action; the A-level describes the operating posture.

| Level | Name | Description |
|---:|---|---|
| A0 | Manual | Human performs the work; system assists with information only |
| A1 | Assisted | System drafts/suggests; human executes every step |
| A2 | Supervised | System acts on individual steps under direct human supervision |
| A3 | Delegated narrow | System runs a narrow, well-scoped task end-to-end with review |
| A4 | Adaptive | System adapts within bounds and handles variation under governance |
| A5 | Self-expanding under strict governance | System proposes and adopts new capability under strict, evidenced governance |
| A6 | Minimal governance | **Future state — NOT current production authority** |

> **A6 is future-state only.** A6 (minimal governance) is an architectural horizon,
> not an authority the system holds today. No part of the current build may operate
> as if A6 is in effect. Current production authority tops out well below A6.

---

## Mandatory Action State Machine

Every governed action moves through this sequence. No stage may be skipped; evidence
is required before an action is considered complete.

```
observed → proposed → classified → approval_requested → approved/rejected
        → claimed → executed/stopped → evidenced → reviewed → learned
```

- **classified** is where the R-level (above) is assigned.
- **approval_requested → approved/rejected** is the GAIL OS policy gate.
- **evidenced** produces the EvidencePacket; an action is not "done" until evidence exists.
- **reviewed → learned** feeds outcomes back to Graphify and Freedom (the CNS learning loop).

---

## Relationship to the CNS

- **Freedom** (executive cognition) may reason (R0/R1) and propose (R2) but must not
  self-approve restricted actions (R3+).
- **GAIL OS** (this repo) owns classification, the policy gate, AuthorityEnvelopes,
  and the evidence ledger — it is where these ladders are enforced.
- **Graphify** (relationship intelligence) provides read-only context; its
  recommendations are mission candidates, not execution approval.

For cross-repo coordination state, see
`agentic-multi-agent-agent-builder/docs/build-control/`.
