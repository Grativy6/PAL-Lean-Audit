# W00 journal 03 — First Lean failure and targeted repair

2026-10-28.

Draft PR 21 was opened, with a focused workflow using the repository's pinned Lean 4.32.1 and Mathlib manifest. This works around the absence of a local Lean compiler; it does not install anything on Speck or Dust.

First attempt:
- Proposed head: `999d23b7f11c2ee9b657d834375fe76a282a378c`.
- Synthetic merge tested: `e9dc7f6bbf5ec436f6adcb1459b09d7b93061185`.
- Workflow run: `40647692016`; job: `122680241069`.
- Artifact: `12798700030`; ZIP SHA-256 `fa7008a87a5608d3f3b5590a28e639cee9de786caa35823165aaa46ec943b5cb`.

The module build failed at `reconstruct_from_pair`. After normalizing divisions, the proof still had the inverse of the determinant; `field_simp` had not used the local nonzero determinant automatically. This was a proof-script failure, not a counterexample to Cramer's rule.

Repair commit `45f4efe36f1d89914b29098beee7cfd4c8f8d55b` explicitly supplies `[hd]` to `field_simp` and removes one unused simp argument. No theorem statement or assumption was weakened. The initial failed build and environment receipt remain available. The repaired build outcome must be read before claiming Lean acceptance.

Separately, a new local Python script checked 12 symbolic polynomial identities and 14,976 exact vector/parameter cases over a declared finite box. It reconstructed (7,-11) in all 13,248 nonblind cases using rational Cramer coefficients. Those finite counts are diagnostic coverage, not 14,976 independent theorems.

## Second attempt: the first repair was insufficient

Run `40648333176`, job `122682275449`, tested head `45f4efe36f1d89914b29098beee7cfd4c8f8d55b` as synthetic merge `57c4c66c655db02902a9af2565eee432532d89e4`. Artifact `12798566492`, SHA-256 `a0fa3fa181599b4deea469cc0dc6ed40cc57e7819fdc095df82d3ac836d76ba1`.

Adding `[hd]` did not clear the normalized inverse. The same two reconstruction goals remained; no theorem statement was changed. The second repair uses separate polynomial numerator identities followed by explicit cancellation of the exact nonzero determinant. This avoids depending on field_simp's atom normalization. Commit `b3b53d1d7e343afceafa18739ed07e984d2db2bd` holds that repair. Its outcome is recorded in the final receipt, not presumed here.
