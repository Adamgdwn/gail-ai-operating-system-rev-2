# Agent Runtime Instructions

Created: 2026-06-21T14:42:00-06:00
Last Updated: 2026-06-21T14:46:16-06:00
Status: active control
Owner: Adam Goodwin

## Purpose

These instructions define the current Rev 2 runtime posture for agent-like work.

They promote the useful stop rules from the copied UAOS v1 runtime reference
into a Rev 2 control without migrating the v1 mission spine, enabling a live
runtime, activating connectors, or starting worker polling.

## Current Runtime Scope

The current runtime is documentation, planning, local repository editing, local
validation, and Git/GitHub chunk closeout under human direction.

Allowed now:

- convert Adam's current request into one bounded work chunk;
- inspect scoped Rev 2 repository files and copied v1 reference docs;
- update active controls, specs, requests, code, or tests only when the chunk
  calls for it;
- run local validation and safe read-only inspection commands;
- commit and push scoped chunk changes under the closeout protocol;
- record validation, stop reasons, and handoff notes in durable docs.

Not allowed now:

- run an autonomous mission loop;
- poll relay records or execute worker claims;
- call live Microsoft 365, QuickBooks, accounting, finance, billing, vendor,
  deployment, client, or third-party business systems;
- read or summarize live business-system content;
- access client data;
- expose, store, print, summarize, or commit secrets, raw credentials, raw logs,
  raw audio, or unredacted sensitive payloads;
- launch persistent services, hosted relay endpoints, public ingress, or
  production deployment;
- perform destructive, public, payment, account, tenant, permission, or
  production actions.

## Autonomy

Rev 2 is currently `A1`.

`A1` means the agent may plan, draft, edit local repo files inside scope, run
local checks, and summarize results while Adam remains the decision maker.

The agent may not raise its own autonomy level. Any future `A2` or higher
behavior requires an explicit owner-approved control update, tests, logging,
approval gates, and a rollback or disable path.

## Planning And Execution Separation

Planning may produce proposed actions, draft files, validation commands, and
handoff notes.

Execution is limited to local repository work and validation already allowed by
the tool permission matrix. Any proposed external, destructive, production,
client-data, money, tenant, account, permission, or live connector action must
stop before the action and wait for explicit approval plus updated controls.

## Stale-State Rules

Before acting, a runtime or agent must re-check:

- current user request;
- `git status --short`;
- active chunk status in `docs/current-build-pathway.md`;
- relevant permission boundary in `docs/tool-permission-matrix.md`;
- source-of-truth routing in `docs/source-of-truth-map.md` when source or device
  roles matter.

Future relay, portal, or worker approvals must also include freshness checks for
record version, timestamp, approver identity, worker identity, and claim status
before execution.

## Stop Behavior

Stop before any action when:

- the action is not explicitly allowed by the tool permission matrix;
- requested data class, account, tenant, connector, or target is unclear;
- an approval record is stale, missing, duplicated, or ambiguous;
- a secret or sensitive payload appears in a command, file, log, prompt, or
  output path;
- unrelated dirty work affects the same files or target;
- validation fails in a way that changes risk or scope;
- a copied v1 reference conflicts with active Rev 2 controls;
- the task would start code migration, worker execution, hosted relay,
  connector activation, or production work outside the current chunk.

When stopping, record the stop reason in the active pathway, request record, or
handoff if the stop affects future work.

## Evidence And Logging

For current Rev 2 work, evidence is:

- validation command output summarized in `docs/current-build-pathway.md`;
- changed files visible in Git diffs;
- committed and pushed chunk records;
- source inventory and source-of-truth updates when controls are promoted.

Logs and evidence must be safe summaries. Do not include secret values,
unredacted sensitive payloads, raw client data, raw logs, or raw audio.

## Future Runtime Requirements

Before any executable runtime or worker is promoted, the repo must have:

- active architecture specs;
- migration decision records;
- model and prompt route approval;
- runtime input/output schemas;
- permission gate tests;
- stale approval tests;
- safe logging and redaction tests;
- dry-run mode where practical;
- disable or rollback procedure;
- explicit connector and data-class boundaries.

## Promotion Notes

This file is rewritten from the reference posture in
`docs/migration/reference/uaos-v1/controls/agent-runtime-instructions.md`.
The v1 file remains reference-only and does not grant Rev 2 runtime authority.
