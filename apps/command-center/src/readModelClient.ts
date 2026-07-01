export interface CommandCenterConfig {
  readonly apiBaseUrl: string;
  readonly authMode: "local-vite-proxy" | "external-proxy";
  readonly hasLocalProxyApiKey: boolean;
  readonly requestTimeoutMs: number;
  readonly staleAfterMs: number;
}

export interface SharedReadModel {
  readonly schemaVersion: string;
  readonly generatedAt: string;
  readonly health: HealthStatus;
  readonly authority: AuthorityStatus;
  readonly connectors: ConnectorRegistryStatus;
  readonly agents: AgentRegistryStatus;
  readonly m365: M365Status;
  readonly recentEvents: readonly TraceEventSummary[];
  readonly recentEvidence: readonly EvidenceSummary[];
}

export interface HealthStatus {
  readonly status: string;
  readonly boundary: string;
  readonly phase: string;
  readonly liveExecutionEnabled: boolean;
}

export interface AuthorityStatus {
  readonly registryValid: boolean;
  readonly source: string;
  readonly boundary: string;
  readonly autonomyLevel: string;
  readonly liveExecutionEnabled: boolean;
  readonly r4RequiresAuthorityEnvelope: boolean;
  readonly r5HumanOnly: boolean;
  readonly authorityLevels: readonly AuthorityLevelSummary[];
}

export interface AuthorityLevelSummary {
  readonly level: string;
  readonly name: string;
  readonly meaning: string;
  readonly agentBoundary: string;
}

export interface ConnectorRegistryStatus {
  readonly registryValid: boolean;
  readonly connectorCount: number;
  readonly liveAccessEnabled: boolean;
  readonly byState: Readonly<Record<string, number>>;
  readonly bySystemFamily: Readonly<Record<string, number>>;
  readonly connectors: readonly ConnectorSummary[];
}

export interface ConnectorSummary {
  readonly connectorId: string;
  readonly displayName: string;
  readonly systemFamily: string;
  readonly currentState: string;
  readonly allowedCapabilities: readonly string[];
  readonly liveAccessEnabled: boolean;
}

export interface AgentRegistryStatus {
  readonly registryValid: boolean;
  readonly agentCount: number;
  readonly liveAccessEnabled: boolean;
  readonly byCnsLayer: Readonly<Record<string, number>>;
  readonly byMaturity: Readonly<Record<string, number>>;
  readonly agents: readonly AgentSummary[];
}

export interface AgentSummary {
  readonly agentId: string;
  readonly displayName: string;
  readonly cnsLayer: string;
  readonly maturity: string;
  readonly maxAuthorityLevel: string;
  readonly liveAccessEnabled: boolean;
}

export interface M365Status {
  readonly configured: boolean;
  readonly tenantIdPresent: boolean;
  readonly clientIdPresent: boolean;
  readonly clientSecretPresent: boolean;
  readonly scope: string;
  readonly boundary: string;
  readonly identityBoundary: string;
  readonly appOnlyProfileState: string;
  readonly note: string;
}

export interface TraceEventSummary {
  readonly eventId: string;
  readonly cnsTraceId: string;
  readonly eventType: string;
  readonly occurredAt: string;
  readonly sourceSystem: string;
  readonly sourceRef: string;
  readonly summary: string;
  readonly missionId: string | null;
  readonly actionId: string | null;
  readonly evidenceId: string | null;
  readonly authorityRef: string | null;
  readonly status: string | null;
  readonly riskTier: number | null;
  readonly idempotencyKey: string | null;
  readonly duplicateDetected: boolean;
  readonly duplicateOfEventId: string | null;
}

export interface EvidenceSummary {
  readonly evidenceId: string;
  readonly cnsTraceId: string | null;
  readonly missionId: string;
  readonly actionId: string;
  readonly result: string;
  readonly executionMode: string;
  readonly actionType: string;
  readonly createdAt: string;
  readonly outcomeSummary: string;
}

