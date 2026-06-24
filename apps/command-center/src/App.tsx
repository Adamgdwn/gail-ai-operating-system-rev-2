import { appShellDecision } from "./appShellDecision";
import {
  type CockpitStatusTone,
  type GovernedSpokeState,
  operatingCockpitSnapshot,
} from "./cockpitData";

const toneLabels: Record<CockpitStatusTone, string> = {
  ready: "Ready",
  watch: "Watch",
  blocked: "Blocked",
  complete: "Complete",
};

const spokeStateLabels: Record<GovernedSpokeState, string> = {
  idle: "Idle",
  active: "Active",
  "waiting-for-approval": "Waiting",
  blocked: "Blocked",
  complete: "Complete",
  gated: "Gated",
};

export function App() {
  const snapshot = operatingCockpitSnapshot;

  return (
    <main className="cockpit-shell" aria-label={appShellDecision.productName}>
      <header className="cockpit-header">
        <div className="cockpit-title-block">
          <p className="shell-kicker">Rev 2 Command Center</p>
          <h1>{appShellDecision.productName}</h1>
          <p className="shell-status">{appShellDecision.statusLabel}</p>
        </div>
        <dl className="shell-facts" aria-label="Current shell state">
          <div>
            <dt>Source</dt>
            <dd>{snapshot.source}</dd>
          </div>
          <div>
            <dt>Updated</dt>
            <dd>{snapshot.generatedAt}</dd>
          </div>
          <div>
            <dt>Phone</dt>
            <dd>Freedom anchor preserved</dd>
          </div>
        </dl>
      </header>

      <section className="cockpit-stage" aria-labelledby="hub-heading">
        <section className="operator-hub" aria-labelledby="hub-heading">
          <div className="hub-heading">
            <div>
              <p className="section-kicker">Operator Hub</p>
              <h2 id="hub-heading">Talk-first command surface</h2>
            </div>
            <StatusPill tone="watch" label="Static" />
          </div>
          <div className="intent-panel" aria-label="Current operator intent">
            <span className="intent-indicator" aria-hidden="true" />
            <p>{snapshot.hub.operatorIntent}</p>
          </div>
          <div className="hub-grid">
            <Meta label="Coordinator" value={snapshot.hub.coordinatorState} />
            <Meta label="Mission" value={snapshot.hub.currentMission} />
            <Meta label="Approval" value={snapshot.hub.approvalBoundary} />
            <Meta label="Phone" value={snapshot.hub.phoneHandoff} />
            <Meta label="Next" value={snapshot.hub.nextReview} />
          </div>
        </section>

        <ol className="spoke-arc" aria-label="Observable governed spokes">
          {snapshot.governedSpokes.map((spoke) => (
            <li className={`spoke-card state-${spoke.state}`} key={spoke.id}>
              <div className="spoke-topline">
                <span className="spoke-label">{spoke.label}</span>
                <StatusPill tone={spoke.tone} label={spokeStateLabels[spoke.state]} />
              </div>
              <h3>{spoke.system}</h3>
              <p className="spoke-role">{spoke.role}</p>
              <p>{spoke.coordination}</p>
              <dl className="spoke-boundary">
                <div>
                  <dt>Boundary</dt>
                  <dd>{spoke.boundary}</dd>
                </div>
                <div>
                  <dt>Observed</dt>
                  <dd>{spoke.observed}</dd>
                </div>
              </dl>
            </li>
          ))}
        </ol>
      </section>

      <section className="review-grid" aria-label="Operating detail">
        <section className="surface surface-primary" aria-labelledby="mission-heading">
          <div className="surface-heading">
            <div>
              <p className="section-kicker">Mission Spine</p>
              <h2 id="mission-heading">{snapshot.mission.title}</h2>
            </div>
            <StatusPill tone="complete" label={snapshot.mission.status} />
          </div>
          <div className="mission-meta">
            <Meta label="Request" value={snapshot.mission.requestId} />
            <Meta label="Mission" value={snapshot.mission.missionId} />
            <Meta label="Domain" value={snapshot.mission.domain} />
            <Meta label="Approval" value={snapshot.mission.approvalLevel} />
            <Meta label="Data" value={snapshot.mission.dataClass} />
          </div>
          <p className="mission-focus">{snapshot.mission.currentFocus}</p>
          <ol className="step-list" aria-label="Local proof steps">
            {snapshot.mission.steps.map((step) => (
              <li className="step-row" key={step.name}>
                <span className={`step-marker tone-${step.status}`} />
                <div>
                  <strong>{step.label}</strong>
                  <span>{step.summary}</span>
                </div>
              </li>
            ))}
          </ol>
        </section>

        <section className="surface" aria-labelledby="approval-heading">
          <div className="surface-heading compact">
            <div>
              <p className="section-kicker">Approval Boundary</p>
              <h2 id="approval-heading">{snapshot.approval.envelopeId}</h2>
            </div>
            <StatusPill tone="watch" label="Read-only" />
          </div>
          <div className="approval-grid">
            <Meta label="Actor" value={snapshot.approval.actor} />
            <Meta label="Device" value={snapshot.approval.deviceRole} />
            <Meta label="Level" value={snapshot.approval.approvalLevel} />
            <Meta label="Capability" value={snapshot.approval.requestedCapability} />
            <Meta label="Status" value={snapshot.approval.relayStatus} />
          </div>
          <div className="trigger-strip" aria-label="Stop triggers">
            {snapshot.approval.stopTriggers.map((trigger) => (
              <span key={trigger}>{trigger}</span>
            ))}
          </div>
        </section>

        <section className="surface" aria-labelledby="workers-heading">
          <div className="surface-heading compact">
            <div>
              <p className="section-kicker">Workers + Devices</p>
              <h2 id="workers-heading">Claim Posture</h2>
            </div>
          </div>
          <div className="row-list">
            {snapshot.workers.map((worker) => (
              <div className="status-row" key={worker.id}>
                <div>
                  <strong>{worker.label}</strong>
                  <span>{worker.role}</span>
                </div>
                <div className="row-state">
                  <StatusPill tone={worker.tone} label={toneLabels[worker.tone]} />
                  <span>{worker.status}</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="surface" aria-labelledby="evidence-heading">
          <div className="surface-heading compact">
            <div>
              <p className="section-kicker">Evidence Ledger</p>
              <h2 id="evidence-heading">Reference Records</h2>
            </div>
          </div>
          <div className="evidence-list">
            {snapshot.evidence.map((item) => (
              <article className="evidence-item" key={item.id}>
                <strong>{item.label}</strong>
                <p>{item.summary}</p>
                <ul>
                  {item.refs.map((ref) => (
                    <li key={ref}>{ref}</li>
                  ))}
                </ul>
              </article>
            ))}
          </div>
        </section>

        <section className="surface surface-wide" aria-labelledby="connectors-heading">
          <div className="surface-heading compact">
            <div>
              <p className="section-kicker">Governed Spokes</p>
              <h2 id="connectors-heading">Connector Posture</h2>
            </div>
          </div>
          <div className="connector-grid">
            {snapshot.connectorPostures.map((connector) => (
              <div className="connector-row" key={connector.label}>
                <div>
                  <strong>{connector.label}</strong>
                  <span>{connector.detail}</span>
                </div>
                <StatusPill tone={connector.tone} label={connector.posture} />
              </div>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}

function Meta({ label, value }: { readonly label: string; readonly value: string }) {
  return (
    <div className="meta-item">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function StatusPill({
  tone,
  label,
}: {
  readonly tone: CockpitStatusTone;
  readonly label: string;
}) {
  return <span className={`status-pill tone-${tone}`}>{label}</span>;
}
