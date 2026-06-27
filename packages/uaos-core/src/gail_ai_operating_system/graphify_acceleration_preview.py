"""Local preview command for Graphify acceleration facts.

The preview is an ignored developer artifact that shows what a future Graphify
ingest boundary might receive. It uses synthetic local records only, validates
every acceleration fact before write, and never calls Graphify or live systems.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sys
from typing import Iterable, Sequence

from .action import Action
from .authority_envelope import AuthorityEnvelope
from .evidence_packet import EvidencePacket
from .graphify_acceleration import (
    GRAPHIFY_ACCELERATION_SCHEMA_VERSION,
    GraphifyAccelerationRecord,
    GraphifyAccelerationValidationError,
    build_graphify_action_record,
    build_graphify_authority_envelope_record,
    build_graphify_evidence_record,
    classify_graphify_reference,
)
from .mission import MissionStatus


DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR = Path("tmp") / "graphify-acceleration-preview"
DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME = "graphify-acceleration-preview.jsonl"
DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_GENERATED_AT = "2026-06-27T17:35:37-06:00"
GRAPHIFY_ACCELERATION_PREVIEW_ENCODING = "utf-8"

_PREVIEW_ENTITY_ORDER = {
    "authority_envelope": 0,
    "action": 1,
    "evidence_packet": 2,
    "mission": 3,
    "connector": 4,
    "system": 5,
}


class GraphifyAccelerationPreviewError(ValueError):
    """Raised when local preview generation would cross the approved boundary."""


@dataclass(frozen=True)
class GraphifyAccelerationPreviewResult:
    """Result of a local Graphify acceleration preview render or write."""

    output_path: str | None
    preview_directory: str
    record_count: int
    schema_version: str
    content: str


def build_graphify_acceleration_preview_records(
    *,
    generated_at: str = DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_GENERATED_AT,
) -> tuple[GraphifyAccelerationRecord, ...]:
    """Build deterministic synthetic records for operator preview.

    These records deliberately model the CNS lane without touching live Graphify,
    AG Operations, M365, QuickBooks, finance, billing, client, log, audio,
    secret, or connector runtime data.
    """

    mission_id = "mission-graphify-preview-001"
    envelope_id = "env-graphify-preview-001"
    action_id = "action-graphify-preview-001"

    envelope = AuthorityEnvelope(
        envelope_id=envelope_id,
        mission_id=mission_id,
        authority_level="R2",
        autonomy_level="A1",
        domain="graphify_acceleration_preview",
        granted_by="Adam Goodwin",
        granted_at=generated_at,
        expires_at=None,
        allowed_action_types=("graphify_acceleration_preview",),
        max_risk_tier=2,
        stop_conditions=(
            "Stop before Graphify runtime access",
            "Stop before live business-system reads",
            "Stop before execution authority",
        ),
        rollback_path="Delete ignored local preview output and rerun from source fixtures.",
        review_cadence="Per local preview generation",
        status="active",
    )
    action = Action(
        action_id=action_id,
        mission_id=mission_id,
        action_type="graphify_acceleration_preview",
        title="Generate local Graphify acceleration preview",
        actor="GAIL AI Operating System Rev 2",
        status=MissionStatus.PROPOSED,
        authority_level="R2",
        risk_tier=2,
        arguments={"preview_mode": "synthetic-local-jsonl"},
        created_at=generated_at,
        claimed_at=None,
        executed_at=None,
        envelope_id=envelope_id,
    )
    packet = EvidencePacket(
        evidence_id="evidence-graphify-preview-001",
        mission_id=mission_id,
        action_id=action_id,
        actor="GAIL AI Operating System Rev 2",
        action_type="graphify_acceleration_preview",
        authority_basis="A1 local synthetic preview",
        result="success",
        execution_mode="dry-run",
        created_at=generated_at,
        envelope_id=envelope_id,
        rollback_note="Delete ignored preview output under tmp/graphify-acceleration-preview/.",
        outcome_summary="Synthetic preview facts validated without external system access.",
    )

    records = (
        build_graphify_authority_envelope_record(
            envelope,
            generated_at=generated_at,
            source_refs=("packages/uaos-core/src/gail_ai_operating_system/authority_envelope.py",),
            data_classification="synthetic",
        ),
        build_graphify_action_record(
            action,
            generated_at=generated_at,
            source_refs=("packages/uaos-core/src/gail_ai_operating_system/action.py",),
            data_classification="synthetic",
        ),
        build_graphify_evidence_record(
            packet,
            generated_at=generated_at,
            source_refs=("packages/uaos-core/src/gail_ai_operating_system/evidence_packet.py",),
            evidence_refs=("records/evidence/evidence-graphify-preview-001",),
            authority_level="R2",
            risk_tier=2,
            data_classification="synthetic",
        ),
    )
    return _ordered_records(records)


def render_graphify_acceleration_preview_jsonl(
    records: Iterable[GraphifyAccelerationRecord],
) -> str:
    """Render validated records as deterministic JSONL."""

    ordered = _ordered_records(records)
    for record in ordered:
        record.require_valid()
    return "".join(
        json.dumps(record.to_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
        for record in ordered
    )


def resolve_graphify_acceleration_preview_path(
    output_path: str | Path | None = None,
    *,
    repo_root: str | Path | None = None,
) -> Path:
    """Resolve an output file inside the approved ignored preview directory."""

    root = Path(repo_root or Path.cwd()).resolve()
    preview_dir = (root / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR).resolve()

    if output_path is None:
        candidate = preview_dir / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME
    else:
        raw_output = Path(output_path)
        if ".." in raw_output.parts:
            raise GraphifyAccelerationPreviewError(
                "Preview output path must not use parent traversal."
            )
        candidate = raw_output if raw_output.is_absolute() else root / raw_output
        candidate = candidate.resolve()
        if candidate == preview_dir:
            candidate = candidate / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME

    try:
        relative_to_preview = candidate.relative_to(preview_dir)
    except ValueError as exc:
        raise GraphifyAccelerationPreviewError(
            "Preview output must stay under tmp/graphify-acceleration-preview/."
        ) from exc

    if len(relative_to_preview.parts) != 1:
        raise GraphifyAccelerationPreviewError(
            "Preview output must be a direct file inside tmp/graphify-acceleration-preview/."
        )
    if candidate.suffix != ".jsonl":
        raise GraphifyAccelerationPreviewError("Preview output must use the .jsonl suffix.")

    relative_to_root = candidate.relative_to(root).as_posix()
    path_check = classify_graphify_reference(relative_to_root, field_name="preview_output_path")
    if not path_check.accepted:
        raise GraphifyAccelerationPreviewError("; ".join(path_check.reasons))

    return candidate


def write_graphify_acceleration_preview(
    *,
    output_path: str | Path | None = None,
    repo_root: str | Path | None = None,
    records: Iterable[GraphifyAccelerationRecord] | None = None,
    print_only: bool = False,
) -> GraphifyAccelerationPreviewResult:
    """Write or render the local ignored Graphify acceleration preview."""

    preview_records = tuple(records) if records is not None else build_graphify_acceleration_preview_records()
    content = render_graphify_acceleration_preview_jsonl(preview_records)

    root = Path(repo_root or Path.cwd()).resolve()
    preview_dir = (root / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR).resolve()

    if print_only:
        return GraphifyAccelerationPreviewResult(
            output_path=None,
            preview_directory=str(preview_dir),
            record_count=len(_ordered_records(preview_records)),
            schema_version=GRAPHIFY_ACCELERATION_SCHEMA_VERSION,
            content=content,
        )

    target = resolve_graphify_acceleration_preview_path(output_path, repo_root=root)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding=GRAPHIFY_ACCELERATION_PREVIEW_ENCODING, newline="\n")
    return GraphifyAccelerationPreviewResult(
        output_path=str(target),
        preview_directory=str(preview_dir),
        record_count=len(_ordered_records(preview_records)),
        schema_version=GRAPHIFY_ACCELERATION_SCHEMA_VERSION,
        content=content,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for local preview generation."""

    parser = argparse.ArgumentParser(
        description="Generate a local JSONL preview of synthetic Graphify acceleration facts."
    )
    parser.add_argument(
        "--output",
        help=(
            "Output .jsonl file. Defaults to "
            "tmp/graphify-acceleration-preview/graphify-acceleration-preview.jsonl."
        ),
    )
    parser.add_argument(
        "--print",
        action="store_true",
        dest="print_only",
        help="Print the deterministic JSONL preview instead of writing a file.",
    )
    parser.add_argument(
        "--repo-root",
        help="Repository root used for output boundary checks. Defaults to the current directory.",
    )
    args = parser.parse_args(argv)

    try:
        result = write_graphify_acceleration_preview(
            output_path=args.output,
            repo_root=args.repo_root,
            print_only=args.print_only,
        )
    except (GraphifyAccelerationPreviewError, GraphifyAccelerationValidationError, ValueError) as exc:
        print(f"Graphify acceleration preview failed: {exc}", file=sys.stderr)
        return 2

    if args.print_only:
        sys.stdout.write(result.content)
    else:
        print(f"Wrote {result.record_count} Graphify acceleration preview records to {result.output_path}")
    return 0


def _ordered_records(
    records: Iterable[GraphifyAccelerationRecord],
) -> tuple[GraphifyAccelerationRecord, ...]:
    return tuple(
        sorted(
            records,
            key=lambda record: (
                _PREVIEW_ENTITY_ORDER.get(record.entity_type, 99),
                record.entity_id,
                record.record_id,
            ),
        )
    )


__all__ = [
    "DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR",
    "DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME",
    "DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_GENERATED_AT",
    "GRAPHIFY_ACCELERATION_PREVIEW_ENCODING",
    "GraphifyAccelerationPreviewError",
    "GraphifyAccelerationPreviewResult",
    "build_graphify_acceleration_preview_records",
    "main",
    "render_graphify_acceleration_preview_jsonl",
    "resolve_graphify_acceleration_preview_path",
    "write_graphify_acceleration_preview",
]


if __name__ == "__main__":
    raise SystemExit(main())