export class ReadModelHttpError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
    this.name = "ReadModelHttpError";
  }
}

export class ReadModelUnavailableError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ReadModelUnavailableError";
  }
}

export class ReadModelProtocolError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ReadModelProtocolError";
  }
}

export function getCommandCenterConfig(): CommandCenterConfig {
  const apiBaseUrl = stringEnv("VITE_GAIL_OS_API_BASE_URL", "/gail-os-api");
  const authMode =
    stringEnv("VITE_GAIL_OS_AUTH_MODE", "local-vite-proxy") === "external-proxy"
      ? "external-proxy"
      : "local-vite-proxy";

  return {
    apiBaseUrl,
    authMode,
    hasLocalProxyApiKey: stringEnv("VITE_GAIL_OS_PROXY_HAS_API_KEY", "") === "true",
    requestTimeoutMs: positiveIntegerEnv("VITE_GAIL_OS_API_TIMEOUT_MS", 8000),
    staleAfterMs: positiveIntegerEnv("VITE_GAIL_OS_STALE_AFTER_MS", 300000),
  };
}

export function isApiConfigMissing(config: CommandCenterConfig): boolean {
  return config.authMode === "local-vite-proxy" && !config.hasLocalProxyApiKey;
}

export async function fetchSharedReadModel(
  config: CommandCenterConfig,
): Promise<SharedReadModel> {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), config.requestTimeoutMs);

  try {
    const response = await fetch(readModelUrl(config.apiBaseUrl), {
      cache: "no-store",
      headers: {
        Accept: "application/json",
      },
      signal: controller.signal,
    });

    if (response.status === 401 || response.status === 403) {
      throw new ReadModelHttpError(
        "GAIL OS rejected the command-center read request.",
        response.status,
      );
    }

    if (!response.ok) {
      throw new ReadModelHttpError(
        `GAIL OS read model returned HTTP ${response.status}.`,
        response.status,
      );
    }

    const payload: unknown = await response.json();
    return parseSharedReadModel(payload);
  } catch (error) {
    if (
      error instanceof ReadModelHttpError ||
      error instanceof ReadModelProtocolError
    ) {
      throw error;
    }
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ReadModelUnavailableError("GAIL OS read model request timed out.");
    }
    throw new ReadModelUnavailableError("GAIL OS read model is unreachable.");
  } finally {
    window.clearTimeout(timeout);
  }
}

export function readModelIsStale(
  readModel: SharedReadModel,
  staleAfterMs: number,
  nowMs = Date.now(),
): boolean {
  const generatedAtMs = Date.parse(readModel.generatedAt);
  if (Number.isNaN(generatedAtMs)) {
    return true;
  }
  return nowMs - generatedAtMs > staleAfterMs;
}

function readModelUrl(apiBaseUrl: string): string {
  return `${apiBaseUrl.replace(/\/+$/, "")}/read-model?limit=25`;
}

