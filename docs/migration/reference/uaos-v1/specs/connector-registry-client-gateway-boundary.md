# Connector Registry And Client Gateway Boundary

Created: 2026-06-14T14:00:57-06:00
Last Updated: 2026-06-14T16:44:31-06:00
Status: active boundary; local validation only
Owner: Adam Goodwin

## Purpose

This boundary turns the REQ-0046 model, connector, OS, and intake blueprint into
concrete local records for connector profiles and isolated Client Gateway
assessment readiness.

This chunk does not enable live Microsoft 365, Graphify API, AWS, Dropbox,
BYOK, voice/transcription, client-stack, or Client Gateway access.

## Core Rule

A connector profile is permission structure, not permission.

The registry can describe a future connector, validate that the record has the
right owner/workspace/data/approval/retention/failure fields, and block unsafe
activation. It must not be treated as a credential, live adapter, customer
workspace, or approval to read client data.

## Local Implementation

REQ-0052 adds:

- `uaos_agent_spine/connector_registry.py`
- `tests/test_connector_registry.py`

The module is local and no-network. It defines:

| Interface | Purpose |
|---|---|
| `ConnectorProfile` | Governed record for a tool, workspace, OS, provider, or client stack. |
| `validate_connector_profile` | Checks required profile fields and rejects unsafe live-enabled or weak client-controlled profiles. |
| `initial_connector_profiles` | First registry records for GitHub, Graphify, Microsoft 365, local OS, AWS, Dropbox, and future client stack. |
| `AssessmentWorkspace` | Readiness record for a future isolated Client Gateway workspace. |
| `validate_assessment_workspace` | Checks scope, roles, retention, connector approvals, data class, review, public-intake, and raw-audio rules. |

## Initial Connector Records

| Connector ID | Family | First maturity | Current live access | Boundary |
|---|---|---|---|---|
| `github-uaos-private-repo` | GitHub | `dry-run` | No by default | Existing narrow issue adapter; broader operations need later profiles. |
| `graphify-workspace-cockpit-handoff` | Graphify | `read-only` | REQ-0053 adapter reads the handoff endpoint only | Graphify Chunk 11 exposes a handoff endpoint; UAOS consumes it through the read-only adapter and still stops before execution. |
| `m365-guided-ai-labs-business` | Microsoft 365 | `planning-only` | No | No Outlook, Teams, SharePoint, OneDrive, calendar, task, tenant, Entra, admin, or billing access. |
| `local-os-trusted-worker-surfaces` | Local OS | `registry-only` | No new power | Local launch/control surfaces only; persistent services or privileged operations need approval. |
| `aws-future-infrastructure-or-client-stack` | AWS | `planning-only` | No | No account read, IAM, billing, resource, infra, or client-data access. |
| `dropbox-future-document-storage` | Dropbox | `planning-only` | No | No private file reads, sync, sharing, deletion, or client document access. |
| `client-stack-gateway-template` | Client Stack | `planning-only` | No | Template only; requires signed scope and Client Gateway boundary before use. |

## Graphify Boundary Check

Before this chunk, UAOS checked the Graphify Workspace Cockpit repo at:

```text
/home/adamgoodwin/code/agents/graphify-workspace-cockpit
```

The cockpit now records Chunk 11 complete and includes the read-only UAOS
handoff endpoint:

```text
GET /actions?status=executed&format=uaos
```

UAOS should therefore treat Graphify as handoff-capable, but still as a
knowledge spoke. The next UAOS Graphify step is a read-only API consumer that
wraps the existing REQ-0050 validator. Graphify decisions, recommendations, and
actions still do not approve UAOS execution.

## Client Gateway Assessment Boundary

Full client-data assessment can begin only when an `AssessmentWorkspace` record
is ready for full assessment.

Required before full assessment:

- client owner;
- Guided AI Labs owner;
- signed scope record;
- isolated workspace boundary;
- roles for Guided AI Labs owner, Guided AI Labs operator, client owner, and
  client sponsor;
- retention/archive/delete rule;
- approved connector profile IDs;
- connector approval state recorded as approved;
- explicit `client-controlled` data class;
- AI outputs marked as review-required before client visibility;
- public intake confirmed non-sensitive;
- raw audio retention set to `none` unless separately approved.

Public prospect intake can remain light and non-sensitive. It is not full
assessment readiness, and it must not auto-create a workspace.

## Stop Triggers Added

REQ-0052 adds a runtime stop action type:

| Action type | Stops when |
|---|---|
| `client_gateway_workspace_creation_without_boundary` | A command asks to create, open, provision, activate, or automatically create a Client Gateway/client workspace before scope, workspace setup, roles, retention, and connector approvals exist. |

Existing stop triggers still cover full client-data assessment, live connector
access, raw voice retention, and unreviewed client-visible AI findings.

## Approval Ladder

Registry records may move through this order only through later approved chunks:

1. `planning-only`
2. `inventory-only`
3. `metadata-read`
4. `content-read`
5. `summarize`
6. `draft-only`
7. `prepare-action`
8. `execute-after-approval`

Live connector activation requires a separate profile activation chunk, updated
tool permission matrix, evaluation coverage, audit path, and explicit Adam or
Guided AI Labs governance approval.

## Governance Note

Selected posture remains unchanged:

- `risk_tier: medium`
- `governance_level: 2`
- runtime autonomy: `A1`

This remains a governance mismatch warning for future live connectors and
client-data assessment. Stronger controls are recommended before live client
data, M365 content, external communications, provider credentials, or write
capabilities.

## Next Chunk

REQ-0053 completed the live read-only Graphify handoff adapter. REQ-0054
completed the shared relay and phone/tablet architecture.

The clean next implementation chunk is a local no-network relay envelope
validator before any hosted relay, phone UI, tunnel, persistent worker service,
or live connector expansion.
