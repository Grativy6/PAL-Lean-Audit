#!/usr/bin/env python3
"""Emit CI benchmark counts from the checked Attack Run 0003 receipts."""

from __future__ import annotations

import argparse
import json
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "Audit" / "attack-run-0003-receipt.json"
AXIOM_PATTERN = re.compile(
    r"^'([^']+)' (does not depend on any axioms|depends on axioms:.*)$",
    re.MULTILINE,
)
POLICY_FIXTURES = (
    ROOT / "Audit" / "fixtures" / "T05-ascii-omega.fixture",
    ROOT / "Audit" / "fixtures" / "T05-symbol-omega.fixture",
    ROOT / "Audit" / "fixtures" / "AR3-explanatory-shorthand-status.fixture",
    ROOT / "Audit" / "fixtures" / "AR3-first-occurrence-closure.fixture",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wall-nanoseconds", required=True, type=int)
    parser.add_argument("--axiom-artifact", required=True, type=pathlib.Path)
    parser.add_argument("--output", required=True, type=pathlib.Path)
    args = parser.parse_args()
    if args.wall_nanoseconds < 0:
        raise SystemExit("wall nanoseconds must be nonnegative")

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    expected_rows = receipt.get("dependency_receipts", [])
    expected = {row["declaration"]: row.get("axioms", []) for row in expected_rows}
    if not expected or len(expected) != len(expected_rows):
        raise SystemExit("dependency receipt inventory is empty or duplicated")

    artifact = args.axiom_artifact.resolve()
    raw = artifact.read_bytes()
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    parsed = AXIOM_PATTERN.findall(raw.decode(encoding, errors="replace").replace("\r\n", "\n"))
    observed = {name: result for name, result in parsed}
    if len(observed) != len(parsed) or set(observed) != set(expected):
        raise SystemExit("captured axiom artifact does not match the dependency inventory")
    for name, axioms in expected.items():
        rendered = (
            "depends on axioms: [" + ", ".join(axioms) + "]"
            if axioms
            else "does not depend on any axioms"
        )
        if observed[name] != rendered:
            raise SystemExit(f"captured axiom mismatch for {name}")

    missing_fixtures = [str(path.relative_to(ROOT)) for path in POLICY_FIXTURES if not path.is_file()]
    if missing_fixtures:
        raise SystemExit(f"missing policy fixtures: {missing_fixtures}")
    results = receipt.get("results", [])
    formal_result_count = sum(
        row.get("classification")
        not in {"EXPECTED_REJECTION", "OPEN_MANUAL", "TRANSLATION_AMBIGUITY"}
        for row in results
    )

    lines = [
        "measurement=cached_lake_build",
        f"wall_nanoseconds={args.wall_nanoseconds}",
        f"checked_declarations={len(expected)}",
        f"empty_axiom_receipts={sum(not axioms for axioms in expected.values())}",
        f"propext_only_receipts={sum(axioms == ['propext'] for axioms in expected.values())}",
        "propext_and_quot_sound_receipts="
        + str(sum(axioms == ["propext", "Quot.sound"] for axioms in expected.values())),
        f"formal_results={formal_result_count}",
        f"negative_controls={len(receipt.get('negative_controls', []))}",
        f"policy_fixtures={len(POLICY_FIXTURES)}",
        "cache_state=warm_after_lean_action",
        "correctness_score=NOT_CALCULATED",
        "count_source=validated_machine_receipts_and_captured_axiom_artifact",
        "",
    ]
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote measured CI benchmark receipt: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
