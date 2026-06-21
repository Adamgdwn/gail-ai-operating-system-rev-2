# Tool Permission Matrix

Created: 2026-06-21T14:12:35-06:00
Last Updated: 2026-06-21T14:16:18-06:00
Status: active control
Owner: Adam Goodwin

## Purpose

This matrix defines the current Rev 2 permissions for tools, devices,
connectors, and worker surfaces used by GAIL AI Operating System Rev 2.

It promotes the copied UAOS v1 permission matrix into active Rev 2 controls
without activating any live business connector, payment system, client data
flow, hosted relay, or autonomous runtime.

## Current Posture

- Project classification: AI agent with tools.
- Selected risk tier: `low`.
- Selected governance level: `1`.
- Runtime autonomy: `A1`.
- Current source of truth: the private GitHub repository
  `Adamgdwn/gail-ai-operating-system-rev-2`, branch `main`, plus active Rev 2
  control records.
- Current execution mode: docs, planning, local validation, local file edits,
  Git/GitHub chunk closeout, and reference migration only.
- Live Microsoft 365, QuickBooks, finance, billing, client-data, vendor,
  infrastructure, hosted-relay, and production actions remain blocked until a
  later explicit boundary is approved.

## Default Rule

If a tool operation is not explicitly allowed here, treat it as not allowed and
stop for Adam approval before execution.

This matrix does not grant credentials, tenant access, business-system access,
client-data access, production access, or autonomous execution authority by
itself.

## Permission Principles

- Prefer read-only inspection before mutation.
- Keep planning separate from execution for risky actions.
- Keep secrets, raw credentials, raw logs, raw audio, and unredacted sensitive
  payloads out of the repo and out of summaries.
- Preserve unrelated user work.
- Record validation, stop reasons, and recovery notes in durable docs when a
  chunk changes controls.
- Use explicit owner approval for destructive, external, public, production,
  money, permission, account, tenant, or client-data actions.

## Tool Matrix

