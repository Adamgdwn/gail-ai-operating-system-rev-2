# CP-1 Contract Export Notes

**Date:** 2026-06-28
**Chunk:** 20C — Canonical CP-1 JSON Contract Export
**Status:** Complete — 9 schemas valid, 43 contract tests passing

---

## What Was Created

Nine JSON Schema contracts derived from the GAIL OS Python dataclasses and enums,
located at `contracts/json-schema/`.

| Schema File | Source Type | Notes |
|---|---|---|
| `mission.schema.json` | `MissionEnvelope` + `MissionStatus` enum | Includes all 12 MissionStatus stages as a closed enum |
| `action.schema.json` | `Action` | Includes R0–R5 enum, risk_tier 0–5 integer bounds, MissionStatus ref |
| `authority-envelope.schema.json` | `AuthorityEnvelope` | Includes AuthorityLevel, AutonomyLevel, EnvelopeStatus enums |
| `evidence-packet.schema.json` | `EvidencePacket` | Includes EvidenceResult, ExecutionMode enums |
| `policy-decision.schema.json` | `PolicyDecision` | Permission decision from GAIL OS policy gate |
| `connector-status.schema.json` | `ConnectorProfile` | ConnectorRegistry profile record |
| `source-ref.schema.json` | Designed for CNS | Source-of-truth reference anchor; no Python class yet |
| `graph-context-ref.schema.json` | Designed for CNS | Graphify entity context reference; no Python class yet |
| `approval-decision.schema.json` | `ApprovalDecision` (Chunk 20B) | Governed approval decision record |

---

## Transport-Parking Constraints Enforced

All schemas are transport-neutral:
- No FastAPI references
- No `localhost` or hardcoded IP addresses
- No HTTP-specific response shapes (status codes, headers)
- `$id` URIs use `https://gail-os.local/` as a non-live namespace

These schemas can be wrapped by any transport layer (FastAPI, gRPC, direct function
calls, CLI) without modification.

---

## Authority and Lifecycle Enums Are Closed

| Enum | Values | Enforced in Schema |
|---|---|---|
| `AuthorityLevel` (R-ladder) | R0, R1, R2, R3, R4, R5 | `authority-envelope.schema.json`, `action.schema.json` |
| `AutonomyLevel` (A-ladder) | A0, A1, A2, A3, A4, A5, A6 | `authority-envelope.schema.json` |
| `MissionStatus` (12-stage lifecycle) | observed → proposed → … → learned | `mission.schema.json`, `action.schema.json` |
| `EvidenceResult` | success, failure, stopped, partial | `evidence-packet.schema.json` |
| `ExecutionMode` | dry-run, live | `evidence-packet.schema.json`, `policy-decision.schema.json` |
| `ApprovalDecisionType` | approved, rejected, held, more_info_requested | `approval-decision.schema.json` |
| `ConnectorCurrentState` | planning-only, registry-only, inventory-only | `connector-status.schema.json` |
| `SystemFamily` | GitHub, Graphify, Microsoft 365, QuickBooks, Local Device, Client Gateway, Vendor Or Deployment | `connector-status.schema.json` |

---

## What These Schemas Unblock

| Next Step | Depends On |
|---|---|
| `@gail/contracts` TypeScript generated types (Chunk 22) | All 9 schemas in `contracts/json-schema/` |
| Freedom TypeScript contract adapter (Chunk 20F) | `mission.schema.json`, `action.schema.json`, `policy-decision.schema.json`, `evidence-packet.schema.json` |
| FastAPI HTTP wrapper (Chunk 21) | `action.schema.json`, `policy-decision.schema.json`, `evidence-packet.schema.json` |
| GAIL OS → Graphify graph-fact extraction lane (Chunk 20E) | `graph-context-ref.schema.json`, `source-ref.schema.json` |
| M365 bridge evidence linkage (future Phase 4) | `evidence-packet.schema.json`, `source-ref.schema.json` |

---

## What Is NOT Published Here

Per the 20C stop condition:
- No npm publish of `@gail/contracts` TypeScript package (Chunk 22)
- No FastAPI routes created (Chunk 21)
- No live HTTP API exposed
- No Freedom code modified (Chunk 20F)
- No M365 access
- No cloud deployment

---

## Validation

```bash
# Run schema validation and synthetic record checks
python scripts/export-cp1-contracts.py --verbose

# Run full test suite
python -m pytest tests/test_contract_exports.py -v
```

Results as of 2026-06-28: 43 contract tests + 191 pre-existing tests = 234 total passing.
Export script exits 0. All 9 schemas valid. All synthetic records accepted. Invalid
R-level, A-level, lifecycle state, and prefix cases correctly rejected.
