export type CockpitStatusTone = "ready" | "watch" | "blocked" | "complete";

export interface MissionStep {
  readonly name: string;
  readonly label: string;
  readonly status: CockpitStatusTone;
  readonly summary: string;
}

export interface MissionSnapshot {
  readonly requestId: string;
  readonly missionId: string;
  readonly title: string;
  readonly status: string;
  readonly domain: string;
  readonly approvalLevel: string;
  readonly dataClass: string;
  readonly currentFocus: string;
  readonly steps: readonly MissionStep[];
}

export interface ApprovalSnapshot {
  readonly envelopeId: string;
  readonly actor: string;
  readonly deviceRole: string;
  readonly approvalLevel: string;
  readonly requestedCapability: string;
  readonly relayStatus: string;
  readonly stopTriggers: readonly string[];
}

export interface WorkerSnapshot {
  readonly id: string;
  readonly label: string;
  readonly role: string;
  readonly status: string;
  readonly tone: CockpitStatusTone;
}

export interface EvidenceSnapshot {
  readonly id: string;
  readonly label: string;
  readonly summary: string;
  readonly refs: readonly string[];
}

export interface ConnectorPosture {
  readonly label: string;
  readonly posture: string;
  readonly tone: CockpitStatusTone;
  readonly detail: string;
}

export interface OperatingCockpitSnapshot {
  readonly generatedAt: string;
  readonly source: string;
  readonly mission: MissionSnapshot;
  readonly approval: ApprovalSnapshot;
  readonly workers: readonly WorkerSnapshot[];
  readonly evidence: readonly EvidenceSnapshot[];
  readonly connectorPostures: readonly ConnectorPosture[];
}

export const operatingCockpitSnapshot: OperatingCockpitSnapshot = {
  generatedAt: "2026-06-21T21:43:50-06:00",
  source: "safe local sample shaped by the Chunk Fifteen proof runner",
  mission: {
    requestId: "REQ-LOCAL-PROOF-001",
    missionId: "mission-local-proof",
    title: "Local proof path from intent to validated evidence",
    status: "completed local proof",
    domain: "validation",
    approvalLevel: "A1 local no-network",
    dataClass: "synthetic",
    currentFocus: "Keep the browser cockpit aligned to governed records before live integrations.",
    steps: [
      {
        name: "mission_intent",
        label: "Mission intent",
        status: "complete",
        summary: "Local dry-run mission envelope created and reloadable.",
      },
      {
        name: "mission_plan_policy",
        label: "Policy gate",
        status: "complete",
        summary: "Deterministic plan evaluated inside the A1 boundary.",
      },
      {
        name: "connector_registry_dry_run",
        label: "Connector check",
        status: "complete",
        summary: "Local-device profile validated as dry-run only.",
      },
      {
        name: "relay_record_persistence",
        label: "Relay record",
        status: "complete",
        summary: "Reference-only approval record persisted as local-file.",
      },
      {
        name: "trusted_worker_claim",
        label: "Worker claim",
        status: "complete",
        summary: "One trusted Linux worker claim accepted for the mission.",
      },
      {
        name: "validated_evidence_record",
        label: "Evidence",
        status: "complete",
        summary: "Safe evidence references attached; relay proof marked complete.",
      },
    ],
  },
  approval: {
    envelopeId: "relay-proof-local",
    actor: "Adam",
    deviceRole: "Freedom phone anchor / Android phone cockpit",
    approvalLevel: "A2 review ceiling",
    requestedCapability: "approval",
    relayStatus: "approved sample, read-only shell",
    stopTriggers: [
      "portal_or_relay_live_action",
      "hosted_relay_or_worker_action",
      "secret_exposure",
      "client_data_access",
      "raw_payload_retention",
      "graphify_action_execution",
    ],
  },
  workers: [
    {
      id: "linux-worker-001",
      label: "Linux worker",
      role: "trusted worker",
      status: "claim accepted in local proof",
      tone: "complete",
    },
    {
      id: "windows-worker-planned",
      label: "Windows worker",
      role: "future trusted worker",
      status: "planned, not bootstrapped",
      tone: "watch",
    },
    {
      id: "browser-cockpit",
      label: "Browser shell",
      role: "operator review surface",
      status: "read-only local sample",
      tone: "ready",
    },
    {
      id: "freedom-phone",
      label: "Freedom phone link",
      role: "phone-side partner layer",
      status: "anchor preserved, runtime not connected",
      tone: "watch",
    },
  ],
  evidence: [
    {
      id: "evidence-proof-local",
      label: "Validated evidence record",
      summary: "Local proof runner moved intent to evidence without live connector access.",
      refs: [
        "packages/uaos-core/src/gail_ai_operating_system/local_proof_runner.py",
        "tests/test_local_proof_runner.py",
      ],
    },
    {
      id: "pathway-ledger",
      label: "Chunk ledger",
      summary: "Active pathway records chunk status, validation, and next handoff.",
      refs: ["docs/current-build-pathway.md", "docs/source-of-truth-map.md"],
    },
  ],
  connectorPostures: [
    {
      label: "Microsoft 365",
      posture: "planning-only",
      tone: "watch",
      detail: "Identity, records, collaboration, and signals wait for a later adapter boundary.",
    },
    {
      label: "QuickBooks",
      posture: "blocked money actions",
      tone: "blocked",
      detail: "Invoices, accounting, payments, and reconciliation stop for explicit approval.",
    },
    {
      label: "Graphify",
      posture: "read-only knowledge spoke",
      tone: "ready",
      detail: "Graph context can inform mission candidates, not approve or execute work.",
    },
    {
      label: "GitHub",
      posture: "private source spine",
      tone: "ready",
      detail: "Durable commits, issues, request records, and evidence references live here.",
    },
    {
      label: "Freedom Engine",
      posture: "phone and partner anchor",
      tone: "watch",
      detail: "Business partner UX, voice/mobile, and learning patterns remain outside runtime access.",
    },
    {
      label: "Local worker surfaces",
      posture: "dry-run local validation",
      tone: "complete",
      detail: "Worker claims and evidence are proven locally with no hosted relay or polling.",
    },
  ],
} as const;
