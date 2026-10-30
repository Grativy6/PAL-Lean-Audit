# Adversarial self-review of the W00 projector extension

**Primary verdict: proved as written.** This verdict concerns the rational
submodule equivalence in TARGET.md and the two stated finite counterexamples.
Its interpretation as a geometric statement remains conditional on the named
source data. Review provenance: Hearthline self-review; no independent-agent or
human review claimed.

Exact audited source identities are in [verification.json](evidence/verification.json).
The audit is attached to those file hashes rather than a future commit. Base:
`bd49451caa409fe9091f209048afe814fa9aa30b`.

Dependency chain:

```
inherited sixth-power arithmetic + rational norm
          -> determinant nonzero for nonzero seed
inherited Cramer reconstruction
          -> explicit cyclic coefficients for G
Fρ coordinate action -> spectral P formula -> pure/nonzero/idempotent P
A stable under Fρ -> A stable under P
A stable under Fμ -> pure algebraic subspace stable under G
known line + those facts
          -> existing Bridge.conditionalWeilDetector_iff
          -> projector_generator_complete_iff
```

| Obligation | Finding | Status |
| --- | --- | --- |
| Domain and coefficients | Q × (Q × Q), rational submodule, linear maps; no implicit complex or integral extension | passed |
| Parameter normalization | rho and mu actions explicitly match the inherited norm-cubed/sixth-power formulas | passed |
| Projector is derived | Defined as `(1/54) • (27 • id − rhoAction)` and proved equal to `(0,w)` | passed |
| Nonzero/pure image | Projection onto an actual two-dimensional plane; explicit nonzero witness | passed |
| Stability | Rational submodule operations derive P-stability from the stated Fρ-stability | passed |
| Cyclicity | Nonzero seed gives positive/nonzero norm; determinant is 360 times that norm; Cramer coefficients reconstruct every target | passed |
| Main theorem is the intended consumer | The proof calls the inherited theorem with explicit P, G and all hypotheses | passed |
| Missing generator stability | Proper submodule contains the known line, is Fρ-stable and has a nonzero projected seed, yet fails Fμ-stability | passed; exact counterexample |
| Enlarged ambient-action claim | Mixed projector fails idempotence at a specified rational vector | passed; exact counterexample |
| Logical dependencies | All 17 outputs use only the permitted three standard axioms; no admission or custom axiom | passed |
| Historical preservation | Core proof, core audit, inherited interface and dependency pins unchanged from the base | passed |
| Geometric identification and actual cycle | Not constructed by this rational formalization | conditional application / outside this target |
| Global priority | Exact existing mechanisms identified; no global priority claim supported | not established |

The minimum nonzero seeds `(1,0)` and `(0,1)` are in the stated plane. At the
zero seed the cyclic premise is explicitly excluded; the main result requires
an actual nonzero projector output. Its forward implication uses that P is a
nonzero map. The known-line assumption is retained as a universal premise and
is not silently discharged by a coordinate example.

The wrong-space counterexample is a rational linear action. It refutes the
unrestricted projector promotion; it is not presented as a new construction
of a geometric cohomology group. Similarly, the proper-subspace counterexample
does not refute the main theorem because it fails its second stability premise.

The native compiler and bundled checker are pinned to Lean 4.32.1. The run reads
the retained Mathlib cache at the recorded Git revision; the focused GitHub
workflow separately obtains the repository's pinned dependencies. Neither
agreement with the ZIP nor a finite numerical test was substituted for a proof.

Mathematical proofreading self-review covered the new proof documentation,
notation and source links. Routine prose cleanup only; no mathematical-token
changes during proofreading. The initial compiler repairs were implementation
repairs recorded in RESULT.md, without weakening any statement.
