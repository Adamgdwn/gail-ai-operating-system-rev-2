# Rev 2 Architecture

Created: 2026-06-21T14:59:46-06:00
Last Updated: 2026-06-21T16:00:50-06:00
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
- documentation and local validation chunks only.

Not active yet:

- browser command center;
- Android phone or tablet portal;
- Windows or Linux worker bootstrap;
- relay envelope validator, relay record store, or worker claim loop;
- hosted relay;
- live Microsoft 365, QuickBooks, billing, vendor, client-data, or deployment
  connectors;
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
| Android phone cockpit | Not built. | Intent capture, approval, pause/resume, status, and safe evidence review. | No local execution, raw secret display, raw logs, raw audio, unrestricted filesystem access, or direct connector access. |
| Android tablet cockpit | Not built. | Larger review surface for evidence, approvals, and handoffs. | Same mobile limits as phone; no unrestricted connector authority. |
| Relay records | Not built in Rev 2. | Coordination records for intent, approval, worker claim, status, evidence links, and recovery. | Relay carries safe summaries and references only; it does not execute work or own permanent audit truth alone. |
| Future hosted relay | Not approved. | Possible low-latency queue, notification, session, and heartbeat service after GitHub-backed proof. | Requires explicit owner approval, auth/session design, threat model, retention rule, and disable path. |
| Rev 2 mission spine | Local no-network mission envelopes, deterministic planning, policy gate, validation, and JSON record store. | Local deterministic runtime for future approved mission records, evidence references, and action logs. | No autonomous mission loop, connector call, worker claim, relay polling, or production action until later controls exist. |
| Graphify knowledge spoke | Reference-only planning posture in Rev 2. | Read-only graph context, handoff records, recommendations as mission candidates. | Graphify recommendations are not execution approval and must pass Rev 2 policy before work. |
| Connector registry | Link-only seed records and planning references. | Governed connector profiles with owner, workspace, data class, approval gate, audit, and retention rules. | Profiles are permission structure, not permission or credentials. |
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

The first usable cockpit should be browser-first and mobile-responsive so the
same operating surface works from Windows, Linux, Android phone, Android
tablet, and ordinary desktop browsers.

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

The portal must not:

- execute local shell commands directly;
- bypass worker permission checks;
- expose raw secrets, raw logs, raw audio, or unrestricted filesystem paths;
- become a separate source of truth;
- activate connectors or production actions by UI affordance alone.

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

## Graphify Architecture

Graphify remains a knowledge spoke, not an execution surface.

Future Rev 2 may consume Graphify handoff records, workspace graph references,
or repo-local graph updates to reduce repeated repository reading and help
route work. The architecture boundary is:

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
graphs, run full semantic rebuilds outside chunk scope, or replace request,
relay, worker, connector, or release controls.

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
| Browser-first cockpit before native apps. | Active direction | It reaches Windows, Linux, Android phone, Android tablet, and desktop browsers with one first surface. |
| Workers pull outward and do not expose public inbound local services. | Active direction | This keeps high-risk execution inside trusted worker boundaries. |
| GitHub-backed relay records come before hosted relay. | Active direction | Durable, auditable, slower proof beats custom infrastructure too early. |
| Graphify remains separate. | Active | It owns knowledge lookup and recommendations; Rev 2 owns mission approval, policy, execution, validation, and evidence. |
| Connector registry entries are not credentials or permission. | Active | Live connector use needs separate approval, tests, and data boundaries. |

## Non-Goals For Current Architecture Chunk

- No code migration.
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
