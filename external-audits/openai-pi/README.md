# OpenAI math: local audit of the pi claim

Chris authorized this check on 2026-10-06 after a read-only exploration.

Target: OpenAI, *The irrationality exponent of pi is 2*, September 24, 2026;
repository revision `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

For every real nu > 2, there is an integer Q >= 2 such that, for all integers
p and q >= Q, |pi - p/q| >= q^(-nu). The exact supremum characterization is
also in the supplied Comparator challenge. The Flint-Hills consequence is
reviewed separately; it is not in that challenge's selected statement.

This workbench preserves the pinned source and local receipts. No claim is
certified by a source scan alone. The review distinguishes the written
argument, the Lean statement and definitions, compilation, permitted axioms,
and kernel replay. It does not change Branchline or publish anything.

Initial state: 869 OAI modules are in the target's import closure, with 94,948
source lines. All external imports are Lean or Mathlib. The initial textual
scan found no sorry/admit, axiom declarations, unsafe declarations, native_decide,
external implementation attributes, or IO/process commands in this closure.
This scan is not a substitute for compiling and checking the proof terms.

Sources stayed byte-identical in `source/`. The isolated build used a smaller
Lake configuration requiring only the pinned Mathlib revision, because the
original whole-collection build pulls unrelated packages. This difference is
documented in `AUDIT.md`. The original Lean files and target were not patched.

Result: COMPLETE and VERIFIED on October 7. All 869 proof modules compiled, and the
official statement/definition comparison, permitted-axiom check, and default
Lean kernel replay passed with exit code 0. Explicit axiom inspection found
only `propext`, `Classical.choice`, and `Quot.sound` for all four inspected
theorems. The separate Flint-Hills comparison and kernel replay also passed.
Post-run source hashes matched Git and the build copies; all nine dependency
repositories matched their pins and had no tracked changes.

Start with `AUDIT.md` for the claim, proof map, findings, and coverage limits.
`evidence/verification-results.json` collects the machine results and exact
tool versions; `evidence/attempt-02/` and `evidence/supplement/` contain the
successful logs and exits. `SHA256SUMS` covers the final documents and receipts.
This was a single-assistant paper review and a real local Lean run; no separate
blind referee or alternative kernel implementation was used.

The temporary Linux build/tool area is `/home/cdpang/math-pi-audit-20261006` in
the existing Ubuntu WSL environment. It uses public tools and source only.
It is retained for replay and occupies about 17 GiB. The H: source-and-notes
workbench occupies about 55 MiB. Branchline remains unchanged.
