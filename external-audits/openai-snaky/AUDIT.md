# Snaky in 21 Maker moves: local audit

Review date: October 8, 2026. Reviewer: Hearthline, working directly for Chris.

**Primary verdict: proved as written for the selected C21 conventional argument,
with its exact finite certificate reproduced.**

**Formal rerun: PARTIAL_RESOURCE.** The separate Lean check stopped at the
30-minute ceiling after compiling 83 of 94 proof modules. It did not reach
the final theorem comparison, axiom acceptance, or kernel replay. This visit
does not claim completed machine verification.

This review concerns the main 21-move result in OpenAI's *Snaky in 21 Maker moves*
(September 25, 2026), at repository revision
adc7f1241b42e322a6451854ab7e4b4c146bf78a.
The readable companion is Snaky-a-win-with-a-ceiling.pdf.

## Exact claim under review

On the initially empty board Z x Z, Maker and Breaker alternately claim one
previously unclaimed cell, with Maker first. Let

    S = {(0,0), (1,0), (2,0), (3,0), (3,1), (4,1)}.

Maker's winning sets contain an integer translate of any of the eight signed
coordinate permutations of S. Extra Maker cells are allowed. Scaling is not
allowed. Breaker only obstructs; there is no separate Breaker target.

**C21.** There exists a single globally legal Maker policy such that, for every
legal Breaker continuation from the empty board, Maker has won by its 21st
actual claim. An early win may be followed by fresh moves solely to express
the theorem at a fixed endpoint.

This is an upper bound, not an optimality result. It does not assert that no
20-move strategy exists, that every play lasts 21 moves, or that a naive greedy
player wins.

The selected official Lean target is:

    OAI.SnakyPrototype.snaky_winning_strategy_21_with_legal_states

The additional paper claim **CFIN** is a win within 21 Maker moves on the
specific 251-cell final envelope, hence also on the 17 x 17 square containing
it. CFIN is reviewed conventionally below; it is outside the selected formal
target.

## Argument and dependency map

1. A conditional card (A,T,h) asserts a win in at most h further Maker moves
   whenever Maker owns A and Breaker owns no cell in T. Both players' current
   ownership sets are finite and disjoint. The card applies to arbitrary
   additional Maker cells and arbitrary Breaker cells outside T.
2. Six base cards have T=S, A=S with one target cell omitted, and h=1.
3. A placement transports a card by a bijection of the entire integer grid
   that preserves allowed target copies.
4. A nonempty finite family of child cards (A_i,T_i,h_i), with pivot p, gives:

       T = {p} union (union_i T_i)
       A = ((union_i A_i) union (intersection_i T_i)) minus {p}
       h = 1 + max_i h_i

   Maker takes p if free, otherwise another fresh cell. Its resulting set
   contains all child requirements and the intersection of all their envelopes.
   A legal Breaker reply cannot be in that intersection, so at least one child
   avoids the new reply. Its envelope also avoids older Breaker stones because
   it lies inside the parent's clean envelope. That child applies next turn.
5. Every actual Maker move spends one unit and passes to a child of strictly
   lower height. Backward references and finite nested expressions allow
   induction to reduce the certificate to the six bases.
6. The final card has A empty, |T|=251, and h=21. Its hypotheses hold on the
   empty board. It has 32 placed children, each of height at most 20.
7. A fixed ordering of children and fresh cells gives one policy chosen before
   any future opponent replies. Lean instead chooses a good legal move
   classically from the winning-position predicate. This proves existence of
   a policy; it does not export an executable game program.

Dependencies:

    target geometry + six base finishes
                    |
        placement and combination lemmas
                    |
      finite certificate (728 numbered cards)
                    |
          empty-board WinsIn 21
                    |
       globally fresh policy + legal replies
                    |
      C21: win and actual move/state counts

The optional four-in-a-row discussion and the 25- and 35-move appendices are
not dependencies of this chosen route and were not separately audited.
No historical priority or novelty claim is made here.

## Obligations and findings

