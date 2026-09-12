# BRIDGE v0.4 four-sector source review

Source identity is the supplied `BRIDGE_v0.4.docx`, SHA-256 `a13d91a728ab6da2a5654b3263a595242397d7fb8edb17cffafdcf32036a2470`. The reviewed scope is P0108-P0199 in the hash-locked TXT and OOXML artifacts. OOXML was consulted because the source displays a 3x3 diagram whose arrows are flattened in TXT.

The source defines the canonical sectors as `C = B∩K`, `Gv = B/(B∩K) ≅ rB`, `H = K/(B∩K)`, and `V = T/(B+K) ≅ rT/rB` (P0110-P0125), warns that they are subquotients rather than chosen complementary subspaces (P0126), and states exactness with the residual sequence `0→H→D→V→0` (P0190-P0192).

The Lean translation uses `K.comap B.subtype` and `B.comap K.subtype` for the two subtype-local presentations of `B∩K`. It audits the raw hidden map, its quotient lift, injectivity, the defect-to-visible quotient, surjectivity, the bottom residual exactness, generic top/middle/defect-column quotient exactness, the left-column exactness, and the right-column residual sequence obtained by exchanging `B` and `K`. It explicitly checks the upper-left inclusion square and lower-left quotient square. It also supplies the first-isomorphism realization of `Gv` as the range of the restricted readout.

`generatedVisibleEquivRange` is classified `CONSISTENT_REALIZATION`: Lean constructs and checks the selected first-isomorphism equivalence in this subtype/comap encoding, while the source-to-encoding translation and its presentation as the source sector identity remain bounded. The kernel calculation it depends on is separately classified as proved from declared rules.

The audit does not name or commute every vertical arrow or square of the displayed 3x3, and therefore does not claim a Lean formalization of the complete diagram. Its right-column map explicitly transports `T/(K⊔B)` to the source-ordered `T/(B⊔K)` along `sup_comm`. It does not formalize `V ≅ rT/rB`; frame morphisms (P0200+); decoder criteria; finite-dimensional accounting; Hodge geometry; or external source claims. These remain separate manual dispositions in the claim receipt.

`Audit/BridgeEndpoint.lean` already contains the v0.2 `fourSector_quotient_finrank` theorem. This lane does not repeat or relabel that dimension identity; it uses the newer v0.4 source identity and audits concrete maps and exactness instead.
