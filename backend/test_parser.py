from backend.app.parsers.screenplay import classify_lines


def test_legacy_classify_lines_interface_returns_source_aligned_blocks():
    blocks = classify_lines("INT. ROOM - DAY\nA door opens.\n")

    assert [block.type for block in blocks] == ["scene_heading", "action"]
    assert [block.text for block in blocks] == ["INT. ROOM - DAY", "A door opens."]
    assert all(block.block_id for block in blocks)
