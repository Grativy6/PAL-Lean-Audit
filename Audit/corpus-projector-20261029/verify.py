#!/usr/bin/env python3
"""Verify the exact projector theorem inventory and its captured axiom output."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_policy import FORBIDDEN, strip_lean_comments_and_strings

SOURCE = ROOT / "Experiments/CorpusBridgeProjector.lean"
AUDIT = ROOT / "Experiments/CorpusBridgeProjectorAxioms.lean"
BASE = "bd49451caa409fe9091f209048afe814fa9aa30b"
BASE_FILES = [
    "Experiments/CorpusBridgeSixLines.lean",
    "Experiments/CorpusBridgeSixLinesAxioms.lean",
    "Audit/BridgeEndpoint.lean",
    "lean-toolchain", "lake-manifest.json", "lakefile.lean",
]


def inspect(source: str, audit: str, receipt: str, manifest: dict) -> dict:
    code = strip_lean_comments_and_strings(source)
    names = re.findall(r"^theorem\s+(\w+)", code, re.M)
    if names != manifest["required"] or not set(manifest["critical"]) <= set(names):
        raise ValueError("Theorem inventory differs from the declared target")
    for label, pattern in FORBIDDEN.items():
        if pattern.search(code):
            raise ValueError(label)
    if "sorryAx" in receipt:
        raise ValueError("Admission dependency in receipt")
    reports = {}
    for name in names:
        full = manifest["namespace"] + "." + name
        if "#check @" + full not in audit or "#print axioms " + full not in audit:
            raise ValueError("Missing type/dependency inspection for " + full)
        pattern = (r"['\"]?" + re.escape(full) +
                   r"['\"]?\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)")
        matches = list(re.finditer(pattern, receipt))
        if len(matches) != 1:
            raise ValueError("Missing or repeated dependency result for " + full)
        used = set(re.findall(r"[A-Za-z_][\w.]*", matches[0].group(1) or ""))
        if not used <= set(manifest["allowed_axioms"]):
            raise ValueError("Unapproved dependencies for " + full + ": " + repr(used))
        reports[full] = sorted(used)
    return reports


def negative_controls(source: str, audit: str, receipt: str, manifest: dict) -> list[str]:
    missing = manifest["namespace"] + "." + manifest["critical"][0]
    cases = {
        "missing_critical_receipt": receipt.replace(missing, missing + "_missing"),
        "custom_axiom": receipt.replace("propext", "Unapproved.assumption", 1),
        "admission": receipt + "\nsorryAx\n",
        "duplicated_receipt": receipt + "\n" + receipt,
    }
    rejected = []
    for name, damaged in cases.items():
        try:
            inspect(source, audit, damaged, manifest)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("Invalid evidence accepted: " + name)
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--axioms", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Use a fresh output file")
    manifest = json.loads((HERE / "declarations.json").read_text())
    source = SOURCE.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    captured = args.axioms.read_text(encoding="utf-8-sig")
    reports = inspect(source, audit, captured, manifest)
    rejected = negative_controls(source, audit, captured, manifest)
    subprocess.run(["git", "diff", "--exit-code", BASE, "--", *BASE_FILES],
                   cwd=ROOT, check=True, capture_output=True)
    files = [SOURCE, AUDIT, HERE / "declarations.json", HERE / "verify.py",
             *[ROOT / p for p in BASE_FILES]]
    result = {
        "status": "PASS", "base": BASE, "declaration_count": len(reports),
        "dependency_reports": reports, "rejected_negative_controls": rejected,
        "base_inputs_unchanged": BASE_FILES,
        "source_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"):
                          hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        "axiom_receipt_sha256": hashlib.sha256(args.axioms.read_bytes()).hexdigest(),
        "scope": "Exact captured declarations and permitted dependencies; process/kernel exits are recorded by the runner.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Accepted {len(reports)} exact dependency reports; rejected {len(rejected)} corrupted receipts.")


if __name__ == "__main__":
    main()
