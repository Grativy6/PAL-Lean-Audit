# APCI — receipt book

8 October 2026 · APCI v1.0.0 · local self-review

**Verdict for the bounded target: proved as written.** Theorems 1–5 match the
existing checked development. The written finite-answer corollary in §4.1 now
also has a checked Lean proof. No mathematical defect was found in that target.

The practical result is precise: if two possible situations leave the same
accessible trace but require different answers, a decoder using that trace alone
cannot answer both correctly. Forgetting some detail is not automatically a
failure; the forgotten detail has to matter to the question being answered.

This pass follows Chris's correction to run **APCI only**. The Abstract Loops,
Single-Cut Transport, Compactification Costs, GPPR, and Finite Abstraction lanes
were not executed or edited. The paper and its original proof repository remain
unchanged.

## What was checked

| Source claim | Exact scope | Evidence and verdict |
| --- | --- | --- |
| Theorem 1, §3, p4; P0048–P0050 | A decoder on the **reachable** trace subtype exists exactly when the required answer is constant on each trace fiber. | Existing A02–A04. **Proved as written**, using classical choice in the reverse direction. |
| Theorem 2, §3.1, pp4–5; P0052–P0057 | Decoding on **all** of the trace type additionally requires a nonempty function space `Trace → Answer`. | Existing A01, A05–A06, A12–A13. **Proved as written**; the empty-answer counterexample is retained. |
| Theorem 3, §3.2, p5; P0059–P0062 | A left inverse implies injectivity. This concerns identity recovery. | Existing A07. **Proved as written**. |
| Theorem 4, §4, p5; P0064–P0066 | A deterministic function of the same trace preserves an existing collision. | Existing A08. **Proved as written**. |
| Theorem 5, §4, p5; P0067–P0070 | For every natural n, a map `Fin (n+1) → Fin n` is noninjective and has no left inverse. | Existing A09–A11 and finite controls A14–A15. **Proved as written**, including n = 0. |
| Finite-answer corollary, §4.1, p6; P0072–P0073 | At most n reachable trace values cannot support exact answers for n+1 witnesses requiring pairwise-distinct answers. | **New formal coverage:** `APCIManuscript.no_exact_on_witness_of_capacity`. **Proved as written**. |

These are five named manuscript theorems corresponding to four original audit
targets, followed by one derived corollary. The original fifteen declarations
include implications, corollaries and controls; they are not fifteen independent
discoveries. The supplement adds one substantive coverage item and three scope
controls, not a second independent proof of the core.

## The new corollary

The formal statement permits arbitrary world, trace, and answer types. A finite
capacity is represented by an injective labeling of the actual reachable trace
subtype into `Fin n`. It does **not** require the ambient trace type or world
type to be finite.

The witness map chooses n+1 alternatives. Injectivity of the composed answer map
says precisely that their required answers are pairwise distinct. This also
prevents a repeated witness from satisfying the hypothesis accidentally. The
conclusion rules out decoding even if success is required only on those
witnesses and the decoder is defined only on their reachable traces.

The dependency chain is:

1. Map each witness through its actual reachable trace into its finite label.
2. The existing finite pigeonhole theorem supplies two different indices with
   the same label.
3. Injectivity of the labeling gives equality of their actual traces.
4. An exact decoder would give equal answers at those indices.
5. Pairwise-distinct answers contradict that equality.

The finite-labeling premise is an explicit mathematical expression of “at most
n reachable trace classes.” If a physical observation identifies different raw
records, that observational equivalence must first be modeled in the declared
trace type; this proof does not establish it.

[Supplementary Lean source](<Audits/2026-10-08-manuscript/APCIManuscript.lean>) ·
[Run result and exact commands](<Receipts/2026-10-08-manuscript-check-01/result.json>)

## Boundaries tested

| Obligation | Outcome |
| --- | --- |
| Reachable decoding must not silently become total decoding. | **Passed.** Original A12–A13 use empty worlds, a one-point trace type, and an empty answer type. Fiber constancy holds but no total decoder exists. |
| An inhabited answer type is sufficient, not necessary. | **Passed.** New control uses `World = Trace = Answer = Empty`; the empty total function works. |
| Noninjectivity alone must not forbid property certification. | **Passed.** New control collapses all natural-number worlds to one trace and still certifies a constant Boolean answer exactly. |
| New side information must not be mislabeled as postprocessing. | **Passed.** New control first loses a Boolean identity through a constant trace, then recovers it after appending the bit as an explicit side input. |
| Finite capacity must concern actual reachable traces. | **Passed.** The new corollary labels the reachable subtype, preserving arbitrary ambient types. |
| The smallest finite case must not disappear. | **Passed.** Original induction handles n = 0 through impossibility of an input's image in `Fin 0`; the supplement retains the universal n parameter. |
| All Appendix A names, target IDs, and dependency summaries must agree. | **Passed: 15/15.** Checked directly against the manuscript's DOCX table, repository inventory, and preserved local dependency output. |
| Source-to-formal translation needs review beyond successful compilation. | **Passed by self-review.** Raw proofs were read, hypotheses traced, and manuscript equations visually inspected on PDF pp4–7. No independent review is claimed. |

