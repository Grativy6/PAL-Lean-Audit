#!/usr/bin/env python3
"""Fail closed on unexpected dependencies in Framed Prime Shells v0.2.

The checker requires both v0.2 receipt files and accepts only Lean's standard
logical dependencies: ``propext``, ``Classical.choice``, and ``Quot.sound``.
It does not establish novelty, source adequacy, physical interpretation, or
publication authority.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from dataclasses import dataclass

ALLOWED = frozenset({"propext", "Classical.choice", "Quot.sound"})
REQUIRED = (
    "prime-shells-v02-three-charts-axioms.txt",
    "prime-shells-v02-ribbons-axioms.txt",
)
PATTERN = re.compile(
    r"'(?P<declaration>[^']+)'\s+depends on axioms:\s*\[(?P<axioms>.*?)\]",
    re.DOTALL,
)


@dataclass(frozen=True)
class Receipt:
    path: pathlib.Path
    declaration: str
    dependencies: frozenset[str]


def parse(raw: str) -> frozenset[str]:
    return frozenset(
        item.strip()
        for item in raw.replace("\n", " ").split(",")
        if item.strip()
    )


def load(directory: pathlib.Path) -> list[Receipt]:
    paths = [directory / name for name in REQUIRED]
    missing = [path.name for path in paths if not path.is_file()]
    if missing:
        raise RuntimeError("missing required v0.2 receipts: " + ", ".join(missing))

    receipts: list[Receipt] = []
    seen: set[str] = set()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        matches = list(PATTERN.finditer(text))
        if not matches:
            raise RuntimeError(f"no parseable dependency receipts in {path}")
        for match in matches:
            declaration = match.group("declaration")
            if declaration in seen:
                raise RuntimeError(f"duplicate declaration receipt: {declaration}")
            seen.add(declaration)
            receipts.append(
                Receipt(path, declaration, parse(match.group("axioms")))
            )
    return receipts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?", default="artifacts", type=pathlib.Path)
    args = parser.parse_args()

    try:
        receipts = load(args.directory)
    except (OSError, RuntimeError) as exc:
        print(f"Framed Prime Shells v0.2 dependency check failed: {exc}", file=sys.stderr)
        return 1

    failures: list[str] = []
    for receipt in receipts:
        extra = receipt.dependencies - ALLOWED
        if extra:
            failures.append(
                f"{receipt.declaration} in {receipt.path}: "
                f"unexpected dependencies {sorted(extra)}"
            )

    if failures:
        print("Framed Prime Shells v0.2 dependency check failed closed:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1

    print(
        "Framed Prime Shells v0.2 dependency check passed: "
        f"{len(receipts)} unique declarations across {len(REQUIRED)} receipt files; "
        f"allowed dependencies={sorted(ALLOWED)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
