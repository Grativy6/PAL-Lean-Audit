"""Receipt runner for the BRIDGE v0.4 generated-span recovery audit.

This controller deliberately has a fixed input list.  The preceding audit is
checked from its saved receipt; it is not silently replayed as part of this
lane.
"""
from __future__ import annotations

import argparse, copy, hashlib, importlib.util, json, os, platform, re, subprocess, sys, time, zipfile
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
AREA = Path(__file__).resolve().parent
RESULT = AREA / "results.json"
MODULE = "BridgeGeneratedRecovery"
PREDECESSOR = "39433c6817c1d78265ec362dc6ff0c48cae2bb8d"
OPEN = {"O04": "OPEN", "O25": "OPEN", "D-FIRST-OCCURRENCE": "OPEN"}
ALLOWED = {"Classical.choice", "Quot.sound", "propext"}
NEW_FILES = (
    "Audit/bridge-v04-generated-recovery/.gitattributes",
    "Audit/bridge-v04-generated-recovery/README.md",
    "Audit/bridge-v04-generated-recovery/SOURCE-CORRESPONDENCE.md",
    "Audit/bridge-v04-generated-recovery/IMPROVEMENTS.md",
    "Audit/bridge-v04-generated-recovery/REVIEW.md",
    "Audit/bridge-v04-generated-recovery/source-manifest.json",
    "Audit/bridge-v04-generated-recovery/claims.json",
    "Audit/bridge-v04-generated-recovery/IMPLEMENTATION.md",
    "Audit/bridge-v04-generated-recovery/CLOSURE.json",
    "Audit/bridge-v04-generated-recovery/run.py",
    "Audit/bridge-v04-generated-recovery/RECEIPTS.md",
    "Audit/bridge-v04-generated-recovery/predecessor-lock.json",
    "Experiments/BridgeGeneratedRecovery.lean",
    "Experiments/BridgeGeneratedRecoveryAxioms.lean",
    ".github/workflows/bridge-generated-recovery.yml",
)

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

def sha(path, canon=False):
    data = path.read_bytes()
    return hashlib.sha256(data.replace(b"\r\n", b"\n") if canon else data).hexdigest()

def rel(path):
    return path.resolve().relative_to(ROOT).as_posix()

def lean_code(path):
    text = path.read_text(encoding="utf-8")
    # Keep this lexical guard intentionally narrow, matching repository policy.
    from scripts.check_policy import strip_lean_comments_and_strings, OMEGA_LITERAL_IDENTIFIER
    clean = strip_lean_comments_and_strings(text)
    assert not re.search(r"\b(sorry|admit|axiom|native_decide)\b", clean)
    assert not OMEGA_LITERAL_IDENTIFIER.search(clean)
    return clean

def parse_axioms(path, expected):
    rows = re.findall(r"'([^']+)' (does not depend on any axioms|depends on axioms: \[(.*?)\])", path.read_text(encoding="utf-8"), re.S)
    found = {}
    for name, form, listed in rows:
        assert name not in found
        found[name] = [] if form.startswith("does not") else sorted(x.strip() for x in listed.replace("\n", " ").split(",") if x.strip())
        assert set(found[name]) <= ALLOWED
    assert set(found) == set(expected)
    return found

