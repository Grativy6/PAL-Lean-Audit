#!/usr/bin/env python3
"""Reproduce the bounded native build using an existing pinned dependency cache.

Run from any directory, with explicit --lean-bin, --packages and fresh --output.
This reads the supplied dependency cache and writes only this checkout's build
output and the new evidence directory. CI separately uses Lake's pinned setup.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean-bin", type=Path, required=True)
    parser.add_argument("--packages", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    suffix = ".exe" if os.name == "nt" else ""
    lean = args.lean_bin / ("lean" + suffix)
    kernel = args.lean_bin / ("leanchecker" + suffix)
    build = ROOT / ".lake/build/lib/lean"
    for name in ["Experiments", "Audit"]:
        (build / name).mkdir(parents=True, exist_ok=True)
    dependencies = sorted(p / ".lake/build/lib/lean" for p in args.packages.iterdir()
                          if (p / ".lake/build/lib/lean").is_dir())
    env = os.environ.copy()
    env["LEAN_PATH"] = os.pathsep.join(str(p) for p in [build, *dependencies])
    records = []
    manifest = {"started_at": datetime.now(timezone.utc).isoformat(),
                "platform": platform.platform(), "python": platform.python_version(),
                "commands": records, "status": "RUNNING"}

    def save() -> None:
        (args.output / "run.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    def run(name: str, command: list[str]) -> str:
        started = time.monotonic()
        proc = subprocess.run(command, cwd=ROOT, env=env, capture_output=True)
        (args.output / (name + ".stdout.txt")).write_bytes(proc.stdout)
        (args.output / (name + ".stderr.txt")).write_bytes(proc.stderr)
        record = {"name": name, "command": [Path(command[0]).name, *command[1:]],
                  "exit_code": proc.returncode, "seconds": round(time.monotonic()-started, 3),
                  "stdout_sha256": hashlib.sha256(proc.stdout).hexdigest(),
                  "stderr_sha256": hashlib.sha256(proc.stderr).hexdigest()}
        records.append(record)
        save()
        print(f"{name}: exit {proc.returncode}", flush=True)
        if proc.returncode:
            print(proc.stdout.decode("utf-8", errors="replace"))
            print(proc.stderr.decode("utf-8", errors="replace"))
            manifest["status"] = "FAIL"
            save()
            raise SystemExit(proc.returncode)
        return proc.stdout.decode("utf-8", errors="replace")

    if (ROOT / "lean-toolchain").read_text().strip() != "leanprover/lean4:v4.32.1":
        raise SystemExit("Unexpected toolchain pin")
    version = run("lean-version", [str(lean), "--version"])
    if "version 4.32.1," not in version or "f054605aea4b840552cca2e725580bffd1e1b704" not in version:
        raise SystemExit("Unexpected compiler identity")
    manifest["lean_version"] = version.strip()
    manifest["compiler_sha256"] = hashlib.sha256(lean.read_bytes()).hexdigest()
    manifest["kernel_binary_sha256"] = hashlib.sha256(kernel.read_bytes()).hexdigest()
    mathlib_head = run("mathlib-head", ["git", "-C", str(args.packages / "mathlib"), "rev-parse", "HEAD"]).strip()
    if mathlib_head != "520045ab14e26149ee970e2e617ca04b09bde5d6":
        raise SystemExit("Unexpected Mathlib revision")
    manifest["mathlib_head"] = mathlib_head
    for module in ["Experiments.CorpusBridgeSixLines", "Audit.BridgeEndpoint", "Experiments.CorpusBridgeProjector"]:
        source = module.replace(".", "/") + ".lean"
        output = build / (module.replace(".", "/") + ".olean")
        run("build-" + module, [str(lean), "-o", str(output), source])
    run("axioms", [str(lean), "Experiments/CorpusBridgeProjectorAxioms.lean"])
    run("verify", [sys.executable, "Audit/corpus-projector-20261029/verify.py",
                   "--axioms", str(args.output / "axioms.stdout.txt"),
                   "--output", str(args.output / "verification.json")])
    run("kernel", [str(kernel), "Experiments.CorpusBridgeProjector"])
    run("historical-policy", [sys.executable, "scripts/check_policy.py"])
    run("diff-check", ["git", "diff", "--check"])
    manifest["status"] = "PASS"
    manifest["completed_at"] = datetime.now(timezone.utc).isoformat()
    save()


if __name__ == "__main__":
    main()
