# Rev 2 Architecture

Created: 2026-06-21T14:59:46-06:00
Last Updated: 2026-06-21T20:51:47-06:00
Status: active architecture
Owner: Adam Goodwin

## Purpose

This document defines the active GAIL AI Operating System Rev 2 architecture
boundary.

It promotes the useful architecture from copied UAOS v1 reference records into
the Rev 2 source of truth without migrating v1 code, activating workers,
calling live connectors, launching a hosted relay, or granting production
authority.

## Current Architecture Posture

Rev 2 is currently a governed private repository and control set.

Active now:

- private GitHub source of truth on
  `Adamgdwn/gail-ai-operating-system-rev-2`, branch `main`;
- local Windows operator workspace for repo edits, validation, commits, and
  pushes;
- copied v1 reference documents under `docs/migration/reference/uaos-v1`;
- active controls for source routing, tool permissions, runtime posture, agent
  inventory, model routes, and prompt sources;
- local no-network mission spine package at
  `packages/uaos-core/src/gail_ai_operating_system/mission_spine.py`;
- focused mission-spine tests in `tests/test_mission_spine.py`;
- active read-only Graphify handoff checkpoint at
  `docs/graphify-handoff-checkpoint.md` plus local candidate validation in
  `packages/uaos-core/src/gail_ai_operating_system/graphify_handoff.py`;
- local no-network relay envelope validator at
  `packages/uaos-core/src/gail_ai_operating_system/relay_envelope.py`;
- local no-network relay record store and single-worker claim proof at
  `packages/uaos-core/src/gail_ai_operating_system/relay_store.py`;
- inter-chunk Microsoft 365 / AG Operations bridge orientation recorded as
  architecture only;
- inter-chunk Freedom Engine objective review recorded as architecture and
  migration routing only, with Freedom now identified as the substantial
  future phone-interface anchor candidate and agentic business partner
  capability source;
- active Freedom phone-interface and business-partner boundary decision record
  at `docs/decisions/freedom-phone-interface-business-partner-boundary.md`;
- documentation and local validation chunks only.

Not active yet:

- browser command center;
- Android phone or tablet portal;
- Windows or Linux worker bootstrap;
- persistent relay worker service or claim loop;
- hosted relay;
- live Microsoft 365, QuickBooks, billing, vendor, client-data, or deployment
  connectors;
- Freedom Engine runtime merge, mobile/gateway/desktop-host activation,
  Supabase schema adoption, LiveKit/OpenAI voice activation, relay secret use,
  or generated runtime artifact import;
- production runtime or release.

## Core Principles

The source of truth is the governed Rev 2 record set, not a device.

Devices and services have roles:

- Windows and Linux can become trusted workers.
- Android and browser surfaces can become cockpits.
- Graphify can become an enhanced knowledge spoke for routing and handoff
  acceleration.
- GitHub remains the durable private spine.
- Relay records coordinate work but do not execute work or replace durable
  records.
- Connectors remain planning-only until a later approved boundary activates a
  specific capability.

Every future executable path must preserve planning and execution separation:
human intent and approval are recorded first, then a worker validates the
current state, policy boundary, and stale-state checks before acting.

## System Layers