def inventory():
    manifest = read(AREA / "source-manifest.json")
    assert manifest["predecessor_head"] == PREDECESSOR
    source_prior = read(ROOT / "Audit/bridge-v04-dimension-recovery/source-manifest.json")
    for key in ("source_id", "sha256", "bytes", "source_excerpts", "source_excerpts_sha256", "source_context", "source_context_sha256"):
        assert manifest[key] == source_prior[key]
    excerpts = read(ROOT / manifest["source_excerpts"])
    assert sha(ROOT / manifest["source_excerpts"], True) == manifest["source_excerpts_sha256"]
    context = read(ROOT / manifest["source_context"])
    assert sha(ROOT / manifest["source_context"], True) == manifest["source_context_sha256"]
    rows = {x["paragraph"]: x for x in excerpts["paragraphs"] + context["paragraphs"]}
    import xml.etree.ElementTree as ET
    tags = {"{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t", "{http://schemas.openxmlformats.org/officeDocument/2006/math}t"}
    for row in rows.values():
        assert "".join(x.text or "" for x in ET.fromstring(row["ooxml"]).iter() if x.tag in tags) == row["text"]
    assert len(excerpts["paragraphs"]) == 92 and len(context["paragraphs"]) == 3
    assert set(rows) == {f"P{i:04d}" for i in range(108, 200)} | {"P0036", "P0087", "P0107"}
    code = lean_code(ROOT / f"Experiments/{MODULE}.lean")
    decls = [f"Experiments.{MODULE}.{x}" for x in re.findall(r"^(?:noncomputable\s+)?(?:def|theorem|abbrev)\s+(\w+)", code, re.M)]
    claims = read(AREA / "claims.json")
    assert claims["module"] == MODULE and claims["claims"]
    names = [x["declaration"] for x in claims["claims"]]
    assert len(names) == len(set(names)) and set(names) == set(decls)
    printed = re.findall(r"^#print axioms (\S+)", lean_code(ROOT / f"Experiments/{MODULE}Axioms.lean"), re.M)
    assert printed == names
    required = {"id", "title", "classification", "declaration", "statement", "source_refs", "assumptions", "dependencies", "countercase", "authority_ceiling", "residual", "reopening"}
    allowed_classes = {"PROVED_FROM_DECLARED_RULES", "CONSISTENT_REALIZATION", "COUNTERMODEL_TO_OVERCLAIM", "ASSUMPTION_BOUND"}
    assert len({x["id"] for x in claims["claims"]}) == len(claims["claims"])
    for claim in claims["claims"]:
        assert required <= claim.keys() and claim["classification"] in allowed_classes
        assert claim["source_refs"] and all(claim[k] for k in required - {"assumptions", "dependencies"})
        assert isinstance(claim["assumptions"], list) and isinstance(claim["dependencies"], list)
        for ref in claim["source_refs"]:
            assert ref["source_id"] == manifest["source_id"]
            m = re.fullmatch(r"P(\d{4})(?:-P(\d{4}))?", ref["paragraphs"]); assert m
            lo, hi = int(m[1]), int(m[2] or m[1]); assert ((193 <= lo <= hi <= 199) or (lo == hi and lo in {36, 87, 107}))
            source = " ".join(rows[f"P{i:04d}"]["text"] for i in range(lo, hi + 1))
            assert ref["excerpt"].strip() and " ".join(ref["excerpt"].split()) in " ".join(source.split())
    return manifest, claims, names

def inputs():
    lock = read(AREA / "predecessor-lock.json")
    prior = read(ROOT / "Audit/bridge-v04-dimension-recovery/results.json")
    paths = set(prior["inputs"]) | set(lock["frozen_paths"]) | set(NEW_FILES)
    paths.discard("Audit/bridge-v04-generated-recovery/results.json")
    return {p: sha(ROOT / p, True) for p in sorted(paths)}

def predecessor_lock():
    lock = read(AREA / "predecessor-lock.json")
    assert lock["predecessor_head"] == PREDECESSOR
    for path, digest in lock["frozen_paths"].items():
        assert sha(ROOT / path, True) == digest, path
    old = ROOT / "Audit/bridge-v04-dimension-recovery/results.json"
    assert old.exists()
    prior = read(old)
    spec = importlib.util.spec_from_file_location("prior_bridge_runner", ROOT / "Audit/bridge-v04-dimension-recovery/run.py")
    runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)
    assert prior["status"] == "PASS_BRIDGE_DIMENSION_RECOVERY"
    assert runner.check_saved() == prior
    return sha(old)

def raw_source(path, manifest):
    assert path.exists() and path.stat().st_size == manifest["bytes"] and sha(path) == manifest["sha256"]
    with zipfile.ZipFile(path) as archive:
        assert archive.testzip() is None
        xml = archive.read("word/document.xml")
    # Snapshots are evidence, not adoption authority. Compare each parsed
    # paragraph's XML serialization with its preserved source serialization.
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml); ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    paragraphs = root.findall(".//" + ns + "p")
    rows = read(ROOT / manifest["source_excerpts"])["paragraphs"] + read(ROOT / manifest["source_context"])["paragraphs"]
    for row in rows:
        assert ET.tostring(paragraphs[int(row["paragraph"][1:]) - 1], encoding="unicode") == row["ooxml"]
    return True

