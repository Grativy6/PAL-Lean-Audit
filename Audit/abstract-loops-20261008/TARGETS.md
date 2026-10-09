# Abstract Loops workshop: selected targets

Activated by Chris on 8 October 2026: "can you do the abstract loops tests
from that wonderful workshop keyring". Only AL-A, AL-B, and AL-C are activated.
The five-paper key remains a historical preparation artifact. This run is local.

Controlling source: Abstract Loops v1.0, Christopher D. Pang, 15 August 2026,
DOI 10.5281/zenodo.21950771. Retained DOCX SHA-256:
`786f8c150917305b5afc3aa13b6fb28d26b1b15c363b28d335ea08089b4ba736`.
PDF SHA-256:
`decea53ec0d24670ed72ec7e68eb91109e885b78327494ed65fd8b09a1111112`.
Paragraph addresses use the frozen extraction under
`Audit/math-stack-20261008/source-reading/Abstract Loops.docx.txt`.

## Targets frozen before proof acceptance

| Batch | Source | Exact mathematical target and controls |
| --- | --- | --- |
| AL-A | P0014-P0026, P0034 | On arbitrary alternatives, finite reachable component images bound the actual joint image by their product. Certification bounds reachable answers by the actual joint image. Equal cardinalities alone do not certify; a diagonal joint image need not fill the product. Empty domains are permitted. |
| AL-A | P0045-P0046 | A fixed deterministic update schedule, initialized through a finite reachable trace image, eventually stabilizes its equality kernel even with infinitely many alternatives. Strict merges lower finite image cardinality; their count has a capacity bound, but their times do not. Delayed Boolean collapse and an infinite-image counterexample distinguish these claims. |
| AL-B | P0048 | One trace-only protocol with a uniformly correct output gives a reachable decoder. Pointwise favorable branches do not suffice. Certification alone does not place its decoder among supplied allowed operations. |
| AL-B | P0049-P0058 | Supplied coupled and baseline supports may be incomparable. Raw surplus can disappear under a readout. Observable surplus entails raw surplus, but not conversely. These are set-theoretic claims, not causal identification of a privileged baseline. |
| AL-B | P0059-P0062 | Declare infinite runs and maximal finite runs with valid indices. Under a nonempty run class, inevitability implies possibility. Possibility alone and an empty run class do not establish meaningful inevitability. Fairness restrictions are inputs. Absorption establishes persistence after entry; a transient visit need not persist. |
| AL-C | P0081-P0089 | Use a shared ambient typed roster space for coupled/baseline comparisons. Give an explicit finite model with separate identity, persistence, provenance, and baseline checks; a new roster tag alone does not qualify a carrier. A deterministic export factors through its complete initializer. A varying environment can prevent factorization through a narrower trace; fixed environment restores that particular factorization. |
| AL-C | P0091-P0107 | Typed returns can move hidden structure without readable residual. Returned identity/direct residual and absent/present export have four nonvacuous combinations. Compare readouts in the same alphabet and on declared reachable support. No physical carrier-generation or authority theorem is inferred. |

## Existing evidence and dependency boundary

C1 and C5 are reused, unchanged, through `AbstractLoopsJoint.lean` and
`AbstractLoopsPostprocessing.lean`. Their source hashes match this DOCX.
C1 has 9 theorems among 19 declarations; C5 has 8 among 12. Reuse is not new
corroboration. Historical ledgers remain unchanged; their former open coverage
items are addressed by a new receipt rather than retroactively relabeled.

All mathematical results in this run concern ordinary sets/functions, finite
models, and declared transition/run accounts. Proposal-level carrier criteria
remain explicit inputs or finite interpretations. Gravity, LQG, physical
realization, authorship/adoption, and other papers are outside this run.

## Verification and completion

For each module: build, inspect every explicit declaration and its exact axioms,
run bundled Lean kernel checking, check source policy, and retain immutable
command logs and input hashes. No proof holes, custom axioms, native decision
escapes, or silent statement changes. Development failures are tooling/proof
attempts unless a checked counterexample establishes otherwise.

Final review is self-review. Report source claim verdicts separately from finite
controls, definitions, helper lemmas, inherited results, and execution status.
Finish with a receipt book and clarification list linked from the paper shelf.
Commit selected files locally; do not publish or modify manuscripts.
