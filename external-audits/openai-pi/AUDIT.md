# Audit of the claimed irrationality exponent of pi

Primary verdict: **proved as written**, for the exact formal pi theorem below,
under Lean's standard permitted axioms and the documented toolchain trust base.
The local official Comparator check passed on October 7, 2026.
The separate Flint-Hills comparison, explicit axiom inspection, and post-run
source-integrity checks also passed. Status: COMPLETE.

Target: OpenAI, *The irrationality exponent of pi is 2* (September 24, 2026),
at repository revision `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
Audit requested by Chris on October 6, 2026. Source files are unmodified.

## Exact claim

For each real `nu > 2`, there is an integer `Q >= 2` such that every pair of
integers `p, q` with `q >= Q` satisfies `q^(-nu) <= |pi - p/q|`.
The supremum of positive exponents attained by infinitely many distinct reduced
rational approximations is exactly 2. The formal statement uses Mathlib's
`Real.pi`, real powers, and the usual rational denominator.

This does not give an effective value of Q, a uniform positive `c/q^2` bound,
or bounded continued-fraction coefficients. The theorem includes unreduced
fractions in its eventual lower bound. Denominators are eventually positive.

The separate Flint-Hills consequence is convergence of
`sum_{n>=1} 1/(n^3 sin(n)^2)`, with radians. It appears in Main.lean but is not
one of the theorems selected by the repository's PiExponent Comparator JSON.
The paper's more general series criterion was not selected as a separate
formal target. This audit does not verify the other papers in the repository.

## Verification results

| Check | Result | Retained evidence |
| --- | --- | --- |
| Compile supplied proof closure | PASS: all 869 OAI modules, including Main.lean | `evidence/attempt-02/comparator-run.log` |
| Exact official pi statement and referenced definitions | PASS: official Comparator target; no definition holes | `evidence/attempt-02/` |
| Allowed axioms and fresh default-kernel replay of pi theorem | PASS, exit 0 | `evidence/attempt-02/` |
| Explicit axiom listing of four named theorems | PASS: exactly the three standard permitted axioms | `evidence/supplement/axioms.log` |
| Separate Flint-Hills statement, definitions, axioms and kernel replay | PASS, exit 0; audit-authored challenge | `evidence/supplement/comparator.log` and `challenge.json` |
| Original source and isolated build copies | PASS: 869 proof files and 832 other preserved source artifacts match Git; original source tree clean | `evidence/source-integrity.json` |
| Nine resolved dependency repositories | PASS: all match their pinned revisions, with no tracked changes | `evidence/verification-results.json` |

The strongest supported statement is that these exact formal theorems have
been checked locally against the intended mathematical statements, with only
`propext`, `Classical.choice`, and `Quot.sound`, using Lean 4.34.1's default
kernel. The written proof review found no missing implication. That prose
review and the formal verification have different coverage, as detailed below.

## Proof structure and reading coverage

The paper's main text and all four proof sections were read. The principal
Lean definitions and implication chain were inspected; this was not a manual
line-by-line review of all 94,948 lines in the 869-module import closure.
Method: a single-assistant audit with self-review of externally authored work.
There was no separate, blind human or model referee pass. Re-running the
formal checker locally is distinct from having an independent referee or an
independent implementation of Lean's kernel.

```
unbounded approximations with exponent nu > 2
  -> rational constants with strict gaps
  -> one fixed finite dimension
  -> successively separated approximation scales and centers
  -> weighted interpolation surjectivity
     [local multiplicity bound -> curve inequality -> ample blow-up bundle
      -> eventual ordinary-power pushdown -> Serre vanishing]
  -> a nonzero square interpolation minor
     -> arithmetic determinant lower bound
     -> analytic determinant upper bound
  -> incompatible bounds, after the degree tends to infinity
  -> eventual lower bound for every nu > 2
  -> exponent exactly 2, using irrationality and pigeonhole
  -> Flint-Hills convergence, by a separate dyadic spacing argument
