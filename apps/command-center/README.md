# GAIL Command Center

Status: initial app-shell scaffold

This is the browser-first Rev 2 command center shell. It is intentionally
limited to a local Vite React TypeScript build until later chunks add cockpit
views and governed record interactions.

## Commands

```powershell
npm --prefix apps/command-center ci
npm --prefix apps/command-center run build
npm --prefix apps/command-center run dev
```

## Boundary

- No service worker, push notification, or offline cache is active.
- No auth, hosted relay, worker bootstrap, live connector, M365, or Freedom
  runtime integration is active.
- Android phone work remains anchored in Freedom unless a later decision
  changes that posture.
- The browser shell is the shared desktop/tablet surface for future cockpit
  views.

## Next Chunk

Chunk Eighteen should build the first local cockpit view from safe sample data
or local proof-runner summaries. It should stop before approval mutation
behavior.
