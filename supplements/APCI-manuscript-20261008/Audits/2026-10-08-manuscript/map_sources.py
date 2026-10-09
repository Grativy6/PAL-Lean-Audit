"""Check the published inventory and preserve exact APCI source locators."""
from pathlib import Path
import hashlib
import json
import re

AREA = Path(__file__).resolve().parent
ROOT = AREA.parents[1]
REPO = ROOT / "Lean project"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


inventory = load(REPO / "THEOREM_INVENTORY.json")["declarations"]
rows = load(AREA / "document-tables.json")[1]["rows"][1:]
receipt = (ROOT / "Receipts/2026-10-08-local-replay/logical-dependencies.log").read_text()
pairs = re.findall(
    r"'([^']+)' (?:does not depend on any axioms|depends on axioms:\s*\[(.*?)\])",
    receipt, re.S)
deps = {name: sorted(v.strip() for v in values.split(",") if v.strip())
        for name, values in pairs}
assert len(inventory) == len(rows) == len(deps) == 15
targets = [
    ("T2", [53, 54]), ("T1", [48, 49]), ("T1", [48, 49]), ("T1", [48, 50]),
    ("T2", [53, 54]), ("T2-inhabited", [52, 55]), ("T3", [59, 62]),
    ("T4", [64, 66]), ("T5", [67, 70]), ("T5", [67, 70]),
    ("T5", [67, 70]), ("empty-boundary", [56, 57]),
    ("empty-boundary", [56, 57]), ("finite-control", [120, 120]),
    ("finite-control", [120, 120]),
]
declarations = []
for entry, row, (claim, span) in zip(inventory, rows, targets, strict=True):
    name = entry["name"]
    assert "APCILeanAudit." + row[1] == name
    assert row[2].upper() == entry["source_target"]
    printed = [] if row[3] == "none" else sorted(x.strip() for x in row[3].split(","))
    assert printed == deps[name]
    matches = []
    for file in sorted((REPO / "APCILeanAudit").glob("*.lean")):
        for line, text in enumerate(file.read_text(encoding="utf-8").splitlines(), 1):
            if re.match(r"theorem\s+" + re.escape(name.split(".")[-1]) + r"\b", text):
                matches.append((file.relative_to(ROOT).as_posix(), line))
    assert len(matches) == 1
    declarations.append({"name": name, "published_id": row[0],
        "docx_table": "T02", "pdf_page": 12, "claim": claim,
        "docx_paragraphs": [f"P{n:04d}" for n in span],
        "file": matches[0][0], "line": matches[0][1],
        "logical_dependencies": deps[name], "inventory_match": True})

source_records = []
for entry in load(ROOT / "source-manifest.json")["sources"]:
    path = ROOT / "Sources" / Path(entry["path"]).name
    assert sha(path) == entry["sha256"]
    source_records.append({"path": path.relative_to(ROOT).as_posix(),
        "sha256": sha(path), "bytes": path.stat().st_size})

