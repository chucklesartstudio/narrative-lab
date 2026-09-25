from __future__ import annotations

import json
import hashlib
from collections import Counter
from pathlib import Path
from typing import Any, Optional

from ..parsers.screenplay import parse_source
from ..schemas.screenplay import BoundaryStatus, ParseResult, SourceSpan


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATASET_DIR = PROJECT_ROOT / "data" / "evaluation" / "screenplay_alignment"
BLOCK_TYPES = (
    "scene_heading",
    "action",
    "character",
    "dialogue",
    "parenthetical",
    "transition",
    "blank",
)


def _ratio(numerator: int, denominator: int) -> Optional[float]:
    if denominator == 0:
        return None
    return numerator / denominator


def _line_texts(text: str) -> list[str]:
    return text.splitlines()


def _line_start_offsets(text: str) -> list[int]:
    starts = [0]
    index = 0
    while index < len(text):
        if text[index] == "\r":
            index += 1
            if index < len(text) and text[index] == "\n":
                index += 1
            starts.append(index)
        elif text[index] == "\n":
            index += 1
            starts.append(index)
        else:
            index += 1
    return starts


def _evaluate_block_labels(
    expected: list[str],
    parse_result: ParseResult,
) -> dict[str, Any]:
    predicted_by_line = {block.start_line: block.block_type for block in parse_result.blocks}
    per_type: dict[str, dict[str, Any]] = {}

    for block_type in BLOCK_TYPES:
        true_positive = 0
        false_positive = 0
        false_negative = 0
        for line_number, expected_type in enumerate(expected, start=1):
            predicted_type = predicted_by_line.get(line_number)
            if expected_type == block_type and predicted_type == block_type:
                true_positive += 1
            elif expected_type == block_type and predicted_type != block_type:
                false_negative += 1
            elif expected_type != block_type and predicted_type == block_type:
                false_positive += 1
        for line_number, predicted_type in predicted_by_line.items():
            if line_number > len(expected) and predicted_type == block_type:
                false_positive += 1

        per_type[block_type] = {
            "true_positive": true_positive,
            "false_positive": false_positive,
            "false_negative": false_negative,
            "precision": _ratio(true_positive, true_positive + false_positive),
            "recall": _ratio(true_positive, true_positive + false_negative),
        }

    correct = sum(
        predicted_by_line.get(line_number) == expected_type
        for line_number, expected_type in enumerate(expected, start=1)
    )
    expected_count = len(expected)
    predicted_count = len(parse_result.blocks)
    return {
        "per_type": per_type,
        "micro_precision": _ratio(correct, predicted_count),
        "micro_recall": _ratio(correct, expected_count),
        "exact_line_accuracy": _ratio(correct, max(expected_count, predicted_count)),
        "expected_blocks": expected_count,
        "predicted_blocks": predicted_count,
    }


def _span_round_trip_count(parse_result: ParseResult) -> tuple[int, int]:
    source_text = parse_result.source.original_text
    if source_text is None:
        return 0, 0

    succeeded = 0
    checked = 0
    blocks_by_id = {block.block_id: block for block in parse_result.blocks}

    for block in parse_result.blocks:
        checked += 1
        if source_text[block.source_start_offset : block.source_end_offset] == block.original_text:
            succeeded += 1

    for scene in parse_result.scenes:
        checked += 1
        if source_text[scene.scene_span.start_offset : scene.scene_span.end_offset] == scene.original_text:
            succeeded += 1

        checked += 1
        heading = blocks_by_id.get(scene.heading_block_id)
        if (
            heading is not None
            and source_text[
                scene.scene_start_span.start_offset : scene.scene_start_span.end_offset
            ]
            == heading.original_text
        ):
            succeeded += 1

        checked += 1
        if (
            source_text[scene.scene_end_span.start_offset : scene.scene_end_span.end_offset]
            == ""
        ):
            succeeded += 1

    for boundary in parse_result.boundary_candidates:
        if boundary.source_span is None:
            continue
        checked += 1
        if (
            source_text[boundary.source_span.start_offset : boundary.source_span.end_offset]
            == boundary.observed_text
        ):
            succeeded += 1

    if parse_result.pre_scene_span is not None:
        checked += 1
        span = parse_result.pre_scene_span
        confirmed_starts = [
            boundary.source_span.start_offset
            for boundary in parse_result.boundary_candidates
            if boundary.boundary_status == BoundaryStatus.CONFIRMED
            and boundary.source_span is not None
        ]
        expected_end = min(confirmed_starts) if confirmed_starts else len(source_text)
        if span.start_offset == 0 and span.end_offset == expected_end:
            succeeded += 1

    return succeeded, checked