| Tool or surface | Purpose | Allowed now | Prohibited until later approval | Approval required | Stop behavior |
|---|---|---|---|---|---|
| Local repo filesystem | Maintain Rev 2 docs, controls, and future code inside this repository. | Read repo files; create or update active docs, specs, request records, tests, local source files, and generated artifacts in approved repo paths. | Read unrelated repos without task reason; write outside the repo; delete user or agent work without explicit instruction; store secrets or raw sensitive data. | Destructive changes, broad filesystem access, sensitive data, or writes outside the repo need explicit approval. | Stop on path ambiguity, unrelated dirty changes that affect the task, sensitive file discovery, or permission uncertainty. |
| Local shell | Run local validation, inspection, and development commands. | `bash scripts/governance-preflight.sh`, schema validation, `git diff --check`, local tests, safe read-only inspection, local non-sensitive dev-server startup when a future app needs it. | Destructive commands, system-wide changes, unbounded scans, secret printing, credential extraction, live connector calls, or persistent services without a boundary. | Destructive/system-wide actions, persistent services, unexpected cost, sensitive data exposure, or privilege changes need explicit approval. | Capture command/result; stop if failure implies risk outside the active chunk. |
| Git | Version control and chunk evidence. | `status`, `diff`, `log`, scoped `add`, commit, push, and non-destructive branch inspection. | `reset --hard`, rewriting history, reverting unrelated work, force-push, deleting branches, or hiding dirty state. | Chunk closeout may commit and push scoped files; destructive Git requires explicit approval. | Stop on mixed unrelated changes that affect the task or a push/remote mismatch. |
| GitHub private remote | Durable private source and future issue/PR evidence. | View private repo metadata; push approved chunk commits; create or update issues, PRs, releases, or labels only when a later chunk explicitly includes that action. | Public repo exposure, repo deletion, repo visibility changes, destructive settings, public release promotion, or storing secrets in GitHub records. | Routine chunk push is allowed by the closeout protocol; issues, PRs, releases, settings, visibility, or destructive actions require explicit task approval. | Stop on auth, visibility, public exposure, secret, unsupported capability, or destructive-setting ambiguity. |
| Active governance docs | Define project controls, pathway, risk posture, and handoffs. | Update active docs when the chunk explicitly changes controls or handoff state. | Silently changing selected risk tier, governance level, owner decisions, or release readiness claims. | Owner approval required before changing selected `risk_tier`, `governance_level`, or any live connector/data classification. | Stop on governance mismatch, missing required doc, or unclear owner decision. |
| Copied v1 reference docs | Provide local evidence and design input from the superseded UAOS v1 workspace. | Read copied reference docs when a promotion chunk calls for them; cite what was promoted or superseded. | Treat copied references as active controls; continue Rev 1 implementation; copy code or artifacts before migration is approved. | Approval required for new reference copying from outside Rev 2 or any code migration chunk. | Stop when a reference contradicts active Rev 2 controls and record the decision path. |
| DirectLink / Linux tunnel | Transport, status, and reference access only. | Use for explicit cross-machine status or file handoff when a chunk calls for it. | Make DirectLink the project home, rely on tunnels for the normal Rev 2 workflow, copy secrets into the repo, or keep Linux v1 as active source. | Cross-machine file movement, secret archive handling, or worker bootstrap needs explicit chunk scope and approval. | Stop on source-of-truth ambiguity, secret exposure risk, or tunnel dependency. |
| Windows operator workspace | Current local editing and validation environment. | Edit Rev 2 repo, run local validation, push private GitHub commits, and operate future local proof apps. | Live business connectors, broad local filesystem reads, credential extraction, system-wide changes, or unapproved background services. | Privileged operations, persistent services, or live connector use require explicit approval. | Stop on privilege, persistence, filesystem, credential, or live-system ambiguity. |
| Linux worker or reference host | Superseded v1 reference host and future trusted worker candidate. | Read copied references in Rev 2; later pull private GitHub into a worker clone after bootstrap controls exist. | New Rev 1 implementation, tunnel-dependent operation, unattended worker polling, live connector use, or treating Linux as the active source. | Worker bootstrap, persistent worker service, connector access, or direct file migration requires explicit approval. | Stop on stale clone, source divergence, unapproved service, or worker identity ambiguity. |
| Android phone and tablet portal | Future mobile cockpit for intent, approval, status, and evidence review. | Planning-only until portal chunks; future approved UI may show safe summaries and collect explicit operator decisions. | Local shell execution, raw secrets/logs/audio, direct connector access, stale approval reuse, or unrestricted worker control. | Live approval actions, hosted relay access, push notifications, or mobile write authority require explicit boundary approval. | Stop on device identity, stale state, raw payload, or approval ambiguity. |
| Browser portal | Shared cockpit surface across desktop and mobile. | Future local or hosted UI for safe mission records, status, approvals, and evidence. | Becoming a second source of truth, bypassing server/worker permission checks, exposing secrets, or executing live connectors directly. | Hosted portal, authentication, write-capable approval flows, or production deployment require explicit approval. | Stop on auth, data exposure, routing, or source-of-truth ambiguity. |
| Relay envelopes and cockpit records | Future coordination records for devices and workers. | Locally validate no-network record shapes in approved chunks; persist non-sensitive proof records only after schema and store are promoted. | Hosted relay, persistent worker polling, public inbound worker access, raw secrets, raw credentials, raw logs, raw audio, full client payloads, stale approvals, or duplicate accepted worker claims. | Hosted relay, phone write authority, persistent services, worker polling, production action, or external communication require explicit approval. | Stop on stale state, unknown device, unsafe summary, duplicate claim, hosted-relay scope, or connector ambiguity. |
| Tool Directory and connector registry | Describe possible tools and future connector profiles. | Maintain link-only records, local schemas, owners, capabilities, data classes, approval gates, retention, maturity, and failure behavior. | Treat registry entries as credentials, live access, or permission to call external systems. | Any live connector, write-capable profile, client data flow, BYOK provider, or external side effect requires explicit approval and updated controls. | Stop if owner, tenant/workspace, data class, retention, approval gate, or audit path is unclear. |
| Graphify | Knowledge graph and routing spoke. | Use approved graph summaries or handoff records before broad exploration when available; update relevant graph only when policy and tooling are available and the chunk warrants it. | Index secrets, broad-read raw source without need, mutate source through Graphify, upload graphs, or treat recommendations as execution approval. | Full semantic rebuilds, new roots, graph upload, or action execution require explicit approval or active chunk scope. | Stop if graph source, selected root, evidence sensitivity, or recommendation/action boundary is unclear. |
| AI model providers and coding agents | Planning, drafting, coding, review, and local validation support. | Use current assistant/coding tools for scoped repo work under active instructions; treat generated output as untrusted until reviewed and validated. | Send secrets, raw client data, raw logs/audio, or confidential business-system content to unapproved providers; silently escalate autonomy. | New model route, BYOK provider, sensitive-data use, or autonomous runtime behavior requires explicit controls and approval. | Stop on data-class uncertainty, prompt-injection risk, provider boundary, or autonomy ambiguity. |
| Browser verification tools | Validate local or preview UI behavior in future portal chunks. | Open local apps, inspect screenshots, run smoke checks, and record non-sensitive results. | Capture sensitive data, interact with private/client accounts, or operate live business systems without approval. | Sensitive/private targets, authenticated external accounts, or production validation require explicit approval. | Stop if the page reveals sensitive data unexpectedly or the target is not clearly approved. |
| Microsoft 365 business environment | Future workspace spoke for Entra, SharePoint, OneDrive, Teams, Outlook, calendar, Planner/To Do, Lists, and documents. | Planning-only. Future inventory-only access must have its own connector boundary and approval. | Reading email, calendar, Teams, SharePoint, OneDrive, documents, or client content; sending/posting messages; creating records; syncing/indexing content; changing tenant, account, security, billing, admin, permission, or sharing settings. | Explicit Adam approval, connector profile, updated data classification, retention/audit rule, and tool permission update required before live access. | Stop on auth, privacy, identity, tenant, communication, content-read, retention, sharing, client-data, admin, or permission ambiguity. |
| QuickBooks, accounting, finance, billing, and payments | Future business/accounting surfaces. | Planning-only until a dedicated boundary exists. | Reading accounting records, invoices, payments, billing exports, vendor bills, bank data, tax records, or making money movement/account changes. | Explicit approval, stronger governance review, least-privilege connector profile, audit path, and rollback/recovery notes required before any live access. | Stop on money, billing, account ownership, client/vendor data, compliance, or irreversible-action ambiguity. |
| Client Gateway assessment workspace | Future isolated workspace for client-data assessment. | Planning-only and local readiness notes only. | Creating client workspaces automatically, accessing client data, exposing unreviewed AI findings, mixing clients, retaining raw audio by default, or connecting live client systems. | Guided AI Labs governance approval required before any live client-data assessment. | Stop on client identity, workspace isolation, connector approval, retention, visibility, or public-intake sensitivity ambiguity. |
| AWS, Dropbox, vendor APIs, and deployment providers | Future infrastructure, storage, vendor, and deployment connectors. | Planning-only profiles and presence checks without secret printing. | Reading private accounts, changing infrastructure, creating paid resources, modifying IAM/security/billing, changing sharing, deleting files, launching production, or changing DNS/domains. | Explicit approval, connector profile, least-privilege scope, logging, cost review, and rollback plan required before live access. | Stop on cost, IAM, production, region, sharing, ownership, retention, data, or reversibility ambiguity. |
| Voice intake and transcription | Future voice-first intake surface. | Planning-only; future approved capture may retain transcript and structured fields by default if the boundary allows it. | Retaining raw audio, transcribing unapproved client data, creating client-visible findings, or using voice without consent and retention rules. | Explicit approval required for raw audio retention; governance review required before transcript-derived findings become client-visible. | Stop on consent, retention, speaker identity, workspace, or data-class ambiguity. |

