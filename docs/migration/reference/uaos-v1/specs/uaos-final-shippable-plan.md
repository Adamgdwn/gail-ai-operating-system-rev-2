# UAOS Final Shippable Plan

Created: 2026-06-14T19:09:41-06:00
Last Updated: 2026-06-14T19:09:41-06:00
Status: active final ship plan
Owner: Adam Goodwin

## Purpose

This plan turns the completed flagship foundation into a bounded path to a
usable User AI Operating System.

The goal is not to keep adding features. The goal is to ship the smallest
complete operating system Adam can safely use from authorized surfaces:
Linux, Windows, browser, Android phone, Android tablet, private GitHub, the
Graphify Workspace Cockpit knowledge spoke, and approved future Microsoft 365
inventory surfaces.

## Finish Line

UAOS v1 is shippable when Adam can:

- open one operating cockpit from an authorized surface;
- enter or review work intent;
- create a governed request or mission envelope;
- use Graphify knowledge handoff without duplicating Graphify's map, chat,
  cluster selection, or recommendation work;
- approve, pause, resume, or reject work from phone/tablet/browser;
- have exactly one trusted Linux or Windows worker claim approved work;
- run approved local worker actions through policy, validation, and action-log
  evidence;
- reconcile request records, relay records, action logs, commit references,
  and handoff records back to the governed source-of-truth spine;
- keep client data, live Microsoft 365 content, live communications, billing,
  destructive changes, raw audio, and production release actions blocked unless
  a separate approved mission explicitly opens that boundary.

Project completion remains Adam's decision. This plan can reach `Release ready`
for UAOS v1, but only Adam can declare the broader project complete.

## Minimum Shippable Scope

### In Scope For UAOS v1

- Local mission spine and policy gate.
- GitHub-backed source-of-truth records and private repo workflow.
- Graphify handoff read-only consumption as mission candidates.
- Local relay envelope, record store, status history, and single-worker claim.
- One global operating cockpit surface that is usable from desktop browser and
  mobile/tablet browser.
- Trusted worker bootstrap for Linux and Windows.
- Phone/tablet approval, pause/resume, status, and evidence summary.
- Explicit connector registry and Client Gateway stop gates.
- M365 inventory-only planning path, activated only if Adam approves that chunk.
- Ship-readiness evidence, runbook, deployment/installation notes, and rollback
  notes.

### Out Of Scope Until After UAOS v1

- Native iOS or Android apps.
- Full Microsoft 365 content indexing, Outlook/Teams sending, tenant/admin
  changes, or permission changes.
- Full client-data assessment or client-controlled connector activation.
- Raw voice/audio retention.
- BYOK provider setup.
- AWS, Dropbox, or client-stack live connectors.
- Freedom runtime coupling.
- Automated durable memory promotion without review.
- Graphify replacement features such as workspace map, graph chat, cluster
  selector, source selector, recommendation engine, or action queue.
- Public production launch or paid-client workspace access.

If a proposed addition does not unblock one of the UAOS v1 acceptance tests, it
belongs in the post-v1 backlog.

## Authorized Surface Model

| Surface | UAOS v1 role | Allowed capabilities | Explicit stops |
|---|---|---|---|
| Linux workstation | Trusted worker and local development source | Pull repo, run tests, claim missions, execute approved local actions, write evidence | Public inbound execution, raw secret/log exposure, client-data-full payloads |
| Windows laptop | Trusted worker and operator surface | Pull repo, run worker bootstrap, claim approved missions, support M365 inventory planning after approval | Live Outlook/Teams send, tenant/admin changes, unapproved OneDrive/SharePoint content reads |
| Browser cockpit | Main operator surface | Intake, mission review, relay status, validation evidence, handoff links | Becoming a generic dashboard or Graphify clone |
| Android phone | Mobile operator cockpit | Command capture, approval, pause/resume, status and evidence review | Local execution, raw file access, raw audio retention |
| Android tablet | Mobile review cockpit | Larger review surface for mission evidence, approval, and handoff | Local execution, unrestricted connector access |
| Private GitHub repo | Durable source-of-truth spine | Request records, commits, issues/PRs, release records, relay references | Secrets, unredacted logs, sensitive client payloads |
| Graphify Workspace Cockpit | Knowledge lookup and optimization spoke | Read-only handoff records, graph snapshot references, evidence-backed mission candidates | Execution approval, graph writes from UAOS, duplicate chat/map/source-selection UI |
| Microsoft 365 | Future governed business workspace spoke | Inventory-only or metadata-read planning after approved activation | Email/calendar/Teams sends, content indexing, admin/security/permission changes |

## Final Stages

### Stage 0 - Ship Scope Freeze

Status: complete as of REQ-0057 at 2026-06-14T19:09:41-06:00

Purpose: freeze the final UAOS v1 path so work stops sprawling into attractive
but non-blocking additions.

Acceptance criteria:

- define what shippable means for UAOS v1;
- define authorized surfaces and their permitted roles;
- identify out-of-scope additions;
- wire this plan into active control documents;
- preserve the Graphify/UAOS boundary.

Output:

- `docs/specs/uaos-final-shippable-plan.md`;
- active pathway, source map, roadmap, manual cockpit, request log, and
  changelog updates.

### Stage 1 - Local Relay Proof Runner

Purpose: make the existing relay envelope and record-store foundation runnable
as one small proof without adding hosted infrastructure or UI first.

Acceptance criteria:

- a CLI or script creates a sample request/mission relay record;
- a phone/tablet/browser approval fixture is persisted;
- one Linux or Windows worker claim is accepted;
- a second worker claim is rejected;
- status transitions and evidence references are printed or written to a safe
  local artifact;
- no network, live connector, hosted relay, or client data is used.

