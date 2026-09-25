from __future__ import annotations

import hashlib
import re
from bisect import bisect_right
from pathlib import Path
from typing import Iterable, Optional, Union

from ..schemas.screenplay import (
    BlockType,
    BoundaryStatus,
    DiagnosticCode,
    LocatorInformation,
    NewlineCharacteristics,
    ParseResult,
    ParserDiagnostic,
    SceneBoundaryCandidate,
    SceneCandidate,
    ScriptBlock,
    SourceInput,
    SourceKind,
    SourceRevision,
    SourceSpan,
)


TRANSITIONS = {
    "FADE IN:",
    "FADE OUT.",
    "FADE OUT:",
    "CUT TO:",
    "DISSOLVE TO:",
    "SMASH CUT TO:",
    "MATCH CUT TO:",
    "JUMP CUT TO:",
}

_STANDARD_HEADING = re.compile(
    r"^(?:INT\./EXT\.|EXT\./INT\.|INT\.|EXT\.|I/E\.)\s+\S.*$",
    re.IGNORECASE,
)
_STANDARD_HEADING_PREFIX = re.compile(
    r"^(?:INT\./EXT\.|EXT\./INT\.|INT\.|EXT\.|I/E\.)\s*$",
    re.IGNORECASE,
)
_MALFORMED_HEADING_PREFIX = re.compile(r"^(?:INT|EXT)(?:\s+|/)", re.IGNORECASE)
_KNOWN_CUE_EXTENSION = re.compile(
    r"\s+\((?:V\.O\.|O\.S\.|O\.C\.|CONT['’]D)\)\s*$",
    re.IGNORECASE,
)
_CUE_CHARACTERS = re.compile(r"^[A-Z0-9][A-Z0-9 .,'’()\-]*$")
_ACTION_WORDS = {
    "CROSSES",
    "ENTERS",
    "EXITS",
    "FALLS",
    "GETS",
    "GOES",
    "JUMPS",
    "LOOKS",
    "MOVES",
    "OPENS",
    "PICKS",
    "RUNS",
    "SITS",
    "STANDS",
    "TURNS",
    "WALKS",
}

BlockTypeName = BlockType
DiagnosticCodeName = DiagnosticCode


def _digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _stable_id(prefix: str, *parts: object) -> str:
    material = "\0".join(str(part) for part in parts).encode("utf-8")
    return "{}_{}".format(prefix, _digest(material)[:24])


def _filename_key(filename: Optional[str]) -> str:
    if not filename:
        return ""
    return filename.replace("\\", "/").rsplit("/", 1)[-1]


def _source_id(
    source_id: Optional[str],
    work_id: Optional[str],
    source_kind: SourceKind,
    original_filename: Optional[str],
    revision_id: Optional[str],
) -> str:
    if source_id:
        return source_id
    identity = _filename_key(original_filename) or revision_id or "unidentified"
    return _stable_id("src", work_id or "", source_kind, identity)


def _newline_characteristics(text: Optional[str]) -> NewlineCharacteristics:
    if not text:
        return NewlineCharacteristics("none", 0, 0, 0)
    crlf_count = text.count("\r\n")
    lf_count = text.count("\n") - crlf_count
    cr_count = text.count("\r") - crlf_count
    styles = sum(count > 0 for count in (crlf_count, lf_count, cr_count))
    if styles == 0:
        style = "none"
    elif styles > 1:
        style = "mixed"
    elif crlf_count:
        style = "crlf"
    elif lf_count:
        style = "lf"
    else:
        style = "cr"
    return NewlineCharacteristics(style, crlf_count, lf_count, cr_count)


