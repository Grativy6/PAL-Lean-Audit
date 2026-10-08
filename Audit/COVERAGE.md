# Source-to-proof coverage

The line locations below refer to the [preserved audited manuscript](../Publication/audited-source/FRONT_v1.0_WORKING_DRAFT.md). The [publication concordance](../Publication/source-concordance.json) records the editorial release and unchanged mathematical statements.

Source: supplied FRONT v1.0 working draft. General means the named formal statement covers the mathematical claim at the scope below. Bounded means an explicit realization or numerical core with the remaining bridge named. Neither label certifies all prose or the Python implementation. Final checking lives in `receipts/formal/receipt.json`.

| Claim | Batch | Disposition | Main declaration |
|---|---|---|---|
| 1 | B | BOUNDED_REALIZATION | `FrontLean.premise_substitution` |
| 2 | B | GENERAL_STATEMENT_CHECKED | `FrontLean.negative_core_transfer` |
| 3 | A | GENERAL_STATEMENT_CHECKED | `FrontLean.answer_sufficiency` |
| 3A | A | GENERAL_STATEMENT_CHECKED | `FrontLean.joint_equality` |
| 3B | E | GENERAL_STATEMENT_CHECKED | `FrontLean.linear_factorization` |
| 4 | A | GENERAL_STATEMENT_CHECKED | `FrontLean.common_action_iff` |
| 5 | D | GENERAL_STATEMENT_CHECKED | `FrontLean.future_output_preservation` |
| 6 | A | GENERAL_STATEMENT_CHECKED | `FrontLean.coordinate_bit_bound` |
| 5A | DE | GENERAL_STATEMENT_CHECKED | `FrontLean.admitted_outputs_sufficiency` |
| 5B | E | GENERAL_STATEMENT_CHECKED | `FrontLean.invariant_kernel_iff` |
| 5C | E | GENERAL_STATEMENT_CHECKED | `FrontLean.finite_readout_subfamily` |
| 5D | E | GENERAL_STATEMENT_CHECKED | `FrontLean.joint_residual_short_exact` |
| 5E | E | GENERAL_STATEMENT_CHECKED | `FrontLean.side_trace_decodable` |
| 5F | DE | GENERAL_STATEMENT_CHECKED | `FrontLean.quotient_update_iff` |
| 7 | F | GENERAL_STATEMENT_CHECKED | `FrontLean.reuse_cheaper_iff` |
| 7A | B | GENERAL_STATEMENT_CHECKED | `FrontLean.finite_stabilization` |
| 7B | B | GENERAL_STATEMENT_CHECKED | `FrontLean.horn_rounds_sound` |
| 7C | B | GENERAL_STATEMENT_CHECKED | `FrontLean.wake_decomposition` |
| 7D | B | BOUNDED_REALIZATION | `FrontLean.increasing_depth_no_cycle` |
| 7E | C | BOUNDED_REALIZATION | `FrontLean.recorded_support_sound` |
| 8 | F | BOUNDED_REALIZATION | `FrontLean.descending_rank_bounds_steps` |

## Proposition 1

Proposition 1 — Scoped deductive reuse — manuscript line 204.

Fixed finitary inference rules, arbitrary proposition labels, every retained premise has a valid present derivation; substitution is proved by structural induction.

**Remaining limit:** Explicit finitary calculus realization. No encoding of all sound monotone calculi or natural deduction with discharged assumptions.

Declarations: `FrontLean.premise_substitution`.

## Proposition 2

Proposition 2 — Negative-core transfer — manuscript line 279.

Arbitrary clauses and valuations with a fixed satisfaction relation; an unsatisfiable core is a subset of the new clause set.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.negative_core_transfer`.

## Proposition 3

Proposition 3 — Fiber criterion for an answer — manuscript line 405.

Arbitrary types and total input/answer maps. Decoder lives on the reachable subtype, including empty domains. Reuses APCI exactOnReachable_iff_fiberConstant.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.answer_sufficiency`.

