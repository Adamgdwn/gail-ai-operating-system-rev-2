# GAIL Command Center

Status: live read-only hub-and-spoke cockpit surface

This is the browser-first Rev 2 command center shell. It is intentionally
limited to a local Vite React TypeScript build and the shared GAIL OS
read-model API. It reads governed status, posture, trace, and evidence
summaries only.

## Commands

```powershell
npm --prefix apps/command-center ci
npm --prefix apps/command-center run build
npm --prefix apps/command-center run dev
.\scripts\install-command-center-desktop-shortcut.ps1
```

## Live Read-Only Run

Start the GAIL OS API in one shell:

```powershell
$env:GAIL_OS_API_KEY = "dev-key-local"
uv run --with-requirements requirements.txt uvicorn main:app --app-dir apps/gail-os-api --host 127.0.0.1 --port 8123
```

Start the command center in a second shell with the same local API key:

```powershell
$env:GAIL_OS_API_KEY = "dev-key-local"
npm --prefix apps/command-center run dev
```

The Vite dev and preview servers proxy `/gail-os-api/*` to the local GAIL OS
API and inject `X-Api-Key` from the shell environment. The browser bundle gets
only a configured/not-configured flag, not the API key value.

Optional local settings:

- `GAIL_OS_API_PROXY_TARGET`, default `http://127.0.0.1:8123`
- `VITE_GAIL_OS_API_BASE_URL`, default `/gail-os-api`
- `VITE_GAIL_OS_AUTH_MODE=external-proxy` for a separately approved reverse
  proxy that handles API authentication outside Vite
- `VITE_GAIL_OS_STALE_AFTER_MS`, default `300000`

## Boundary

- The operator hub, governed spokes, mission, approval, agent/device, evidence,
  and connector posture areas are rendered from `GET /api/v1/read-model`.
- Freedom can read the same trace spine through
  `GET /api/v1/freedom/relationship-briefs/{cns_trace_id}` for posture briefs
  that carry no execution authority.
- Loading, empty, missing local API key, unauthorized, offline, stale-data, and
  protocol-error states are visible in the cockpit.
- The browser icon uses the symbol-only Guided AI Labs signal mark at
  `public/gail-command-icon.svg`.
- The Windows desktop shortcut uses `public/gail-command-icon.ico` and launches
  `scripts/launch-command-center.ps1`, which starts the local browser app on
  loopback.
- Desktop and larger tablet browsers show the command center as a talk-first
  hub with observable governed spokes.
- Phone-browser fallback is hub-first and preserves Freedom as the phone-side
  operator anchor.
- No approval, reject, hold, request-more-info, pause, resume, or redirect
  mutation behavior is active.
- No service worker, push notification, or offline cache is active.
- No desktop wrapper, service install, or persistent background process is
  active.
- No hosted relay, worker bootstrap, live connector, Microsoft 365 live read or
  write, Graphify ingest, R4 live execution, or Freedom runtime integration is
  active.
- Android phone work remains anchored in Freedom unless a later decision
  changes that posture.
- The browser shell is the shared desktop/tablet surface for future cockpit
  views.

## Next Chunk

The next chunk should be explicitly selected from the remediation plan. The
current command center and Freedom brief paths remain read-only until a later
owner-approved action, connector, OAuth, or execution boundary is built and
tested.
