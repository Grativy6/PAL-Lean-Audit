# SCT-B frozen target

Source SCT v0.1 P0086-P0110, SCT-03/04. Reuse SCT-A's actual finite rank support. For any nonempty U and any corridor lengths c,d, the charges agree with fixed e and U. Arbitrary permutations of the fully selected corridor ranks leave the selected support unchanged. This covers insertion/deletion of any finite number of selected corridor positions.

For e in {0,1}, admissibility is equivalent to prefix slack <= 1-e; for admissible rows e+slack+unused=1. False (e=1) forces exact prefix, true (e=0) permits at most one skipped prefix rank. Zero slack, in particular a full clause subset, satisfies both orientations and cannot decode them.

For any support and selected strictly interior rank, erasing that selected rank preserves hull and increases charge by one. Specialize to removing one interior position from a corridor extended by one selected position: this is an inserted unselected corridor column relative to the shorter serial account.

Countercontrols: same endpoint/target data with puncture changes feasibility; dropping orientation makes charge nonunique; invalid rows cannot close the budget merely using truncated subtraction. Fan-out is explicitly a family of separate unit row accounts, not conservation of a global token.
