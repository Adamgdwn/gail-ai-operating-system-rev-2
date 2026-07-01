# App Shell Command Center

Created: 2026-06-21T21:06:13-06:00
Last Updated: 2026-07-01T11:41:25-06:00
Status: active decision
Owner: Adam Goodwin

## Purpose

Choose the first Rev 2 app shell in a way that supports Windows, Linux,
ordinary browsers, Android tablet review, and the Freedom phone-interface
anchor without activating runtime integrations or building a competing Android
phone app.

## Decision

Use a browser-first Vite React TypeScript shell under
`apps/command-center`.

The shell is PWA-ready but not yet a PWA runtime. Chunk Seventeen creates the
buildable project boundary only. It does not add a service worker, offline
cache, push notifications, auth, relay calls, local shell access, Freedom API
calls, Microsoft 365 access, live connectors, worker bootstrap, hosted relay,
or production deployment.

## Options Reviewed

| Option | Result | Reason |
|---|---|---|
| Static HTML command-center proof | Not selected | Useful for quick visual proofs, but too thin for the governed cockpit, typed records, responsive states, and future approval/evidence workflows. |
| Next.js / React app router | Deferred | Strong future option for hosted or server-side routes, but adds server/app-router assumptions before auth, relay, hosted deployment, and connector boundaries are approved. |
| Vite React TypeScript browser shell | Selected | Gives a simple local static build, TypeScript feedback, browser reach across Windows/Linux/Android tablet, and a clean path to PWA, hosted, or desktop-wrapper promotion later. |
| Tauri or Electron desktop wrapper | Deferred | Useful later for trusted desktop ergonomics, but too close to local execution and OS integration before worker boundaries exist. |
| Native Android Rev 2 phone app | Blocked for now | Would compete with the Freedom phone anchor before the explicit Freedom integration and phone-link decisions are ready. |

## Ownership Boundary

Rev 2 owns:

- the browser command center shell;
- mission, relay, evidence, worker-status, and approval views after later
  chunks build them;
- local build validation and future static/browser deployment readiness;
- governed records and source-of-truth reconciliation.

Freedom owns or informs:

- the first phone-side operator link;
- business-partner continuity, voice/mobile interaction, and high-level
  agentic partner experience;
- future bridge candidates through safe records, not direct runtime coupling.

The shell must remain compatible with Freedom without depending on Freedom
runtime access.

## Initial Structure

Chunk Seventeen creates:

- `apps/command-center/package.json`;
- `apps/command-center/package-lock.json`;
- `apps/command-center/index.html`;
- `apps/command-center/vite.config.ts`;
- `apps/command-center/tsconfig.json`;
- `apps/command-center/tsconfig.node.json`;
- `apps/command-center/src/main.tsx`;
- `apps/command-center/src/App.tsx`;
- `apps/command-center/src/appShellDecision.ts`;
- `apps/command-center/src/styles.css`;
- `apps/command-center/README.md`.

## Dependency Review

Initial dependencies are limited to the browser shell:

| Package | Role | Boundary |
|---|---|---|
| `react` | UI rendering | Browser UI only; no connector or runtime authority. |
| `react-dom` | DOM rendering | Browser UI only. |
| `vite` | Local build tool | Build/dev server only; no production deployment authority. |
| `typescript` | Type checking | Local validation only. |
| `@vitejs/plugin-react` | Vite React transform | Build-time only. |
| `@types/react`, `@types/react-dom` | Type declarations | Development-only. |

These packages are acceptable for this chunk because they are common, narrow,
replaceable, and support a static build. The package lock records the resolved
dependency tree. Any later UI framework, design system, service worker,
desktop wrapper, hosted platform, auth layer, or API client requires its own
bounded decision or implementation chunk.

## Device Posture

| Surface | Shell posture |
|---|---|
| Windows desktop browser | Primary local operator shell. |
| Linux desktop browser | Supported through the same static/browser shell after clone or local serve. |
| Android tablet browser | Supported review cockpit target for future responsive views. |
| Android phone | Browser fallback only; Freedom remains the phone anchor. |
| Desktop wrapper | Deferred until worker/local-host boundaries are approved. |

## Stop Triggers

Stop and require explicit owner approval before:

- adding auth, accounts, or identity provider configuration;
- adding service workers, push notifications, offline caches, or installable
  PWA behavior;
- reading or writing live relay records;
- calling the local proof runner from the browser;
- exposing local filesystem or shell capabilities to the browser app;
- importing Freedom source, generated config, local state, or runtime data;
- activating Freedom gateway, relay, voice, desktop-host, Supabase, provider,
  or mobile runtime behavior;
- adding Microsoft 365, QuickBooks, finance, billing, client-data, or other
  live connector access;
- adding Tauri, Electron, native Android, hosted relay, worker bootstrap, or
  production deployment behavior.

## Validation

Chunk Seventeen validation should include:

- governance preflight;
- dependency version review;
- `npm --prefix apps/command-center install`;
- `npm --prefix apps/command-center run build`;
- Python unit discovery for the existing local core;
- schema validation;
- `git diff --check`;
- changed-file forbidden filename and strict secret-pattern scans;
- Graphify incremental update after the code structure exists.

## Current Result

This decision originally permitted a buildable browser shell scaffold only.
Chunk Eighteen built the first operating cockpit view from local sample data.
Chunk Nineteen hardened the multi-viewport hub-and-spoke surface. EX-2 later
wired the cockpit to the shared GAIL OS read-only read model through the local
Vite proxy.

The current command center still must not add approval mutation behavior, live
bridge behavior, Freedom runtime access, Microsoft 365 live read/write work,
Graphify ingest, R4 live execution, worker bootstrap, hosted relay, live
connector access, client data, or production behavior without a later approved
chunk.
