# Local Mission Agent Runtime Instructions

Created: 2026-06-06T22:31:12-06:00
Status: active control record
Owner: Adam Goodwin

## Purpose

These instructions govern the Chunk 15 deterministic local mission spine in
`uaos_agent_spine/`.

The runtime exists to prove the control loop before model routes, broader live
tool adapters, external account actions, or production deployment are added.
Chunk 16 added a narrow GitHub issue adapter foundation behind the policy gate.
Chunk 17 added safety evaluations for stop triggers, connector boundaries,
Graphify action boundaries, reviewed output, raw voice retention, and recursive
log redaction.
REQ-0050 added a no-network Graphify handoff validator that can turn safe
handoff-shaped records into dry-run-only mission proposals.
REQ-0051 added the Microsoft 365 business-environment boundary and explicit
stop triggers for M365 live content reads, Outlook/Teams communications, and
tenant, Entra, admin, security, sharing, billing, app, or permission changes.
REQ-0052 added local connector-profile and Client Gateway readiness validation
plus a stop trigger for premature Client Gateway workspace creation.
REQ-0053 added the live read-only Graphify handoff adapter for
`GET /actions?status=executed&format=uaos`, wrapped around the REQ-0050
validator and REQ-0052 connector profile.

## Runtime Scope

The Local Mission Agent may:

- convert one cockpit command into a structured mission object;
- produce a small deterministic step plan;
- evaluate every proposed action through the permission gate;
- generate a draft request artifact in an approved local output path;
- record action log entries with plan, decision, tool arguments, result,
  validation, and stop reason;
- dry-run tool actions and validation commands.
- dry-run GitHub issue creation through the Chunk 16 adapter;
- validate Graphify handoff-shaped payloads locally and represent accepted
  records as dry-run-only `graphify_handoff_read` mission proposals;
- fetch Graphify handoff records through the REQ-0053 read-only adapter when
  a caller supplies an approved Graphify base URL and optional API key;
- validate connector-profile and Client Gateway readiness records locally
  without enabling live connector access;
- stop on unapproved Graphify action execution, raw voice/audio retention,
  connector access, M365 content reads, M365 communications, M365
  tenant/permission/admin changes, Client Gateway assessment or workspace
  creation, destructive Git, and unreviewed client-visible AI output.

The Local Mission Agent must not:

- call live external APIs unless a narrow adapter, explicit mission approval,
  token presence, argument validation, and action logging are all in place;
- execute a real GitHub, deployment, billing, messaging, vendor, or account
  action;
- expose, store, summarize, print, or commit secret values;
- touch client-controlled data;
- couple this repo to Freedom Engine OS code or runtime state;
- bypass a stop-for-approval trigger.

## Planning And Execution Separation

The deterministic planner proposes actions. The policy gate decides whether
each proposed action may proceed. The dry-run executor records what would
happen and may write local request artifacts or action logs.

Live execution remains off by default. Chunk 16 defines and tests the first
GitHub issue adapter, but the CLI runner still invokes the spine in dry-run
mode. A live GitHub issue action must pass the policy gate with an explicit
approved mission flag before the adapter may call GitHub.

## Stop Behavior

If an action is not explicitly allowed, or if it matches a stop-for-approval
trigger, the runtime must:

1. stop before any tool call;
2. record the stop reason in the action log;
3. return the stop reason to the caller;
4. leave external state unchanged.

## Evidence

Chunk 15 evidence is:

- unit tests in `tests/test_agent_spine.py`;
- generated local draft artifacts under `tmp/agent-spine/`;
- JSON action logs under `tmp/agent-spine/`;
- validation records in `docs/current-build-pathway.md`;
- the request records for REQ-0043, REQ-0047, and REQ-0049;
- safety evaluations in `tests/test_safety_evaluations.py`;
- Graphify handoff validation tests in `tests/test_graphify_handoff.py`;
- connector registry and Client Gateway readiness tests in
  `tests/test_connector_registry.py`;
- Graphify live read-only adapter tests in `tests/test_graphify_adapter.py`;
- request record `docs/requests/REQ-0050-graphify-handoff-read-only-adapter-prep.md`;
- request record `docs/requests/REQ-0051-microsoft-365-business-environment-boundary.md`;
- request record `docs/requests/REQ-0052-connector-registry-client-gateway-boundary.md`;
- request record `docs/requests/REQ-0053-graphify-handoff-live-read-only-adapter.md`.
