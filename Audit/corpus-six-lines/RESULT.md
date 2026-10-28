# W00-T1 — One detector, a separate generator

**28 October 2026 · CHARTER–BRIDGE arithmetic and rational-plane investigation**

Christopher D. Pang supplied the corpus, research direction and authorization. Claude's *Bridges Across the Corpus* supplied the general-parameter six-line proposal. Hearthline reconstructed the source conventions, developed the explicit two-operator completion below, wrote the new proof code and checks, and retained the unsuccessful proof-script attempts. No literature-priority claim is made.

## 1. Target

Determine exactly how CHARTER's six exceptional lines relate to BRIDGE's detector, and whether a parameter which detects but fails to generate with its own action can still be used productively.

**Result of the derivation:** the detector needs one nonzero factor; same-operator generation needs two. A fixed second action removes the second restriction. This is an explicit instantiation of a two-operator interface already present in `Bridge.conditionalWeilDetector_iff`, not a new discovery of that abstract principle.

Machine verification and tested revisions are recorded separately in `RUN-RECEIPT.json`. This note's geometric corollary is a written conditional argument; the Lean module checks the coordinate/rational-plane statements.

## 2. Sources and correspondence

The original source bytes and hashes are recorded in `SOURCE-LOCK.json`.

| Source | Relevant location | Role here |
|---|---|---|
| CHARTER v1.0 | §§2, 5, 7.2 | Eisenstein convention, three determinants, six-line locus |
| BRIDGE v0.4 | Adjacent Weil Detector Theorem; One Cycle K Generation Equivalence | Specified rational Hodge target, actual algebraic action, sixth-power eigenvalues, detector and missing cycle |
| BRIDGE v0.5 | Changing Intent manuscript | Preserved intermediate version; not substituted for the geometric source |
| BRIDGE v0.6 | §§12–13 | Explicit retention of v0.4's detailed geometry and component-matched construction obligation |
| Claude, Bridges Across the Corpus | §1 | General-parameter identity and three-regime proposal being investigated |
| Existing repository | `Audit/BridgeEndpoint.lean`, `Bridge.conditionalWeilDetector_iff` | Already separates detector D from cyclic action J |

CHARTER and BRIDGE both use η=exp(iπ/3), η²=η−1 and q=N(a+bη)=a²+ab+b². No coordinate-sign change is needed. CHARTER's determinant convention is

\[
A_0=b(2a+b),\quad A_1=a^2-b^2,\quad A_2=-a(a+2b).
\]

A version number is not permission to change a theorem: BRIDGE v0.6 retains the original geometry by reference rather than replacing it with its new answer-shift calculus.

## 3. Object

Work first with pairs over a commutative ring:

\[
(a,b)(c,d)=(ac-bd,\;ad+bc+bd).
\]

Write `N(x,y)=x²+xy+y²` and `det(u,v)=u₁v₂−u₂v₁`. Polynomial identities hold over every commutative ring. Nonvanishing and reconstruction below are on the rational plane, where

\[
4N(x,y)=(2x+y)^2+3y^2,
\]

so the norm vanishes exactly at zero. For the complex reading, embed the pair as x+yη; its imaginary part is √3 y/2. That embedding supplies the meaning of “real”, but the initial Lean calculation does not require complex-number machinery.

For λ=a+bη set

\[
B=3ab(a+b),\qquad T=(a-b)(2a+b)(a+2b),\qquad q=N(\lambda).
\]

Let Fλ be multiplication by λ⁶ on this rational plane and Rλ=Fλ−q³I. These are explicit coordinate operators here; identifying them with the corresponding geometric actions requires the source hypotheses in §6 below.

## 4. Mechanism and direct derivation

Expanding the cube gives

\[
\lambda^3=(a^3-3ab^2-b^3)+B\eta,
\qquad 2\operatorname{Re}(\lambda^3)=T,
\qquad T^2+3B^2=4q^3.
\]

Consequently

\[
[\lambda^6]_\eta=BT=-3A_0A_1A_2,
\qquad \operatorname{Im}(\lambda^6)={\sqrt3\over2}BT.
\]

Over the integers, this coefficient vanishes exactly on the union of the six factor-zero lines (the origin is included). This closes the arithmetic comparison with CHARTER's locus.

The more useful distinction comes from two different determinants:

\[
\det R_\lambda=N(\lambda^6-q^3)=3q^3B^2,
\]
\[
\det(w,F_\lambda w)=BT\,N(w).
\]

For a nonzero rational vector w:

| Parameter | Detector Rλ | Pair (w,Fλw) |
|---|---|---|
| B=0 | Zero | Dependent |
| B≠0, T=0 | Nonzero scalar: −2q³I | Dependent |
| BT≠0 | Invertible | Independent |

