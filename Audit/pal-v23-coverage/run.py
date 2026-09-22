"""Bounded source and Lean receipt runner for PAL v2.3 coverage supplement."""

from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, os, platform, re, subprocess, sys, time, zipfile
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
AREA = Path(__file__).resolve().parent
RESULT = AREA / "results.json"
LANES = (
    (
        "cadence",
        "Experiments.Pal23Cadence",
        "cadence-claims.json",
        "Experiments/Pal23CadenceAxioms.lean",
    ),
    (
        "interface",
        "Experiments.Pal23Interface",
        "interface-claims.json",
        "Experiments/Pal23InterfaceAxioms.lean",
    ),
    (
        "trace-replay",
        "Experiments.Pal23TraceReplay",
        "trace-claims.json",
        "Experiments/Pal23TraceReplayAxioms.lean",
    ),
)
PREDECESSOR = "71ef6bbb604664a1b5f8bce6ade08939e13bd286"
OPEN = {"O04": "OPEN", "O25": "OPEN", "D-FIRST-OCCURRENCE": "OPEN"}
ALLOWED = {"Classical.choice", "Quot.sound", "propext"}
NEW_FILES = (
    "Audit/pal-v23-coverage/.gitattributes",
    "Audit/pal-v23-coverage/RECEIPTS.md",
    "Audit/pal-v23-coverage/run.py",
    "Audit/pal-v23-coverage/source-manifest.json",
    "Audit/pal-v23-coverage/predecessor-lock.json",
    "Audit/pal-v23-coverage/potential-source-excerpts.json",
    "Audit/pal-v23-coverage/cadence-claims.json",
    "Audit/pal-v23-coverage/interface-claims.json",
    "Audit/pal-v23-coverage/trace-claims.json",
    "Audit/pal-v23-coverage/README.md",
    "Audit/pal-v23-coverage/COVERAGE.md",
    "Audit/pal-v23-coverage/OTHER-CANDIDATES.md",
    "Audit/pal-v23-coverage/SOURCE-CORRESPONDENCE.md",
    "Audit/pal-v23-coverage/REVIEW.md",
    "Audit/pal-v23-coverage/RELEASE-NOTES.md",
    "Audit/pal-v23-coverage/CADENCE-NOTES.md",
    "Audit/pal-v23-coverage/INTERFACE-NOTES.md",
    "Audit/pal-v23-coverage/TRACE-NOTES.md",
    "Experiments/Pal23Cadence.lean",
    "Experiments/Pal23CadenceAxioms.lean",
    "Experiments/Pal23Interface.lean",
    "Experiments/Pal23InterfaceAxioms.lean",
    "Experiments/Pal23TraceReplay.lean",
    "Experiments/Pal23TraceReplayAxioms.lean",
    ".github/workflows/pal-coverage.yml",
)


def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def sha(p, canon=False):
    b = Path(p).read_bytes()
    return hashlib.sha256(b.replace(b"\r\n", b"\n") if canon else b).hexdigest()


def rel(p):
    return Path(p).resolve().relative_to(ROOT).as_posix()


