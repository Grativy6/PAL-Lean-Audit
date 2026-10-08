# Challenges to stronger readings

These controls retain the mathematical claim's boundaries. They are not defects in the manuscript, which already distinguishes these cases. Final theorem signatures and axiom dependencies are in `receipts/formal/receipt.json`.

| Tempting inference | Retained challenge |
|---|---|
| A historically valid premise remains usable | `FrontLean.stale_premise_counterexample` |
| One good parent is enough for an AND rule | `FrontLean.missing_conjunct_is_rejected` |
| A cycle can ground itself | `FrontLean.empty_seed_stays_empty`; finite Horn truth-table suite |
| A supported answer repairs its old receipt | `FrontLean.independent_answer_invalid_receipt`; 30 such offered-receipt failures in the unchecked arm |
| The current answer determines its ancestry | `FrontLean.answer_does_not_recover_history` |
| Observation labels can be discarded | `FrontLean.lost_labels_counterexample` |
| Naming an unavailable reading supplies its content | `FrontLean.absent_reading_is_not_content` |
| Protected future outputs imply an update for the same encoding | `FrontLean.output_sufficient_without_online_update` |
| Separate generated baselines preserve the joint quotient | `FrontLean.independent_baselines_lose_relation` |
| A static quotient always permits the proposed dynamics | `FrontLean.quotient_update_can_fail` |
| Accumulated return can omit transport | `FrontLean.untransported_return_wrong` |
| A technically valid changed candidate may commit without a grant | `FrontLean.technically_valid_but_not_authorized` |
| Fixing one condition is enough | `FrontLean.failed_secondary_condition_is_recorded`; 16 failed revalidations rolled back in each 96-case suite |
| A completed task should be summoned again | Frozen `quiet_summon` mutation is detected; the 525 budget cases include 21 STOP outcomes with zero spending |
| Exhausting recorded alternatives disproves the query | `FrontLean.no_recorded_proof_is_not_negation` |
| SAT has the same strengthening direction as UNSAT | `FrontLean.sat_does_not_transfer_to_strengthening` |

The correction study also retains eight injected-error controls: erased history, promoted intent, stale warrant, hash treated as warrant, invented coverage, collapsed outcome type, alternate-route grant bypass, and a reopened completed task. All were detected in both fresh runs. The `A` control remains deliberately wrong; its failures are part of the result.

The Single-Cut contribution is confined to the supplied finite row/slack checks and 5,040-order assay. No public-version comparison, geometric extension, or separate Single-Cut research lane was opened.
