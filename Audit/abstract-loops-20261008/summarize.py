"""Render the current run summary from checked receipts, keeping inventory roles separate."""
from collections import Counter
import verify

AREA = verify.AREA

def main():
    integration = verify.read(AREA / "integration-results.json")
    if integration["status"] != "PASS_INTEGRATION":
        raise ValueError("Integration has not passed")
    batches = []
    for batch, module in verify.MODULES.items():
        verify.check(batch)
        receipt = verify.read(AREA / batch / "results.json")
        if verify.sha(AREA / batch / "results.json") != integration["receipts"][batch]:
            raise ValueError("Integration points to an older receipt")
        claims = verify.read(AREA / batch / "claims.json")
        roles = Counter(r["role"] for r in claims["declarations"])
        kinds = Counter(r["kind"] for r in claims["declarations"])
        batches.append({"batch": batch, "execution_state": receipt["status"],
            "source_groups": [g["id"] for g in claims["groups"]],
            "explicit_declarations": len(claims["declarations"]), "declaration_kinds": dict(kinds),
            "declaration_roles": dict(roles), "receipt": batch + "/results.json",
            "receipt_sha256": verify.sha(AREA / batch / "results.json"),
            "module": "Experiments." + module,
            "axiom_union": sorted({a for axioms in receipt["axioms"].values() for a in axioms})})
    result = {"schema": "abstract-loops-workshop-summary-v1", "local_date": "2026-10-08",
        "key": "MATH-SHELF-FIVE-PAPERS-v1", "activated_scope": ["AL-A", "AL-B", "AL-C"],
        "state": "COMPLETE_SELECTED_BATCHES", "batches": batches,
        "new_source_defects_found": [],
        "earlier_coverage_gaps_closed": ["C1 reachable-capacity obligations", "C5 arbitrary alternatives with finite reachable image"],
        "existing_evidence": {"C1": {"declarations": 19, "theorems": 9, "count_as_new": False},
                              "C5": {"declarations": 12, "theorems": 8, "count_as_new": False}},
        "review": "REVIEW.md", "clarifications": "CLARIFICATIONS.md",
        "readable_receipt_book": "RECEIPT_BOOK.md", "integration": "integration-results.json",
        "limits": ["Self-review, bundled kernel implementation", "No physical carrier generation, LQG, causal-baseline identification or implementation efficiency theorem", "No manuscript edit, source adoption, CI or publication"],
        "unactivated_key_batches": ["SCT-A", "SCT-B", "SCT-C", "CC-A", "CC-B", "CC-C", "GPPR-A", "GPPR-B", "GPPR-C", "FA-A"]}
    verify.write(AREA / "summary.json", result)
    print("COMPLETE_SELECTED_BATCHES", len(batches))

if __name__ == "__main__":
    main()
