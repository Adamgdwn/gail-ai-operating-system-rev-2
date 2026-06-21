# Prompt Register

Created: 2026-06-21T14:42:00-06:00
Last Updated: 2026-06-21T14:46:16-06:00
Status: active control
Owner: Adam Goodwin

## Purpose

This register identifies the active prompt and instruction sources that govern
GAIL AI Operating System Rev 2 work.

It does not store secrets, model credentials, raw client content, raw logs, raw
audio, or provider-specific hidden instructions.

## Current Prompt Posture

The active prompt surface is the human-directed coding session plus the
repository instruction files listed below.

There is no approved production runtime prompt, connector-driving prompt,
client-data prompt, hosted relay prompt, or autonomous worker prompt yet.

## Registered Instruction Sources

| Prompt or instruction ID | Applies to | Status | Purpose | Current version | Change control |
|---|---|---|---|---|---|
| PR-001 | Repo collaborator agents | Active | `AGENTS.md` defines repo-local startup, governance triggers, Graphify policy, context hygiene, and chunk closeout. | 2026-06-21 repo version | Update only when repo operating rules change; validate with the active pathway. |
| PR-002 | Material work sessions | Active | `START_HERE.md` routes current priorities, stop triggers, and the active pathway. | 2026-06-21 repo version | Update only when top-level plan or handoff point changes. |
| PR-003 | Build pathway sessions | Active | `docs/current-build-pathway.md` defines chunk packets, validation evidence, completion labels, and handoff. | 2026-06-21 repo version | Update every active chunk when status, validation, or next handoff changes. |
| PR-004 | Tool and connector behavior | Active | `docs/tool-permission-matrix.md` defines allowed and blocked tools, devices, workers, and connector actions. | 2026-06-21T14:16:18-06:00 | Update before any new tool, connector, worker, or action class is allowed. |
| PR-005 | Runtime and agent behavior | Active | `docs/agent-runtime-instructions.md` defines Rev 2 A1 runtime posture, planning/execution separation, stale-state behavior, and stop rules. | 2026-06-21T14:46:16-06:00 | Update before code migration creates an executable runtime or worker. |
| PR-006 | Source routing | Active | `docs/source-of-truth-map.md` defines active controls, reference-only material, device roles, and source-of-truth boundaries. | 2026-06-21T14:46:16-06:00 | Update when a control is promoted or a device/source role changes. |
| PR-007 | System/developer instructions outside the repo | Runtime context only | Higher-priority session instructions from the active assistant environment. | Current session | Do not copy hidden or provider-managed instructions into the repo; summarize only durable repo-relevant effects when needed. |

## Future Prompt Approval Requirements

A future runtime prompt must record:

- owning agent or surface;
- purpose and non-goals;
- allowed tools;
- allowed data classes;
- prohibited data classes;
- model route;
- prompt-injection and instruction-priority behavior;
- evaluation or test expectations;
- approval and review trigger;
- rollback or disable path.

## Promotion Notes

This register replaces the scaffold example row and records active instruction
sources without approving a production prompt route.