def summary(receipt):
    counts = Counter(receipt['classifications'].values())
    return "\n".join([
        "# BRIDGE v0.4 generated-span recovery bounded audit", "", f"**{receipt['status']}**", "",
        "One selected source clause: P0195 generated-span recovery, interpreted with P0107. This is not a coverage claim for all BRIDGE.", "",
        "| Formal inventory classification | Declarations |", "|---|---:|",
        *[f"| {name} | {count} |" for name,count in sorted(counts.items())], "",
        f"Total: {len(receipt['declarations'])} declarations, including definitions, equivalent formulations and examples. They share dependencies and are not independent discoveries.",
        "", "One additional unstructured-answer type-checking fixture in the axiom module guards the translation boundary; it is not an additional manuscript claim.",
        "", f"Receipt rejection guards: {len(receipt['receipt_guards'])}. These test the evidence checker and are not mathematical counterexamples.",
        "", "The checked realization separates chosen-answer factorization from full identity recovery and records countercases independently from controller/tooling checks.",
        "", f"All {len(receipt['commands'])} controller commands passed. The predecessor receipt is preserved by hash and checked through its saved receipt.",
        "", "The DOCX and 95 preserved OOXML paragraphs are checked locally when supplied; CI checks committed snapshots only.",
        "", "PAL obligations O04, O25 and D-FIRST-OCCURRENCE remain OPEN.", "",
        "Reproduce: `python Audit/bridge-v04-generated-recovery/run.py --run --lake <lake> --source-file <BRIDGE_v0.4.docx>`; use `--check` for the saved receipt.", ""
    ])

def commands(lake, python, evidence=None):
    out = [
        ("lean-version", [lake, "env", "lean", "--version"]),
        ("build-project", [lake, "build"]),
        ("build-module", [lake, "build", f"Experiments.{MODULE}"]),
        ("generated-axioms", [lake, "env", "lean", f"Experiments/{MODULE}Axioms.lean"]),
        ("generated-kernel", [lake, "env", "leanchecker", f"Experiments.{MODULE}"]),
        ("pal-kernel", [lake, "env", "leanchecker", "PALLeanAudit"]),
        ("prior-saved-check", [python, "Audit/bridge-v04-dimension-recovery/run.py", "--check"]),
        ("policy", [python, "scripts/check_policy.py"]),
        ("migration", [python, "scripts/check_release_migration.py"]),
        ("ar3-policy", [python, "scripts/check_attack_run_0003_policy.py"]),
        ("ar3", [python, "scripts/check_attack_run_0003.py"]),
        ("report", [python, "scripts/render_report.py", "--check"]),
        ("migration-report", [python, "scripts/render_migration_report.py", "--check"]),
        ("ar3-report", [python, "scripts/render_attack_run_0003.py", "--check"]),
        ("diff-check", ["git", "diff", "--check"]),
    ]
    return out