| Layer | Current role | Future role | Boundary |
|---|---|---|---|
| Private GitHub spine | Canonical private remote, commits, active docs, and chunk evidence. | Durable request, mission, relay, issue, PR, release, and evidence references. | No secrets, raw logs, raw audio, unredacted sensitive payloads, or client data. |
| Active control records | Define source routing, permissions, runtime scope, agents, prompts, models, and architecture. | Gate future code migration, workers, connectors, portal actions, and release readiness. | Controls do not activate live capabilities by themselves. |
| Windows operator workspace | Current local editing and validation environment. | Trusted worker and operator surface after bootstrap controls exist. | No live business connectors, persistent worker service, or broad local filesystem automation without later approval. |
| Linux reference or worker surface | Superseded v1 reference host only. | Trusted worker clone that pulls from private GitHub. | Linux is not the Rev 2 source of truth and must not rely on tunnel-dependent operation. |
| Browser command center | Not built. | Main shared cockpit for desktop and mobile browser use. | Must read and write governed records through approved local or relay paths, not become a second truth store. |
| Android phone cockpit | Not built in Rev 2. | Freedom is the preferred phone-interface anchor candidate for intent capture, approval, pause/resume, status, and safe evidence review; Rev 2 may provide a browser fallback or compatibility surface later. | No local execution, raw secret display, raw logs, raw audio, unrestricted filesystem access, direct connector access, generated Freedom config import, or Freedom runtime activation without a bounded later chunk. |
| Android tablet cockpit | Not built. | Larger review surface for evidence, approvals, and handoffs. | Same mobile limits as phone; no unrestricted connector authority. |
| Relay records | Local no-network JSON-backed proof for validated relay envelopes, status transitions, reference-only evidence records, and single trusted-worker claim attempts. | Coordination records for intent, approval, worker claim, status, evidence links, and recovery. | Relay carries safe summaries and references only; it does not execute work, poll workers, call connectors, or own permanent audit truth alone. |
| Future hosted relay | Not approved. | Possible low-latency queue, notification, session, and heartbeat service after GitHub-backed proof. | Requires explicit owner approval, auth/session design, threat model, retention rule, and disable path. |
| Rev 2 mission spine | Local no-network mission envelopes, deterministic planning, policy gate, validation, and JSON record store. | Local deterministic runtime for future approved mission records, evidence references, and action logs. | No autonomous mission loop, connector call, worker claim, relay polling, or production action until later controls exist. |
| Graphify knowledge spoke | Active read-only route status and handoff candidate validation. | Read-only graph context, handoff records, recommendations as mission candidates. | Graphify recommendations are not execution approval and must pass Rev 2 policy before work. |
| Microsoft 365 / AG Operations business substrate | Local architecture references reviewed for bridge posture only. | Identity, SharePoint records, Lists, Planner tasks, Teams coordination, Exchange signals, Forms intake, and audit surfaces feeding governed mission candidates through approved adapters. | Planning-only in Rev 2; no live tenant reads, content ingestion, Outlook/Teams sends, app consent, permission changes, client data, or setup-helper grant reuse. |
| Freedom Engine operating partner OS | Downloaded archive reviewed at summary level with no code import or runtime activation. | Substantial phone-interface anchor candidate plus high-level agentic business partner runtime, self-learning, research, agent/tool calling, voice/mobile/desktop UX, gateway/desktop-host coordination, Action Fabric, Device Mesh, model routing, storage-map, business memory, and operator-run patterns feeding Rev 2 bridge candidates. | Reference and bridge-planning only until a bounded phone-link or integration chunk; no secret values, generated runtime config, local state, APKs, logs, provider state, Supabase runtime data, contacts, email data, memories, raw transcripts, live Freedom services, code merge, or source import in Rev 2. |
| Connector registry | Link-only seed records and planning references. | Governed connector profiles with owner, workspace, data class, approval gate, audit, and retention rules. | Profiles are permission structure, not permission or credentials. |
| Relay envelopes | Local-file-only schema validation for intent, approval, status, evidence, and handoff records. | Future relay records for device/cockpit coordination before worker claims or hosted relay. | Envelopes carry safe summaries and references only; persistence is limited to the local relay store proof with no polling, hosted relay, client data, raw payloads, or execution authority. |
| Model and prompt controls | Current Codex coding session only for repo collaboration. | Future runtime route only after model and prompt approval records exist. | No production runtime model, BYOK provider, client-data route, or connector-driving prompt is approved. |

## Source-Of-Truth Flow

The durable spine is:

```text
Adam request or approved work packet
  -> active pathway / request record / issue or PR reference
    -> private GitHub commit history
      -> validation evidence and handoff notes
        -> future portal, relay, worker, and Graphify references reconcile back
           to the same durable records
```

Future device-local drafts are not authoritative until reconciled into a
governed record. A phone-captured note, worker-local status file, relay cache,
or Graphify recommendation remains draft or candidate material until a Rev 2
record accepts it.

## Device Role Contracts

Every future device or surface must be able to answer these questions before it
participates in work:

1. Which repo, branch, and commit is it using?
2. Which role is it playing: operator cockpit, trusted worker, viewer,
   reviewer, knowledge spoke, or future business workspace?