def _source_revision(
    text: Optional[str],
    *,
    work_id: Optional[str],
    source_kind: SourceKind,
    original_filename: Optional[str],
    source_id: Optional[str],
    original_bytes: Optional[bytes] = None,
) -> SourceRevision:
    if text is not None:
        encoded = original_bytes if original_bytes is not None else text.encode("utf-8")
        digest = _digest(encoded)
        content_hash = "sha256:{}".format(digest)
        revision_id = "rev_{}".format(digest)
        resolved_bytes = encoded
    elif original_bytes is not None:
        digest = _digest(original_bytes)
        content_hash = "sha256:{}".format(digest)
        revision_id = "rev_{}".format(digest)
        resolved_bytes = original_bytes
    else:
        content_hash = None
        revision_id = None
        resolved_bytes = None

    resolved_source_id = _source_id(
        source_id,
        work_id,
        source_kind,
        original_filename,
        revision_id,
    )
    return SourceRevision(
        source_id=resolved_source_id,
        work_id=work_id,
        source_kind=source_kind,
        original_filename=original_filename,
        original_text=text,
        content_hash=content_hash,
        revision_id=revision_id,
        newline_characteristics=_newline_characteristics(text),
        locator_information=LocatorInformation(),
        original_bytes=resolved_bytes,
    )


def _line_spans(text: str) -> list[tuple[int, int, int]]:
    """Return (body_start, body_end, one_based_line) without newline characters."""
    result: list[tuple[int, int, int]] = []
    line_start = 0
    line_number = 1
    index = 0

    while index < len(text):
        char = text[index]
        if char not in "\r\n":
            index += 1
            continue

        result.append((line_start, index, line_number))
        if char == "\r" and index + 1 < len(text) and text[index + 1] == "\n":
            index += 2
        else:
            index += 1
        line_start = index
        line_number += 1

    if line_start < len(text):
        result.append((line_start, len(text), line_number))
    elif not result and text == "":
        return []

    return result


def _line_starts(text: str) -> list[int]:
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


def _offset_to_line_column(offset: int, starts: list[int]) -> tuple[int, int]:
    line_index = bisect_right(starts, offset) - 1
    return line_index + 1, offset - starts[line_index] + 1


def _span(text: str, start: int, end: int, starts: list[int]) -> SourceSpan:
    start_line, start_column = _offset_to_line_column(start, starts)
    end_line, end_column = _offset_to_line_column(end, starts)
    return SourceSpan(
        start_offset=start,
        end_offset=end,
        start_line=start_line,
        end_line=end_line,
        start_column=start_column,
        end_column=end_column,
    )


def _classification_text(raw_line: str, line_number: int) -> str:
    value = raw_line.strip()
    if line_number == 1:
        value = value.lstrip("\ufeff")
    return value


def _heading_assessment(line: str) -> Optional[tuple[BoundaryStatus, str]]:
    if _STANDARD_HEADING.fullmatch(line):
        return BoundaryStatus.CONFIRMED, "standard_scene_heading_prefix_and_descriptor"
    if _STANDARD_HEADING_PREFIX.fullmatch(line):
        return BoundaryStatus.UNCERTAIN, "standard_prefix_without_scene_descriptor"
    if _MALFORMED_HEADING_PREFIX.match(line):
        return BoundaryStatus.CANDIDATE, "scene_heading_prefix_missing_standard_punctuation"
    return None


def is_scene_heading(line: str) -> bool:
    assessment = _heading_assessment(line.strip())
    return assessment is not None and assessment[0] == BoundaryStatus.CONFIRMED


def is_transition(line: str) -> bool:
    return line.strip().upper() in TRANSITIONS


