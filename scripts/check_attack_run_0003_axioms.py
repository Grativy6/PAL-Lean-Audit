#!/usr/bin/env python3
"""Validate Attack Run 0003 dependency receipts against its machine receipt."""

from __future__ import annotations

import argparse
import json
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_RECEIPT = ROOT / "Audit" / "attack-run-0003-receipt.json"
RECEIPT_PATTERN = re.compile(
    r"^'([^']+)' (does not depend on any axioms|depends on axioms:.*)$",
    re.MULTILINE,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=pathlib.Path, required=True)
    parser.add_argument("--receipt", type=pathlib.Path, default=DEFAULT_RECEIPT)
    args = parser.parse_args()

    receipt_path = args.receipt if args.receipt.is_absolute() else ROOT / args.receipt
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    rows = receipt.get("dependency_receipts", [])
    expected = {row["declaration"]: row.get("axioms", []) for row in rows}
    if len(expected) != len(rows) or not expected:
        raise SystemExit("dependency receipt inventory is empty or contains duplicates")

    raw = args.artifact.read_bytes()
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    text = raw.decode(encoding, errors="replace").replace("\r\n", "\n")
    parsed = RECEIPT_PATTERN.findall(text)
    observed = {name: result for name, result in parsed}
    if len(observed) != len(parsed) or set(observed) != set(expected):
        raise SystemExit(
            "Attack Run 0003 dependency set mismatch: "
            f"missing={sorted(set(expected) - set(observed))}, "
            f"unexpected={sorted(set(observed) - set(expected))}, rows={len(parsed)}"
        )

    mismatches: dict[str, str] = {}
    for name, result in observed.items():
        expected_axioms = expected[name]
        if expected_axioms:
            rendered = "depends on axioms: [" + ", ".join(expected_axioms) + "]"
            if result != rendered:
                mismatches[name] = result
        elif result != "does not depend on any axioms":
            mismatches[name] = result
    if mismatches:
        raise SystemExit(f"Attack Run 0003 dependency mismatch: {mismatches}")

    empty = sum(not axioms for axioms in expected.values())
    nonempty = len(expected) - empty
    print(
        f"Verified {len(expected)} Attack Run 0003 dependency receipts: "
        f"empty={empty}, nonempty={nonempty}."
    )
    print(
        "This empty/nonempty population describes this declared realization only; "
        "it is not a universal PAL-conformance rule."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
