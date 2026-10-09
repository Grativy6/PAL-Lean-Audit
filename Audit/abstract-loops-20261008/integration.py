"""Verify the new receipt set and the existing project gates without rewriting old reports."""
from pathlib import Path
import json
import re
import sys
from datetime import datetime, timezone
import verify

ROOT, AREA = verify.ROOT, verify.AREA

def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    directory = AREA / "integration" / stamp
    directory.mkdir(parents=True)
    rows = []
    for batch in verify.MODULES:
        verify.check(batch)
    verify.self_test()
    commands = [
        ("default-build", [verify.LAKE, "build"]),
        ("root-kernel", [verify.LAKE, "env", "leanchecker", "PALLeanAudit"]),
        ("historical-policy", [sys.executable, "scripts/check_policy.py"]),
        ("report-check", [sys.executable, "scripts/render_report.py", "--check"]),
        ("migration-report-check", [sys.executable, "scripts/render_migration_report.py", "--check"]),
        ("attack-run-0003-report-check", [sys.executable, "scripts/render_attack_run_0003.py", "--check"]),
        ("diff-check", ["git", "diff", "--check"]),
    ]
    for label, argv in commands:
        row = verify.run(argv, directory, label)
        rows.append(row)
        print(label, "exit", row["exit_code"], flush=True)
    for batch in verify.MODULES:
        verify.check(batch)
    status = "PASS_INTEGRATION" if all(row["exit_code"] == 0 for row in rows) else "FAILED_INTEGRATION_GATE"
    result = {"schema": "abstract-loops-integration-v1", "status": status,
              "started_utc": stamp, "commands": rows,
              "receipt_mutation_controls": 6,
              "selected_source_policy": "Every new module and inspection module checked by verify.py, exact declaration inventory and no forbidden proof escapes; historical policy has its original narrower scope.",
              "receipts": {b: verify.sha(AREA / b / "results.json") for b in verify.MODULES},
              "scope": "Local integration; no CI, remote write, source adoption or publication"}
    verify.write(directory / "results.json", result)
    verify.write(AREA / "integration-results.json", result)
    if status != "PASS_INTEGRATION":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
