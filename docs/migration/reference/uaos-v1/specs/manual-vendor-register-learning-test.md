# Manual Vendor Register And Learning Test

Created: 2026-06-06T20:37:32-06:00
Completed: 2026-06-06T20:40:01-06:00
Status: complete test artifact
Owner: Adam Goodwin

## Purpose

This artifact tests Chunk 12 without connecting live billing, account exports,
credentials, vendor APIs, bank feeds, invoices, or client-controlled data.

It uses a small non-sensitive sample to answer whether the manual subscription
and vendor register fields are usable, and whether the manual learning
classification set captures the right product signals before automation.

## Scope Boundary

Allowed in this test:

- use known public/vendor names or tools already visible in repo context;
- leave cost fields blank unless already safe and non-sensitive;
- mark account, billing, API, and access details as unknown when not safely
  verified;
- record field friction and learning classifications.

Not allowed in this test:

- live billing review;
- invoice, receipt, card, bank, or accounting-source review;
- vendor account login or settings changes;
- purchasing, cancellation, downgrade, upgrade, or subscription changes;
- API calls to vendor accounts;
- credential values;
- client-controlled vendor data.

## Sample Register

This sample is intentionally conservative. It is not an approved vendor list,
spend ledger, or account inventory.

| Vendor name | Service/product | Category | Purpose | Owner | Status | Type | Expected cost | Verified actual cost | Cost status | Billing source | Renewal/review date | Account access | Data export | API access | Access status | Usage confidence | Better-deal status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GitHub | Private repository and development workflow | Business operations | Source control, issue tracking, and release path for the operating-system repo | Adam Goodwin | Approved | Unknown |  |  | Needs source | Unknown | 2026-07-06 | Admin portal | Unknown | Available | Partial | High | Not reviewed | Already used for private repo and issue proof; cost/access not verified in this test. |
| OpenAI | AI model/API platform | AI model or agent platform | AI-assisted development and future operating-loop intelligence | Adam Goodwin | Watch | Usage-based |  |  | Needs source | Unknown | 2026-07-06 | Unknown | Unknown | Available | Unknown | High | Not reviewed | Useful but needs finance, account, and data-access review before vendor automation. |
| Vercel | Preview deployment candidate | Infrastructure and hosting | Candidate preview deployment path for cockpit or portal surfaces | Adam Goodwin | Candidate | Unknown |  |  | Needs source | Unknown | 2026-07-06 | Unknown | Unknown | Unknown | Unknown | Unknown | Not reviewed | Readiness script found token presence but local CLI missing; no deployment used in this test. |
| Supabase | Database/auth/storage candidate | Infrastructure and hosting | Candidate backend platform for future portal capabilities | Adam Goodwin | Candidate | Unknown |  |  | Needs source | Unknown | 2026-07-06 | Unknown | Unknown | Unknown | Unknown | Unknown | Not reviewed | Readiness script found token presence but local CLI missing; no project/resource work used in this test. |
| Microsoft | Outlook / Microsoft workspace tools | Business operations | Email, calendar, documents, and possible client/workspace operations | Adam Goodwin | Watch | Unknown |  |  | Needs source | Unknown | 2026-07-06 | Unknown | Unknown | Unknown | Unknown | Medium | Not reviewed | Mentioned as preferred email/calendar workflow family; account and cost not reviewed. |

## Field Test Findings

| Question | Finding | Handling |
|---|---|---|
| Are the fields too many, too few, or unclear? | The fields are broad but usable for a careful first-pass review. They are too wide for a compact cockpit card. | Keep the full table as an audit/detail view; future cockpit should show only status, purpose, cost status, access status, review date, and next action. |
| Which fields are hard to fill without sensitive data? | Expected cost, verified actual cost, billing source, account access, data export, and renewal date. | Default these to blank or unknown until a safe source is intentionally reviewed. |
| Which fields should appear in the future cockpit first? | Vendor name, category, purpose, status, cost status, access status, review date, and notes/next action. | Treat remaining fields as drill-down detail. |
| What should become a portal alert versus a quiet register field? | Needs source, mismatch, fails access standard, restricted, retire, disqualified, and upcoming renewal should alert. Candidate, unknown, and not reviewed can stay quiet unless operationally important. | Add future alert rules only after another manual sample or Adam review. |
| What requires governance reassessment before automation? | Billing-source review, account login, API queries, invoice retention, cost verification, cancellation/purchase recommendations, and vendor switching. | Reassess project data/money posture before live integrations or account-resource work. |

## Learning Classification Test

| Classification | Signal | Evidence | Suggested handling | Promotion owner | Review timing |
|---|---|---|---|---|---|
| Process improvement | The flagship plan should be marked in the actual chunk sections, not a separate table. | Adam corrected the Chunk 11/12 line reference and preferred clean mark-as-you-go status lines. | Keep the `Chunk Navigation` note and follow section-level `Status:` updates. | Codex / Adam | Next chunk and future handoffs |
| Product requirement | The future cockpit needs a compact vendor card plus a detailed register view. | Full vendor register fields are useful but too wide for a first-screen cockpit. | Capture as future portal requirement before UI design. | Adam / future product reviewer | Before portal vendor surface |
| Governance rule candidate | Vendor automation must distinguish research from account/billing action. | Field test shows many useful vendor fields need sensitive account or billing sources. | Keep billing/account/API access as stop-for-review until controls are updated. | Adam | Before live vendor integrations |
| Workflow rule candidate | Unknown should be treated as a useful status, not a failure. | Most sample fields are safer as unknown than guessed. | Use explicit unknown/default values in future vendor records. | Codex | After another sample |
| Template candidate | The field-test findings table is useful for testing register shape. | It answered field friction, cockpit display, alerts, and governance reassessment cleanly. | Reuse this table when testing another operational register. | Codex | After repetition |

## Decision Notes

- The register is useful as a manual audit surface.
- It should not become a first-screen cockpit table in full width.
- The first cockpit version should probably show a vendor queue: `approved`,
  `watch`, `candidate`, `restricted`, `retire`, `unknown`, with cost/access
  flags.
- Cost verification and account access should remain manual and approved until
  the project governance posture explicitly changes.
- The sample produced no payment, account, deployment, vendor-resource, or
  client-data action.

## Next Action

Choose one:

- run a second manual vendor sample with Adam-provided non-sensitive vendors;
- turn the compact vendor cockpit card into a UI requirement;
- return to GitHub/preview/packaging proof work;
- define governance controls for future live vendor/account access.
