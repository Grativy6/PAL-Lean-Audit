# Source correspondence and bounded claims

Source: the supplied BRIDGE v0.4 DOCX, SHA256 `a13d91a728ab6da2a5654b3263a595242397d7fb8edb17cffafdcf32036a2470`. Paragraph IDs enumerate every `w:p` in `word/document.xml`, including empty and table paragraphs. The preserved snapshots contain the original OOXML as well as readable text; flattened equation text does not replace the OOXML.

P0107 states: “A requested answer q:W→Q is decodable exactly when it is constant on these fibers, subject to APCI’s stated reachable-versus-total codomain boundary.” The paragraph explicitly distinguishes the arbitrary-answer lane from the linear lane. This batch specializes that general principle to the generated span, rather than claiming a new theorem for every corpus adapter.

P0195 states: “For APCI applied to the generated span with trace r|B, C is the collision space for full identity recovery; for a coarser answer it is an obstruction only where that answer varies.” Only this first clause is the new source target. The later residual-space clause belongs to the preceding audit.

| Source object or obligation | Exact interpretation in this batch | Boundary |
|---|---|---|
| P0036, P0087: supplied field and endpoint instance | Vector spaces over a field, supplied submodule `B`, linear `r : T → R` | `B` represents `im e`; constructing generators is not required for these theorems |
| P0195: trace `r|B` | `r.comp B.subtype`, corestricted to its actual range | No enlargement to all ambient readouts is implicit |
| P0107/P0195: requested answer | Arbitrary function `a : B → A` | No linear structure on the answer type is needed for the function theorem |
| P0195: varies on a collision | For all `x,y ∈ B`, `r x = r y` implies `a x = a y` | Checking only the fiber over zero is insufficient for arbitrary answers |
| Linear specialization | For a linear answer, `generatedCollision B r.ker ≤ a.ker` | Kernel notation is not applied to arbitrary functions |
| Full identity recovery | A left inverse on reachable readouts recovers elements of `B` | It does not recover the original generator domain `G` without a condition on `e` |
| Reachable decoder uniqueness | Two decoders satisfying the answer equation agree on the entire reachable range | Unreachable ambient points are not constrained by that equation |

The arbitrary answer theorem uses classical preimage selection. Its factorization is nevertheless unique on the reachable range; this should not be confused with uniqueness of a representative or a total extension. The linear factorization uses the quotient-kernel equivalence and no finite-dimensional hypothesis. Mathematical existence does not assert executable reconstruction, computability, persistence, or a preferred complementary subspace.

The examples in [the claim ledger](claims.json) check stronger readings of these statements. They are not counterexamples to the source's explicitly bounded principle. Definitions, equivalent formulations, and their boundary examples share dependencies and must not be counted as independent discoveries.

Historical evidence is preserved by [the predecessor lock](predecessor-lock.json). [The improvement note](IMPROVEMENTS.md) corrects an overstatement in the preceding generated summary without rewriting its original receipt. The new disposition in [CLOSURE.json](CLOSURE.json) applies only to the local P0195 formalization gap; it changes no PAL obligation or source-adoption status.
