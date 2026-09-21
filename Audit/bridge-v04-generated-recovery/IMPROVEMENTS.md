# What these checks suggest improving

These are source-grounded proposals and audit-process corrections. They do not amend Christopher D. Pang's manuscript. The source already distinguishes arbitrary and linear answers, and already states the reachable-versus-total boundary in P0107. The recommendations below make that structure easier to see where P0195 uses it.

## 1. Spell out what “the answer varies” means

For the generated span, a useful expanded statement is:

> Let `q = r|B : B → R`. A requested answer `a : B → A` admits a unique decoder on `im q` exactly when `q(x) = q(y)` implies `a(x) = a(y)` for all `x,y ∈ B`. If `a` is linear, this is equivalent to `C ≤ ker a`, where `C = ker q` is a submodule of `B`.

This mirrors P0107 in the local statement. The quantification over every fiber matters: for `r(x,y)=x`, the nonlinear answer `a(x,y)=xy` vanishes on the zero fiber but differs at `(1,0)` and `(1,1)`. A condition checked only on `C` would miss that obstruction. The companion Lean countercase records this stronger reading precisely.

## 2. Name the recovered object and decoder domain

“Full identity” in P0195 means identity on `B = im e`. Recovering an exported value does not recover every possible original generator. For example, exporting `(x,y)` as `x` loses `y` even when the subsequent endpoint reads `x` perfectly. That distinction matters for applications which interpret an export as a complete account of its origin.

The reachable decoder, when it exists, is unique. A total extension to the ambient readout space need not be: the maps `(x,y) ↦ x` and `(x,y) ↦ x+y` agree on the reachable line `(x,0)` but differ away from it. Reserve “noncanonical” for representative selection or such extensions, rather than applying it to the unique reachable factorization. A classical existence proof is also separate from an executable reconstruction procedure.

## 3. Correct our previous coverage summary

The generated `Audit/bridge-v04-dimension-recovery/SUMMARY.md` says: “The generated-span answer criterion and checked countercases are described in the claim ledgers.” This overstates that batch's coverage. Its README and CLOSURE.json correctly say that P0195's direct generated-span clause remained `OPEN_MANUAL`; its recovery ledger formalizes residual-space recovery instead.

**Correction:** the preceding batch checked finite accounting and residual recovery. Direct generated-span factorization receives its own evidence in this batch. The historical summary, receipts, and source dispositions are preserved unchanged so the correction remains traceable.

Our process now gives the source clause an explicit correspondence table and a separate current disposition. The generated summary derives declaration and classification counts from the checked inventory and reports one selected source clause, not a discovery count. Equivalent formulations, helper definitions, examples, and receipt guards remain separate from manuscript coverage.

## 4. Keep source addresses reproducible

During this review, an initial source-reading return used a different paragraph count and incorrectly pointed the arbitrary-answer statement at P0069–P0071. Comparison with the original OOXML rejected that address: the correct span is P0105–P0107, and the committed context contains P0107. The corrected review is the adopted evidence.

Use the existing canonical `w:p` enumeration, including empty and table paragraphs, for every source address. The runner checks literal excerpts against preserved text and reconstructs that text from the original OOXML. Local source verification also compares the snapshots with the supplied DOCX. CI checks the committed snapshots; it does not claim to reread the absent original document.

## 5. Inspect elaborated assumptions, not just the proof text

The first implementation compiled and passed the kernel check, but its printed signatures exposed an unintended restriction: the supposedly arbitrary answer type still carried additive-group and module instances from the surrounding Lean section. The initial source review and proof-text review had both missed this. Those receipts establish the narrower statements only; the attempt is preserved with a `SUPERSEDED.json` annotation and its original module snapshot.

The corrected function theorems bind a fresh arbitrary answer type independently of the linear-answer context. The final axiom log prints their elaborated signatures, and a type-checking example applies the theorem to an entirely unstructured answer type. Keep this check when moving a general claim into a file that also contains stronger structured variants. A successful compilation alone cannot tell us whether we accidentally proved a narrower translation.

## Next independent seams

Frame-morphism transport should test which commuting-map conditions actually preserve a certificate. Return dynamics should distinguish a chosen representative from recovery of the whole original. Both remain separate source-bound audit batches; no result here settles geometric or Hodge applications.
