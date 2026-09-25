from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from backend.app.parsers.screenplay import normalize_character_cue, parse_source
from backend.app.schemas.screenplay import BoundaryStatus, SourceInput


def _assert_span_round_trips(result):
    source_text = result.source.original_text
    assert source_text is not None

    for block in result.blocks:
        assert source_text[block.source_start_offset : block.source_end_offset] == block.original_text

    for scene in result.scenes:
        assert source_text[scene.scene_span.start_offset : scene.scene_span.end_offset] == scene.original_text
        heading = next(block for block in result.blocks if block.block_id == scene.heading_block_id)
        assert source_text[scene.scene_start_span.start_offset : scene.scene_start_span.end_offset] == heading.original_text
        assert scene.scene_end_span.start_offset == scene.scene_end_span.end_offset

    for boundary in result.boundary_candidates:
        if boundary.source_span is not None:
            assert source_text[boundary.source_span.start_offset : boundary.source_span.end_offset] == boundary.observed_text


def test_original_text_hash_revision_and_source_metadata_are_preserved():
    original = "\ufeffINT. CAFÉ - NIGHT\r\n  A door opens.\r\n"
    result = parse_source(
        SourceInput(
            original_text=original,
            work_id="work-1",
            original_filename="draft.txt",
            source_id="source-1",
        )
    )

    assert result.source.original_text == original
    assert result.source.content_hash == "sha256:{}".format(
        hashlib.sha256(original.encode("utf-8")).hexdigest()
    )
    assert result.source.revision_id == "rev_{}".format(
        hashlib.sha256(original.encode("utf-8")).hexdigest()
    )
    assert result.source.source_id == "source-1"
    assert result.source.work_id == "work-1"
    assert result.source.original_filename == "draft.txt"
    assert result.source.newline_characteristics.style == "crlf"
    assert result.source.locator_information.offset_base == 0
    assert result.source.locator_information.interval == "half_open"
    _assert_span_round_trips(result)


def test_revision_and_structural_ids_are_deterministic_for_unchanged_input():
    text = "INT. ROOM - DAY\nMAYA\nHello.\n"
    first = parse_source(text, work_id="work-1", original_filename="script.txt")
    second = parse_source(text, work_id="work-1", original_filename="script.txt")

    assert first.source.source_id == second.source.source_id
    assert first.source.revision_id == second.source.revision_id
    assert [block.block_id for block in first.blocks] == [block.block_id for block in second.blocks]
    assert [scene.scene_id for scene in first.scenes] == [scene.scene_id for scene in second.scenes]


def test_changed_content_creates_a_new_revision_without_mutating_old_result():
    original = "INT. ROOM - DAY\nA door opens.\n"
    first = parse_source(original, source_id="source-1")
    second = parse_source(original + "A light turns on.\n", source_id="source-1")

    assert first.source.source_id == second.source.source_id
    assert first.source.revision_id != second.source.revision_id
    assert first.source.original_text == original
    assert second.source.original_text.endswith("A light turns on.\n")
    assert [block.block_id for block in first.blocks] != [block.block_id for block in second.blocks]


def test_each_block_has_original_text_offsets_and_derived_line_column_locators():
    text = "  INT. ROOM - DAY\r\n\tMAYA\r\n    Hello, café.\r\n"
    result = parse_source(text)

    assert [block.block_type for block in result.blocks] == ["scene_heading", "character", "dialogue"]
    for block in result.blocks:
        assert text[block.source_start_offset : block.source_end_offset] == block.original_text
        assert block.start_line >= 1
        assert block.end_line >= block.start_line
        assert block.start_column >= 1
        assert block.end_column >= 1
    assert result.blocks[0].original_text == "  INT. ROOM - DAY"
    assert result.blocks[1].original_text == "\tMAYA"
    assert result.blocks[2].original_text == "    Hello, café."
    _assert_span_round_trips(result)


def test_scenes_are_constructed_only_from_confirmed_headings_and_align_to_source():
    text = "CARD\n\nINT. ROOM - DAY\nA enters.\n\nEXT. ROAD - NIGHT\nA leaves."
    result = parse_source(text, work_id="work-1", source_id="source-1")

    assert len(result.scenes) == 2
    assert [scene.sequence for scene in result.scenes] == [1, 2]
    assert [scene.original_text for scene in result.scenes] == [
        "INT. ROOM - DAY\nA enters.\n\n",
        "EXT. ROAD - NIGHT\nA leaves.",
    ]
    assert all(scene.source_id == "source-1" for scene in result.scenes)
    assert all(scene.source_revision_id == result.source.revision_id for scene in result.scenes)
    assert all(scene.heading_block_id in scene.contained_block_ids for scene in result.scenes)
    assert result.pre_scene_span is not None
    assert text[result.pre_scene_span.start_offset : result.pre_scene_span.end_offset] == "CARD\n\n"
    _assert_span_round_trips(result)