def _evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    fixture_path = DATASET_DIR / case["fixture"]
    raw_bytes = fixture_path.read_bytes()
    original_text = raw_bytes.decode("utf-8")
    result = parse_source(fixture_path, work_id="evaluation-{}".format(case["case_id"]))
    block_types = [block.block_type for block in result.blocks]
    expected_types = case["expected_block_types"]
    type_match = block_types == expected_types

    actual_confirmed_lines = sorted(
        candidate.source_span.start_line
        for candidate in result.boundary_candidates
        if candidate.boundary_status == BoundaryStatus.CONFIRMED
        and candidate.source_span is not None
    )
    boundary_candidates = sorted(
        (
            candidate.source_span.start_line,
            candidate.boundary_status.value,
        )
        for candidate in result.boundary_candidates
        if candidate.boundary_status
        in {BoundaryStatus.CANDIDATE, BoundaryStatus.UNCERTAIN}
        and candidate.source_span is not None
    )
    expected_candidate_boundaries = sorted(
        (item["line"], item["status"]) for item in case["candidate_boundaries"]
    )
    actual_diagnostics = sorted({diagnostic.code for diagnostic in result.diagnostics})
    expected_diagnostics = sorted(case["expected_diagnostics"])
    diagnostic_match = expected_diagnostics == actual_diagnostics

    source_lines = _line_texts(original_text)
    block_by_line = {block.start_line: block for block in result.blocks}
    relevant_spans_match = True
    for expected_span in case.get("relevant_source_spans", []):
        line_number = expected_span["line"]
        expected_span_text = expected_span["text"]
        block = block_by_line.get(line_number)
        relevant_spans_match = relevant_spans_match and (
            line_number <= len(source_lines)
            and source_lines[line_number - 1] == expected_span_text
            and block is not None
            and block.original_text == expected_span_text
            and original_text[block.source_start_offset : block.source_end_offset]
            == expected_span_text
        )

    normalized_cues_match = True
    for line_text, expected_cue in case.get("normalized_cues", {}).items():
        block = block_by_line.get(int(line_text))
        normalized_cues_match = normalized_cues_match and (
            block is not None and block.normalized_cue == expected_cue
        )

    round_trip_succeeded, round_trip_checked = _span_round_trip_count(result)
    human_review_required = any(diagnostic.review_required for diagnostic in result.diagnostics)
    human_review_required = human_review_required or any(
        item.boundary_status in {BoundaryStatus.CANDIDATE, BoundaryStatus.UNCERTAIN}
        for item in result.boundary_candidates
    )

    confirmed_starts = [
        boundary.source_span.start_offset
        for boundary in result.boundary_candidates
        if boundary.boundary_status == BoundaryStatus.CONFIRMED
        and boundary.source_span is not None
    ]
    pre_scene_expected_end = min(confirmed_starts) if confirmed_starts else len(original_text)
    pre_scene_span_consistent = (
        result.pre_scene_span is None
        and pre_scene_expected_end == 0
    ) or (
        result.pre_scene_span is not None
        and result.pre_scene_span.start_offset == 0
        and result.pre_scene_span.end_offset == pre_scene_expected_end
    )
    return {
        "case_id": case["case_id"],
        "fixture": case["fixture"],
        "block_types_match": type_match,
        "block_classification": _evaluate_block_labels(expected_types, result),
        "confirmed_boundary_lines_expected": case["confirmed_heading_lines"],
        "confirmed_boundary_lines_actual": actual_confirmed_lines,
        "confirmed_boundaries_match": actual_confirmed_lines
        == case["confirmed_heading_lines"],
        "candidate_boundaries_expected": expected_candidate_boundaries,
        "candidate_boundaries_actual": boundary_candidates,
        "candidate_boundaries_match": boundary_candidates
        == expected_candidate_boundaries,
        "scene_count_expected": case["scene_count"],
        "scene_count_actual": len(result.scenes),
        "scene_count_match": len(result.scenes) == case["scene_count"],
        "pre_scene_expected": case["has_pre_scene_material"],
        "pre_scene_actual": result.pre_scene_span is not None
        and bool(
            original_text[
                result.pre_scene_span.start_offset : result.pre_scene_span.end_offset
            ].strip()
        ),
        "pre_scene_span_consistent": pre_scene_span_consistent,
        "relevant_source_spans_match": relevant_spans_match,
        "normalized_cues_match": normalized_cues_match,
        "newline_style_expected": case.get("newline_style"),
        "newline_style_actual": result.source.newline_characteristics.style,
        "newline_style_match": case.get("newline_style") is None
        or result.source.newline_characteristics.style == case["newline_style"],
        "diagnostics_expected": expected_diagnostics,
        "diagnostics_actual": actual_diagnostics,
        "expected_diagnostics_present": diagnostic_match,
        "source_text_preserved": result.source.original_text == original_text,
        "source_content_hash_match": result.source.content_hash
        == "sha256:{}".format(hashlib.sha256(raw_bytes).hexdigest()),
        "diagnostic_counts": dict(Counter(diagnostic.code for diagnostic in result.diagnostics)),
        "human_review_required": human_review_required,
        "round_trip_succeeded": round_trip_succeeded,
        "round_trip_checked": round_trip_checked,
        "round_trip_rate": _ratio(round_trip_succeeded, round_trip_checked),
        "source_revision_id": result.source.revision_id,
    }