| Obligation | Finding and decisive reason |
| --- | --- |
| Target and transformations | The six cells agree between paper, Python, solution Model, and challenge. The eight maps are signed coordinate permutations, followed by translations. |
| Orientation numbering | Certificate and Model use different numberings. The map currentCode = [0,1,4,5,2,3,6,7] and theorem currentOrient_eq explicitly bridge them. |
| Nonempty child family | Both parsers reject empty lists. Lean's combination API requires a nonempty type; its finite intersection helper uses Fin (r+1). |
| Earlier and distant Breaker stones | Child envelopes lie inside the parent. Any reply outside the parent misses every child. The actual opponent has no imposed finite search radius. |
| Extra Maker ownership | A card tolerates extra Maker cells. An already-owned pivot is replaced by a real fresh move, including an actual ensuing Breaker reply. |
| Actual move count | Height is one plus the maximum child height. The policy is fresh on all finite states, and the formal endpoint explicitly has 21 distinct Maker cells. |
| Quantifier order | Maker chooses its move before the reply and a surviving child afterward. Existential policy precedes universal opponent continuation. |
| Legal-reply premise | An infinite grid minus finite ownership has a fresh cell. Semantics/Replies.lean proves existence of legal reply sequences, avoiding a vacuous result. |
| Final-turn indexing | For N=21, k+1<N checks Breaker replies 0 through 19. Final Maker ownership is compared with Breaker ownership after 20 rounds. An unconstrained 21st Breaker insertion does not affect the 21st Maker set. No legal post-win reply is required. |
| Universal bridge | The set reconstruction supports the composition lemma and induction. The 37,042 local reply classes are not enumeration of all complete games. |
| Finite board | Every prescribed pivot and base target stays in the nested final envelope. Before move m<=21, at most 2(m-1)<=40 cells are occupied. Its 251 cells therefore supply any needed fresh replacement. |
| Optimality | No lower bound excluding 20 was established or claimed. |

The written combination proof and move-count bridge are sound under these
rules, with no gap identified in the selected argument. The finite certificate
calculations were reproduced. The separate formal implementation remains
only partially rechecked locally, as detailed below.

## Finite computation

Exact certificate SHA-256:

    3fa12d36a6d4dbb185e3f2808c8dfde13d85ee309afbca030d6ad17ae9fe3d04

The certificate has 38,367 bytes, 722 numbered nonbase rows, 898 inline
combinations, 1,620 combination nodes, 4,089 references, and 37,042 local
reply classes.

Executed without changing the original programs:

- verification/verify_certificate.py, with assertions enabled.
- verification/supporting/route21/run_tests.py, directed to a fresh output
  folder. It runs primary.py and independent.py in normal, -O, and -OO modes.

**PASS.** All 728 complete numbered card records and 1,620 postorder records
agree across all six runs. The final requirement is empty, its envelope has
251 cells inside [0,16]^2, its pivot is (8,8), and its height is 21.

The tests also cover 108 malformed cases (18 mutations x two implementations
x three modes), each rejected both by raw reconstruction and by the checksum
entrypoint: 108 + 108 successful rejections. All 24 shifted-envelope boundary
tests passed. The second evaluator checks eight distinct signed permutation
matrices and all 64 pairwise compositions.

The evaluators have different parsers and transformation implementations,
but both are supplied by the same repository. Their agreement is implementation
diversity, not separate authorship or a second referee.

The bounded run used CPython 3.14.4 in Ubuntu WSL, exact integers, no randomness,
one CPU core, a 512 MiB per-process address-space cap, a 240-second per-process
CPU cap, and a 300-second wall cap. It completed in 226.577 seconds with exit 0.
The skill's manifest validator accepted the record and current input/output
hashes. Mathematical interpretation was reviewed separately.

Receipts are in computations/route21-001/: manifest.json, tests/report.json,
six complete reconstructed JSON files, and captured stdout/stderr. The input
contract is scripts/contract-finite.json.

## Formal run

**PARTIAL_RESOURCE.** The service ran from 04:07:10Z to 04:37:11Z on October 8,
2026, and stopped at its wall-clock ceiling. The log records 83 successful
solution-module builds out of the 94-module closure. It reported no proof
error before the timeout. The challenge statement compiled and was exported;
the solution's Main module was not reached.

The wrapper returned exit 1; the service reports timeout, signal TERM, runtime
30min 224ms, CPU time 51min 55.006s, and memory peak 8 GiB with 448.1 MiB swap.
No comparison acceptance, final axiom acceptance, or default-kernel replay was
obtained. The explicit AxiomAudit.lean inspection is PREPARED_NOT_RUN.

