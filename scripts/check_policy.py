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
OMEGA_IDENTIFIER = re.compile(r"(?<![A-Za-z0-9_'])Omega(?![A-Za-z0-9_'])|Ω")
OMEGA_DIAGNOSTIC = "object-language Omega identifier forbidden by T05"
EXPECTED_FIREWALL_FIXTURES = (
    ROOT / "Audit" / "fixtures" / "T05-ascii-omega.fixture",
    ROOT / "Audit" / "fixtures" / "T05-symbol-omega.fixture",
)


def lean_files() -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for item in LEAN_ROOTS:
        if item.is_dir():
            files.extend(sorted(item.rglob("*.lean")))
        elif item.exists():
            files.append(item)
    return files


def strip_lean_comments_and_strings(text: str) -> str:
    """Blank comments and strings while preserving offsets and line numbers."""
    chars = list(text)
    index = 0
    block_depth = 0
    in_line_comment = False
    in_string = False
    escaped = False

    while index < len(text):
        pair = text[index : index + 2]
        char = text[index]

        if in_line_comment:
            if char == "\n":
                in_line_comment = False
            else:
                chars[index] = " "
            index += 1
            continue

        if block_depth:
            if pair == "/-":
                chars[index] = chars[index + 1] = " "
                block_depth += 1
                index += 2
            elif pair == "-/":
                chars[index] = chars[index + 1] = " "
                block_depth -= 1
                index += 2
            else:
                if char != "\n":
                    chars[index] = " "
                index += 1
            continue

        if in_string:
            if char != "\n":
                chars[index] = " "
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue

        if pair == "--":
            chars[index] = chars[index + 1] = " "
            in_line_comment = True
            index += 2
        elif pair == "/-":
            chars[index] = chars[index + 1] = " "
            block_depth = 1
            index += 2
        elif char == '"':
            chars[index] = " "
            in_string = True
            index += 1
        else:
            index += 1

    return "".join(chars)


def omega_diagnostics(path: pathlib.Path, text: str) -> list[str]:
    code = strip_lean_comments_and_strings(text)
    diagnostics: list[str] = []
    for match in OMEGA_IDENTIFIER.finditer(code):
        line = code.count("\n", 0, match.start()) + 1
        diagnostics.append(f"{path.relative_to(ROOT)}:{line}: {OMEGA_DIAGNOSTIC}")
    return diagnostics


def main() -> int:
    failures: list[str] = []
    for path in lean_files():
        text = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                failures.append(f"{path.relative_to(ROOT)}:{line}: {label}")
        failures.extend(omega_diagnostics(path, text))

    expected_rejections: list[str] = []
    for path in EXPECTED_FIREWALL_FIXTURES:
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT)}: missing expected T05 fixture")
            continue
        diagnostics = omega_diagnostics(path, path.read_text(encoding="utf-8"))
        if len(diagnostics) != 1:
            failures.append(
                f"{path.relative_to(ROOT)}: expected one stable T05 diagnostic, "
                f"observed {len(diagnostics)}"
            )
        else:
            expected_rejections.extend(diagnostics)
    if failures:
        print("Policy check failed:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"Policy check passed for {len(lean_files())} Lean files.")
    print("Expected T05 rejections:")
    print("\n".join(expected_rejections))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
