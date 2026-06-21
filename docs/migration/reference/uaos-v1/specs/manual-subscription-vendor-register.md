# Manual Subscription And Vendor Register

Created: 2026-05-31T18:04:08-06:00
Status: draft manual register
Owner: Adam Goodwin

## Purpose

This document defines the first manual subscription and vendor register fields for Guided AI Labs.

The goal is to test subscription and vendor intelligence safely before any live billing source, vendor account, API, bank feed, invoice repository, credential, or automation is connected.

## Scope

This is a manual planning and inventory artifact.

It may track:

- known subscriptions;
- known vendors;
- expected cost;
- manually verified cost status;
- renewal timing;
- account and data access status;
- review cadence;
- whether the vendor should be approved, watched, restricted, retired, or disqualified.

It must not contain:

- passwords;
- API keys;
- card numbers;
- bank account data;
- full invoices;
- private account exports;
- client-controlled vendor data;
- cancellation instructions that have not been approved;
- payment or purchasing authority.

## First Register Fields

| Field | Required | Purpose |
|---|---|---|
| Vendor name | Yes | Names the company or service provider. |
| Service or product | Yes | Names the specific subscription, product, plan, or tool. |
| Company category | Yes | Uses the categories from `subscription-vendor-intelligence.md`. |
| Business purpose | Yes | Explains why Guided AI Labs uses or is considering the service. |
| Owner | Yes | Names who is responsible for the account or decision. |
| Status | Yes | Approved, watch, restricted, retire, disqualified, candidate, unknown. |
| Subscription type | Yes | Monthly, annual, usage-based, trial, free, one-time, unknown. |
| Expected cost | Yes, if known | The cost believed to apply before verification. |
| Verified actual cost | No | The cost confirmed from a trusted billing source. Leave blank until safely verified. |
| Cost verification status | Yes | Unverified, verified, mismatch, not applicable, needs source. |
| Billing source | No | Invoice, receipt, accounting export, card statement, vendor billing page, unknown. Do not paste sensitive data. |
| Renewal or review date | Yes, if known | Date to review value, access, cost, or renewal risk. |
| Account access method | Yes | Admin portal, account owner, API, export, support request, unknown, none. |
| Data export method | Yes | API, CSV, JSON, PDF, admin export, support request, unknown, none. |
| API or programmatic access | Yes | Available, limited, unavailable, unknown, not needed. |
| Access standard status | Yes | Meets standard, partial, fails standard, unknown, exception approved. |
| Usage confidence | No | High, medium, low, unused, unknown. |
| Better-deal review status | No | Not reviewed, review due, alternatives found, no better option, defer. |
| Notes | No | Short non-sensitive notes only. |

## Status Values

| Status | Meaning |
|---|---|
| Approved | Acceptable for current use under known controls. |
| Watch | Useful but needs cost, access, renewal, usage, or risk review. |
| Restricted | May be used only with limits or explicit approval. |
| Retire | Candidate to cancel, replace, downgrade, or stop using after approval. |
| Disqualified | Should not be used because access, data, risk, or fit is unacceptable. |
| Candidate | Being considered but not yet approved. |
| Unknown | Not enough information yet. |

## Cost Verification Status

| Status | Meaning |
|---|---|
| Unverified | Expected cost is known or guessed but actual cost is not confirmed. |
| Verified | Actual cost has been checked against a trusted source. |
| Mismatch | Expected and verified actual costs do not match. |
| Not applicable | No paid subscription or cost does not apply. |
| Needs source | A verification source must be identified before review. |

## Access Standard Status

| Status | Meaning |
|---|---|
| Meets standard | Practical account and data access exists through API, export, admin portal, or equivalent. |
| Partial | Some access exists, but a gap needs review. |
| Fails standard | The vendor does not provide acceptable account/data access. |
| Unknown | Access has not been checked. |
| Exception approved | Adam accepted a documented, time-limited exception. |

## Manual Review Cadence

Use a simple cadence before automation:

| Trigger | Review timing |
|---|---|
| New vendor or subscription | Before approval or first operational use. |
| Unknown cost | Review before next payment or within 30 days. |
| Renewal date known | Review 30 days before renewal when possible. |
| Access standard unknown | Review before the vendor becomes operationally important. |
| Cost mismatch | Review immediately before taking any action. |
| Low usage or unclear purpose | Review monthly until keep/retire decision. |
| Restricted or exception-approved vendor | Review at the exception date or every 90 days, whichever comes first. |

## First Manual Table

Use this table format for the first manual test.

Do not add sensitive billing, credential, banking, or account-export details.

| Vendor name | Service/product | Category | Purpose | Owner | Status | Type | Expected cost | Verified actual cost | Cost status | Billing source | Renewal/review date | Account access | Data export | API access | Access status | Usage confidence | Better-deal status | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  | Unknown | Unknown |  |  | Unverified |  |  | Unknown | Unknown | Unknown | Unknown | Unknown | Not reviewed |  |

## Safe Manual Workflow

1. List vendors from memory or known non-sensitive sources.
2. Categorize each vendor.
3. Mark unknowns explicitly instead of guessing.
4. Add expected cost only when already known.
5. Mark verified cost blank until a safe source is reviewed.
6. Check account and data access before marking approved.
7. Flag failed access standards as restricted or disqualified unless Adam approves an exception.
8. Do not recommend cancellation, purchase, downgrade, upgrade, migration, or payment changes without explicit approval.

## Next Test

The first practical test should use a small sample of known non-sensitive vendors, not a full financial export.

Suggested starting sample:

- one AI model or agent platform;
- one infrastructure or hosting provider;
- one business operations tool;
- one creative/content tool;
- one candidate vendor being considered.

The test should answer:

1. Are the fields too many, too few, or unclear?
2. Which fields are hard to fill without sensitive data?
3. Which fields should appear in the future cockpit first?
4. What should become a portal alert versus a quiet register field?
5. What requires governance reassessment before automation?