The build remains cached for a fresh bounded continuation. The 11 remaining
modules are listed exactly in evidence/verification-results.json. Nothing is
running in the background for this check.

The exact import closure contains 94 OAI modules and 71,326 source lines.
Its external import is Mathlib. The initial textual scan found no sorry, admit,
axiom declaration, native_decide, unsafe declaration, external implementation
hook, or compile-time IO command in the solution closure. This does not
replace checking proof terms.

The challenge file intentionally ends with sorry: it supplies the desired
statement for Comparator to compare with the separately built solution.
That placeholder is not imported by the solution and is not a gap in its proof.

The isolated Lake configuration changes only build scope. It retains
autoImplicit=false, all original solution/challenge files, Lean 4.34.1, and
Mathlib revision d13f23b723b8a846827a245b89c10fc7d3f11612. The original
whole-collection configuration and lock remain in source/; the narrowed
configuration is preserved in evidence/.

The run reuses pinned Lean, Comparator, lean4export, landrun, and Mathlib cache
from the pi workbench. It does not independently rebuild or bootstrap that
dependency stack. Executable hashes and actual Lean/Lake versions are in
evidence/build-source-manifest.json.

The official configuration permits only propext, Quot.sound, and Classical.choice.
Those are permitted axioms, not a completed axiom audit in this run. Nanoda is
disabled. Any later default Lean kernel replay would still not constitute a
second independent kernel implementation.

Resource ceiling: one 30-minute service, CPU quota 200%, memory 8 GiB, swap
1 GiB, Lean worker count 2. Its command and limits are in scripts/run-lean.sh.
The separate build lives at /home/cdpang/math-snaky-audit-20261007/project.
The prior pi proof source/results and neighboring PAL-lean workbench are untouched.

Post-run integrity checks passed for all 146 exported source files, 97 copied
build inputs, six tool files, and all nine dependency revision pins with clean
tracked source. The retained Linux build uses about 850 million logical bytes;
the H: entry was about 10.5 million bytes before final documents and sealing.

The next formal step is to resume the existing project under a new finite
allowance and a new log label, then run the same official Comparator through
acceptance and kernel replay. Only after Main compiles should the prepared
AxiomAudit.lean file be evaluated. Do not overwrite comparator-001 or interpret
its timeout as either a passed check or a mathematical refutation.

## Provenance and practical limits

The snapshot contains 146 selected files (6,399,798 bytes): the entire chosen
manuscript folder, exact target import closure, challenge, license, and build
metadata. Every exported blob was checked against its pinned Git object and
given a SHA-256 receipt in evidence/source-manifest.json.

An initial export preflight requested sizes across the blobless repository.
It was stopped when that began retrieving unrelated blob metadata. The export
was narrowed to tree names and selected objects. A subsequent storage count
hit Windows' ordinary path-length limit; extended-length paths resolved it.
These were preparation failures, not failed mathematical checks. No tracked
source was changed.

Before the snapshot the H: shelf contained 127,697,352,483 logical bytes, within
its 500,000,000,000-byte ceiling. This dive uses its own Snaky folder. It did
not use subagents, paid model calls, publication, or Branchline modifications.

The native LaTeX compiler returned "Unable to find standard directories for
platform". The editable TeX is retained with compilation unverified. The
readable PDF was generated separately with ReportLab and visually checked
by rendering all four pages; it is not a compilation of that TeX.

This is a single-assistant audit, not a blind referee report. A proof of this
game theorem does not establish a general safety or success guarantee for
open-ended agents. The resemblance in descending budgets is an analogy.

## Sources

- [Pinned manuscript](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Snaky-in-21-Maker-moves-September-25-2026/article.pdf)
- [Combination rule](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Snaky-in-21-Maker-moves-September-25-2026/build/templates.tex)
- [Certificate and endpoint](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Snaky-in-21-Maker-moves-September-25-2026/build/certificate-proof.tex)
- [Policy and finite-board proof](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Snaky-in-21-Maker-moves-September-25-2026/build/strategy.tex)
- [Formal scope](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/docs/187.md)
- [Selected theorem](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/OAI/GameTheory/SnakyTwentyOne/Main.lean)
- [Comparator challenge](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/SnakyTwentyOne.lean)
