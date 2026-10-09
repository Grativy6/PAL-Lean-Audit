# Reproducing this APCI pass

Use the installed pinned Lean 4.32.1 toolchain and the unchanged `Lean project`
at commit `0f85cc7fac47c3b34ecfd11160f3efae454b900c`. The preserved first run
is in `Receipts/2026-10-08-manuscript-check-01` relative to the APCI paper root.

`verify.py` records the exact compiler/checker arguments in `result.json`.
It uses the original project's already-built library and compares all tracked
source hashes with the earlier replay receipt before compiling the supplement.
It does not edit or rebuild the original project. The installed binary locations
are explicit Windows paths in the script; a different host must supply equivalent
pinned paths and report that adaptation.

From the APCI paper root, an authorized repeat should use the computation-audit
skill's `run_experiment.py` with:

- `computation-contract.json` from this audit;
- each path in that contract's `execution_artifacts` repeated as `--input`;
- a **new** directory under `Receipts` for `--output`;
- `--timeout 360 --max-output-bytes 2097152`;
- declared results `result.json`, `APCIManuscript.olean`,
  `compile-and-dependencies.log`, and `bundled-kernel.log` below that directory;
- command: the recorded Python interpreter with `-X utf8`, `verify.py`, and
  the same new receipt-directory path as its sole argument.

Validate the resulting manifest with the skill's `validate_manifest.py`, passing
the APCI paper root to `--root`. Validation checks evidence structure and hashes;
it does not establish source-to-formal meaning.

`map_sources.py` compares all fifteen published Appendix A entries with the
existing inventory and dependencies. It also writes the manually reviewed claim
mapping. It assumes the saved DOCX paragraph/table extraction and successful
first receipt are present; preserve them before revising this audit.

The original manuscript, repository, and earlier receipts are inputs. Do not
overwrite them to reproduce or extend this pass. A new pass should receive a
new receipt directory and should state whether it changes the claim or only
repeats its evidence.
