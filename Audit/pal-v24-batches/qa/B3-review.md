# B3 independent review — nested-account realization

**Review date:** 2026-09-22  
**Scope:** `Experiments/Pal24NestedAccount.lean`, its explicit axioms ledger, `Audit/pal-v24-batches/B3/claims.json`, `NOTES.md`, and the candidate source routes named there. No final batch receipt was produced.

## Disposition

The review findings were addressed within B3. The ledger now states the actual unrestricted type-level domain of the append theorem instead of recording scope/freshness conditions absent from its signature. A cross-level duplicate-ID fixture now demonstrates the parent/child overlap failure, and an accepted-account theorem packages the recursive/flattened equality with uniqueness of the modeled event IDs. The administrative exhaustion fixture now follows T75’s explicit boundary by returning a denial together with an unchanged nested-account projection.

## Repairs and remaining ceiling

- `appendOwn_known_monotone` at `Experiments/Pal24NestedAccount.lean:78` remains the valid unconditional list-arithmetic identity: every modeled account, ID, and `Nat` amount is covered. `claims.json` and `NOTES.md` now state that it does **not** validate scope, freshness, unit compatibility, or acceptance; those remain caller obligations.
- `accepted_aggregate_matches_flattening_with_unique_ids` at line 65 ties the arithmetic decomposition to `Nodup` under the local accepted predicate. Count-once remains relative to the stipulation that supplied event IDs are identity keys. It is not evidence of external identity, unique attribution in reality, or inventory completeness.
- `duplicateParentChildAttribution` and `parent_child_duplicate_attribution_rejected` at lines 96 and 108 exercise repeated ID 1 at the root and a child. The fixture is rejected by the global flattened-ID uniqueness predicate. The earlier same-node duplicate fixture remains as a distinct case.
- `AccountWork` and `administrationAttempt` at lines 14 and 50 support `insufficient_administrative_fuel_preserves_account_work` at line 113. This is routed to T75 and PAL v2.3 A13/A14, and states exactly what is preserved: the nested-account projection only. It still does not model the full protected work state, a scheduler, interference, or real resource behavior.
- `linked_epoch_preserves_old_spend` continues to assume the caller-supplied Boolean link flag and resolved aggregate; it does not establish epoch identity or lineage. Unit tags remain exact-match only, and the tree remains finite and binary.

## Verification

The targeted `lake build Experiments.Pal24NestedAccount` succeeded after correcting a conjunction projection in the new accepted-account theorem. `lake env lean Experiments/Pal24NestedAccountAxioms.lean` typechecked all paired `#check`/`#print axioms` entries; the declarations use only the allowed standard Lean axioms (including `propext`, `Quot.sound`, and `Classical.choice` where reported). `lake env leanchecker Experiments.Pal24NestedAccount` exited successfully.

A textual inventory check found 48 source declarations and 48 ledger rows in identical order, including 18 theorems; the axioms module has one paired check/print for each row in that same order. A source scan found no `sorry`, `admit`, `axiom`, `native_decide`, or `unsafe`. These targeted checks are not a final runner receipt and do not close O65 or adopt PAL v2.4.

## Source ceiling

M-NESTED-ACCOUNT / D42 / O65 / T75 license a finite, named-scope account calculation with compatible units, complete declared inputs, unique and non-overlapping event attribution, and explicit uncertainty handling. This module implements a narrower exact-tag finite binary tree. Its proofs concern only that encoded tree and its stipulated predicates; they cannot establish that the supplied tree is a complete or authorized account of external resources.
