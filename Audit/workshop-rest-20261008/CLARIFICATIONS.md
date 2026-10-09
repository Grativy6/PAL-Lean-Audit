# Clarifications for Chris

This is the cross-paper account for the activated remainder of the five-paper key. Manuscripts were not edited. Existing Abstract Loops clarifications remain in [their earlier account](../abstract-loops-20261008/CLARIFICATIONS.md). The items below distinguish mathematical corrections, existing conditions and coverage limits.

## GPPR G06: specify what a ribbon root promises

**Fixture qualification / wording to tighten.** Appendix B, G06 expects two event orders with the same factor multiset to have the same endpoint and distinct event-ribbon roots. Proposition 1's endpoint/path distinction is sound. Distinct exact ordered records, however, do not by themselves guarantee distinct finite hashes. An actual root representation, the tested pair and an integrity/collision assumption are needed for that expected hash result.

Recommended clarification: "same endpoint; distinct ordered event receipts; root distinction checked under the declared root representation and integrity assumptions." A finite hash should not be promoted to unconditional exact identity. GPPR §10 already disclaims security claims, so this is a local fixture qualification, not a reason to discard the endpoint theorem. GPPR-C's collision controls and pair-specific injectivity condition provide the decisive formal comparison. No production hash implementation was tested in this workshop.

## Golden transcendence: external theorem versus checked dependency

**Library coverage gap, not a discovered source error.** GPPR §3.3 and Theorem 1 use the complex Gelfond-Schneider theorem correctly at the declared logarithm branch. The [primary-source record](GPPR-A/LITERATURE.md) verifies the needed theorem/convention via Ricci 1935. The Lean specialization explicitly takes GelfondSchneiderRealExponent as a hypothesis. Its golden arithmetic, algebraic irrational exponent and branch identity are checked; the long transcendence theorem itself is outside the kernel dependency closure.

Do not describe this receipt as an unconditional Lean proof of golden transcendence. Closing that remaining formal dependency would require a checked Gelfond-Schneider development or an equivalent checked result. The literature-supported mathematics and the conditional Lean theorem can both be reported, with their different evidence routes visible.

## Compactification: where the assumptions enter

**Conditions already present; useful sharpening.** CC Lemma 1 and Theorem 1: dense embeddings plus Hausdorff uniqueness establish boundary preservation; surjectivity of the comparison map establishes boundary onto. Compactness and an open resolved interior supply a compact boundary for the quotient/continuous-decoder step. Some source assumptions are stronger than necessary for individual steps. No manuscript correction is required.

**Implementation convention.** CC §6.3 excludes sector ties. The formal fixture assigns a tie to the upper sector and uses a half-open residual interval. It also recovers phase modulo a turn, not an absolute unwrapped angle. An implementation should declare its own tie rule. This is an explicit extension at a source-excluded boundary.

**Domain condition already present.** CC §6.1 and Proposition 6: the one-bit hub result concerns the two discrete vertices 000/111. Its proof does not transfer to a solid cube's line-segment fibers. The actual complex projection and discrete edge counts were checked.

**Optional research remains.** Lens signed-area integration, Euler boundary incidence formulas and analytic extension classes were optional follow-ups in the key. They need their separate oriented parameterizations, surface/triangulation hypotheses or function classes. They were not required to complete the three selected CC batches and are not claimed covered.

## Single-Cut Transport: keep the local account local

**Conditions already present.** SCT §§2-5 and §9: filled selected corridors preserve charge, punctures do not; natural unused-capacity arithmetic is valid only when the row is feasible; zero slack is compatible with both orientations. The complete local gadget counts agree with the source. No selected-claim correction was found. A global reduction, minimality and priority remain separate work.

## Finite Abstraction: name the uniformity burden precisely

**Conditions already present.** P0009-P0025 distinguish fixed finite capacity from finite descriptions and growing finite records. A finite unary record for each natural number is injective despite every individual record being finite. The checked quantifier counterexample concerns a single common bound, not the existence of a choice function: its pointwise witnesses actually have the uniform formula n+1. This guards against accidentally turning the synthesis into an objection to finite proofs or a claim about P versus NP.

No source adoption, publication or amendment follows from this account. Failed proof tactics were retained as development evidence and were not relabeled mathematical counterexamples.
