# Model Registry

Created: 2026-06-21T14:42:00-06:00
Last Updated: 2026-06-21T14:46:16-06:00
Status: active control
Owner: Adam Goodwin

## Purpose

This registry records model routes approved for GAIL AI Operating System Rev 2.

It is a permission control, not a credential record. Do not store API keys,
tokens, tenant IDs, secrets, client data, raw logs, raw audio, or provider
account details here.

## Current Model Posture

Rev 2 has no approved production runtime model route yet.

The current coding session may use the available Codex assistant surface only
for repo-scoped planning, drafting, code/doc edits, and local validation under
the active repository instructions. That use does not authorize future hosted
model calls, BYOK provider use, client-data processing, live connector
execution, or autonomous runtime behavior.

## Model Routes

| Model route ID | Provider or surface | Status | Approved use | Data allowed | Explicitly blocked | Review trigger |
|---|---|---|---|---|---|---|
| MR-001 | Current Codex coding session | Active for repo collaboration | Human-directed local repository planning, drafting, edits, validation summaries, and chunk closeout. | Non-sensitive Rev 2 repository content and copied v1 reference docs already in the repo. | Secrets, raw credentials, raw logs, raw audio, client data, Microsoft 365 content, QuickBooks/accounting data, billing/payment data, vendor account data, and production operations. | Any change to data class, autonomy, provider, retained logs, live connector use, or production runtime behavior. |
| MR-002 | Rev 2 production runtime model | Not approved | None yet. | None yet. | All runtime model execution, hosted inference, persistent agent loops, and connector-driving model calls. | Future architecture and model-selection decision record. |
| MR-003 | BYOK or third-party model provider | Not approved | None yet. | None yet. | Provider credentials, external uploads, sensitive data processing, or account configuration. | Explicit provider decision, privacy review, cost review, and updated permission matrix. |

## Future Model Approval Requirements

A future model route must record:

- purpose and owner;
- provider and deployment boundary;
- approved data classes;
- prohibited data classes;
- retention and logging posture;
- prompt-injection and tool-use boundaries;
- evaluation or test expectations;
- rollback or disable path;
- approval date and review trigger.

## Promotion Notes

This registry replaces the scaffold example row and preserves the current
`A1`, no-live-runtime posture.