The first row follows because λ³ is real and its square is q³. In the second row λ³ is purely imaginary, so λ⁶=−q³. The last row follows from the displayed determinants and positivity of the rational norm.

**The six-line condition does not say that all six lines are blind.** Three are blind; on the other three the detector works but its own Fλ cannot produce a second direction.

## 5. Construction: separate the two jobs

Fix μ=2+η and let G=Fμ. Direct multiplication gives

\[
\mu^6=-323+360\eta,\qquad \det(v,Gv)=360N(v).
\]

Every nonzero rational v therefore gives an independent pair (v,Gv). In particular, with u=Rλw,

\[
\boxed{\det(u,Gu)=1080q^3B^2N(w).}
\]

This is nonzero whenever B≠0 and w≠0, with **no T≠0 assumption**. Thus the entire detecting-but-scalar regime is usable once this second operator is available.

The completion is constructive: for any target t, set d=det(u,Gu). Then

\[
t={\det(t,Gu)\over d}u+{\det(u,t)\over d}Gu.
\]

The new module includes the general rational reconstruction identity, rather than reporting only that two vectors should span.

### Exact small witness

Take λ=1+η. Then q=3, λ⁶=−27 and Rλ=−54I. With w=(1,0), the old same-operator pair has determinant zero, whereas

\[
\det(R_\lambda w, G R_\lambda w)=1,049,760.
\]

This simultaneously refutes “detecting implies cyclic under the same operator” and demonstrates its two-operator repair.

### A wrong shortcut rejected

The action induced by η itself is not an auxiliary rotation on this sixth-power representation: η⁶=1. Replacing G with that action leaves the pair dependent. The negative fixture is a named Lean theorem, not merely a warning in prose.

## 6. Smallest remaining bridge to geometry

Here is the exact conditional geometric consequence; it is **not** an additional machine-checked Hodge formalization.

Assume the BRIDGE target Hdg³(A)=Qh³⊕W and that W is the rational plane represented above. Suppose actual algebraic correspondences realize both Fλ and G on this same target, with Fλh³=q³h³, and preserve rational algebraic classes. Let B≠0. For an algebraic class c with nonzero W-component w, Rλc is a nonzero algebraic class lying entirely in W. G(Rλc) is also algebraic. Their determinant in any corresponding rational basis is nonzero by §5, so they span W over Q. Together with h³ they span the stated Hodge target.

The proof uses only algebraicity preservation, the horizontal-killing property and the explicit independent pair. It supplies the cyclic premise of the repository's **existing** `Bridge.conditionalWeilDetector_iff` using a different action from the detector.

What this changes: the chosen detector parameter no longer needs to be off all six lines; it only needs to be off the three blind lines, provided the fixed second action is admitted.

What is still needed to apply it to the intended geometric component: a detector-positive **algebraic cycle on that component**, and the stipulated actual correspondences. The arithmetic gives an exact completion once that seed exists. It does not substitute a cohomology vector for the cycle or move a split-fiber cycle into another moduli component.

## 7. Checks, failures and artifacts

- New Lean file: `Experiments/CorpusBridgeSixLines.lean`, 22 named theorem declarations. This count includes supporting identities and controls; it is not a claim of 22 independent discoveries.
- Every declaration has an explicit type/axiom audit in `Experiments/CorpusBridgeSixLinesAxioms.lean`.
- Focused workflow: `.github/workflows/corpus-six-lines.yml`; it builds the actual module, inspects its declarations and invokes the pinned bundled `leanchecker` on it.
- Independent diagnostic: `check.py` and `local-checks.json`. Twelve exact symbolic identities; 624 nonzero parameter pairs; 14,976 parameter/vector cases; 13,248 successful rational reconstructions in the nonblind cases. Finite tests and general proof checks are different evidence.
- Failed compiler attempts and the eventual checking status are retained through the references in `EVIDENCE.md`, `RUN-RECEIPT.json`, and the downloadable workshop bundle. Neither failed tactic execution nor a successful old repository workflow is a result for the new theorem.

No original manuscript, inherited proof, dependency pin or main-branch content was changed. No paper release or canon adoption is performed by this draft PR.

## 8. Next live seam

The next compact derivation is a normal form. Put J=(G+143I)/180. In the rational-plane realization J²=−3I and

\[
2R_\lambda=-3B^2I+BTJ.
\]

That displays the detecting scalar and rotating parts separately. These normal-form identities are recorded as the next candidate, not added to the present 22-theorem receipt. A further practical question is which prescribed algebraic correspondences make this J available; a separate geometric investigation must supply the seed cycle.

The original Pell-frame queue remains available, but this episode stops at the completed W00-T1 proof/check boundary rather than silently launching several unrelated investigations.