## Proposition 3A

Proposition 3A — Indexed joint sufficiency — manuscript line 444.

Dependent labeled family of readouts, with a decoder on its actual reachable tuples; classical choice is explicit in the dependency inventory.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.joint_equality`, `FrontLean.joint_sufficiency`.

## Proposition 3B

Proposition 3B — View-to-view factorization — manuscript line 468.

Linear maps on one full vector space over a field; the decoder domain is the image of J and existence is equivalent to ker J <= ker q.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.linear_factorization`.

## Proposition 4

Proposition 4 — Common-continuation criterion — manuscript line 490.

One adequate action common to each reachable fiber, with adequacy supplied as a relation. The proof permits arbitrary sets; the finite manuscript case is an instance.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.common_action_iff`.

## Proposition 5

Proposition 5 — Future-output preservation — manuscript line 581.

All finite words over the declared deterministic update alphabet; output preservation and a same-encoding transition function have separate iff statements.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.future_output_preservation`, `FrontLean.online_update_iff`, `FrontLean.future_eq_is_right_congruence`.

## Proposition 6

Proposition 6 — Cost of protecting all coordinate queries — manuscript line 618.

Exact recovery of every coordinate of d Boolean bits from a fixed-length b-bit representation. No noise, probabilistic guarantee, variable length, or external rereading.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.coordinate_bit_bound`.

## Proposition 5A

Proposition 5A — Combined-interface sufficiency — manuscript line 644.

The actual admitted index set, not its rectangular completion. Dependent indexed outputs. Linear joint-kernel and refinement statements in Linear.lean.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.admitted_outputs_sufficiency`, `FrontLean.joint_kernel`, `FrontLean.kernel_refinement`.

## Proposition 5B

Proposition 5B — Persistent invisibility and finite-horizon closure — manuscript line 712.

Full vector-space difference domain; one linear endomorphism and readout. Stabilization at dim T holds for any finite-dimensional field vector space (including zero dimension). The Lean proof uses strict dimension drop, not Cayley-Hamilton.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.invariant_kernel_iff`, `FrontLean.horizon_antitone`, `FrontLean.finite_horizon_closure`, `FrontLean.infinite_invariant`, `FrontLean.all_outputs_equal_iff`.

## Proposition 5C

Proposition 5C — Finite subfamily with the same hidden space — manuscript line 730.

Arbitrary indexed family; finite-dimensional input. At most dim T readouts preserve the common kernel. The proof works even without finite-dimensional codomains; no effective selection or acquisition claim.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.finite_readout_subfamily`, `FrontLean.finite_subfamily_inside`.

## Proposition 5D

Proposition 5D — BRIDGE at the combined interface — manuscript line 751.

One common B and actual J; typed hidden injection, residual quotient map, exactness, injectivity, surjectivity and visible equivalence. Finite dimension only for the dimension identity. Refinement uses the same B. Verbatim inherited BRIDGE proofs keep their identity.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.joint_residual_short_exact`, `FrontLean.joint_visible_equiv`, `FrontLean.joint_sector_dimensions`, `FrontLean.visibleRefinement`, `FrontLean.refinement_commutes`, `Experiments.BridgeRecovery.ker_residualReadout`.

## Proposition 5E

Proposition 5E — Query-specific side-trace capacity and minimum rank — manuscript line 774.

Finite-dimensional input, state query q, actual J and linear side trace. Lower bound plus attaining noncanonical extension. Finite-side-space dimension iff; arbitrary side spaces use an equivalent injective-copy capacity statement. Residual target uses T/B and the range of its named hidden injection. Rank is not acquisition cost.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.side_trace_decodable`, `FrontLean.side_trace_rank_lower_bound`, `FrontLean.minimum_side_trace`, `FrontLean.side_trace_capacity`, `FrontLean.side_trace_capacity_injection`, `FrontLean.residual_query_criterion`, `FrontLean.residual_debt_image`, `FrontLean.residual_side_trace_capacity`, `Experiments.BridgeRecovery.answer_decodable_iff`.

