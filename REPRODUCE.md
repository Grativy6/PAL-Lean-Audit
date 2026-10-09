# Reproduce the selected checks

Clone this repository normally. The personal projects use **Lean 4.32.1**.
The root and FRONT retain their own pinned Mathlib manifests; APCI uses core
and Std only. Install the declared Lean toolchain with Elan. From each
Mathlib project's directory, obtain its pinned dependencies and cached
compiled library with `lake exe cache get` before building.

| Check | Run from the repository root |
| --- | --- |
| Import identities, current links, external receipt preservation | `python scripts/check_collection.py` |
| Saved PAL v2.4 / Abstract Loops / workshop inputs and receipts | `python scripts/replay_collection_batches.py` |
| Fresh 22-batch replay, sequentially | `python scripts/replay_collection_batches.py --replay` |
| APCI core and separate manuscript supplement | `python scripts/replay_apci.py` |
| FRONT frozen inputs and publication concordance | `python projects/FRONT/scripts/ci_verify.py` |
| FRONT fresh replay | From `projects/FRONT`, run `python scripts/ci_verify.py --replay` |
| Historical root project | `lake build` then `lake env leanchecker PALLeanAudit` |
| Historical source policy and reports | `python scripts/check_policy.py` and `python scripts/render_report.py --check` |
| Original 27 PAL/CHARTER declarations | `python Audit/pal-v23-charter/check_publication.py --replay --lake lake` |

Use Python 3.10 or newer. On Linux, `python3` may be the interpreter's name.
Each fresh replay needs a new output directory; `--output` chooses one. The
batch adapter supports `--family pal24`, `--family loops` or `--family workshop`
for the three CI jobs. It never follows historical absolute manuscript paths.

The batch adapter verifies all saved logs, exits, ordered declarations,
signatures and axiom lists before a replay. It preserves the historical
receipts and writes fresh output under `.collection-evidence/`. Its negative
controls reject incomplete, altered and missing-input receipts.

For local manuscript/preparation-byte verification, pass `--source-root` with
the retained personal PAL-lean folder. The exact paths and hashes are in the
[batch inventory](provenance/migrations/2026-10-09/batch-inventory.json).
Public CI reports these local-only inputs as **NOT_REPLAYED_SOURCE_BYTES_LOCAL_ONLY**.
A passing code replay is not a claim that absent manuscript bytes were checked.
Some preexisting public files use LF where historical Windows receipts recorded
CRLF; each such byte translation is explicitly recorded, with both hashes.

The old local runners remain as historical evidence. They may depend on their
original folder layout, binaries and compiled-artifact hashes. Use these new
adapters for a portable replay; do not rewrite old receipts to match a new path.
In particular, the older whole-directory PAL/CHARTER scan can flag later files;
the scoped publication replay preserves its exact original population.

MIND's historical runner also binds a whole-repository inventory. Its CI uses
`python scripts/prepare_mind_replay.py FRESH_DIRECTORY` to verify all 520
original proof, runner, ledger and dependency input identities against this
collection, and then replays the original 521-input population in a detached
historical checkout. The one separately recorded difference is the current CI
orchestration file. New unrelated projects do not enter that old population.
The correspondence record accompanies the fresh MIND receipt.

The [collection workflow](.github/workflows/collection.yml) builds each project
in its own job and uploads the fresh logs, including hidden evidence folders.
Existing historical workflows remain. Read the tested revision and outcome;
the presence of a workflow is not proof that a run passed.

External audits retain their original toolchains (including Lean 4.34.1),
scripts and partial/completed statuses. See the [paper index](papers/INDEX.md).
This workflow checks their preserved bytes; it does not rerun the pi program,
complete Snaky or turn the Fourier reading visit into a Lean audit.

No offline environment or independent kernel implementation is promised.
Published Zenodo packages and mathematical statements are unchanged.
