# Subscription And Vendor Intelligence

Created: 2026-05-31T17:18:02-06:00
Status: draft product requirement
Owner: Adam Goodwin

## Purpose

Guided AI Labs needs the operating system to eventually track every recurring subscription, categorize each vendor, verify actual costs, and periodically review whether better options exist.

This is a planning artifact only. It does not authorize live account access, credential storage, payment action, cancellation, procurement, or automated vendor switching.

The first manual register shape is defined in [manual-subscription-vendor-register.md](manual-subscription-vendor-register.md).

## Product Intent

The operating layer should help answer:

> What are we paying for, why do we use it, what access do we have, is the cost correct, and is there a better option now?

This belongs in the future portal because subscriptions are not only bookkeeping. They affect tool access, data rights, account control, risk, operating cost, client delivery, and AI-native workflow quality.

## Required Capability

The future system should maintain a subscription and vendor register with:

- vendor name;
- company category;
- service category;
- business purpose;
- owner;
- renewal cadence;
- expected cost;
- verified actual cost;
- billing source;
- account access method;
- data export method;
- API or similar programmatic access status;
- cancellation and portability notes;
- approved, watch, restricted, or retire status;
- last review date;
- next review date;
- linked alternatives or better-deal research.

## Company Categories

Use a simple category set at first:

| Category | Examples |
|---|---|
| AI model or agent platform | LLMs, coding agents, research tools, automation agents |
| Infrastructure and hosting | Cloud, database, deployment, storage, monitoring |
| Business operations | Email, calendar, accounting, CRM, documents, project tools |
| Creative and content | Design, video, audio, writing, publishing |
| Security and identity | Password, authentication, endpoint, access management |
| Learning and research | Courses, communities, market intelligence, publications |
| Client delivery | Tools used to assess, build, host, or support client work |
| Personal productivity | Tools that support Adam's AI-native work pattern |
| Other | Temporary bucket until a better category is justified |

## Cost Verification

The system should separate expected cost from verified actual cost.

Expected cost can come from the vendor's plan page, original purchase note, invoice, or account settings.

Verified actual cost should come from a trusted billing source such as an invoice, receipt, accounting export, credit card transaction, bank feed, or vendor billing API.

If costs do not match, the portal should flag:

- unexpected price increase;
- duplicate subscription;
- unused or low-use tool;
- billing-cycle mismatch;
- seat-count mismatch;
- tax, currency, or fee change;
- trial converted to paid;
- cancelled service still billing.

## Layered AI Review

The operating system should support a periodic layered review, not a one-shot recommendation.

| Layer | Review question | Output |
|---|---|---|
| Inventory layer | What subscriptions exist and are they categorized correctly? | Clean vendor register |
| Cost layer | Do expected and verified actual costs match? | Cost variance alerts |
| Usage layer | Is the service still used enough to justify the spend? | Keep, watch, reduce, or retire recommendation |
| Access layer | Does the vendor provide acceptable account and data access? | Approved, restricted, or disqualified status |
| Market layer | Are there better deals, plans, bundles, or competitors? | Alternatives shortlist |
| Strategy layer | Does the vendor still fit Guided AI Labs' operating model? | Decision brief |
| Approval layer | Should Adam keep, renegotiate, downgrade, replace, cancel, or defer? | Human-approved next action |

Market-layer review should use current research at the time of review because prices, plans, terms, and competitors change often.

## Account And Data Access Standard

Guided AI Labs should not start or continue doing business with organizations that do not provide full practical access to Guided AI Labs accounts and data through an API, structured export, admin portal, or equivalent documented mechanism.

Minimum acceptable access:

- view account, plan, billing, usage, and renewal data;
- export Guided AI Labs data in a usable format;
- retrieve invoices or billing history;
- manage seats, users, and permissions where applicable;
- close, downgrade, or transfer the account without dark patterns;
- document data retention and deletion behavior;
- support programmatic access where the service is operationally important.

Vendors without acceptable access should be marked `restricted` or `disqualified` unless Adam explicitly approves a time-limited exception.

## Exception Rule

An exception may be allowed only when:

- the tool is materially valuable;
- no practical alternative exists yet;
- the missing access is documented;
- the risk is accepted by Adam;
- a review date is set;
- exit, export, or replacement notes are captured.

Exceptions should be recorded in the vendor register or a future exception record before the vendor becomes operationally important.

## Governance Notes

This feature touches finance, vendor accounts, API access, billing data, and possibly client-delivery systems. Before implementation connects to live accounts or billing sources, reassess:

- `project-control.yaml` data and money flags;
- data classification;
- secret and credential handling;
- approval level for cancellations, purchases, downgrades, upgrades, and vendor switching;
- retention rules for invoices, receipts, usage logs, and account exports;
- whether account access requires a restricted or no-AI path.

AI may research, compare, summarize, and draft recommendations. Human approval is required before any purchase, cancellation, account change, payment change, legal acceptance, or vendor migration.

## MVP Discovery Questions

Before building this into the portal, answer:

1. Where is the current source of truth for subscriptions?
2. Which billing sources can verify actual cost safely?
3. What counts as a subscription versus a one-time purchase?
4. Which vendors are critical to daily AI-native work?
5. Which vendors must have API access on day one?
6. What review cadence is useful: monthly, quarterly, renewal-based, or spend-threshold based?
7. What should the first alert show: cost mismatch, renewal coming up, missing API access, or better deal found?
8. What actions are safe for AI to suggest, and which require explicit Adam approval?
9. What information is too sensitive for general AI routes?
10. What should happen when a vendor fails the account and data access standard?
