# GAIL Command Center

Status: first read-only operating cockpit shell

This is the browser-first Rev 2 command center shell. It is intentionally
limited to a local Vite React TypeScript build and safe sample/proof-runner
shaped records until later chunks add governed record interactions.

## Commands

```powershell
npm --prefix apps/command-center ci
npm --prefix apps/command-center run build
npm --prefix apps/command-center run dev
```

## Boundary

- Mission, approval, worker, evidence, and connector posture areas are rendered
  from local static sample data only.
- No approval, reject, hold, request-more-info, pause, resume, or redirect
  mutation behavior is active.
- No service worker, push notification, or offline cache is active.
- No auth, hosted relay, worker bootstrap, live connector, M365, or Freedom
  runtime integration is active.
- Android phone work remains anchored in Freedom unless a later decision
  changes that posture.
- The browser shell is the shared desktop/tablet surface for future cockpit
  views.

## Next Chunk

Chunk Nineteen should harden the multi-viewport cockpit surface for desktop,
Android tablet/browser review, and phone-browser fallback while preserving
Freedom as the phone anchor.
