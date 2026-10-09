# Independent review — PAL v2.4 candidate B1

**Scope:** Read-only review of `Experiments/Pal24Continuation.lean`, `Experiments/Pal24ContinuationAxioms.lean`, `Audit/pal-v24-batches/B1/claims.json`, `Audit/pal-v24-batches/B1/NOTES.md`, and their cited candidate continuation-profile routes. No Lean execution was performed in this review. This is a source/statement audit, not a build receipt.

## Verdict

**Scoped pass, with source binding still pending as the batch notes disclose.** The code and claim inventory agree. The main theorem is a conditional, generic finite-suffix result under an explicit step-simulation relation and a fixed, input-only aperture. The fixture correctly refutes extension from a narrower declared aperture to a widened one. The materials do not purport to prove that a concrete freeze/restore satisfies those premises, or to establish persistence, resources, fairness, source authenticity, or PAL adoption.

There are **four explicit Lean theorem declarations**, not three: `run_append`, `one_suffix_of_step_simulation`, `all_finite_suffixes_of_step_simulation`, and `aperture_expansion_distinguishes_future` (`Pal24Continuation.lean:43-78,107-133`). `claims.json` inventories all four at entries 6-8 and 13; `Pal24ContinuationAxioms.lean:17-32` contains a corresponding `#check`/`#print axioms` pair for each. It inventories 13 top-level declarations total: one structure, eight definitions, and four theorems, matching the Lean file and claims array. Thus, if the worker's “three theorems” meant the three results beyond finite-run composition, that is a reasonable characterization but should be stated as “three substantive simulation/fixture results plus `run_append`”; otherwise the theorem count should be corrected to four.

## Checked semantics and bounds

- `TransitionProfile` packages `State`, `Input`, `Answer`, `observe`, deterministic `step`, and an `admits : Input → Prop` predicate (`Pal24Continuation.lean:16-23`). `admissibleSuffix` is exactly pointwise membership in that state-independent predicate (`:30-32`); it is not state-dependent enabledness.
- `run_append` is the ordinary recursive composition law for finite input lists (`:43-49`). It makes no admission or restore claim.
- `one_suffix_of_step_simulation` assumes observation agreement for related states and relation preservation for every admitted input and related state pair; it concludes equal observations after one supplied admissible suffix (`:51-68`). `all_finite_suffixes_of_step_simulation` universally quantifies only finite suffixes admitted by this same profile, under the same supplied hypotheses (`:69-78`). The quantifier and assumptions support the wording in claims entries 7-8 and the limitations in `NOTES.md`.
- The Boolean fixture's two profiles share the same state, observation and transition; only the input aperture changes (`:80-102`). From `(0,true)` and `(0,false)`, the current observations agree and the full states differ. Every narrow-admitted suffix consists only of `false` inputs, which leave the observed count unchanged. The wide profile admits `[true]`, which increments one count and not the other. It also agrees on the selected widened suffix `[false]` (`:104-133`). This exactly witnesses failure of the proposed widened-aperture implication; it does not imply that all profile changes cause a distinction.
- The source card M-CONTINUATION-PROFILE and SC-22.2 separate selected-answer equality, exact recovery of protected work, and continuation equivalence over a named suffix family. B1 formalizes the generic continuation-preservation implication and an aperture-changing countercase. It does not define freeze/restore maps or prove exact recovery. That is a bounded slice of the source route, and the code header, batch notes, claim residuals, and source card keep the missing restore bridge visible.

## Assumptions, predecessor boundary, and residuals

The theorem's state/input/answer types and transition are caller-supplied; the theorem does not establish that a chosen relation exists, that it is inhabited by the compared states, or that the supplied aperture and transition encode an external task. The `hStep` premise applies to any related pair at every admitted input, while `hObserve` requires equal observations at each related pair. The result covers all finite lists, including repeated inputs, and no infinite runs or progress. This matches `NOTES.md`'s stated generalization limits.

The notes distinguish reused MIND and PAL v2.3 predecessor results from B1's declarations. In particular, `natBool_chosen_suffix_vs_other_suffix` is acknowledged as predecessor evidence, while B1's widened-profile countercase adds an explicit narrower-versus-wider aperture comparison. I found no claim that predecessor theorem counts transfer into B1.

`claims.json` has `source_inputs: []` and `NOTES.md` labels the source hashes as pending freeze. Accordingly, this review does not treat the development theorem or this review as source-bound evidence; the batch must bind and check its exact candidate source inputs before any source-correspondence receipt is claimed.

## No further correction required for this bounded review

No mismatch was found between theorem signatures as written, their corresponding ledger statements, the tested fixture behavior, and the stated limits. The only clarification is the four-versus-three theorem-count wording above; all four declarations are already inventoried.
