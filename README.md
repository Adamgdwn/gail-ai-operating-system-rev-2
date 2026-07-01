# GAIL AI Operating System Rev 2

## Purpose

Clean rev-two workspace for the Guided AI Labs agentic operating system.

This repo is the governed home for the Rev 2 command center, relay/worker core,
tool directory, connector boundaries, and migration path from the existing UAOS
proof work. It is now being coordinated with Freedom and AG Operations
Workspace as one related build ecosystem, but not consolidated into one repo or
runtime. DirectLink remains a transport/status project; the Linux UAOS repo
remains the v1/reference source until selected material is copied here
deliberately.

## Status

- Owner: Adam Goodwin
- Technical lead: codex session
- Governance level: 1
- Risk tier: low for the initial local scaffold and planning track
- Production status: not production; narrow Azure Container Apps pilot is
  documented, with live connector and production-readiness gates still closed
- Current direction: park Freedom implementation work unless Adam explicitly
  routes there, and use
  `docs/decisions/2026-06-29 - Graphify Boundary Transfer And GAIL OS Informing Plan.md`
  for the active GAIL OS Graphify-boundary informing lane

## Quick Start

Prerequisites: install `uv` for Python command execution and Node/npm for the
command-center app. Python dependencies are currently resolved from
`requirements.txt` at command time rather than from a pinned lockfile.

```powershell
cd "C:\Users\adamg\01. Code Projects\GAIL AI Operating System Rev 2"
uv run --with-requirements requirements.txt python -m pytest -q
uv run --with-requirements requirements.txt python scripts/export-cp1-contracts.py --verbose
npm --prefix apps/command-center ci
npm --prefix apps/command-center run build
git status --short
```

`python -m unittest discover -s tests` is a historical partial check, not the
current full Python validation gate.

The first executable Rev 2 slice is the local no-network mission spine under
`packages/uaos-core/src/gail_ai_operating_system`. It can create, validate,
plan, policy-check, save, and load local mission records without connector,
portal, worker, hosted relay, or production side effects.

The first browser app shell lives under `apps/command-center`. It is a local
Vite React TypeScript command-center cockpit that renders safe static mission,
approval-boundary, worker-status, evidence, and connector-posture sample
records. It does not activate approval actions, service workers, live
connectors, Freedom runtime access, hosted relay, workers, or production
behavior. Live read-only command-center data is planned for the EX-2 remediation
track and is not present in this first-run app shell.

Do not connect live Microsoft 365, QuickBooks, finance, billing, client,
or third-party account systems from this workspace until a later approved
connector activation chunk exists.

Next startup should acknowledge the coordination posture before implementation:
Freedom remains the core operator interface and high-level agentic business
partner surface, AG Operations Workspace remains the live Microsoft 365
business substrate, Graphify remains relationship intelligence and graph
memory, and Rev 2 remains the governed authority/evidence spine.

## Documentation

New durable documents and work-tracking records should use date-stamped
filenames going forward, such as `YYYY-MM-DD - <title>.md`. Use the first
durable save or promotion date in the filename, then update internal metadata
on later edits. Stable required repo files may keep their existing names unless
a bounded rename plan updates all references.

- `docs/architecture.md`
- `docs/context-map.md`
- `docs/source-of-truth-map.md`
- `docs/current-build-pathway.md`
- `docs/manual.md`
- `docs/roadmap.md`
- `docs/policy/durable-development-engineering-policy.md`
- `docs/standards/README.md`
- `docs/standards/2026-06-25 - Document Control Standard.md`
- `docs/standards/engineering-governance-by-use-case.md`
- `docs/standards/ship-ready-engineering-standard.md`
- `docs/standards/context-hygiene-standard.md`
- `docs/deployment-guide.md`
- `docs/runbook.md`
- `docs/CHANGELOG.md`
- `docs/risks/risk-register.md`
- `docs/decisions/2026-06-29 - Graphify Boundary Transfer And GAIL OS Informing Plan.md`

## Support Model

Adam Goodwin owns product and governance decisions. Agents may propose and
implement scoped local changes, but live connectors, sensitive data, money,
client systems, communications, and production-impacting actions stop for
explicit approval.