## Proposition 5F

Proposition 5F — When an update descends to a quotient — manuscript line 796.

Arbitrary subspace B and linear L: a commuting quotient update exists iff B is invariant. B may be ker J. Equation 20m uses powers of the same endomorphism and transports the second return.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.quotient_update_iff`, `FrontLean.transported_return`.

## Proposition 7

Proposition 7 — Amortized reuse condition — manuscript line 851.

Equal-unit real costs in the stated model; algebraic break-even identity. No-cost-saving corollary assumes m>=1, B>=0 and R>=D.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.reuse_cheaper_iff`, `FrontLean.no_saving_when_reuse_is_costlier`.

## Proposition 7A

Proposition 7A — Finite stabilization and least closure — manuscript line 915.

Finite atom type, finite rule set, inflationary monotone Horn step. At most card atoms minus card seeds strict growth rounds; fixed point contains seeds and is least among closed supersets. Final no-change scan is additional work.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.finite_stabilization`, `FrontLean.horn_least_closure`, `FrontLean.stable_round_persists`.

## Proposition 7B

Proposition 7B — Sound propagation relative to a basis — manuscript line 927.

Declared true roots and truth-preserving rules; every conjunctive parent is checked. No unsupported cycle generates support. Empty-body rules require their own declared rule soundness.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.horn_rounds_sound`, `FrontLean.derivation_sound`, `FrontLean.empty_seed_stays_empty`.

## Proposition 7C

Proposition 7C — Decomposing the exposed wake — manuscript line 952.

Finite set partition with E subset B subset S and old/new least-closure properties supplied for the redundancy corollary. No generic speedup is asserted.

**Remaining limit:** No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.

Declarations: `FrontLean.wake_decomposition`, `FrontLean.redundant_seed`.

## Proposition 7D

Proposition 7D — Transfer of a selected, rooted derivation — manuscript line 974.

Any strictly increasing discovery ranking rules out cycles. A finite rooted derivation remains valid when every actually used root and rule retains validity; that returned derivation implies its head under sound interpretations.

**Remaining limit:** Sharing is represented by the finite tree obtained after unfolding a DAG. No verified parser, DAG-to-tree compiler, exact byte matcher or Python implementation refinement theorem.

Declarations: `FrontLean.increasing_depth_no_cycle`, `FrontLean.valid_under_unchanged_basis`, `FrontLean.derivation_sound`.

## Proposition 7E

Proposition 7E — Conditional support and history preservation under correction — manuscript line 1030.

Finite recorded witnesses with all children grounded; conditional root/rule truth. An explicit pure scratch transition commits changed state iff its grant and postcondition hold, otherwise retains the original state. Every transition appends history; prefix preservation composes.

**Remaining limit:** A checked realization of the conditional correction claims, not a proof for arbitrary repair implementations. The grant/postcondition are fixed supplied predicates; the Python fixture increments a version on commit and is not compiled from this Lean transition. External authority, concurrent revocation and crash recovery remain outside.

Declarations: `FrontLean.recorded_support_sound`, `FrontLean.unchanged_alternative_survives`, `FrontLean.scratch_commit_iff`, `FrontLean.failed_scratch_keeps_original`, `FrontLean.scratch_preserves_history`, `FrontLean.finite_history_preservation`.

## Proposition 8

Proposition 8 — Polynomial accounting consequence — manuscript line 1081.

Natural-valued strictly decreasing rank, bounded initial rank, bounded per-stage cost, polynomial init cost. Proves the p0+(p1+1)*p2 numerical bound and polynomial expression.

**Remaining limit:** No encoding of a uniform SAT decider or machine-level complexity classes. The source consequence about P=NP remains conditional on its stated algorithm, correctness, totality and cost hypotheses; none is constructed here.

Declarations: `FrontLean.descending_rank_bounds_steps`, `FrontLean.total_cost_bound`, `FrontLean.polynomial_accounting`.
