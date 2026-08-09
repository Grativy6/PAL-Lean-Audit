# Codex working instructions

This repository is an adversarial Lean audit of bounded claims from PAL v2.0. It is not a venue for silently rewriting PAL into whatever is easiest to formalize.

## Controlling sources

Use the exact source identities and hashes in `Audit/source-manifest.yaml`.

The coordinated PAL v2.0 authority surfaces control only their declared roles:

1. Mechanical Structural Spine — ordered mechanical claims.
2. Mathematical Realization Atlas — licensed formal realizations, countermodels, and return handles.
3. Obligation and Decision Ledger — adopted decisions, open burdens, provenance, and reopening addresses.
4. Conformance Tests — positive and negative fixtures and required receipts.
5. PAL 1.x Compatibility Note — migration and rejected legacy mappings.

PECAN, PEA Core, SEED, and optional PPP govern only their declared integration roles. BLA, boundary-readable trace, absorber-informed closure, CLEF, and similar works are bounded branches or laboratories. They may illuminate a model but may not redefine the spine.

## Hard formal boundaries

- Omega names unresolved possibility metalinguistically. Do not define a Lean object, type, constructor, value, set, model envelope, exterior, or residue as Omega.
- A0 is a supplied cut.
- Omega-star is the cut-indexed reflection, not Omega and not A0.
- Theta carries a prior trace-bearing turn or asymmetry. It selects no side and has no generic A1 eliminator.
- A1 earns readable oriented distinction.
- A2 earns recoverable consequence or occurrence trace; it is not merely duration.
- Residue is account-relative to a cut. Reopening preserves history and returns to a current unresolved boundary, never to Omega.
- Preserve no-free-distinction, trace conservation, witness-source honesty, no authority backflow, no branch absorption, and local closure.

## Formalization discipline

For every adopted Lean claim:

1. Name the controlling source card, decision, obligation, or T-number.
2. State the bounded realization separately from the PAL source claim.
3. Record assumptions, imported axioms, and authority ceiling.
4. Include a predecessor countercase or explain why the primitive-floor exception applies.
5. Prefer checked countermodels over prose claims that something is impossible.
6. Never turn a failed proof attempt into a counterexample.
7. Never strengthen `OPEN` into `PROVED` because a convenient encoding made the theorem trivial.

No `sorry`, `admit`, or unlisted `axiom` declaration may merge. Open burdens belong in `Audit/claim-ledger.json`, not in proof holes.

## Repository workflow

- Work on `agent/*` branches.
- Open draft pull requests first.
- Keep one attack run or infrastructure change per PR.
- Do not commit generated benchmark claims unless their source data and generator are included.
- Treat timing as runner-dependent measurement, never as theorem strength.
- Update generated reports with `python3 scripts/render_report.py` and verify with `--check`.
- Require the Lean audit workflow to pass before asking Christopher D. Pang to adopt or merge a formalization.

## Authorship and adoption

Christopher D. Pang is the author and steward of PAL and controls adoption decisions. AI systems are assistants and tools, not co-authors or authorities. A Codex-produced branch is a proposal until reviewed and adopted by Christopher D. Pang.
