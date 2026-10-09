# Abstract Loops v1.0 — workshop receipt book

**Completed locally on 8 October 2026.** All three selected batches passed their
module builds, exact declaration/type/axiom inspection, and the bundled Lean
kernel checker. The final inputs and logs also passed saved-receipt validation.

The main new result closes the earlier C5 coverage gap: **finitely many reachable
trace values are enough for eventual kernel stabilization, even with infinitely
many alternatives.** The initializer only needs to be defined on reachable
trace values. No new observation enters, and the update schedule is fixed.

No new mathematical defect was found in the selected source claims. Several
counterexamples confirm why the paper's existing restrictions matter. This is
a source-bound audit of selected mathematics, not a proof of the whole paper
or its proposed physical realizations.

## What came back

| Batch | What was checked | Receipt |
| --- | --- | --- |
| AL-A — capacity and stabilization | Reachable joint capacity, necessary answer capacity, the full finite-image stabilization statement, a bound on strict merge events, arbitrarily delayed merging, and an infinite-image counterexample. | [Execution](AL-A/results.json) · [Claim ledger](AL-A/claims.json) · [Lean](../../Experiments/AbstractLoopsFiniteImage.lean) |
| AL-B — dynamics and quantifiers | Uniform deterministic/nondeterministic protocols versus favorable individual branches; raw versus observable surplus; incomparable reachable sets; complete runs, nonempty run classes, possibility, inevitability, explicit run restrictions, and absorbing failure. | [Execution](AL-B/results.json) · [Claim ledger](AL-B/claims.json) · [Lean](../../Experiments/AbstractLoopsDynamics.lean) |
| AL-C — return and export | Hidden state motion with readable identity; all four return/export combinations; a common ambient roster model with explicit address, cut, persistence, source-copy and baseline witnesses; full-initializer versus narrower-trace information ceilings. | [Execution](AL-C/results.json) · [Claim ledger](AL-C/claims.json) · [Lean](../../Experiments/AbstractLoopsReturnExport.lean) |

## What the results mean

**Capacity counts reachable values.** Pairing two traces cannot exceed the
product of their reachable capacities, and a certifiable answer cannot have
more reachable values than the joint trace. A diagonal support can miss most
of the ambient product. Even having enough labels does not establish that
those labels distinguish the right answers: the inherited XOR obstruction
supplies a checked control.

**A limit on losses is not a deadline.** If the initial reachable state image
has `m > 0` values, at most `m - 1` update steps can strictly merge kernel
blocks. Each such step is proved equivalent to a strict decrease in reachable
image cardinality. A two-value schedule can nevertheless wait any chosen
number of steps before merging. With an infinite initial image, predecessor
on natural numbers keeps producing fresh merges forever. These are universal
proofs about all natural delays/times, not tests of a finite sample.

**A favorable branch is not a uniform method.** A constant trace can accompany
a choice that happens to match each world's answer, without furnishing a
decoder from that trace. Conversely, a protocol whose allowed outputs depend
only on the trace, are nonempty there, and are all correct does give
certification. A set-theoretic decoder can still be unavailable to a supplied
machine with restricted output operations.

**Possibility and inevitability need different receipts.** Both a forever-waiting
run and a failing run are complete paths of the same declared transition
system. Failure is possible there and is not inevitable. Restricting the run
class changes the result, but that restriction must be stated. Empty run
classes expose the vacuity trap. Infinite-run persistence is proved under an
explicit absorption hypothesis; finite runs have actual finite index types,
and a maximal finite deadlock fixture checks the endpoint convention.

**Return and export remain separate.** In the finite roster model, A/B readouts
can agree before and after while C has a new address, retains a source-derived
value, persists at every positive time, and is absent from the declared
baseline. Separate counterfixtures show that a new address alone guarantees
neither persistence nor the stated source-copy relation. These are checks of
an explicit mathematical interpretation; deciding that such witnesses are
adequate for a physical carrier is a further task.

**The input boundary matters.** If a varying environmental coordinate reaches
the export, the information ceiling belongs to the complete initializer.
The smaller original trace can fail to certify that export. Fixing the extra
coordinate restores the corresponding trace factorization. The paper already
states this distinction at P0087-P0089.

## Coverage and counting

| Batch | Explicit declarations | Theorems within that inventory | Definitions / inductive types |
| --- | ---: | ---: | ---: |
| AL-A | 22 | 19 | 3 |
| AL-B | 28 | 17 | 11 |
| AL-C | 26 | 12 | 14 |

The 48 theorem declarations include helper lemmas, counterexamples, elementary
interface checks, and two explicitly marked reused results/specializations.
They are **not 48 independent discoveries or 48 independently audited source
claims**. The [machine summary](summary.json) separates declaration roles.
Compiler-generated constructors and recursors are not added to these counts.

The earlier C1 and C5 modules are reused unchanged. C1's 19 declarations/9
theorems and C5's 12 declarations/8 theorems keep their original receipts and
counts. Their historical open entries were not overwritten; this new run
records which former coverage gaps it closes.

## Source, verification, and remaining limits

Source: Christopher D. Pang, *Abstract Loops v1.0*, 15 August 2026,
DOI `10.5281/zenodo.21950771`. The retained DOCX and PDF match the prepared key's
full SHA-256 identities. No manuscript was edited. See the
[source manifest](source-manifest.json), [frozen targets](TARGETS.md), and
[mathematical review](REVIEW.md).

Lean/Mathlib remain v4.32.1. The only axioms reported across these declarations
are the standard `propext`, `Quot.sound`, and `Classical.choice`, with exact
per-declaration lists in each receipt. There are no proof holes, custom axiom
declarations, or native-decision shortcuts in the new modules.

The [integration receipt](integration-results.json) records the default project
build, root kernel check, historical source policy, and all three generated
report checks. New experiment sources receive their own inventory/policy
checks because the historical policy script does not scan that directory.
Six mutation controls check that the receipt validator rejects missing or
reordered commands, a failed command, altered signatures/axioms, and changed
input records. Timings are local execution records, not performance claims.

This is **self-review using the bundled checker**, not an independent review
or an independently implemented kernel. Carrier adequacy, causal identification
of a privileged baseline, resource/implementation bounds, and the gravity/LQG
realization program remain outside what these receipts establish.

For details Chris might want to emphasize in the writing, see
[Clarifications for Chris](CLARIFICATIONS.md). The existing wording already
contains the important qualifications; none of these checks requires a new
version of the manuscript.

## Replay

From the shared Lean project, run `verify.py --batch AL-A`, then AL-B, then
AL-C with the local Python runtime. It records new evidence directories and
updates only the new batch's latest receipt. Add `--check` to validate an
existing receipt without running Lean. `integration.py` checks the receipt set
and existing project gates. These scripts use the retained source copies on
this shelf and the local pinned toolchain; they never follow historical E:
source locations.

[Abstract Loops shelf](<../../../Other mathematics/Abstract Loops/README.md>) ·
[Personal workbench](../../../WORKBENCH.md) ·
[Workshop key](../../workbench/keys/20261008-five-paper-audit/WORKFLOW_KEY.md)
