# SCT-A self-review

Primary verdict: **proved as written within the explicit finite rank realization** for SCT-01/02. The source's Boolean endpoint charge is the specialization e=0 or 1 of a proved natural-charge extension. Actual accepted signatures and dependencies are in results.json.

Dependency graph: supplied bijective rank order -> finite support image/cardinality and realized hull positions -> interval cardinality minus selected cardinality -> serial min/max/card -> exact endpoint decomposition. No conclusion is supplied as a structure field or premise.

Obligations: nonempty support and clause subset passed; empty/singleton controls passed; all hull ranks lie in the ordered carrier passed; one-hole support has the stated two-block form passed; actual interval/disjoint-union counting passed. Primitive PAL interpretation and full reduction are out of scope.

Evidence: SingleCutSpan.lean; 18 explicit declarations including 14 theorems (helpers and controls included); successful module build, exact signature/axiom inspection, bundled kernel replay and saved receipt validation. Only standard Lean axioms permitted. Failed development attempts were library lemma/API errors, retained in development/, not mathematical counterexamples.

No manuscript defect found in the selected claims. This is self-review; the bundled checker is not an independent kernel implementation. Local formal evidence does not amend the manuscript or its release status.
