#!/usr/bin/env python3
"""Fail closed on unexpected axioms in Prime Shells dependency receipts.

The checker reads every ``prime-shells-*-axioms.txt`` file in the selected
artifact directory and accepts only Lean's standard logical dependencies:
``propext``, ``Classical.choice``, and ``Quot.sound``.  An empty dependency
list is also valid.

This does not prove source adequacy, novelty, or mathematical interpretation.
It only prevents a manuscript-specific axiom, ``sorryAx``, native-decision
axiom, or other unreviewed dependency from passing silently in the recorded
Prime Shells theorem surface.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from dataclasses import dataclass

ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
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
    """Normalize a comma-separated Lean axiom list."""
    return frozenset(
        item.strip()
        for item in raw.replace("\n", " ").split(",")
        if item.strip()
    )


def read_receipts(directory: pathlib.Path) -> list[ReceiptResult]:
    paths = sorted(directory.glob("prime-shells-*-axioms.txt"))
    if not paths:
        raise RuntimeError(
            f"no Prime Shells axiom receipts found in {directory}; "
            "the checker will not pass an absent receipt set"
        )

    results: list[ReceiptResult] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        matches = list(RECEIPT_PATTERN.finditer(text))
        if not matches:
            raise RuntimeError(f"no parseable '#print axioms' receipts in {path}")
        for match in matches:
            results.append(
                ReceiptResult(
                    path=path,
                    declaration=match.group("declaration"),
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
        help="directory containing prime-shells-*-axioms.txt receipts",
    )
    args = parser.parse_args()

    try:
        receipts = read_receipts(args.directory)
    except (OSError, RuntimeError) as exc:
        print(f"Prime Shells axiom check failed: {exc}", file=sys.stderr)
        return 1

    unexpected: list[tuple[ReceiptResult, frozenset[str]]] = []
    for receipt in receipts:
        extra = receipt.axioms - ALLOWED_AXIOMS
        if extra:
            unexpected.append((receipt, extra))

    if unexpected:
        print("Prime Shells axiom check failed closed:", file=sys.stderr)
        for receipt, extra in unexpected:
            print(
                f"- {receipt.declaration} in {receipt.path}: "
                f"unexpected axioms {sorted(extra)}",
                file=sys.stderr,
            )
        return 1

    files = sorted({result.path.name for result in receipts})
    print(
        "Prime Shells axiom check passed: "
        f"{len(receipts)} declarations across {len(files)} receipt files; "
        f"allowed dependencies={sorted(ALLOWED_AXIOMS)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