def write(p, x):
    Path(p).write_text(
        json.dumps(x, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def clean(path):
    from scripts.check_policy import (
        strip_lean_comments_and_strings,
        OMEGA_LITERAL_IDENTIFIER,
    )

    s = strip_lean_comments_and_strings(Path(path).read_text(encoding="utf-8"))
    assert not re.search(
        r"\b(sorry|admit|axiom|native_decide)\b", s
    ) and not OMEGA_LITERAL_IDENTIFIER.search(s)
    return s


def parse_axioms(path, names):
    rows = re.findall(
        r"'([^']+)' (does not depend on any axioms|depends on axioms: \[(.*?)\])",
        Path(path).read_text(encoding="utf-8"),
        re.S,
    )
    out = {}
    for n, form, items in rows:
        assert n not in out
        out[n] = (
            []
            if form.startswith("does not")
            else sorted(
                x.strip() for x in items.replace("\n", " ").split(",") if x.strip()
            )
        )
        assert set(out[n]) <= ALLOWED
    assert list(out) == names
    return out


def _check_excerpt_file(path, expected_hash=None):
    data = read(ROOT / path)
    if expected_hash:
        assert sha(ROOT / path, True) == expected_hash
    assert data["source_id"] == "PAL-v2.3-M"
    source = next(
        x
        for x in read(AREA / "source-manifest.json")["sources"]
        if x["id"] == "PAL-v2.3-M"
    )
    assert data["source_sha256"] == source["sha256"]
    paragraphs = data["paragraphs"]
    assert len({x["paragraph"] for x in paragraphs}) == len(paragraphs)
    return data


def source_data():
    manifest = read(AREA / "source-manifest.json")
    assert manifest["predecessor_head"] == PREDECESSOR
    primary_path = manifest.get(
        "source_excerpts", "Audit/pal-v23-roundtrip/source-excerpts.json"
    )
    primary_hash = manifest.get("source_excerpts_sha256")
    primary = _check_excerpt_file(primary_path, primary_hash)
    assert [x["paragraph"] for x in primary["paragraphs"]] == [
        f"P{i}" for i in range(1384, 1535)
    ]
    excerpts = [primary]
    context_path = manifest.get("context_file")
    if context_path:
        excerpts.append(
            _check_excerpt_file(context_path, manifest.get("context_sha256"))
        )
    prior = read(AREA.parent / "pal-v23-charter" / "source-manifest.json")
    prior_by_id = {
        x["id"]: x for x in prior["sources"] if x["id"].startswith("PAL-v2.3")
    }
    assert len(prior_by_id) == 5 == len(manifest["sources"])
    for src in manifest["sources"]:
        old = prior_by_id[src["id"]]
        assert (src["filename"], src["bytes"], src["sha256"]) == (
            old["filename"],
            old["bytes"],
            old["sha256"],
        )
    tags = {
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t",
        "{http://schemas.openxmlformats.org/officeDocument/2006/math}t",
    }
    for excerpt_file in excerpts:
        for row in excerpt_file["paragraphs"]:
            text = "".join(
                node.text or ""
                for node in ET.fromstring(row["ooxml"]).iter()
                if node.tag in tags
            )
            assert text == row["text"]
    return manifest, excerpts


def inventory():
    manifest, excerpts = source_data()
    source_rows = {row["paragraph"]: row for e in excerpts for row in e["paragraphs"]}
    all_claims, all_names, inventory_by_lane = [], [], {}
    required = {
        "id",
        "title",
        "classification",
        "declaration",
        "statement",
        "source_refs",
        "assumptions",
        "dependencies",
        "countercase",
        "authority_ceiling",
        "residual",
        "reopening",
    }
    classes = {
        "PROVED_FROM_DECLARED_RULES",
        "CONSISTENT_REALIZATION",
        "ASSUMPTION_BOUND",
        "COUNTERMODEL_TO_OVERCLAIM",
    }
    for slug, module, ledger_file, axioms_file in LANES:
        code = clean(ROOT / f"Experiments/{module.rsplit('.', 1)[1]}.lean")
        ledger = read(AREA / ledger_file)
        assert ledger["module"] == module and ledger["claims"]
        declarations = [
            f"{module}.{name}"
            for name in re.findall(
                r"^(?:noncomputable\s+)?(?:def|theorem|abbrev|inductive|structure)\s+(\w+)",
                code,
                re.M,
            )
        ]
        inductive_blocks = re.finditer(
            r"^inductive\s+(\w+)[^\n]*\n(.*?)(?=^(?:noncomputable\s+)?(?:def|theorem|abbrev|inductive|structure|namespace|end)\b|\Z)",
            code,
            re.M | re.S,
        )
        for block in inductive_blocks:
            declarations.extend(
                f"{module}.{block.group(1)}.{constructor}"
                for constructor in re.findall(r"^\s*\|\s+(\w+)", block.group(2), re.M)
            )
        claims = ledger["claims"]
        names = [row["declaration"] for row in claims]
        ids = [row["id"] for row in claims]
        assert (
            names and len(names) == len(set(names)) and set(names) == set(declarations)
        )
        assert len(ids) == len(set(ids))
        axcode = clean(ROOT / axioms_file)

        def qualified(source_name):
            # Commands inside `namespace Module` may use a local identifier;
            # receipts and claim ledgers bind the canonical fully qualified name.
            return (
                source_name
                if source_name.startswith(module + ".")
                else f"{module}.{source_name}"
            )

        checked = [
            qualified(name) for name in re.findall(r"^#check @?(\S+)", axcode, re.M)
        ]
        printed = [
            qualified(name)
            for name in re.findall(r"^#print axioms (\S+)", axcode, re.M)
        ]
        assert checked == names and printed == names
        for claim in claims:
            assert required <= claim.keys() and claim["classification"] in classes
            assert all(claim[key] for key in required - {"assumptions", "dependencies"})
            assert isinstance(claim["assumptions"], list) and isinstance(
                claim["dependencies"], list
            )
            for ref in claim["source_refs"]:
                assert ref["source_id"] == "PAL-v2.3-M"
                match = re.fullmatch(r"P(\d{4})(?:-P(\d{4}))?", ref["paragraphs"])
                assert match
                lo, hi = int(match[1]), int(match[2] or match[1])
                assert lo <= hi and all(
                    f"P{i}" in source_rows for i in range(lo, hi + 1)
                )
                quote = " ".join(ref["excerpt"].split())
                body = " ".join(
                    " ".join(
                        source_rows[f"P{i}"]["text"] for i in range(lo, hi + 1)
                    ).split()
                )
                assert quote and quote in body
        inventory_by_lane[slug] = {
            "module": module,
            "claims_file": ledger_file,
            "axioms_file": axioms_file,
            "declarations": names,
            "claims": claims,
        }
        all_claims.extend(claims)
        all_names.extend(names)
    ids = [claim["id"] for claim in all_claims]
    assert len(ids) == len(set(ids)) and len(all_names) == len(set(all_names))
    return manifest, excerpts, inventory_by_lane, all_claims, all_names


def inputs():
    lock = read(AREA / "predecessor-lock.json")
    prior = read(ROOT / "Audit/pal-v23-roundtrip/results.json")
    paths = set(lock["frozen_paths"]) | set(prior["inputs"]) | set(NEW_FILES)
    manifest = read(AREA / "source-manifest.json")
    for key in ("source_excerpts", "context_file"):
        if manifest.get(key):
            paths.add(manifest[key])
    paths.discard("Audit/pal-v23-coverage/results.json")
    return {path: sha(ROOT / path, True) for path in sorted(paths)}


def verify_predecessor():
    lock = read(AREA / "predecessor-lock.json")
    assert lock["predecessor_head"] == PREDECESSOR
    for p, h in lock["frozen_paths"].items():
        assert sha(ROOT / p, True) == h, p
    runpath = ROOT / "Audit/pal-v23-roundtrip/run.py"
    spec = importlib.util.spec_from_file_location("pal_roundtrip_prev", runpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    prior = mod.check_saved()
    return sha(runpath.with_name("results.json")), prior


def raw_sources(directory, manifest, excerpts):
    directory = Path(directory)
    counts = {}
    atlas = None
    for source in manifest["sources"]:
        path = directory / source["filename"]
        assert (
            path.is_file()
            and path.stat().st_size == source["bytes"]
            and sha(path) == source["sha256"]
        )
        with zipfile.ZipFile(path) as archive:
            assert archive.testzip() is None
            document = ET.fromstring(archive.read("word/document.xml"))
        paragraphs = document.findall(
            ".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"
        )
        assert len(paragraphs) == source["canonical_paragraph_count"], source["id"]
        counts[source["id"]] = len(paragraphs)
        if source["id"] == "PAL-v2.3-M":
            atlas = paragraphs
    assert atlas is not None
    for excerpt_file in excerpts:
        for row in excerpt_file["paragraphs"]:
            index = int(row["paragraph"][1:]) - 1
            assert ET.tostring(atlas[index], encoding="unicode") == row["ooxml"], row[
                "paragraph"
            ]
    return counts


def parse_signatures(path, names):
    text = Path(path).read_text(encoding="utf-8")
    escaped = [re.escape(name) for name in names]
    header = re.compile(
        r"^@?(" + "|".join(escaped) + r")(?:\.\{[^}]+\})?(?=\s|$)", re.M
    )
    axioms = re.compile(
        r"^'[^']+' (?:does not depend on any axioms|depends on axioms:)", re.M
    )
    starts = list(header.finditer(text))
    assert [match.group(1) for match in starts] == names, (
        f"Signature inventory mismatch in {Path(path).name}; "
        "inspection output must use the fully qualified ledger names"
    )
    result = {}
    for index, match in enumerate(starts):
        next_start = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        axiom_start = axioms.search(text, match.end(), next_start)
        stop = axiom_start.start() if axiom_start else next_start
        signature = text[match.start() : stop].strip()
        assert signature
        result[match.group(1)] = signature
    return result


def summary(receipt):
    counts = {}
    for classification in receipt["classifications"].values():
        counts[classification] = counts.get(classification, 0) + 1
    lines = [
        "# PAL v2.3 coverage receipt summary",
        "",
        f"Status: **{receipt['status']}**",
        "",
        f"Lean declaration population: {len(receipt['declarations'])} across three bounded modules.",
        "These declaration counts describe formal coverage and are not independent discoveries.",
        "",
        "Classification counts:",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in sorted(counts.items()))
    lines.extend(
        [
            "",
            f"Controller commands passed: {len(receipt['commands'])}.",
            f"Receipt rejection guards: {len(receipt.get('receipt_guards', []))} (controller checks, not theorems).",
            "",
            "Five source DOCX identities are hash-bound. Original DOCX and paragraph checks are local-only; CI checks committed snapshots.",
            "The prior roundtrip receipt is checked as saved evidence, not freshly replayed by this lane.",
            "This bounded coverage supplement does not amend or adopt PAL v2.3, establish full conformance, or close PAL obligations.",
            "O04, O25, and D-FIRST-OCCURRENCE remain OPEN.",
            "",
        ]
    )
    return "\n".join(lines)


def commands(lake, python):
    result = [
        ("lean-version", [lake, "env", "lean", "--version"]),
        ("build-project", [lake, "build"]),
    ]
    for slug, module, _ledger, axioms_file in LANES:
        result.append((f"build-{slug}", [lake, "build", module]))
        result.append((f"{slug}-axioms-signatures", [lake, "env", "lean", axioms_file]))
        result.append((f"{slug}-kernel", [lake, "env", "leanchecker", module]))
    result.extend(
        [
            ("pal-kernel", [lake, "env", "leanchecker", "PALLeanAudit"]),
            (
                "predecessor-saved-check",
                [python, "Audit/pal-v23-roundtrip/run.py", "--check"],
            ),
            (
                "pal-publication-check",
                [python, "Audit/pal-v23-charter/check_publication.py", "--check"],
            ),
            ("policy", [python, "scripts/check_policy.py"]),
            ("migration", [python, "scripts/check_release_migration.py"]),
            ("ar3-policy", [python, "scripts/check_attack_run_0003_policy.py"]),
            ("ar3", [python, "scripts/check_attack_run_0003.py"]),
            ("report", [python, "scripts/render_report.py", "--check"]),
            (
                "migration-report",
                [python, "scripts/render_migration_report.py", "--check"],
            ),
            ("ar3-report", [python, "scripts/render_attack_run_0003.py", "--check"]),
            ("diff-check", ["git", "diff", "--check"]),
        ]
    )
    return result


def execute(r, d):
    for label, argv in commands(r["lake"], r["python_executable"]):
        print("Running " + label, flush=True)
        start = time.monotonic()
        try:
            p = subprocess.run(
                argv,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=1500,
            )
            code, out = p.returncode, p.stdout
        except subprocess.TimeoutExpired as e:
            out = e.stdout or ""
            out = out.decode("utf-8", "replace") if isinstance(out, bytes) else out
            code = 124
            out += "\nEXECUTION_TIMEOUT\n"
        except OSError as e:
            code, out = 127, f"EXECUTION_ERROR: {e}\n"
        log = d / (label + ".txt")
        log.write_text(out.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
        r["commands"].append(
            {
                "label": label,
                "argv": argv,
                "exit_code": code,
                "log": rel(log),
                "sha256": sha(log),
                "elapsed_seconds": round(time.monotonic() - start, 6),
            }
        )
        if code:
            raise RuntimeError(f"{label} failed ({code})")


def formal_outputs(receipt_dir, by_lane):
    axioms, signatures = {}, {}
    for slug, info in by_lane.items():
        names = info["declarations"]
        log = receipt_dir / f"{slug}-axioms-signatures.txt"
        axioms.update(parse_axioms(log, names))
        signatures.update(parse_signatures(log, names))
    return axioms, signatures


def validate(r, manifest, lanes, claims, names, prevhash):
    assert r["status"] == "PASS_PAL_V23_COVERAGE"
    assert r["inputs"] == inputs() == r["input_after"]
    assert (
        r["predecessor_head"] == PREDECESSOR
        and r["predecessor_receipt_sha256"] == prevhash
    )
    assert (
        r["authority_ceiling"] == manifest["authority_ceiling"]
        and r["obligations"] == OPEN
    )
    assert r["declarations"] == names
    assert r["module_declarations"] == {
        slug: info["declarations"] for slug, info in lanes.items()
    }
    assert r["classifications"] == {
        claim["id"]: claim["classification"] for claim in claims
    }
    excerpt_hashes = {
        manifest.get(
            "source_excerpts", "Audit/pal-v23-roundtrip/source-excerpts.json"
        ): sha(
            ROOT
            / manifest.get(
                "source_excerpts", "Audit/pal-v23-roundtrip/source-excerpts.json"
            ),
            True,
        )
    }
    if manifest.get("context_file"):
        excerpt_hashes[manifest["context_file"]] = sha(
            ROOT / manifest["context_file"], True
        )
    assert r["source_excerpt_files_sha256"] == excerpt_hashes
    assert r["source_docx_sha256"] == {
        src["id"]: src["sha256"] for src in manifest["sources"]
    }
    expected_source = (
        {
            "performed": True,
            "paragraph_counts": {
                src["id"]: src["canonical_paragraph_count"]
                for src in manifest["sources"]
            },
        }
        if r["source_check"]["performed"]
        else {"performed": False, "paragraph_counts": {}}
    )
    assert r["source_check"] == expected_source
    assert r["scope_status"] == "BOUNDED_PAL_V23_COVERAGE_SUPPLEMENT"
    expected = commands(r["lake"], r["python_executable"])
    assert len(expected) == len(r["commands"])
    evidence = ROOT / r["evidence_directory"]
    for got, (label, argv) in zip(r["commands"], expected):
        assert got["label"] == label and got["argv"] == argv and got["exit_code"] == 0
        assert got["sha256"] == sha(evidence / (label + ".txt"))
        assert got["log"] == r["evidence_directory"] + "/" + label + ".txt"
        assert got["elapsed_seconds"] >= 0
    assert r["axioms"].keys() == set(names) and r["signature_outputs"].keys() == set(
        names
    )
    expected_axioms, expected_signatures = formal_outputs(evidence, lanes)
    assert (
        r["axioms"] == expected_axioms and r["signature_outputs"] == expected_signatures
    )
    assert r["mode"] in {"local", "replay"} and re.fullmatch(
        r"[a-f0-9]{40}", r["tested_checkout_sha"]
    )
    if r["mode"] == "local":
        assert r["ci_status"] == "NOT_RUN" and all(
            r[key] is None
            for key in (
                "github_run_id",
                "pr_head_sha",
                "tested_merge_sha",
                "ci_environment_claim",
            )
        )
    elif r["github_run_id"]:
        assert (
            r["ci_status"] == "GITHUB_ACTIONS_REPLAY"
            and r["ci_environment_claim"]
            == "GITHUB_ACTIONS environment variables; not independently attested"
            and r["tested_merge_sha"] == r["tested_checkout_sha"]
            and r["tested_merge_sha"] == os.getenv("GITHUB_SHA")
            and os.getenv("GITHUB_ACTIONS") == "true"
        )
        assert (
            re.fullmatch(r"[a-f0-9]{40}", r["pr_head_sha"] or "")
            and r["clean_worktree"]
        )
    else:
        assert (
            r["ci_status"] == "LOCAL_REPLAY"
            and r["pr_head_sha"] is None
            and r["tested_merge_sha"] is None
            and r["ci_environment_claim"] is None
        )
    assert r["clean_worktree"] == (not bool(r["worktree_status"].strip()))


def guards(r, manifest, lanes, claims, names, prevhash):
    validate(r, manifest, lanes, claims, names, prevhash)
    kernel_index = next(
        i for i, row in enumerate(r["commands"]) if row["label"] == "cadence-kernel"
    )
    tests = {
        "missing-command": lambda x: x["commands"].pop(),
        "duplicate-command": lambda x: x["commands"].append(
            copy.deepcopy(x["commands"][0])
        ),
        "failed-kernel": lambda x: x["commands"][kernel_index].update(exit_code=1),
        "wrong-argv": lambda x: x["commands"][0].update(argv=["wrong"]),
        "bad-log": lambda x: x["commands"][0].update(sha256="0" * 64),
        "wrong-input": lambda x: x["inputs"].update({"lean-toolchain": "0" * 64}),
        "wrong-after-input": lambda x: x["input_after"].update(
            {"lean-toolchain": "0" * 64}
        ),
        "bad-axioms": lambda x: x["axioms"].clear(),
        "bad-signature": lambda x: x["signature_outputs"].clear(),
        "bad-source": lambda x: x["source_check"].update(
            performed=not x["source_check"]["performed"]
        ),
        "bad-predecessor": lambda x: x.update(predecessor_receipt_sha256="0" * 64),
        "invented-ci": lambda x: x.update(ci_status="INVENTED_CI"),
        "bad-mode": lambda x: x.update(mode="invented"),
        "closed-obligation": lambda x: x["obligations"].update(O04="CLOSED"),
        "promoted-authority": lambda x: x.update(authority_ceiling="ADOPTED"),
        "bad-declaration": lambda x: x["declarations"].pop(),
        "bad-classification": lambda x: x["classifications"].clear(),
    }
    for name, mutate in tests.items():
        bad = copy.deepcopy(r)
        mutate(bad)
        try:
            validate(bad, manifest, lanes, claims, names, prevhash)
        except (AssertionError, KeyError):
            continue
        raise AssertionError("receipt guard accepted " + name)
    return sorted(tests)


def run(args, replay=False):
    manifest, excerpts, lanes, claims, names = inventory()
    prevhash, _ = verify_predecessor()
    frozen = check_saved() if replay else None
    counts = (
        raw_sources(args.source_dir, manifest, excerpts) if args.source_dir else None
    )
    evidence = (
        args.output_dir
        or AREA
        / "evidence"
        / datetime.now(timezone.utc).strftime("attempt-%Y%m%dT%H%M%S%fZ")
    ).resolve()
    assert not evidence.exists()
    evidence.mkdir(parents=True)
    checkout = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    ci = bool(
        replay
        and os.getenv("GITHUB_ACTIONS") == "true"
        and os.getenv("GITHUB_RUN_ID")
        and os.getenv("GITHUB_SHA")
    )
    excerpt_hashes = {
        manifest.get(
            "source_excerpts", "Audit/pal-v23-roundtrip/source-excerpts.json"
        ): sha(
            ROOT
            / manifest.get(
                "source_excerpts", "Audit/pal-v23-roundtrip/source-excerpts.json"
            ),
            True,
        )
    }
    if manifest.get("context_file"):
        excerpt_hashes[manifest["context_file"]] = sha(
            ROOT / manifest["context_file"], True
        )
    receipt = {
        "schema_version": "1.0",
        "status": "RUNNING",
        "mode": "replay" if replay else "local",
        "lake": args.lake,
        "python_executable": sys.executable,
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "tested_checkout_sha": checkout,
        "tested_merge_sha": checkout if ci else None,
        "pr_head_sha": os.getenv("PAL_COVERAGE_PR_HEAD_SHA") if ci else None,
        "github_run_id": os.getenv("GITHUB_RUN_ID") if ci else None,
        "ci_environment_claim": (
            "GITHUB_ACTIONS environment variables; not independently attested"
            if ci
            else None
        ),
        "platform": platform.platform(),
        "python": sys.version,
        "inputs": inputs(),
        "declarations": names,
        "module_declarations": {
            slug: info["declarations"] for slug, info in lanes.items()
        },
        "classifications": {claim["id"]: claim["classification"] for claim in claims},
        "obligations": OPEN.copy(),
        "predecessor_head": PREDECESSOR,
        "predecessor_receipt_sha256": prevhash,
        "source_excerpt_files_sha256": excerpt_hashes,
        "source_docx_sha256": {src["id"]: src["sha256"] for src in manifest["sources"]},
        "source_check": {
            "performed": bool(args.source_dir),
            "paragraph_counts": counts or {},
        },
        "scope_status": "BOUNDED_PAL_V23_COVERAGE_SUPPLEMENT",
        "authority_ceiling": manifest["authority_ceiling"],
        "evidence_directory": rel(evidence),
        "commands": [],
        "axioms": {},
        "signature_outputs": {},
        "ci_status": (
            "GITHUB_ACTIONS_REPLAY" if ci else "LOCAL_REPLAY" if replay else "NOT_RUN"
        ),
    }
    succeeded = False
    try:
        execute(receipt, evidence)
        receipt["axioms"], receipt["signature_outputs"] = formal_outputs(
            evidence, lanes
        )
        if frozen is not None:
            assert receipt["declarations"] == frozen["declarations"]
            assert receipt["axioms"] == frozen["axioms"]
            assert receipt["signature_outputs"] == frozen["signature_outputs"]
        receipt["status"] = "PASS_PAL_V23_COVERAGE"
        receipt["input_after"] = inputs()
        receipt["worktree_status"] = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True
        )
        receipt["clean_worktree"] = not bool(receipt["worktree_status"].strip())
        receipt["receipt_guards"] = guards(
            receipt, manifest, lanes, claims, names, prevhash
        )
        succeeded = True
    except Exception as exc:
        receipt["status"] = "FAILED_PAL_V23_COVERAGE"
        receipt["error"] = str(exc)
        raise
    finally:
        receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
        receipt.setdefault("input_after", inputs())
        receipt.setdefault(
            "worktree_status",
            subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=ROOT, text=True
            ),
        )
        receipt.setdefault(
            "clean_worktree", not bool(receipt["worktree_status"].strip())
        )
        write(evidence / "execution.json", receipt)
    if succeeded and not replay:
        summary_path = AREA / "SUMMARY.md"
        temporary_summary = summary_path.with_suffix(".md.tmp")
        temporary_summary.write_text(summary(receipt), encoding="utf-8", newline="\n")
        temporary_summary.replace(summary_path)
        write(RESULT, receipt)
    print(receipt["status"])


def check_saved():
    manifest, excerpts, lanes, claims, names = inventory()
    prevhash, _ = verify_predecessor()
    receipt = read(RESULT)
    validate(receipt, manifest, lanes, claims, names, prevhash)
    assert receipt["receipt_guards"] == guards(
        receipt, manifest, lanes, claims, names, prevhash
    )
    assert read(ROOT / receipt["evidence_directory"] / "execution.json") == receipt
    assert (AREA / "SUMMARY.md").read_text(encoding="utf-8") == summary(receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--replay", action="store_true")
    group.add_argument("--check-inputs", action="store_true")
    parser.add_argument("--lake", default="lake")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--source-dir", type=Path)
    args = parser.parse_args()
    if args.check or args.check_inputs:
        inventory()
        verify_predecessor()
        inputs()
        if args.source_dir:
            manifest, excerpts = source_data()
            counts = raw_sources(args.source_dir, manifest, excerpts)
            if args.check:
                assert check_saved()["source_check"] == {
                    "performed": True,
                    "paragraph_counts": counts,
                }
        if args.check and not args.source_dir:
            check_saved()
        print(
            "PASS_PAL_V23_COVERAGE_RECEIPTS"
            if args.check
            else "PASS_PAL_V23_COVERAGE_INPUTS"
        )
    else:
        run(args, args.replay)


if __name__ == "__main__":
    main()
