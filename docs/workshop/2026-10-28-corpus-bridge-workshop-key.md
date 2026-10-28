# W00 — Cross-Corpus Lean Workshop Key

**Working key · revised 2026-10-28 (v0.2) · status: plan, not an executed Lean audit**

> **Turn W00-T1:** Read the original CHARTER and BRIDGE sources, inspect existing Lean declarations, then prove or break the six-line arithmetic bridge. Return a derivation or counterexample and a reproducible receipt. Do not mistake a repeated definition for a new result.

## Mission and authority

The goal is one defensible new mathematical connection per turn, using the user's forty-four research keys and Claude's *Bridges Across the Corpus* as **research proposals**, not as accepted proofs. Begin with the stated object; reconstruct the mechanism; identify a necessary bridge; attack it by proof, counterexample, or an exact failed obligation.

Repo: https://github.com/Grativy6/PAL-Lean-Audit
Initial observed main commit: `81eeea6a15d571b58b1434f875ce89aa3aee685e`. Recheck HEAD each turn.
Source identities observed in the **earlier** user research pack:
- CHARTER v1.0, SHA-256 `3f813ecadfcea957bdccb157d83792612a85c78e318a4ec22da62efc3d8bcabf`.
- BRIDGE v0.4, SHA-256 `a13d91a728ab6da2a5654b3263a595242397d7fb8edb17cffafdcf32036a2470` — a **historical baseline**, NOT the current BRIDGE master source.

**New user-provided version facts (2026-10-28):** BRIDGE **v0.5** exists, and the user has recently **turned a v0.6 build/workflow key**. The v0.6 outcome, exact manuscript bytes, publication/adoption status, location, and hashes were **not present in the earlier corpus ZIP or inspected repository tree** at this revision; do not invent them or conclude that a v0.6 manuscript exists merely because its key was turned.

### Source-resolution gate for every BRIDGE-facing claim
1. Locate BRIDGE v0.5 and its exact status, publication identity if any, and bytes. Locate the v0.6 workflow key, its input locks, its current output/build status, and any resulting v0.6 draft, if available. User-supplied local/private artifacts take precedence over guessed public versions; do not silently download a different object by title.
2. Record a **version ledger** with `work | version | role (historical/candidate/current adopted) | source path | hash | claim location | accessible? | conflicts? | reviewer decision`. Treat a key, a generated draft, and an adopted/published manuscript as different things.
3. Compare relevant definitions, norm/conjugation conventions, standing hypotheses, and theorem statements **across v0.4 → v0.5 → any actual v0.6 output**. Do not assume the old Weil detector statement or coefficient generalization carried forward unchanged.
4. Scope W00-T1 initially to the **exact integer-coordinate identity** that can be checked independently of BRIDGE's version. Do not present the CHARTER–BRIDGE theorem transfer as current-version-consistent until the newly discovered source versions have been read and reconciled.
5. If newer sources are unavailable, **report that exact gap and stop at the arithmetic-only result**. Preserve the v0.4 comparison explicitly as historical; do not demand that the user repeat an answer already given.

The original manuscripts govern their own notation and hypotheses. The repo experiments, key pack and Claude document are not substitutes for those manuscripts. The corpus key pack's **K22 and K23** presently cite BRIDGE v0.4 and likewise require this version gate before any present-day BRIDGE work.

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

Check the CHARTER frame convention and compare the BRIDGE λ normalization across the **available** v0.4, v0.5 and any actual v0.6 draft before transferring the result between papers. Do not silently identify a complex-analytic statement with an algebraic-cycle statement.

### 2. Mechanism

Let z=(a,b), z3=z·z·z and z6=z3·z3. Derive in integer coordinates:

    z3 = (a³ − 3ab² − b³, 3ab(a+b))
    2 Re(λ³) = (a−b)(2a+b)(a+2b)
    [z6]_η = 3ab(a+b)(a−b)(2a+b)(a+2b)
    Im(λ⁶) = (√3/2)[z6]_η

Here [z6]_η means the coefficient of η. Its vanishing is equivalent over ℤ to the union of six factor-zero lines, without needing complex analysis inside the first Lean proof.

**Local preflight only:** SymPy expansion checked these three integer polynomial identities and the examples below on 2026-10-28. This is NOT a Lean build, a source-convention audit, or Hodge-theoretic verification.

### 3. Smallest missing bridge

Claude proposes that CHARTER's mirror-line locus is exactly the arithmetic exception to the **BRIDGE v0.4** one-cycle-generation condition. Recover the geometric assumptions from the relevant **current resolved BRIDGE source** only **after** proving the polynomial statements; compare against v0.4 as a historical test. Distinguish: an arithmetic invariant; invertibility of a specified linear detector; cyclic spanning under given hypotheses; and existence of a detector-positive algebraic cycle. These are separate propositions.

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
- **W00-T3 / K23:** First resolve BRIDGE v0.5 and the recently turned v0.6 workflow/result. Then investigate the version-correct detector domain and extra bridge to an algebraic cycle, not just a cohomological readout.
- **W00-T4 / K08, K22:** Shared proof-library imports only where a specific theorem consumer justifies the refactor.
- **W00-T5:** SCT's schedule-aware receipt or GPPR path-signature claim in a separate attack run and separate PR.

Do not transform this queue into forty-four concurrent proof attempts. Stop the current target after an exact theorem, reproducible counterexample, bounded partial result, or a precisely named missing premise.

## Eight-part return receipt

1. **Target:** exact formula or conditional claim.
2. **Sources:** CHARTER/BRIDGE version ledger (v0.4 historical, v0.5, v0.6 key/output as applicable), source/status distinctions, available hashes, repo base/head SHA, and verified conventions.
3. **Object:** domains, multiplication, allowed operations, excluded cases.
4. **Work:** derivation, Lean code, calculations, counterexamples.
5. **Result:** exact conclusion and *freshly* checked tools/commands.
6. **Failure account:** gaps, unsupported hypotheses, failed proof paths, finite-search bounds.
7. **Artifacts:** branch/commit, file paths, test outputs and draft PR URL, if one exists.
8. **Next seam:** the smallest testable follow-up.

**Resume prompt:** "Turn W00-T1 from the revised PAL-Lean-Audit workshop key. First resolve CHARTER v1.0, BRIDGE v0.5 and the recently turned BRIDGE v0.6 key/output; retain BRIDGE v0.4 as historical comparison. Prove or break the integer-coordinate identity in Lean. Attempt the geometric transfer only with the exact resolved source hypotheses, or name the missing version/source as the stop condition. Return the eight-part receipt. Do not modify main."