3. Which active controls did it load before acting?
4. Which tools and connectors are present, absent, planning-only, or approved?
5. Which secrets are present by name only, without printing values?
6. Which approval level, stop triggers, and stale-state checks apply?
7. Where will safe evidence and handoff records land?
8. How can the surface be disabled or recovered if it drifts?

## Portal And Cockpit Architecture

The first usable cockpit should keep Rev 2 browser-first for Windows, Linux,
Android tablet, and ordinary desktop browsers while treating Freedom as the
preferred phone-interface anchor candidate. The app-shell choice should be made
after a dedicated Freedom phone-link boundary chunk defines what crosses
between Freedom and Rev 2.

Expected first portal capabilities:

- show current focus, active requests, planned chunks, validation state, stop
  triggers, and next action;
- capture rough intent as a draft;
- display safe evidence summaries;
- approve, reject, pause, resume, or redirect bounded work only after the
  approval boundary exists;
- link to durable records, commits, validation output summaries, and future
  worker status;
- show Graphify handoff candidates as read-only context, not as approved work.
- interoperate with the Freedom phone link through safe records once that
  boundary is defined.

The portal must not:

- execute local shell commands directly;
- bypass worker permission checks;
- expose raw secrets, raw logs, raw audio, or unrestricted filesystem paths;
- become a separate source of truth;
- activate connectors or production actions by UI affordance alone.
- duplicate or replace Freedom's phone work before the Freedom phone-link
  boundary is explicitly defined.

## Worker Architecture

Windows and Linux workers should be outbound, pull-based, and role-checked.

Future worker flow:

```text
Worker starts
  -> pulls private GitHub state
    -> confirms role, commit, controls, and tool boundary
      -> reads approved local or relay work record
        -> validates stale state, approval metadata, and stop triggers
          -> claims exactly one allowed task
            -> executes only local approved behavior
              -> writes safe evidence and status back to governed records
```

Workers must stop on:

- stale repo state or missing commit reference;
- unknown worker identity or role;
- missing, duplicated, or conflicting claim;
- connector, data class, approval level, or stop-trigger ambiguity;
- request for live business-system access before activation;
- raw secret, client data, raw logs, or raw audio in relay or evidence payloads;
- tunnel-dependent source-of-truth behavior.

## Relay Architecture

The first relay proof should be local and no-network. The next relay posture
should use private GitHub-backed records before any custom hosted relay.

Relay records may carry:

- project ID;
- request ID;
- mission ID;
- actor and device role;
- approval level and timestamp;
- observed commit or state reference;
- worker claim state;
- connector profile IDs;
- stop triggers shown to the approver;
- validation result summary;
- action-log or evidence references.

Relay records must not carry:

- secret values or raw credentials;
- raw command logs;
- raw audio;
- unrestricted filesystem paths;
- full client payloads;
- unreviewed sensitive business content;
- direct worker command authority;
- production deployment or connector execution approval by itself.

A future hosted relay can be evaluated only after the GitHub-backed pattern
proves the state contract. It must support safe summaries, auth/session
controls, device disable, stale-state rejection, audit/retention rules, and
reconciliation back to durable records.

## Connector Architecture

Connector records are planning and permission structure until a later chunk
explicitly activates a capability.

The connector capability ladder is:

1. planning-only;
2. inventory-only;
3. metadata-read;
4. content-read;
5. summarize;
6. draft-only;
7. prepare-action;
8. execute-after-approval.

Current Rev 2 approval stops before all live Microsoft 365, QuickBooks,
accounting, finance, billing, vendor, client-data, hosted relay, infrastructure,
and deployment connector actions.

Any future live connector must have:

- connector profile;
- owner and workspace;
- approved data classes;
- prohibited data classes;
- approval gate;
- retention and audit rules;
- dry-run behavior where practical;
- safe logging;
- tests for allowed and denied behavior;
- disable or rollback path;
- explicit owner approval for the activated capability.

## Microsoft 365 Bridge Posture

Microsoft 365 should feed the cockpit as the governed business substrate, not
as the central cockpit brain or execution authority.

The intended separation is:

```text
Microsoft 365
  -> identity, records, tasks, signals, collaboration, audit
Graphify
  -> knowledge map, decisions, recommendations, handoff candidates
Rev 2
  -> mission spine, policy gate, approvals, relay records, workers, evidence
```

The future bridge should read approved metadata, source links, action-log
records, decision records, Planner/List state, CRM records, and reviewed
summaries from Microsoft 365. It should not copy raw Microsoft 365 content into
Rev 2 by default.

The safe future flow is:

```text
M365 record or signal
  -> approved M365 adapter reads metadata or a reviewed safe summary
    -> Rev 2 connector profile and policy gate validate the request
      -> mission candidate or relay envelope
        -> browser or Android cockpit approval/status/evidence view
          -> worker claim and execution only after approval
            -> evidence links back to Rev 2 and M365 action logs
```

The AG Operations Stage 9 bridge posture maps cleanly onto Rev 2:

- G0 read-only inventory, classification, summary, and gap detection;
- G1 propose-and-log records, especially suggested Agent Action Log rows;
- G2 approved internal writes to Lists, Planner, drafts, and evidence;
- G3 restricted external or access writes requiring explicit approval;
- G4 blocked autonomous actions.

Rev 2 still treats every Microsoft 365 capability as planning-only until a
later connector activation chunk creates the adapter profile, permission
design, rollback worksheet, dry-run tests, action logging, and explicit owner
approval. The future adapter must not reuse broad setup-helper grants as
production bridge power.

## Freedom Engine Bridge Posture

Freedom Engine is Adam's current operating partner OS, a high-level agentic
business partner, and the preferred phone-interface anchor candidate for Rev 2.
It already has mature runtime and product ideas that Rev 2 has not activated
yet: a Next.js control plane, Android companion, local gateway, desktop host,
voice runtime, operator-run ledger, self-learning and learning-review loops,
research and programming-request workflows, agent/tool calling concepts, Action
Fabric contracts, Device Mesh contracts, storage persistence map, and
Supabase-backed business memory surfaces.

The objective review in
`docs/migration/freedom-engine-objective-review.md` concludes that the repos
should not be merged wholesale. Freedom should remain the active operating
partner runtime; Rev 2 should remain the clean governed mission, relay, policy,
worker, connector, and evidence spine.

The active Chunk Sixteen boundary decision in
`docs/decisions/freedom-phone-interface-business-partner-boundary.md` makes
that relationship operational for the next build phase: Freedom is the first
phone-interface anchor candidate and the high-level agentic business partner
capability source; Rev 2 owns the mission, policy, relay, connector, worker,
and evidence contracts that any future Freedom bridge must satisfy.

The future bridge should translate Freedom concepts into Rev 2 records:

```text
Freedom request, run, device, or runtime signal
  -> safe summary and reference-only bridge candidate
    -> Rev 2 connector profile and policy gate
      -> mission or relay envelope
        -> browser/Android cockpit approval
          -> worker claim and evidence only after approval
```

The strongest fold-in candidates are operator-run lifecycle vocabulary,
evidence vocabulary, consequence review, Device Mesh, environment capability
snapshots, Action Fabric classification, storage persistence rules,
self-learning, research, programming-request handling, agent/tool calling, tool
selection, business-memory feedback loops, and gateway/desktop-host pairing and
evidence patterns. These should be translated or rewritten in later Rev 2
chunks, not copied directly from Freedom. The phone-interface and
business-partner path should start with a dedicated boundary record after the
local proof runner, then a browser/app-shell decision that treats Freedom as
the phone anchor and business-partner layer rather than racing to build a
separate native Android portal.

Rev 2 must not import Freedom generated mobile runtime config, `.local-data`,
build outputs, APKs, provider state, Supabase runtime data, contacts, email
data, memories, raw transcripts, logs, secret-shaped files, live runtime routes,
or A3 autonomy posture. Any live Freedom connector or runtime activation needs a
separate connector profile, explicit approval, tests, rollback path, and secret
containment.

## Graphify Architecture

Graphify remains a knowledge spoke, not an execution surface.

Rev 2 may consume validated Graphify handoff records, workspace graph
references, or future repo-local graph updates to reduce repeated repository
reading and help route work. The architecture boundary is:

