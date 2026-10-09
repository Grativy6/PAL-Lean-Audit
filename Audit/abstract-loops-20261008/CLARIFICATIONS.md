# Clarifications for Chris

No confirmed manuscript defect was found in the selected Abstract Loops v1.0
claims. These distinctions already appear in the paper. The checks give them
receipts rather than creating a reason to rewrite the source.

| Item | Category | Source and evidence | Possible editorial use |
| --- | --- | --- | --- |
| Finite reachable image is weaker than finitely many alternatives. | Limitation of the earlier encoding, now resolved | P0014, P0045-P0046; `finite_trace_initialized_kernel_stabilizes`. The final initializer is defined only on reachable traces. | Describe the receipt as closing the C5 coverage gap, not correcting the paper. |
| At most m-1 strict losses does not mean stabilization by time m-1. | Condition already present, worth emphasizing | P0045-P0046; `finite_image_merge_budget` and `merge_can_be_arbitrarily_late`. | A single sentence separating number of merges from their timing may help readers. No new assumption is needed. |
| A branch that happens to work is weaker than one uniformly correct trace-only protocol. | Condition already present, checked directly | P0048, P0058; deterministic/nondeterministic protocol theorems and the Boolean branch counterexample. | Keep the universal quantifier and nonempty allowed-output condition visible in implementations. |
| Raw surplus, observable surplus, and strict enlargement are different. | Condition already present, checked directly | P0051-P0057; hidden-coordinate and incomparable-support counterexamples. | Useful as a short example when introducing the baseline/readout distinction. |
| A new address is not by itself a qualified new carrier. | Proposed criterion remains an explicit input | P0081-P0086; roster-tag counterfixtures and the separate persistent source-copy model. | Retain the existing identity, cut, persistence, provenance and matching requirements. The model does not prove that these criteria are physically satisfied. |
| The information ceiling follows every varying input actually supplied. | Condition already present, checked directly | P0087-P0089; `varying_environment_defeats_narrow_ceiling` and the fixed-environment positive counterpart. | Preserve the full initializer in any later implementation or experiment; do not silently drop its environment/resource coordinates. |

No manuscript changes are proposed as necessary. General carrier adequacy,
physical interpretation, and the cost of a real implementation are separate
research questions, rather than failures hidden by the present checks.