def execute(receipt, directory, timeout=1200):
    for label, argv in commands(receipt["lake"], receipt["python_executable"], directory):
        started = time.monotonic(); print("Running " + label, flush=True)
        try:
            p = subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", timeout=timeout)
            code, output = p.returncode, p.stdout
        except subprocess.TimeoutExpired as exc:
            output = exc.stdout or ""; code = 124; output = (output.decode("utf-8", "replace") if isinstance(output, bytes) else output) + "\nEXECUTION_TIMEOUT\n"
        except OSError as exc:
            code, output = 127, f"EXECUTION_ERROR: {exc}\n"
        log = directory / f"{label}.txt"; log.write_text(output.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
        receipt["commands"].append({"label": label, "argv": argv, "exit_code": code, "log": rel(log), "sha256": sha(log), "elapsed_seconds": round(time.monotonic() - started, 6)})
        if code: raise RuntimeError(f"{label} failed ({code})")

def validate(receipt, manifest, claims, names):
    assert receipt["status"] == "PASS_BRIDGE_GENERATED_RECOVERY"
    assert receipt["inputs"] == inputs() == receipt["input_after"]
    assert receipt["predecessor_head"] == PREDECESSOR and receipt["source_sha256"] == manifest["sha256"]
    assert receipt["predecessor_receipt_sha256"] == sha(ROOT / "Audit/bridge-v04-dimension-recovery/results.json")
    assert receipt["obligations"] == OPEN and receipt["declarations"] == names
    assert receipt["classifications"] == {c["id"]: c["classification"] for c in claims["claims"]}
    evidence = ROOT / receipt["evidence_directory"]
    expected = commands(receipt["lake"], receipt["python_executable"], receipt["evidence_directory"])
    assert len(receipt["commands"]) == len(expected)
    for got, (label, argv) in zip(receipt["commands"], expected):
        assert got["label"] == label and got["argv"] == argv and got["exit_code"] == 0
        assert got["sha256"] == sha(evidence / f"{label}.txt") and got["log"] == receipt["evidence_directory"] + "/" + label + ".txt"
    assert receipt["axioms"] == parse_axioms(evidence / "generated-axioms.txt", names)
    assert receipt["clean_worktree"] == (not bool(receipt["worktree_status"].strip()))
    assert receipt["source_check"] == ({"performed": True, "docx_sha256": manifest["sha256"], "original_ooxml_paragraphs": 95} if receipt["source_check"]["performed"] else {"performed": False, "docx_sha256": None, "original_ooxml_paragraphs": 0})
    assert receipt["scope_status"] == "BOUNDED_GENERATED_SPAN_FACTORISATION"
    assert receipt["mode"] in {"local", "replay"} and re.fullmatch(r"[a-f0-9]{40}", receipt["tested_checkout_sha"])
    if receipt["mode"] == "local":
        assert receipt["ci_status"] == "NOT_RUN" and receipt["github_run_id"] is None and receipt["pr_head_sha"] is None and receipt["tested_merge_sha"] is None
    elif receipt["github_run_id"]:
        assert receipt["ci_status"] == "GITHUB_ACTIONS_REPLAY" and receipt["tested_merge_sha"] == receipt["tested_checkout_sha"] and re.fullmatch(r"[a-f0-9]{40}", receipt["pr_head_sha"] or "") and receipt["clean_worktree"]
        assert re.fullmatch(r"[0-9]+", str(receipt["github_run_id"]))
    else:
        assert receipt["ci_status"] == "LOCAL_REPLAY" and receipt["github_run_id"] is None and receipt["pr_head_sha"] is None and receipt["tested_merge_sha"] is None
    assert all(c["elapsed_seconds"] >= 0 for c in receipt["commands"])

def guards(receipt, manifest, claims, names):
    validate(receipt, manifest, claims, names)
    cases = {
        "missing-command": lambda x: x["commands"].pop(),
        "duplicate-command": lambda x: x["commands"].append(copy.deepcopy(x["commands"][0])),
        "bad-log": lambda x: x["commands"][0].update(sha256="0" * 64),
        "bad-input": lambda x: x["inputs"].update({"lean-toolchain": "0" * 64}),
        "bad-axiom": lambda x: x["axioms"].clear(),
        "bad-source": lambda x: x.update(source_sha256="0" * 64),
        "closed-obligation": lambda x: x["obligations"].update({"O04": "CLOSED"}),
        "promoted-scope": lambda x: x.update(scope_status="BRIDGE_PROVED"),
        "failed-kernel": lambda x: x["commands"][4].update(exit_code=1),
        "bad-declaration": lambda x: x["declarations"].pop(),
        "bad-predecessor-hash": lambda x: x.update(predecessor_receipt_sha256="0" * 64),
        "bad-after-input": lambda x: x["input_after"].update({"lean-toolchain": "0" * 64}),
        "bad-classification": lambda x: x["classifications"].clear(),
        "bad-argv": lambda x: x["commands"][0].update(argv=["wrong"]),
        "falsified-docx": lambda x: x["source_check"].update(performed=not x["source_check"]["performed"]),
        "invented-ci": lambda x: x.update(ci_status="INVENTED_CI"),
        "bad-mode": lambda x: x.update(mode="invented"),
    }
    for label, mutate in cases.items():
        bad = copy.deepcopy(receipt); mutate(bad)
        try: validate(bad, manifest, claims, names)
        except (AssertionError, KeyError): continue
        raise AssertionError("guard accepted " + label)
    return sorted(cases)

def run(args, replay=False):
    manifest, claims, names = inventory(); predecessor = predecessor_lock()
    frozen = check_saved() if replay else None
    if args.source_file: raw_source(args.source_file, manifest)
    directory = (args.output_dir or AREA / "evidence" / datetime.now(timezone.utc).strftime("attempt-%Y%m%dT%H%M%S%fZ")).resolve()
    assert not directory.exists(); directory.mkdir(parents=True)
    checkout = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    ci = bool(replay and os.getenv("GITHUB_RUN_ID"))
    receipt = {"schema_version": "1.0", "status": "RUNNING", "mode": "replay" if replay else "local", "lake": args.lake, "python_executable": sys.executable, "started_utc": datetime.now(timezone.utc).isoformat(), "tested_checkout_sha": checkout, "tested_merge_sha": checkout if ci else None, "pr_head_sha": os.getenv("BRIDGE_GENERATED_PR_HEAD_SHA") if ci else None, "github_run_id": os.getenv("GITHUB_RUN_ID") if ci else None, "platform": platform.platform(), "python": sys.version, "inputs": inputs(), "declarations": names, "classifications": {c["id"]: c["classification"] for c in claims["claims"]}, "obligations": OPEN.copy(), "predecessor_head": PREDECESSOR, "predecessor_receipt_sha256": predecessor, "source_sha256": manifest["sha256"], "source_check": {"performed": bool(args.source_file), "docx_sha256": manifest["sha256"] if args.source_file else None, "original_ooxml_paragraphs": 95 if args.source_file else 0}, "scope_status": "BOUNDED_GENERATED_SPAN_FACTORISATION", "evidence_directory": rel(directory), "commands": [], "axioms": [], "ci_status": "GITHUB_ACTIONS_REPLAY" if ci else "LOCAL_REPLAY" if replay else "NOT_RUN"}
    try:
        execute(receipt, directory)
        receipt["axioms"] = parse_axioms(directory / "generated-axioms.txt", names)
        if frozen is not None:
            assert receipt["declarations"] == frozen["declarations"] and receipt["axioms"] == frozen["axioms"]
        receipt["input_after"] = inputs(); receipt["worktree_status"] = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True); receipt["clean_worktree"] = not bool(receipt["worktree_status"].strip()); receipt["status"] = "PASS_BRIDGE_GENERATED_RECOVERY"; receipt["receipt_guards"] = guards(receipt, manifest, claims, names)
    except Exception as exc:
        receipt["status"] = "FAILED_BRIDGE_GENERATED_RECOVERY"; receipt["error"] = str(exc); raise
    finally:
        receipt["finished_utc"] = datetime.now(timezone.utc).isoformat(); receipt.setdefault("input_after", inputs()); receipt.setdefault("worktree_status", subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)); receipt.setdefault("clean_worktree", not bool(receipt["worktree_status"].strip())); write(directory / "execution.json", receipt)
    if not replay:
        write(RESULT, receipt)
        (AREA / "SUMMARY.md").write_text(summary(receipt), encoding="utf-8", newline="\n")
    print(receipt["status"])