```

The key order of choices is dimension first, approximation scales and centers
second, degree limit last. The interpolation thresholds must not depend on the
chosen centers. The paper states this uniformity and supplies its multiplicity
argument for it. The formal chain discharges the existence of admissible
parameters from the assumed unbounded approximations; it does not merely assume
that an arbitrarily complicated set of inequalities is satisfiable.

## Obligations checked in the written argument

| Obligation | Reading result and limits |
| --- | --- |
| Same mathematical target | Passed: ordinary pi, positive eventual denominators, reduced rational supremum, no claim at the uniform exponent-2 boundary. The official formal comparison passed. |
| Constants can be chosen together | Passed on reconstruction: `A^2 < theta` leaves room for `A/theta < C < 1/A`, then `A < B < min(1/C,C*theta)`. A small positive eta preserves the strict approximation gap. |
| Dimension limit does what is required | Passed: `CB < 1`, `C*theta/B > 1`, and `B/A > 1` respectively drive the unwanted errors down and collision saving up. The chosen dimension then stays fixed. |
| Centers remain distinct | Passed: sufficiently large good approximants have nonzero numerators, so multiples of each coordinate step are distinct. Independence between different coordinates is not required. |
| Multiplicity and persistence argument | Traced: dimension counting supplies auxiliary polynomials; nested components at consecutive levels supply persistent derivative vanishing; the uniform local bound compares every pair of normal bases. No gap identified in this reading. |
| Differential obstruction | Passed on reconstruction: `dX_i = dY/Y` on an algebraic curve is incompatible with nonconstant Y, because exact meromorphic differentials have zero residues whereas a zero or pole of Y supplies a nonzero logarithmic residue. Characteristic zero is essential and present. |
| Remaining constant-Y case | Traced: separated weights force a unique normal basis and a constant coordinate; coordinatewise distinctness allows at most one center; the final zero-pole comparison contradicts the proposed violating curve. |
| Singular blow-up allowed | Passed against cited inputs: projective schemes suffice for nef plus ample, and the ideal is coherent and nonzero on an integral Noetherian scheme. No smoothness assumption was silently supplied. |
| Rees powers, not integral closures | Passed against cited inputs: only sufficiently high graded pieces are used. A finite affine cover gives a common threshold for ordinary powers and higher direct-image vanishing. |
| Direction of quotient map | Passed: `I^n` is contained in the ideal of series of weighted order at least `nR`. Surjectivity modulo `I^n` therefore gives the desired smaller quotient. Equality of these ideals is not required. |
| Formal/algebraic coordinates | Passed on reconstruction: replacing logarithms by sufficiently long Taylor polynomials gives mutually inverse filtration-preserving changes on each finite packet. |
| Nonzero determinant and lower bound | Traced: interpolation supplies full row rank and a nonzero minor; denominator clearing produces a nonzero Gaussian integer, whose modulus is at least one. |
| Analytic upper bound | Traced: repeated row indices annihilate terms; distinct derivative degrees give collision saving, with a complementary approximation-error case. Constants and error margins were checked against the final parameter selection. |
| Final contradiction | Passed on reconstruction: the same fixed data satisfy both estimates, with total error below the strict gap and collision saving exceeding the lower-bound margin. |
| Exponent at least 2 | Passed: pigeonhole plus irrationality supplies infinitely many reduced denominators for every exponent below 2. |
| Flint-Hills implication | Traced separately: choose `2 < nu < 5/2`; dyadic spacing yields a summable geometric exponent `2*nu-5 < 0`. No assertion at equality `nu = 5/2`. Separate exact formal target passed Comparator and kernel replay. |

These reading results are not substitutes for a kernel receipt, and finding no
gap is not an exhaustive certification of every prose step.

## External inputs checked

The following are primary-source checks of the forms used by the proof, not
novelty or community-acceptance claims. Their hypotheses were compared with the
specific construction in Section 2 of the paper.

- [Mondal, arXiv:1806.05346v5](https://arxiv.org/pdf/1806.05346v5),
  Corollary VIII.3 and Section IV.4.2: isolated affine intersections obey the
  degree-product bound, with multiplicity measured by the completed local
  quotient and equivalently by the local quotient at a smooth point. The
  paper uses complex affine slices. One-based PDF pages 150 and 76
  (printed pages 144 and 70) respectively; both were visually checked.
- [Lazarsfeld, Chapter 1](https://www.math.stonybrook.edu/robert.lazarsfeld/Reprints/Laz.PAG.Chapt1.pdf),
  Corollary 1.4.10, printed page 53 (one-based PDF page 49, visually checked):
  a nef real divisor plus a positive multiple
  of an ample real divisor is ample on a projective variety or scheme. This
  covers the possibly singular ordinary blow-up used here.
- Stacks [02OS](https://stacks.math.columbia.edu/tag/02OS),
  [02ND](https://stacks.math.columbia.edu/tag/02ND),
  [02NS](https://stacks.math.columbia.edu/tag/02NS): blow-up isomorphism away
  from the center, effective exceptional Cartier divisor, integrality and
  projectivity, and the sign of the relatively ample tautological bundle.
- Stacks [0AG6](https://stacks.math.columbia.edu/tag/0AG6) and
  [0AG7](https://stacks.math.columbia.edu/tag/0AG7): eventual cohomology
  vanishing and graded-piece recovery on Proj for a finitely generated,
  degree-one-generated algebra over a Noetherian ring. They apply to the
  ordinary Rees algebra on affine patches; the argument needs no claim for
  small powers.
- Stacks [0B5U](https://stacks.math.columbia.edu/tag/0B5U): Serre vanishing for
  coherent twists of an ample line bundle on a proper scheme over a
  Noetherian ring.
- Stacks [0BXX](https://stacks.math.columbia.edu/tag/0BXX), especially
  Theorem 53.2.6 and Lemma 53.2.8: nonsingular projective models of curves,
  smooth over a perfect field. The field here is C.

Historical best bounds and every background citation are outside this bounded
audit. The proof's own series argument was read instead of relying on the
secondary statement of a convergence criterion.

One background-source notation issue was confirmed visually in
[Meiburg, arXiv:2208.13356v1](https://arxiv.org/pdf/2208.13356v1),
Definition 2.1 on PDF page 2: the display takes an infimum over positive
exponents admitting infinitely many approximations. That formulation needs
a supremum; alternatively an infimum must range over exponents admitting
only finitely many. The following sentences use the standard intended
meaning, so this appears to be a typographical error. It is not a gap in the
OpenAI proof: that paper defines the exponent correctly and gives its own
Flint-Hills argument. The rendered page is retained in
`evidence/meiburg-definition-page2.png`. This observation is not a full audit
of Meiburg's paper.

The four reference PDFs used for the local literature checks are retained by
content hash in `.research-cache/literature/`; metadata, URLs, and integrity
results are recorded in `evidence/retained-reference-receipts.json`. These are
local research copies, not a proposed redistribution package.

## Formal verification setup

- Original Git revision: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
- Lean: `4.34.1`, official Linux release, commit
  `5045d0056413266e57c625dcd7c365b10e377c52`.
- Mathlib: `d13f23b723b8a846827a245b89c10fc7d3f11612`.
- Comparator: `d03acab154d269c06e60e4de7e4cc85deebff94b`.
  Its toolchain file alone was moved from Lean 4.34.0 to 4.34.1 so it could
  check this project. Comparator's proof-checking source was not changed.
- Lean4export: `076e8e57707e813375e8f9da8bf989799ace9680`.
- Landrun: `811cfff51ceaf3d9843708aa6d22e9b84ccac8b4`.
- Public Lean and Go downloads were checked against published SHA-256 values.
- The actual proof files were copied byte-for-byte; `evidence/build-source-manifest.json`
  records each SHA-256. An isolated Lake configuration registers the OAI library
  and pins only Mathlib, the sole external proof-library dependency of this
  closure. This is not a replay of the whole collection's unrelated dependency
  installation hooks.
- The standard Mathlib build cache was used. A claim of rebuilding every
  unrelated Mathlib module from source is not made.
- The repository's unmodified Comparator challenge selects `OAI.PiExponent.main`
  and permits only `propext`, `Quot.sound`, and `Classical.choice`.
- Its challenge intentionally contains `sorry` to specify the target. The
  solution must discharge that target without `sorryAx`. The initial textual
  scan found no proof holes or newly declared axioms in the supplied closure;
  the axiom audit, not that scan, is decisive.
- The supplied configuration has `enable_nanoda: false`. Standard Lean kernel
  replay was performed; no independent implementation of the kernel was run.
- Runs occur in an isolated folder in the existing Ubuntu WSL environment.
  Landrun remains enabled; a wrapper passes two Lean workers. The user service
  also denies Unix-domain sockets and caps memory/CPU. No host virtualization,
  global toolchain, application, or Branchline workspace was changed.

## Execution record

1. Source, tools and pinned Mathlib acquired; tool binaries built successfully.
2. First Comparator run built and exported the challenge, then stopped because
   the audit's initial narrow Lake root registration did not register the
   solution's sibling modules. This was an audit setup error, not a rejection
   of a proof term. The failed receipt is retained in `evidence/comparator-run.log`.
3. Lake registration corrected to `lean_lib OAI`, matching the original
   namespace registration. The supplied proof files remained unchanged.
4. `attempt-02` compiled all 869 OAI proof modules, including Main.lean,
   successfully on October 7 (the Lake run reports 9,792 jobs including
   dependencies). The official statement/definition comparison, permitted
   axiom check, and fresh-environment default Lean kernel replay all passed.
   The run exited 0, with both `Lean default kernel accepts the solution`
   and `Your solution is okay!` in the retained log.
5. Explicit `#print axioms` inspections of `main`,
   `pi_eventual_lower_bound`, `pi_irrationalityExponent_eq_two`, and
   `flint_hills_summable` all returned exactly `propext`, `Classical.choice`,
   and `Quot.sound`. That run exited 0. There is no `sorryAx` dependency.
