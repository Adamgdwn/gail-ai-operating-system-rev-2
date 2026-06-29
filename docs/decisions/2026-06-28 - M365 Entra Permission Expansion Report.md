# M365 Entra Permission Expansion Report

Document type: integration permission report
Date: 2026-06-28
Saved: 2026-06-28T20:55:36-06:00
Status: integration permission gate complete (2026-06-28T20:55:36-06:00)
Owner: Adam Goodwin

## Purpose

Record the owner-approved Microsoft 365 / Entra delegated permission expansion
for the local Microsoft 365 agent app used by the AG Operations Workspace,
Freedom, Graphify, and GAIL OS integration lane.

This is a tenant permission expansion record only. It does not approve live
business-system writes, unattended app-only operation, source-of-truth
migration, Graphify production ingest, R4 live execution, or production service
readiness.

## Owner Approval

Adam explicitly approved adding the Linux-requested delegated Microsoft 365
permissions plus email, calendar, and Exchange Online delegated permissions in
chat on 2026-06-28.

Approved boundary:

- delegated permissions only;
- admin consent for A.G. Operations Ltd;
- no client secret;
- no certificate;
- no app-only grant;
- no redirect URI change;
- no guest or external sharing change;
- no live business action as part of this permission change.

## App Registration

- App name: `Guided AI Labs - CLI for Microsoft 365 Local Agent`
- App/client ID: `9aeeeae6-be2a-476c-9c34-389dbc927c99`
- Tenant: `1ca92af5-21ff-42e3-87ae-3bde9c2cc501`
- Sign-in audience: `AzureADMyOrg`

Credential check after the change:

- password credential count: `0`
- key credential count: `0`

No client secret or certificate was created.

## Delegated Permissions Added

Microsoft Graph delegated scopes:

- `Sites.ReadWrite.All`
- `Files.ReadWrite.All`
- `Group.ReadWrite.All`
- `TeamSettings.ReadWrite.All`
- `ChannelSettings.ReadWrite.All`
- `ChannelMessage.Send`
- `Tasks.ReadWrite`
- `offline_access`
- `Mail.ReadWrite`
- `Mail.Send`
- `Calendars.ReadWrite`
- `MailboxSettings.ReadWrite`

Microsoft Flow Service delegated scopes:

- `Flows.Manage.All`

Office 365 Exchange Online delegated scopes:

- `Exchange.Manage`
- `Exchange.ManageV2`
- `Exchange.AdminAPI.Manage`

Existing permissions retained:

- Microsoft Graph `User.Read`
- Microsoft Flow Service `Flows.Read.All`
- Microsoft Flow Service `User`
- Azure Service Management `user_impersonation`

## Scope Name Notes

The tenant metadata did not expose `Team.ReadWrite.All` as an enabled
delegated Microsoft Graph scope. The closest delegated live equivalents used
for the approved Teams channel/settings boundary were:

- `TeamSettings.ReadWrite.All`
- `ChannelSettings.ReadWrite.All`

The tenant metadata also exposed the Flow management permission as
`Flows.Manage.All`, not `Flow.Manage.All`. The live `Flows.Manage.All` scope was
added and consented.

## Consent Verification

`az ad app permission list-grants` showed tenant-wide delegated grants
(`consentType=AllPrincipals`) after the update for:

- Microsoft Graph:
  `User.Read Sites.ReadWrite.All Files.ReadWrite.All Group.ReadWrite.All TeamSettings.ReadWrite.All ChannelSettings.ReadWrite.All ChannelMessage.Send Tasks.ReadWrite offline_access Mail.ReadWrite Mail.Send Calendars.ReadWrite MailboxSettings.ReadWrite`
- Microsoft Flow Service:
  `Flows.Read.All Flows.Read.All User Flows.Manage.All`
- Office 365 Exchange Online:
  `Exchange.Manage Exchange.ManageV2 Exchange.AdminAPI.Manage`

The repeated `Flows.Read.All` entry existed in the app permission manifest
before this chunk and was not cleaned up during this permission expansion.

## Validation Evidence

- Governance preflight passed with 0 warnings.
- Timestamp captured: `2026-06-28T20:48:10-06:00`.
- Azure CLI logged into the A.G. Operations tenant as
  `adamgoodwin@guidedailabs.com`.
- Permission IDs were resolved from live Entra service-principal metadata
  before applying changes.
- `az ad app permission admin-consent` completed.
- Exchange Online delegated grant was explicitly updated so all three approved
  Exchange scopes were effective.
- Final app check showed `passwordCredentialCount=0` and
  `keyCredentialCount=0`.

## Boundaries Preserved

No tenant secret, client secret, certificate, auth code, token, API key, storage
key, or credential value was written to git, docs, Exchange files, or command
output.

No Microsoft 365 content read, SharePoint write, Teams message send, Planner
write, Outlook send, calendar mutation, Power Automate flow change, Exchange
configuration mutation, live business-system action, Graphify production
ingest, R4 live execution, or source-of-truth migration was performed.

## Next Step

Linux may re-authenticate the Microsoft 365 CLI using app
`9aeeeae6-be2a-476c-9c34-389dbc927c99` so the new delegated scopes appear in
fresh tokens. The next proof should remain bounded to an owner-approved test
surface and should report evidence without printing tokens or business data.
