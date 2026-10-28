# W00 — Cross-Corpus Lean Workshop Key

**Working key · 2026-10-28 · status: plan, not an executed Lean audit**

> **Turn W00-T1:** Read the original CHARTER and BRIDGE sources, inspect existing Lean declarations, then prove or break the six-line arithmetic bridge. Return a derivation or counterexample and a reproducible receipt. Do not mistake a repeated definition for a new result.

## Mission and authority

The goal is one defensible new mathematical connection per turn, using the user's forty-four research keys and Claude's *Bridges Across the Corpus* as **research proposals**, not as accepted proofs. Begin with the stated object; reconstruct the mechanism; identify a necessary bridge; attack it by proof, counterexample, or an exact failed obligation.

Repo: https://github.com/Grativy6/PAL-Lean-Audit
Initial observed main commit: `81eeea6a15d571b58b1434f875ce89aa3aee685e`. Recheck HEAD each turn.
Controlling original sources in the user's research pack:
- CHARTER v1.0, SHA-256 `3f813ecadfcea957bdccb157d83792612a85c78e318a4ec22da62efc3d8bcabf`.
- BRIDGE v0.4, SHA-256 `a13d91a728ab6da2a5654b3263a595242397d7fb8edb17cffafdcf32036a2470`.

The original manuscripts govern their own notation and hypotheses. The repo experiments, key pack and Claude document are not substitutes for those manuscripts.

Work on an `agent/*` branch. Preserve historical receipts, frozen publication hashes and adopted versions. No direct main edits, merges, force pushes, credential access, paid training, unrequested releases or automatic canonical adoption. Follow repository `AGENTS.md`, `papers/INDEX.md` and `REPRODUCE.md`. Separate scholarly evidence from the author's adoption decision.

## Already in the repository — reuse instead of re-proving

- `Experiments/AbstractLoopsJoint.lean` contains the joint-kernel law, reachable certification equivalence, and XOR counterexamples. Do not present these existing L1/L2 statements as new.
- `Experiments/Bridge.lean` gives endpoint residue and decoder results; `Audit/BridgeEndpoint.lean` gives appended-trace calculus and a **conditional** Weil detector theorem.
- `Experiments/Charter.lean` defines integer Q(a,b)=a²+ab+b² and proves adjacent-shell arithmetic.
- `Experiments/Pal24HistoryQuotient.lean` already analyzes continuation equivalence and a missing aperture-closure hypothesis.

The repository pins Lean `4.32.1` with Mathlib `v4.32.1`. Some other nested/external projects use different environments and are not interchangeable.

## W00-T1: CHARTER–BRIDGE six-line arithmetic

### 1. Object

Take η = exp(iπ/3), η² = η − 1, and represent λ = a + bη by (a,b) in ℤ × ℤ. Use *exact integer arithmetic*, with multiplication

    (a,b) · (c,d) = (ac − bd, ad + bc + bd)

and norm Q(a,b)=a²+ab+b².

Check the original CHARTER frame convention and original BRIDGE λ normalization before transferring the result between papers. Do not silently identify a complex-analytic statement with an algebraic-cycle statement.

### 2. Mechanism

Let z=(a,b), z3=z·z·z and z6=z3·z3. Derive in integer coordinates:

    z3 = (a³ − 3ab² − b³, 3ab(a+b))
    2 Re(λ³) = (a−b)(2a+b)(a+2b)
    [z6]_η = 3ab(a+b)(a−b)(2a+b)(a+2b)
    Im(λ⁶) = (√3/2)[z6]_η

Here [z6]_η means the coefficient of η. Its vanishing is equivalent over ℤ to the union of six factor-zero lines, without needing complex analysis inside the first Lean proof.

**Local preflight only:** SymPy expansion checked these three integer polynomial identities and the examples below on 2026-10-28. This is NOT a Lean build, a source-convention audit, or Hodge-theoretic verification.

