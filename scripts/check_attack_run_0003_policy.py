#!/usr/bin/env python3
"""Enforce Gate 5 policy without changing historical Attack Run checks."""

from __future__ import annotations

import pathlib
import re
import sys

from check_policy import ROOT, lean_files, strip_lean_comments_and_strings


SHORTHAND_DECLARATION = re.compile(
    r"^\s*(?:inductive|structure|class|def|abbrev|opaque|axiom|theorem|lemma)\s+"
    r"OccurrenceClosedSourceOpen\b",
    re.MULTILINE | re.IGNORECASE,
)
DEBT_CLOSURE_DECLARATION = re.compile(
    r"^\s*(?:theorem|lemma|def|abbrev|opaque|axiom)\s+"
    r"(?:"
    r"close\w*(?:O04|O25|FirstOccurrence)\w*|"
    r"(?:O04|O25|FirstOccurrence)\w*(?:Closed|Closure)\w*"
    r")\b",
    re.MULTILINE | re.IGNORECASE,
)
SHORTHAND_DIAGNOSTIC = (
    "selected declaration spelling would promote explanatory shorthand to an object-language primitive or status"
)
DEBT_DIAGNOSTIC = (
    "selected declaration spelling would purport to close an OPEN first-occurrence burden"
)
EXPECTED_FIXTURES = {
    ROOT / "Audit" / "fixtures" / "AR3-explanatory-shorthand-status.fixture": (
        SHORTHAND_DECLARATION,
        SHORTHAND_DIAGNOSTIC,
    ),
    ROOT / "Audit" / "fixtures" / "AR3-first-occurrence-closure.fixture": (
        DEBT_CLOSURE_DECLARATION,
        DEBT_DIAGNOSTIC,
    ),
}


def diagnostics(path: pathlib.Path, text: str) -> list[str]:
    code = strip_lean_comments_and_strings(text)
    rows: list[str] = []
    for pattern, message in (
        (SHORTHAND_DECLARATION, SHORTHAND_DIAGNOSTIC),
        (DEBT_CLOSURE_DECLARATION, DEBT_DIAGNOSTIC),
    ):
        for match in pattern.finditer(code):
            line = code.count("\n", 0, match.start()) + 1
            rows.append(f"{path.relative_to(ROOT)}:{line}: {message}")
    return rows


def main() -> int:
    failures: list[str] = []
    for path in lean_files():
        failures.extend(diagnostics(path, path.read_text(encoding="utf-8")))

    expected: list[str] = []
    for path, (pattern, message) in EXPECTED_FIXTURES.items():
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT)}: missing expected Gate 5 fixture")
            continue
        code = strip_lean_comments_and_strings(path.read_text(encoding="utf-8"))
        matches = list(pattern.finditer(code))
        all_rows = diagnostics(path, path.read_text(encoding="utf-8"))
        matching_rows = [row for row in all_rows if row.endswith(message)]
        if len(matches) != 1 or len(matching_rows) != 1 or len(all_rows) != 1:
            failures.append(
                f"{path.relative_to(ROOT)}: expected exactly one stable Gate 5 diagnostic"
            )
        else:
            expected.extend(matching_rows)

    if failures:
        print("Attack Run 0003 policy check failed:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"Attack Run 0003 policy passed for {len(lean_files())} Lean files.")
    print("Expected Gate 5 rejections:")
    print("\n".join(expected))
    print(
        "These are bounded naming guards, not semantic completeness checks; "
        "differently named surrogates remain OPEN_MANUAL source review."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
