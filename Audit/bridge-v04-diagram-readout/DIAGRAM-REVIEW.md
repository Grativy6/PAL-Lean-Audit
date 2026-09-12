# BRIDGE v0.4 diagram review

This lane audits the displayed 3x3 in BRIDGE v0.4, source SHA-256
`a13d91a728ab6da2a5654b3263a595242397d7fb8edb17cffafdcf32036a2470`, through
the preserved OOXML excerpts P0108-P0192. It formalizes supplied submodules
`B` and `K` of a module `T` over a field. It does not adopt the manuscript,
choose complements, assume finite dimension, or formalize the readout-range
comparison.

`Experiments.BridgeDiagram.complete_diagram_certified` packages exactly six
short-exact local sequences and four source-ordered squares:

| Rows | Columns | Squares |
| --- | --- | --- |
| `C → B → Gv` | `C → K → H` | upper-left inclusion |
| `K → T → T/K` | `B → T → D` | lower-left quotient |
| `H → D → V` | `Gv → T/K → V` | upper-right quotient; lower-right transported quotient |

The right column is stated using the actual displayed map
`generatedVisibleToKernelQuotient`; Lean unfolds it to the previously checked
swapped residual construction. The latter retains the explicit `sup_comm`
transport already present in `BridgeFourSector`.

Every new theorem has a matching `#print axioms` directive in
`Experiments/BridgeDiagramAxioms.lean`. The direct check reports only
`propext`, `Classical.choice`, and `Quot.sound` for the new declarations. The
checked rational zero-map fixture proves that a commuting square by itself
does not imply exactness, so the aggregate certificate retains endpoint and
exactness evidence for every sequence.

The separate readout lane remains responsible for `V = T/(B+ker r)` versus
`range(r)/r(B)` and its representative map. FS-M04 remains open: this lane
does not make dimension, recovery, Hodge, Weil, frame-morphism, or PAL claims.
