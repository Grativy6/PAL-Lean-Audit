"""Sequential local Lean receipt checks for the three selected Abstract Loops batches."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

AREA = Path(__file__).resolve().parent
ROOT = AREA.parents[1]
LAKE = Path(r"C:\Users\cdpan\.elan\bin\lake.exe")
ALLOWED = {"propext", "Quot.sound", "Classical.choice"}
MODULES = {"AL-A": "AbstractLoopsFiniteImage", "AL-B": "AbstractLoopsDynamics",
           "AL-C": "AbstractLoopsReturnExport"}
DECL = re.compile(r"^(?:noncomputable )?(def|theorem|inductive|structure) ([A-Za-z_][A-Za-z0-9_]*)", re.M)
FORBIDDEN = re.compile(r"\b(sorry|admit|axiom|unsafe|native_decide|run_tac|implemented_by|extern)\b")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()

def run(argv, directory, label):
    start = time.monotonic()
    p = subprocess.run(list(map(str, argv)), cwd=ROOT, capture_output=True, timeout=600)
    out, err = directory / (label + ".stdout.txt"), directory / (label + ".stderr.txt")
    out.write_bytes(p.stdout)
    err.write_bytes(p.stderr)
    return {"label": label, "argv": list(map(str, argv)), "cwd": str(ROOT),
            "exit_code": p.returncode, "elapsed_seconds": time.monotonic() - start,
            "stdout": relative(out), "stdout_sha256": sha(out),
            "stderr": relative(err), "stderr_sha256": sha(err)}

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, encoding="utf-8").strip()

spec = importlib.util.spec_from_file_location("policy", ROOT / "scripts/check_policy.py")
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)

def inventory(module):
    path = ROOT / "Experiments" / (module + ".lean")
    code = policy.strip_lean_comments_and_strings(path.read_text(encoding="utf-8"))
    if FORBIDDEN.search(code):
        raise ValueError("Unacceptable proof escape or axiom in " + relative(path))
    if policy.omega_literal_diagnostics(path, path.read_text(encoding="utf-8")):
        raise ValueError("Literal Omega identifier in " + relative(path))
    return [{"name": "Experiments." + module + "." + name, "kind": kind}
            for kind, name in DECL.findall(code)]

def inputs(batch):
    module = MODULES[batch]
    paths = [Path(__file__), AREA / "source-manifest.json", AREA / "TARGETS.md",
             AREA / batch / "claims.json", ROOT / "scripts/check_policy.py",
             ROOT / "lean-toolchain", ROOT / "lakefile.lean", ROOT / "lake-manifest.json",
             ROOT / "Experiments" / (module + ".lean"),
             ROOT / "Experiments" / (module + "Axioms.lean"),
             ROOT / "Experiments/AbstractLoopsJoint.lean"]
    if batch != "AL-B":
        paths.append(ROOT / "Experiments/AbstractLoopsPostprocessing.lean")
    manifest = read(AREA / "source-manifest.json")
    for row in manifest["inputs"]:
        p = (ROOT / row["path"]).resolve()
        if not p.is_relative_to(ROOT.parent):
            raise ValueError("Source path leaves the authorized personal math home")
        if sha(p) != row["sha256"]:
            raise ValueError("Source hash mismatch: " + row["path"])
        paths.append(p)
    return {str(p.resolve()): sha(p) for p in paths}

def inspections(text, names):
    headers = list(re.finditer(r"^@?(" + "|".join(map(re.escape, names)) +
                              r")(?:\.\{[^}]+\})?\s*:", text, re.M))
    if [m.group(1) for m in headers] != names:
        raise ValueError("Printed signature inventory differs from declaration ledger")
    axrows = re.findall(r"'([^']+)' (does not depend on any axioms|depends on axioms: \[(.*?)\])",
                        text, re.S)
    if [row[0] for row in axrows] != names:
        raise ValueError("Printed axiom inventory differs from declaration ledger")
    axioms = {name: ([] if form.startswith("does not") else
                     sorted(x.strip() for x in raw.replace("\n", " ").split(",") if x.strip()))
              for name, form, raw in axrows}
    if any(set(v) - ALLOWED for v in axioms.values()):
        raise ValueError("Unexpected axiom dependency")
    signatures = {}
    for i, match in enumerate(headers):
        stop = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        signatures[names[i]] = text[match.start():stop].split("'" + names[i] + "'")[0].strip()
    return signatures, axioms

def validate_structure(receipt, declared, signatures, axioms):
    if receipt["status"] != "PASS_BOUNDED_LEAN_CHECKS":
        raise ValueError("Not a passing receipt")
    if receipt["declarations"] != declared or receipt["signatures"] != signatures or receipt["axioms"] != axioms:
        raise ValueError("Receipt inventory does not match actual declarations and inspection")
    if receipt["input_hashes_before"] != receipt["input_hashes_after"]:
        raise ValueError("Inputs changed during run")
    module = "Experiments." + MODULES[receipt["batch"]]
    expected = [
        ("lean-version", [str(LAKE), "env", "lean", "--version"]),
        ("build", [str(LAKE), "build", module]),
        ("inspect", [str(LAKE), "env", "lean", str(ROOT / "Experiments" / (MODULES[receipt["batch"]] + "Axioms.lean"))]),
        ("kernel", [str(LAKE), "env", "leanchecker", module]),
    ]
    if len(receipt["commands"]) != len(expected):
        raise ValueError("Incomplete command sequence")
    for row, (label, argv) in zip(receipt["commands"], expected):
        if row["label"] != label or row["argv"] != argv or row["cwd"] != str(ROOT) or row["exit_code"] != 0:
            raise ValueError("Command identity or status mismatch")
    if any(set(v) - ALLOWED for v in axioms.values()):
        raise ValueError("Unlisted axioms")

def check(batch):
    receipt = read(AREA / batch / "results.json")
    current = inputs(batch)
    if current != receipt["input_hashes_after"]:
        raise ValueError("Current inputs differ from the final receipt")
    for row in receipt["commands"]:
        for stream in ("stdout", "stderr"):
            if sha(ROOT / row[stream]) != row[stream + "_sha256"]:
                raise ValueError("Changed command output")
    for filename, digest in receipt["compiled_artifacts"].items():
        if sha(Path(filename)) != digest:
            raise ValueError("Changed compiled artifact")
    declared = inventory(MODULES[batch])
    ledger = read(AREA / batch / "claims.json")
    if [{k: r[k] for k in ("name", "kind")} for r in ledger["declarations"]] != declared:
        raise ValueError("Ledger no longer matches source")
    signatures, axioms = inspections((ROOT / receipt["commands"][2]["stdout"]).read_text(encoding="utf-8"),
                                    [row["name"] for row in declared])
    validate_structure(receipt, declared, signatures, axioms)
    print("PASS_SAVED_RECEIPT_CHECK", batch, "(no Lean rerun)")

def execute(batch):
    module = MODULES[batch]
    declared = inventory(module)
    ledger = read(AREA / batch / "claims.json")
    if [{k: r[k] for k in ("name", "kind")} for r in ledger["declarations"]] != declared:
        raise ValueError("Ledger must list every explicit declaration in source order")
    ax = ROOT / "Experiments" / (module + "Axioms.lean")
    axtext = ax.read_text(encoding="utf-8")
    names = [r["name"] for r in declared]
    if re.findall(r"^#check @?(\S+)", axtext, re.M) != names or re.findall(r"^#print axioms (\S+)", axtext, re.M) != names:
        raise ValueError("Axiom inspection source inventory mismatch")
    if FORBIDDEN.search(policy.strip_lean_comments_and_strings(axtext)):
        raise ValueError("Proof escape in inspection source")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    directory = AREA / batch / "evidence" / stamp
    directory.mkdir(parents=True)
    before = inputs(batch)
    mathlib = git("-C", ".lake/packages/mathlib", "rev-parse", "HEAD")
    if mathlib != read(AREA / "source-manifest.json")["mathlib_commit"]:
        raise ValueError("Mathlib revision differs from the key")
    mathlib_dirty = git("-C", ".lake/packages/mathlib", "status", "--porcelain")
    if mathlib_dirty:
        raise ValueError("Mathlib contains local modifications")
    receipt = {"schema": "abstract-loops-local-lean-receipt-v1", "batch": batch,
               "status": "RUNNING", "started_utc": stamp, "branch": git("branch", "--show-current"),
               "git_head": git("rev-parse", "HEAD"), "working_tree": git("status", "--porcelain"),
               "mathlib_commit": mathlib, "mathlib_dirty": mathlib_dirty,
               "python": sys.version, "declarations": declared, "input_hashes_before": before,
               "commands": [], "signatures": {}, "axioms": {}, "compiled_artifacts": {},
               "review": "self-review; bundled checker is not an independent implementation",
               "authority": "local bounded proof evidence; no manuscript adoption or publication"}
    write(directory / "receipt.json", receipt)
    try:
        for label, argv in [
            ("lean-version", [LAKE, "env", "lean", "--version"]),
            ("build", [LAKE, "build", "Experiments." + module]),
            ("inspect", [LAKE, "env", "lean", ax]),
            ("kernel", [LAKE, "env", "leanchecker", "Experiments." + module]),
        ]:
            row = run(argv, directory, label)
            receipt["commands"].append(row)
            write(directory / "receipt.json", receipt)
            print(batch, label, "exit", row["exit_code"], flush=True)
            if row["exit_code"] != 0:
                raise RuntimeError(label + " failed; see retained logs")
        text = (ROOT / receipt["commands"][2]["stdout"]).read_text(encoding="utf-8")
        receipt["signatures"], receipt["axioms"] = inspections(text, names)
        receipt["input_hashes_after"] = inputs(batch)
        artifact = ROOT / ".lake/build/lib/lean/Experiments" / (module + ".olean")
        receipt["compiled_artifacts"][str(artifact)] = sha(artifact)
        receipt["status"] = "PASS_BOUNDED_LEAN_CHECKS"
        validate_structure(receipt, declared, receipt["signatures"], receipt["axioms"])
    except Exception as exc:
        receipt["status"] = "FAILED_OR_BLOCKED"
        receipt["error"] = repr(exc)
        write(directory / "receipt.json", receipt)
        raise
    write(directory / "receipt.json", receipt)
    write(AREA / batch / "results.json", receipt)
    check(batch)

def self_test():
    # Ensure missing/reordered commands, altered signatures, unlisted axioms and changed inputs fail.
    module = MODULES["AL-A"]
    names = [r["name"] for r in inventory(module)]
    receipt = read(AREA / "AL-A/results.json")
    sig, axioms = inspections((ROOT / receipt["commands"][2]["stdout"]).read_text(encoding="utf-8"), names)
    mutations = [lambda r: r["commands"].pop(), lambda r: r["commands"].reverse(),
                 lambda r: r["commands"][1].update(exit_code=1),
                 lambda r: r["signatures"].update({names[0]: "False"}),
                 lambda r: r["axioms"].update({names[0]: ["sorryAx"]}),
                 lambda r: r["input_hashes_after"].clear()]
    for mutate in mutations:
        copy = json.loads(json.dumps(receipt)); mutate(copy)
        try:
            validate_structure(copy, inventory(module), sig, axioms)
        except ValueError:
            continue
        raise AssertionError("Receipt mutation was not rejected")
    print("PASS_RECEIPT_MUTATION_CONTROLS", len(mutations))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", choices=MODULES)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.batch:
        (check if args.check else execute)(args.batch)
    else:
        parser.error("Choose --batch or --self-test")
