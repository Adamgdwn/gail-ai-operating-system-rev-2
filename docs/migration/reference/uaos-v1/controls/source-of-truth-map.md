# Source Of Truth Map

Created: 2026-06-02T22:16:05-06:00
Last Updated: 2026-06-14T19:22:11-06:00
Status: active navigation
Owner: Adam Goodwin

## Purpose

This map makes the operating-layer documents easier to follow without deleting history.

Use it when you need to know which document controls the current path, which document records evidence, and which older artifacts should be opened only when relevant.

## Open First

| Order | Document | Use it for |
|---|---|---|
| 1 | `START_HERE.md` | Fast project orientation and current priorities. |
| 2 | `docs/specs/guided-ai-labs-flagship-build-plan.md` | Clear forward pathway, chunk order, rules, risks, and build gates. |
| 3 | `docs/specs/uaos-final-shippable-plan.md` | Bounded v1 finish line, final stages, authorized surfaces, acceptance tests, and stop conditions. |
| 4 | `docs/turnover-2026-06-14.md` | Clean pause/resume note after the heavy build day. |
| 5 | `docs/current-build-pathway.md` | Detailed ledger, completed chunks, validation log, and handoff. |
| 6 | `docs/manual-operating-cockpit.md` | Current focus, next best actions, waiting items, drift alerts, and active artifact. |
| 7 | `docs/request-log.md` | Compact index of request records and next actions. |

## Active Operating Rules

| Document | Controls |
|---|---|
| `project-control.yaml` | Governance level, risk tier, required controls, exceptions, and data/money posture. |
| `AGENTS.md` | Agent working rules, preflight, timestamping, and commit/push semantics. |
| `docs/context-map.md` | Short routing map for scoped context loads, task-specific reads, and context hygiene. |
| `docs/standards/README.md` | Local engineering standards index for meaningful coding and agent work. |
| `docs/standards/context-hygiene-standard.md` | Context windows, token budgets, scoped reads, compaction, and handoff practice. |
| `docs/policy/durable-development-engineering-policy.md` | Durable development policy: smallest useful thing in the safest durable way. |
| `docs/standards/engineering-governance-by-use-case.md` | Use-case governance expectations, including AI agents with tools. |
| `docs/standards/ai-agent-governance-standard.md` | Required records and controls for agentic systems. |
| `docs/decisions/ai-agent-governance-posture.md` | Current governance mismatch warning and selected agent-control posture. |
| `docs/agent-inventory.md` | Active agent inventory and required design decisions. |
| `docs/model-registry.md` | Model route registry and model change rules. |
| `docs/prompt-register.md` | Prompt and instruction register. |
| `docs/tool-permission-matrix.md` | Tool permissions, prohibited actions, approval requirements, and failure behavior. |
| `docs/evaluation-approach.md` | Initial evaluation approach and regression triggers. |
| `docs/agent-oversight-and-disable-procedure.md` | Oversight, escalation, rollback, and disable procedure. |
| `docs/agent-runtime-instructions.md` | Active instructions for the deterministic local mission spine. |
| `uaos_agent_spine/` | Chunk 15 local mission schema, planner, policy gate, dry-run executor, action log, and runtime coordinator. |
| `scripts/run-agent-spine.py` | Dry-run CLI for local mission spine smoke checks. |
| `tests/test_safety_evaluations.py` | Chunk 17 automated safety evaluations for stop triggers, future connector boundaries, Graphify boundaries, raw voice retention, reviewed outputs, and recursive log redaction. |
| `uaos_agent_spine/graphify_handoff.py` | REQ-0050 local, no-network Graphify handoff validator/parser. |
| `tests/test_graphify_handoff.py` | REQ-0050 tests for handoff validation, rejection reasons, and dry-run-only policy behavior. |
| `uaos_agent_spine/graphify_adapter.py` | REQ-0053 live read-only Graphify handoff endpoint consumer. |
| `tests/test_graphify_adapter.py` | REQ-0053 tests for URL/header behavior, ETag no-change handling, transport failures, and validator integration. |
| `uaos_agent_spine/connector_registry.py` | REQ-0052 local, no-network connector profile and Client Gateway readiness validator. |
| `tests/test_connector_registry.py` | REQ-0052 tests for initial profiles, unsafe live access, signed-scope gates, and full-assessment readiness. |
| `uaos_agent_spine/relay_envelope.py` | REQ-0055 local, no-network relay envelope validator for future device/cockpit records. |
| `tests/test_relay_envelope.py` | REQ-0055 tests for safe relay summaries, graph snapshots, device roles, stale state, connector IDs, live-action rejection, M365 planning-only posture, Client Gateway stops, and outbound-worker assumptions. |
| `docs/mandatory-request-artifacts.md` | Required artifacts by request tier. |
| `docs/conventions/timestamp-status-convention.md` | Timestamp and status conventions. |
| `docs/specs/compact-request-intake-shape.md` | Current manual intake shape for rough intent -> governed request record. |
| `docs/specs/model-connector-os-intake-blueprint.md` | Hidden model routes, connector profiles, OS/workspace spokes, voice intake, and Client Gateway assessment boundary. |
| `docs/specs/cross-device-source-of-truth-foundation.md` | Multi-device, multi-OS, company-wide source-of-truth contract and device-role baseline. |
| `docs/specs/shared-relay-phone-cockpit-architecture.md` | Shared relay and phone/tablet cockpit architecture; GitHub-backed interim relay first, hosted relay later only as a coordination cache. |
| `docs/specs/uaos-final-shippable-plan.md` | Bounded UAOS v1 finish-line plan, authorized surfaces, final stages, acceptance tests, stop conditions, and post-v1 parking lot. |
| `docs/turnover-2026-06-14.md` | Repo-local closeout and resume note for the current pause. |
| `docs/specs/graphify-handoff-read-only-adapter-prep.md` | UAOS-side Graphify handoff validation and read-only adapter preparation. |
| `docs/specs/graphify-handoff-live-read-only-adapter.md` | UAOS-side live read-only adapter for pulling Graphify handoff records into validation. |
| `docs/specs/microsoft-365-business-environment-boundary.md` | Planning-only M365 business-environment boundary, first candidate connector profile, capability ladder, prohibited actions, and stop triggers. |
| `docs/specs/connector-registry-client-gateway-boundary.md` | Concrete connector records and Client Gateway readiness boundary before live connector activation or full client-data assessment. |
| `docs/specs/autonomous-mission-envelope-weekend-proof.md` | Approved autonomy boundary and stop-for-approval triggers for Chunk 10. |
| `apps/cockpit-command-proof/` | Hardened local software proof of the cockpit command loop. |
| `scripts/launch-cockpit.*` | Cross-platform launchers for the local cockpit runner. |
| `scripts/check-tool-spokes.py` | Presence-only readiness checker for external tool spokes. |
| `docs/specs/approved-tool-spokes-first-proof.md` | First tool-spoke readiness and permission spec. |
| GitHub issue `Adamgdwn/user-ai-operating-system#1` | First executable external spoke proof in the private repo. |

