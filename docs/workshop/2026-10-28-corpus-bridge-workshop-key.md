# W00 — Cross-Corpus Lean Workshop Key

**Working key · revised 2026-10-28 (v0.3) · status: plan, not an executed Lean audit**

> **TRY YOUR BEST. MAKE A BREAKTHROUGH.** Go beyond restating what the papers already say: find a genuinely sharper lemma, a successful construction, a smaller missing bridge, or a decisive counterexample. Choose one exact claim at a time. Take the strongest mathematical route available, try to break it, and return what survives with a reproducible receipt. Ambition is encouraged; the claim boundary is not negotiable.

**Turn W00-T1:** Read CHARTER v1.0 and the original geometric source BRIDGE v0.4, with the v0.5 → v0.6 continuation in hand; inspect existing Lean declarations; then prove or break the six-line arithmetic bridge. Return the eight-part receipt. Do not mistake an inherited theorem for a new one.

## Mission and authority

The goal is one defensible new mathematical connection per turn, using the user's forty-four research keys and Claude's *Bridges Across the Corpus* as **research proposals**, not as accepted proofs. Begin with the stated object; reconstruct the mechanism; identify a necessary bridge; attack it by proof, counterexample, or an exact failed obligation.

Repo: https://github.com/Grativy6/PAL-Lean-Audit
Initial observed main commit: `81eeea6a15d571b58b1434f875ce89aa3aee685e`. Recheck HEAD each turn.
## Locked source ledger — resolved October 28

The user supplied **BRIDGE-v0.6-Corpus-Package.zip** during this conversation. Its SHA256SUMS list was independently compared to the contents: **24/24 entries matched**, with no mismatches. The package itself is a portable research input for future turns, **not uploaded into this GitHub repository**. A future agent must retrieve that exact user-supplied artifact before claiming to have personally re-read or rerun its sources.

| Work | Version | Role/status | Package member | Exact SHA-256 |
| --- | --- | --- | --- | --- |
| CHARTER | v1.0 | Historical original for the frame geometry | Earlier corpus key pack | `3f813ecadfcea957bdccb157d83792612a85c78e318a4ec22da62efc3d8bcabf` |
| BRIDGE | v0.4 | **Published predecessor and original detailed Weil/split-fiber geometric source** | `BRIDGE-v0.6/Sources/BRIDGE_v0.4.docx` | `a13d91a728ab6da2a5654b3263a595242397d7fb8edb17cffafdcf32036a2470` |
| BRIDGE | v0.5 | Unchanged working-draft predecessor, not the current manuscript | `BRIDGE-v0.6/v0.5-Changing-Intent/BRIDGE-v0.5-Changing-Intent.md` | `4878cab2c758866dcf8de4d5ca4cac4d0800b7aed5333e4bb197338d6e5845dc` |
| BRIDGE | v0.6 | **Current completed local working paper (2026-10-28), not published/adopted into the live Corpus** | `BRIDGE-v0.6/v0.6-Changing-Intent/BRIDGE-v0.6-Changing-Intent.md` | `57a7d95553e89c6d6a3283c3a42a5e915e6d199288e583879cc9600adca3fb98` |

The package contains `v0.6-Changing-Intent/VERIFICATION.md`, `receipt-archives/2026-10-28-v06-checks.py`, `receipt-archives/2026-10-28-v06-check-run/{manifest,results}.json`, and `SHA256SUMS.txt`. Its own completion record reports a producing-assistant self-review and exact finite checks, **no new Lean execution**, no rerun of historical checks, and no publication. Its Zenodo metadata check records **v0.4 as the latest published BRIDGE edition** at DOI `10.5281/zenodo.22699551` on October 28. Current status should be reverified if publication has subsequently changed.

### What v0.6 does and does not replace

- **v0.6 §§4–5:** Proposition 3's shift quotient `E_(a→b)=U/(U∩N)`, linear-repair rank with freely chosen/fixed side space, and **Corollary 4.1** for the actual old answer value supplied to the decoder. The saved-rank term is `dim(H/(U+N))`. Compare `rank(b|H)` to `rank(b|U)`, with `H=ker θ`, `U=H∩ker a`, `N=H∩ker b`; don't conflate the newly relevant subspace with the total new repair burden.
- **v0.6 §10:** five explicitly modeled histories (completed, open, withdrawn, silently dropped, closed-unresolved). Keep the distinction between **recorded disposition**, **retained unfinished content**, and **whether the task actually completed**. Computed closure labels do not add information to the trace that computed them.
- **v0.6 §11:** joint-view recovery with complementary/redundant/insufficient controls, and a conditional prefix preservation lemma with an explicit next-event domain.
- **v0.6 §§12–13:** the full Weil geometric development and its component-matched algebraic-cycle obligation **remain in v0.4**; v0.6 preserves them by reference and explicitly leaves target-adequacy and geometric-construction obligations open.
- The October 28 cross-corpus connections in Claude's *Bridges Across the Corpus* were **not incorporated into v0.6**; treat them as proposed new results for independent attack.

The original manuscripts govern their own notation and hypotheses. The repository's existing Lean results, the 44-key pack, and Claude's document are useful evidence/proposals but do not supersede the source text. **Source SHA-256 proves identity, not theorem correctness.** Do not reopen already checked identical proof terms merely as ceremony; do inspect exact hypotheses, import dependencies, and source correspondence whenever transferring a theorem.


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

