# Shared Relay And Phone Cockpit Architecture

Created: 2026-06-14T16:44:31-06:00
Last Updated: 2026-06-14T17:30:33-06:00
Status: complete as of REQ-0054 at 2026-06-14T16:44:31-06:00; active architecture note
Owner: Adam Goodwin

## Purpose

This architecture note defines the first shared relay and phone/tablet cockpit
pattern for UAOS.

The goal is to let Android, tablet, Windows, Linux, and browser surfaces
coordinate missions without exposing the local agent runtime directly to the
public internet, without requiring Tailscale, and without creating a second
source of truth.

This note does not implement a hosted relay, mobile app, tunnel, live Microsoft
365 access, live client workspace, or new connector capability.

## Core Decision

The first prototype evaluation should use a GitHub-backed interim relay record
pattern before any custom hosted relay.

That means:

- the private UAOS GitHub repo remains the durable spine;
- request records, mission records, action-log references, commit SHAs, issue or
  PR IDs, and connector profile IDs remain the durable references;
- phone/tablet approval can be tested through private GitHub/browser surfaces
  or a thin cockpit that writes back to governed records;
- workers still pull or poll outbound;
- no local worker accepts public inbound connections;
- a later hosted relay may cache state and route notifications, but it must
  reconcile back to the governed repo or approved workspace records.

## Architecture Shape

```text
Phone / tablet / browser cockpit
  -> private relay record or future hosted relay
    -> outbound-polling trusted worker
      -> UAOS mission spine
        -> policy gate
          -> connector adapter
            -> validation evidence and action log
              -> governed source-of-truth spine

Graphify Workspace Cockpit
  -> read-only handoff endpoint
    -> UAOS Graphify adapter
      -> dry-run mission candidate
```

The relay coordinates work. It does not execute work.

## Responsibilities

| Layer | Owns | Must not own |
|---|---|---|
| Phone/tablet cockpit | Intent capture, status review, approve/pause/redirect prompts, human comments, evidence summary review. | Secret values, unrestricted filesystem access, raw logs, raw client data, raw audio, or direct tool execution. |
| Interim GitHub-backed relay | Durable request/mission references, approval comments, status issues, action-log links, commit/PR/issue links. | Private credentials, raw tool output dumps, local machine state, or unreviewed sensitive artifacts. |
| Future hosted relay | Low-latency queue/cache, session state, notification delivery, device heartbeat, compact approval prompt delivery. | Sole source of truth, permanent audit trail without repo/workspace reconciliation, connector credentials, or direct worker command authority. |
| Trusted worker | Repo clone, local secrets, tool adapters, tests, validation, action logs, outbound polling, controlled execution. | Public inbound service exposure or unapproved client/business connector reads. |
| UAOS mission spine | Mission envelope, approval boundary, policy gate, action logging, validation, request records, learning promotion. | Graph map/recommendation ownership, M365 ingestion ownership, or client-visible findings without review. |
| Graphify Workspace Cockpit | Workspace map, Ask/Map/Decisions/Recommendations/Work Queue, Graphify handoff records. | UAOS execution approval or mission policy decisions. |

## First Prototype Pattern

Use private GitHub records as the first relay evaluation:

| Record | First shape |
|---|---|
| Request | `docs/requests/REQ-xxxx-*.md` plus request-log row. |
| Mission | Future `missions/<mission_id>.json` or issue body that references a request ID. |
| Project / graph registry | Stable project ID, graph source, graph snapshot ID or ETag, and active Graphify workspace reference. |
| Approval prompt | Private GitHub issue comment or cockpit note containing only safe summary, approval level, stop triggers, and evidence links. |
| Worker status | Action-log summary, test result, commit SHA, and current state written back to repo or issue. |
| Phone view | GitHub mobile/browser or thin future cockpit reading the safe prompt and status record. |

This is intentionally slower than a custom relay, but it has the right bias:
durable first, auditable first, small first.

## Future Hosted Relay Pattern

A later hosted relay may be evaluated after the GitHub-backed pattern proves the
state contract. Candidate implementations include Cloudflare Workers with D1 or
KV, Supabase, or a small authenticated web service.

Minimum requirements before building it:

- explicit owner approval for the hosting choice;
- identity/session design;
- device enrollment and disable flow;
- audit and retention rules;
- threat model for approval spoofing, replay, prompt injection, and stale state;
- no secrets in relay payloads;
- no public inbound access to local workers;
- reconciliation back to request records, mission records, action logs, and
  commit or issue references.

The hosted relay should support outbound worker polling or long-poll/WebSocket
client connections initiated by the worker. It should never require opening a
local workstation port to the public internet.

## Device Trust And Authentication

Interim posture:

- private GitHub authentication is the first identity boundary;
- only Adam should approve mission progression until Guided AI Labs roles are
  defined;
- phone/tablet approval remains human approval, not runtime autonomy expansion;
- any approval record must include timestamp, actor, request ID, mission ID,
  approval level, and stop triggers shown.

Future posture:

- Microsoft 365 / Entra is the likely business identity layer for Guided AI
  Labs personnel;
- device enrollment should assign a role: operator cockpit, trusted worker,
  viewer, reviewer, client sponsor, or client employee;
- sessions should expire;
- devices should be remotely disable-able;
- every approval should be auditable and tied to a durable record;
- lost, stale, or unknown devices should lose approval capability first.

## Phone And Tablet Capabilities

