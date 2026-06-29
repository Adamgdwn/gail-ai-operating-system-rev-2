# Azure Container Apps Pilot Deployment Report

Document type: deployment report
Date: 2026-06-28
Saved: 2026-06-28T20:22:25-06:00
Last Updated: 2026-06-28T20:22:25-06:00
Status: integration complete for pilot health endpoints (2026-06-28T20:22:25-06:00)
Owner: Adam Goodwin

## Purpose

Record the owner-approved Azure Container Apps pilot deployment for the GAIL AI
Operating System API and Graphify CNS API without storing or exposing secrets.

This report documents cloud placement evidence only. It does not promote live
Microsoft 365 access, Graphify persistent ingest, R4 live execution,
source-of-truth migration, or production service readiness.

## Owner Approval

Adam approved the exact scope in chat on 2026-06-28 after Linux sent
`X:\LINUX_TO_WINDOWS__2026-06-28-deploy-steps-7-8.md`.

Approved scope:

- create the GAIL OS Azure Container App from the existing ACR image;
- create the Graphify CNS API Azure Container App from the existing ACR image;
- replace placeholder pilot API keys with fresh generated Key Vault values;
- verify unauthenticated health endpoints;
- write a non-secret DirectLink handoff back to Linux.

## Deployment Inputs

Azure subscription:

- Subscription name: `Azure subscription 1`
- Subscription ID: `91924cd2-575f-448e-af49-3f8065afc9c2`
- Tenant ID: `bb833221-b5de-43fe-815a-8a33d1c62dbc`
- Signed-in account: `adamgdwn@hotmail.com`

Azure resources:

- Resource group: `rg-gail-cns-pilot-canadacentral`
- Container Apps environment: `aca-env-gail-cns-pilot`
- ACR: `acrgailcnspilot.azurecr.io`
- Key Vault: `kv-gail-cns-pilot`
- Storage account: `stgailcnspilot`
- Azure Files share: `graphify-cns-data`

Images:

- `acrgailcnspilot.azurecr.io/gail-os-api:latest`
- `acrgailcnspilot.azurecr.io/graphify-cns-api:latest`

## Secret Handling

Fresh pilot API key values were generated locally and stored as new Key Vault
secret versions before deployment:

- `kv-gail-cns-pilot/gail-os-api-key`
- `kv-gail-cns-pilot/cns-api-key`

The deployment did not write API key values, ACR passwords, storage keys,
tokens, tenant secrets, or credential values to Exchange, git, repo docs, or
command transcripts.

## Deployed Apps

### GAIL OS API

- App: `aca-gail-os-api`
- Image: `acrgailcnspilot.azurecr.io/gail-os-api:latest`
- URL: `https://aca-gail-os-api.ambitiousforest-f57e95ff.canadacentral.azurecontainerapps.io`
- Revision: `aca-gail-os-api--xhobzi1`
- Revision state: active/running
- Traffic weight: `100`

Health evidence:

```text
GET https://aca-gail-os-api.ambitiousforest-f57e95ff.canadacentral.azurecontainerapps.io/api/v1/health
HTTP 200
{"status":"ok","boundary":"A1 local no-network","phase":"1"}
```

### Graphify CNS API

- App: `aca-graphify-cns-api`
- Image: `acrgailcnspilot.azurecr.io/graphify-cns-api:latest`
- URL: `https://aca-graphify-cns-api.ambitiousforest-f57e95ff.canadacentral.azurecontainerapps.io`
- Revision: `aca-graphify-cns-api--2xw7yzq`
- Revision state: active/running
- Traffic weight: `100`

Health evidence:

```text
GET https://aca-graphify-cns-api.ambitiousforest-f57e95ff.canadacentral.azurecontainerapps.io/health
HTTP 200
{"status":"ok","store":"connected","node_count":0}
```

## Storage Status

The ACA environment storage registration succeeded:

- Storage name: `graphify-files`
- Storage account: `stgailcnspilot`
- Share: `graphify-cns-data`
- Access mode: `ReadWrite`

The installed `az containerapp create` surface did not expose the requested
`--volume` / `--volume-mount` flags. Windows used the documented fallback path
from the Linux handoff for this first pilot:

- `CNS_STORE_PATH=/tmp/cns.db`
- Graphify CNS API uses ephemeral SQLite until a YAML-based or update-command
  mount path is supplied and approved.

## Boundaries Preserved

This deployment only created two pilot Azure Container Apps and verified
public health endpoints.

Not performed:

- Microsoft 365 content access;
- SharePoint, CRM, Teams, email, or Planner writes;
- Microsoft Graph permission expansion or tenant/admin consent;
- live Microsoft Graph calls;
- persistent Graphify CNS store ingest;
- R4 live execution;
- client-facing business action;
- source-of-truth migration;
- runtime consolidation;
- production service readiness claim.

## Handoff

DirectLink handoff written:

`X:\WINDOWS_TO_LINUX__2026-06-28-aca-apps-deployed.md`

Linux confirmed visibility over DirectLink.

## Next Owner-Gated Decisions

Recommended next bounded decisions:

- whether Linux should attach persistent Graphify storage with a YAML/update
  deployment path;
- whether to run authenticated endpoint probes using pilot API keys without
  exposing those keys through Exchange;
- whether to add workflow dispatch triggers to the image build workflows;
- whether to document or automate a rollback/scale-to-zero path for the pilot;
- whether to proceed with any Microsoft 365 connector-promotion design gate.
