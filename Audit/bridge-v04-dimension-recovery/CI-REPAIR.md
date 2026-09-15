# Historical cache portability correction

The first candidate, 9a061b96247491d7004554756db4e834f9d78619, ran in [CI run 34678573452](https://github.com/Grativy6/PAL-Lean-Audit/actions/runs/34678573452). All sixteen candidate commands and the nested eighteen-command historical replay completed successfully. The enclosing receipt validation then rejected the nested checkout because its recorded worktree status was `?? .lake`.

The pinned historical repository ignores `.lake/`, which matches a directory. The first helper exposed the cache as a symlink at that path; on Unix the directory-only ignore rule did not hide the symlink. The standalone historical workflow accepted its own bounded replay, but the new enclosing validator correctly required a clean historical tree and rejected the artifact. This is a tooling result, not a failed theorem or a mathematical counterexample.

The correction creates a real `.lake` directory and links the prepared cache entries inside it. It verifies cleanliness immediately after cache setup as well as in the completed nested receipt. No tracked ignore rule, source file, theorem, historical receipt, or clean-tree requirement was weakened. New local execution and exact-head CI receipts verify the corrected helper; the first failed CI artifact is retained locally under `artifacts/pr15-failed-ci-34678573452`.

A separate Windows cleanup warning left orphaned temporary-worktree metadata under `.git/worktrees/checkout` after its checkout and registration file were gone. The controller verified that absence and moved the remaining metadata into `artifacts/pr15-stale-worktree-metadata`; no source or user work was removed.