supplement = load(ROOT / "Receipts/2026-10-08-manuscript-check-01/result.json")
claims = [
    {"id":"T1", "source":"§3; PDF p4; P0048-P0050", "verdict":"proved as written",
     "statement":"For arbitrary W,T,Q, exact decoding on Reachable(trace) iff FiberConstant(trace,answer).",
     "hypotheses":["Classical logic in the reverse direction; reachable subtype, not all T"],
     "evidence":["A02","A03","A04"], "new_coverage":False},
    {"id":"T2", "source":"§3.1; PDF pp4-5; P0052-P0057", "verdict":"proved as written",
     "statement":"Exact total decoder iff fiber constancy and Nonempty(T -> Q).",
     "hypotheses":["Classical logic; all empty-type cases retained"],
     "evidence":["A01","A05","A06","A12","A13"], "new_coverage":False},
    {"id":"T3", "source":"§3.2; PDF p5; P0059-P0062", "verdict":"proved as written",
     "statement":"A left inverse implies injectivity; this is identity recovery, not arbitrary property certification.",
     "hypotheses":["One decoder is a left inverse on every input"],
     "evidence":["A07"], "new_coverage":False},
    {"id":"T4", "source":"§4; PDF p5; P0064-P0066", "verdict":"proved as written",
     "statement":"Equal traces remain equal under any deterministic function of that trace.",
     "hypotheses":["Fixed original trace; no fresh side input"],
     "evidence":["A08"], "new_coverage":False},
    {"id":"T5", "source":"§4; PDF p5; P0067-P0070", "verdict":"proved as written",
     "statement":"For all n : Nat, any Fin(n+1) -> Fin n has a collision and no left inverse.",
     "hypotheses":["Fixed finite codomain; n=0 retained and its map assumption is impossible"],
     "evidence":["A09","A10","A11","A14","A15"], "new_coverage":False},
    {"id":"finite-answer-corollary", "source":"§4.1; PDF p6; P0072-P0073", "verdict":"proved as written",
     "statement":"An injective labeling of Reachable(trace) into Fin n plus n+1 witnesses with pairwise-distinct answers rules out an exact decoder even restricted to their reachable traces.",
     "hypotheses":["Capacity is on actual reachable traces","Injective(answer composed with witness)","No assumption that W or T is finite"],
     "evidence":["APCIManuscript.no_exact_on_witness_of_capacity"], "new_coverage":True},
    {"id":"property-control", "source":"§2 and §7.1; PDF pp4,7; P0044,P0097", "verdict":"proved as written",
     "statement":"A one-point trace on Nat still exactly certifies a constant Boolean property.",
     "evidence":["APCIManuscript.infinite_world_constant_property"], "kind":"boundary control"},
    {"id":"side-information-control", "source":"§2 and §7.3; PDF pp3,7; P0039,P0101", "verdict":"proved as written",
     "statement":"A constant trace cannot recover a Boolean identity, but appending that bit as side information can.",
     "evidence":["APCIManuscript.side_information_changes_interface"], "kind":"boundary control"},
    {"id":"empty-total-control", "source":"§3.1; PDF pp4-5; P0052-P0056", "verdict":"proved as written",
     "statement":"For W=T=Q=Empty, an exact total decoder exists, so inhabited Q is sufficient rather than necessary.",
     "evidence":["APCIManuscript.empty_trace_allows_empty_answer"], "kind":"boundary control"},
    {"id":"entropy", "source":"§6; PDF p7; P0091-P0093", "verdict":"conditional on a named input",
     "statement":"H(X|Y) >= log2(m)-log2(n) for finite uniform X and deterministic Y of support size at most n.",
     "hypotheses":["m>=1 and n>=1, implicit in the existence of these distributions","Finite Shannon entropy chain rule and support-size maximum bound"],
     "evidence":["Written algebra in RECEIPT_BOOK.md; no Lean entropy formalization or new external-source verification"]},
    {"id":"physical-application", "source":"§5 and §9; PDF pp6,9-10; P0079-P0084,P0148-P0150", "verdict":"conditional on a named input",
     "statement":"A concrete complete-access model and a conflicting-answer collision imply failure of exact trace-only certification.",
     "hypotheses":["Actual operational interface and distinguishability model","All retained side information included","Always conclusive exact decoding","Separately justified physical capacity if using finite argument"],
     "evidence":["T1 and T4 supply abstract implication only"]},
]
output = {
    "schema":"apci-manuscript-source-map-v1", "date":"2026-10-08",
    "scope":"APCI only", "review_type":"self-review; no independent reviewer",
    "primary_verdict":{"target":"Theorems 1-5 and section 4.1 of APCI v1.0.0", "verdict":"proved as written"},
    "sources":source_records,
    "locator_convention":"P numbers count direct word/document.xml body/w:p including blank paragraphs. T numbers count direct body/w:tbl. Extracted OMML text is navigation only; equations also inspected in PDF pp4-7.",
    "original_repository":{"commit":supplement["commit"],"tree":supplement["tree"],"unchanged":supplement["original_repository_unchanged"]},
    "original_declarations":declarations, "claims":claims,
    "supplementary_dependencies":supplement["dependencies"],
    "supplement_sha256":supplement["supplement_sha256"],
    "receipts":["Receipts/2026-10-08-local-replay/receipt.json","Receipts/2026-10-08-manuscript-check-01/result.json","Receipts/2026-10-08-manuscript-check-01/manifest.json"],
    "out_of_scope":["thermodynamic literature and empirical bridge validation","stochastic or quantum extensions","novelty/priority","historical CI live status and artifact download","unavailable predecessor archive bytes","all other keyring lanes"],
    "receipt_byte_note":{"git_blob_matches_paper":True,"sha256":supplement["historical_receipt_git_blob_sha256"],"checkout_difference":"Windows CRLF only; original bytes not rewritten"},
}
(AREA / "SOURCE_MAP.json").write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("PASS: all 15 Appendix A names, targets and logical dependencies match.")
print("Saved APCI-only source map; 5 core theorems, 1 new corollary, 3 boundary controls.")