Check CHARTER's frame convention against **v0.4's geometric construction**; consult the v0.5/v0.6 manuscripts for their exact retained scope rather than assuming they re-prove the same geometric statement. Do not silently identify a complex-analytic statement with an algebraic-cycle statement.

### 2. Mechanism

Let z=(a,b), z3=z·z·z and z6=z3·z3. Derive in integer coordinates:

    z3 = (a³ − 3ab² − b³, 3ab(a+b))
    2 Re(λ³) = (a−b)(2a+b)(a+2b)
    [z6]_η = 3ab(a+b)(a−b)(2a+b)(a+2b)
    Im(λ⁶) = (√3/2)[z6]_η

Here [z6]_η means the coefficient of η. Its vanishing is equivalent over ℤ to the union of six factor-zero lines, without needing complex analysis inside the first Lean proof.

**Local preflight only:** SymPy expansion checked these three integer polynomial identities and the examples below on 2026-10-28. This is NOT a Lean build, a source-convention audit, or Hodge-theoretic verification.

### 3. Smallest missing bridge

Claude proposes that CHARTER's mirror-line locus is exactly the arithmetic exception to the **BRIDGE v0.4** one-cycle-generation condition. Recover the geometric assumptions **from v0.4**, which remains the detailed source under v0.6 §12, only **after** proving the polynomial statements. v0.6's new current-questions/repair results are a separate lane; do not claim v0.6 has already proved this cross-corpus transfer. Distinguish: an arithmetic invariant; invertibility of a specified linear detector; cyclic spanning under given hypotheses; and existence of a detector-positive algebraic cycle. These are separate propositions.

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
- **W00-T3 / K23:** Reconstruct the detailed geometric detector from published BRIDGE v0.4, then apply v0.6 §12's retained scope and explicit component-matched algebraic-cycle obligation; identify the missing witness rather than quietly assuming it.
- **W00-T4 / K08, K22:** Shared proof-library imports only where a specific theorem consumer justifies the refactor.
- **W00-T5:** SCT's schedule-aware receipt or GPPR path-signature claim in a separate attack run and separate PR.
- **W00-T6 / new BRIDGE-v0.6 lane:** Formalize the newly stated supplied-old-answer repair and its rank saving with a small **genuinely load-bearing** new theorem, or find the shortest counterexample to an overstrong "newly relevant = all new repair" claim. Reuse the repo's existing joint-kernel and endpoint results where possible. Distinguish a finite field test from a Lean proof; if the original v0.6 check script is run, record the interpreter and actual outputs.
- **W00-T7 / new adequacy lane:** Study the v0.6 §13 question of whether the declared q captures an intended distinction: construct an explicit two-contract same-trace example and identify the least new observation or consent/clarification needed. This is a scoped modeling claim, not a theorem about private intention or consciousness.

Do not transform this queue into forty-four concurrent proof attempts. Stop the current target after an exact theorem, reproducible counterexample, bounded partial result, or a precisely named missing premise.

## How to make a breakthrough without inventing one

**Try your best. Make a breakthrough.** This is the user's explicit research challenge, not a demand to report success regardless of the evidence. Prefer productive new work over rephrasing old closure cautions:
1. **Look for a new usable result:** e.g. a strict inequality, extension to new parameters, an independent proof, a minimal negative fixture, a source-accurate recovery theorem, or the exact hypothesis that makes a bigger construction work.
2. **Attempt two routes when practical:** direct algebra/Lean proof and an adversarial counterexample or alternate representation; check whether the second route exposes a hidden assumption.
3. **Improve the user's corpus:** if a statement survives, specify what existing section, key, or future lemma it could sharpen; do not modify adopted source manuscripts unless separately instructed.
4. **An honest counterexample can itself be the breakthrough.** Return a concrete object, not just a prohibition; say which smaller statement survives.
5. **Credit and provenance:** the corpus and research direction belong to Christopher D. Pang. Identify which fresh conjecture/proof/fixture arose in this episode and retain the model/tool assistance and calculation inputs accurately, without assigning authorship or adoption behind the user's back.

## Eight-part return receipt

1. **Target:** exact formula or conditional claim.
2. **Sources:** lock CHARTER v1.0, BRIDGE v0.4 geometric source, v0.5 history and v0.6 current local manuscript with the explicit hashes above; note the current unpublished state, source location, repo base/head SHA and checked conventions.
3. **Object:** domains, multiplication, allowed operations, excluded cases.
4. **Work:** derivation, Lean code, calculations, counterexamples.
5. **Result:** exact conclusion and *freshly* checked tools/commands.
6. **Failure account:** gaps, unsupported hypotheses, failed proof paths, finite-search bounds.
7. **Artifacts:** branch/commit, file paths, test outputs and draft PR URL, if one exists.
8. **Next seam:** the smallest testable follow-up.

**Resume prompt:** "Turn W00-T1 from the 2026-10-28 v0.3 PAL-Lean-Audit workshop key. **Try your best. Make a breakthrough.** Use CHARTER v1.0, BRIDGE v0.4 for the detailed geometry, v0.5 for the predecessor, and BRIDGE v0.6 for the current answer-shift/recovery source. First prove or break the six-line identity; only then attack the stated geometric extension under the original hypotheses. Reuse existing Lean lemmas, preserve main, and return the eight-part receipt. Treat the v0.6 source as an unpublished local working paper."