```text
Graphify graph or handoff record
  -> read-only Rev 2 validation
    -> proposed request or mission candidate
      -> human approval and Rev 2 policy gate
        -> worker execution only if allowed
```

The enhanced Graphify checkpoint belongs before broad source exploration,
architecture rerouting, dependency tracing, or graph-dependent migration work.

Graphify must not approve execution, mutate Rev 2 source, index secrets, upload
graphs, run full semantic rebuilds outside chunk scope, perform live adapter
fetches without a later boundary, or replace request, relay, worker, connector,
or release controls.

## Data And Evidence Boundaries

Allowed in the Rev 2 repo now:

- active docs and controls;
- copied v1 reference docs already inventoried;
- safe validation summaries;
- commit SHAs, issue or PR references, and handoff notes;
- future synthetic test fixtures that contain no sensitive values.

Not allowed in the Rev 2 repo:

- `.env` files;
- secret values, credentials, tokens, tenant secrets, or private keys;
- QuickBooks, accounting, invoice, payment, billing, or finance exports;
- Microsoft 365 content;
- client data;
- raw logs;
- raw audio;
- unredacted screenshots or sensitive payload dumps.

## Functional Verification Ladder

Chunk verification should match the surfaces that exist.

| Build stage | Verification expected |
|---|---|
| Current control/spec chunks | Governance preflight, schema validation, link/path checks, placeholder and stale-authority searches, diff check, secret scans, commit/push verification. |
| Local mission spine chunks | Unit tests for mission envelopes, policy gate, validation errors, safe logging, and stop triggers. |
| Relay proof chunks | No-network relay envelope tests, stale-state rejection, unsafe-payload rejection, single-worker claim proof, and conflict recovery checks. |
| Portal chunks | Browser smoke tests, mobile viewport checks, empty/loading/success/error/unauthorized states, approval action tests, and safe evidence display checks. |
| Worker chunks | Windows and Linux bootstrap dry runs, role checks, pull-before-act checks, stale commit rejection, claim conflict tests, and safe evidence writeback. |
| Connector chunks | Mock or sandbox tests first, dry-run proof, allowed/denied capability tests, safe log review, least-privilege profile checks, and explicit approval evidence. |
| Pilot and release chunks | End-to-end walkthrough from intent to approval, worker claim, execution or dry run, validation evidence, handoff, runbook, rollback, and Adam release decision. |

This means current chunks can be verified as architecture/control artifacts, but
future runtime chunks must add functional smoke tests for the actual surface
being introduced.

## Key Decisions

| Decision | Status | Rationale |
|---|---|---|
| Private GitHub is the durable spine. | Active | It gives Rev 2 a private, auditable, device-independent source of truth. |
| DirectLink is transport/status only. | Active | It can help with explicit cross-machine work, but Rev 2 should not depend on tunneling for normal operation. |
| Browser-first Rev 2 cockpit with Freedom as phone anchor. | Active direction | Rev 2 should reach Windows, Linux, Android tablet, and desktop browsers through a browser/app shell, while Freedom carries the first phone-side operator link unless a later chunk decides otherwise. |
| Workers pull outward and do not expose public inbound local services. | Active direction | This keeps high-risk execution inside trusted worker boundaries. |
| GitHub-backed relay records come before hosted relay. | Active direction | Durable, auditable, slower proof beats custom infrastructure too early. |
| Graphify remains separate. | Active | It owns knowledge lookup and recommendations; Rev 2 owns mission approval, policy, execution, validation, and evidence. |
| Microsoft 365 is the business substrate, not the cockpit brain. | Active direction | M365 owns identity, records, collaboration, and signals; Graphify owns knowledge intelligence; Rev 2 owns mission policy, relay, worker execution, evidence, and stop rules. |
| Freedom Engine is operating-partner runtime, agentic business partner, and phone-interface anchor candidate, not the Rev 2 spine. | Active decision | Freedom should carry the first phone-side link and feed mature self-learning, research, agent/tool calling, business-memory, UX, and action-ledger patterns into Rev 2 through safe bridge records defined in `docs/decisions/freedom-phone-interface-business-partner-boundary.md`; Rev 2 should not inherit Freedom's live provider/runtime posture by default. |
| Connector registry entries are not credentials or permission. | Active | Live connector use needs separate approval, tests, and data boundaries. |
| Local relay store proof exists before worker bootstrap. | Active | Claim and stale-state semantics now have a deterministic local proof before Windows/Linux worker services or hosted relay are evaluated. |