### 3. Smallest missing bridge

Claude proposes that CHARTER's mirror-line locus is exactly the arithmetic exception to BRIDGE's one-cycle-generation condition. Recover the geometric assumptions from BRIDGE v0.4 **after** proving the polynomial statements. Distinguish: an arithmetic invariant; invertibility of a specified linear detector; cyclic spanning under given hypotheses; and existence of a detector-positive algebraic cycle. These are separate propositions.

### 4. Attack

1. Reconcile conjugation, signs, units, and the norm in both original papers; write an explicit change of coordinates if required.
2. Prove the formula for z3 and the η-coordinate of z6, preferably with `ring` and a minimal integer-pair representation.
3. Derive the six-line iff result using product-zero over ℤ, including λ=0 handling.
4. Retain these controls with exact values:
   - (0,1) = η: η-coefficient of z6 is 0; original 'blind' category.
   - (1,1) = 1+η: η-coefficient of z3 is 6 but of z6 is 0; detects-versus-generates distinction.
   - (2,1) = 2+η: Q=7, [z6]_η=360, Im(λ⁶)=180√3; off all six lines.
5. Attempt to falsify a stronger transfer claim: an integer identity alone does not provide the Weil-sixfold action or the required algebraic cycle. Name the first missing assumption precisely.

## Implementation lane (only after source check)

- Proposed new file: `Experiments/CorpusBridgeSixLines.lean`. Leave `Experiments/Charter.lean` and `Audit/BridgeEndpoint.lean` untouched.
- Proposed axiom report: `Experiments/CorpusBridgeSixLinesAxioms.lean` with #check and #print axioms for each declaration.
- No `sorry`, `admit`, or unlisted `axiom`. Keep failed routes and positive controls separate.
- Check with the pinned toolchain: `lake env lean Experiments/CorpusBridgeSixLines.lean` and the separate axiom file; run `lake build` and relevant repo policy/replay checks when integrating. A successful `lake build` that never imports the proposed module is NOT a test of it.
- If a compiler is unavailable locally, label this honestly; do not turn the SymPy check into a Lean success claim. CI results must be read from their actual run and SHA, not guessed.
- One mathematical target per PR. A draft PR is for review; a merge is not manuscript adoption.

## Queue after W00-T1, not parallel obligations

- **W00-T2 / K15:** CHARTER squared frame-area bound, equality family, Pell recurrence, and source conditions.
- **W00-T3 / K23:** BRIDGE detector domain and the exact extra bridge to an algebraic cycle, not just a cohomological readout.
- **W00-T4 / K08, K22:** Shared proof-library imports only where a specific theorem consumer justifies the refactor.
- **W00-T5:** SCT's schedule-aware receipt or GPPR path-signature claim in a separate attack run and separate PR.

Do not transform this queue into forty-four concurrent proof attempts. Stop the current target after an exact theorem, reproducible counterexample, bounded partial result, or a precisely named missing premise.

## Eight-part return receipt

1. **Target:** exact formula or conditional claim.
2. **Sources:** CHARTER/BRIDGE versions, file hashes, repo base/head SHA, and verified conventions.
3. **Object:** domains, multiplication, allowed operations, excluded cases.
4. **Work:** derivation, Lean code, calculations, counterexamples.
5. **Result:** exact conclusion and *freshly* checked tools/commands.
6. **Failure account:** gaps, unsupported hypotheses, failed proof paths, finite-search bounds.
7. **Artifacts:** branch/commit, file paths, test outputs and draft PR URL, if one exists.
8. **Next seam:** the smallest testable follow-up.

**Resume prompt:** "Turn W00-T1 from the PAL-Lean-Audit workshop key, using the original CHARTER v1.0 and BRIDGE v0.4 documents. Verify the integer-coordinate bridge in Lean and attack the transfer to BRIDGE's geometric detector. Return the eight-part receipt. Do not modify main."
