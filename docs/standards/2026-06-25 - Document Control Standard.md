# Document Control Standard

Document type: standard
Date: 2026-06-25
Saved: 2026-06-25T09:18:39-06:00
Last Updated: 2026-06-25T10:31:18-06:00
Status: active
Owner: Adam Goodwin
Audience: coding agents, human coders, reviewers, and project owners

## Purpose

This standard keeps durable documents easy to identify, sort, and compare
across GAIL AI Operating System Rev 2, Freedom, AG Operations Workspace, and
future Guided AI Labs builds.

The owner requirement is simple: newly saved durable documents should carry the
date in the filename so current work is easier to track.

## Core Rule

New durable documents and work-tracking records saved after 2026-06-25 should
use this filename pattern:

```text
YYYY-MM-DD - <clear-title>.md
```

Use the date the document is first saved, promoted, or accepted as a durable
record. Later edits should update internal metadata such as `Last Updated` or a
validation log; do not rename the file on every edit.

Examples:

- `2026-06-25 - Document Control Standard.md`
- `2026-06-25 - AG Operations Consolidation Review Packet.md`
- `2026-06-25 - Freedom Bridge Boundary Review.md`

## Applies To

Use date-prefixed names for newly authored:

- decision records;
- work packets;
- handoffs;
- build plans;
- pathway supplements;
- review packets;
- audits;
- implementation notes;
- runbooks that are not stable required routes;
- cross-build coordination records;
- AG Operations, Freedom, or Rev 2 work-tracking notes.

This applies especially to records that might be compared across multiple
active builds.

## Stable-Path Exceptions

Some files should keep stable names because agents, tools, templates, or humans
route to them directly.

Stable-path files may keep their current names, including:

- `README.md`;
- `START_HERE.md`;
- `AGENTS.md`;
- `CARRY_FORWARD.md`;
- `project-control.yaml`;
- `docs/current-build-pathway.md`;
- `docs/context-map.md`;
- `docs/source-of-truth-map.md`;
- required standards, runbooks, manuals, roadmaps, and registries that already
  have stable paths;
- schema-bound, generated, or tool-owned files.

When a stable-path file needs a dated decision trail, create a dated companion
record instead of renaming the stable route.

## Dependency And Tooling Safety

This standard must not interfere with dependency resolution, imports, build
tools, generated artifacts, package managers, or external integrations.

Do not date-prefix files whose names are part of a tool contract, dependency
graph, import path, package identity, schema lookup, CI workflow, runtime
configuration, or generated-output convention.

Keep stable names for dependency and tooling files such as:

- `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`;
- `pyproject.toml`, `requirements.txt`, `uv.lock`, `poetry.lock`;
- `tsconfig.json`, `vite.config.ts`, `eslint.config.js`, `vitest.config.ts`;
- `.github/workflows/*.yml`;
- `.env.example` and other safe template files;
- source files imported by name or module path;
- schema files, generated files, manifests, and tool-owned config files.

If a dependency, package, schema, generated file, or tool config needs a dated
history note, create a separate dated companion document. Do not rename the
tool-facing file.

## Cross-Build Rule

When working across GAIL AI Operating System Rev 2, Freedom, and AG Operations
Workspace, use the same naming convention for new durable records unless the
target repo already has a stronger local rule.

Do not rename existing documents in another build just to satisfy this standard
without a bounded rename plan that updates links, startup routes, references,
and validation.

## Internal Metadata

Durable Markdown records should include enough metadata for future readers to
know what they are looking at. Prefer:

```md
Date: YYYY-MM-DD
Saved: YYYY-MM-DDTHH:MM:SS-06:00
Last Updated: YYYY-MM-DDTHH:MM:SS-06:00
Status: draft | active | superseded | archived
Owner: <name>
```

Use only the fields that fit the document. For stable route files, `Last
Updated` may be enough when the filename cannot change.

## Migration Posture

Do not bulk-rename existing docs during ordinary work.

Rename existing documents only when:

- the owner explicitly approves the rename;
- the rename has a bounded scope;
- all references are updated;
- validation checks pass;
- the active pathway records the change.

For now, prefer applying this rule to new documents and new work-tracking
records. Existing required docs can keep stable names.
