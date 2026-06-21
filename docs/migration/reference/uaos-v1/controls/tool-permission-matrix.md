# Tool Permission Matrix

Created: 2026-06-06T21:28:50-06:00
Last Updated: 2026-06-14T18:46:40-06:00
Status: active control record
Owner: Adam Goodwin

## Purpose

This matrix defines allowed operations, prohibited operations, approval
requirements, and failure behavior for tools a future User AI Operating System
agent may use.

## Default Rule

If a tool operation is not explicitly allowed here, the agent must treat it as
not allowed and stop for Adam approval before execution.

Dry-run or proposal mode is preferred until Chunk 15 proves the local agent
spine and Adam approves any execution mode.

## Tool Matrix

| Tool or class | Purpose | Allowed operations | Prohibited operations | Approval requirements | Failure behavior |
|---|---|---|---|---|---|
| Local repo filesystem | Read/write repo-local docs and future runtime files. | Read repo files; create/update request records, specs, standards, tests, local app files; generate artifacts in approved paths. | Read unrelated repos unless needed and stated; write outside repo; delete user/agent work without explicit instruction; store secrets. | No extra approval for scoped repo work inside active chunk; approval required for destructive changes or sensitive data. | Stop on permission ambiguity; preserve unrelated changes; record recovery notes. |
| Local shell | Run validation and local development commands. | `bash scripts/governance-preflight.sh`, `git diff --check`, local tests/builds, local launch scripts, safe read-only inspections. | Destructive commands, system-level changes, unbounded network scans, printing secrets, modifying account state without adapter controls. | Approval required for destructive/system-wide actions or unexpected risk/cost/data exposure. | Capture command/result; stop if failure implies risk outside the mission envelope. |
| Git | Version control. | Status, diff, log, add scoped files, commit requested work. | Reset hard, checkout/revert unrelated work, rewrite history without explicit request. | Commit allowed when Adam requests commit/push or chunk handoff expects it; destructive Git requires explicit approval. | Stop on mixed unrelated changes that affect the task. |
| GitHub | First external tool adapter. | View private repo metadata; create private issues in `Adamgdwn/user-ai-operating-system` through the Chunk 16 adapter; update issues, create PR/release records, or push commits only after specific chunk approval. | Public repo exposure, unsupported issue arguments, destructive repo settings, deleting repos/issues/releases, exposing secrets, production release promotion without approval. | Dry-run is default. Live issue creation requires explicit mission approval, valid token presence, adapter validation, and action logging. Destructive/public/production actions require explicit approval. | Stop on auth, visibility, secret, malformed arguments, unsupported capability, public/destructive risk, or live-approval uncertainty; record issue URLs only after live creation. |
| Graphify Workspace Cockpit / Graphify graph | Knowledge lookup and optimization spoke. | Read approved graph summaries, evidence nodes, decisions, recommendations, and exported handoff records through the REQ-0053 read-only adapter. REQ-0050 validates handoff-shaped payloads as dry-run-only `graphify_handoff_read` mission proposals. REQ-0052 records the read-only Graphify connector profile. Major UAOS turns should check this boundary before duplicating knowledge-spoke behavior. | Mutate source files, execute queued actions, index secrets, read unapproved roots, call live Graphify APIs outside the approved read-only handoff adapter, upload graphs, or treat recommendations as execution approval. | No extra approval for local read-only approved graph/handoff validation or the REQ-0053 handoff endpoint read. Approval required before file mutation, shared-state expansion, graph upload, or action execution. | Stop if graph source, selected root, evidence sensitivity, recommendation/action boundary, adapter scope, or UAOS/Graphify ownership is unclear. |
| Microsoft 365 business environment | Future business workspace spoke for Entra, SharePoint, OneDrive, Teams, Outlook, calendar, Planner/To Do, Lists, documents, and operational records. | Planning-only boundary is defined in `docs/specs/microsoft-365-business-environment-boundary.md`; future inventory-only profile may be approved in a later chunk. | Reading email/calendar/Teams/SharePoint/OneDrive content, sending or posting messages, creating calendar/task/file records, syncing or indexing content, changing tenant/account/security/billing/admin/permission/sharing settings, or accessing client/sensitive data before approval. | Explicit Adam approval, connector profile, updated data classification, retention/audit rule, and tool permission update required before any live M365 access; stronger governance review before confidential/client data, communications, writes, or admin surfaces. | Stop on auth, privacy, identity, tenant, communication, content-read, retention, sharing, client-data, admin, or permission ambiguity. |
| Connector registry / future client stacks | Inventory for GitHub, Graphify, Microsoft 365, local OSes, AWS, Dropbox, BYOK model providers, and client-approved systems. | Define and locally validate connector profiles, owners, allowed capabilities, data classes, approval gates, retention, audit needs, maturity, and failure behavior through `uaos_agent_spine/connector_registry.py`. | Treat registry entries as live access, enable connectors without a boundary, or use client-stack data before approval. | Guided AI Labs governance review required before any client-data, live connector, BYOK, or write-capable profile moves beyond planning. | Stop if owner, tenant/workspace, data class, retention, or approval gate is unclear. |
| Relay envelopes / cross-device cockpit records | Future phone, tablet, browser, Windows, and Linux coordination records. | Locally validate `RelayEnvelope` records with project, graph snapshot, request, mission, actor, device, approval, connector, stop-trigger, and observed-state references; persist validated records and trusted-worker claim attempts through `uaos_agent_spine/relay_store.py`. | Raw secrets, raw credentials, raw logs, raw audio, client-data-full payloads, unrestricted filesystem access, live connector sessions, inbound worker exposure, stale approvals, Graphify execution, phone/tablet live-action approval, or multiple accepted worker claims for one mission. | No extra approval for local no-network validation or local record/claim proof. Explicit approval and updated controls are required before hosted relay, phone UI write authority, persistent worker polling, live connector activation, Client Gateway data flow, production action, or external communication. | Stop on stale state, superseded or conflicting records, unknown devices, unknown connector profiles, unsafe summaries, inbound worker mode, duplicate worker claim, M365 beyond planning-only, or Client Gateway full-assessment ambiguity. |
| Local operating-system surfaces | Future cross-platform workstation, desktop, and mobile control surfaces. | Use approved launchers, local proof apps, local shell validation, and OS-specific setup notes inside approved scopes. | System-wide changes, credential extraction, unapproved background services, or reading unrelated local folders. | Approval required for persistent services, system settings, privileged operations, or broad filesystem access. | Stop on privilege, persistence, filesystem, or credential ambiguity. |
| AWS | Future infrastructure or client-stack connector. | Planning-only connector profiles until a concrete internal or client need is approved. | Reading accounts, changing infrastructure, creating paid resources, changing IAM/security/billing, or accessing client data before approval. | Explicit approval, connector profile, least-privilege scope, logging, and rollback plan required before live access. | Stop on cost, IAM, production, region, data, or reversibility ambiguity. |
| Dropbox / document storage | Future document and storage connector. | Planning-only connector profiles until a concrete workspace and data boundary are approved. | Reading private files, syncing/indexing client documents, changing sharing, deleting files, or retaining restricted data before approval. | Explicit approval and connector profile required before read access; stronger approval for sharing or writes. | Stop on sharing, ownership, retention, client-data, or sensitivity ambiguity. |
| Voice intake / transcription | Future voice-first intake surface. | Planning-only; future approved capture may retain transcript and structured fields by default. | Retain raw audio, transcribe unapproved client data, create client-visible findings, or use voice without consent/boundary record. | Explicit approval required for raw audio retention; Guided AI Labs review required before transcript-derived findings become client-visible. | Stop on consent, retention, speaker identity, workspace, or data-class ambiguity. |
| Client Gateway assessment workspace | Future isolated workspace for full client-data assessment. | Planning-only and local readiness validation through `uaos_agent_spine/connector_registry.py` until scope, identity, roles, retention, connector profiles, and governance review exist. | Create workspaces automatically from public intake, expose unreviewed AI findings, mix clients, retain raw audio by default, or connect live systems before boundary setup. | Guided AI Labs governance approval required before live client-data assessment. | Stop on client identity, workspace isolation, connector approval, retention, public-intake sensitivity, raw-audio retention, or visibility ambiguity. |
| Browser verification | Validate local or preview UI. | Open local app, inspect screenshots, run smoke checks, record non-sensitive results. | Capture sensitive data; interact with client/private accounts unless approved. | No extra approval for local proof app; approval required for sensitive/private targets. | Record viewport/result; stop if page reveals sensitive data unexpectedly. |
| Deployment providers | Preview or deployment proof. | Presence checks and future preview deployment only after a dedicated chunk defines provider and target. | Production launch, DNS/domain changes, unexpected paid resources, destructive deployment/project actions. | Explicit approval for production, DNS, public client/customer launch, cost/risk changes. | Stop on unexpected cost, policy, data exposure, or irreversible operation. |
| Vendor/account APIs | Future vendor, billing, messaging, database, or business APIs. | Presence-only credential checks and dry-run planning until live controls exist. | Live billing/payment changes, external messages, client data access, account ownership changes, destructive resource changes. | Explicit approval and updated governance required before live account/API actions. | Stop on material risk, cost, data exposure, or policy issue. |

## Action Risk Tiers

| Tier | Action type | Current runtime posture |
|---|---|---|
| Tier 0 | Read-only, low sensitivity | Allowed with logging. |
| Tier 1 | Read private repo or internal docs | Allowed only when relevant to active chunk; log source. |
| Tier 2 | Draft action or proposed file/tool change | Allowed; user review before execution where risk warrants. |
| Tier 3 | External reversible action | Requires permission check, action log, and recovery note. |
| Tier 4 | Destructive or production action | Stop for explicit Adam approval. |
| Tier 5 | Irreversible/high-stakes action | Human decision required; agent may assist only. |

## Required Tool Adapter Behavior

Every future adapter must:

- validate arguments before calls;
- support dry-run where practical;
- log action summary, target, result, and stop reason;
- avoid logging secret values, including values nested inside arguments, summaries, results, and validation fields;
- map failures to retry, stop, or rollback/recovery notes;
- expose user-visible summaries before and after execution.
