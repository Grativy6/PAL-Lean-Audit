# W00 projector/generator — a checked concrete corollary

**29 October 2026 · Native Lean 4.32.1 proof, dependency inspection and bundled kernel replay passed.**

The activated target is reached in the stated rational model. The norm-three
projector and norm-seven generator now instantiate the existing
`Bridge.conditionalWeilDetector_iff`. The inherited six-line core is unchanged.
The new result is `Experiments.CorpusBridgeProjector.projector_generator_complete_iff`.

Let `W = Q²`, `H = Q × W`, and use eta² = eta − 1. For rho = 1+eta and
mu = 2+eta, the maps are

```
Fρ(h,w) = (27h, -27w)
G(w)    = multiplication by mu^6 = -323 + 360 eta on W
Fμ(h,w) = (343h, G(w))
P       = (27 I - Fρ) / 54.
```

For **every rational submodule A of H** containing the known line and preserved
by both Fρ and Fμ, Lean proves

```
A = H  if and only if  some c in A has P(c) != 0.
```

This is an exact theorem with explicit hypotheses. It is not a claim that the
formal model constructs an abelian variety or an algebraic cycle.

## What the proof contributes

The action-to-coordinate lemmas tie both selected parameters to the unchanged
Eisenstein arithmetic. The projector is defined by the displayed spectral
formula, then proved to satisfy `P(h,w) = (0,w)`. Its purity, nonvanishing and
idempotence follow. Stability under Fρ implies stability under P because A is
a rational submodule.

The generator step uses the existing determinant identity
`det(w,Gw) = 360 N(w)`. For nonzero rational w this is nonzero. The core's
already checked Cramer reconstruction supplies explicit coefficients for every
target vector in the pair `(w,Gw)`. It discharges the cyclic-generation premise
of `Bridge.conditionalWeilDetector_iff`; the main proof actually calls that
theorem with P and G, rather than merely mentioning it in a report.

The two mathematical controls also passed Lean and kernel replay:

- `dropping_generator_stability_fails`: `span(h,e1)` contains the known line,
  is Fρ-stable and has a nonzero projected seed, but is a proper subspace. Its
  failure of Fμ-stability is exhibited. The second action hypothesis matters.
- `mixedProjector_not_idempotent`: on the extra mixed action represented by
  multiplication by `-27 + 27 eta`, the same projector formula fails
  idempotence at `(1,0)`. The domain restriction matters.

The 17 named declarations include supporting facts and controls; they are not
17 independent discoveries. Their exact inventory is [declarations.json](declarations.json).

## Is the bridge novel?

The connection is mathematically valid and now usable by the existing formal
interface. Its mechanism is an **explicit formal corollary**, not a new general
principle of projection or generation. The prior BRIDGE paper already supplies
a rational projector and one-cycle generation account, and the repository
already separates detector and generator abstractly. This change supplies the
concrete norm-three/norm-seven instance, source correspondence and checked
consumer that were missing from this implementation.

The supporting ideas have clear older antecedents. Involution/projector
correspondence appears, for example, in Harvard Math 23a's 2002 assignment,
problem 4. Quadratic-field generation follows from the standard simple-extension
basis theorem. Markman's cited split-Weil account explicitly uses one nonzero
algebraic Weil class and the K-action to obtain the whole Weil space.
[Exact sources, translations and bounded search scope](SOURCES.md).

Accordingly, this episode establishes a useful explicit corollary and its Lean
implementation. It does **not** establish global mathematical priority for the
specific parameter pairing or a new Hodge-theoretic existence result.

## Checks and retained failures

The native run [receipt](evidence/run.json) records the actual compiler identity,
pinned Mathlib revision, command exits and output hashes. It built the inherited
core and detector interface, built the extension, inspected every declared
type/dependency list, ran bundled leanchecker on the extension, and checked the
affected source policy. All commands passed. The existing detector-interface
linter warning is retained in its output; the new proof module builds without
warnings.

[Verification](evidence/verification.json) accepts exactly 17 dependency reports,
all using subsets of `propext`, `Classical.choice`, and `Quot.sound`. It also
rejects missing critical output, an unapproved axiom, an admission dependency
and duplicated output. These four evidence controls are separate from the
mathematical counterexamples. The inherited proof files and pins match base
`bd49451caa409fe9091f209048afe814fa9aa30b`.

The first compilation failed on a name collision with Mathlib's extended norm,
tuple ascription syntax, and a proof presentation of product scalar actions.
Those local typing/presentation errors were repaired without changing the
target's hypotheses or conclusion. The original [compiler output](development/attempt-01.txt)
is retained. A theorem-inventory draft also caught a word in a block comment;
the final verifier reuses the repository's comment-aware scanner. No failed
attempt is counted as a mathematical counterexample.

The first CI integration exposed a frozen-input conflict: a root Git attribute
rule for these new logs changed MIND's preserved inventory. The rule was moved
into this run's own directory, the root file restored exactly, and all 520
current MIND input identities checked without mismatch. The proof sources were
unchanged. [Integration record](development/integration-01.json).

Fresh CI is provided by [the focused workflow](../../.github/workflows/corpus-projector.yml).
Its current run outcome belongs to the PR checks, separately from the local
receipt. It builds the actual extension, checks all dependencies and replays
the kernel; a successful old root workflow is not substituted for that result.

## Review and stopping point

[Adversarial self-review](REVIEW.md) reconstructs the target, dependency chain,
source correspondence and hypothesis controls. No independent human or
fresh-agent review is claimed. The source papers and the earlier W00 versions
remain unchanged; this extension is a proposal on its own branch.

The selected projector/generator key is finished at this proof boundary.
The full operator-algebra classification, a Lean minimum-norm certificate,
Pell-frame work and geometric cycle construction are separate follow-ups.
They are not needed to turn this completed corollary into a result, and none
was silently activated here.

Christopher D. Pang supplied the corpus, direction and activation. Hearthline
provided implementation, checks and self-review assistance. No source adoption,
merge or publication of a new manuscript is performed by this record.
