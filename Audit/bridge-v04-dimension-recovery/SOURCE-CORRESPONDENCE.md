# Source correspondence

Source: the exact supplied BRIDGE_v0.4.docx, 74384 bytes, SHA256 a13d91a728ab6da2a5654b3263a595242397d7fb8edb17cffafdcf32036a2470. Identity is local-source identity; no independently verified published v0.4 identity is asserted. Original OOXML from the same document is retained in the prior source-excerpts.json (P0108-P0199) and source-context.json (P0036, P0087, P0107). Paragraph numbers are original document paragraph positions, including empty paragraphs. New targets are P0193-P0199; the rest is definition and assumption context.

| Source | Exact mathematical target | Translation obligation |
|---|---|---|
| P0036, P0087, P0107 | Vector spaces over a field; B = im e, K = ker r | Generic supplied B can represent im e by taking e = B.subtype. Readout-specific statements use K = r.ker. |
| P0115-P0124 | C = B intersection K, Gv = B/C, H = K/C, V = T/(B+K) | C is represented as K.comap B.subtype inside B; the quotient in K uses B.comap K.subtype. The two presentations share the same ambient intersection but their types remain distinct. |
| P0193-P0194 | dim T = dim C + dim Gv + dim H + dim V | Natural-number finrank is used only with finite-dimensional hypotheses in the positive accounting theorem. This identity does not choose complements or splittings. |
| P0195, generated-span clause | Generated trace has collision C; a coarser answer is obstructed only where it varies on collisions | OPEN_MANUAL: direct answer factorization through r restricted to B is not a new theorem in this batch. The residual criterion below uses a different domain. |
| P0196-P0198 | A requested linear answer a on D = T/B is endpoint-decodable iff H is contained in ker a | H is not literally a submodule of D: the condition is range(hiddenToDefect B (ker r)) <= ker a. The decoder factors a through residualReadout into range(r)/r(B). |
| P0199 | Full residual identity is recoverable iff H = 0 iff K <= B | H = 0 means the quotient type is subsingleton, equivalently its embedded image is bottom. Recovery is a left inverse for the residual readout, not a section selecting representatives in T. |

The canonical visible-readout equivalence and its representative action are imported from the preceding audit, not assumed from a matching target name. Source-to-Lean correspondence is a recorded manual review; compilation checks the chosen typed statements. This batch cannot establish all applications of BRIDGE, novelty, source adoption, or the truth of external geometric hypotheses.