## What remains conditional

The physical application in §§5 and 9 is **conditional on a named input**: a
correct model of a concrete protocol's complete accessible trace, its allowed
side information, and its conflicting-answer collision or finite capacity. The
formal result proves the implication once those premises are supplied. It does
not establish a universal physical capacity or compulsory information loss.

The Shannon inequality in §6 is separate from the checked core. For a valid
finite uniform X with m alternatives and deterministic Y of support size at
most n, m and n are positive. The written algebra is

`H(X|Y) = H(X,Y) − H(Y) = log₂(m) − H(Y) ≥ log₂(m) − log₂(n)`.

This derivation is **conditional on the finite Shannon chain rule and the
support-size entropy bound**, which this pass did not formalize or re-audit
against the original literature. The physics citations, empirical premises,
and stochastic/quantum extensions were outside the bounded target. The paper
itself keeps those layers separate. No claim about RH, P versus NP, novelty,
priority, or numerical efficiency follows from this audit.

## Receipts and provenance

- Native Lean **4.32.1**, commit
  `f054605aea4b840552cca2e725580bffd1e1b704`; core plus bundled Std; no Mathlib or
  additional theorem package.
- The [earlier local replay](<Receipts/2026-10-08-local-replay/receipt.json>)
  passed the original fresh project build, fifteen-declaration inventory,
  dependency comparison, source policy, and bundled kernel checks. This pass
  compared every tracked source hash with that receipt and reused it honestly.
- The supplementary module compiled successfully and was explicitly replayed
  by bundled `leanchecker`. All four printed dependency records matched the
  expected inventory. No proof holes or custom postulates were introduced.
- The new corollary uses the standard dependencies `Classical.choice`,
  `propext`, and `Quot.sound`. The three new controls report no axioms. This is
  not an “axiom-free” label for the full development.
- Compilation took about 1.36 seconds; the supplemental kernel replay took
  about 3.07 seconds. The first attempt passed; no proof repairs were needed.
  The [run manifest](<Receipts/2026-10-08-manuscript-check-01/manifest.json>)
  records input/output hashes, versions, actual command, and resource limits.
- The supplement is local, separately hash-bound, and outside the frozen Git
  repository. Nothing was published or pushed. The original repository remained
  clean at the manuscript's commit and tree.
- Bundled `leanchecker` is another use of Lean's kernel, not an independent
  external verifier. The historical Rust nanoda attempt remains blocked before
  declaration checking. It was not rerun or promoted to a pass.

The manuscript cites post-merge CI run `31726224678`; the repository inventory
retains an earlier run `31725279522`. They identify different historical stages.
This pass verified the local commit/tree and dependency content, not the live
status or downloaded artifacts of those remote runs.

One byte-level detail was resolved: the published dependency-receipt hash
matches the Git blob exactly. The checked-out Windows copy differs only by
CRLF line endings. Both identities are recorded; neither was silently rewritten.
The predecessor ZIP remains unavailable for byte verification.

## Source lock and navigation

Manuscript: **Exact Certification Through a Declared Interface: Fiber
Factorization, Finite Capacity, and a Lean 4 Audit (APCI Run 0001)**,
Christopher D. Pang, v1.0.0, 13 August 2026.

| Artifact | SHA-256 / immutable identity |
| --- | --- |
| DOCX | `2068b0f359c32077989ed777d77520f3d8ee367c6cd705cd9ca6da39d0459c30` |
| PDF | `85602cf6801a543028f902f28cc43631e4a5cfacead56c07b8ef19f976e15fe3` |
| Original repository commit | `0f85cc7fac47c3b34ecfd11160f3efae454b900c` |
| Original repository tree | `a4418e2fb2c1fe5ffe6be768a419385da8834c99` |
| Original dependency receipt, Git blob | `16ef054d37dd5ec002ce95112f2209558459c5765dd7fb42bb304e47430a1753` |
| Supplementary Lean source | `e996a7b38e71402d6e58a07551015e858c0523ba6e475d15f8bf500a2e2005cf` |

[Full source-to-proof map](<Audits/2026-10-08-manuscript/SOURCE_MAP.json>) ·
[Bounded contract](<Audits/2026-10-08-manuscript/CONTRACT.md>) ·
[Reproduction notes](<Audits/2026-10-08-manuscript/REPRODUCE.md>)

Paragraph locators count direct DOCX body paragraphs, including blanks; table
locators count direct body tables. The extraction files are navigation aids,
not substitutes for the original equation structure. The source map preserves
exact declaration names and source line locations.

The bounded APCI lane is complete. The next mathematical gap, if reopened, is
a separately specified operational bridge or entropy/quantum development, not
a missing proof of the deterministic fiber core.
