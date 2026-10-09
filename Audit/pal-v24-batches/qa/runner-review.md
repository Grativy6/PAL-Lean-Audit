# Independent review: PAL v2.4 receipt runner

Review scope: static review of `Audit/pal-v24-batches/run.py` and its README on 2026-09-22. No Lean/Lake commands or receipts were run or modified.

## Finding addressed — saved-check validation accepted incomplete or inconsistent PASS receipts (high)

`validate_saved` (run.py:317–342) verifies only the input-hash entries that happen to be present and only the output-log hashes for command/version rows that happen to be present. It does not require the expected input-key set, the three version probes, or the three Lean commands; it does not validate command names/order/argv, zero exit codes, or compare log `EXIT` records with receipt `exit_code` values. `validate_receipt_core` (345–350) checks schema, a self-reported unchanged flag/hash-map equality, and declaration inventory, but does not close those gaps. The PASS-only checks validate theorem count, candidate freeze binding, and axiom/signature key sets/allowed axiom names, not the evidence fields' consistency.

Before the repair, a saved PASS receipt could have command rows removed (including all three Lean checks), an input-hash map with required target/runner/config entries omitted, or a nonzero `exit_code` in the receipt while retaining `status: PASS_BOUNDED_LEAN_CHECKS`; `--check` could still print `PASS_SAVED_RECEIPT_CHECK`. Since the README expressly says the receipt does not hash itself and needs later external binding, this is not tamper-evidence. It was a validation defect: the saved checker advertised a PASS check without verifying required records.

Repair implemented in `run.py`: passing receipts require the exact tool-input inventory, three version probes, three expected Lean commands in order, zero exits/no error diagnostics, and matching parsed signatures/axioms. Length-delimited command logs are checked against their command rows, output digests, exit codes, and saved output maps. The Python-only self-check now exercises removed/added/reordered commands, nonzero exit, missing/changed inputs, forged signature/axiom maps, and failure-status preservation. `--check` remains non-replaying and validates consistency rather than independently re-executing Lean.

## Scoped observations

- The live `--run` path checks each command return code and rejects Lean error diagnostics, runs the three declared checks sequentially, and returns nonzero for a run failure. `--check` distinguishes saved-record validation from Lean success by retaining and printing the receipt status.
- The receipt still does not hash itself. The new checks establish local byte/field consistency only; they do not authenticate who created a receipt or prevent coordinated rewriting of `results.json` and its logs. Bind those artifacts with a containing commit or separately held digest when that provenance is needed.
- The inspected checkout currently lacks `Audit/pal-v24-candidate/source-manifest.json` (the runner's `FREEZE`, run.py:17, 189–211). Thus any new `--run` is currently blocked before Lean execution, including a C1 run; this is an environment/release-input gap, not evidence against C1's theorem statements.

Verification: a Python source compile check and `--self-check` are the appropriate bounded checks for this repair. No Lean run, final receipt, or particular saved receipt is assessed here. The candidate source-manifest file is still required before `--run` can produce a Lean receipt.