def is_parenthetical(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("(") and stripped.endswith(")")


def _cue_shape(line: str) -> bool:
    return (
        bool(line)
        and len(line) <= 40
        and any(char.isalpha() for char in line)
        and line.upper() == line
        and _CUE_CHARACTERS.fullmatch(line) is not None
    )


def is_character(line: str) -> bool:
    """Compatibility predicate: checks cue shape, not context or identity."""
    return _cue_shape(line.strip())


def normalize_character_cue(cue: str) -> str:
    normalized = " ".join(cue.strip().split())
    while True:
        without_extension, count = _KNOWN_CUE_EXTENSION.subn("", normalized)
        if count == 0:
            break
        normalized = without_extension.strip()
    return " ".join(normalized.split())


def _next_nonblank(
    lines: list[tuple[int, int, int]], text: str, index: int
) -> Optional[str]:
    for start, end, line_number in lines[index + 1 :]:
        candidate = _classification_text(text[start:end], line_number)
        if candidate:
            return candidate
    return None


def _looks_like_character_action(line: str) -> bool:
    words = {word.strip(".,'’()") for word in line.split()}
    return bool(words & _ACTION_WORDS)


def _classify_line(
    text: str,
    lines: list[tuple[int, int, int]],
    index: int,
    previous_type: Optional[BlockType],
) -> tuple[BlockType, Optional[str], Optional[str], Optional[str]]:
    start, end, line_number = lines[index]
    raw_line = text[start:end]
    value = _classification_text(raw_line, line_number)

    if not value:
        return "blank", None, None, None

    heading = _heading_assessment(value)
    if heading is not None:
        return "scene_heading", None, None, None
    if is_transition(value):
        return "transition", None, None, None
    if is_parenthetical(value) and previous_type in {
        "character",
        "parenthetical",
        "dialogue",
    }:
        return "parenthetical", None, None, None

    if _cue_shape(value):
        next_text = _next_nonblank(lines, text, index)
        has_extension = _KNOWN_CUE_EXTENSION.search(value) is not None
        has_action_word = _looks_like_character_action(value)
        next_is_boundary = (
            next_text is not None
            and (_heading_assessment(next_text) is not None or is_transition(next_text))
        )
        next_can_be_dialogue = (
            next_text is not None
            and not next_is_boundary
            and (is_parenthetical(next_text) or next_text.upper() != next_text)
        )
        token_count = len(value.split())
        leading_indentation = len(raw_line) - len(raw_line.lstrip())
        multiword_name_is_ambiguous = token_count > 1 and leading_indentation == 0

        if (
            next_can_be_dialogue
            and not has_action_word
            and (has_extension or token_count == 1 or not multiword_name_is_ambiguous)
        ):
            return "character", value, normalize_character_cue(value), None
        if next_text is None or next_is_boundary or has_action_word or multiword_name_is_ambiguous:
            return "action", None, None, "uppercase_line_may_be_action_or_character_cue"

    if previous_type in {"character", "parenthetical", "dialogue"}:
        return "dialogue", None, None, None
    return "action", None, None, None


def _build_diagnostic(
    code: DiagnosticCodeName,
    message: str,
    span: Optional[SourceSpan] = None,
    review_required: bool = False,
    details: Iterable[str] = (),
) -> ParserDiagnostic:
    return ParserDiagnostic(
        code=code,
        message=message,
        source_span=span,
        review_required=review_required,
        details=tuple(details),
    )


def _empty_result(
    source: SourceRevision,
    diagnostics: Iterable[ParserDiagnostic],
) -> ParseResult:
    return ParseResult(
        source=source,
        blocks=(),
        boundary_candidates=(),
        scenes=(),
        diagnostics=tuple(diagnostics),
    )


def _parse_supported_text(source: SourceRevision) -> ParseResult:
    text = source.original_text or ""
    starts = _line_starts(text)
    lines = _line_spans(text)
    blocks: list[ScriptBlock] = []
    boundaries: list[SceneBoundaryCandidate] = []
    diagnostics: list[ParserDiagnostic] = []
    previous_type: Optional[BlockType] = None

    for index, (line_start, line_end, line_number) in enumerate(lines):
        raw_line = text[line_start:line_end]
        block_type, character_cue, normalized_cue, ambiguity = _classify_line(
            text,
            lines,
            index,
            previous_type,
        )
        block_span = _span(text, line_start, line_end, starts)
        block_id = _stable_id(
            "blk",
            source.source_id,
            source.revision_id,
            line_start,
            line_end,
            block_type,
        )
        block = ScriptBlock(
            block_id=block_id,
            block_type=block_type,
            original_text=raw_line,
            source_start_offset=line_start,
            source_end_offset=line_end,
            start_line=block_span.start_line,
            end_line=block_span.end_line,
            start_column=block_span.start_column,
            end_column=block_span.end_column,
            character_cue=character_cue,
            normalized_cue=normalized_cue,
        )
        blocks.append(block)

        classification = _classification_text(raw_line, line_number)
        heading = _heading_assessment(classification)
        if heading is not None:
            status, reason = heading
            flags: list[str] = []
            if status != BoundaryStatus.CONFIRMED:
                flags.append("human_review_required")
                diagnostics.append(
                    _build_diagnostic(
                        "suspicious_scene_heading",
                        "Heading-like text was not promoted to a confirmed scene boundary.",
                        block_span,
                        review_required=True,
                        details=(reason,),
                    )
                )
            if status == BoundaryStatus.UNCERTAIN:
                diagnostics.append(
                    _build_diagnostic(
                        "malformed_structure",
                        "A scene-heading prefix is present but has no usable scene descriptor.",
                        block_span,
                        review_required=True,
                        details=(reason,),
                    )
                )
            boundaries.append(
                SceneBoundaryCandidate(
                    candidate_id=_stable_id(
                        "bnd",
                        source.source_id,
                        source.revision_id,
                        line_start,
                        line_end,
                        status.value,
                        reason,
                    ),
                    source_span=block_span,
                    observed_text=raw_line,
                    boundary_status=status,
                    reason=reason,
                    diagnostic_flags=tuple(flags),
                )
            )

        if ambiguity is not None:
            diagnostics.append(
                _build_diagnostic(
                    "ambiguous_character_cue",
                    "An uppercase line could be a character cue or action text; it remains action.",
                    block_span,
                    review_required=True,
                    details=(ambiguity,),
                )
            )

        if "\x00" in raw_line or "\f" in raw_line or "\v" in raw_line:
            diagnostics.append(
                _build_diagnostic(
                    "unsupported_construct",
                    "A non-line-oriented control character was preserved but not interpreted.",
                    block_span,
                    review_required=True,
                    details=("control_character",),
                )
            )

        previous_type = None if block_type == "blank" else block_type

    confirmed_blocks = [
        block
        for block in blocks
        if block.block_type == "scene_heading"
        and _heading_assessment(
            _classification_text(block.original_text, block.start_line)
        )
        == (BoundaryStatus.CONFIRMED, "standard_scene_heading_prefix_and_descriptor")
    ]
    confirmed_starts = {block.source_start_offset for block in confirmed_blocks}
    confirmed_boundaries = [
        candidate
        for candidate in boundaries
        if candidate.boundary_status == BoundaryStatus.CONFIRMED
    ]

    if not confirmed_blocks:
        zero_span = _span(text, 0, 0, starts)
        boundaries.append(
            SceneBoundaryCandidate(
                candidate_id=_stable_id(
                    "bnd",
                    source.source_id,
                    source.revision_id,
                    "no-expected-boundary",
                ),
                source_span=zero_span,
                observed_text="",
                boundary_status=BoundaryStatus.NO_EXPECTED,
                reason="no_recognizable_scene_heading_found",
                diagnostic_flags=("missing_scene_heading",),
            )
        )
        diagnostics.append(
            _build_diagnostic(
                "missing_scene_heading",
                "No confirmed scene heading was found; no scene was constructed.",
                _span(text, 0, len(text), starts),
                review_required=True,
            )
        )

    first_heading_start = confirmed_blocks[0].source_start_offset if confirmed_blocks else None
    pre_scene_span: Optional[SourceSpan] = None
    if first_heading_start is not None and first_heading_start > 0:
        pre_scene_span = _span(text, 0, first_heading_start, starts)
    elif first_heading_start is None and text:
        pre_scene_span = _span(text, 0, len(text), starts)

    if pre_scene_span is not None and text[pre_scene_span.start_offset : pre_scene_span.end_offset].strip():
        diagnostics.append(
            _build_diagnostic(
                "pre_scene_text",
                "Nonblank source material occurs before the first confirmed scene heading.",
                pre_scene_span,
                review_required=False,
            )
        )

    scenes: list[SceneCandidate] = []
    for sequence, heading_block in enumerate(confirmed_blocks, start=1):
        scene_start = heading_block.source_start_offset
        later_starts = [
            block.source_start_offset
            for block in confirmed_blocks
            if block.source_start_offset > scene_start
        ]
        scene_end = min(later_starts) if later_starts else len(text)
        scene_span = _span(text, scene_start, scene_end, starts)
        end_anchor = _span(text, scene_end, scene_end, starts)
        contained_ids = tuple(
            block.block_id
            for block in blocks
            if scene_start <= block.source_start_offset < scene_end
        )
        scenes.append(
            SceneCandidate(
                scene_id=_stable_id(
                    "scn",
                    source.source_id,
                    source.revision_id,
                    sequence,
                    heading_block.block_id,
                ),
                source_id=source.source_id,
                source_revision_id=source.revision_id or "",
                sequence=sequence,
                heading_block_id=heading_block.block_id,
                scene_start_span=_span(
                    text,
                    heading_block.source_start_offset,
                    heading_block.source_end_offset,
                    starts,
                ),
                scene_end_span=end_anchor,
                scene_span=scene_span,
                original_text=text[scene_start:scene_end],
                contained_block_ids=contained_ids,
            )
        )

    # Protect against accidental disagreement between boundary and scene stages.
    if {
        item.source_span.start_offset
        for item in confirmed_boundaries
        if item.source_span is not None
    } != confirmed_starts:
        diagnostics.append(
            _build_diagnostic(
                "malformed_structure",
                "Confirmed boundary records and scene-heading blocks do not align.",
                review_required=True,
            )
        )

    return ParseResult(
        source=source,
        blocks=tuple(blocks),
        boundary_candidates=tuple(boundaries),
        scenes=tuple(scenes),
        diagnostics=tuple(diagnostics),
        pre_scene_span=pre_scene_span,
    )


def _failed_source_result(
    source: SourceRevision,
    code: DiagnosticCodeName,
    message: str,
) -> ParseResult:
    return _empty_result(
        source,
        (
            _build_diagnostic(
                code,
                message,
                review_required=True,
            ),
        ),
    )


def parse_source(
    source: Union[SourceInput, str, Path],
    *,
    work_id: Optional[str] = None,
    source_id: Optional[str] = None,
    source_kind: SourceKind = "screenplay",
    original_filename: Optional[str] = None,
) -> ParseResult:
    """Parse pasted screenplay text or a UTF-8 .txt file without rewriting its source."""
    if isinstance(source, Path):
        filename = source.name
        if source.suffix.lower() != ".txt":
            revision = _source_revision(
                None,
                work_id=work_id,
                source_kind=source_kind,
                original_filename=filename,
                source_id=source_id,
            )
            return _failed_source_result(
                revision,
                "unknown_format",
                "Only UTF-8 .txt screenplay files are supported by this experiment.",
            )
        raw_bytes = source.read_bytes()
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            revision = _source_revision(
                None,
                work_id=work_id,
                source_kind=source_kind,
                original_filename=filename,
                source_id=source_id,
                original_bytes=raw_bytes,
            )
            return _failed_source_result(
                revision,
                "unknown_format",
                "The .txt source is not valid UTF-8; original bytes were retained without parsing.",
            )
        source_input = SourceInput(
            original_text=text,
            work_id=work_id,
            source_kind=source_kind,
            original_filename=filename,
            source_id=source_id,
        )
        revision = _source_revision(
            source_input.original_text,
            work_id=source_input.work_id,
            source_kind=source_input.source_kind,
            original_filename=source_input.original_filename,
            source_id=source_input.source_id,
            original_bytes=raw_bytes,
        )
    elif isinstance(source, SourceInput):
        source_input = source
        revision = _source_revision(
            source_input.original_text,
            work_id=source_input.work_id,
            source_kind=source_input.source_kind,
            original_filename=source_input.original_filename,
            source_id=source_input.source_id,
        )
    elif isinstance(source, str):
        source_input = SourceInput(
            original_text=source,
            work_id=work_id,
            source_kind=source_kind,
            original_filename=original_filename,
            source_id=source_id,
        )
        revision = _source_revision(
            source_input.original_text,
            work_id=source_input.work_id,
            source_kind=source_input.source_kind,
            original_filename=source_input.original_filename,
            source_id=source_input.source_id,
        )
    else:
        raise TypeError("source must be a SourceInput, raw text string, or Path")

    if revision.source_kind != "screenplay":
        return _failed_source_result(
            revision,
            "unsupported_construct",
            "Only screenplay text is parsed; film_reference Sources are metadata-only.",
        )
    if revision.original_text is None:
        return _failed_source_result(
            revision,
            "unknown_format",
            "Source text could not be decoded and is not available to the parser.",
        )
    return _parse_supported_text(revision)


def classify_lines(text: str) -> list[ScriptBlock]:
    """Compatibility wrapper returning source-aligned blocks for raw text."""
    return list(parse_source(text).blocks)


def parse_source_file(path: Union[str, Path], **metadata: object) -> ParseResult:
    """Convenience wrapper for callers that keep paths as strings."""
    return parse_source(Path(path), **metadata)
