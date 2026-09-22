# M-INTERFACE-FIBER coverage lane

**Status: local formal coverage, not PAL adoption or a new release.** This supplement addresses the previously unchecked relation-level claims in PAL v2.3 Atlas M-INTERFACE-FIBER. It does not change earlier receipts or claim that prior artifacts automatically count toward a future release.

The source identity and literal paragraph quotations are recorded in `interface-claims.json` against the supplied PAL v2.3 Atlas snapshot. The principal targets are P1387 (the lost-distinction relation), P1389 (auxiliary-label intersection and collision postprocessing), P1395 (deterministic restatement, answer coarsening, and the finite label bound), and P1408 (the XOR joint-trace fixture).

The Lean module defines `lostDistinctions` and `labelKernel`, proves the joint-label intersection identity, proves that deterministic trace postprocessing preserves existing loss and may enlarge it, proves deterministic restatement equality, and proves the answer-coarsening inclusion. Finite fixtures demonstrate strict coarsening and XOR insufficiency under either coordinate with joint sufficiency. The finite lower-bound theorem is conditional on a finite indexed family, one common trace value, pairwise distinct answers, and joint sufficiency; it proves the label map injective on that family and bounds its cardinality by the label type. It does not by itself compute the maximum over all reachable trace fibers stated in P1395.

All types and maps are unstructured and total. The XOR result establishes only the stated Boolean function factorization. It establishes no causal interaction, generation, computability cost, privacy, consent, permission, standing, jurisdiction, or authority. The reachable decoder remains distinct from extension to the ambient trace codomain; no totalization is added here.

The saved signature/axiom module checks every declaration in the same order as the claim inventory. A targeted Lean build is the implementation check for this lane; broader release, CI, exhaustive conformance, and publication receipts remain separate.
