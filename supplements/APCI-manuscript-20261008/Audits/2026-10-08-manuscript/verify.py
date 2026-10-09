"""Bounded APCI-only supplement check; no downloads or source-repository writes."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

AREA = Path(__file__).resolve().parent
ROOT = AREA.parents[1]
REPO = ROOT / "Lean project"
GIT = Path(r"C:\Program Files\Git\mingw64\bin\git.exe")
BIN = Path(r"C:\Users\cdpan\.elan\toolchains\leanprover--lean4---v4.32.1\bin")
COMMIT = "0f85cc7fac47c3b34ecfd11160f3efae454b900c"
TREE = "a4418e2fb2c1fe5ffe6be768a419385da8834c99"
EXPECTED = {
    "APCIManuscript.no_exact_on_witness_of_capacity":
        ["Classical.choice", "Quot.sound", "propext"],
    "APCIManuscript.infinite_world_constant_property": [],
    "APCIManuscript.side_information_changes_interface": [],
    "APCIManuscript.empty_trace_allows_empty_answer": [],
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> bytes:
    return subprocess.run([str(GIT), *args], cwd=REPO, check=True,
                          capture_output=True, timeout=10).stdout


def snapshot() -> dict[str, str]:
    names = git("ls-files", "-z").decode("utf-8").strip("\0").split("\0")
    return {name: sha(REPO / name) for name in names}


def dependencies(text: str) -> dict[str, list[str]]:
    pairs = re.findall(
        r"'([^']+)' (?:does not depend on any axioms|depends on axioms:\s*\[(.*?)\])",
        text, re.S)
    assert len(pairs) == len(EXPECTED), "Unexpected dependency record count"
    return {name: sorted(x.strip() for x in deps.split(",") if x.strip())
            for name, deps in pairs}


def main() -> None:
    output = (ROOT / sys.argv[1]).resolve()
    assert output.is_relative_to(ROOT / "Receipts")
    assert output.is_dir(), "Outer runner must prepare a fresh receipt directory"
    assert not (output / "result.json").exists(), "Receipt already exists"
    result = {
        "schema": "apci-manuscript-supplement-v1",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "status": "RUNNING", "commands": [],
        "scope": "one derived corollary and three boundary controls; APCI only",
        "commit": git("rev-parse", "HEAD").decode().strip(),
        "tree": git("rev-parse", "HEAD^{tree}").decode().strip(),
        "git_status_before": git("status", "--porcelain").decode(),
        "tracked_before": snapshot(),
    }

    def run(name: str, argv: list[str], env: dict[str, str] | None = None) -> str:
        started = time.perf_counter()
        proc = subprocess.run(argv, cwd=REPO, env=env, capture_output=True,
                              timeout=120)
        data = proc.stdout + proc.stderr
        (output / f"{name}.log").write_bytes(data)
        result["commands"].append({
            "name": name, "argv": argv, "cwd": str(REPO),
            "exit_code": proc.returncode,
            "seconds": time.perf_counter() - started,
            "log_sha256": hashlib.sha256(data).hexdigest(),
        })
        print(f"{name}: exit {proc.returncode}", flush=True)
        text = data.decode("utf-8")
        if proc.returncode:
            print(text, flush=True)
        assert proc.returncode == 0, f"{name} failed"
        return text

    try:
        assert result["commit"] == COMMIT and result["tree"] == TREE
        assert result["git_status_before"] == ""
        assert (REPO / "lean-toolchain").read_text().strip() == "leanprover/lean4:v4.32.1"
        assert json.loads((REPO / "lake-manifest.json").read_text())["packages"] == []
        old = json.loads((ROOT / "Receipts/2026-10-08-local-replay/receipt.json").read_text())
        assert result["tracked_before"] == old["tracked_files_before"]
        result["reused_core_receipt"] = {
            "path": "Receipts/2026-10-08-local-replay/receipt.json",
            "sha256": sha(ROOT / "Receipts/2026-10-08-local-replay/receipt.json"),
            "status": old["status"],
            "source_bytes_match": True,
        }
        result["source_hashes"] = {}
        for entry in json.loads((ROOT / "source-manifest.json").read_text())["sources"]:
            path = ROOT / "Sources" / Path(entry["path"]).name
            assert sha(path) == entry["sha256"]
            result["source_hashes"][path.name] = sha(path)
        blob = git("show", "HEAD:audit/AXIOM_RECEIPT.txt")
        result["historical_receipt_git_blob_sha256"] = hashlib.sha256(blob).hexdigest()
        assert result["historical_receipt_git_blob_sha256"] == \
            "16ef054d37dd5ec002ce95112f2209558459c5765dd7fb42bb304e47430a1753"
        result["checkout_receipt_differs_only_by_crlf"] = \
            (REPO / "audit/AXIOM_RECEIPT.txt").read_bytes().replace(b"\r\n", b"\n") == blob
        assert result["checkout_receipt_differs_only_by_crlf"]
        source = AREA / "APCIManuscript.lean"
        code = source.read_text(encoding="utf-8")
        assert not re.search(r"\b(sorry|admit|axiom|opaque|unsafe|native_decide|run_tac)\b", code)
        assert re.findall(r"^import (.+)$", code, re.M) == ["APCILeanAudit"]
        assert re.findall(r"^theorem (\w+)", code, re.M) == \
            [name.split(".")[-1] for name in EXPECTED]
        result["source_policy"] = "PASS"
        version = run("lean-version", [str(BIN / "lean.exe"), "--version"])
        assert "version 4.32.1," in version
        env = os.environ.copy()
        env["LEAN_PATH"] = os.pathsep.join([
            str(output), str(REPO / ".lake/build/lib/lean")])
        result["lean_search_path"] = env["LEAN_PATH"]
        receipt = run("compile-and-dependencies", [
            str(BIN / "lean.exe"), "-R", str(AREA), "-j", "1", "-M", "2048",
            "-o", str(output / "APCIManuscript.olean"), str(source)], env)
        actual = dependencies(receipt)
        assert actual == EXPECTED, f"Unexpected logical dependencies: {actual}"
        assert "sorryAx" not in receipt
        result["dependencies"] = actual
        replay = run("bundled-kernel", [str(BIN / "leanchecker.exe"),
                     "--verbose", "APCIManuscript"], env)
        assert "replaying APCIManuscript" in replay, "Target replay not witnessed"
        result["supplement_sha256"] = sha(source)
        result["olean_sha256"] = sha(output / "APCIManuscript.olean")
        result["status"] = "PASS_SUPPLEMENT_AND_SOURCE_ALIGNMENT"
    except Exception as error:
        result["status"] = "FAILED"
        result["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        result["tracked_after"] = snapshot()
        result["git_status_after"] = git("status", "--porcelain").decode()
        result["original_repository_unchanged"] = \
            result["tracked_before"] == result["tracked_after"] and \
            result["git_status_after"] == result["git_status_before"] == ""
        if not result["original_repository_unchanged"]:
            result["status"] = "FAILED_ORIGINAL_REPOSITORY_CHANGED"
        result["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (output / "result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert result["status"] == "PASS_SUPPLEMENT_AND_SOURCE_ALIGNMENT"
    print("PASS: one corollary, three controls; original APCI repository unchanged.")


if __name__ == "__main__":
    main()
