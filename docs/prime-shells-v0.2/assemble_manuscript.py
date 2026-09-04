#!/usr/bin/env python3
"""Assemble the Framed Prime Shells v0.2 Markdown source in declared order."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARTS = (
    "MANUSCRIPT_PART_00_FRONT.md",
    "MANUSCRIPT_PART_01_V01_CORE.md",
    "MANUSCRIPT_PART_02_V02_ATLAS_RIBBONS.md",
    "MANUSCRIPT_PART_03_BACKMATTER.md",
)
OUTPUT = ROOT / "Framed_Prime_Shells_v0.2_Working_Manuscript.md"


def main() -> None:
    missing = [name for name in PARTS if not (ROOT / name).is_file()]
    if missing:
        raise SystemExit("missing manuscript parts: " + ", ".join(missing))
    text = "\n".join((ROOT / name).read_text(encoding="utf-8").rstrip() for name in PARTS) + "\n"
    OUTPUT.write_text(text, encoding="utf-8", newline="\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
