# PAL v2.4 batch receipt runner

This directory contains a reusable, local-only runner for source-bound PAL v2.4 Lean batches. Each batch is a child directory (`B1`, `B2`, …) with a `claims.json`, target Lean module, and explicit axioms-inspection module. The runner has no network, publication, Git-write, or Lean-proof-generation behavior. It never edits Lean files.

A batch ledger has `batch`, `module`, `axioms_module`, `source_inputs`, and `claims`. Each source input has `path`, `sha256` (exact raw bytes), and `role`. Paths can be checkout-relative or absolute, including candidate documents and corpus files outside this repository. Each claim has a fully qualified `name`, `kind` (`theorem`, `def`, `structure`, or `inductive`), `classification`, `source_routes`, `assumptions`, human-readable `statement`, `ceiling`, and `residual`. Optional `allowed_axioms` may name a specifically reviewed imported axiom for that declaration; without it, only Lean's usual `propext`, `Quot.sound`, and `Classical.choice` are accepted. This exception is explicit evidence in the ledger, not a general allow-all switch.

The target module's explicit declarations must match the ledger exactly. The runner reports every inventoried declaration, while `theorem_count` counts only theorems. Structure-generated constructors/projections and compiler-generated helpers are not separate explicit source declarations. The axioms-inspection module must contain one `#check @Fully.Qualified.Name` and one `#print axioms Fully.Qualified.Name` per ledger claim, in ledger order. The executed Lean output is retained verbatim in a hash-recorded log, and the receipt stores the exact printed signatures and axiom lists. Human `statement` text is not substituted for Lean's checked type.

A run checks the candidate freeze marker at `Audit/pal-v24-candidate/source-manifest.json`. Any source input identified by candidate role or located under that candidate directory must have the same path and SHA-256 in that manifest. Every declared source-input hash is checked before execution, and all captured inputs—including ledger, target and inspection modules, runner, protocol, freeze manifest, and available Lake configuration—are hashed before and after. A changed input makes the receipt fail. Git branch, HEAD, dirty status, and exact porcelain text are recorded as observations; a dirty tree is reported honestly and is not silently called clean.

The Lean checks run sequentially and stop after the first failed command:

1. `lake build <target-module>`
2. `lake env lean <path-to-axioms-module>` (typechecks `#check` and emits `#print axioms`)
3. `lake env leanchecker <target-module>`

Lake/Lean/Python version commands are run first and recorded too. For every command the runner records argv, working directory, exit code, elapsed seconds, stdout/stderr digests, and a separate raw log with its own SHA-256. Forbidden source tokens (`sorry`, `admit`, `axiom`, `native_decide`, and `unsafe`) cause a preflight failure. The runner does not label a failed proof as a counterexample.

```powershell
python Audit/pal-v24-batches/run.py --run --batch B1 --lake C:\path\to\lake.exe
python Audit/pal-v24-batches/run.py --check --batch B1
python Audit/pal-v24-batches/run.py --self-check
```

`--run` requires an absolute Lake executable path and writes `B1/results.json` plus a unique `B1/evidence/attempt-.../` directory. Attempts and receipts are separate from source files. Each command log has a length-delimited header and retains the exact UTF-8 stdout/stderr bytes, so stream boundaries remain checkable even when output contains marker-like text. The receipt does not hash itself; the result and its evidence should be bound later by the containing Git commit or another separately held digest. A completed receipt is evidence only for these exact inputs and these bounded checks. It does not adopt PAL v2.4, prove the full source framework, authenticate external sources, establish authority, or certify physical persistence or runtime behavior.

`--check` performs no build, Lean invocation, or replay. For a passing receipt, it requires the complete current input inventory, all three version probes, and all three Lean checks in their expected order and with their ledger-derived arguments; every command must have exited successfully without Lean error diagnostics. It checks each raw log's byte hash, command metadata, exit status, stdout/stderr digests, the saved signature and axiom maps against the captured `#check`/`#print axioms` output, theorem count, and exact candidate-freeze digest. For failed receipts, it validates the recorded failure status, any sequential command prefix and its logs, and the recorded post-run input hashes; `PASS_SAVED_RECEIPT_CHECK ... status=FAILED_OR_BLOCKED` means the failure record is internally consistent, not that Lean passed. `--self-check` exercises pure-Python mutation guards for omitted/extra commands, wrong order, nonzero exit, missing or changed input hashes, forged signature/axiom maps, and the distinction between passing and failed records; it does not invoke Lean. A successful self-check is not a Lean receipt.

Do not interpret a missing freeze marker, source hash mismatch, failed command, changed input, or malformed receipt as a theorem counterexample. Preserve the failure record and investigate the specific boundary.
