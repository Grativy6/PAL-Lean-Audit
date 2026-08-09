#!/usr/bin/env python3
"""Fail closed unless every expected theorem has an empty Lean axiom receipt."""

from __future__ import annotations

import argparse
import pathlib
import re


EXPECTED_BY_RUN = {
    "attack-0002": (
        "PAL.AttackRun0002.sourceFiberCountermodel",
        "PAL.AttackRun0002.downstreamCannotDistinguishSameCut",
        "PAL.AttackRun0002.occurrenceDoesNotIdentifySource",
        "PAL.AttackRun0002.costDoesNotImplyCause",
        "PAL.AttackRun0002.historicalPersistence",
        "PAL.AttackRun0002.noGlobalFirstFromLocalFirst",
        "PAL.AttackRun0002.inquiryCreatesNewReceipt",
        "PAL.AttackRun0002.noRetroactivePayment",
    ),
}
RECEIPT_PATTERN = re.compile(
    r"^'([^']+)' (does not depend on any axioms|depends on axioms:.*)$",
    re.MULTILINE,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", choices=sorted(EXPECTED_BY_RUN), required=True)
    parser.add_argument("--artifact", type=pathlib.Path, required=True)
    args = parser.parse_args()

    raw = args.artifact.read_bytes()
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    text = raw.decode(encoding, errors="replace").replace("\r\n", "\n")
    receipts = RECEIPT_PATTERN.findall(text)
    expected = set(EXPECTED_BY_RUN[args.run_id])
    observed = {name for name, _ in receipts}
    if observed != expected or len(receipts) != len(expected):
        missing = sorted(expected - observed)
        unexpected = sorted(observed - expected)
        raise SystemExit(
            "Axiom receipt set mismatch: "
            f"missing={missing}, unexpected={unexpected}, rows={len(receipts)}"
        )
    nonempty = {
        name: result
        for name, result in receipts
        if result != "does not depend on any axioms"
    }
    if nonempty:
        raise SystemExit(f"Nonempty axiom dependencies found: {nonempty}")
    print(f"Verified {len(expected)} empty axiom receipts for {args.run_id}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
