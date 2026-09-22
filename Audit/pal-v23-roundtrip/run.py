"""Bounded source and Lean receipt runner for PAL v2.3 roundtrip supplement."""

from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, os, platform, re, subprocess, sys, time, zipfile
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
AREA = Path(__file__).resolve().parent
RESULT = AREA / "results.json"
MODULE = "Experiments.Pal23Roundtrip"
PREDECESSOR = "13108ed8f71f8a94e8fbed1cab3ac1323b984bd6"
OPEN = {"O04": "OPEN", "O25": "OPEN", "D-FIRST-OCCURRENCE": "OPEN"}
ALLOWED = {"Classical.choice", "Quot.sound", "propext"}
NEW_FILES = (
    "Audit/pal-v23-roundtrip/.gitattributes",
    "Audit/pal-v23-roundtrip/RECEIPTS.md",
    "Audit/pal-v23-roundtrip/run.py",
    "Audit/pal-v23-roundtrip/source-manifest.json",
    "Audit/pal-v23-roundtrip/source-excerpts.json",
    "Audit/pal-v23-roundtrip/predecessor-lock.json",
    "Audit/pal-v23-roundtrip/claims.json",
    "Audit/pal-v23-roundtrip/IMPLEMENTATION.md",
    "Audit/pal-v23-roundtrip/README.md",
    "Audit/pal-v23-roundtrip/SOURCE-CORRESPONDENCE.md",
    "Audit/pal-v23-roundtrip/PROPOSED-v2.3.1.md",
    "Audit/pal-v23-roundtrip/REVIEW.md",
    "Experiments/Pal23Roundtrip.lean",
    "Experiments/Pal23RoundtripAxioms.lean",
    ".github/workflows/pal-roundtrip.yml",
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


def source_data():
    m = read(AREA / "source-manifest.json")
    assert m["predecessor_head"] == PREDECESSOR
    e = read(ROOT / m["source_excerpts"])
    assert sha(ROOT / m["source_excerpts"], True) == m["source_excerpts_sha256"]
    assert e["source_id"] == "PAL-v2.3-M" and e["source_sha256"] == next(
        x["sha256"] for x in m["sources"] if x["id"] == "PAL-v2.3-M"
    )
    assert [x["paragraph"] for x in e["paragraphs"]] == [
        f"P{i}" for i in range(1384, 1535)
    ]
    prior = read(AREA.parent / "pal-v23-charter" / "source-manifest.json")
    prior_by_id = {
        x["id"]: x for x in prior["sources"] if x["id"].startswith("PAL-v2.3")
    }
    assert len(prior_by_id) == 5 == len(m["sources"])
    for src in m["sources"]:
        old = prior_by_id[src["id"]]
        assert (src["filename"], src["bytes"], src["sha256"]) == (
            old["filename"],
            old["bytes"],
            old["sha256"],
        )
    texttags = {
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t",
        "{http://schemas.openxmlformats.org/officeDocument/2006/math}t",
    }
    for row in e["paragraphs"]:
        assert (
            "".join(
                x.text or ""
                for x in ET.fromstring(row["ooxml"]).iter()
                if x.tag in texttags
            )
            == row["text"]
        )
    return m, e


def inventory():
    manifest, excerpts = source_data()
    source = {x["paragraph"]: x for x in excerpts["paragraphs"]}
    code = clean(ROOT / "Experiments/Pal23Roundtrip.lean")
    claims = read(AREA / "claims.json")
    assert claims["module"] == MODULE and claims["claims"]
    decls = [
        f"{MODULE}.{x}"
        for x in re.findall(
            r"^(?:noncomputable\s+)?(?:def|theorem|abbrev)\s+(\w+)", code, re.M
        )
    ]
    names = [c["declaration"] for c in claims["claims"]]
    ids = [c["id"] for c in claims["claims"]]
    assert (
        names
        and len(names) == len(set(names))
        and set(names) == set(decls)
        and len(ids) == len(set(ids))
    )
    ax = clean(ROOT / "Experiments/Pal23RoundtripAxioms.lean")
    assert (
        re.findall(r"^#print axioms (\S+)", ax, re.M) == names
        and re.findall(r"^#check @(\S+)", ax, re.M) == names
    )
    req = {
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
    for c in claims["claims"]:
        assert (
            req <= c.keys()
            and c["classification"] in classes
            and all(c[k] for k in req - {"assumptions", "dependencies"})
        )
        assert (
            isinstance(c["assumptions"], list)
            and isinstance(c["dependencies"], list)
            and c["source_refs"]
        )
        for ref in c["source_refs"]:
            assert ref["source_id"] == "PAL-v2.3-M"
            mm = re.fullmatch(r"P(\d{4})(?:-P(\d{4}))?", ref["paragraphs"])
            assert mm
            lo, hi = int(mm[1]), int(mm[2] or mm[1])
            assert 1384 <= lo <= hi <= 1534
            quote = " ".join(ref["excerpt"].split())
            body = " ".join(
                " ".join(source[f"P{i}"]["text"] for i in range(lo, hi + 1)).split()
            )
            assert quote and quote in body
    return manifest, excerpts, claims, names


def inputs():
    lock = read(AREA / "predecessor-lock.json")
    prior_path = ROOT / "Audit/bridge-v04-generated-recovery/results.json"
    prior = read(prior_path)
    paths = set(lock["frozen_paths"]) | set(prior["inputs"]) | set(NEW_FILES)
    paths.discard("Audit/pal-v23-roundtrip/results.json")
    return {p: sha(ROOT / p, True) for p in sorted(paths)}


def verify_predecessor():
    lock = read(AREA / "predecessor-lock.json")
    assert lock["predecessor_head"] == PREDECESSOR
    for p, h in lock["frozen_paths"].items():
        assert sha(ROOT / p, True) == h, p
    runpath = ROOT / "Audit/bridge-v04-generated-recovery/run.py"
    spec = importlib.util.spec_from_file_location("pal_roundtrip_prev", runpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    prior = mod.check_saved()
    return sha(runpath.with_name("results.json")), prior


def raw_sources(directory, manifest, excerpts):
    directory = Path(directory)
    counts = {}
    atlas = None
    for s in manifest["sources"]:
        p = directory / s["filename"]
        assert p.is_file() and p.stat().st_size == s["bytes"] and sha(p) == s["sha256"]
        with zipfile.ZipFile(p) as z:
            assert z.testzip() is None
            doc = ET.fromstring(z.read("word/document.xml"))
        paras = doc.findall(
            ".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"
        )
        assert len(paras) == s["canonical_paragraph_count"], s["id"]
        counts[s["id"]] = len(paras)
        if s["id"] == "PAL-v2.3-M":
            atlas = paras
    assert atlas is not None
    for row in excerpts["paragraphs"]:
        assert (
            ET.tostring(atlas[int(row["paragraph"][1:]) - 1], encoding="unicode")
            == row["ooxml"]
        ), row["paragraph"]
    return counts


def parse_signatures(path, names):
    text = Path(path).read_text(encoding="utf-8")
    escaped = [re.escape(name) for name in names]
    header = re.compile(r"^@?(" + "|".join(escaped) + r")(?:\.\{[^}]+\})?(?=\s|$)", re.M)
    axioms = re.compile(
        r"^'[^']+' (?:does not depend on any axioms|depends on axioms:)", re.M
    )
    starts = list(header.finditer(text))
    assert [match.group(1) for match in starts] == names
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
        "# PAL v2.3 roundtrip supplement receipt summary",
        "",
        f"Status: **{receipt['status']}**",
        "",
        f"Lean declaration population: {len(receipt['declarations'])}.",
        "Includes definitions, related formulations and shared countercase components; these are not independent discoveries.",
        "One anonymous unstructured-answer type-checking fixture is separate from that population.",
        "",
        "Classification counts:",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in sorted(counts.items()))
    lines += [
        "",
        f"Controller commands passed: {len(receipt['commands'])}.",
        f"Receipt rejection guards: {len(receipt.get('receipt_guards', []))} (controller checks, not theorems).",
        "",
        "Five source DOCX identities are hash-bound. Original DOCX and paragraph checks are local-only; CI checks committed snapshots.",
        "The predecessor receipt is checked as saved evidence, not freshly replayed by this lane.",
        "This is a bounded formal supplement only; it does not amend or adopt PAL v2.3, establish full conformance, or close PAL obligations.",
        "O04, O25 and D-FIRST-OCCURRENCE remain OPEN.",
        "",
    ]
    return "\n".join(lines)


def commands(lake, python):
    return [
        ("lean-version", [lake, "env", "lean", "--version"]),
        ("build-project", [lake, "build"]),
        ("build-roundtrip", [lake, "build", MODULE]),
        (
            "roundtrip-axioms-signatures",
            [lake, "env", "lean", "Experiments/Pal23RoundtripAxioms.lean"],
        ),
        ("roundtrip-kernel", [lake, "env", "leanchecker", MODULE]),
        ("pal-kernel", [lake, "env", "leanchecker", "PALLeanAudit"]),
        (
            "predecessor-saved-check",
            [python, "Audit/bridge-v04-generated-recovery/run.py", "--check"],
        ),
        ("pal-publication-check", [python, "Audit/pal-v23-charter/check_publication.py", "--check"]),
        ("policy", [python, "scripts/check_policy.py"]),
        ("migration", [python, "scripts/check_release_migration.py"]),
        ("ar3-policy", [python, "scripts/check_attack_run_0003_policy.py"]),
        ("ar3", [python, "scripts/check_attack_run_0003.py"]),
        ("report", [python, "scripts/render_report.py", "--check"]),
        ("migration-report", [python, "scripts/render_migration_report.py", "--check"]),
        ("ar3-report", [python, "scripts/render_attack_run_0003.py", "--check"]),
        ("diff-check", ["git", "diff", "--check"]),
    ]


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


def validate(r, m, claims, names, prevhash):
    assert (
        r["status"] == "PASS_PAL_V23_ROUNDTRIP"
        and r["inputs"] == inputs() == r["input_after"]
    )
    assert (
        r["predecessor_head"] == PREDECESSOR
        and r["predecessor_receipt_sha256"] == prevhash
        and r["authority_ceiling"] == m["authority_ceiling"]
        and r["obligations"] == OPEN
    )
    assert r["declarations"] == names and r["classifications"] == {
        c["id"]: c["classification"] for c in claims["claims"]
    }
    assert r["source_excerpts_sha256"] == m["source_excerpts_sha256"]
    assert r["source_docx_sha256"] == {s["id"]: s["sha256"] for s in m["sources"]}
    expected_source = (
        {
            "performed": True,
            "paragraph_counts": {
                s["id"]: s["canonical_paragraph_count"] for s in m["sources"]
            },
        }
        if r["source_check"]["performed"]
        else {"performed": False, "paragraph_counts": {}}
    )
    assert r["source_check"] == expected_source
    assert r["scope_status"] == "BOUNDED_PAL_V23_ATLAS_ROUNDTRIP_SUPPLEMENT"
    expected = commands(r["lake"], r["python_executable"])
    assert len(expected) == len(r["commands"])
    ev = ROOT / r["evidence_directory"]
    for got, (label, argv) in zip(r["commands"], expected):
        assert (
            got["label"] == label
            and got["argv"] == argv
            and got["exit_code"] == 0
            and got["sha256"] == sha(ev / (label + ".txt"))
            and got["log"] == r["evidence_directory"] + "/" + label + ".txt"
            and got["elapsed_seconds"] >= 0
        )
    assert r["axioms"] == parse_axioms(
        ev / "roundtrip-axioms-signatures.txt", names
    ) and r["signature_outputs"] == parse_signatures(
        ev / "roundtrip-axioms-signatures.txt", names
    )
    assert r["mode"] in {"local", "replay"} and re.fullmatch(
        r"[a-f0-9]{40}", r["tested_checkout_sha"]
    )
    if r["mode"] == "local":
        assert r["ci_status"] == "NOT_RUN" and all(
            r[x] is None for x in ("github_run_id", "pr_head_sha", "tested_merge_sha")
        )
    elif r["github_run_id"]:
        assert (
            r["ci_status"] == "GITHUB_ACTIONS_REPLAY"
            and r["tested_merge_sha"] == r["tested_checkout_sha"]
            and re.fullmatch(r"[a-f0-9]{40}", r["pr_head_sha"] or "")
            and r["clean_worktree"]
        )
    else:
        assert (
            r["ci_status"] == "LOCAL_REPLAY"
            and r["pr_head_sha"] is None
            and r["tested_merge_sha"] is None
        )
    assert r["clean_worktree"] == (not bool(r["worktree_status"].strip()))


def guards(r, m, c, n, h):
    validate(r, m, c, n, h)
    tests = {
        "missing-command": lambda x: x["commands"].pop(),
        "duplicate-command": lambda x: x["commands"].append(
            copy.deepcopy(x["commands"][0])
        ),
        "failed-kernel": lambda x: x["commands"][4].update(exit_code=1),
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
            validate(bad, m, c, n, h)
        except (AssertionError, KeyError):
            continue
        raise AssertionError("receipt guard accepted " + name)
    return sorted(tests)


def run(a, replay=False):
    m, e, c, n = inventory()
    prevhash, _ = verify_predecessor()
    frozen = check_saved() if replay else None
    counts = raw_sources(a.source_dir, m, e) if a.source_dir else None
    d = (
        a.output_dir
        or AREA
        / "evidence"
        / datetime.now(timezone.utc).strftime("attempt-%Y%m%dT%H%M%S%fZ")
    ).resolve()
    assert not d.exists()
    d.mkdir(parents=True)
    checkout = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    ci = bool(replay and os.getenv("GITHUB_RUN_ID"))
    r = {
        "schema_version": "1.0",
        "status": "RUNNING",
        "mode": "replay" if replay else "local",
        "lake": a.lake,
        "python_executable": sys.executable,
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "tested_checkout_sha": checkout,
        "tested_merge_sha": checkout if ci else None,
        "pr_head_sha": os.getenv("PAL_ROUNDTRIP_PR_HEAD_SHA") if ci else None,
        "github_run_id": os.getenv("GITHUB_RUN_ID") if ci else None,
        "platform": platform.platform(),
        "python": sys.version,
        "inputs": inputs(),
        "declarations": n,
        "classifications": {x["id"]: x["classification"] for x in c["claims"]},
        "obligations": OPEN.copy(),
        "predecessor_head": PREDECESSOR,
        "predecessor_receipt_sha256": prevhash,
        "source_excerpts_sha256": m["source_excerpts_sha256"],
        "source_docx_sha256": {src["id"]: src["sha256"] for src in m["sources"]},
        "source_check": {
            "performed": bool(a.source_dir),
            "paragraph_counts": counts or {},
        },
        "scope_status": "BOUNDED_PAL_V23_ATLAS_ROUNDTRIP_SUPPLEMENT",
        "authority_ceiling": m["authority_ceiling"],
        "evidence_directory": rel(d),
        "commands": [],
        "axioms": {},
        "signature_outputs": {},
        "ci_status": (
            "GITHUB_ACTIONS_REPLAY" if ci else "LOCAL_REPLAY" if replay else "NOT_RUN"
        ),
    }
    try:
        execute(r, d)
        r["axioms"] = parse_axioms(d / "roundtrip-axioms-signatures.txt", n)
        r["signature_outputs"] = parse_signatures(
            d / "roundtrip-axioms-signatures.txt", n
        )
        if frozen is not None:
            assert (
                r["declarations"] == frozen["declarations"]
                and r["axioms"] == frozen["axioms"]
                and r["signature_outputs"] == frozen["signature_outputs"]
            )
        r["input_after"] = inputs()
        r["worktree_status"] = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True
        )
        r["clean_worktree"] = not bool(r["worktree_status"].strip())
        r["status"] = "PASS_PAL_V23_ROUNDTRIP"
        r["receipt_guards"] = guards(r, m, c, n, prevhash)
    except Exception as exc:
        r["status"] = "FAILED_PAL_V23_ROUNDTRIP"
        r["error"] = str(exc)
        raise
    finally:
        r["finished_utc"] = datetime.now(timezone.utc).isoformat()
        r.setdefault("input_after", inputs())
        r.setdefault(
            "worktree_status",
            subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=ROOT, text=True
            ),
        )
        r.setdefault("clean_worktree", not bool(r["worktree_status"].strip()))
        write(d / "execution.json", r)
    if not replay:
        write(RESULT, r)
        (AREA / "SUMMARY.md").write_text(summary(r), encoding="utf-8", newline="\n")
    print(r["status"])


def check_saved():
    m, e, c, n = inventory()
    h, _ = verify_predecessor()
    r = read(RESULT)
    validate(r, m, c, n, h)
    assert (
        r["receipt_guards"] == guards(r, m, c, n, h)
        and read(ROOT / r["evidence_directory"] / "execution.json") == r
    )
    assert (AREA / "SUMMARY.md").read_text(encoding="utf-8") == summary(r)
    return r


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--run", action="store_true")
    g.add_argument("--check", action="store_true")
    g.add_argument("--replay", action="store_true")
    g.add_argument("--check-inputs", action="store_true")
    p.add_argument("--lake", default="lake")
    p.add_argument("--output-dir", type=Path)
    p.add_argument("--source-dir", type=Path)
    a = p.parse_args()
    if a.check or a.check_inputs:
        inventory()
        verify_predecessor()
        inputs()
        if a.source_dir:
            manifest, excerpts = source_data()
            counts = raw_sources(a.source_dir, manifest, excerpts)
            if a.check:
                assert check_saved()["source_check"] == {
                    "performed": True,
                    "paragraph_counts": counts,
                }
        if a.check and not a.source_dir:
            check_saved()
        print(
            "PASS_PAL_V23_ROUNDTRIP_RECEIPTS"
            if a.check
            else "PASS_PAL_V23_ROUNDTRIP_INPUTS"
        )
    else:
        run(a, a.replay)


if __name__ == "__main__":
    main()
