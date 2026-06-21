# Cross-Device Source Of Truth Foundation

Created: 2026-06-14T11:30:50-06:00
Last Updated: 2026-06-14T16:44:31-06:00
Status: active architecture note
Owner: Adam Goodwin

## Purpose

Guided AI Labs will operate across multiple builds, laptops, operating systems,
and device types. UAOS must therefore become a company-wide source-of-truth
spine, not a single-machine project that only works from the current Linux
workspace.

This note defines the baseline wiring assumptions for future Android tablet,
Windows laptop, Linux workstation, hosted relay, Microsoft 365, Graphify, and
client/workspace integrations.

No live sync service, mobile app, Microsoft 365 access, or production relay is
implemented by this note.

## Core Principle

The source of truth is not a device.

The durable source of truth is the governed record set:

- private GitHub repo and commit history;
- request records in `docs/requests/`;
- the active dashboard in `docs/current-build-pathway.md`;
- source routing in `START_HERE.md`, `docs/source-of-truth-map.md`, and
  `docs/context-map.md`;
- control records for models, tools, prompts, evaluations, risks, and runtime
  instructions;
- reviewed artifacts promoted through the learning and governance process.

Devices are access points, workers, viewers, approval surfaces, or execution
surfaces. They must not become competing truth islands.

## Device Roles

| Role | Examples | Allowed purpose | Boundary |
|---|---|---|---|
| Trusted worker | Linux workstation, future Windows laptop build machine | Clone repo, run local tests, execute approved local/tool-adapter work, generate action logs. | Must preserve repo controls, secret boundaries, and stop triggers. |
| Operator cockpit | Android tablet, phone, laptop browser, future portal | Capture intent, review status, approve/pause/redirect missions, inspect evidence summaries. | Must not receive unrestricted secrets, raw credentials, or unredacted sensitive logs. |
| Business workspace | Microsoft 365 on Windows/web/mobile | Documents, calendar/tasks planning, SharePoint/OneDrive/Teams/Outlook surfaces after boundary approval. | Planning-only until M365 permission boundary exists. |
| Knowledge spoke | Graphify Workspace Cockpit | Workspace lookup, graph evidence, recommendations, and handoff records. | Read-only until handoff contract exists; recommendations are not execution approval. |
| Client workspace | Future Client Gateway | Scoped client assessment and delivery workspace after roles, retention, approvals, and connector profiles exist. | Isolated per client; no public-intake full client data. |

## Sync And Orchestration Rules

- `main` on the private GitHub repo is the current canonical code/doc spine.
- Each device or worker should pull before work, check `git status`, and avoid
  editing from stale state.
- Meaningful work must produce a request record or dashboard update before it
  is treated as durable.
- Local generated files, temp logs, credentials, and machine-specific state stay
  local unless explicitly promoted through a governed artifact path.
- Future hosted relay or portal state must reference durable request IDs,
  mission IDs, action-log IDs, commit SHAs, issue/PR IDs, and connector profile
  IDs rather than inventing a second source of truth.
- Conflicts resolve toward the latest reviewed durable record, not whichever
  device wrote last.
- Offline capture can exist, but it remains draft until reconciled into the
  governed repo or approved workspace.

## Cross-Platform Bootstrap Contract

Every new build surface should be able to answer:

1. Which repo, branch, and commit am I on?
2. Which device role am I playing?
3. Which source-of-truth docs should I load first?
4. Which tools/connectors are present, absent, or planning-only on this device?
5. Which secrets are present by name only, without printing values?
6. Which approval level and stop triggers apply?
7. Where will action logs, evidence, and handoff records land?
8. How do I disable, disconnect, or recover this device if it drifts?

The first cross-platform bootstrap reads are:

- `START_HERE.md`;
- `docs/context-map.md`;
- `docs/source-of-truth-map.md`;
- `docs/current-build-pathway.md`;
- `docs/tool-permission-matrix.md`;
- this file.

## Identity And Access Direction

- Adam remains the initial owner and governance authority.
- Guided AI Labs personnel may become role-based reviewers, operators, and
  approvers later.
- Microsoft 365 / Entra is the likely business identity boundary, but no live
  access is approved yet.
- Local workstation credentials remain local. Future shared services should use
  least-privilege device/session identity rather than copying broad local
  credentials across devices.
- Device trust, session expiry, remote disable, and audit trails must be
  designed before a phone/tablet/portal can approve live actions.

## Future Relay Implications

Chunk 18 must design the shared relay/control plane as a coordination layer,
not a new truth store.

REQ-0054 completed that Chunk 18 design in
`docs/specs/shared-relay-phone-cockpit-architecture.md`. It chooses
GitHub-backed interim relay records as the first prototype path and requires a
local no-network relay envelope validator before hosted relay or phone UI work.

The relay may carry:

- mission state;
- approval prompts and decisions;
- action status;
- evidence summaries;
- links to durable logs/artifacts;
- paused/resumed state;
- operator comments.

The relay must not become the only place where decisions, validation, or
client/workspace boundaries live. Durable state must reconcile back to the
governed source-of-truth spine.

## Non-Goals For This Chunk

- No live Android app.
- No Windows service.
- No Microsoft 365 connector.
- No hosted relay.
- No cross-device secret sync.
- No client workspace creation.
- No production deployment.
- No governance-level change.

## Acceptance Standard For Future Device Work

A future cross-device or company-wide UAOS feature is not ready until it
defines:

- device role;
- identity/session boundary;
- source-of-truth read/write path;
- offline/draft behavior;
- sync and conflict behavior;
- logging and evidence path;
- connector profile dependencies;
- stop triggers;
- disable/recovery path;
- validation scenario across at least two device classes.
