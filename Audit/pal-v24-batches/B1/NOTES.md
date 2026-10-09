# B1 — finite continuation profile

## Status

Development module and explicit `#check` / `#print axioms` inspection are present. The target module build completed successfully with `C:\Users\cdpan\.elan\bin\lake.exe build Experiments.Pal24Continuation`; the inspection module also typechecked with `lake env lean Experiments/Pal24ContinuationAxioms.lean`. No final receipt was run. The only theorem axiom reported is Lean's permitted `propext`, used by the two proposition-valued simulation results and their fixture application; all definitions and `run_append` report no axioms. The aperture theorem is kernel-checked and its newly admitted `[true]` suffix refutes the widened universal predicate.

Candidate layout metadata is still being repaired, so `claims.json` intentionally has an empty `source_inputs` array for development. Before final receipt, bind the exact frozen v2.4 Mechanical Structural Spine and Mathematical Realization Atlas byte hashes from `Audit/pal-v24-candidate/source-manifest.json`, and verify the target tree against that freeze. Do not treat this development build as source-bound evidence.

Development build failures were proof-script/authoring errors, not counterexamples: an unavailable arithmetic tactic; an escaped newline accidentally left in Lean source; an already-closed contradiction goal followed by an extra tactic; and a malformed tuple type annotation. These were corrected. The final target build and inspection module pass.

## Formal result and scope

`TransitionProfile` declares state, input, answer observation, deterministic transition, and an input-only aperture. `run_append` proves finite-run composition. `one_suffix_of_step_simulation` proves an answer equality for one admitted finite suffix from a supplied initial relation, output agreement, and per-admitted-input relation preservation. `all_finite_suffixes_of_step_simulation` lifts the same premises to every finite suffix admitted by this exact profile. This distinguishes a selected suffix from universal quantification over the encoded aperture; it does not show that a particular restore operation meets the premises.

`aperture_expansion_distinguishes_future` gives two unequal `Nat × Bool` states with the same current Nat answer. They agree on every finite narrow-aperture suffix and on the selected widened suffix `[false]`; adding `true` admits `[true]`, which yields different answers. Thus equality for one tested suffix and even universal equality over a narrower aperture do not establish equality over a changed aperture or exact state recovery.

## Reused predecessor evidence (references, not copied claims)

- MIND v0.4 protected `Work` explicitly includes account, pending evidence, fixed rule, and receipts; its `OperationalState` additionally includes fuel, context, and administrative count. Relevant existing declarations: `Experiments.MindContinuation.prefix_checkpoint_resume`, `checkpoint_resume_preserves_continuation`, `dropping_rule_changes_continuation_fixture`, `dropping_pending_from_capsule_changes_continuation_fixture`, `capsule_omits_operational_state_fixture`, `stale_context_rejected_fixture`, `admin_exhausts_fuel_and_starves_fixture`, `insufficient_fuel_leaves_pending_fixture`, `nonmatching_evidence_fixture`, and `inconsistent_receipt_delta_fixture`.
- PAL v2.3 predecessor declarations: `Experiments.Pal23Roundtrip.same_suffix_under_work_roundtrip`, `fiber_constant_does_not_validate_faulty_thaw`, `natBool_stable_but_not_recovered`, `natBool_first_answer_preserved`, `natBool_second_answer_not_preserved`, and `natBool_chosen_suffix_vs_other_suffix`.
- These predecessor results are not reclassified or counted as new B1 theorems. Their own prior scope and evidence remain version-bound.

## Source routes

- Mechanical Structural Spine SC-22.1–SC-22.3: distinguish selected answer, protected continuation state, and continuation equivalence; declare the finite horizon/input aperture; avoid overclaiming from a selected probe.
- Mathematical Realization Atlas M-CONTINUATION-PROFILE: route D40/O63/T73 and v2.3 anchors P0071–P0073, P0157–P0160, P0206–P0212, P0668–P0693, and P1472–P1502.
- Obligation and Decision Ledger D40/O63 and Conformance Tests T73: keep answer equality, exact state recovery, and aperture-wide continuation equivalence distinct; require omission, changed-aperture, faulty-decoder, and distinguishing-suffix countercases.
- The exact source files and hashes remain pending the source freeze. These routes are candidate-document addresses, not adoption or authority.

## Generalization assumptions and residuals

The formal universal result quantifies only finite lists, only the fixed profile's state-independent `admits` predicate, and only under caller-supplied simulation premises. Generalizing to state-dependent enabled inputs requires representing each state's enabled set and proving compatible enabledness/transition preservation; otherwise the same suffix may not be available from both states. Generalizing beyond finite suffixes needs an additional infinite-run/coinductive argument and any required progress or fairness premises. Applying this result to checkpoint restoration requires proving the restore's result is related to the original state, that its observation agrees, and that the relation survives every admitted step under the same task/version/dependencies and transition semantics.

The fixture's unequal whole states formalize why a selected answer is weaker than exact work recovery only for this declared projection. To infer full state from answer equality, the observation would need to be injective on the reachable/protected domain. The MIND predecessor separately shows that preserving `Work` does not preserve fuel, context, or administrative state; successful continuation also needs adequate fresh resources and guard checks. Its retained receipt can record a processed event/rule with no account increment, so unchanged account count is not equivalent to no recorded processing. These distinctions stay within the reduced deterministic models: they prove no full MIND/cognition claim, physical storage property, contextual authority, source authenticity, universal external-task permission, or PAL adoption.
