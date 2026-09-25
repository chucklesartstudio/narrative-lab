from dataclasses import dataclass
from typing import Literal


BlockType = Literal[
    "scene_heading",
    "action",
    "character",
    "dialogue",
    "parenthetical",
    "transition",
    "blank",
]


@dataclass
class ScriptBlock:
    type: BlockType
    text: str


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


def is_scene_heading(line: str) -> bool:
    upper = line.upper()

    return (
        upper.startswith("INT.")
        or upper.startswith("EXT.")
        or upper.startswith("INT./EXT.")
        or upper.startswith("EXT./INT.")
        or upper.startswith("I/E.")
    )


def is_transition(line: str) -> bool:
    return line.upper() in TRANSITIONS


def is_character(line: str) -> bool:
    """
    Basic screenplay heuristic:
    character cues are usually uppercase and relatively short.
    """
    stripped = line.strip()

    if not stripped:
        return False

    if len(stripped) > 40:
        return False

    return stripped.isupper()


def is_parenthetical(line: str) -> bool:
    stripped = line.strip()

    return stripped.startswith("(") and stripped.endswith(")")


def classify_lines(text: str) -> list[ScriptBlock]:
    lines = text.splitlines()

    blocks: list[ScriptBlock] = []

    previous_type: BlockType | None = None

    for raw_line in lines:
        line = raw_line.strip()

        # Blank line
        if not line:
            blocks.append(
                ScriptBlock(
                    type="blank",
                    text="",
                )
            )

            previous_type = "blank"
            continue

        # Scene heading
        if is_scene_heading(line):
            blocks.append(
                ScriptBlock(
                    type="scene_heading",
                    text=line,
                )
            )

            previous_type = "scene_heading"
            continue

        # Transition
        if is_transition(line):
            blocks.append(
                ScriptBlock(
                    type="transition",
                    text=line,
                )
            )

            previous_type = "transition"
            continue

        # Parenthetical after a character cue
        if is_parenthetical(line) and previous_type == "character":
            blocks.append(
                ScriptBlock(
                    type="parenthetical",
                    text=line,
                )
            )

            previous_type = "parenthetical"
            continue

        # Character cue
        if is_character(line):
            blocks.append(
                ScriptBlock(
                    type="character",
                    text=line,
                )
            )

            previous_type = "character"
            continue

        # Dialogue normally follows character / parenthetical
        if previous_type in {"character", "parenthetical", "dialogue"}:
            blocks.append(
                ScriptBlock(
                    type="dialogue",
                    text=line,
                )
            )

            previous_type = "dialogue"
            continue

        # Everything else is action
        blocks.append(
            ScriptBlock(
                type="action",
                text=line,
            )
        )

        previous_type = "action"

    return blocks