function parseSharedReadModel(payload: unknown): SharedReadModel {
  const record = requireRecord(payload, "read model");
  const health = requireRecord(record.health, "health");
  const authority = requireRecord(record.authority, "authority");
  const connectors = requireRecord(record.connectors, "connectors");
  const agents = requireRecord(record.agents, "agents");
  const m365 = requireRecord(record.m365, "m365");

  return {
    schemaVersion: requireString(record, "schema_version"),
    generatedAt: requireString(record, "generated_at"),
    health: {
      status: requireString(health, "status"),
      boundary: requireString(health, "boundary"),
      phase: requireString(health, "phase"),
      liveExecutionEnabled: requireBoolean(health, "live_execution_enabled"),
    },
    authority: {
      registryValid: requireBoolean(authority, "registry_valid"),
      source: requireString(authority, "source"),
      boundary: requireString(authority, "boundary"),
      autonomyLevel: requireString(authority, "autonomy_level"),
      liveExecutionEnabled: requireBoolean(authority, "live_execution_enabled"),
      r4RequiresAuthorityEnvelope: requireBoolean(
        authority,
        "r4_requires_authority_envelope",
      ),
      r5HumanOnly: requireBoolean(authority, "r5_human_only"),
      authorityLevels: requireArray(authority, "authority_levels").map(
        parseAuthorityLevel,
      ),
    },
    connectors: {
      registryValid: requireBoolean(connectors, "registry_valid"),
      connectorCount: requireNumber(connectors, "connector_count"),
      liveAccessEnabled: requireBoolean(connectors, "live_access_enabled"),
      byState: readCountRecord(connectors.by_state, "connectors.by_state"),
      bySystemFamily: readCountRecord(
        connectors.by_system_family,
        "connectors.by_system_family",
      ),
      connectors: requireArray(connectors, "connectors").map(parseConnector),
    },
    agents: {
      registryValid: requireBoolean(agents, "registry_valid"),
      agentCount: requireNumber(agents, "agent_count"),
      liveAccessEnabled: requireBoolean(agents, "live_access_enabled"),
      byCnsLayer: readCountRecord(agents.by_cns_layer, "agents.by_cns_layer"),
      byMaturity: readCountRecord(agents.by_maturity, "agents.by_maturity"),
      agents: requireArray(agents, "agents").map(parseAgent),
    },
    m365: {
      configured: requireBoolean(m365, "configured"),
      tenantIdPresent: requireBoolean(m365, "tenant_id_present"),
      clientIdPresent: requireBoolean(m365, "client_id_present"),
      clientSecretPresent: requireBoolean(m365, "client_secret_present"),
      scope: requireString(m365, "scope"),
      boundary: requireString(m365, "boundary"),
      identityBoundary: requireString(m365, "identity_boundary"),
      appOnlyProfileState: requireString(m365, "app_only_profile_state"),
      note: requireString(m365, "note"),
    },
    recentEvents: requireArray(record, "recent_events").map(parseTraceEvent),
    recentEvidence: requireArray(record, "recent_evidence").map(parseEvidence),
  };
}

function parseAuthorityLevel(value: unknown): AuthorityLevelSummary {
  const record = requireRecord(value, "authority level");
  return {
    level: requireString(record, "level"),
    name: requireString(record, "name"),
    meaning: requireString(record, "meaning"),
    agentBoundary: requireString(record, "agent_boundary"),
  };
}

function parseConnector(value: unknown): ConnectorSummary {
  const record = requireRecord(value, "connector");
  return {
    connectorId: requireString(record, "connector_id"),
    displayName: requireString(record, "display_name"),
    systemFamily: requireString(record, "system_family"),
    currentState: requireString(record, "current_state"),
    allowedCapabilities: readStringArray(record, "allowed_capabilities"),
    liveAccessEnabled: requireBoolean(record, "live_access_enabled"),
  };
}

function parseAgent(value: unknown): AgentSummary {
  const record = requireRecord(value, "agent");
  return {
    agentId: requireString(record, "agent_id"),
    displayName: requireString(record, "display_name"),
    cnsLayer: requireString(record, "cns_layer"),
    maturity: requireString(record, "maturity"),
    maxAuthorityLevel: requireString(record, "max_authority_level"),
    liveAccessEnabled: requireBoolean(record, "live_access_enabled"),
  };
}

function parseTraceEvent(value: unknown): TraceEventSummary {
  const record = requireRecord(value, "trace event");
  return {
    eventId: requireString(record, "event_id"),
    cnsTraceId: requireString(record, "cns_trace_id"),
    eventType: requireString(record, "event_type"),
    occurredAt: requireString(record, "occurred_at"),
    sourceSystem: requireString(record, "source_system"),
    sourceRef: requireString(record, "source_ref"),
    summary: requireString(record, "summary"),
    missionId: optionalString(record, "mission_id"),
    actionId: optionalString(record, "action_id"),
    evidenceId: optionalString(record, "evidence_id"),
    authorityRef: optionalString(record, "authority_ref"),
    status: optionalString(record, "status"),
    riskTier: optionalNumber(record, "risk_tier"),
    idempotencyKey: optionalString(record, "idempotency_key"),
    duplicateDetected: requireBoolean(record, "duplicate_detected"),
    duplicateOfEventId: optionalString(record, "duplicate_of_event_id"),
  };
}

