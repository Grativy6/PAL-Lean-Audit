# Tooling observations

On 2026-09-07, initial Lake invocations reported:

```text
error: operation not permitted (error code: 4294963248)
file: C:\Users\cdpan\OneDrive\Documents\Lean4 PAL test\.lake\config\0\lakefile.olean
```

This occurred after registering the experimental library. The cache files were
OneDrive reparse points. No specific OneDrive or Windows root cause was proved.
The controller verified that both cache paths were inside this workspace and
preserved the generated config directory as `.lake/config-preserved-20260907`.
An abandoned earlier CHARTER compiler process was stopped only after its exact
command and process identity were checked. No source documents or historical
audit records were deleted or changed by this repair.

Lake regenerated the configuration successfully; `lake env lean --version`
reported Lean 4.32.1. The separate historical `lake build PALLeanAudit` then
passed with 486 jobs. The combined final run records its own exact outputs.
These observations are tooling and preparation history, not PAL or CHARTER
proofs, countermodels, or source conformance verdicts.

Worker resumes PAL-RESUME-20260907-01 and CHAR-RESUME-20260907-01 preserved the
same task and grant after the cache repair. Their earlier blocked observations
remain preparation history. Every combined runner attempt is retained under a
unique evidence directory; the latest result is also available as results.json.

The first combined attempt passed every Lean and regression command, then
refused final success because claim metadata changed during semantic review.
Its complete output remains in its attempt directory. The corrected metadata
narrows labels and source routes without strengthening a theorem. The final
attempt uses those corrected inputs from its start.

Root also narrowed PAL23 imports before the final attempt. A source-inspection
candidate omitted the import supplying Set.range and failed elaboration with
Unknown constant Set.range. Adding Mathlib.Data.Set.Image made the same theorem
file compile successfully. This is an import repair, not a changed theorem or
a counterexample. Broad Mathlib.Tactic is no longer imported by PAL23.
