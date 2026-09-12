# BRIDGE v0.4 visible readout review

This lane closes the prior FS-M03 opening in the declared linear realization.
For a supplied field `k`, modules `T` and `R`, a supplied submodule `B`, and a
supplied linear map `r : T →ₗ[k] R`, `generatedReadout B r` is defined as the
range of `r` restricted to `B`, with codomain `range r`.  Thus the target is
precisely `range(r) / r(B)` in a subtype encoding, not a quotient of ambient
`R`.

`rawReadoutToVisible B r` is the actual map `t ↦ [r(t)]`. Lean checks that it
is surjective and that its kernel is `B ⊔ ker r`. The first-isomorphism
construction therefore gives `T/(B ⊔ ker r) ≃ range(r)/r(B)`. Its action on a
representative is checked definitionally, and the descended residual map from
`T/B` is checked equal to this comparison composed with the existing
`defectToVisible B r.ker`.

The source basis is the supplied BRIDGE v0.4 DOCX with SHA-256
`a13d91a728ab6da2a5654b3263a595242397d7fb8edb17cffafdcf32036a2470` and the
preserved excerpts P0108-P0192. P0123-P0124 supplies the displayed comparison;
P0190-P0192 supplies the induced-by-quotient reading. This is a bounded Lean
realization, not source adoption, a complement choice, a finite-dimensional
account, a recovery claim, or a geometric/Hodge statement.

Two concrete rational countercases keep both terms in the kernel formula: with
`r = Prod.fst` and `B = ⊥`, `(0,1)` requires `ker r`; with `r = id` and
`B = ⊤`, `1` requires `B`.
