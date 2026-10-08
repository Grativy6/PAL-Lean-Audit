# FRONT v1.0 — Lean audit companion

A source-bound mathematical companion to **FRONT — The Unclosed Dependency: Correction at the Next-Cut Seam**. The controlling source is Chris's supplied v1.0 working-draft archive, SHA-256 `e82195a52d3b65dcca8e6a16b1055c9772d43aa2ebecea6a4a5cd1409167fd9c`.

Start with the [receipt book](Audit/RECEIPT_BOOK.md), the [21-claim coverage map](Audit/COVERAGE.md), and the [machine-readable ledger](Audit/claims.json). Final verification is recorded in [the formal receipt](Audit/receipts/formal/receipt.json). A green build alone is not a verdict about the whole manuscript.

The work covers six approved batches: answers and adequate decisions; reuse and propagation; correction; continuation; linear interfaces and repair; costs and evidence. It keeps general mathematical theorems, explicitly bounded realizations, and finite program tests distinct. No new complexity separation, universal agent safety, external authentication, or independent peer review is claimed.

## Proofs

- `FrontLean/Answers.lean`: reachable-image sufficiency, labeled observations, common actions and exact coordinate capacity.
- `FrontLean/Propagation.lean`: a finite derivation calculus, conditional soundness, finite least Horn closure and wake decomposition.
- `FrontLean/Correction.lean`: recorded support, alternative derivations, commit guards and history-preserving scratch repair.
- `FrontLean/Continuation.lean`: future outputs and the separate condition for updating the chosen representation.
- `FrontLean/Horizon.lean`: finite observation horizon and a finite subfamily with the same common kernel.
- `FrontLean/Linear.lean`: linear factorization, the actual BRIDGE exact sequence, minimum side-trace rank and quotient dynamics.
- `FrontLean/Costs.lean`: amortized cost and conditional polynomial accounting.
- `FrontLean/Controls.lean`: counterexamples to stronger, unsupported readings.

The inherited APCI and BRIDGE modules are byte-preserved copies with their original namespaces. See [attribution and dependency notes](NOTICE.md). They are reused proofs, not new discoveries.

## Reproduce

Pinned Lean: `leanprover/lean4:v4.32.1`. Pinned Mathlib: `520045ab14e26149ee970e2e617ca04b09bde5d6`; all package revisions are in `lake-manifest.json`.

With the pinned dependencies available, run `lake build FrontLean`, then `lake env lean Audit/Axioms.lean`. For a bundled kernel replay of one module, run `lake env leanchecker FrontLean.Linear`; the exact 13-module sequence is retained in the final receipt.

On the original Windows audit checkout, `python scripts/verify_formal.py --check` verifies saved hashes, signatures and receipts without rerunning Lean. A new full run requires a fresh copy with `Audit/receipts/formal` absent; preserve existing evidence first. `scripts/verify_formal.py` refuses to overwrite that directory. The mathematical files themselves are not Windows-specific.

`Audit/fixture-source` contains the byte-locked correction study and its fixtures. The two fresh normal/optimized runs, raw events and manifests live in `Audit/runs`. The wrapper adapts only unavailable Windows resource telemetry to `null`; it leaves the frozen program unchanged. To run it directly, create a fresh empty directory under `Audit/runs`, then use `python scripts/replay_correction.py --output Audit/runs/your-fresh-name`. Add `-O` before the script for the optimized variant. Existing result directories are rejected by the original program.

`python scripts/audit_evidence.py` reaggregates all four correction records and the saved legacy reuse record, and extracts selected native Word equations. It also needs the preserved manuscript archive extracted at the adjacent `../Sources/v1.0/extracted/FRONT_v1.0_Working_Draft` location. This source package is not silently replaced by the older v0.4 image archive. No fresh legacy solver run is implied.

## Boundaries

The dedicated FRONT checkout was authorized by its own six-batch key. The shared PAL/CHARTER/BRIDGE checkout and other research projects were preserved. All execution here was local, with no model calls. This companion does not amend or adopt the manuscript. Publication and licensing require their own decision.
