#!/usr/bin/env python3
"""Fail closed on unexpected dependencies in Prime Shells Lean receipts.

The checker requires the complete five-file receipt set and accepts only Lean's
standard logical dependencies: ``propext``, ``Classical.choice``, and
``Quot.sound``. An empty dependency list is also valid.

This does not prove source adequacy, novelty, or mathematical interpretation.
It prevents an absent receipt file, a manuscript-specific postulate,
``sorryAx``, native-decision dependency, or other unreviewed dependency from
passing silently in the recorded Prime Shells theorem surface.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from dataclasses import dataclass

ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
REQUIRED_RECEIPTS = (
    "prime-shells-axioms.txt",
    "prime-shells-mod-three-kernel-axioms.txt",
    "prime-shells-conditioning-axioms.txt",
    "prime-shells-basis-transport-axioms.txt",
    "prime-shells-condition-number-axioms.txt",
)
RECEIPT_PATTERN = re.compile(
    r"'(?P<declaration>[^']+)'\s+depends on axioms:\s*\[(?P<axioms>.*?)\]",
    re.DOTALL,
)


@dataclass(frozen=True)
class ReceiptResult:
    path: pathlib.Path
    declaration: str
    axioms: frozenset[str]


def parse_axioms(raw: str) -> frozenset[str]:
    """Normalize a comma-separated Lean dependency list."""
    return frozenset(
        item.strip()
        for item in raw.replace("\n", " ").split(",")
        if item.strip()
    )


def read_receipts(directory: pathlib.Path) -> list[ReceiptResult]:
    paths = [directory / name for name in REQUIRED_RECEIPTS]
    missing = [path.name for path in paths if not path.is_file()]
    if missing:
        raise RuntimeError(
            "missing required Prime Shells receipt files: " + ", ".join(missing)
        )

    results: list[ReceiptResult] = []
    seen_declarations: set[str] = set()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        matches = list(RECEIPT_PATTERN.finditer(text))
        if not matches:
            raise RuntimeError(f"no parseable '#print axioms' receipts in {path}")
        for match in matches:
            declaration = match.group("declaration")
            if declaration in seen_declarations:
                raise RuntimeError(
                    f"duplicate Prime Shells declaration receipt: {declaration}"
                )
            seen_declarations.add(declaration)
            results.append(
                ReceiptResult(
                    path=path,
                    declaration=declaration,
                    axioms=parse_axioms(match.group("axioms")),
                )
            )
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory",
        nargs="?",
        default="artifacts",
        type=pathlib.Path,
        help="directory containing the five Prime Shells receipt files",
    )
    args = parser.parse_args()

    try:
        receipts = read_receipts(args.directory)
    except (OSError, RuntimeError) as exc:
        print(f"Prime Shells dependency check failed: {exc}", file=sys.stderr)
        return 1

    unexpected: list[tuple[ReceiptResult, frozenset[str]]] = []
    for receipt in receipts:
        extra = receipt.axioms - ALLOWED_AXIOMS
        if extra:
            unexpected.append((receipt, extra))

    if unexpected:
        print("Prime Shells dependency check failed closed:", file=sys.stderr)
        for receipt, extra in unexpected:
            print(
                f"- {receipt.declaration} in {receipt.path}: "
                f"unexpected dependencies {sorted(extra)}",
                file=sys.stderr,
            )
        return 1

    print(
        "Prime Shells dependency check passed: "
        f"{len(receipts)} unique declarations across "
        f"{len(REQUIRED_RECEIPTS)} required receipt files; "
        f"allowed dependencies={sorted(ALLOWED_AXIOMS)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
