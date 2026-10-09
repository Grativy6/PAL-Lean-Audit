# Mathematical review and source-to-formal dictionary

Reviewer: Hearthline, self-review under Chris's selected Abstract Loops key.
Review date: 8 October 2026. Controlling targets were frozen in TARGETS.md
before final proof acceptance. Verdicts below apply to the exact current
statements and matching PASS receipts, not to an unqualified reading of titles.

## Main source obligations

| Target | Source locator | Primary verdict | Decisive evidence and boundary |
| --- | --- | --- | --- |
| Reachable joint capacity is at most the product of reachable component capacities. | P0014-P0026 | proved as written | `joint_capacity_bound`; inject the actual joint support into the product of the two reachable subtypes. Finiteness is on those subtypes, not on worlds or ambient alphabets. Empty domains are allowed. |
| Joint certification requires answer capacity at most joint capacity. | P0016-P0026 | proved as written | `certification_capacity`, `certified_joint_capacity_chain`; a reachable decoder induces a surjection onto reachable answers and also proves that image finite. No total decoder on unreachable values is required. |
| Fixed closed deterministic processing eventually stabilizes its kernel with finite initial reachable image. | P0045-P0046 | proved as written | `finite_initial_image_kernel_stabilizes` factors the evolution through the finite initial-image subtype and reuses C5's finite relation-chain theorem. `finite_trace_initialized_kernel_stabilizes` accepts an initializer only on the reachable source image, as the paper requires. Worlds and state alphabets may be infinite. |
| Strict partition merges are finite in number. | P0045-P0046 | proved as written | `scheduled_merge_iff_capacity_drop` connects actual merged world pairs to strict reachable-image cardinality loss; `finite_image_merge_budget` bounds strict steps in every prefix by m-1 for a nonempty world type. This is not a last-merge-time bound. |
| Uniform trace-only correctness implies certification. | P0048 | proved as written | Deterministic strategy and nondeterministic output-set versions. The latter requires at least one allowed output at each reachable trace and that every such output is correct. It does not assume the existence of a successful strategy merely from abstract certification. |
| Observable surplus requires raw surplus. | P0049-P0058 | proved as written | `observable_surplus_requires_raw_surplus`; the comparison uses one state type/readout. `one_jump_reachable_support` realizes the counterexample supports as actual reflexive-transitive reachable sets from a common initializer. |
| Under a nonempty run class, inevitable failure implies possible failure. | P0059-P0062 | proved as written | `nonempty_inevitable_implies_possible`; the implication itself is a quantifier check. The complete, common-initializer run witnesses are checked separately in `fork_runs_are_complete_and_nonempty`. |
| Absorbing failure persists along declared transitions. | P0062 | proved as written | `absorbing_failure_persists` proves the statement for every future finite offset on an infinite path. Finite-run indexing and maximality are modeled and checked separately; no theorem about an unobserved padded tail is asserted. |
| No readable residual means identity at that readout. | P0101-P0104 | proved as written | `no_direct_residual_iff_readable_identity` is a definition/interface check. Hidden motion is demonstrated independently; no identity of the full state is inferred. |
| Returned status and candidate export status permit four combinations. | P0105-P0107 | proved as written | `all_four_return_export_combinations` checks all Boolean controls over a nonempty four-state input support, with a common contributor-readout alphabet. Full carrier qualification is not inferred merely from nonbottom candidate output. |
| The displayed finite carrier interpretation has the listed address, persistence, source-copy, and baseline witnesses. | P0081-P0089; P0091; P0107 | proved as written | `generated_fixture_receipt`, `coupled_history_after_entry`, `baseline_keeps_original_roster`, `declared_cut_witness`. Same ambient roster type, same inputs, unchanged contributor readouts, new address 2, every positive time, and exact source-copy data. These are the stated fixture claims, not a universal carrier-generation criterion. |
| Deterministic export preserves the complete initializer's kernel; a fixed environment permits trace factorization. | P0087-P0089 | proved as written | `export_respects_complete_initializer` is expressly a reuse of C5's postprocessing theorem. `fixed_environment_restores_trace_factorization` constructs the reachable decoder. |

The normalized infinite-path persistence target is proved without a fairness
assumption. The general finite-path persistence induction is not a separately
declared result in this batch; finite completeness and valid observation indices
receive their own maximal-finite-path fixture. The receipt does not conflate
these distinct coverage statements.

## Adversarial controls

These refute stronger claims that the manuscript already rejects. They are
not counterexamples to the manuscript's qualified statements.