function parseEvidence(value: unknown): EvidenceSummary {
  const record = requireRecord(value, "evidence");
  return {
    evidenceId: requireString(record, "evidence_id"),
    cnsTraceId: optionalString(record, "cns_trace_id"),
    missionId: requireString(record, "mission_id"),
    actionId: requireString(record, "action_id"),
    result: requireString(record, "result"),
    executionMode: requireString(record, "execution_mode"),
    actionType: requireString(record, "action_type"),
    createdAt: requireString(record, "created_at"),
    outcomeSummary: requireString(record, "outcome_summary"),
  };
}

function requireRecord(
  value: unknown,
  label: string,
): Readonly<Record<string, unknown>> {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new ReadModelProtocolError(`${label} must be an object.`);
  }
  return value as Readonly<Record<string, unknown>>;
}

function requireArray(
  record: Readonly<Record<string, unknown>>,
  key: string,
): readonly unknown[] {
  const value = record[key];
  if (!Array.isArray(value)) {
    throw new ReadModelProtocolError(`${key} must be an array.`);
  }
  return value;
}

function requireString(
  record: Readonly<Record<string, unknown>>,
  key: string,
): string {
  const value = record[key];
  if (typeof value !== "string") {
    throw new ReadModelProtocolError(`${key} must be a string.`);
  }
  return value;
}

function optionalString(
  record: Readonly<Record<string, unknown>>,
  key: string,
): string | null {
  const value = record[key];
  if (value === null || value === undefined) {
    return null;
  }
  if (typeof value !== "string") {
    throw new ReadModelProtocolError(`${key} must be a string or null.`);
  }
  return value;
}

function requireBoolean(
  record: Readonly<Record<string, unknown>>,
  key: string,
): boolean {
  const value = record[key];
  if (typeof value !== "boolean") {
    throw new ReadModelProtocolError(`${key} must be a boolean.`);
  }
  return value;
}

function requireNumber(
  record: Readonly<Record<string, unknown>>,
  key: string,
): number {
  const value = record[key];
  if (typeof value !== "number" || !Number.isFinite(value)) {
    throw new ReadModelProtocolError(`${key} must be a finite number.`);
  }
  return value;
}

function optionalNumber(
  record: Readonly<Record<string, unknown>>,
  key: string,
): number | null {
  const value = record[key];
  if (value === null || value === undefined) {
    return null;
  }
  if (typeof value !== "number" || !Number.isFinite(value)) {
    throw new ReadModelProtocolError(`${key} must be a finite number or null.`);
  }
  return value;
}

function readStringArray(
  record: Readonly<Record<string, unknown>>,
  key: string,
): readonly string[] {
  return requireArray(record, key).map((item) => {
    if (typeof item !== "string") {
      throw new ReadModelProtocolError(`${key} must contain only strings.`);
    }
    return item;
  });
}

function readCountRecord(
  value: unknown,
  label: string,
): Readonly<Record<string, number>> {
  const record = requireRecord(value, label);
  return Object.fromEntries(
    Object.entries(record).map(([key, count]) => {
      if (typeof count !== "number" || !Number.isFinite(count)) {
        throw new ReadModelProtocolError(`${label}.${key} must be a number.`);
      }
      return [key, count];
    }),
  );
}

function stringEnv(key: string, fallback: string): string {
  const value = import.meta.env[key];
  return typeof value === "string" && value.trim() ? value.trim() : fallback;
}

function positiveIntegerEnv(key: string, fallback: number): number {
  const value = import.meta.env[key];
  if (typeof value !== "string") {
    return fallback;
  }
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}
