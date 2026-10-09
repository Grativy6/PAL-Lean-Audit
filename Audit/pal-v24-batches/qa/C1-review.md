# Independent review: C1 Abstract Loops joint certification

Review scope: static comparison of `Experiments/AbstractLoopsJoint.lean`, its `#check`/`#print axioms` module, `Audit/pal-v24-batches/C1/claims.json`, `NOTES.md`, and the preserved source excerpts P0014–P0026. No Lean execution or source edits were performed.

## Verdict

The explicit Lean model and advertised claims are appropriately bounded and materially correspond to the cited source. I found no counterexample to the encoded theorems and no material quantifier/domain strengthening beyond the declared ordinary total-function realization. The 19 explicit declarations appear to have one-for-one ledger rows and same-order inspection directives. The model is a consistent functional realization of the Abstract Loops source, not a proof of its empirical, causal, coalition, or finite-capacity interpretations.

## Claim-to-source audit

- `kernel`, `jointTrace`, `Reachable`, and `Certifies` (Lean lines 9–19) instantiate P0014–P0016 directly: arbitrary `World`, trace, and answer types; the image is represented by a subtype carrying an actual preimage witness; and decoding is required only on that reachable subtype. This correctly avoids a total decoder over impossible ambient trace values.
- `joint_kernel_eq_intersection` (21–25) proves P0018 for ordinary functions with the same domain. The two sides are binary relations on `World`, and the proof establishes extensional equality. It does not infer capacity or causal interaction.
- `reachable_certifies_iff_kernel_subset` (27–43) matches P0017/P0019. The forward direction uses equality of trace values to identify the two reachable subtype elements; the reverse direction chooses a world preimage of each reachable value and applies answer constancy on each fiber. `Classical.choice` is disclosed in the claim ledger and inspection file. Its result is existence of an unrestricted set-theoretic decoder on reachable values; computability or constrained decoders are expressly residual.
- `common_collision_blocks_joint_certification` (45–54) is the exact shared q-conflicting collision obstruction of P0024. It assumes both component collisions and a conflicting answer, so it does not confuse individual insufficiency with joint insufficiency.
- The Boolean-pair definitions and XOR declarations (56–80) match P0023: the answer is Boolean inequality/XOR, coordinate traces are projections, and the paired trace is the identity pair. Explicit collisions refute each single-coordinate decoder, while the paired reachable decoder computes XOR. This is a finite functional example only.
- The constant-trace/first-bit fixture and joint obstruction (82–93) instantiate P0024's negative boundary; the pair is collapsed by both traces while answers differ. Ledger descriptions stay fixture-specific.

P0025–P0026's fixed finite capacity inequality is explicitly OPEN_MANUAL and absent from the Lean declarations, as C1 notes. The model also appropriately avoids identifying a product-codomain size with reachable-pair cardinality or implying sufficiency from a capacity bound.

## Limits and handoff note

The source excerpt gives direct support for all cited clauses. The corpus source path/hash is recorded in the ledger, and the separate extracted excerpt records that identity and the paragraph text. This review did not authenticate the external source or independently recompute its hash. The runner issue reported in `runner-review.md` affects saved-receipt validation generally; additionally the currently absent candidate source-manifest file blocks a new runner invocation. Neither issue changes the logical correspondence verdict above.
