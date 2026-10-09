# Compactification Costs v0.2 — workshop receipt book

All three selected batches passed local builds, exact statement/axiom inspections and bundled Lean kernel replays on 8 October 2026. These are selected source-mapped results, not verification of every claim or interpretation in the paper.

| Batch | New checked coverage | Evidence |
| --- | --- | --- |
| CC-A | Dense-interior argument derives boundary preservation and surjectivity; compact-to-Hausdorff quotient supplies a unique continuous decoder. | [Review](../CC-A/REVIEW.md) · [Receipt](../CC-A/results.json) · [Lean](../../../Experiments/CompactificationBoundary.lean) |
| CC-B | Exact conflict refinement, question coarsening, empty extension and undefined detector controls, quotient descent, compatible extension/detector transport, telescoping. | [Review](../CC-B/REVIEW.md) · [Receipt](../CC-B/results.json) · [Lean](../../../Experiments/CompactificationProfile.lean) |
| CC-C | Side-label lower bound; actual complex cube projection and edges; six-channel mean and five-dimensional kernel; sector/residual recovery with tie policy. | [Review](../CC-C/REVIEW.md) · [Receipt](../CC-C/results.json) · [Lean](../../../Experiments/CompactificationFixtures.lean) |

The topology has a useful sharper boundary: dense embeddings and Hausdorff uniqueness do the boundary-preservation work. Compactness and openness enter later to obtain a compact boundary and continuous decoder. All used assumptions remain in the checked signatures. The manuscript's stronger package remains sufficient.

The geometric maps were constructed rather than replaced with desired quotient properties. In particular the integer cube coordinates were bridged injectively to exp(2*pi*i/3). The one-bit result is about its two discrete central vertices. Phase recovery is modulo a full turn; the source excludes ties and the implementation assigns ties to the upper sector. Empty extensions, undefined detectors and lost answers remain separate cases.

No source correction surfaced in these selected claims. Ordinary fiber lifting uses the same mathematical mechanism as the existing APCI result and is not independent corroboration. Lens integration, Euler triangulation identities, and analytic extension examples remain optional unselected follow-ups with their additional prerequisites listed in the CC-C review. None is claimed proved here.

Inventories: CC-A 10 declarations / 8 theorems; CC-B 19 / 16; CC-C 33 / 23. Counts include definitions, supporting lemmas and controls; they are not counts of independent paper claims. Only standard Lean axioms occur. The [source manifest](../source-manifest.json) fixes the retained v0.2 DOCX/PDF and extracts; [batch targets](../TARGETS.md) separate the manuscript from the bounded realizations. No manuscript edit, adoption, publication or fresh CI run is implied.
