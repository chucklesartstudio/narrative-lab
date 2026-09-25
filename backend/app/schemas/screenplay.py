from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal, Optional


BlockType = Literal[
    "scene_heading",
    "action",
    "character",
    "dialogue",
    "parenthetical",
    "transition",
    "blank",
]

SourceKind = Literal["screenplay", "film_reference"]
DiagnosticCode = Literal[
    "unknown_format",
    "suspicious_scene_heading",
    "missing_scene_heading",
    "ambiguous_character_cue",
    "pre_scene_text",
    "malformed_structure",
    "unsupported_construct",
]


class BoundaryStatus(str, Enum):
    CONFIRMED = "confirmed_boundary"
    CANDIDATE = "candidate_boundary"
    UNCERTAIN = "uncertain_malformed"
    NO_EXPECTED = "no_expected_boundary"


@dataclass(frozen=True)
class SourceInput:
    original_text: str
    work_id: Optional[str] = None
    source_kind: SourceKind = "screenplay"
    original_filename: Optional[str] = None
    source_id: Optional[str] = None


@dataclass(frozen=True)
class NewlineCharacteristics:
    style: Literal["none", "lf", "crlf", "cr", "mixed"]
    crlf_count: int
    lf_count: int
    cr_count: int


@dataclass(frozen=True)
class LocatorInformation:
    canonical_unit: str = "unicode_codepoint"
    offset_base: int = 0
    interval: str = "half_open"
    line_column_base: int = 1
    line_endings_in_block_spans: bool = False


@dataclass(frozen=True)
class SourceRevision:
    source_id: str
    work_id: Optional[str]
    source_kind: SourceKind
    original_filename: Optional[str]
    original_text: Optional[str]
    content_hash: Optional[str]
    revision_id: Optional[str]
    newline_characteristics: NewlineCharacteristics
    locator_information: LocatorInformation = field(default_factory=LocatorInformation)
    original_bytes: Optional[bytes] = field(default=None, repr=False, compare=False)


@dataclass(frozen=True)
class SourceSpan:
    start_offset: int
    end_offset: int
    start_line: int
    end_line: int
    start_column: int
    end_column: int


@dataclass(frozen=True)
class ScriptBlock:
    block_id: str
    block_type: BlockType
    original_text: str
    source_start_offset: int
    source_end_offset: int
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    character_cue: Optional[str] = None
    normalized_cue: Optional[str] = None

    # Compatibility properties for the original type/text parser interface.
    @property
    def type(self) -> BlockType:
        return self.block_type

    @property
    def text(self) -> str:
        return self.original_text


@dataclass(frozen=True)
class SceneBoundaryCandidate:
    candidate_id: str
    source_span: Optional[SourceSpan]
    observed_text: str
    boundary_status: BoundaryStatus
    reason: str
    diagnostic_flags: tuple[str, ...] = ()


@dataclass(frozen=True)
class SceneCandidate:
    scene_id: str
    source_id: str
    source_revision_id: str
    sequence: int
    heading_block_id: str
    scene_start_span: SourceSpan
    scene_end_span: SourceSpan
    scene_span: SourceSpan
    original_text: str
    contained_block_ids: tuple[str, ...]


@dataclass(frozen=True)
class ParserDiagnostic:
    code: DiagnosticCode
    message: str
    source_span: Optional[SourceSpan] = None
    review_required: bool = False
    details: tuple[str, ...] = ()


@dataclass(frozen=True)
class ParseResult:
    source: SourceRevision
    blocks: tuple[ScriptBlock, ...]
    boundary_candidates: tuple[SceneBoundaryCandidate, ...]
    scenes: tuple[SceneCandidate, ...]
    diagnostics: tuple[ParserDiagnostic, ...]
    pre_scene_span: Optional[SourceSpan] = None

    @property
    def source_revision_id(self) -> Optional[str]:
        return self.source.revision_id