## Action Risk Tiers

| Tier | Action type | Current Rev 2 posture |
|---|---|---|
| Tier 0 | Read-only, low sensitivity | Allowed when relevant to the active chunk and logged in validation or handoff notes where material. |
| Tier 1 | Read private repo or internal non-secret docs | Allowed when relevant to the active chunk; do not broaden into unrelated repos or sensitive stores. |
| Tier 2 | Draft action, local doc/code edit, or proposed tool change | Allowed inside scoped chunks; validate before closeout. |
| Tier 3 | External reversible action | Requires explicit boundary, action summary, confirmation, audit note, and recovery path. |
| Tier 4 | Destructive, public, production, permission, infrastructure, tenant, account, or provider action | Stop for explicit Adam approval, dry-run where practical, and rollback or recovery notes. |
| Tier 5 | Irreversible or high-stakes action involving money, legal, HR, public communications, safety, client-visible findings, or sensitive production data | Human decision required; the agent may assist only with planning, drafting, validation, or evidence gathering. |

## Required Future Adapter Behavior

Every future tool adapter must:

- validate arguments before calls;
- support dry-run where practical;
- log a safe action summary, target, result, and stop reason;
- avoid logging secret values, including values nested inside arguments,
  summaries, results, and validation fields;
- map failures to retry, stop, rollback, or recovery notes;
- expose user-visible summaries before and after execution;
- respect stale-state checks before acting on approvals or relay records;
- fail closed when connector scope, identity, data class, or approval state is
  unclear.

## Promotion Notes

This active matrix was rewritten from
`docs/migration/reference/uaos-v1/controls/tool-permission-matrix.md` for the
Rev 2 repository. The copied v1 file remains reference-only and is no longer
the active permission source.
