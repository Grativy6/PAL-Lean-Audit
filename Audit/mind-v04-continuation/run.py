"""Source-bound Lean 4 continuation receipt runner for the MIND v0.4 draft."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
AREA = Path(__file__).resolve().parent
RESULT = AREA / "results.json"
BASE_COMMIT = "93d9c7811e833b57367d1939c862b08fd8d187bb"
SOURCE_SHA256 = "7c84265b3dbb05dc9846afb78539d73e8eec4dd262578f43a2bc8e604fb534ad"
MODULE = "Experiments.MindContinuation"
MODULE_FILE = "Experiments/MindContinuation.lean"
AXIOMS_FILE = "Experiments/MindContinuationAxioms.lean"
LEDGER_FILE = "Audit/mind-v04-continuation/claims.json"
MANIFEST_FILE = "Audit/mind-v04-continuation/source-manifest.json"
EXCERPTS_FILE = "Audit/mind-v04-continuation/source-excerpts.json"
EXPLICIT_INPUTS = (
    ".gitattributes", "lean-toolchain", "lakefile.lean", "lake-manifest.json",
    "Audit/mind-v04-continuation/.gitattributes",
    "Audit/mind-v04-continuation/run.py",
    "Audit/mind-v04-continuation/README.md",
    "Audit/mind-v04-continuation/SOURCE-CORRESPONDENCE.md",
    "Audit/mind-v04-continuation/REVIEW.md",
    MANIFEST_FILE, EXCERPTS_FILE, LEDGER_FILE, MODULE_FILE, AXIOMS_FILE,
    ".github/workflows/mind-continuation.yml",
    "scripts/check_policy.py", "scripts/check_release_migration.py",
    "scripts/check_attack_run_0003_policy.py", "scripts/check_attack_run_0003.py",
    "scripts/render_report.py", "scripts/render_migration_report.py",
    "scripts/render_attack_run_0003.py",
)
DECL_KINDS = {"def", "theorem", "abbrev", "opaque", "inductive", "structure", "class"}
CLASSIFICATIONS = {
    "PROVED_FROM_DECLARED_RULES", "CONSISTENT_REALIZATION", "ASSUMPTION_BOUND",
    "COUNTERMODEL_TO_OVERCLAIM",
}
ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}
FORBIDDEN = re.compile(r"\b(sorry|admit|axiom|native_decide)\b")
OMEGA = re.compile(r"(?<![\w'])Omega(?![\w'])|(?<![\w'])Ω(?![\w'])")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="")
    temp.replace(path)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(text: str) -> str:
    return " ".join(text.split())


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def checkout_state():
    return git("rev-parse", "HEAD"), git("status", "--porcelain")


def tracked_input_paths() -> list[str]:
    """Conservatively cover code and data read by the recorded baseline checks."""
    raw = subprocess.check_output([
        "git", "ls-files", "-z", "--", "*.lean", "Audit", "scripts",
        "docs/generated", ".github/workflows", "AGENTS.md", "docs/REPORTING.md",
        ".gitignore",
    ], cwd=ROOT)
    paths = {part.decode("utf-8") for part in raw.split(b"\0") if part}
    # Policy scans and Lake can see local Lean files before they are staged.
    # Include them so a dirty local run is bound to their contents as well.
    for dirname in ("PAL", "Audit", "Experiments"):
        paths.update(rel(path) for path in (ROOT / dirname).rglob("*.lean") if path.is_file())
    paths.update(rel(path) for path in ROOT.glob("*.lean") if path.is_file())
    # The new receipt is an output. Historical receipts remain frozen inputs.
    paths.discard("Audit/mind-v04-continuation/results.json")
    paths.update((MODULE_FILE, AXIOMS_FILE))
    return sorted(paths)


def input_hashes() -> tuple[dict[str, str], dict[str, str]]:
    """Return exact checkout hashes and CRLF-to-LF hashes for cross-OS comparison."""
    paths = sorted(set(EXPLICIT_INPUTS) | set(tracked_input_paths()))
    raw_hashes, canonical_hashes = {}, {}
    for name in paths:
        path = ROOT / name
        if not path.is_file():
            raise FileNotFoundError(f"required input missing: {name}")
        raw = path.read_bytes()
        raw_hashes[name] = hashlib.sha256(raw).hexdigest()
        canonical_hashes[name] = hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()
    return raw_hashes, canonical_hashes


def load_source():
    manifest = read_json(ROOT / MANIFEST_FILE)
    assert manifest["source_id"] and manifest["source_in_repository"] is False
    assert manifest["base_commit"] == BASE_COMMIT
    assert manifest["filename"] == "MIND_v0.4_Draft.pdf"
    assert manifest["sha256"] == SOURCE_SHA256
    assert isinstance(manifest["bytes"], int) and manifest["bytes"] > 0
    assert isinstance(manifest["pages"], int) and manifest["pages"] > 0
    assert manifest["identity_basis"] and manifest["authority_ceiling"]
    snapshot = read_json(ROOT / EXCERPTS_FILE)
    assert snapshot["source_id"] == manifest["source_id"]
    assert snapshot["source_sha256"] == manifest["sha256"]
    rows = snapshot["excerpts"]
    assert rows and len({row["id"] for row in rows}) == len(rows)
    for row in rows:
        assert isinstance(row["page"], int) and 1 <= row["page"] <= manifest["pages"]
        assert row["section"] and row["text"].strip()
    return manifest, snapshot


def verify_source_pdf(pdf: Path, manifest, snapshot):
    pdf = pdf.resolve()
    assert pdf.is_file() and pdf.stat().st_size == manifest["bytes"]
    assert sha(pdf) == manifest["sha256"] == SOURCE_SHA256
    try:
        from pypdf import PdfReader, __version__ as pypdf_version
    except ImportError as exc:
        raise RuntimeError("pypdf is required for --source-pdf verification") from exc
    reader = PdfReader(str(pdf))
    assert len(reader.pages) == manifest["pages"]
    for row in snapshot["excerpts"]:
        page = canonical(reader.pages[row["page"] - 1].extract_text() or "")
        assert canonical(row["text"]) in page, (row["id"], row["page"], row["section"])
    return {
        "performed": True, "filename": pdf.name, "sha256": sha(pdf),
        "bytes": pdf.stat().st_size, "pages": len(reader.pages),
        "matched_excerpt_ids": [row["id"] for row in snapshot["excerpts"]],
        "extractor": {"name": "pypdf", "version": pypdf_version},
    }


def clean_lean(path: Path) -> str:
    from scripts.check_policy import strip_lean_comments_and_strings
    text = strip_lean_comments_and_strings(path.read_text(encoding="utf-8"))
    assert not FORBIDDEN.search(text), f"forbidden Lean construct in {rel(path)}"
    assert not OMEGA.search(text), f"literal Omega identifier in {rel(path)}"
    return text


def source_declarations():
    text = clean_lean(ROOT / MODULE_FILE)
    pattern = re.compile(
        r"^(?:(?:private|protected|noncomputable|partial|unsafe)\s+)*"
        r"(def|theorem|abbrev|opaque|inductive|structure|class)\s+([A-Za-z_][A-Za-z0-9_'.]*)",
        re.MULTILINE,
    )
    names, kinds = [], {}
    for kind, name in pattern.findall(text):
        full = f"{MODULE}.{name}"
        assert full not in kinds, f"duplicate declaration: {full}"
        names.append(full)
        kinds[full] = kind
    return names, kinds


def validate_ledger():
    manifest, snapshot = load_source()
    names, kinds = source_declarations()
    ledger = read_json(ROOT / LEDGER_FILE)
    assert ledger["module"] == MODULE and ledger["source_id"] == manifest["source_id"]
    claims = ledger["claims"]
    assert claims
    claim_ids = [claim["id"] for claim in claims]
    declared = [claim["declaration"] for claim in claims]
    assert len(claim_ids) == len(set(claim_ids))
    assert len(declared) == len(set(declared)) and declared == names
    required = {
        "id", "declaration", "kind", "classification", "statement", "source_refs",
        "assumptions", "dependencies", "countercase", "authority_ceiling", "residual", "reopening",
        "expected_axioms", "expected_signature",
    }
    excerpt_ids = {row["id"] for row in snapshot["excerpts"]}
    for claim in claims:
        assert required <= claim.keys()
        assert claim["kind"] == kinds[claim["declaration"]]
        assert claim["classification"] in CLASSIFICATIONS
        assert all(claim[key] for key in required - {"assumptions", "dependencies", "expected_axioms"})
        assert isinstance(claim["assumptions"], list) and isinstance(claim["dependencies"], list)
        assert isinstance(claim["expected_axioms"], list)
        assert set(claim["expected_axioms"]) <= ALLOWED_AXIOMS
        assert claim["expected_signature"].lstrip("@").startswith(claim["declaration"] + " :")
        refs = claim["source_refs"]
        assert isinstance(refs, list) and refs
        assert all(isinstance(ref, str) and ref in excerpt_ids for ref in refs)
    return manifest, snapshot, ledger, claims, names, kinds


def validate_axiom_source(names):
    text = clean_lean(ROOT / AXIOMS_FILE)
    checked = re.findall(r"^#check\s+@?(\S+)", text, re.MULTILINE)
    printed = re.findall(r"^#print axioms\s+(\S+)", text, re.MULTILINE)
    assert checked == names and printed == names


def validate_static():
    manifest, snapshot, ledger, claims, names, kinds = validate_ledger()
    validate_axiom_source(names)
    head = git("rev-parse", "HEAD")
    ancestry = subprocess.run(["git", "merge-base", "--is-ancestor", BASE_COMMIT, head], cwd=ROOT)
    assert ancestry.returncode == 0, f"base revision {BASE_COMMIT} is not an ancestor of {head}"
    return manifest, snapshot, ledger, claims, names, kinds, input_hashes()


def parse_axioms_text(text: str, names):
    rows = re.findall(
        r"'([^']+)' (does not depend on any axioms|depends on axioms: \[(.*?)\])",
        text, re.DOTALL,
    )
    result = {}
    for name, form, raw in rows:
        assert name not in result
        axioms = [] if form.startswith("does not") else sorted(
            x.strip() for x in raw.replace("\n", " ").split(",") if x.strip()
        )
        assert set(axioms) <= ALLOWED_AXIOMS, (name, axioms)
        result[name] = axioms
    assert list(result) == names
    return result


def parse_signatures_text(text: str, names):
    escaped = "|".join(re.escape(name) for name in names)
    # A body line can also start with an inventoried function name. Only a
    # name followed by the declaration's type separator is an inspection header.
    headers = list(re.finditer(r"^@?(" + escaped + r")(?:\.\{[^}]+\})?[ \t]*:", text, re.MULTILINE))
    assert [match.group(1) for match in headers] == names, (
        "Signature inspection must print every fully qualified declaration in ledger order. "
        "Place #check commands outside namespaces or use full-name pretty printing."
    )
    axioms = re.compile(r"^'[^']+' (?:does not depend on any axioms|depends on axioms:)", re.MULTILINE)
    result = {}
    for index, match in enumerate(headers):
        stop = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        axiom_line = axioms.search(text, match.end(), stop)
        end = axiom_line.start() if axiom_line else stop
        result[names[index]] = text[match.start():end].strip()
        assert result[names[index]]
    return result


def parse_axioms(path: Path, names):
    return parse_axioms_text(path.read_text(encoding="utf-8"), names)


def parse_signatures(path: Path, names):
    return parse_signatures_text(path.read_text(encoding="utf-8"), names)


def commands(lake, python):
    return [
        ("lean-version", [lake, "env", "lean", "--version"]),
        ("lake-version", [lake, "--version"]),
        ("target-build", [lake, "build", MODULE]),
        ("whole-project-build", [lake, "build"]),
        ("axioms-signatures", [lake, "env", "lean", AXIOMS_FILE]),
        ("continuation-kernel", [lake, "env", "leanchecker", MODULE]),
        ("pal-kernel", [lake, "env", "leanchecker", "PALLeanAudit"]),
        ("policy", [python, "scripts/check_policy.py"]),
        ("migration-policy", [python, "scripts/check_release_migration.py"]),
        ("attack-run-policy", [python, "scripts/check_attack_run_0003_policy.py"]),
        ("attack-run", [python, "scripts/check_attack_run_0003.py"]),
        ("generated-report", [python, "scripts/render_report.py", "--check"]),
        ("migration-report", [python, "scripts/render_migration_report.py", "--check"]),
        ("attack-run-report", [python, "scripts/render_attack_run_0003.py", "--check"]),
        ("diff-check", ["git", "diff", "--check", "HEAD"]),
    ]


def ensure_ignored_output(path: Path):
    target = path.resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError("--output-dir must be inside this repository's ignored artifacts directory")
    probe = target / ".mind-continuation-ignore-probe"
    check = subprocess.run(["git", "check-ignore", "-q", str(probe)], cwd=ROOT, check=False)
    if check.returncode:
        raise ValueError("--output-dir must be ignored by Git (for example artifacts/mind-continuation-local)")
    target.mkdir(parents=True, exist_ok=True)
    if any(target.iterdir()):
        raise ValueError("--output-dir must be empty so this replay cannot overwrite prior evidence")
    return target


def validate_receipt(receipt, manifest, snapshot, claims, names, hashes_canonical):
    assert receipt["status"] == "PASS_MIND_V04_CONTINUATION"
    assert receipt["scope_status"] == "BOUNDED_MIND_V04_CONTINUATION"
    assert receipt["authority_ceiling"] == manifest["authority_ceiling"]
    assert receipt["base_commit"] == BASE_COMMIT == manifest["base_commit"]
    assert receipt["source_id"] == manifest["source_id"]
    assert receipt["source_sha256"] == manifest["sha256"] == SOURCE_SHA256
    assert receipt["input_hashes_canonical_before"] == hashes_canonical == receipt["input_hashes_canonical_after"]
    assert receipt["input_hashes_before"] == receipt["input_hashes_after"]
    assert set(receipt["input_hashes_before"]) == set(hashes_canonical)
    assert all(re.fullmatch(r"[a-f0-9]{64}", value) for value in receipt["input_hashes_before"].values())
    assert receipt["declarations"] == names
    assert receipt["module_declarations"] == {MODULE: names}
    assert receipt["classifications"] == {claim["id"]: claim["classification"] for claim in claims}
    assert list(receipt["axioms"]) == names and list(receipt["signatures"]) == names
    assert all(set(items) <= ALLOWED_AXIOMS for items in receipt["axioms"].values())
    assert receipt["axioms"] == {row["declaration"]: row["expected_axioms"] for row in claims}
    assert receipt["signatures"] == {row["declaration"]: row["expected_signature"] for row in claims}
    source_check = receipt["source_check"]
    assert isinstance(source_check["performed"], bool)
    if source_check["performed"]:
        assert source_check["sha256"] == SOURCE_SHA256
        assert source_check["bytes"] == manifest["bytes"]
        assert source_check["pages"] == manifest["pages"]
        assert source_check["filename"] == manifest["filename"]
        assert source_check["matched_excerpt_ids"] == [row["id"] for row in snapshot["excerpts"]]
        assert receipt["source_pdf_sha256_before"] == receipt["source_pdf_sha256_after"] == SOURCE_SHA256
        assert re.fullmatch(r"[a-f0-9]{64}", receipt["source_verification_sha256"])
        assert receipt["source_pdf_status"] == "LOCAL_VERIFIED"
    else:
        assert receipt["source_pdf_sha256_before"] is None
        assert receipt["source_pdf_sha256_after"] is None
        assert receipt["source_verification_sha256"] is None
        assert receipt["source_pdf_status"] == ("UNAVAILABLE_IN_CI" if receipt["ci"]["claimed"] else "NOT_SUPPLIED")
    assert receipt["mode"] == "replay"
    assert receipt["elapsed_seconds"] >= 0 and receipt["exit_status"] == 0
    assert len(receipt["commands"]) == len(commands(receipt["lake"], receipt["python_executable"]))
    expected_commands = commands(receipt["lake"], receipt["python_executable"])
    for record, (label, argv) in zip(receipt["commands"], expected_commands):
        assert record["label"] == label and record["argv"] == argv
        assert record["exit_code"] == 0 and record["elapsed_seconds"] >= 0
        assert re.fullmatch(r"[a-f0-9]{64}", record["sha256"])
        log_path = ROOT / record["log"]
        if log_path.is_file():
            assert sha(log_path) == record["sha256"]
    inspection = receipt["axiom_inspection_stdout"]
    assert isinstance(inspection, str) and inspection
    inspection_record = next(row for row in receipt["commands"] if row["label"] == "axioms-signatures")
    assert hashlib.sha256(inspection.encode("utf-8")).hexdigest() == inspection_record["sha256"]
    assert receipt["axioms"] == parse_axioms_text(inspection, names)
    assert receipt["signatures"] == parse_signatures_text(inspection, names)
    assert re.fullmatch(r"[a-f0-9]{40}", receipt["tested_commit"])
    ci = receipt["ci"]
    if ci["claimed"]:
        assert ci["environment_source"] == "GITHUB_ACTIONS environment variables; not independently attested"
        assert isinstance(ci["run_id"], str) and ci["run_id"]
        assert ci["merge_sha"] == receipt["tested_commit"]
        assert re.fullmatch(r"[a-f0-9]{40}", ci["head_sha"] or "")
        assert receipt["dirty_before"] is False
        assert receipt["dirty_after"] is False
    else:
        assert ci["merge_sha"] is None and ci["head_sha"] is None
    assert receipt["dirty_before"] == bool(receipt["worktree_status_before"])
    assert receipt["dirty_after"] == bool(receipt["worktree_status_after"])
    software = {row["name"]: row["version"] for row in receipt["environment"]["software"]}
    assert all(software.get(name) for name in ("Python", "Lean", "Lake"))
    if "computation_manifest_sha256" in receipt:
        assert re.fullmatch(r"[a-f0-9]{64}", receipt["computation_manifest_sha256"])
        execution_manifest = ROOT / receipt["execution_manifest_path"]
        if execution_manifest.is_file():
            assert sha(execution_manifest) == receipt["computation_manifest_sha256"]
    if source_check["performed"]:
        source_artifact = ROOT / receipt["evidence_directory"] / "source-verification.json"
        if source_artifact.is_file():
            assert sha(source_artifact) == receipt["source_verification_sha256"]
            assert read_json(source_artifact) == source_check


def validate_guards(receipt, manifest, snapshot, claims, names, hashes_canonical):
    validate_receipt(receipt, manifest, snapshot, claims, names, hashes_canonical)
    probes = {
        "removed-declaration": lambda x: x["declarations"].pop(),
        "forbidden-axiom": lambda x: x["axioms"][names[0]].append("sorryAx"),
        "wrong-source": lambda x: x.update(source_sha256="0" * 64),
        "changed-input": lambda x: x["input_hashes_canonical_after"].update({"lean-toolchain": "0" * 64}),
        "wrong-status": lambda x: x.update(status="FAILED"),
        "changed-signature": lambda x: x["signatures"].update({names[0]: names[0] + " : False"}),
        "added-allowed-axiom": lambda x: x["axioms"][names[0]].append("Classical.choice"),
    }
    passed = []
    for name, mutate in probes.items():
        candidate = copy.deepcopy(receipt)
        mutate(candidate)
        try:
            validate_receipt(candidate, manifest, snapshot, claims, names, hashes_canonical)
        except (AssertionError, KeyError, TypeError, ValueError):
            passed.append(name)
        else:
            raise AssertionError(f"receipt mutation guard failed to reject {name}")
    return passed


def make_computation_manifest(receipt):
    outcome = "completed" if receipt["status"] == "PASS_MIND_V04_CONTINUATION" else "failed"
    return {
        "schema_version": 1,
        "claim_id": "MIND-v0.4-continuation-formalization",
        "repository": {"commit": receipt["tested_commit"], "dirty": receipt["dirty_before"]},
        "command": "Sequential Lean build, signature and axiom inspection, kernel checks, and repository policy/report checks; consult per-command argv and logs.",
        "environment": {"software": receipt["environment"]["software"], "hardware": "Platform: " + receipt["environment"]["platform"]},
        "mathematics": {
            "assertion_tested": "The finite MIND continuation model elaborates and its listed declarations pass the Lean kernel checker with the recorded imported-axiom inventory.",
            "coefficient_domain": "Lean 4 type theory with the explicit types in Experiments.MindContinuation.",
            "conventions": "Pinned Lean toolchain; imported axioms are restricted to propext, Quot.sound, and Classical.choice.",
            "inputs": ([{"path": name, "sha256": digest, "hash_convention": "CRLF normalized to LF"} for name, digest in receipt["input_hashes_canonical_before"].items()]
                       + ([{"path": "MIND_v0.4_Draft.pdf (local-only; excluded from repository)",
                            "sha256": receipt["source_pdf_sha256_before"]}]
                          if receipt["source_check"]["performed"] else [])),
            "bounds": {"explicit_declarations": len(receipt["declarations"]), "module": MODULE,
                       "proof_domain": "Arbitrary finite queues in the quantified theorems; exact closed fixtures as inventoried. Symbolic kernel checking, not sampled enumeration."},
            "non_claims": [
                "This reduced finite formalization does not prove the source PDF, MIND in full, or empirical or physical interpretations.",
                "A successful build and kernel check do not confer adoption, authority, or closure of source questions.",
                "CI identity values are supplied by the environment and are not independently attested by this runner.",
            ],
        },
        "randomness": {"used": False, "generator": "", "seed": None},
        "run": {"started_at": receipt["started_at"], "runtime_seconds": receipt["elapsed_seconds"], "exit_status": receipt["exit_status"]},
        "outputs": ([{"path": row["log"], "sha256": row["sha256"]} for row in receipt["commands"]]
                    + ([{"path": receipt["evidence_directory"] + "/source-verification.json",
                         "sha256": receipt["source_verification_sha256"]}]
                       if receipt["source_check"]["performed"] else [])),
        "checks": [f"{row['label']}: exit={row['exit_code']} elapsed={row['elapsed_seconds']} seconds" for row in receipt["commands"]],
        "result": "All recorded commands passed and source declarations, signatures, and axiom inventory matched the frozen ledger." if outcome == "completed" else "The run failed or did not complete; inspect the recorded command outputs.",
        "residual_risks": [
            "The source PDF is checked only in a local replay supplied with --source-pdf; CI does not contain that draft.",
            "Schema 1 records bounded execution evidence and is not a universal proof or independent source authentication.",
        ],
    }


def run_replay(args):
    manifest, snapshot, ledger, claims, names, kinds, (hashes_before, canonical_before) = validate_static()
    output = ensure_ignored_output(args.output_dir)
    source_check = verify_source_pdf(args.source_pdf, manifest, snapshot) if args.source_pdf else {"performed": False}
    source_pdf_hash_before = source_check.get("sha256")
    if source_check["performed"]:
        write_json(output / "source-verification.json", source_check)
    source_verification_sha = sha(output / "source-verification.json") if source_check["performed"] else None
    commit, status_before = checkout_state()
    ci_claim = os.getenv("GITHUB_ACTIONS") == "true" and bool(os.getenv("GITHUB_RUN_ID"))
    if os.getenv("GITHUB_ACTIONS") == "true":
        assert ci_claim, "GitHub Actions replay requires GITHUB_RUN_ID"
        assert os.getenv("GITHUB_SHA") == commit, "GITHUB_SHA must identify the checked-out merge commit"
        assert re.fullmatch(r"[a-f0-9]{40}", os.getenv("MIND_CONTINUATION_PR_HEAD_SHA", ""))
    ci = {
        "claimed": ci_claim,
        "environment_source": "GITHUB_ACTIONS environment variables; not independently attested" if ci_claim else None,
        "run_id": os.getenv("GITHUB_RUN_ID") if ci_claim else None,
        "head_sha": os.getenv("MIND_CONTINUATION_PR_HEAD_SHA") if ci_claim else None,
        "merge_sha": os.getenv("GITHUB_SHA") if ci_claim else None,
    }
    receipt = {
        "schema_version": "1.0", "status": "RUNNING", "mode": "replay",
        "lake": args.lake, "python_executable": sys.executable,
        "base_commit": BASE_COMMIT, "tested_commit": commit,
        "dirty_before": bool(status_before), "worktree_status_before": status_before,
        "source_id": manifest["source_id"], "source_sha256": manifest["sha256"],
        "source_check": source_check, "source_verification_sha256": source_verification_sha,
        "source_pdf_sha256_before": source_pdf_hash_before,
        "source_pdf_sha256_after": None, "input_hashes_before": hashes_before,
        "input_hashes_after": {}, "input_hashes_canonical_before": canonical_before,
        "input_hashes_canonical_after": {}, "declarations": names, "module_declarations": {MODULE: names},
        "classifications": {claim["id"]: claim["classification"] for claim in claims},
        "authority_ceiling": manifest["authority_ceiling"],
        "scope_status": "BOUNDED_MIND_V04_CONTINUATION",
        "tested_scope": "One reduced source-bound finite Lean realization in Experiments.MindContinuation.",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "software": [
                {"name": "Python", "version": sys.version.split()[0]},
            ],
            "lean_toolchain": (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip(),
            "platform": platform.platform(),
        },
        "ci": ci, "source_pdf_status": "LOCAL_VERIFIED" if source_check["performed"] else ("UNAVAILABLE_IN_CI" if ci_claim else "NOT_SUPPLIED"),
        "commands": [], "axioms": {}, "signatures": {}, "axiom_inspection_stdout": "",
        "evidence_directory": rel(output), "recorded": False,
    }
    start_all = time.monotonic()
    if source_check["performed"]:
        receipt["environment"]["software"].append(source_check["extractor"])
    exit_status = 0
    try:
        for label, argv in commands(args.lake, sys.executable):
            start = time.monotonic()
            completed = subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       text=True, encoding="utf-8", errors="replace", check=False)
            elapsed = round(time.monotonic() - start, 6)
            log = output / f"{label}.txt"
            log.write_text(completed.stdout, encoding="utf-8", newline="")
            receipt["commands"].append({
                "label": label, "argv": argv, "exit_code": completed.returncode,
                "log": rel(log), "sha256": sha(log), "elapsed_seconds": elapsed,
            })
            if completed.returncode:
                exit_status = completed.returncode
                receipt["failed_command"] = label
                break
            if label in {"lean-version", "lake-version"}:
                receipt["environment"]["software"].append({
                    "name": "Lean" if label == "lean-version" else "Lake",
                    "version": completed.stdout.strip(),
                })
        if exit_status == 0:
            log = output / "axioms-signatures.txt"
            receipt["axiom_inspection_stdout"] = log.read_bytes().decode("utf-8")
            receipt["axioms"] = parse_axioms_text(receipt["axiom_inspection_stdout"], names)
            receipt["signatures"] = parse_signatures_text(receipt["axiom_inspection_stdout"], names)
            receipt["status"] = "PASS_MIND_V04_CONTINUATION"
        else:
            receipt["status"] = "FAILED_MIND_V04_CONTINUATION"
    except Exception as exc:
        exit_status = 1
        receipt["status"] = "FAILED_MIND_V04_CONTINUATION"
        receipt["error"] = f"{type(exc).__name__}: {exc}"
    receipt["elapsed_seconds"] = round(time.monotonic() - start_all, 6)
    receipt["finished_at"] = datetime.now(timezone.utc).isoformat()
    receipt["exit_status"] = exit_status
    try:
        raw_after, canonical_after = input_hashes()
        receipt["input_hashes_after"] = raw_after
        receipt["input_hashes_canonical_after"] = canonical_after
        if raw_after != hashes_before or canonical_after != canonical_before:
            receipt["status"] = "FAILED_INPUTS_CHANGED"
            receipt["exit_status"] = exit_status = 1
    except Exception as exc:
        receipt["input_hashes_after"] = {}
        receipt["input_hashes_canonical_after"] = {}
        receipt["input_hash_error"] = f"{type(exc).__name__}: {exc}"
        receipt["status"] = "FAILED_INPUTS_CHANGED"
        receipt["exit_status"] = exit_status = 1
    if args.source_pdf:
        try:
            receipt["source_pdf_sha256_after"] = sha(args.source_pdf.resolve())
            if receipt["source_pdf_sha256_after"] != source_pdf_hash_before:
                receipt["status"] = "FAILED_SOURCE_CHANGED"
                receipt["exit_status"] = exit_status = 1
        except Exception as exc:
            receipt["source_pdf_sha256_after"] = None
            receipt["source_pdf_hash_error"] = f"{type(exc).__name__}: {exc}"
            receipt["status"] = "FAILED_SOURCE_CHANGED"
            receipt["exit_status"] = exit_status = 1
    _commit, status_after = checkout_state()
    receipt["dirty_after"] = bool(status_after)
    receipt["worktree_status_after"] = status_after
    receipt["receipt_guards"] = []
    if exit_status == 0:
        try:
            receipt["receipt_guards"] = validate_guards(receipt, manifest, snapshot, claims, names, canonical_before)
        except Exception as exc:
            receipt["status"] = "FAILED_RECEIPT_GUARD"
            receipt["error"] = f"{type(exc).__name__}: {exc}"
            receipt["exit_status"] = exit_status = 1
    # Preserve failed attempts too; output directory is unique/empty and ignored.
    if not receipt["commands"]:
        failure_log = output / "runner-failure.txt"
        failure_log.write_text(receipt.get("error", "Replay ended before a command ran."), encoding="utf-8", newline="")
    receipt["execution_manifest_path"] = rel(output / "computation-manifest.json")
    comp = make_computation_manifest(receipt)
    write_json(output / "computation-manifest.json", comp)
    receipt["computation_manifest_sha256"] = sha(output / "computation-manifest.json")
    write_json(output / "results.json", receipt)
    if exit_status == 0 and args.record:
        receipt["recorded"] = True
        write_json(RESULT, receipt)
    print(receipt["status"])
    return exit_status


def validate_local_artifacts(receipt, require):
    directory = (ROOT / receipt["evidence_directory"]).resolve()
    assert directory.is_relative_to(ROOT), "evidence directory must be inside the repository"
    if not directory.is_dir():
        if require:
            raise FileNotFoundError("Recorded raw artifacts are absent; replay or supply the retained local artifact directory.")
        return "RECORDED_HASHES_ONLY_REPLAY_REQUIRED"
    records = [(row["log"], row["sha256"]) for row in receipt["commands"]]
    records.append((receipt["execution_manifest_path"], receipt["computation_manifest_sha256"]))
    if receipt["source_check"]["performed"]:
        records.append((receipt["evidence_directory"] + "/source-verification.json", receipt["source_verification_sha256"]))
    for name, digest in records:
        path = (ROOT / name).resolve()
        assert path.is_relative_to(directory), "artifact must remain inside the declared evidence directory"
        assert path.is_file(), f"missing recorded artifact: {name}"
        assert sha(path) == digest, f"changed recorded artifact: {name}"
    return "VERIFIED_LOCAL_ARTIFACTS"


def validate_saved(require_artifacts=False):
    manifest, snapshot, ledger, claims, names, kinds, (raw_hashes, canonical_hashes) = validate_static()
    receipt = read_json(RESULT)
    validate_receipt(receipt, manifest, snapshot, claims, names, canonical_hashes)
    guards = validate_guards(receipt, manifest, snapshot, claims, names, canonical_hashes)
    assert receipt["receipt_guards"] == guards
    return receipt, validate_local_artifacts(receipt, require_artifacts)


def main():
    if not __debug__:
        raise RuntimeError("Receipt validation requires Python assertions; do not use -O or PYTHONOPTIMIZE.")
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check-inputs", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--replay", action="store_true")
    parser.add_argument("--lake", default="lake")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--source-pdf", type=Path)
    parser.add_argument("--record", action="store_true")
    parser.add_argument("--require-artifacts", action="store_true",
                        help="With --check, require every retained raw log and manifest to exist and match its digest.")
    args = parser.parse_args()
    if args.record and not args.replay:
        parser.error("--record is valid only with --replay")
    if args.require_artifacts and not args.check:
        parser.error("--require-artifacts is valid only with --check")
    if args.replay:
        if args.output_dir is None:
            parser.error("--replay requires --output-dir")
        return run_replay(args)
    if args.check_inputs:
        manifest, snapshot, ledger, claims, names, kinds, (raw_hashes, canonical_hashes) = validate_static()
        if args.source_pdf:
            verify_source_pdf(args.source_pdf, manifest, snapshot)
        print(f"PASS_MIND_V04_CONTINUATION_INPUTS declarations={len(names)} inputs={len(raw_hashes)}")
        return 0
    receipt, artifact_status = validate_saved(args.require_artifacts)
    if args.source_pdf:
        manifest, snapshot = load_source()
        assert receipt["source_check"] == verify_source_pdf(args.source_pdf, manifest, snapshot)
        assert receipt["source_pdf_sha256_before"] == receipt["source_pdf_sha256_after"] == SOURCE_SHA256
    print(f"PASS_MIND_V04_CONTINUATION_RECEIPTS artifacts={artifact_status} source={receipt['source_pdf_status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
