# Attack Run 0003 benchmark receipt

- Measured at: `2026-08-10T02:29:31+00:00`
- Environment: Lean (version 4.32.1, x86_64-w64-windows-gnu, commit f054605aea4b840552cca2e725580bffd1e1b704, Release); Mathlib revision 520045ab14e26149ee970e2e617ca04b09bde5d6; Windows-10-10.0.19045-SP0
- Baseline commit: `144b08973fde16ebeabefc78166691afc861abec`
- Tracked commit under test: `UNAVAILABLE_FOR_UNCOMMITTED_WORKTREE`
- Worktree identity: UNCOMMITTED_GATE5_WORKTREE; exact PR head and synthetic merge commits are captured separately by CI because a tracked receipt cannot self-identify its own future commit.
- Method: One wall-clock observation using Python perf_counter after an earlier successful build; local Lake and Mathlib caches were warm.
- Repetitions: 1
- Cache state: `WARM_LOCAL_CACHE`
- Missing data: Peak memory was not collected locally; CI retains its own runner evidence separately.
- Privacy handling: Machine-local repository and published-ZIP paths are replaced by role labels in the committed validation log.

| Measurement | Actual value | Unit |
|---|---:|---|
| Build wall time | 3.060529 | seconds |
| Checked declarations | 73 | declarations |
| Empty axiom receipts | 61 | declarations |
| Nonempty axiom receipts | 12 | declarations |
| propext-only receipts | 7 | declarations |
| propext + Quot.sound receipts | 5 | declarations |
| Formal result rows | 21 | results |
| Adversarial/negative controls | 10 | controls |
| Policy fixtures | 4 | fixtures |
| Repository checks | 10 | checks |

Build duration is runner- and cache-dependent. Counts describe this declared run; none is a PAL correctness score.

_Generated from `Audit/attack-run-0003-benchmarks.json`; do not edit by hand._