Phone/tablet can:

- capture a new rough intent as draft;
- view current mission status;
- review safe evidence summaries;
- approve a bounded next step when the approval level allows it;
- pause or cancel a mission;
- redirect a mission back to clarification;
- request a handoff summary;
- mark a decision as needing Guided AI Labs review.

Phone/tablet must stop before:

- approving destructive local or external actions;
- approving production release, billing, payment, client-data, raw-audio, or
  external communication actions;
- approving live connector activation;
- viewing raw secret values, raw credentials, unrestricted filesystem paths, or
  unredacted logs;
- turning Graphify recommendations into execution;
- making unreviewed AI findings client-visible.

## What Never Leaves The Trusted Worker

These remain local unless a later approved boundary says otherwise:

- secret values and raw credentials;
- unrestricted filesystem access;
- local `.env` files and provider tokens;
- raw command logs that may contain sensitive data;
- unredacted screenshots;
- raw audio;
- unscoped client-controlled data;
- broad local OS control;
- live connector sessions;
- unreviewed AI analysis for client work.

Safe relay payloads should carry references and summaries:

- project ID;
- graph registry ID or active graph reference;
- graph snapshot ID, ETag, or observed graph timestamp;
- request ID;
- mission ID;
- action-log ID;
- connector profile ID;
- commit SHA;
- issue or PR URL;
- validation result summary;
- risk and approval level;
- stop triggers displayed to the approver.

## Sync And Conflict Rules

- Repo state wins over device-local draft state.
- A phone-captured item is draft until reconciled into a request record,
  mission record, or approved workspace record.
- A worker must pull before acting and must record the commit SHA or issue state
  it used.
- If two devices submit conflicting approvals, the worker stops for human review.
- If a relay record references a stale request, missing mission, unknown
  connector profile, or superseded stop trigger, the worker stops.
- Graphify handoff records remain read-only mission candidates and must pass the
  REQ-0050 validator and REQ-0053 adapter path before UAOS can propose work.
- Relay records should reference the project graph used for orientation so
  Android, Windows, Linux, browser, Graphify, and UAOS agents can confirm they
  are acting from the same map before approving or executing work.

## External Transcript Learning

On 2026-06-14, UAOS reviewed the auto-generated transcript from
`https://www.youtube.com/watch?v=Owv503rTqYY`.

The useful lesson was not a direction change. It reinforced that Graphify's
highest leverage is a shared, queryable project map that reduces repeated repo
reading and lets multiple agents or devices work from the same context.

UAOS already has Graphify as a separate knowledge spoke and a read-only handoff
adapter. The extra relay requirement is that future relay envelopes should
reference the relevant project registry and graph snapshot, not only request or
mission IDs.

## Why This Avoids Tailscale While Preserving Safety

The worker connects outward to a private GitHub record or future hosted relay.
The phone connects to the same governed surface. Neither device needs a private
mesh network for first proof, and the local worker does not need a public
listener.

This keeps the highest-risk powers in the local trusted worker while still
allowing phone/tablet command, approval, and status review.

## Threat And Permission Notes

| Threat | Control |
|---|---|
| Stale approval | Include request ID, mission ID, stop triggers, approval level, and observed commit/state hash in every approval prompt. |
| Approval spoofing | Use private GitHub identity first; later use Entra/device enrollment and signed session tokens. |
| Prompt injection through relay text | Treat relay text as data; worker revalidates mission envelope and policy gate before acting. |
| Sensitive log leakage | Relay receives summaries and references only; raw logs stay local or in approved redacted artifacts. |
| Graphify overlap | Graphify remains the knowledge spoke; UAOS consumes handoff records and owns execution policy. |
| Client-data bleed | Client Gateway work remains blocked until scoped workspace, roles, retention, connector approvals, and review states exist. |
| Device loss | Revoke GitHub/session access; future relay must support device disable and session expiry. |

## Acceptance Scenarios

| Scenario | Expected result |
|---|---|
| Android phone captures a request draft | Draft remains non-authoritative until reconciled into a request record. |
| Windows laptop acts as trusted worker | It pulls latest repo state, validates role and stop triggers, runs only approved local work, and writes evidence back. |
| Linux workstation and Windows worker both see a mission | Only one worker claims the mission; conflicting claims stop for review. |
| Phone approves an A1/A2 planning step | Worker rechecks policy, records approval metadata, then proceeds only inside the mission envelope. |
| Phone tries to approve live M365 access | Stop; M365 remains planning-only until connector activation is approved. |
| Graphify produces a handoff | UAOS pulls through the REQ-0053 read-only adapter and treats the result as a dry-run mission candidate only. |
| Hosted relay cache is stale | Worker rejects stale relay state and reconciles against the repo/workspace record. |

## Implemented Validation Chunk

REQ-0055 implemented the local, no-network relay envelope validator:

- define `RelayEnvelope`;
- validate project ID, graph registry ID or snapshot reference, request ID,
  mission ID, actor, device role, approval level, connector profile IDs, stop
  triggers, and source commit/state references;
- reject raw secret-looking fields, raw logs, client-data-full payloads,
  unapproved live connector actions, and stale/superseded approval records;
- add tests before any hosted relay or phone UI exists.

That gives UAOS a concrete contract before adding infrastructure. The next
safe implementation chunk is a local relay record store and worker-claim proof
that persists validated relay records and rejects stale or conflicting worker
claims without introducing hosted relay infrastructure.
