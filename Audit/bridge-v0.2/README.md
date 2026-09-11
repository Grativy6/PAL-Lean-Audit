# BRIDGE v0.2 — Lean endpoint supplement

**Author and steward:** Christopher D. Pang  
**Controlling manuscript:** *BRIDGE: Binding Residue and Information Dynamics of Generative Export*, v0.2  
**Reserved DOI:** 10.5281/zenodo.22699551  
**Lean / Mathlib:** 4.32.1 / 4.32.1

This supplement turns the manuscript's finite-dimensional endpoint calculus into
kernel-checked Lean statements. Its affirmative content is:

| ID | Lean declaration | Checked content |
|---|---|---|
| BR-LA-01 | `Bridge.dualCollisionSpace` | Dual collisions are exactly annihilators of the generated range. |
| BR-LA-02 | `Bridge.quotientDualEquivDualCollision` | The exact defect dual `(T / range e)∗` is linearly equivalent to the dual-collision kernel. |
| BR-LA-03 | `Bridge.generativeDefect_iff_dualCollision` | Failure of generation is equivalent to a collision under pullback of dual probes. |
| BR-LA-04 | `Bridge.readoutCollision_iff_differenceInKernel` | Equal readout is equivalent to an invisible difference. |
| BR-LA-05 | `Bridge.appendedTrace_determines_iff` | A base readout plus appended trace determines an authority map exactly under the common-kernel criterion. |
| BR-LA-06 | `Bridge.deterministicTranslator_unique` | A surjective bridge fixes any downstream deterministic translator uniquely. |
| BR-LA-07 | `Bridge.oneScalarProbe_separatesHiddenLine` | One scalar probe exists for every nonzero hidden line. |
| BR-LA-08 | `Bridge.zeroProbe_notInjectiveOnHiddenLine` | The predecessor countercase: a probe vanishing on the direction cannot separate its line. |
| BR-LA-09 | `Bridge.fourSector_quotient_finrank` | The four actual quotient-sector dimensions sum to the target dimension. |

## Assumption and dependency account

- BR-LA-01 through BR-LA-08 are stated over a field and modules.
- BR-LA-07 uses Mathlib's algebraic dual-separation theorem
  `Module.Projective.exists_dual_eq_one`; the vector-space projectivity instance
  supplies its choice-dependent witness.
- BR-LA-09 additionally assumes the target is finite-dimensional and uses the
  Grassmann dimension formula.
- Every declaration has a `#print axioms` command in
  `Audit/BridgeEndpoint.lean`, and the repository's build, policy check, and
  `leanchecker` workflow are the verification gate.

## Authority ceiling

These results certify the exact Lean propositions above. They establish the
linear endpoint mechanism used by BRIDGE, including its necessity/sufficiency
kernel criterion and its minimal one-line probe result. The companion does not
encode the Hodge decomposition, compatible-polarization identities,
Hodge–Riemann sign input, algebraicity of a field action, or existence of the
cycle required by the manuscript's conditional Weil-class detector. Those
remain separate mathematical dependencies.

This branch is an AI-assisted formalization proposal. Merge, source adoption,
and any claim transfer remain Christopher D. Pang's decisions.
