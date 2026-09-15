# BRIDGE v0.4 finite-dimension review

Source lock: `BRIDGE_v0.4.docx`, SHA-256
`a13d91a728ab6da2a5654b3263a595242397d7fb8edb17cffafdcf32036a2470`.
This lane reads P0193-P0194 only:

> Thus the total generative defect has a hidden part H and a visible part V. In finite dimension,
> dimT=dimC+dimGv+dimH+dimV.

`Experiments.BridgeDimension` proves that equation for the already-audited
submodule and quotient definitions: `C = B ∩ K` through its two named subtype
presentations, `Gv = B/C`, `H = K/C`, and `V = T/(B ⊔ K)`. The proof uses
finite-dimensional rank-nullity and the dimension formula for a supremum and
intersection. It neither chooses complements nor identifies `H` with a
submodule of `D`.

The checked rational Finsupp countercase takes `T = ℚ × (ℕ →₀ ℚ)`,
`B = range(inl)`, and `K = ⊥`. It computes a four-sector finrank sum of one
while `finrank T` is zero under Lean's non-finite convention. It limits the
result to the source's explicit finite-dimensional hypothesis; it does not
refute the source equation under that hypothesis. P0195-P0199 remain for the
recovery lane.
