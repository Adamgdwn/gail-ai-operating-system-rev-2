import {
  type AgentSummary,
  type ConnectorSummary,
  type EvidenceSummary,
  type SharedReadModel,
  type TraceEventSummary,
} from "./readModelClient";

export type CockpitStatusTone = "ready" | "watch" | "blocked" | "complete";
export type GovernedSpokeState =
  | "idle"
  | "active"
  | "waiting-for-approval"
  | "blocked"
  | "complete"
  | "gated";

export interface MissionStep {
  readonly name: string;
  readonly label: string;
  readonly status: CockpitStatusTone;
  readonly summary: string;
}

export interface MissionSnapshot {
  readonly requestId: string;
  readonly missionId: string;
  readonly traceId: string;
  readonly title: string;
  readonly status: string;
  readonly domain: string;
  readonly approvalLevel: string;
  readonly dataClass: string;
  readonly currentFocus: string;
  readonly steps: readonly MissionStep[];
}

export interface TalkHubSnapshot {
  readonly operatorIntent: string;
  readonly coordinatorState: string;
  readonly approvalBoundary: string;
  readonly currentMission: string;
  readonly phoneHandoff: string;
  readonly nextReview: string;
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

export interface GovernedSpokeSnapshot {
  readonly id: string;
  readonly label: string;
  readonly system: string;
  readonly state: GovernedSpokeState;
  readonly tone: CockpitStatusTone;
  readonly role: string;
  readonly coordination: string;
  readonly boundary: string;
  readonly observed: string;
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
  readonly freshness: string;
  readonly hub: TalkHubSnapshot;
  readonly mission: MissionSnapshot;
  readonly approval: ApprovalSnapshot;
  readonly governedSpokes: readonly GovernedSpokeSnapshot[];
  readonly workers: readonly WorkerSnapshot[];
  readonly evidence: readonly EvidenceSnapshot[];
  readonly connectorPostures: readonly ConnectorPosture[];
}

const FAMILY_LABELS: Readonly<Record<string, string>> = {
  "Microsoft 365": "M365",
  Graphify: "Graphify",
  QuickBooks: "QB",
  GitHub: "GitHub",
  "Local Device": "Workers",
  "Client Gateway": "Client",
  "Vendor Or Deployment": "Vendor",
};

export const waitingCockpitSnapshot: OperatingCockpitSnapshot = {
  generatedAt: "Not connected",
  source: "GAIL OS read model API",
  freshness: "Waiting for live read model",
  hub: {
    operatorIntent: "Connect to the governed read model before acting.",
    coordinatorState: "Command center is waiting for GAIL OS.",
    approvalBoundary: "Read-only surface, no mutation controls exposed",
    currentMission: "No live read-model response yet",
    phoneHandoff: "Freedom remains the phone-side operator anchor.",
    nextReview: "Start GAIL OS API and refresh this surface.",
  },
  mission: {
    requestId: "Unavailable",
    missionId: "Unavailable",
    traceId: "Unavailable",
    title: "Live mission posture unavailable",
    status: "not connected",
    domain: "read-model",
    approvalLevel: "R0 observe only",
    dataClass: "safe summaries",
    currentFocus: "No live read-model records are being rendered yet.",
    steps: [
      {
        name: "config",
        label: "Configuration",
        status: "watch",
        summary: "Local proxy and API key posture must be available.",
      },
      {
        name: "api",
        label: "API reachability",
        status: "watch",
        summary: "GAIL OS read model has not returned state yet.",
      },
      {
        name: "ledger",
        label: "Evidence freshness",
        status: "watch",
        summary: "Trace events and evidence will appear after connection.",
      },
    ],
  },
  approval: {
    envelopeId: "read-only",
    actor: "Adam",
    deviceRole: "Command center browser",
    approvalLevel: "R0 observe",
    requestedCapability: "read-model",
    relayStatus: "not connected",
    stopTriggers: [
      "live_connector_action",
      "m365_live_content_read",
      "external_message_send",
      "graphify_action_execution",
      "r4_live_execution",
    ],
  },
  governedSpokes: [],
  workers: [],
  evidence: [
    {
      id: "empty-ledger",
      label: "No live evidence rendered",
      summary: "Evidence records will load from the GAIL OS read model.",
      refs: ["GET /api/v1/read-model"],
    },
  ],
  connectorPostures: [],
};

export function cockpitSnapshotFromReadModel(
  readModel: SharedReadModel,
  isStale: boolean,
): OperatingCockpitSnapshot {
  const latestEvent = readModel.recentEvents[0] ?? null;
  const latestEvidence = readModel.recentEvidence[0] ?? null;
  const latestTraceId =
    latestEvent?.cnsTraceId ?? latestEvidence?.cnsTraceId ?? "No trace yet";
  const latestMissionId =
    latestEvent?.missionId ?? latestEvidence?.missionId ?? "No mission yet";
  const latestActionId =
    latestEvent?.actionId ?? latestEvidence?.actionId ?? "No action yet";
  const latestRecordAt = latestTimestamp(readModel);
  const hasLedgerRecords =
    readModel.recentEvents.length > 0 || readModel.recentEvidence.length > 0;

  return {
    generatedAt: readModel.generatedAt,
    source: `GAIL OS ${readModel.schemaVersion}`,
    freshness: isStale ? "Stale read model" : "Fresh read model",
    hub: {
      operatorIntent: "Observe governed state before any system acts.",
      coordinatorState: `${readModel.health.status} - ${readModel.health.boundary}`,
      approvalBoundary: authorityBoundary(readModel),
      currentMission: latestEvent?.summary ?? "No lifecycle event recorded yet",
      phoneHandoff: "Freedom remains the phone-side operator anchor.",
      nextReview: latestRecordAt
        ? `Latest record ${latestRecordAt}`
        : "No trace or evidence records yet",
    },
    mission: {
      requestId: latestEvent?.idempotencyKey ?? "No idempotency key yet",
      missionId: latestMissionId,
      traceId: latestTraceId,
      title: latestEvent?.summary ?? "No mission event recorded yet",
      status: latestEvent?.status ?? latestEvidence?.result ?? "no lifecycle records",
      domain: latestEvent?.sourceSystem ?? "read-model",
      approvalLevel: readModel.authority.autonomyLevel,
      dataClass: "safe summaries and references",
      currentFocus: hasLedgerRecords
        ? `Latest action reference: ${latestActionId}`
        : "The cockpit is connected, but the local trace/evidence stores are empty.",
      steps: lifecycleSteps(readModel, hasLedgerRecords),
    },
    approval: {
      envelopeId: readModel.authority.source,
      actor: "Adam / governed operator",
      deviceRole: "Laptop, tablet, phone fallback through Freedom",
      approvalLevel: readModel.authority.autonomyLevel,
      requestedCapability: "read-only posture and evidence inspection",
      relayStatus: readModel.health.liveExecutionEnabled
        ? "live execution flag is on"
        : "read-only, no live execution",
      stopTriggers: [
        "live_connector_action",
        "m365_live_content_read",
        "external_message_send",
        "graphify_action_execution",
        "r4_live_execution",
      ],
    },
    governedSpokes: governedSpokesFromReadModel(readModel),
    workers: workersFromReadModel(readModel),
    evidence: evidenceFromReadModel(readModel),
    connectorPostures: connectorPosturesFromReadModel(readModel),
  };
}

export function readModelHasNoLedgerRecords(readModel: SharedReadModel): boolean {
  return readModel.recentEvents.length === 0 && readModel.recentEvidence.length === 0;
}

function lifecycleSteps(
  readModel: SharedReadModel,
  hasLedgerRecords: boolean,
): readonly MissionStep[] {
  return [
    {
      name: "health",
      label: "GAIL OS health",
      status: readModel.health.status === "ok" ? "ready" : "blocked",
      summary: `${readModel.health.status} in ${readModel.health.boundary}`,
    },
    {
      name: "authority",
      label: "Authority posture",
      status:
        readModel.authority.registryValid && !readModel.authority.liveExecutionEnabled
          ? "ready"
          : "blocked",
      summary: authorityBoundary(readModel),
    },
    {
      name: "connectors",
      label: "Connector registry",
      status:
        readModel.connectors.registryValid && !readModel.connectors.liveAccessEnabled
          ? "ready"
          : "blocked",
      summary: `${readModel.connectors.connectorCount} connectors, ${stateCounts(
        readModel.connectors.byState,
      )}`,
    },
    {
      name: "agents",
      label: "Agent registry",
      status:
        readModel.agents.registryValid && !readModel.agents.liveAccessEnabled
          ? "ready"
          : "blocked",
      summary: `${readModel.agents.agentCount} agents, ${stateCounts(
        readModel.agents.byMaturity,
      )}`,
    },
    {
      name: "m365",
      label: "Microsoft 365",
      status: "watch",
      summary: `${readModel.m365.identityBoundary}; ${readModel.m365.appOnlyProfileState}`,
    },
    {
      name: "ledger",
      label: "Trace and evidence",
      status: hasLedgerRecords ? "complete" : "watch",
      summary: `${readModel.recentEvents.length} events and ${readModel.recentEvidence.length} evidence refs`,
    },
  ];
}

function governedSpokesFromReadModel(
  readModel: SharedReadModel,
): readonly GovernedSpokeSnapshot[] {
  const connectors = readModel.connectors.connectors;
  const families = [
    "Microsoft 365",
    "Freedom",
    "Graphify",
    "QuickBooks",
    "GitHub",
    "Evidence",
    "Local Device",
  ] as const;

  return families.map((family) => {
    if (family === "Freedom") {
      return freedomSpoke(readModel.agents.agents);
    }
    if (family === "Evidence") {
      return evidenceSpoke(readModel);
    }
    const connector = connectorByFamily(connectors, family);
    return connector
      ? connectorSpoke(connector)
      : missingConnectorSpoke(family, FAMILY_LABELS[family] ?? family);
  });
}

function connectorSpoke(connector: ConnectorSummary): GovernedSpokeSnapshot {
  const tone = connector.liveAccessEnabled ? "blocked" : "watch";
  return {
    id: connector.connectorId,
    label: FAMILY_LABELS[connector.systemFamily] ?? connector.systemFamily,
    system: connector.displayName,
    state: connector.liveAccessEnabled ? "blocked" : stateFromConnector(connector),
    tone,
    role: connector.systemFamily,
    coordination: capabilitySummary(connector.allowedCapabilities),
    boundary: connector.liveAccessEnabled
      ? "Live access flag is enabled; stop for review."
      : "Read-only registry posture; no connector action exposed.",
    observed: connector.currentState,
  };
}

function missingConnectorSpoke(
  family: string,
  label: string,
): GovernedSpokeSnapshot {
  return {
    id: `missing-${family.toLowerCase().replaceAll(" ", "-")}`,
    label,
    system: family,
    state: "blocked",
    tone: "blocked",
    role: "missing connector profile",
    coordination: "Connector family was expected but not present in the registry.",
    boundary: "Stop before assuming capability.",
    observed: "not registered",
  };
}

function freedomSpoke(agents: readonly AgentSummary[]): GovernedSpokeSnapshot {
  const freedomAgents = agents.filter((agent) => agent.cnsLayer === "freedom");
  const liveAccessEnabled = freedomAgents.some((agent) => agent.liveAccessEnabled);
  return {
    id: "freedom-agent-surface",
    label: "Freedom",
    system: "Freedom agent layer",
    state: liveAccessEnabled ? "blocked" : "gated",
    tone: liveAccessEnabled ? "blocked" : "watch",
    role: "phone and partner anchor",
    coordination: `${freedomAgents.length} Freedom profiles registered.`,
    boundary: "Augments the command center; execution still routes through GAIL OS authority.",
    observed: liveAccessEnabled ? "live flag present" : "registered, no live access",
  };
}

function evidenceSpoke(readModel: SharedReadModel): GovernedSpokeSnapshot {
  const count = readModel.recentEvidence.length;
  return {
    id: "evidence-ledger",
    label: "Evidence",
    system: "Evidence ledger",
    state: count > 0 ? "complete" : "idle",
    tone: count > 0 ? "complete" : "watch",
    role: "audit trail",
    coordination: `${count} recent evidence references returned.`,
    boundary: "Safe references only; no raw provider payloads shown.",
    observed: count > 0 ? "evidence refs present" : "empty",
  };
}

function workersFromReadModel(readModel: SharedReadModel): readonly WorkerSnapshot[] {
  const agentRows = readModel.agents.agents.slice(0, 6).map((agent) => ({
    id: agent.agentId,
    label: agent.displayName,
    role: `${agent.cnsLayer} - ${agent.maxAuthorityLevel}`,
    status: agent.liveAccessEnabled
      ? "live access flag present"
      : `${agent.maturity}, no live access`,
    tone: agent.liveAccessEnabled ? "blocked" : ("ready" as CockpitStatusTone),
  }));

  if (agentRows.length > 0) {
    return agentRows;
  }

  return [
    {
      id: "no-agent-profiles",
      label: "No agent profiles",
      role: "registry",
      status: "GAIL OS returned an empty agent registry",
      tone: "watch",
    },
  ];
}

function evidenceFromReadModel(
  readModel: SharedReadModel,
): readonly EvidenceSnapshot[] {
  if (readModel.recentEvidence.length === 0 && readModel.recentEvents.length === 0) {
    return [
      {
        id: "empty-ledger",
        label: "No trace or evidence records yet",
        summary: "The read model is reachable, but local lifecycle stores are empty.",
        refs: ["GET /api/v1/read-model"],
      },
    ];
  }

  const evidenceRows = readModel.recentEvidence.slice(0, 5).map((item) => ({
    id: item.evidenceId,
    label: item.result,
    summary: item.outcomeSummary,
    refs: compactRefs([
      item.evidenceId,
      item.cnsTraceId,
      item.missionId,
      item.actionId,
      item.executionMode,
    ]),
  }));
  const eventRows = readModel.recentEvents.slice(0, 3).map((event) => ({
    id: event.eventId,
    label: event.eventType,
    summary: event.summary,
    refs: compactRefs([
      event.cnsTraceId,
      event.missionId,
      event.actionId,
      event.evidenceId,
      event.occurredAt,
    ]),
  }));
  return [...evidenceRows, ...eventRows];
}

function connectorPosturesFromReadModel(
  readModel: SharedReadModel,
): readonly ConnectorPosture[] {
  return readModel.connectors.connectors.map((connector) => ({
    label: connector.displayName,
    posture: connector.liveAccessEnabled ? "live flag present" : connector.currentState,
    tone: connector.liveAccessEnabled ? "blocked" : ("watch" as CockpitStatusTone),
    detail: `${connector.systemFamily}; ${capabilitySummary(
      connector.allowedCapabilities,
    )}`,
  }));
}

function connectorByFamily(
  connectors: readonly ConnectorSummary[],
  family: string,
): ConnectorSummary | null {
  return (
    connectors.find((connector) => connector.systemFamily === family) ?? null
  );
}

function stateFromConnector(connector: ConnectorSummary): GovernedSpokeState {
  if (connector.currentState === "registry-only") {
    return "idle";
  }
  if (connector.currentState === "inventory-only") {
    return "waiting-for-approval";
  }
  return "gated";
}

function authorityBoundary(readModel: SharedReadModel): string {
  const r5 = readModel.authority.r5HumanOnly ? "R5 human-only" : "R5 not enforced";
  const r4 = readModel.authority.r4RequiresAuthorityEnvelope
    ? "R4 requires AuthorityEnvelope"
    : "R4 envelope flag missing";
  const live = readModel.authority.liveExecutionEnabled
    ? "live execution flag on"
    : "no live execution";
  return `${readModel.authority.autonomyLevel}; ${r4}; ${r5}; ${live}`;
}

function capabilitySummary(capabilities: readonly string[]): string {
  if (capabilities.length === 0) {
    return "no capabilities listed";
  }
  return capabilities.slice(0, 3).join(", ");
}

function stateCounts(counts: Readonly<Record<string, number>>): string {
  const entries = Object.entries(counts);
  if (entries.length === 0) {
    return "no counts";
  }
  return entries.map(([label, count]) => `${label}: ${count}`).join(", ");
}

function latestTimestamp(readModel: SharedReadModel): string | null {
  const timestamps = [
    ...readModel.recentEvents.map((event) => event.occurredAt),
    ...readModel.recentEvidence.map((evidence) => evidence.createdAt),
  ].filter(Boolean);
  if (timestamps.length === 0) {
    return null;
  }
  return timestamps.sort().at(-1) ?? null;
}

function compactRefs(values: readonly (string | null)[]): readonly string[] {
  return values.filter((value): value is string => Boolean(value));
}
