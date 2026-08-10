#!/usr/bin/env python3
"""Run local Gate 5 checks and write measured Attack Run 0003 evidence."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import platform
import subprocess
import sys
import time


ROOT = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "Audit" / "evidence" / "attack-run-0003"
BUILD_LOG = EVIDENCE_DIR / "local-lake-build.txt"
AXIOM_LOG = EVIDENCE_DIR / "local-axiom-receipts.txt"
VALIDATION_LOG = EVIDENCE_DIR / "local-validation.txt"
BENCHMARKS = ROOT / "Audit" / "attack-run-0003-benchmarks.json"
RECEIPT = ROOT / "Audit" / "attack-run-0003-receipt.json"
LEDGER = ROOT / "Audit" / "attack-run-0003-claim-ledger.json"


def run(command: list[str]) -> tuple[int, str, float]:
    started = time.perf_counter()
    result = subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=os.environ.copy(),
        check=False,
    )
    return result.returncode, result.stdout, time.perf_counter() - started


def canonical_lf_sha256(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    return hashlib.sha256(
        text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    ).hexdigest()


def display(command: list[str]) -> str:
    return subprocess.list2cmdline(command)


def redact(value: str, published_zip: pathlib.Path) -> str:
    """Remove machine-local user paths while retaining exact command roles."""
    return (
        value.replace(str(published_zip), "<published-zip>")
        .replace(str(ROOT), "<repository>")
        .replace(sys.executable, "python")
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--published-zip", type=pathlib.Path, required=True)
    args = parser.parse_args()
    published_zip = args.published_zip.resolve()
    if not published_zip.is_file():
        raise SystemExit(f"published ZIP is missing: {published_zip}")
    if not RECEIPT.is_file() or not LEDGER.is_file():
        raise SystemExit("Attack Run 0003 receipt and ledger must exist first")

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    measured_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

    build_command = ["lake", "build"]
    build_code, build_output, build_seconds = run(build_command)
    BUILD_LOG.write_text(
        f"measured_at_utc={measured_at}\n"
        f"command={display(build_command)}\n"
        f"exit_code={build_code}\n"
        f"wall_seconds={build_seconds:.6f}\n\n"
        f"{build_output}",
        encoding="utf-8",
    )
    if build_code != 0:
        raise SystemExit(f"lake build failed; see {BUILD_LOG.relative_to(ROOT)}")

    axiom_command = ["lake", "env", "lean", "Audit/AttackRun0003.lean"]
    axiom_code, axiom_output, _ = run(axiom_command)
    AXIOM_LOG.write_text(axiom_output, encoding="utf-8")
    if axiom_code != 0:
        raise SystemExit(f"axiom capture failed; see {AXIOM_LOG.relative_to(ROOT)}")

    py = sys.executable
    checks: list[tuple[str, list[str]]] = [
        ("historical_policy", [py, "scripts/check_policy.py"]),
        ("gate5_policy", [py, "scripts/check_attack_run_0003_policy.py"]),
        ("candidate_input_regression", [py, "scripts/check_candidate_inputs.py"]),
        (
            "published_source_and_migration",
            [
                py,
                "scripts/check_release_migration.py",
                "--published-zip",
                str(published_zip),
            ],
        ),
        ("attack_run_0001_report", [py, "scripts/render_report.py", "--check"]),
        (
            "attack_run_0002_report",
            [
                py,
                "scripts/render_report.py",
                "--ledger",
                "Audit/attack-run-0002-claim-ledger.json",
                "--summary",
                "docs/generated/attack-run-0002-summary.md",
                "--chart",
                "docs/generated/attack-run-0002-outcomes.svg",
                "--check",
            ],
        ),
        ("migration_report", [py, "scripts/render_migration_report.py", "--check"]),
        ("attack_run_0003_structure", [py, "scripts/check_attack_run_0003.py"]),
        (
            "attack_run_0003_dependencies",
            [
                py,
                "scripts/check_attack_run_0003_axioms.py",
                "--artifact",
                str(AXIOM_LOG),
            ],
        ),
        (
            "leanchecker",
            [
                "lake",
                "env",
                "leanchecker",
                "PALLeanAudit",
            ],
        ),
    ]
    validation_lines = [
        f"measured_at_utc={measured_at}",
        f"published_zip={published_zip.name}",
        "",
    ]
    check_rows: list[dict] = []
    failed = False
    for name, command in checks:
        code, output, seconds = run(command)
        check_lines = [
            f"## {name}",
            f"command={redact(display(command), published_zip)}",
            f"exit_code={code}",
            f"wall_seconds={seconds:.6f}",
        ]
        rendered_output = redact(output.rstrip(), published_zip)
        if rendered_output:
            check_lines.append(rendered_output)
        check_lines.append("")
        validation_lines.extend(check_lines)
        check_rows.append(
            {
                "name": name,
                "command": redact(display(command), published_zip),
                "exit_code": code,
                "wall_seconds": round(seconds, 6),
            }
        )
        failed = failed or code != 0
    VALIDATION_LOG.write_text("\n".join(validation_lines), encoding="utf-8")
    if failed:
        raise SystemExit(f"one or more checks failed; see {VALIDATION_LOG.relative_to(ROOT)}")

    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    dependencies = receipt["dependency_receipts"]
    formal_statuses = {
        "PROVED_FROM_DECLARED_RULES",
        "CONSISTENT_REALIZATION",
        "ASSUMPTION_BOUND",
        "COUNTERMODEL_TO_OVERCLAIM",
    }
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    ).stdout.strip()
    lean_code, lean_version, _ = run(["lean", "--version"])
    if lean_code != 0:
        raise SystemExit("lean --version failed")
    mathlib_revision = json.loads((ROOT / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib = next(
        package for package in mathlib_revision["packages"] if package["name"] == "mathlib"
    )
    data = {
        "schema_version": "1.0.0",
        "run_id": "attack-0003",
        "measured": True,
        "measured_at_utc": measured_at,
        "environment": f"{lean_version.strip()}; Mathlib revision {mathlib['rev']}; {platform.platform()}",
        "baseline_commit": head,
        "commit_under_test": None,
        "worktree_state": "UNCOMMITTED_GATE5_WORKTREE; exact PR head and synthetic merge commits are captured separately by CI because a tracked receipt cannot self-identify its own future commit.",
        "measurement_method": "One wall-clock observation using Python perf_counter after an earlier successful build; local Lake and Mathlib caches were warm.",
        "repetitions": 1,
        "cache_state": "WARM_LOCAL_CACHE",
        "missing_data": ["Peak memory was not collected locally; CI retains its own runner evidence separately."],
        "privacy_redactions": [
            "Machine-local repository and published-ZIP paths are replaced by role labels in the committed validation log."
        ],
        "build_measurement": {
            "command": display(build_command),
            "exit_code": build_code,
            "wall_seconds": round(build_seconds, 6),
            "output_log": str(BUILD_LOG.relative_to(ROOT)).replace("\\", "/"),
            "output_canonical_lf_sha256": canonical_lf_sha256(BUILD_LOG),
        },
        "axiom_evidence": {
            "command": display(axiom_command),
            "exit_code": axiom_code,
            "output_log": str(AXIOM_LOG.relative_to(ROOT)).replace("\\", "/"),
            "output_canonical_lf_sha256": canonical_lf_sha256(AXIOM_LOG),
        },
        "repository_checks": check_rows,
        "validation_log": {
            "path": str(VALIDATION_LOG.relative_to(ROOT)).replace("\\", "/"),
            "canonical_lf_sha256": canonical_lf_sha256(VALIDATION_LOG),
        },
        "measurements": {
            "build_wall_seconds": round(build_seconds, 6),
            "checked_declarations": len(dependencies),
            "empty_axiom_receipts": sum(not row["axioms"] for row in dependencies),
            "nonempty_axiom_receipts": sum(bool(row["axioms"]) for row in dependencies),
            "propext_only_receipts": sum(
                row["axioms"] == ["propext"] for row in dependencies
            ),
            "propext_and_quot_sound_receipts": sum(
                row["axioms"] == ["propext", "Quot.sound"] for row in dependencies
            ),
            "formal_result_count": sum(
                claim["classification"] in formal_statuses for claim in ledger["claims"]
            ),
            "negative_control_count": len(receipt["negative_controls"]),
            "policy_fixture_count": 4,
            "repository_check_count": len(check_rows),
        },
        "authority_ceiling": "Timing and population counts describe this measured run only. They are not theorem strength, adoption authority, or a PAL correctness score.",
    }
    BENCHMARKS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {BENCHMARKS.relative_to(ROOT)}")
    print(f"lake build wall seconds: {build_seconds:.6f}")
    print(f"repository checks: {len(check_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