6. The supplementary, audit-authored Flint-Hills challenge passed its own
   exact comparison, axiom restriction check, and default-kernel replay,
   exiting 0 with both acceptance markers. Its intentional `sorry` warning
   belongs to the challenge template, not the supplied solution.
7. Post-run hashes matched all original proof sources to their Git objects
   and isolated build copies. The original source checkout stayed clean.
   All nine resolved dependency repositories matched their locked revisions
   and had no tracked changes. Tool revisions, the sole Comparator toolchain
   patch, binary hashes, and measured storage were collected in
   `evidence/verification-results.json`.

The main run started at `2026-10-07T03:37:47Z` and ended at
`2026-10-07T04:56:57Z`. The service reports 1h 19m 9.293s runtime,
2h 37m 29.099s aggregate CPU time, and 11 GiB peak memory with 166.2 MiB
swap. These are measurements from the local WSL run, not performance promises
for another machine. The compilation and kernel replay are retained in
`evidence/attempt-02/`; the initial setup failure remains separately retained.
The supplementary sequence ran from `2026-10-07T04:57:09Z` to
`2026-10-07T05:15:32Z`. Within it, the explicit axiom run took 11.309s and
the Flint-Hills Comparator service took 18m 11.661s, peaking at 5 GiB with
no swap. Final receipt collection completed at approximately 05:15:52Z.

