# SCT-C self-review

Primary verdict: **proved as written** for the finite local OR realization. The numerical counts are independently implemented bounded computations, with self-review, not an independent mathematical authority.

Dependency graph: structural list-permutation enumerator -> coverage of exactly all Perm(range 7) lists and no duplicates -> actual row-position sets and hull charges, prefix slack as a proved missing-position count -> accepted truth table by kernel reduction -> existential local OR statement. All three supplied witnesses pass separately.

Obligations: exactly 5040 permutations, 8 truth triples, all three H sets and U sets copied from source P0113/P0115, source witness orders P0123/P0125/P0127, no hidden symmetry filter, no sampled extrapolation. The Python enumerator computes holes directly and cross-checks span/slack arithmetic. All source counts agree: 000:0, 001:8, 010:4, 011:28, 100:2, 101:12, 110:14, 111:50.

The first Lean route used the library's well-founded permutation implementation, whose reduction got stuck under decide. The structurally recursive equivalent List.permutations' was used instead, with library proofs of equivalence, coverage and no duplicates. No native decision axiom was used: `decide +kernel` is kernel reduction, and final #print axioms and bundled replay passed. The failed route is retained as tooling evidence, not a counterexample.

No selected source defect found. Full reduction, slot forcing, minimality and priority are outside this result. The receipt's declaration count includes definitions, helpers, witnesses and the two source/predicate comparison lemmas.