| Stronger claim under test | Primary verdict | Checked counterexample |
| --- | --- | --- |
| The joint reachable image always fills the ambient product. | refuted, with a valid counterexample | A diagonal Boolean joint trace cannot reach (false,true). |
| Having as many reachable trace labels as answers guarantees certification. | refuted, with a valid counterexample | Both first-coordinate trace and XOR answer surject onto Bool; the first coordinate still fails to certify XOR. The obstruction is inherited C1 evidence. |
| Initial capacity alone bounds the time of the final merge under any fixed schedule. | refuted, with a valid counterexample | `merge_can_be_arbitrarily_late`: the same two-value domain can postpone its merge for any supplied natural delay. |
| Infinite reachable image alone still guarantees finite kernel stabilization. | refuted, with a valid counterexample | Natural-number predecessor, identity initializer: for each n, the pair n,n+1 merges at the next step. The proof rules out every alleged stabilization index. |
| One favorable branch per world supplies a trace decoder. | refuted, with a valid counterexample | Two Boolean worlds share one trace; a world-selected favorable Boolean branch exists, but no decoder from that trace does. |
| An independent branch label necessarily adds information about the world. | refuted, with a valid counterexample | With the same branch label fixed, the two world values still collide. |
| A set-theoretic certificate guarantees implementation by supplied allowed operations. | refuted, with a valid counterexample | The constant-true query is certifiable, while a machine permitted only false cannot implement it. |
| Raw surplus guarantees observable surplus or strict reachable-set enlargement. | refuted, with valid counterexamples | Hidden Boolean coordinate disappears under first-coordinate readout; supports {0,1} and {0,2} have surplus in both directions. |
| Possibility implies inevitability. | refuted, with a valid counterexample | The complete waiting and failing runs of the same declared Boolean system. |
| An empty run restriction establishes meaningful inevitability. | refuted, with a valid counterexample | The universal visit formula is vacuous while no possible visit exists. The source's required nonemptiness blocks this inference. |
| A failure visit automatically persists. | refuted, with a valid counterexample | A complete infinite path for the universal relation visits true and then leaves it. |
| A roster tag or unchanged contributor readouts establish persistence/provenance. | refuted, with valid counterexamples | Reset removes the new address; a different C value preserves A/B readouts but fails the declared source-copy relation. |
| Closed determinism always permits using the smaller original trace instead of the full initializer. | refuted, with a valid counterexample | The omitted second Boolean coordinate controls the exported value; the full pair certifies it and the first coordinate does not. |

## Dependency graph

```text
Exact Abstract Loops v1.0 source + frozen workshop targets
  ├─ C1 reachable decoder / kernel criterion (unchanged)
  │    ├─ AL-A answer capacity and inherited XOR control
  │    ├─ AL-B uniform protocols / collision controls
  │    └─ AL-C initializer counterexample / reachable decoder
  ├─ C5 scheduled iteration / finite relation-chain theorem (unchanged)
  │    ├─ AL-A factor through finite initial range → stabilize on arbitrary worlds
  │    └─ AL-C explicit histories and reused kernel preservation
  ├─ pinned Mathlib finite sets/cardinalities → capacity loss and merge budget
  └─ explicit Boolean/natural/typed-roster models → counterexamples and fixtures
```

No philosophical analogy, physics citation, unverified external theorem, or
paper assertion is introduced as a Lean axiom. Existing Mathlib propositions
are imported proof dependencies in the pinned Lean environment. The physical
sections' literature and realization questions were not used as proof leaves.

## Obligation matrix

| Obligation | Disposition | Evidence / remaining boundary |
| --- | --- | --- |
| Exact source identity and paragraph mapping | passed | Both manuscript hashes and retained text/JSON/PDF extracts match the prepared source map. |
| Actual reachable support rather than ambient alphabet | passed | Reachable subtype capacity proofs; reachable-only initializer in the final stabilization theorem. |
| Finiteness, nonemptiness and quantifier placement | passed | Explicit finite-image premises; nonempty-world m-1 theorem; nonempty run-class implication and negative controls. |
| Supplied examples inhabit the modeled domain | passed | Fin 3 and Boolean supports, actual one-jump reachability lemma, complete run fixtures, common roster type. |
| Source statement versus chosen representation | passed | Typed return maps, output sets, run constructors, roster convention, readout and source-copy assumptions recorded in claims.json. |
| Exact declaration and axiom inventories | passed | Every explicit declaration is inspected; only propext, Quot.sound, Classical.choice appear. |
| Build and bundled kernel checks | passed | Matching per-batch results.json, raw command logs and hashes. |
| Receipt validation and six mutation controls | passed | Saved receipt checks and integration receipt. |
| General carrier qualification, indispensable causal provenance, physical identity/cuts | conditional | Requires a justified application of the proposed criteria; a label or fixture cannot supply it. |
| Operational decoder cost, fairness justification, privileged baseline selection | out of scope | Supplied conditions are recorded; no efficiency or authority is inferred. |
| Gravity/LQG, noise, measurement, or physical carrier generation | out of scope | No physical model or external experimental evidence audited. |
| Independent review | not addressed | This is source-grounded self-review, with the same bundled Lean kernel implementation. |

## Development history and corrections

Development logs retain ordinary Lean failures. AL-A needed an explicit
function argument and a reflexivity step instead of an arithmetic tactic.
AL-B and AL-C initially used Lean keywords as variable names; those were
renamed. The finite Boolean four-case check needed its predicate definitions
unfolded before decidable checking. None was a mathematical counterexample.

Final source review broadened AL-A's initializer from an ambient-alphabet map
to a map defined only on reachable values. The earlier passing receipt is
retained in its evidence directory and has a narrower signature; current
`AL-A/results.json` points to the rechecked, source-matching statement. The
broader statement removes an unnecessary formalization assumption without
changing the paper.

Strongest safe conclusion: the selected exact claims and finite controls have
source-bound Lean receipts. The former finite-world restriction in C5 and its
missing capacity coverage are resolved by these new results. There is no
confirmed source defect to repair, and no omitted build step remains for the
three selected batches.
