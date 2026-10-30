# W00 projector/generator extension — target

Activated by Chris on 29 October 2026, America/New_York. Base checkpoint:
PR #21 at `bd49451caa409fe9091f209048afe814fa9aa30b`.

Chris wants a proof, a counterexample, or an honest reason to move on. The
accepted target is to give the ZIP's norm-three projector and fixed generator
a concrete consumer in the existing conditional detector theorem, while
preserving the checked W00 core. Full operator-algebra classification and
minimum-norm formalization remain separate follow-ups.

Let `W = Q × Q`, `H = Q × W`, and use the existing Eisenstein multiplication
with eta² = eta − 1. Define `Fρ(h,w) = (27h, −27w)` for rho = 1+eta,
`G(w) = F_(2+eta)(w)`, and the whole-space auxiliary action
`Fμ(h,w) = (343h, G(w))`. Define `P = (27 I − Fρ)/54` as a rational linear map.

For every rational submodule A of H containing the entire known line and
preserved by Fρ and Fμ, prove:

`A = top ↔ ∃ c ∈ A, P c ≠ 0`.

The proof must actually instantiate `Bridge.conditionalWeilDetector_iff`.
Required supporting results: P's coordinate/spectral formula and idempotence;
nonzero/pure image; cyclic spanning by the fixed generator using the core's
checked determinant and reconstruction; preservation of P and G from the
stated action hypotheses. Include exact counterexamples to dropping generator
stability and to extending the projector to the wrong ambient action.

Success means the exact typed theorem and its controls compile, all named
declarations have permitted dependency receipts, bundled leanchecker accepts
the actual module, and affected integration checks pass. A proof-script failure
is not a mathematical counterexample. No claim of an actual algebraic cycle is
included: applying this finite model to geometry still requires the source's
component, correspondence and algebraicity hypotheses.

Routes: construct the maps and specialize the inherited theorem; independently
check the critical cyclic implication through explicit Cramer reconstruction;
test hypothesis removal with a proper invariant subspace. Novelty assessment
compares the result with the inherited theorem, original source conventions,
and classical involution projections/quadratic-field actions. It does not infer
global novelty from a failed search.

Original checkout and ZIP remain intact. Implementation and evidence belong
to this branch; historical checks remain source records. No manuscript adoption
or merge is authorized by this implementation task.
