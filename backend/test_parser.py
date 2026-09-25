from pathlib import Path

from app.parsers.screenplay import classify_lines


screenplay_path = Path("../data/works/test-screenplay.txt")
text = screenplay_path.read_text(encoding="utf-8")

blocks = classify_lines(text)

for block in blocks:
    print(f"{block.type:15} | {block.text}")