## Build Readiness Sources

Open these before choosing or implementing the first software surface.

| Document | Why it matters |
|---|---|
| `docs/decisions/portal-as-ai-native-environment.md` | Confirms the portal/workbench is required, not optional. |
| `docs/guided-ai-labs-portal-end-state-vision.md` | Describes the end-state cockpit/workbench. |
| `docs/specs/portal-mvp-discovery-questions.md` | Lists questions to answer before portal design or implementation. |
| `docs/specs/portal-mvp-cockpit-field-assessment.md` | Identifies the first MVP surface as request-and-focus, not a broad dashboard wrapper. |
| `docs/specs/adaptive-cockpit-logic-and-learning.md` | Defines adaptive context, tools, approvals, validation, learning, and artifact behavior. |
| `docs/specs/manual-learning-classifications.md` | Controls learning hygiene before persistent memory or automation. |
| `docs/specs/manual-subscription-vendor-register.md` | Controls vendor/subscription proof before account or billing integrations. |
| `docs/specs/manual-vendor-register-learning-test.md` | First safe sample testing register fields and learning classifications. |
| `docs/specs/graphify-workspace-cockpit-uaos-integration.md` | Graphify Workspace Cockpit as knowledge lookup/optimization spoke and Microsoft 365 as future business-environment spoke. |
| `docs/specs/graphify-handoff-read-only-adapter-prep.md` | UAOS-side validation rules for Graphify handoff records. |
| `docs/specs/graphify-handoff-live-read-only-adapter.md` | UAOS-side live read-only adapter for the Graphify handoff endpoint. |
| `docs/specs/microsoft-365-business-environment-boundary.md` | M365 surface inventory, capability ladder, planning-only connector profile, and live-access stop triggers before any tenant/content/communication/admin work. |
| `docs/specs/model-connector-os-intake-blueprint.md` | Route-based model planning, connector registry shape, voice-first intake, employee/customer surface split, and isolated Client Gateway assessment flow. |
| `docs/specs/connector-registry-client-gateway-boundary.md` | Concrete connector registry records and full-assessment readiness rules before any live connector activation or client-data gateway assessment. |
| `docs/specs/cross-device-source-of-truth-foundation.md` | Android/tablet/phone, Windows, Linux, hosted relay, M365, Graphify, and client workspace source-of-truth rules. |
| `docs/specs/shared-relay-phone-cockpit-architecture.md` | Chunk 18 relay/device architecture before hosted relay, phone UI, worker poller, tunnel, or cross-device approval implementation. |
| `docs/specs/uaos-final-shippable-plan.md` | The final shippable-stage sequence before adding more v1 work or claiming release readiness. |
| `docs/standards/` | Local standards copied from the New Build Agent standards source in Chunk 13 and refreshed with the context-hygiene baseline in REQ-0044. |

## Product And Boundary Sources

Open these before changing public paths, offers, client workspaces, or Freedom integration.

