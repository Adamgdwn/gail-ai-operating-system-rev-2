# Manual

## What This Project Is

GAIL AI Operating System Rev 2 is the governed technical spine for mission,
policy, relay, approval-record, evidence, worker, and connector-boundary work.
It is currently being coordinated with Freedom and AG Operations Workspace as
related builds, but they are not consolidated. Freedom remains the core
operator interface and high-level agentic business partner surface. AG
Operations Workspace remains the live Microsoft 365 business substrate and
current operating workflow environment.

## How To Work In This Repo

For ordinary scoped work, start lean:

1. Check `git status --short`.
2. Read `START_HERE.md` and the short repo-local agent instructions.
3. Use `docs/context-map.md` to choose only the docs and source areas needed for the task.
4. Review `docs/current-build-pathway.md` for the active chunk, completion target, stop condition, and validation expectations.
5. Run task-relevant validation.

On the next startup, acknowledge the three-repo coordination direction before
opening implementation files. Resume Chunk Twenty only when the user wants Rev
2 local implementation; do not treat the coordination pivot as approval for a
source merge, shared runtime, live connector, or new bridge layer.

For material or risk-triggering work, add the full governance path:

1. Review `docs/standards/README.md`.
2. Review `docs/standards/engineering-governance-by-use-case.md`.
3. Review `docs/policy/durable-development-engineering-policy.md`.
4. Review `docs/standards/ship-ready-engineering-standard.md`.
5. Run `bash scripts/governance-preflight.sh`.
6. Review `project-control.yaml`.
7. Capture a timestamp with `date -Iseconds`.
8. Confirm the current roadmap and runbook still match reality.
9. Update docs when behavior or operating expectations change.

For new durable documents and work-tracking records, follow
`docs/standards/2026-06-25 - Document Control Standard.md`: prefix the filename with the
first durable saved/promoted date, for example
`YYYY-MM-DD - <clear-title>.md`. Later edits update `Last Updated` metadata
instead of renaming the file.

## Expected Outputs

- working code or deliverables
- current operational documentation
- a maintained roadmap
- timestamped build pathway updates for material work
- scoped context and budget notes for meaningful chunks
- reviewable governance records

## Operator Notes

Current handoff: let AG Operations Workspace finish and box its current
evolution, keep Freedom as the operator/business-partner interface, and use
`docs/decisions/2026-06-24 - Build Consolidation Decision Process.md` before
any fold, bridge, shared runtime, connector activation, or source-of-truth
change across the three builds.

Document-control note: apply dated filenames to new durable records across Rev
2, Freedom, and AG Operations Workspace unless a target repo's stable route,
schema, or stronger local rule requires a different name.
