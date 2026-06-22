"""End-to-end local no-network proof runner for the Rev 2 core spine."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .connector_registry import ConnectorOperationRequest, ConnectorRegistry
from .mission_spine import (
    LocalMissionStore,
    MissionEnvelope,
    PermissionGate,
    build_local_plan,
    create_mission,
    current_timestamp,
)
from .relay_envelope import PROJECT_ID, SCHEMA_VERSION, RelayEnvelope, RelayValidationContext, validate_relay_envelope
from .relay_store import LocalRelayRecordStore, RelayEvidenceRecord, RelayWorkerClaim


DEFAULT_PROOF_COMMAND = "Build a synthetic local proof path from intent to validated evidence."
DEFAULT_PROOF_REQUEST_ID = "REQ-LOCAL-PROOF-001"
DEFAULT_REPO_STATE_REF = "local-proof-repo-state"
DEFAULT_GRAPH_SNAPSHOT_REF = "local-proof-graph-snapshot"
LOCAL_PROOF_CONNECTOR_ID = "local-device-worker-surfaces"
PHONE_DEVICE_ID = "android-phone-001"
WORKER_DEVICE_ID = "linux-worker-001"

RELAY_STOP_TRIGGERS = (
    "portal_or_relay_live_action",
    "hosted_relay_or_worker_action",
    "secret_exposure",
    "client_data_access",
    "raw_payload_retention",
    "graphify_action_execution",
)


class LocalProofError(RuntimeError):
    """Raised when the local proof cannot safely advance to the next step."""

    def __init__(self, step: str, reasons: Iterable[str]) -> None:
        self.step = step
        self.reasons = tuple(str(reason) for reason in reasons if str(reason).strip())
        detail = "; ".join(self.reasons) or "Local proof step failed."
        super().__init__(f"{step}: {detail}")


@dataclass(frozen=True)
class LocalProofStep:
    """One successful boundary crossed by the local proof runner."""

    name: str
    summary: str
    evidence_refs: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "summary": self.summary,
            "evidence_refs": list(self.evidence_refs),
        }


@dataclass(frozen=True)
class LocalProofReport:
    """Compact evidence that one local mission reached validated evidence."""

    request_id: str
    mission_id: str
    envelope_id: str
    claim_id: str
    evidence_id: str
    relay_status: str
    relay_store_path: str
    mission_store_path: str
    connector_id: str
    connector_mode: str
    completed: bool
    steps: tuple[LocalProofStep, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "mission_id": self.mission_id,
            "envelope_id": self.envelope_id,
            "claim_id": self.claim_id,
            "evidence_id": self.evidence_id,
            "relay_status": self.relay_status,
            "relay_store_path": self.relay_store_path,
            "mission_store_path": self.mission_store_path,
            "connector_id": self.connector_id,
            "connector_mode": self.connector_mode,
            "completed": self.completed,
            "steps": [step.to_dict() for step in self.steps],
        }


def run_local_proof(
    relay_store_path: str | Path,
    *,
    command: str = DEFAULT_PROOF_COMMAND,
    request_id: str = DEFAULT_PROOF_REQUEST_ID,
    observed_at: str | None = None,
    repo_state_ref: str = DEFAULT_REPO_STATE_REF,
    graph_snapshot_ref: str = DEFAULT_GRAPH_SNAPSHOT_REF,
) -> LocalProofReport:
    """Exercise one complete local mission-to-evidence path with no network calls."""

    timestamp = observed_at or current_timestamp()
    relay_path = Path(relay_store_path)
    mission_store_path = relay_path.parent / "missions"
    steps: list[LocalProofStep] = []

    mission = _create_and_store_mission(
        command=command,
        request_id=request_id,
        observed_at=timestamp,
        repo_state_ref=repo_state_ref,
        mission_store_path=mission_store_path,
    )
    steps.append(
        LocalProofStep(
            name="mission_intent",
            summary="Created and reloaded a local dry-run mission envelope.",
            evidence_refs=(f"missions/{mission.mission_id}.json",),
        )
    )

    gate = PermissionGate()
    mission_plan = build_local_plan(mission)
    mission_decisions = gate.evaluate_plan(mission, mission_plan)
    _require_allowed(
        "mission_plan_policy",
        [decision.allowed for decision in mission_decisions],
        [
            f"{decision.action_id}: {decision.reason} {decision.stop_reason or ''}".strip()
            for decision in mission_decisions
            if not decision.allowed
        ],
    )
    steps.append(
        LocalProofStep(
            name="mission_plan_policy",
            summary="Evaluated the deterministic local plan through the A1 policy gate.",
        )
    )

    registry = ConnectorRegistry()
    registry_report = registry.validate()
    if not registry_report.valid:
        reasons = list(registry_report.reasons)
        for profile_report in registry_report.profile_reports:
            reasons.extend(profile_report.reasons)
        raise LocalProofError("connector_registry_validation", reasons)

    connector_decision = registry.evaluate(
        ConnectorOperationRequest(
            request_id=mission.request_id,
            connector_id=LOCAL_PROOF_CONNECTOR_ID,
            capability="local-validation",
            data_classification="synthetic",
            dry_run=True,
        )
    )
    _require_allowed("connector_registry_dry_run", (connector_decision.allowed,), (connector_decision.reason,))
    steps.append(
        LocalProofStep(
            name="connector_registry_dry_run",
            summary="Validated the local-device connector profile as dry-run local validation only.",
        )
    )

    observed_state_refs = _observed_state_refs(
        mission=mission,
        repo_state_ref=repo_state_ref,
        graph_snapshot_ref=graph_snapshot_ref,
    )
    relay_context = RelayValidationContext(
        approved_device_ids=(PHONE_DEVICE_ID, WORKER_DEVICE_ID),
        known_request_ids=(mission.request_id,),
        known_mission_ids=(mission.mission_id,),
        current_state_refs=observed_state_refs,
        known_graph_snapshot_refs=(graph_snapshot_ref,),
        validated_at=timestamp,
    )
    envelope = _build_approval_envelope(
        mission=mission,
        observed_at=timestamp,
        observed_state_refs=observed_state_refs,
        graph_snapshot_ref=graph_snapshot_ref,
    )
    envelope_report = validate_relay_envelope(envelope, context=relay_context)
    if not envelope_report.valid or envelope_report.mission_action is None:
        raise LocalProofError("relay_envelope_validation", envelope_report.reasons)

    envelope_decision = gate.evaluate(mission, envelope_report.mission_action)
    _require_allowed("relay_envelope_policy", (envelope_decision.allowed,), (envelope_decision.reason,))
    relay_store = LocalRelayRecordStore(relay_path, context=relay_context)
    add_report = relay_store.add_envelope(envelope, observed_at=timestamp, context=relay_context)
    _require_allowed("relay_record_persistence", (add_report.accepted,), add_report.reasons)
    steps.append(
        LocalProofStep(
            name="relay_record_persistence",
            summary="Validated and persisted a local-file relay approval record.",
            evidence_refs=("packages/uaos-core/src/gail_ai_operating_system/relay_store.py",),
        )
    )

    claim = _build_worker_claim(
        mission=mission,
        envelope=envelope,
        observed_at=timestamp,
        observed_state_refs=observed_state_refs,
    )
    claim_decision = gate.evaluate(mission, claim.to_mission_action())
    _require_allowed("worker_claim_policy", (claim_decision.allowed,), (claim_decision.reason,))
    claim_report = relay_store.claim_worker(claim, context=relay_context)
    _require_allowed("trusted_worker_claim", (claim_report.accepted,), claim_report.reasons)
    steps.append(
        LocalProofStep(
            name="trusted_worker_claim",
            summary="Accepted exactly one trusted Linux worker claim for the mission.",
        )
    )

    evidence = _build_evidence_record(
        mission=mission,
        envelope=envelope,
        claim=claim,
        observed_at=timestamp,
        observed_state_refs=observed_state_refs,
    )
    evidence_report = relay_store.add_evidence(evidence, context=relay_context)
    _require_allowed("validated_evidence_record", (evidence_report.accepted,), evidence_report.reasons)
    completed_report = relay_store.update_status(
        envelope.envelope_id,
        "completed",
        changed_at=timestamp,
        reason="local proof runner reached validated evidence",
        observed_state_refs=observed_state_refs,
        context=relay_context,
    )
    _require_allowed("relay_completion_status", (completed_report.accepted,), completed_report.reasons)
    steps.append(
        LocalProofStep(
            name="validated_evidence_record",
            summary="Attached reference-only evidence and marked the relay proof completed.",
            evidence_refs=evidence.evidence_refs,
        )
    )

    record = relay_store.get_record(envelope.envelope_id)
    if record is None:
        raise LocalProofError("relay_record_reload", ("completed relay record was not found",))

    return LocalProofReport(
        request_id=mission.request_id,
        mission_id=mission.mission_id,
        envelope_id=envelope.envelope_id,
        claim_id=claim.claim_id,
        evidence_id=evidence.evidence_id,
        relay_status=record.status,
        relay_store_path=str(relay_path),
        mission_store_path=str(mission_store_path),
        connector_id=connector_decision.connector_id,
        connector_mode=connector_decision.mode,
        completed=record.status == "completed" and bool(record.evidence_records),
        steps=tuple(steps),
    )


def _create_and_store_mission(
    *,
    command: str,
    request_id: str,
    observed_at: str,
    repo_state_ref: str,
    mission_store_path: Path,
) -> MissionEnvelope:
    mission = create_mission(
        command,
        domain="validation",
        request_id=request_id,
        requested_tools=("local_repo", "local_validation", "policy_gate"),
        data_classification="synthetic",
        created_at=observed_at,
        source_commit=repo_state_ref,
    )
    store = LocalMissionStore(mission_store_path)
    store.save(mission)
    return store.load(mission.mission_id)


def _observed_state_refs(
    *,
    mission: MissionEnvelope,
    repo_state_ref: str,
    graph_snapshot_ref: str,
) -> dict[str, str]:
    return {
        "repo_commit": repo_state_ref,
        "request": mission.request_id,
        "mission": mission.mission_id,
        "graph_snapshot": graph_snapshot_ref,
    }


def _build_approval_envelope(
    *,
    mission: MissionEnvelope,
    observed_at: str,
    observed_state_refs: Mapping[str, str],
    graph_snapshot_ref: str,
) -> RelayEnvelope:
    proof_id = mission.mission_id.removeprefix("mission-")
    return RelayEnvelope(
        schema_version=SCHEMA_VERSION,
        envelope_id=f"relay-proof-{proof_id}",
        record_type="approval",
        project_id=PROJECT_ID,
        request_id=mission.request_id,
        mission_id=mission.mission_id,
        actor_id="adam",
        device_id=PHONE_DEVICE_ID,
        device_role="android_phone_cockpit",
        approval_level="A2",
        requested_capability="approval",
        connector_profile_ids=("github-rev2-private-source", "graphify-enhanced-handoff", LOCAL_PROOF_CONNECTOR_ID),
        stop_triggers=RELAY_STOP_TRIGGERS,
        observed_state_refs=dict(observed_state_refs),
        safe_summary={
            "intent": "Approve the local no-network proof runner.",
            "mission_ref": mission.mission_id,
            "source_refs": ["docs/current-build-pathway.md"],
        },
        evidence_refs=("docs/current-build-pathway.md", "docs/source-of-truth-map.md"),
        relay_status="approved",
        relay_transport="local-file",
        worker_connection_mode="not-started",
        graph_registry_id="graphify-enhanced-handoff",
        graph_snapshot_ref=graph_snapshot_ref,
        graph_observed_at=observed_at,
        filesystem_scope_refs=("packages/uaos-core/src/gail_ai_operating_system/local_proof_runner.py",),
        graphify_handoff_candidate_status="read-only-candidate",
    )


def _build_worker_claim(
    *,
    mission: MissionEnvelope,
    envelope: RelayEnvelope,
    observed_at: str,
    observed_state_refs: Mapping[str, str],
) -> RelayWorkerClaim:
    proof_id = mission.mission_id.removeprefix("mission-")
    return RelayWorkerClaim(
        claim_id=f"claim-proof-{proof_id}",
        envelope_id=envelope.envelope_id,
        mission_id=mission.mission_id,
        worker_device_id=WORKER_DEVICE_ID,
        worker_role="linux_trusted_worker",
        observed_state_refs=dict(observed_state_refs),
        connector_profile_ids=(LOCAL_PROOF_CONNECTOR_ID,),
        claimed_at=observed_at,
        requested_capability="local-validation",
        evidence_refs=("docs/current-build-pathway.md",),
    )


def _build_evidence_record(
    *,
    mission: MissionEnvelope,
    envelope: RelayEnvelope,
    claim: RelayWorkerClaim,
    observed_at: str,
    observed_state_refs: Mapping[str, str],
) -> RelayEvidenceRecord:
    proof_id = mission.mission_id.removeprefix("mission-")
    return RelayEvidenceRecord(
        evidence_id=f"evidence-proof-{proof_id}",
        envelope_id=envelope.envelope_id,
        mission_id=mission.mission_id,
        recorder_device_id=claim.worker_device_id,
        recorder_role=claim.worker_role,
        recorded_at=observed_at,
        safe_summary={
            "result": "Local proof runner moved intent to validated evidence.",
            "checks": [
                "mission validation",
                "policy gate dry-run",
                "connector registry dry-run",
                "relay envelope validation",
                "trusted worker claim",
                "reference-only evidence",
            ],
        },
        evidence_refs=(
            "packages/uaos-core/src/gail_ai_operating_system/local_proof_runner.py",
            "tests/test_local_proof_runner.py",
        ),
        observed_state_refs=dict(observed_state_refs),
    )


def _require_allowed(step: str, flags: Iterable[bool], reasons: Iterable[str]) -> None:
    if not all(flags):
        raise LocalProofError(step, reasons)
