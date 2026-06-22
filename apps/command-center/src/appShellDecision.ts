export type DeviceSurface =
  | "windows-browser"
  | "linux-browser"
  | "android-tablet-browser"
  | "android-phone-fallback";

export interface AppShellDecision {
  readonly decisionId: string;
  readonly productName: string;
  readonly selectedShell: string;
  readonly statusLabel: string;
  readonly deviceSurfaces: readonly DeviceSurface[];
  readonly blockedForThisChunk: readonly string[];
}

export const appShellDecision: AppShellDecision = {
  decisionId: "app-shell-command-center",
  productName: "GAIL Command Center",
  selectedShell: "vite-react-typescript-browser-shell",
  statusLabel: "Shell scaffold ready",
  deviceSurfaces: [
    "windows-browser",
    "linux-browser",
    "android-tablet-browser",
    "android-phone-fallback",
  ],
  blockedForThisChunk: [
    "approval-mutations",
    "freedom-runtime-access",
    "m365-adapter",
    "hosted-relay",
    "worker-bootstrap",
    "live-connectors",
    "production-deployment",
  ],
} as const;