def check_saved():
    manifest, claims, names = inventory(); predecessor_lock(); receipt = read(RESULT); validate(receipt, manifest, claims, names); assert receipt["receipt_guards"] == guards(receipt, manifest, claims, names); assert read(ROOT / receipt["evidence_directory"] / "execution.json") == receipt
    assert (AREA / "SUMMARY.md").read_text(encoding="utf-8") == summary(receipt)
    return receipt

def main():
    p = argparse.ArgumentParser(); m = p.add_mutually_exclusive_group(required=True); m.add_argument("--run", action="store_true"); m.add_argument("--check", action="store_true"); m.add_argument("--replay", action="store_true"); m.add_argument("--check-inputs", action="store_true"); p.add_argument("--lake", default="lake"); p.add_argument("--output-dir", type=Path); p.add_argument("--source-file", type=Path); a = p.parse_args()
    if a.check or a.check_inputs:
        inventory(); predecessor_lock(); inputs();
        if a.source_file: raw_source(a.source_file, read(AREA / "source-manifest.json"))
        check_saved() if a.check else None; print("PASS_BRIDGE_GENERATED_RECOVERY_RECEIPTS" if a.check else "PASS_BRIDGE_GENERATED_RECOVERY_INPUTS")
    else: run(a, a.replay)

if __name__ == "__main__": main()