def _identity_stability_check() -> dict[str, Any]:
    text = "INT. ROOM - DAY\nANNA\nHello.\n"
    metadata = {
        "work_id": "identity-check",
        "source_id": "source-identity-check",
        "original_filename": "identity-check.txt",
    }
    first = parse_source(text, **metadata)
    second = parse_source(text, **metadata)
    changed = parse_source(text + "A new line.\n", **metadata)

    first_structures = (
        [block.block_id for block in first.blocks],
        [scene.scene_id for scene in first.scenes],
        [
            (
                block.source_start_offset,
                block.source_end_offset,
                block.start_line,
                block.end_line,
                block.start_column,
                block.end_column,
            )
            for block in first.blocks
        ],
    )
    second_structures = (
        [block.block_id for block in second.blocks],
        [scene.scene_id for scene in second.scenes],
        [
            (
                block.source_start_offset,
                block.source_end_offset,
                block.start_line,
                block.end_line,
                block.start_column,
                block.end_column,
            )
            for block in second.blocks
        ],
    )
    return {
        "same_input_source_id_stable": first.source.source_id == second.source.source_id,
        "same_input_revision_id_stable": first.source.revision_id == second.source.revision_id,
        "same_input_structural_ids_and_locators_stable": first_structures == second_structures,
        "changed_content_keeps_logical_source_id": first.source.source_id == changed.source.source_id,
        "changed_content_changes_revision_id": first.source.revision_id
        != changed.source.revision_id,
    }


def evaluate_dataset() -> dict[str, Any]:
    manifest = json.loads((DATASET_DIR / "cases.json").read_text(encoding="utf-8"))
    cases = [_evaluate_case(case) for case in manifest["cases"]]

    round_trip_success = sum(case["round_trip_succeeded"] for case in cases)
    round_trip_checked = sum(case["round_trip_checked"] for case in cases)
    diagnostic_totals: Counter[str] = Counter()
    for case in cases:
        diagnostic_totals.update(case["diagnostic_counts"])

    total_correct = sum(
        case["block_classification"]["micro_precision"]
        * case["block_classification"]["predicted_blocks"]
        for case in cases
        if case["block_classification"]["micro_precision"] is not None
    )
    expected_total = sum(
        case["block_classification"]["expected_blocks"] for case in cases
    )
    predicted_total = sum(
        case["block_classification"]["predicted_blocks"] for case in cases
    )
    boundary_true_positive = sum(
        len(
            set(case["confirmed_boundary_lines_expected"])
            & set(case["confirmed_boundary_lines_actual"])
        )
        for case in cases
    )
    boundary_false_positive = sum(
        len(
            set(case["confirmed_boundary_lines_actual"])
            - set(case["confirmed_boundary_lines_expected"])
        )
        for case in cases
    )
    boundary_false_negative = sum(
        len(
            set(case["confirmed_boundary_lines_expected"])
            - set(case["confirmed_boundary_lines_actual"])
        )
        for case in cases
    )
    identity = _identity_stability_check()

    return {
        "dataset_id": manifest["dataset_id"],
        "description": manifest["description"],
        "case_count": len(cases),
        "block_classification": {
            "micro_precision": _ratio(round(total_correct), predicted_total),
            "micro_recall": _ratio(round(total_correct), expected_total),
            "expected_blocks": expected_total,
            "predicted_blocks": predicted_total,
        },
        "scene_boundary": {
            "true_positive": boundary_true_positive,
            "false_positive": boundary_false_positive,
            "false_negative": boundary_false_negative,
            "precision": _ratio(boundary_true_positive, boundary_true_positive + boundary_false_positive),
            "recall": _ratio(boundary_true_positive, boundary_true_positive + boundary_false_negative),
            "candidate_status_cases_match": sum(
                case["candidate_boundaries_match"] for case in cases
            ),
            "candidate_status_cases": len(cases),
        },
        "span_round_trip": {
            "succeeded": round_trip_success,
            "checked": round_trip_checked,
            "rate": _ratio(round_trip_success, round_trip_checked),
        },
        "source_revision_identity_stability": identity,
        "diagnostics_by_type": dict(sorted(diagnostic_totals.items())),
        "cases_requiring_human_review": [
            case["case_id"] for case in cases if case["human_review_required"]
        ],
        "all_cases_pass": all(
            case["block_types_match"]
            and case["confirmed_boundaries_match"]
            and case["candidate_boundaries_match"]
            and case["scene_count_match"]
            and case["pre_scene_expected"] == case["pre_scene_actual"]
            and case["pre_scene_span_consistent"]
            and case["relevant_source_spans_match"]
            and case["normalized_cues_match"]
            and case["newline_style_match"]
            and case["expected_diagnostics_present"]
            and case["source_text_preserved"]
            and case["source_content_hash_match"]
            and case["round_trip_succeeded"] == case["round_trip_checked"]
            for case in cases
        ),
        "cases": cases,
    }


def main() -> None:
    print(json.dumps(evaluate_dataset(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
