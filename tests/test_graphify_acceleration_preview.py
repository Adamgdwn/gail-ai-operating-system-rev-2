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
    main,
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


if __name__ == "__main__":
    unittest.main()
