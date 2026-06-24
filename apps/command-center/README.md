# GAIL Command Center

Status: multi-viewport read-only hub-and-spoke cockpit surface

This is the browser-first Rev 2 command center shell. It is intentionally
limited to a local Vite React TypeScript build and safe sample/proof-runner
shaped records until later chunks add governed record interactions.

## Commands

```powershell
npm --prefix apps/command-center ci
npm --prefix apps/command-center run build
npm --prefix apps/command-center run dev
.\scripts\install-command-center-desktop-shortcut.ps1
```

## Boundary

- The operator hub, governed spokes, mission, approval, worker, evidence, and
  connector posture areas are rendered from local static sample data only.
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
- No auth, hosted relay, worker bootstrap, live connector, M365, or Freedom
  runtime integration is active.
- Android phone work remains anchored in Freedom unless a later decision
  changes that posture.
- The browser shell is the shared desktop/tablet surface for future cockpit
  views.

## Next Chunk

Chunk Twenty should add local governed approval actions only after the cockpit
surface has been accepted.
