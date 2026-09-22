# PAL v2.3 finite trace/schedule coverage

This bounded supplement models a finite deterministic runner whose `step` returns a next state and an explicit action value. The retained receipt list is chronological and pairs each action value with its declared schedule site. Restoration applies those entries in reverse order. A generic one-step left-inverse hypothesis proves finite-schedule restoration; schedule tags and receipt length are separately conserved.

The concrete fixture uses the existing `Experiments.Pal23Followup.repairedExchange` and `restoreExchange` on three `Nat` coordinates. A `Bool` names pair 01 or pair 12. For schedule `[false, true]` and input `(0, 1, 2)`, the resulting state is `(1, 2, 0)` and chronological receipt is `[(false, true), (true, true)]`. The source-backed inverse is proved for either site and arbitrary triples, then lifted to any finite Bool schedule.

The checked wrapper accepts only when receipt site tags exactly match the supplied schedule. It rejects a reversed-tag receipt, a missing entry, and a wholly absent trace. A corrupted action bit retains valid schedule tags and is therefore accepted by that shape check; the fixture then recovers `(1, 0, 2)` rather than `(0, 1, 2)`. This is a bounded counterexample to treating schedule/tag shape as bit-integrity validation.

The receipt establishes only the stated Lean definitions and theorems. It does not model or establish physical storage, durability, complete input/output/event binding, action-bit integrity, independent recovery evidence, authority, or operational A2 admission. Those remain OPEN. The local finite schedule is supplied and known; no schedule-independent or whole-run minimality claim is made. This supplement does not amend PAL or close any PAL obligation.
