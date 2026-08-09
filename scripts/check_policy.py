#!/usr/bin/env python3
"""Reject proof placeholders and undeclared axiom declarations in Lean sources."""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEAN_ROOTS = (
    ROOT / "PAL",
    ROOT / "Audit",
    ROOT / "PAL.lean",
    ROOT / "Audit.lean",
    ROOT / "PALLeanAudit.lean",
)
FORBIDDEN = {
    "proof placeholder sorry": re.compile(r"\bsorry\b"),
    "proof placeholder admit": re.compile(r"\badmit\b"),
    "unlisted axiom declaration": re.compile(r"^\s*axiom\b", re.MULTILINE),
}


def lean_files() -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for item in LEAN_ROOTS:
        if item.is_dir():
            files.extend(sorted(item.rglob("*.lean")))
        elif item.exists():
            files.append(item)
    return files


def main() -> int:
    failures: list[str] = []
    for path in lean_files():
        text = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                failures.append(f"{path.relative_to(ROOT)}:{line}: {label}")
    if failures:
        print("Policy check failed:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"Policy check passed for {len(lean_files())} Lean files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
