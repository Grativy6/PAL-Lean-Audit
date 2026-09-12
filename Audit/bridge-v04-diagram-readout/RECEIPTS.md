# BRIDGE diagram and readout receipt account

This lane records bounded Lean realizations for the selected BRIDGE v0.4
diagram and visible-sector readout claims. It preserves the four-sector and
13-declaration predecessor receipts byte-for-byte. The source snapshot is
immutable through P0199; this lane selects only P0108-P0192.

Use `python Audit/bridge-v04-diagram-readout/run.py --check` to validate a
saved receipt. Use `--run` for a new local receipt or `--replay` for a fresh CI
receipt. Passing `--source-file` performs the separately reported raw DOCX and
OOXML paragraph verification; CI uses only the selected snapshot.

The checks are formal evidence within declared assumptions. They do not prove
the whole manuscript, Hodge or geometric claims, recovery accounting, source
adoption, or closure of PAL obligations.

Each replay builds and kernel-checks the two new modules and the fourteen-declaration prerequisite, then runs historical checks. A saved Windows receipt is validated using its recorded command paths; Linux replay records its own paths and compares the resulting axioms against the frozen receipt. The local checkout, proposed PR head, and tested merge have separate fields. Sixteen altered-receipt guards require rejection after first validating the unaltered receipt.

The runner retains failed commands and their output in an execution receipt. Reproduce three real tooling failure probes (missing executable, nonzero exit, timeout) with `python Audit/bridge-v04-diagram-readout/failure_probes.py --output-dir <new-directory>`. These are separate from mathematical countercases. Failure outputs never replace a passing local result.