@pytest.mark.parametrize(
    ("cue", "normalized"),
    [
        ("ANNA", "ANNA"),
        ("ANNA (V.O.)", "ANNA"),
        ("ANNA (O.S.)", "ANNA"),
        ("ANNA (O.C.)", "ANNA"),
        ("ANNA (CONT'D)", "ANNA"),
    ],
)
def test_character_cue_normalization_keeps_original_cue(cue, normalized):
    result = parse_source("INT. ROOM - DAY\n{}\nHello.\n".format(cue))
    cue_block = result.blocks[1]

    assert cue_block.block_type == "character"
    assert cue_block.original_text == cue
    assert cue_block.character_cue == cue
    assert cue_block.normalized_cue == normalized
    assert normalize_character_cue(cue) == normalized
    _assert_span_round_trips(result)


def test_dialogue_parentheticals_transitions_and_multiple_lines_are_distinguished():
    text = "INT. ROOM - DAY\nELI\nFirst line.\nSecond line.\n(quietly)\nThird line.\nCUT TO:\n"
    result = parse_source(text)

    assert [block.block_type for block in result.blocks] == [
        "scene_heading",
        "character",
        "dialogue",
        "dialogue",
        "parenthetical",
        "dialogue",
        "transition",
    ]
    _assert_span_round_trips(result)


@pytest.mark.parametrize(
    ("heading", "status"),
    [
        ("INT. ROOM - NIGHT", BoundaryStatus.CONFIRMED),
        ("INT KITCHEN - NIGHT", BoundaryStatus.CANDIDATE),
        ("INT.", BoundaryStatus.UNCERTAIN),
    ],
)
def test_boundary_statuses_do_not_promote_malformed_headings(heading, status):
    result = parse_source(heading + "\nSomeone waits.\n")

    candidate = next(
        item for item in result.boundary_candidates if item.boundary_status != BoundaryStatus.NO_EXPECTED
    )
    assert candidate.boundary_status == status
    assert len(result.scenes) == (1 if status == BoundaryStatus.CONFIRMED else 0)
    if status != BoundaryStatus.CONFIRMED:
        assert any(item.boundary_status == BoundaryStatus.NO_EXPECTED for item in result.boundary_candidates)
    _assert_span_round_trips(result)


def test_missing_heading_preserves_entire_text_as_pre_scene_material():
    text = "MAYA\nWe should go.\nThe door opens.\n"
    result = parse_source(text)

    assert not result.scenes
    assert result.pre_scene_span is not None
    assert text[result.pre_scene_span.start_offset : result.pre_scene_span.end_offset] == text
    assert any(item.boundary_status == BoundaryStatus.NO_EXPECTED for item in result.boundary_candidates)
    assert {diagnostic.code for diagnostic in result.diagnostics} >= {
        "missing_scene_heading",
        "pre_scene_text",
    }
    _assert_span_round_trips(result)


def test_file_input_preserves_original_crlf_bytes_and_filename(tmp_path: Path):
    content = "INT. ROOM - DAY\r\nA door opens.\r\n".encode("utf-8")
    path = tmp_path / "original.txt"
    path.write_bytes(content)

    result = parse_source(path, work_id="work-1")

    assert result.source.original_text == content.decode("utf-8")
    assert result.source.original_bytes == content
    assert result.source.original_filename == "original.txt"
    assert result.source.content_hash == "sha256:{}".format(hashlib.sha256(content).hexdigest())
    assert result.source.newline_characteristics.style == "crlf"
    _assert_span_round_trips(result)


def test_mixed_line_endings_are_counted_without_normalizing_source():
    text = "INT. ROOM - DAY\r\nMAYA\nHello.\rEXT. ROAD - DAY"
    result = parse_source(text)

    assert result.source.original_text == text
    assert result.source.newline_characteristics.style == "mixed"
    assert result.source.newline_characteristics.crlf_count == 1
    assert result.source.newline_characteristics.lf_count == 1
    assert result.source.newline_characteristics.cr_count == 1
    assert [scene.scene_start_span.start_line for scene in result.scenes] == [1, 4]
    _assert_span_round_trips(result)


def test_unsupported_file_format_is_reported_without_parsing(tmp_path: Path):
    path = tmp_path / "script.pdf"
    path.write_bytes(b"not parsed")

    result = parse_source(path)

    assert not result.blocks
    assert not result.scenes
    assert [diagnostic.code for diagnostic in result.diagnostics] == ["unknown_format"]


def test_source_input_accepts_film_reference_but_does_not_parse_it_as_screenplay():
    result = parse_source(SourceInput(original_text="not screenplay text", source_kind="film_reference"))

    assert result.source.original_text == "not screenplay text"
    assert not result.blocks
    assert [diagnostic.code for diagnostic in result.diagnostics] == ["unsupported_construct"]
