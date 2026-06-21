# Cockpit Command Proof

Created: 2026-06-06T16:46:15-06:00
Last Updated: 2026-06-06T19:38:49-06:00
Status: hardened local proof artifact
Owner: Adam Goodwin

## Purpose

This static app began as the Chunk 10 proof surface and was hardened in
REQ-0035 into a local cockpit-command runner for the User AI Operating System.

It turns one cockpit command into:

- route and approval status;
- a mission plan;
- validation checks;
- learning capture;
- a visual execution map.
- local draft persistence;
- generated request-record markdown;
- visible stop-for-approval triggers.

## Run

Open `index.html` directly in a browser.

Or use the launcher for your platform from the repository root.

Linux:

```bash
scripts/launch-cockpit.sh
```

macOS:

```bash
scripts/launch-cockpit.command
```

Windows PowerShell:

```powershell
.\scripts\launch-cockpit.ps1
```

Windows Command Prompt:

```bat
scripts\launch-cockpit.bat
```

For local HTTP validation without opening a browser:

```bash
scripts/launch-cockpit.sh --no-open --port 4173
```

## Validation

```bash
python3 scripts/validate-cockpit-proof.py
chromium --headless --no-sandbox --disable-gpu --screenshot=tmp/cockpit-proof.png --window-size=1440,1000 file://$PWD/apps/cockpit-command-proof/index.html
```
