# C4 independent review

## Scope reviewed

Reviewed `Experiments/Pal24Feedback.lean`, its axiom module, C4 ledger, notes,
source excerpts, and the live Atlas SHA-256
`c053292376363edd6fc743f0f2e31e3bb3850edc78ade3a289bbb07e7e8452c5`.
No build was run in this review lane.

## Result: scoped pass

P0689 defines dependence through one admitted common input/action pair with
distinct retained outputs and unequal successors. C4's certificate and
`AdmittedVariation` use precisely that existential, with the explicitly chosen
equality being equality of full retained and successor records. P0687's
lineage field is carried in those records, and the ledger states that this is a
selected comparison semantics rather than source authentication or causal
evidence.

The certificate/predicate equivalence is a direct witness rearrangement, not a
restatement of an assumption. The y-independent predecessor theorem genuinely
rules out a certificate because any candidate successor pair is equal. The
restricted-admission fixture is meaningful: `boolEcho` is ambiently
nonconstant, yet its false-only admitted domain has no distinct admitted pair.
The full Boolean domain then gives a positive finite witness. This correctly
keeps admitted-domain dependence distinct from ambient nonconstancy.

The notes and manual dispositions retain the material limits from P0699 and
P0701--P0705: no causal intervention, reachable influence, stability, agency,
noise, stochasticity, threshold, or A4-transition claim. The lineage theorem
only proves field copying in the fixture.

## Inventory check

Static inspection found 15 Lean declarations, 15 ledger rows, and 15 ordered
axiom checks with no missing or extra names. No source defect found within this
reduced extensional scope. This review does not certify a final receipt,
reachability model, causal mechanism, or authority.
