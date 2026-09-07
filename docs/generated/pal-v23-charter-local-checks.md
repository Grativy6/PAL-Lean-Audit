# PAL v2.3 and CHARTER local Lean checks

Result: **PASS_LOCAL_BOUNDED_CHECKS**. 27 named theorem targets across three local run groups.

The selected PAL models preserve the intended limits: a requested answer can be decoded on the reachable image exactly when equal traces cannot disagree on that answer; work-state restoration and heartbeat recurrence need not restore total state, spent resources, grants, or progress.

The selected CHARTER arithmetic checks establish the adjacent-bank identities and a fixed-total norm minimum. The indices at m = 1, 2, 3 are prime (7, 19, 37), while m = 5 gives 91 = 7 * 13. A new derived consequence gives an entire composite subfamily:

```text
n_(7k+5) = 7 * (21k^2 + 33k + 13), for every natural k.
```

The composite family agrees with CHARTER's explicit warning that adjacent-bank indices need not be prime. It is a counterexample to universal primality, not a contradiction of CHARTER. No claim about an infinite prime subsequence follows.

Lean checks the stated realizations and counterexamples. This is partial source coverage, not a complete PAL conformance suite, proof of PAL, or full CHARTER formalization. It does not adopt or close any source claim.

Sources: six user-supplied DOCX files matched their locked SHA-256 values. These checks use the local supplied bytes; public release-package identity was not independently verified.

| Classification | Targets |
|---|---:|
| ASSUMPTION_BOUND | 4 |
| COUNTERMODEL_TO_OVERCLAIM | 5 |
| PROVED_FROM_DECLARED_RULES | 18 |

| Run | Target | Result | Lean declaration |
|---|---|---|---|
| local-pal23-projection | reachable decoder iff trace fibers preserve the requested answer | PROVED_FROM_DECLARED_RULES | `Experiments.Pal23.reachable_decoder_iff` |
| local-pal23-projection | trace collision prevents a reachable decoder when answers differ | ASSUMPTION_BOUND | `Experiments.Pal23.collision_prevents_reachable_decoder` |
| local-pal23-projection | unqualified totalization fails with empty source and nonempty ambient interface | COUNTERMODEL_TO_OVERCLAIM | `Experiments.Pal23.no_total_decoder_empty_source_nonempty_ambient` |
| local-pal23-reentry | freeze is injective under a thaw left inverse | ASSUMPTION_BOUND | `Experiments.Pal23.freeze_injective` |
| local-pal23-reentry | same suffix function respects the exact freeze/thaw equality | ASSUMPTION_BOUND | `Experiments.Pal23.suffix_preserved` |
| local-pal23-reentry | Boolean identity round-trip fixture | PROVED_FROM_DECLARED_RULES | `Experiments.Pal23.bool_capsule_roundtrip` |
| local-pal23-projection | heartbeat preserves the declared work coordinate | PROVED_FROM_DECLARED_RULES | `Experiments.Pal23.heartbeat_work_stutter` |
| local-pal23-projection | heartbeat has hidden total-state motion | COUNTERMODEL_TO_OVERCLAIM | `Experiments.Pal23.heartbeat_hidden_motion` |
| local-pal23-projection | one heartbeat does not change the declared progress coordinate | PROVED_FROM_DECLARED_RULES | `Experiments.Pal23.heartbeat_not_progress` |
| local-pal23-projection | finite heartbeat loop has no declared progress | PROVED_FROM_DECLARED_RULES | `Experiments.Pal23.heartbeat_loop_no_progress` |
| local-pal23-reentry | work restoration leaves the changed spent/grant fields in the fixture | COUNTERMODEL_TO_OVERCLAIM | `Experiments.Pal23.restore_work_not_restore_budget_or_grant` |
| local-pal23-reentry | work restoration is not total-state recovery | COUNTERMODEL_TO_OVERCLAIM | `Experiments.Pal23.restore_work_is_not_total_state_recovery` |
| local-charter-banks | Integer norm decomposition | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.four_Q_identity` |
| local-charter-banks | Adjacent index polynomial | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.adjacent_index_formula` |
| local-charter-banks | Odd-total index identity | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.four_adjacent_index_formula` |
| local-charter-banks | Adjacent bank total | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.adjacent_banks_total` |
| local-charter-banks | Adjacent banks are distinct | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.adjacent_banks_ordered_distinct` |
| local-charter-banks | Closest gap-one split is unique | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.closest_ordered_distinct_split_unique` |
| local-charter-banks | Ordered split gap is positive | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.ordered_distinct_gap_positive` |
| local-charter-banks | Derived arithmetic: adjacent banks minimize Nat Q | ASSUMPTION_BOUND | `Experiments.Charter.adjacent_banks_minimize_Q` |
| local-charter-banks | Concrete composite index | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.index_five_is_ninety_one` |
| local-charter-banks | Ninety-one factorization | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.ninety_one_factorization` |
| local-charter-banks | Derived composite subfamily factorization | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.composite_subfamily_factorization` |
| local-charter-banks | Derived composite subfamily | COUNTERMODEL_TO_OVERCLAIM | `Experiments.Charter.composite_subfamily` |
| local-charter-banks | Index one prime | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.index_one_prime` |
| local-charter-banks | Index two prime | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.index_two_prime` |
| local-charter-banks | Index three prime | PROVED_FROM_DECLARED_RULES | `Experiments.Charter.index_three_prime` |

The classifications count theorem targets, not independent corroborations. Several targets share definitions or lemmas. PAL and CHARTER belong to one source lineage.

## Evidence and limits

- Exact axiom inventory: 27 declarations, including reports with no axioms.
- Allowed foundational dependencies are propext, Classical.choice, and Quot.sound; each actual dependency list is recorded in results.json. No custom axioms or proof placeholders are admitted.
- The full local Lake build and bundled leanchecker checks cover Experiments and the historical PALLeanAudit module. The bundled checker is a second kernel check, not an independent scientific validation.
- Existing lexical policy, retained historical metadata, and generated-report regressions are recorded separately. The old published source archive was not downloaded or reverified.
- O04 and O25 remain two OPEN interfaces to the single OPEN D-FIRST-OCCURRENCE debt. The multi-parent-lineage boundary remains OPEN. These are not counted as theorem outcomes.
- Broader decoder classes, full-state restoration, liveness, authority, empirical performance, prime-shell occupancy, and remaining CHARTER post-core claims are not established by this run.
- CI and publication were not run. Source-to-model correspondence and adoption remain human review matters.

## Reproduce

With the pinned Lean toolchain, Mathlib dependencies, and the six source files available at their manifest paths:

```text
python scripts/run_pal23_charter.py --run --lake <path-to-lake>
python scripts/run_pal23_charter.py --check
```

The check command validates the stored execution evidence, input digests, exact theorem/claim/axiom inventories, and generated report. It does not pretend to rerun Lean.

Detailed source routes, exact statements, assumptions, countercases, ceilings, and reopening conditions are in Audit/pal-v23-charter/pal-claims.json and charter-claims.json. Raw execution output and result identities are in that directory's evidence folder and results.json.
