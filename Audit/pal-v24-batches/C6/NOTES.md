# C6 — Task-relative quotient of finite histories

This batch follows PAL v2.3-M Atlas paragraphs P0807–P0821. The source document, extraction, and exact paragraph excerpts are bound by SHA-256 in `claims.json`.

The staged Lean module models histories as every finite list over a supplied alphabet, continuations as every finite list, and task observation as a supplied total function. `futureEquivalent` compares observations under every finite suffix. The reflexive, symmetric, and transitive results make it a Setoid; common finite right extension preserves the relation by append associativity. The quotient classes and observation-descending map are explicit, with class equality characterized exactly by future-equivalence.

A restricted continuation aperture is represented by a predicate on suffixes. The restricted right-congruence theorem requires closure under prefixing the appended task symbol as an explicit premise. No closure is inferred. `aperture_closure_is_load_bearing` supplies a finite counterfixture: the empty-suffix aperture admits `[]` and rejects `[false]`; length-divided-by-two observation makes `[]` and `[false]` equivalent on it but distinguishes `[false]` and `[false, false]` after common extension. This does not refute universal finite-suffix right congruence or the closure-conditional theorem. No history-indexed aperture is represented.

A constant Boolean task yields a subsingleton quotient, which demonstrates that quotienting alone does not prove nontrivial work or usefulness. The head-reading fixture separates the empty history from a one-symbol history. Replacing the task observation changes whether that same pair is equivalent.

The statements do not prove Myhill–Nerode minimality, decidability, efficiency, application-level source adequacy, reachable-image decoder existence, totalization, decoder-class separation, aperture stability across task changes, or forget-to-A8. The module makes no physical, cognitive, authority, or execution claim.

This remains staged. It has no final batch receipt or controller-approved promotion into `Experiments/`.