## Non-Goals For Current Architecture Chunk

- No further code migration beyond local proof modules.
- No app scaffold.
- No worker bootstrap.
- No hosted relay.
- No persistent polling service.
- No live connector activation.
- No Microsoft 365, QuickBooks, finance, billing, vendor, deployment, or client
  data access.
- No production deployment or release-readiness claim.

## Promotion References

This active architecture was rewritten from these copied reference inputs:

- `docs/migration/reference/uaos-v1/specs/cross-device-source-of-truth-foundation.md`
- `docs/migration/reference/uaos-v1/specs/shared-relay-phone-cockpit-architecture.md`
- `docs/migration/reference/uaos-v1/specs/uaos-final-shippable-plan.md`
- `docs/migration/reference/uaos-v1/specs/connector-registry-client-gateway-boundary.md`
- `docs/migration/reference/uaos-v1/specs/microsoft-365-business-environment-boundary.md`
- `docs/migration/reference/uaos-v1/specs/graphify-workspace-cockpit-uaos-integration.md`
- `docs/migration/reference/uaos-v1/apps/cockpit-command-proof-README.md`

Those files remain reference-only unless a later chunk promotes specific code,
tests, or records under Rev 2 controls.

## External Local Orientation Inputs

On 2026-06-21, an inter-chunk read-only pass reviewed local documentation from
`C:\Users\adamg\01. Code Projects\AG Operations Workspace Setup` to align the
future Microsoft 365 bridge posture with Rev 2. The reviewed inputs were
architecture and control records only, including:

- `M365_STAGE_9_AGENTIC_OS_BRIDGE_READINESS.md`;
- `M365_GRAPHIFY_UAOS_ALIGNMENT.md`;
- `docs/AGENTIC_M365_READINESS.md`;
- `config/M365_STAGE_9_AGENT_CAPABILITY_MODEL.json`;
- `config/M365_STAGE_9_BRIDGE_READINESS_CONTROL.json`;
- `docs/CARD_PLAN_AGENT_CONTROL_PLANE.md`;
- `docs/WORKSPACE_CHUNK_7_FINAL_USABILITY_WALKTHROUGH.md`.

No live Microsoft 365 content, OneDrive material, tenant data, local
environment file, secret value, app consent, permission change, connector call,
or unattended automation was read or activated during that pass.

On 2026-06-21, an inter-chunk review inspected the downloaded Freedom Engine
archive at `C:\Users\adamg\Downloads\the-freedom-engine-os-main.zip` through a
temporary local extraction. The review recorded the objective relationship in
`docs/migration/freedom-engine-objective-review.md`. No Freedom code was copied
into active Rev 2 source, no secret values were printed or recorded, and no
Freedom gateway, desktop-host, mobile, relay, Supabase, LiveKit, OpenAI, email,
or production behavior was activated. On 2026-06-21T19:29:48-06:00, the plan
was updated to treat Freedom as the substantial future phone-interface anchor
candidate. On 2026-06-21T19:49:09-06:00, the plan was also updated to preserve
and elevate Freedom as a high-level agentic business partner with
self-learning, research, agent/tool calling, business memory, voice/mobile, and
operator-run capabilities while preserving the no-code, no-merge, no-import,
no-generated-config, and no-runtime-activation boundary until a dedicated later
chunk.

On 2026-06-21T20:45:31-06:00, Chunk Sixteen created the active Freedom
phone-interface and business-partner boundary decision record at
`docs/decisions/freedom-phone-interface-business-partner-boundary.md`. That
record defines the first safe bridge envelope and record shapes for summaries,
runs, evidence, learning, research, action requests, and agent/tool-calling
intents, while keeping all Freedom code import, generated config, local state,
runtime activation, live providers, and competing Android phone work blocked
until a later explicit chunk.