| Document | Use it before |
|---|---|
| `docs/decisions/freedom-master-cockpit-guided-ai-labs-domain.md` | Freedom coupling, portal architecture, personal/business boundaries, or client hub strategy. |
| `docs/freedom-guided-ai-labs-boundary.md` | Any shared-runtime or implementation dependency with Freedom. |
| `docs/specs/client-entry-offer-pathway-package.md` | Public offers, entry paths, payment/fit flow, or Client Gateway positioning. |
| `docs/specs/client-pathway-product-structure.md` | Guided AI Journey, OldSkoolAI.com, reusable tools, website flows, or Client Gateway handoffs. |
| `docs/client-pathway-architecture.md` | Customer pathway changes. |
| `docs/personal-business-ai-native-ecosystem-architecture.md` | Personal/business ecosystem and hub-and-spoke changes. |
| `docs/decisions/website-operating-layer-boundary.md` | Website work or public intake changes. |

## Evidence Archive

These are supporting evidence, not first-stop navigation.

| Area | Documents |
|---|---|
| Request history | `docs/requests/` |
| Local proof apps | `apps/` |
| Client-readiness method | `docs/client-readiness/` |
| Diagrams | `docs/*architecture*.md`, `.svg`, and `.png` files |
| Templates | `docs/templates/` |
| Risks and operations | `docs/risks/risk-register.md`, `docs/runbook.md`, `docs/deployment-guide.md`, `docs/CHANGELOG.md` |

## Build Gate

The project has its first hardened local software proof at
`apps/cockpit-command-proof/`, with launchers in `scripts/launch-cockpit.*`.
Tool-spoke readiness is checked with `scripts/check-tool-spokes.py`.
The first executable external spoke proof created private GitHub issue #1.
Chunk 12 completed the manual vendor-register and learning test. Chunk 13
completed local standards alignment. Chunk 14 completed agent control records.
Chunk 15 completed the deterministic local functional agent spine. REQ-0044
incorporated the New Build Agent context-map and context-hygiene governance
updates. REQ-0045 captured Graphify Workspace Cockpit as the knowledge
lookup/optimization spoke and Microsoft 365 as a future governed business
environment spoke. REQ-0046 captured the model, connector, OS, voice intake,
and Client Gateway assessment blueprint. REQ-0047 completed the first GitHub
adapter foundation. REQ-0048 captured the cross-device source-of-truth
foundation. REQ-0049 completed the first automated safety evaluation set.
REQ-0050 completed the UAOS-side Graphify handoff read-only adapter prep with a
local validator and tests. REQ-0051 completed the Microsoft 365
business-environment boundary and explicit M365 stop-trigger safety checks.
REQ-0052 completed the connector registry and isolated Client Gateway
assessment readiness boundary. REQ-0053 completed the live read-only Graphify
handoff adapter. REQ-0054 completed the shared relay and phone/tablet cockpit
architecture, choosing GitHub-backed interim relay records before custom hosted
relay infrastructure. REQ-0055 completed the local no-network relay envelope
validator before any hosted relay, global cockpit UI, phone UI, tunnel, or
persistent worker service. REQ-0056 completed local relay record persistence
and worker-claim/reconciliation proof before any shared relay service or UI
surface. REQ-0057 added the bounded UAOS final shippable plan, freezing v1
scope around authorized surfaces, final stages, acceptance tests, and stop
conditions. REQ-0058 added the clean closeout/turnover note and shared
work-tracking entries before pausing.

Before running the next autonomous proof, confirm:

1. the selected mission is concrete enough to test in one chunk;
2. Adam has approved the mission envelope: allowed actions,
   stop-for-approval triggers, tools, approvals, validation, rollback, and
   stopping points;
3. the software surface supports cockpit command, planning, execution,
   validation, and learning rather than becoming a generic dashboard;
4. live billing changes, production payment changes, public production launch,
   client data, destructive account changes, and Freedom runtime coupling stop
   for Adam approval under the approved envelope;
5. validation and handoff defaults are clear enough to support autonomous work
   inside the approved boundary.

## Next Action

Use this map and `docs/context-map.md` to keep future sessions short. For the
next relay, cockpit, phone/tablet, or M365 activation turn, review
`docs/specs/uaos-final-shippable-plan.md`,
`docs/specs/graphify-workspace-cockpit-uaos-integration.md`,
`docs/specs/graphify-handoff-live-read-only-adapter.md`,
`docs/specs/connector-registry-client-gateway-boundary.md`,
`docs/specs/shared-relay-phone-cockpit-architecture.md`,
`docs/specs/model-connector-os-intake-blueprint.md`,
`docs/specs/cross-device-source-of-truth-foundation.md`,
`docs/specs/microsoft-365-business-environment-boundary.md`,
`uaos_agent_spine/relay_envelope.py`, `uaos_agent_spine/relay_store.py`,
`tests/test_relay_envelope.py`, and `tests/test_relay_store.py`.
Before any model
route, connector registry, voice intake, BYOK, client-stack, or Client Gateway
assessment work, review `docs/specs/model-connector-os-intake-blueprint.md` and
the REQ-0052 connector boundary.
