#!/usr/bin/env python3
"""Source-bound, per-batch Lean receipt runner (stdlib only; no remote actions)."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AREA = Path(__file__).resolve().parent
FREEZE = ROOT / "Audit/pal-v24-candidate/source-manifest.json"
ALLOWED_AXIOMS = {"propext", "Quot.sound", "Classical.choice"}
KINDS = {"theorem", "def", "structure", "inductive"}
FORBIDDEN = re.compile(r"\b(sorry|admit|axiom|native_decide|unsafe)\b")
DECL = re.compile(r"^\s*(?:(?:private|protected|noncomputable|partial|unsafe)\s+)*(theorem|def|structure|inductive)\s+([A-Za-z_][A-Za-z0-9_'.]*)\b")
UNSUPPORTED_DECL = re.compile(r"^\s*(?:(?:private|protected|noncomputable|partial|unsafe)\s+)*(abbrev|opaque|class|axiom|instance)\b")
HASH = re.compile(r"^[0-9a-f]{64}$")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def input_key(path: Path) -> str:
    resolved = path.resolve()
    return resolved.relative_to(ROOT).as_posix() if resolved.is_relative_to(ROOT) else "external:" + str(resolved)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def git(*args: str) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=True)
    return p.stdout.strip()


def git_state():
    return {"branch": git("branch", "--show-current"), "head": git("rev-parse", "HEAD"),
            "dirty": bool(git("status", "--porcelain", "--untracked-files=all")),
            "status_porcelain": git("status", "--porcelain", "--untracked-files=all")}


def module_file(module: str) -> Path:
    if not isinstance(module, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*", module):
        raise ValueError(f"invalid Lean module name: {module!r}")
    return ROOT.joinpath(*module.split(".")).with_suffix(".lean")


def uncomment(text: str) -> str:
    """Remove Lean comments and quoted strings while preserving line boundaries."""
    out, i, depth, string = [], 0, 0, False
    while i < len(text):
        if depth:
            if text.startswith("/-", i): depth += 1; out.extend("  "); i += 2
            elif text.startswith("-/", i): depth -= 1; out.extend("  "); i += 2
            else:
                out.append("\n" if text[i] == "\n" else " "); i += 1
        elif string:
            if text[i] == "\\": out.extend("  "); i += 2
            elif text[i] == '"': string = False; out.append(" "); i += 1
            else: out.append("\n" if text[i] == "\n" else " "); i += 1
        elif text.startswith("/-", i): depth = 1; out.extend("  "); i += 2
        elif text.startswith("--", i):
            while i < len(text) and text[i] != "\n": out.append(" "); i += 1
        elif text[i] == '"': string = True; out.append(" "); i += 1
        else: out.append(text[i]); i += 1
    if depth or string:
        raise ValueError("unterminated Lean comment or string")
    return "".join(out)


def declarations(path: Path, module: str):
    text = uncomment(path.read_text(encoding="utf-8"))
    if FORBIDDEN.search(text):
        raise ValueError(f"forbidden Lean token in {rel(path)}")
    namespace = []
    found = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped: continue
        if stripped.startswith("namespace "):
            namespace.append(stripped.split()[1]); continue
        if stripped == "end" or stripped.startswith("end "):
            if namespace: namespace.pop()
            continue
        # A declaration nested under a `where` or `mutual` block is not a
        # module-level declaration. Only declarations at column zero or one
        # indentation level in a namespace are inventoried.
        match = DECL.match(line)
        if match:
            kind, name = match.groups()
            # Lean namespace bodies are indented; reject deeper local declarations.
            if len(line) - len(line.lstrip()) > (2 if namespace else 0):
                continue
            full = ".".join([*namespace, name]) if namespace else f"{module}.{name}"
            found.append((full, kind))
        elif UNSUPPORTED_DECL.match(line) and len(line) - len(line.lstrip()) <= (2 if namespace else 0):
            raise ValueError(f"unsupported explicit declaration form in target module: {stripped.split()[0]}")
    names = [n for n, _ in found]
    if len(names) != len(set(names)):
        raise ValueError("duplicate explicit declaration in target module")
    return found


def validate_claims(batch_dir: Path):
    ledger_path = batch_dir / "claims.json"
    ledger = read_json(ledger_path)
    for key in ("batch", "module", "axioms_module", "source_inputs", "claims"):
        if key not in ledger: raise ValueError(f"claims.json missing {key}")
    if ledger["batch"] != batch_dir.name: raise ValueError("batch field must equal batch directory name")
    target, axioms = module_file(ledger["module"]), module_file(ledger["axioms_module"])
    if not target.is_file() or not axioms.is_file(): raise FileNotFoundError("target or axioms module is missing")
    rows = ledger["claims"]
    if not isinstance(rows, list) or not rows: raise ValueError("claims must be a non-empty array")
    names = [row.get("name") for row in rows]
    if len(names) != len(set(names)): raise ValueError("duplicate claim names")
    declared = declarations(target, ledger["module"])
    decl_map = dict(declared)
    if set(names) != set(decl_map):
        raise ValueError(f"declaration inventory mismatch: missing={sorted(set(decl_map)-set(names))}; extraneous={sorted(set(names)-set(decl_map))}")
    required = {"name", "kind", "classification", "source_routes", "assumptions", "statement", "ceiling", "residual"}
    for row in rows:
        if not required <= row.keys(): raise ValueError(f"claim {row.get('name')} missing fields {sorted(required-row.keys())}")
        if row["kind"] not in KINDS or row["kind"] != decl_map[row["name"]]: raise ValueError(f"kind mismatch for {row['name']}")
        for key in ("source_routes", "assumptions"):
            if not isinstance(row[key], list): raise ValueError(f"{key} must be a list for {row['name']}")
        allowed = row.get("allowed_axioms", [])
        if not isinstance(allowed, list) or not all(isinstance(a, str) and a for a in allowed): raise ValueError(f"allowed_axioms must be a list of names for {row['name']}")
        for key in ("classification", "statement", "ceiling", "residual"):
            if not isinstance(row[key], str) or not row[key].strip(): raise ValueError(f"{key} is empty for {row['name']}")
    axtext = uncomment(axioms.read_text(encoding="utf-8"))
    if FORBIDDEN.search(axtext): raise ValueError(f"forbidden Lean token in {rel(axioms)}")
    checked = re.findall(r"^\s*#check\s+@?(\S+)", axtext, re.MULTILINE)
    printed = re.findall(r"^\s*#print axioms\s+@?(\S+)", axtext, re.MULTILINE)
    if checked != names or printed != names:
        raise ValueError("axioms module must #check and #print axioms for every ledger name exactly once, in ledger order")
    srcs = ledger["source_inputs"]
    if not isinstance(srcs, list): raise ValueError("source_inputs must be an array")
    input_paths = {rel(ledger_path): ledger_path, rel(target): target, rel(axioms): axioms}
    for row in srcs:
        if not isinstance(row, dict) or not {"path", "sha256", "role"} <= row.keys():
            raise ValueError("each source_inputs row needs path, sha256, and role")
        if not isinstance(row["path"], str) or not row["path"] or not isinstance(row["role"], str) or not row["role"]:
            raise ValueError("source input path and role must be non-empty strings")
        if not HASH.fullmatch(row["sha256"]): raise ValueError(f"invalid SHA-256 for {row['path']}")
        p = Path(row["path"])
        p = p.resolve() if p.is_absolute() else (ROOT / p).resolve()
        if not p.is_file(): raise FileNotFoundError(f"source input missing: {row['path']}")
        if digest(p) != row["sha256"]: raise ValueError(f"source hash mismatch: {row['path']}")
        input_paths[input_key(p)] = p
    for dirname in ("PAL", "Audit", "Experiments"):
        root = ROOT / dirname
        if root.is_dir():
            for p in root.rglob("*.lean"):
                if ".lake" not in p.parts and ".git" not in p.parts: input_paths[rel(p)] = p
    for p in ROOT.glob("*.lean"):
        input_paths[rel(p)] = p
    for name in ("lean-toolchain", "lakefile.lean", "lakefile.toml", "lake-manifest.json"):
        p = ROOT / name
        if p.is_file(): input_paths[name] = p
    input_paths[rel(Path(__file__))] = Path(__file__).resolve()
    input_paths[rel(AREA / "README.md")] = AREA / "README.md" if (AREA / "README.md").exists() else Path(__file__).resolve()
    input_paths[rel(FREEZE)] = FREEZE
    return ledger, rows, declared, input_paths


def freeze_check(source_inputs):
    if not FREEZE.is_file(): raise ValueError("BLOCKED_CANDIDATE_SOURCE_FREEZE: source-manifest.json is absent")
    manifest = read_json(FREEZE)
    entries = {}
    def freeze_key(raw):
        candidate = Path(raw)
        candidate = candidate.resolve() if candidate.is_absolute() else (ROOT / candidate).resolve()
        return candidate.relative_to(ROOT).as_posix() if candidate.is_relative_to(ROOT) else candidate.as_posix()
    def walk(value):
        if isinstance(value, dict):
            if isinstance(value.get("path"), str) and isinstance(value.get("sha256"), str):
                entries[freeze_key(value["path"])] = value["sha256"]
            for child in value.values(): walk(child)
        elif isinstance(value, list):
            for child in value: walk(child)
    walk(manifest)
    for row in source_inputs:
        path = freeze_key(row["path"])
        if row["role"].lower() in {"candidate", "candidate_source", "source_candidate"} or path.startswith("Audit/pal-v24-candidate/"):
            key = path
            if key not in entries or entries[key] != row["sha256"]:
                raise ValueError(f"candidate freeze does not bind exact input: {path}")
    return digest(FREEZE)


def snapshot(paths):
    return {name: digest(path) for name, path in sorted(paths.items())}


def run_command(argv, cwd, evidence, label):
    started = time.monotonic()
    p = subprocess.run(argv, cwd=cwd, text=True, encoding="utf-8", errors="replace", capture_output=True)
    elapsed = time.monotonic() - started
    log = evidence / f"{label}.log"
    stdout_bytes = p.stdout.encode("utf-8")
    stderr_bytes = p.stderr.encode("utf-8")
    header = {"argv": argv, "cwd": str(cwd), "exit_code": p.returncode,
              "stdout_bytes": len(stdout_bytes), "stderr_bytes": len(stderr_bytes)}
    log.write_bytes(b"PAL-RUN-LOG-1\n" + json.dumps(header, ensure_ascii=False).encode("utf-8") +
                    b"\n" + stdout_bytes + b"\nPAL-STDERR-1\n" + stderr_bytes)
    return {"name": label, "argv": argv, "cwd": str(cwd), "exit_code": p.returncode,
            "runtime_seconds": round(elapsed, 6), "stdout_log": rel(log), "stdout_log_sha256": digest(log),
            "stdout_sha256": digest_bytes(p.stdout.encode("utf-8")),
            "stderr_sha256": digest_bytes(p.stderr.encode("utf-8")), "stdout": p.stdout, "stderr": p.stderr}


def parse_inspection(text: str, names):
    escaped = "|".join(re.escape(n) for n in names)
    headers = list(re.finditer(r"^@?(" + escaped + r")(?:\.\{[^}]+\})?[ \t]*:", text, re.MULTILINE))
    if [m.group(1) for m in headers] != names:
        raise ValueError("axioms module output did not print every exact claim signature in ledger order")
    axiom_header = re.compile(r"^'[^']+' (?:does not depend on any axioms|depends on axioms:)", re.MULTILINE)
    signatures = {}
    for i, match in enumerate(headers):
        stop = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        ax = axiom_header.search(text, match.end(), stop)
        signatures[names[i]] = text[match.start():ax.start() if ax else stop].strip()
    rows = re.findall(r"'([^']+)' (does not depend on any axioms|depends on axioms: \[(.*?)\])", text, re.DOTALL)
    axioms = {}
    for name, form, raw in rows:
        if name in axioms: raise ValueError(f"duplicate #print axioms output for {name}")
        axioms[name] = [] if form.startswith("does not") else sorted(x.strip() for x in raw.replace("\n", " ").split(",") if x.strip())
    if list(axioms) != names: raise ValueError("axioms module output did not list claims in ledger order")
    return signatures, axioms


def parse_command_log(path: Path):
    """Read a length-delimited run log and recover its exact command streams."""
    raw = path.read_bytes()
    prefix = b"PAL-RUN-LOG-1\n"
    if not raw.startswith(prefix): raise ValueError(f"unsupported command log format: {rel(path)}")
    header_end = raw.find(b"\n", len(prefix))
    if header_end < 0: raise ValueError(f"truncated command log header: {rel(path)}")
    try:
        header = json.loads(raw[len(prefix):header_end].decode("utf-8"))
        stdout_size, stderr_size = header["stdout_bytes"], header["stderr_bytes"]
        if not isinstance(stdout_size, int) or stdout_size < 0 or not isinstance(stderr_size, int) or stderr_size < 0:
            raise ValueError("invalid stream byte count")
    except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"malformed command log header: {rel(path)}") from exc
    body_start = header_end + 1
    stdout_end = body_start + stdout_size
    marker = b"\nPAL-STDERR-1\n"
    if stdout_end + len(marker) + stderr_size != len(raw) or raw[stdout_end:stdout_end + len(marker)] != marker:
        raise ValueError(f"command log stream boundary mismatch: {rel(path)}")
    try:
        stdout = raw[body_start:stdout_end].decode("utf-8")
        stderr = raw[stdout_end + len(marker):].decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"command log is not UTF-8: {rel(path)}") from exc
    return {**header, "stdout": stdout, "stderr": stderr}


def validate_command_rows(rows, expected_specs, cwd, require_complete):
    if not isinstance(rows, list): raise ValueError("receipt command inventory is not an array")
    expected_prefix = expected_specs if require_complete else expected_specs[:len(rows)]
    if len(rows) > len(expected_specs) or len(rows) != len(expected_prefix):
        raise ValueError("receipt command inventory has an invalid length")
    for index, (row, (name, argv)) in enumerate(zip(rows, expected_prefix)):
        if not isinstance(row, dict) or row.get("name") != name or row.get("argv") != argv or row.get("cwd") != str(cwd):
            raise ValueError(f"receipt command inventory mismatch at position {index + 1}")
        if isinstance(row.get("exit_code"), bool) or not isinstance(row.get("exit_code"), int): raise ValueError(f"receipt command exit code is invalid for {name}")
        if index < len(rows) - 1 and row["exit_code"] != 0:
            raise ValueError(f"receipt records a later command after failed command {name}")
        if require_complete and row["exit_code"] != 0:
            raise ValueError(f"passing receipt records failed command {name}")
    return len(rows)


def validate_pass_inventory(receipt, expected_declarations, expected_input_keys,
                            expected_versions, expected_commands, actual_signatures, actual_axioms):
    if receipt.get("status") != "PASS_BOUNDED_LEAN_CHECKS": return
    if receipt.get("error"): raise ValueError("passing receipt contains an error")
    if receipt.get("declared") != expected_declarations: raise ValueError("saved declaration inventory mismatch")
    if not receipt.get("inputs_unchanged") or receipt.get("input_hashes_before") != receipt.get("input_hashes_after"):
        raise ValueError("passing receipt reports changed inputs")
    hashes = receipt.get("input_hashes_after")
    if not isinstance(hashes, dict) or set(hashes) != set(expected_input_keys):
        raise ValueError("passing receipt input inventory is incomplete or unexpected")
    validate_command_rows(receipt.get("versions"), expected_versions, ROOT, True)
    validate_command_rows(receipt.get("commands"), expected_commands, ROOT, True)
    if receipt.get("signatures") != actual_signatures:
        raise ValueError("saved signatures do not match the captured axiom-inspection output")
    if receipt.get("axioms") != actual_axioms:
        raise ValueError("saved axiom inventory does not match the captured axiom-inspection output")


def validate_saved_logs(receipt, batch_dir, version_specs, command_specs):
    seen_logs = set()
    attempt_dir = None
    first_failure = False
    parsed = {"versions": [], "commands": []}
    for section, specs in (("versions", version_specs), ("commands", command_specs)):
        rows = receipt.get(section, [])
        if not isinstance(rows, list): raise ValueError(f"saved {section} inventory is not an array")
        if len(rows) > len(specs): raise ValueError(f"saved {section} inventory is too long")
        for index, row in enumerate(rows):
            label, argv = specs[index]
            if not isinstance(row, dict): raise ValueError(f"saved {section} row is malformed")
            if row.get("name") != label or row.get("argv") != argv or row.get("cwd") != str(ROOT):
                raise ValueError(f"saved {section} command mismatch for {label}")
            runtime = row.get("runtime_seconds")
            if isinstance(runtime, bool) or not isinstance(runtime, (int, float)) or runtime < 0:
                raise ValueError(f"saved runtime is invalid for {label}")
            log_name = row.get("stdout_log")
            if not isinstance(log_name, str) or not log_name:
                raise ValueError(f"saved log path is missing for {label}")
            log_path = (ROOT / log_name).resolve()
            evidence_root = (batch_dir / "evidence").resolve()
            if not log_path.is_relative_to(evidence_root) or log_path.name != f"{label}.log":
                raise ValueError(f"saved log path is outside the expected evidence directory for {label}")
            if attempt_dir is None: attempt_dir = log_path.parent
            if log_path.parent != attempt_dir or log_path in seen_logs:
                raise ValueError("saved command logs do not belong to one unique attempt")
            seen_logs.add(log_path)
            expected_log_hash = row.get("stdout_log_sha256")
            if not isinstance(expected_log_hash, str) or not HASH.fullmatch(expected_log_hash) or not log_path.is_file() or digest(log_path) != expected_log_hash:
                raise ValueError(f"saved output log mismatch: {log_name}")
            recovered = parse_command_log(log_path)
            for field in ("argv", "cwd", "exit_code"):
                if row.get(field) != recovered.get(field):
                    raise ValueError(f"saved {field} does not match command log for {label}")
            for field, value in (("stdout_sha256", recovered["stdout"].encode("utf-8")),
                                 ("stderr_sha256", recovered["stderr"].encode("utf-8"))):
                expected = row.get(field)
                if not isinstance(expected, str) or not HASH.fullmatch(expected) or digest_bytes(value) != expected:
                    raise ValueError(f"saved {field} does not match command log for {label}")
            if section == "versions":
                output = (recovered["stdout"] + recovered["stderr"]).strip()
                if row.get("output") != output: raise ValueError(f"saved version output does not match command log for {label}")
            diagnostic = bool(re.search(r"(?im)^\s*(?:error|fatal error):", recovered["stdout"] + "\n" + recovered["stderr"]))
            failed = recovered["exit_code"] != 0 or diagnostic
            if receipt.get("status") == "PASS_BOUNDED_LEAN_CHECKS" and failed:
                raise ValueError(f"passing receipt contains failed or error-emitting command {label}")
            if first_failure: raise ValueError("saved receipt contains commands after a failed command")
            if failed: first_failure = True
            parsed[section].append(recovered)
        if section == "versions" and len(rows) < len(specs) and receipt.get("commands"):
            raise ValueError("saved receipt has Lean commands despite an incomplete version-probe sequence")
    return parsed


def run_batch(args):
    batch_dir = (AREA / args.batch).resolve()
    if not batch_dir.is_relative_to(AREA) or not batch_dir.is_dir(): raise ValueError("batch must name a directory under Audit/pal-v24-batches")
    ledger, claims, declared, paths = validate_claims(batch_dir)
    freeze_sha = freeze_check(ledger["source_inputs"])
    for row in ledger["source_inputs"]:
        path = Path(row["path"])
        path = path.resolve() if path.is_absolute() else (ROOT / path).resolve()
        if digest(path) != row["sha256"]: raise ValueError(f"source hash mismatch: {row['path']}")
    lake = str(Path(args.lake).resolve())
    if not Path(lake).is_absolute() or not Path(lake).is_file(): raise ValueError("--lake must be an absolute path to an existing executable")
    paths[input_key(Path(lake))] = Path(lake)
    python_exe = Path(sys.executable).resolve()
    if not python_exe.is_file(): raise ValueError("Python executable is not a readable file")
    paths[input_key(python_exe)] = python_exe
    before = snapshot(paths)
    evidence = batch_dir / "evidence" / datetime.now(timezone.utc).strftime("attempt-%Y%m%dT%H%M%S%fZ")
    evidence.mkdir(parents=True, exist_ok=False)
    version_commands = [[lake, "--version"], [lake, "env", "lean", "--version"], [str(python_exe), "--version"]]
    receipt = {"schema": "pal-v24-batch-receipt-v2", "batch": ledger["batch"], "module": ledger["module"],
               "axioms_module": ledger["axioms_module"], "started_utc": datetime.now(timezone.utc).isoformat(),
               "candidate_freeze_sha256": freeze_sha, "git_before": git_state(), "input_hashes_before": before,
               "declared": [{"name": n, "kind": k} for n, k in declared],
               "theorem_count": sum(k == "theorem" for _, k in declared), "versions": [], "commands": [], "status": "RUNNING"}
    try:
        for i, argv in enumerate(version_commands):
            r = run_command(argv, ROOT, evidence, f"version-{i+1}")
            receipt["versions"].append({k: r[k] for k in ("name", "argv", "cwd", "exit_code", "runtime_seconds", "stdout_log", "stdout_log_sha256", "stdout_sha256", "stderr_sha256")})
            receipt["versions"][-1]["output"] = (r["stdout"] + r["stderr"]).strip()
            if r["exit_code"] != 0 or re.search(r"(?im)^\s*(?:error|fatal error):", r["stdout"] + "\n" + r["stderr"]): raise RuntimeError("version probe failed")
        jobs = [
            ("build-target", [lake, "build", ledger["module"]]),
            ("check-axioms", [lake, "env", "lean", str(module_file(ledger["axioms_module"]))]),
            ("leanchecker-target", [lake, "env", "leanchecker", ledger["module"]]),
        ]
        for label, argv in jobs:
            result = run_command(argv, ROOT, evidence, label)
            # Full actual output is in the content-addressed logs; retain stdout and stderr hashes in receipt.
            receipt["commands"].append({k: result[k] for k in ("name", "argv", "cwd", "exit_code", "runtime_seconds", "stdout_log", "stdout_log_sha256", "stdout_sha256", "stderr_sha256")})
            if result["exit_code"] != 0 or re.search(r"(?im)^\s*(?:error|fatal error):", result["stdout"] + "\n" + result["stderr"]): raise RuntimeError(f"{label} exited {result['exit_code']} or emitted an error")
        expected_names = [row["name"] for row in claims]
        axlog = parse_command_log(evidence / "check-axioms.log")["stdout"]
        signatures, actual_axioms = parse_inspection(axlog, expected_names)
        allowed_by_claim = {row["name"]: ALLOWED_AXIOMS | set(row.get("allowed_axioms", [])) for row in claims}
        unexpected = {n: sorted(set(axs)-allowed_by_claim[n]) for n, axs in actual_axioms.items() if set(axs)-allowed_by_claim[n]}
        if unexpected: raise ValueError(f"unlisted imported axioms: {unexpected}")
        receipt["axioms"] = actual_axioms
        receipt["signatures"] = signatures
        receipt["status"] = "PASS_BOUNDED_LEAN_CHECKS"
    except Exception as exc:
        receipt["status"] = "FAILED_OR_BLOCKED"
        receipt["error"] = f"{type(exc).__name__}: {exc}"
    try:
        after = snapshot(paths)
    except Exception as exc:
        after = {}
        receipt["input_hash_error"] = f"{type(exc).__name__}: {exc}"
        receipt["status"] = "FAILED_INPUTS_CHANGED"
    receipt["input_hashes_after"] = after
    receipt["inputs_unchanged"] = before == after
    receipt["git_after"] = git_state()
    if before != after:
        receipt["status"] = "FAILED_INPUTS_CHANGED"
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    write_json(batch_dir / "results.json", receipt)
    print(receipt["status"])
    return 0 if receipt["status"] == "PASS_BOUNDED_LEAN_CHECKS" else 1


def validate_saved(batch_dir: Path):
    batch_dir = batch_dir.resolve()
    if not batch_dir.is_relative_to(AREA.resolve()) or not batch_dir.is_dir():
        raise ValueError("batch must name a directory under Audit/pal-v24-batches")
    receipt = read_json(batch_dir / "results.json")
    ledger, claims, declared, current_paths = validate_claims(batch_dir)
    actual = [{"name": n, "kind": k} for n, k in declared]
    validate_receipt_core(receipt, actual)
    if receipt.get("theorem_count") != sum(k == "theorem" for _, k in declared): raise ValueError("saved theorem count mismatch")
    status = receipt["status"]
    before, after = receipt["input_hashes_before"], receipt["input_hashes_after"]
    if not isinstance(before, dict) or not isinstance(after, dict): raise ValueError("saved input hash inventories are malformed")
    for key, hashes in (("input_hashes_before", before), ("input_hashes_after", after)):
        for name, expected in hashes.items():
            if not isinstance(name, str) or not isinstance(expected, str) or not HASH.fullmatch(expected):
                raise ValueError(f"saved {key} contains an invalid path or SHA-256")
    if receipt.get("inputs_unchanged") != (before == after):
        raise ValueError("saved unchanged-input flag disagrees with recorded inventories")

    # For a PASS, recover the tool paths from the recorded probes and require the
    # exact source/config/code/tool input set captured by --run.
    versions = receipt.get("versions", [])
    lake = None
    python_path = None
    if versions:
        first_argv = versions[0].get("argv", [])
        if isinstance(first_argv, list) and first_argv and isinstance(first_argv[0], str):
            lake = Path(first_argv[0]).resolve()
    if status == "PASS_BOUNDED_LEAN_CHECKS":
        if len(versions) != 3 or lake is None or not lake.is_file():
            raise ValueError("passing receipt lacks its complete Lake/Python version probes")
        third = versions[2].get("argv", [])
        if not isinstance(third, list) or len(third) != 2 or third[1] != "--version" or not isinstance(third[0], str):
            raise ValueError("passing receipt has an invalid Python version probe")
        python_path = Path(third[0]).resolve()
        if not python_path.is_file(): raise ValueError("passing receipt's Python executable is unavailable")
        version_specs = [("version-1", [str(lake), "--version"]),
                         ("version-2", [str(lake), "env", "lean", "--version"]),
                         ("version-3", [str(python_path), "--version"])]
        expected_inputs = dict(current_paths)
        expected_inputs[input_key(lake)] = lake
        expected_inputs[input_key(python_path)] = python_path
        if set(after) != set(expected_inputs):
            raise ValueError("passing receipt input inventory is incomplete or unexpected")
    else:
        # Failed attempts may end during version probing. Validate each recorded
        # row as a sequential prefix, without converting failure into a PASS.
        version_specs = []
        if lake is not None:
            version_specs = [("version-1", [str(lake), "--version"]),
                             ("version-2", [str(lake), "env", "lean", "--version"])]
        if len(versions) >= 3:
            third = versions[2].get("argv", [])
            if isinstance(third, list) and len(third) == 2 and third[1] == "--version" and isinstance(third[0], str):
                python_path = Path(third[0]).resolve()
                version_specs.append(("version-3", [str(python_path), "--version"]))
        if set(current_paths) - set(after) and after:
            raise ValueError("saved post-run inputs omit currently required source or tool files")

    if lake is not None:
        command_specs = [("build-target", [str(lake), "build", ledger["module"]]),
                         ("check-axioms", [str(lake), "env", "lean", str(module_file(ledger["axioms_module"]))]),
                         ("leanchecker-target", [str(lake), "env", "leanchecker", ledger["module"]])]
    else:
        command_specs = []
    parsed_logs = validate_saved_logs(receipt, batch_dir, version_specs, command_specs)
    if status == "PASS_BOUNDED_LEAN_CHECKS":
        freeze_sha = freeze_check(ledger["source_inputs"])
        if receipt.get("candidate_freeze_sha256") != freeze_sha:
            raise ValueError("saved candidate freeze digest mismatch")
        # Receipt declarations retain source order; inspection follows ledger order.
        expected_declarations = actual
        expected_versions = [("version-1", [str(lake), "--version"]),
                             ("version-2", [str(lake), "env", "lean", "--version"]),
                             ("version-3", [str(python_path), "--version"])]
        expected_commands = [("build-target", [str(lake), "build", ledger["module"]]),
                             ("check-axioms", [str(lake), "env", "lean", str(module_file(ledger["axioms_module"]))]),
                             ("leanchecker-target", [str(lake), "env", "leanchecker", ledger["module"]])]
        actual_signatures, actual_axioms = parse_inspection(parsed_logs["commands"][1]["stdout"], [row["name"] for row in claims])
        validate_pass_inventory(receipt, expected_declarations, set(expected_inputs),
                                expected_versions, expected_commands, actual_signatures, actual_axioms)
        allowed_by_claim = {row["name"]: ALLOWED_AXIOMS | set(row.get("allowed_axioms", [])) for row in claims}
        if any(set(ax) - allowed_by_claim[name] for name, ax in actual_axioms.items()):
            raise ValueError("saved receipt contains unlisted axioms")

    # Validate all post-run hashes against the current bytes. A failed attempt
    # remains a validated failure record; changed inputs do not become a theorem result.
    for name, expected in after.items():
        p = Path(name[len("external:"):]).resolve() if name.startswith("external:") else (ROOT / name).resolve()
        if (not name.startswith("external:") and not p.is_relative_to(ROOT)) or not p.is_file() or digest(p) != expected:
            raise ValueError(f"saved input hash mismatch: {name}")
    return receipt


def validate_receipt_core(receipt, expected_declarations):
    if receipt.get("schema") != "pal-v24-batch-receipt-v2": raise ValueError("malformed saved receipt schema")
    if receipt.get("status") not in {"PASS_BOUNDED_LEAN_CHECKS", "FAILED_OR_BLOCKED", "FAILED_INPUTS_CHANGED"}:
        raise ValueError("saved receipt has an unknown or incomplete status")
    if receipt.get("declared") != expected_declarations:
        raise ValueError("saved declaration inventory mismatch")


def self_check():
    # Pure in-memory mutation guards. They never invoke Lean or Lake.
    declarations_expected = [{"name": "M.x", "kind": "theorem"}]
    signature = {"M.x": "@M.x : True"}
    axioms = {"M.x": []}
    input_keys = {"input-a", "input-b"}
    version_specs = [(f"version-{i}", [f"lake", str(i)]) for i in range(1, 4)]
    command_specs = [(name, [name]) for name in ("build-target", "check-axioms", "leanchecker-target")]
    def row(name, argv):
        return {"name": name, "argv": argv, "cwd": str(ROOT), "exit_code": 0}
    base = {"schema": "pal-v24-batch-receipt-v2", "status": "PASS_BOUNDED_LEAN_CHECKS",
            "inputs_unchanged": True, "input_hashes_before": {key: "0" * 64 for key in input_keys},
            "input_hashes_after": {key: "0" * 64 for key in input_keys},
            "declared": declarations_expected, "error": "", "versions": [row(*spec) for spec in version_specs],
            "commands": [row(*spec) for spec in command_specs], "signatures": signature, "axioms": axioms}
    def validate(item):
        validate_receipt_core(item, declarations_expected)
        validate_pass_inventory(item, declarations_expected, input_keys, version_specs, command_specs, signature, axioms)
    mutations = [
        ("schema", lambda x: x.update(schema="bad")),
        ("missing input", lambda x: x["input_hashes_after"].pop("input-b")),
        ("removed command", lambda x: x["commands"].pop()),
        ("added command", lambda x: x["commands"].append(row("extra", ["extra"]))),
        ("wrong command order", lambda x: x["commands"].reverse()),
        ("nonzero command exit", lambda x: x["commands"][1].update(exit_code=1)),
        ("forged signature", lambda x: x["signatures"].update({"M.x": "@M.x : False"})),
        ("forged axiom inventory", lambda x: x["axioms"].update({"M.x": ["Fake.axiom"]})),
        ("changed input inventory", lambda x: x["input_hashes_after"].update({"input-a": "1" * 64})),
    ]
    for label, mutate in mutations:
        item = json.loads(json.dumps(base)); mutate(item)
        try: validate(item)
        except ValueError: continue
        raise AssertionError(f"mutation guard failed to reject {label}")
    failed = json.loads(json.dumps(base))
    failed.update(status="FAILED_OR_BLOCKED", error="RuntimeError: bounded check failed",
                  inputs_unchanged=False, input_hashes_after={"input-a": "1" * 64})
    validate_receipt_core(failed, declarations_expected)
    print("PASS_PURE_PYTHON_MUTATION_GUARDS (receipt consistency only; no Lean/Lake execution)")


def main():
    if not __debug__: raise RuntimeError("Do not use Python -O; receipt validation uses assertions.")
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="verify a saved receipt and its files, without replay")
    group.add_argument("--run", action="store_true", help="run sequential local Lean checks and record a receipt")
    group.add_argument("--self-check", action="store_true", help="run Python-only mutation guards")
    parser.add_argument("--batch")
    parser.add_argument("--lake", help="absolute path to the lake executable (required with --run)")
    args = parser.parse_args()
    if args.self_check: self_check(); return 0
    if not args.batch: parser.error("--batch is required")
    batch_dir = (AREA / args.batch).resolve()
    if args.check:
        receipt = validate_saved(batch_dir)
        print(f"PASS_SAVED_RECEIPT_CHECK batch={receipt['batch']} status={receipt['status']} (no replay)")
        return 0
    if not args.lake or not Path(args.lake).is_absolute(): parser.error("--run requires --lake with an absolute path")
    return run_batch(args)


if __name__ == "__main__":
    raise SystemExit(main())
