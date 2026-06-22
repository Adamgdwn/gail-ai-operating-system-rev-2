import { appShellDecision } from "./appShellDecision";

export function App() {
  return (
    <main className="app-shell" aria-label={appShellDecision.productName}>
      <section className="shell-panel">
        <p className="shell-kicker">Rev 2</p>
        <h1>{appShellDecision.productName}</h1>
        <p className="shell-status">{appShellDecision.statusLabel}</p>
      </section>
    </main>
  );
}
