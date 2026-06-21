# Domain Language

Document type: shared vocabulary
Audience: project owner, builders, AI coding agents, reviewers, and operators
Purpose: define the terms used consistently across code, docs, tests, UI, prompts, runbooks, and release notes.

## Purpose

This file defines the shared vocabulary for the project.

Important domain terms should be named consistently across labels, database tables, functions, services, tests, docs, prompts, and runbooks.

When a term changes, update this file and the affected code or documentation in the same chunk where practical.

## Terms

| Term | Meaning | Avoid Saying | Code/Docs Usage |
|---|---|---|---|
| Mission envelope | Local structured record of an operator intent, request ID, domain, approval level, data class, and dry-run state. | command blob, task data | `MissionEnvelope`, pathway chunks, future portal mission views. |
| Mission action | One proposed local action inside a mission plan before the policy gate evaluates it. | step, task, tool call | `MissionAction`, mission-spine tests, future evidence views. |
| Policy decision | The result of evaluating a mission action against current Rev 2 boundaries. | approval result, tool result | `PolicyDecision`, permission gate tests, future worker evidence. |
| Stop trigger | A policy reason that turns proposed work into a stop-for-approval record instead of executable behavior. | error, failure, block | `detect_stop_trigger`, tool permission matrix, pathway validation notes. |
| Local no-network | Current execution boundary where mission-spine behavior can validate and store synthetic/local records but cannot call connectors, hosted relay, workers, or production systems. | offline mode, sandbox | Mission spine, architecture, runtime controls, tests. |

## Naming Guidance

Use domain-specific names. A name should explain the responsibility it owns.

Challenge vague names when they hide unclear responsibility:

- `manager`
- `helper`
- `utils`
- `thing`
- `stuff`
- `data`
- `processor`
- `handler`
- `misc`
- `temp`
- `common`
- `general`

Prefer names that point to the actual domain concept, boundary, or behavior.

## Agent Guidance

When terminology is vague or inconsistent, the agent should:

1. Flag the naming issue.
2. Explain the risk to comprehension, tests, prompts, or future changes.
3. Recommend the smallest safe naming improvement.
4. Keep related code, docs, tests, UI, and prompts aligned when the owner accepts the change.

Do not rename broadly just for style. Improve names when the change fits the active chunk or the owner approves the refactor.