Reproduction entry point, from PowerShell with this workbench present:

```powershell
wsl -d Ubuntu --exec bash "/mnt/h/Hearthline's Path/Math Workbench/openai-math-pi-2026-10-06/scripts/run-comparator.sh" a-new-attempt-label
```

The installed isolated Linux tools and cached dependencies are prerequisites
for that entry point. Setup scripts are preserved in `scripts/`.

## Remaining limits and shelf contents

There is no unfinished required check in this bounded audit and no identified
mathematical gap to report. The reading is not a line-by-line certification of
all 94,948 source lines. The trusted public Lean release, pinned Mathlib cache,
default kernel implementation, operating system, and hardware remain part of
the verification trust base. Other papers and the broader series criterion
remain outside the selected formal targets.

Additional independence, if wanted later, would come from a blind specialist
review or a different kernel implementation. Repeating the same successful
default-kernel run would not supply that independence. Neither is required to
finish the present bounded local check.

The H: workbench occupies about 55 MiB including the pinned source, reports,
reference PDFs, and receipts. The isolated Linux tools, dependency cache, and
compiled objects occupy about 17 GiB in the existing WSL environment. They are
retained for reproducibility; no Branchline files or applications were changed.

`SHA256SUMS` covers the final report, README, scripts, and evidence files.
The source manifest and Git-object check cover the preserved upstream files;
the literature-cache receipt covers the public reference PDFs. The replay
scripts, original failed setup log, corrected run log, supplemental challenge,
axiom listing, tool versions, and dependency manifest remain available together.
