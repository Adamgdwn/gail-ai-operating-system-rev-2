"""Tests for local Graphify acceleration preview generation."""

from __future__ import annotations

from contextlib import redirect_stdout
from dataclasses import replace
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "packages" / "uaos-core" / "src"
sys.path.insert(0, str(SRC))

from gail_ai_operating_system.graphify_acceleration import (  # noqa: E402
    GRAPHIFY_ACCELERATION_SCHEMA_VERSION,
    GraphifyAccelerationValidationError,
    validate_graphify_acceleration_record,
)
from gail_ai_operating_system.graphify_acceleration_preview import (  # noqa: E402
    DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR,
    DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME,
    GraphifyAccelerationPreviewError,
    build_graphify_acceleration_preview_records,
    build_graphify_acceleration_preview_diff,
    compare_graphify_acceleration_preview_records,
    load_graphify_acceleration_preview_records,
    main,
    render_graphify_acceleration_preview_diff_json,
    render_graphify_acceleration_preview_jsonl,
    resolve_graphify_acceleration_preview_path,
    write_graphify_acceleration_preview,
)


class GraphifyAccelerationPreviewTests(unittest.TestCase):
    def test_preview_records_are_valid_deterministic_and_ordered(self) -> None:
        first = build_graphify_acceleration_preview_records()
        second = build_graphify_acceleration_preview_records()

        self.assertEqual(first, second)
        self.assertEqual(
            [record.entity_type for record in first],
            ["authority_envelope", "action", "evidence_packet"],
        )

        rendered = render_graphify_acceleration_preview_jsonl(first)
        rendered_again = render_graphify_acceleration_preview_jsonl(second)
        self.assertEqual(rendered, rendered_again)

        lines = rendered.strip().splitlines()
        self.assertEqual(len(lines), 3)
        for line, record in zip(lines, first):
            with self.subTest(record=record.record_id):
                payload = json.loads(line)
                self.assertEqual(payload["schema_version"], GRAPHIFY_ACCELERATION_SCHEMA_VERSION)
                self.assertTrue(payload["fingerprint"].startswith("sha256-"))
                self.assertFalse(payload["contains_raw_payload"])
                self.assertEqual(validate_graphify_acceleration_record(record), [])

    def test_writes_default_preview_under_ignored_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            result = write_graphify_acceleration_preview(repo_root=temp_root)

            expected_path = (
                Path(temp_root)
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME
            )
            self.assertEqual(Path(result.output_path or ""), expected_path)
            self.assertTrue(expected_path.exists())
            self.assertEqual(expected_path.read_text(encoding="utf-8"), result.content)
            self.assertEqual(result.record_count, 3)

    def test_print_only_does_not_write_preview_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            result = write_graphify_acceleration_preview(
                repo_root=temp_root,
                print_only=True,
            )

            expected_path = (
                Path(temp_root)
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME
            )
            self.assertIsNone(result.output_path)
            self.assertFalse(expected_path.exists())
            self.assertIn("graphify-fact-action-graphify-preview-001", result.content)

    def test_resolves_explicit_file_and_directory_inside_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            direct_file = resolve_graphify_acceleration_preview_path(
                "tmp/graphify-acceleration-preview/custom-preview.jsonl",
                repo_root=temp_root,
            )
            directory_default = resolve_graphify_acceleration_preview_path(
                "tmp/graphify-acceleration-preview",
                repo_root=temp_root,
            )

            self.assertEqual(
                direct_file,
                Path(temp_root) / "tmp" / "graphify-acceleration-preview" / "custom-preview.jsonl",
            )
            self.assertEqual(
                directory_default,
                (
                    Path(temp_root)
                    / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR
                    / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME
                ),
            )

    def test_rejects_output_paths_outside_preview_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            unsafe_paths = (
                "tmp/other-preview.jsonl",
                "../graphify-acceleration-preview.jsonl",
                str(Path(temp_root).parent / "outside-preview.jsonl"),
            )

            for unsafe_path in unsafe_paths:
                with self.subTest(path=unsafe_path):
                    with self.assertRaises(GraphifyAccelerationPreviewError):
                        resolve_graphify_acceleration_preview_path(unsafe_path, repo_root=temp_root)

    def test_rejects_nested_sensitive_or_wrong_suffix_preview_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            unsafe_paths = (
                "tmp/graphify-acceleration-preview/nested/preview.jsonl",
                "tmp/graphify-acceleration-preview/.env-preview.jsonl",
                "tmp/graphify-acceleration-preview/preview.log",
            )

            for unsafe_path in unsafe_paths:
                with self.subTest(path=unsafe_path):
                    with self.assertRaises(GraphifyAccelerationPreviewError):
                        resolve_graphify_acceleration_preview_path(unsafe_path, repo_root=temp_root)

    def test_invalid_record_is_rejected_before_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            output = (
                Path(temp_root)
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME
            )
            invalid_record = replace(
                build_graphify_acceleration_preview_records()[0],
                fingerprint="",
            )

            with self.assertRaises(GraphifyAccelerationValidationError):
                write_graphify_acceleration_preview(
                    repo_root=temp_root,
                    records=(invalid_record,),
                )

            self.assertFalse(output.exists())

    def test_cli_print_only_outputs_jsonl_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            stdout = io.StringIO()

            with redirect_stdout(stdout):
                exit_code = main(["--repo-root", temp_root, "--print"])

            expected_path = (
                Path(temp_root)
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME
            )
            self.assertEqual(exit_code, 0)
            self.assertFalse(expected_path.exists())
            lines = stdout.getvalue().strip().splitlines()
            self.assertEqual(len(lines), 3)
            self.assertEqual(json.loads(lines[0])["entity_type"], "authority_envelope")

    def test_diff_against_missing_or_empty_cache_reports_all_added(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            missing_diff = build_graphify_acceleration_preview_diff(repo_root=temp_root)

            self.assertEqual(missing_diff.cache_status, "missing")
            self.assertEqual(len(missing_diff.added), 3)
            self.assertEqual(len(missing_diff.changed), 0)
            self.assertEqual(len(missing_diff.unchanged), 0)
            self.assertEqual(len(missing_diff.removed), 0)
            self.assertFalse(missing_diff.to_dict()["mutates_source"])
            self.assertFalse(missing_diff.to_dict()["mutates_graphify"])

            empty_path = (
                Path(temp_root)
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME
            )
            empty_path.parent.mkdir(parents=True, exist_ok=True)
            empty_path.write_text("", encoding="utf-8")

            empty_diff = build_graphify_acceleration_preview_diff(repo_root=temp_root)

            self.assertEqual(empty_diff.cache_status, "empty")
            self.assertEqual(len(empty_diff.added), 3)

    def test_diff_reports_added_changed_unchanged_and_removed_facts(self) -> None:
        previous = build_graphify_acceleration_preview_records()
        unchanged = previous[0]
        changed = replace(previous[1], fingerprint="sha256-changed-action")
        added = replace(
            previous[2],
            record_id="graphify-fact-evidence-graphify-preview-002",
            entity_id="evidence-graphify-preview-002",
            fingerprint="sha256-added-evidence",
        )

        diff = compare_graphify_acceleration_preview_records(
            previous,
            (unchanged, changed, added),
            previous_source="inline-test",
            cache_status="loaded",
        )
        rendered = json.loads(render_graphify_acceleration_preview_diff_json(diff))

        self.assertEqual(rendered["counts"], {
            "added": 1,
            "changed": 1,
            "unchanged": 1,
            "removed": 1,
        })
        self.assertEqual([entry.fact_id for entry in diff.unchanged], [unchanged.record_id])
        self.assertEqual([entry.fact_id for entry in diff.changed], [changed.record_id])
        self.assertEqual([entry.fact_id for entry in diff.added], [added.record_id])
        self.assertEqual([entry.fact_id for entry in diff.removed], [previous[2].record_id])
        self.assertEqual(diff.removed[0].current_fingerprint, None)
        self.assertEqual(rendered["authority_effect"], "none")

    def test_load_preview_records_rejects_invalid_previous_output_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            preview_path = (
                Path(temp_root)
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME
            )
            preview_path.parent.mkdir(parents=True, exist_ok=True)
            preview_path.write_text("{bad-json\n", encoding="utf-8")

            with self.assertRaisesRegex(GraphifyAccelerationPreviewError, "line 1"):
                load_graphify_acceleration_preview_records(repo_root=temp_root)

            invalid_record = build_graphify_acceleration_preview_records()[0].to_dict()
            invalid_record["fingerprint"] = ""
            preview_path.write_text(json.dumps(invalid_record) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(GraphifyAccelerationPreviewError, "Invalid previous"):
                build_graphify_acceleration_preview_diff(repo_root=temp_root)

    def test_diff_rejects_duplicate_fact_ids(self) -> None:
        records = build_graphify_acceleration_preview_records()

        with self.assertRaisesRegex(GraphifyAccelerationPreviewError, "duplicate fact ID"):
            compare_graphify_acceleration_preview_records((records[0], records[0]), records)

        with self.assertRaisesRegex(GraphifyAccelerationPreviewError, "duplicate fact ID"):
            compare_graphify_acceleration_preview_records(records, (records[0], records[0]))

    def test_cli_diff_outputs_safe_summary_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_root:
            stdout = io.StringIO()

            with redirect_stdout(stdout):
                exit_code = main(["--repo-root", temp_root, "--diff"])

            expected_path = (
                Path(temp_root)
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_DIR
                / DEFAULT_GRAPHIFY_ACCELERATION_PREVIEW_FILENAME
            )
            payload = json.loads(stdout.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertFalse(expected_path.exists())
            self.assertEqual(payload["mode"], "local-preview-diff")
            self.assertEqual(payload["cache_status"], "missing")
            self.assertEqual(payload["counts"]["added"], 3)
            self.assertEqual(payload["mutates_graphify"], False)
            self.assertNotIn("summary", json.dumps(payload))


if __name__ == "__main__":
    unittest.main()