Why this comes first: it proves the state loop before UI and cross-device
coordination make failures harder to understand.

### Stage 2 - Global Cockpit Shell

Purpose: create the first real UAOS cockpit surface that pulls from existing
records rather than becoming a new source of truth.

Acceptance criteria:

- browser-accessible local cockpit shows current focus, requests, relay records,
  worker claims, validation status, stop triggers, and next action;
- cockpit can launch or link to the local relay proof runner;
- cockpit shows Graphify handoff candidates as read-only mission candidates;
- cockpit does not implement Graphify chat, map, source/cluster selection, or
  recommendation ownership;
- UI handles empty, loading, success, error, unauthorized, and mobile layout
  states.

### Stage 3 - Authorized Mobile/Tablet Approval Surface

Purpose: make phone and tablet useful without giving them local execution
authority.

Acceptance criteria:

- phone/tablet browser can view pending mission envelopes and safe evidence
  summaries;
- Adam can approve, reject, pause, resume, or request changes;
- approvals produce validated relay envelopes and record-store entries;
- raw audio, raw logs, credentials, unrestricted file paths, and client data do
  not leave the worker/source-of-truth boundary;
- session expiry and disable behavior are documented.

### Stage 4 - Trusted Worker Bootstrap For Linux And Windows

Purpose: make multiple machines useful as workers without creating competing
operating systems.

Acceptance criteria:

- documented bootstrap for Linux and Windows clone/pull/setup/test flow;
- worker identity and role are explicit;
- worker can read authorized relay records and claim exactly one approved
  mission;
- worker refuses stale, superseded, conflicting, or out-of-boundary records;
- all outputs reconcile to request records, action logs, relay records, and
  commits.

### Stage 5 - Minimal Connector Activation

Purpose: activate only the connectors needed for the v1 operating loop.

Acceptance criteria:

- GitHub adapter remains dry-run by default and live actions require explicit
  mission approval;
- Graphify handoff consumption remains read-only;
- M365 remains blocked unless Adam approves inventory-only activation;
- connector registry, permission matrix, action log, and tests are updated for
  any activated capability;
- no connector writes, communications, client-data assessment, billing action,
  or destructive action can occur without a separate approved mission.

### Stage 6 - Client-Safe Intake And Delivery Preview

Purpose: make the customer/employee experience coherent without opening live
client data too early.

Acceptance criteria:

- public/prospect intake stays non-sensitive;
- internal Guided AI Labs operator review is required before client-visible AI
  findings;
- Client Gateway full assessment stays blocked until signed scope, workspace,
  roles, retention, connector approval, and review gates exist;
- employee/customer-facing language is documented for what the system can and
  cannot do in v1;
- no automatic client workspace creation.

### Stage 7 - Ship-Readiness Hardening

Purpose: prove the v1 product increment can survive real use by Adam on his
authorized surfaces.

Acceptance criteria:

- full unit suite passes;
- focused relay, Graphify, connector, policy, and safety tests pass;
- setup/installation notes cover Linux, Windows, browser, Android phone, and
  Android tablet use;
- runbook and deployment guide identify current local/private-GitHub release
  path and the absence of a production deployment target;
- changed-file secret scan passes;
- rollback and disable procedures are current;
- known limitations are visible and do not contradict the v1 claim.

### Stage 8 - Adam Pilot And Release Decision

Purpose: run the system with real Adam-owned work and decide whether UAOS v1 is
release ready.

Acceptance criteria:

- at least one real internal mission moves from intake to approval, worker
  claim, execution or dry-run proof, validation, evidence, and learning review;
- at least one phone/tablet approval or status-review path is used;
- at least one Windows or Linux worker bootstrap path is exercised;
- Graphify handoff is checked for overlap and consumed only as read-only
  candidate input;
- Adam records a release decision: hold, revise, release-ready for internal
  use, or project-complete for this phase.

## Acceptance Test Matrix

| Scenario | Must prove |
|---|---|
| Linux worker claim | Accepted worker claim changes one approved relay record to claimed and logs evidence. |
| Windows worker claim | Same mission cannot be claimed twice; stale source-state refs are rejected. |
| Phone approval | Phone/browser approval can create or approve a safe relay envelope without raw logs, secrets, or execution authority. |
| Tablet review | Tablet surface can review safe evidence and pause/resume/reject without local execution. |
| Graphify handoff | Graphify records are read-only mission candidates and never execution approval. |
| M365 boundary | Inventory-only access is blocked until approved; content reads and communications remain prohibited. |
| Client Gateway | Full assessment is blocked until signed scope, workspace, roles, retention, connector approvals, and review gates exist. |
| Hidden model routes | User sees route rationale and risk, not a model/provider picker. |
| Ship handoff | Setup, runbook, limitations, rollback, and validation evidence are current. |

## Stop Conditions

Stop and require Adam approval before:

- live client data;
- full Microsoft 365 content, Outlook, Teams, SharePoint, OneDrive, Entra,
  tenant, admin, security, permission, billing, calendar, or task access;
- public production release;
- paid-client workspace access;
- billing, payment, purchase, cancellation, or vendor-account action;
- destructive Git, filesystem, account, or connector write;
- raw audio retention;
- unreviewed client-visible AI findings;
- Freedom runtime coupling;
- any new connector capability not already covered by connector registry,
  permission matrix, tests, and an approved mission envelope.

## Post-v1 Backlog Parking Lot

These can be valuable later, but they are not allowed to extend the v1 finish
line:

- native mobile app;
- hosted relay beyond the minimum needed for browser/mobile authorization;
- persistent memory automation;
- BYOK and multi-provider client setup;
- AWS/Dropbox/client-stack connectors;
- public client portal;
- full Microsoft 365 operational automation;
- market-ready infographic and external marketing assets.
