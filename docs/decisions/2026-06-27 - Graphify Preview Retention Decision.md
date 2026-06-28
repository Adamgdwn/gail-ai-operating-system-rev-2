# Graphify Preview Retention Decision

Document type: decision record
Date: 2026-06-27
Saved: 2026-06-27T17:15:09-06:00
Last Updated: 2026-06-27T18:06:31-06:00
Status: draft complete (2026-06-27T17:15:09-06:00)
Owner: Adam Goodwin

## Purpose

This record decides where future local Graphify acceleration preview output may
live before any preview writer is built.

The decision is GAIL-side only. It does not modify Graphify, create a Graphify
adapter, upload graph data, expose an HTTP API, select cloud placement, read
live business systems, or grant execution authority.

## Decision

Future GA-C2 preview output should default to ignored local developer artifact
retention under:

```text
tmp/graphify-acceleration-preview/
```

This path is already covered by the repository's ignored `tmp/` rule. The
future preview command may write deterministic JSONL or JSON files there for
operator inspection, but those generated preview files are not evidence
records, relay records, approval records, source-of-truth records, or Graphify
ingest records.

No preview output may be committed by default.

## Selected Retention Mode

Selected option: ignored local developer artifact.

Preview output may be retained only as disposable local working output. It may
be deleted at any time, overwritten by later previews, or regenerated from safe
local fixtures.

GA-C2 may create a stable default filename such as:

```text
tmp/graphify-acceleration-preview/graphify-acceleration-preview.jsonl
```

The exact filename can be chosen during GA-C2, but it must remain under
`tmp/graphify-acceleration-preview/` unless Adam explicitly approves a
different retention boundary.

## Options Reviewed

| Option | Decision | Reason |
|---|---|---|
| Ignored local developer artifact | Selected | Fastest safe path for inspection; avoids creating a premature evidence, audit, or source-of-truth lane. |
| Controlled committed test fixture | Deferred | Useful later only if examples are synthetic, reviewed, and intentionally added as tests or docs. Generated preview output itself should not be committed. |
| Relay-store-adjacent record | Rejected for GA-C | Relay records carry governed approval/evidence meaning. Preview facts are inspectable graph-fact candidates, not relay evidence or authority records. |
| Dedicated local export store | Deferred | A store implies lifecycle, cleanup, audit, migration, and retention duties that are not needed for the first preview command. |

## Commit Boundary

Allowed to commit in GA-C2:

- source code for a local preview command or callable function;
- tests for deterministic preview generation and path safety;
- documentation describing how to inspect and clean the preview output;
- intentionally authored synthetic example fixtures only if a future chunk
  explicitly approves controlled retention.

Not allowed to commit:

- generated preview output from `tmp/graphify-acceleration-preview/`;
- raw Graphify output such as `graphify-out/` or `graph.json`;
- raw logs, raw audio, transcripts, client payloads, M365 exports, QuickBooks
  exports, finance or billing records, credentials, tokens, or `.env` material;
- live connector state or live business-system content.

## Data Boundary

GA-C2 preview generation may use only safe local synthetic fixtures or already
validated local sample records produced by the GA-B contract builders.

Preview records must keep `contains_raw_payload: false` and must validate under
the `GraphifyAccelerationRecord` contract before any write.

Preview generation must not read:

- Microsoft 365 tenant content, SharePoint files, Outlook messages, Teams
  content, or calendar records;
- QuickBooks, accounting, invoice, payment, tax, banking, billing, or finance
  data;
- client data, client payloads, client-visible drafts, or signed-scope work;
- raw logs, raw audio, recordings, transcripts, model-provider payloads, or
  debugging dumps;
- secrets, credentials, `.env` files, generated Graphify output, or live
  connector runtime state.

## Cleanup Expectations

The preview directory is disposable. Operators and agents may delete it during
cleanup without preserving history.

Future preview commands should either overwrite the default preview file or
write deterministic timestamp-free filenames unless a later chunk approves
controlled preview retention. If timestamped scratch files are ever useful,
they must remain ignored under `tmp/graphify-acceleration-preview/` and should
not become the default.

Before committing GA-C2 or later preview work, agents should verify that no
generated preview output has become tracked.

## No Ingest Implication

The preview location does not imply that Graphify will read from this folder.
It is an operator inspection surface only.

Any future Graphify ingest path still requires separate owner approval,
connector-like boundary review, authentication and authorization review,
retention rules, audit behavior, rollback expectations, and a stop condition
that Graphify cannot approve, execute, mutate source, deploy, change
permissions, or read live business systems.

## GA-C2 Guidance

The next safe implementation slice may build a local export preview command or
callable function that:

- writes only under `tmp/graphify-acceleration-preview/` by default;
- validates every preview record immediately before writing;
- uses deterministic ordering and includes schema version plus fingerprint;
- can run without network access, Graphify runtime access, live connectors, or
  business-system reads;
- rejects output paths outside the approved ignored preview directory unless a
  later explicit owner decision changes the retention boundary;
- treats preview output as disposable inspection data, not audit evidence.

## GA-C3 And GA-C4 Guidance

Preview diff/cache checks may read existing JSONL under
`tmp/graphify-acceleration-preview/` as disposable local cache input. Diff
output may be printed for operator inspection, but it must remain a safe
summary of fact IDs, entity labels, fingerprints, counts, and non-authority
flags only.

Preview diff output is not evidence, approval, relay, source-of-truth,
Graphify ingest, or execution-authority material. Removed facts in a preview
diff are information only; they do not delete source records, mutate Graphify,
or change any approval/evidence/relay state.

## Validation Evidence

Validated during GA-C1:

- `bash scripts/governance-preflight.sh` passed with 0 warnings;
- `.gitignore` already ignores `tmp/` and `graphify-out/`;
- relay store behavior was reviewed and kept separate from preview retention;
- `EvidencePacket` and `GraphifyAccelerationRecord` boundaries were reviewed;
- no preview writer, preview output, Graphify call, adapter, transport, HTTP
  API, cloud placement, live connector, client data, or execution authority was
  added.
