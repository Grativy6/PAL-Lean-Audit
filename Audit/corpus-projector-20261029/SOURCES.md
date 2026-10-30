# Source correspondence and bounded novelty check

Checked 29 October 2026, America/New_York. Purpose: distinguish the explicit
W00 corollary from existing mechanisms and from unproved geometric existence.
This is not an exhaustive priority survey.

## Corpus and code identities

The four manuscript identities agree with W00's source lock in
[PR #21](../corpus-six-lines/SOURCE-LOCK.json): CHARTER v1.0, BRIDGE v0.4,
and the retained v0.5/v0.6 manuscripts. BRIDGE v0.4 was checked locally at
SHA-256 `a13d91a728ab6da2a5654b3263a595242397d7fb8edb17cffafdcf32036a2470`.
Selected passages were read through the supplied equation-preserving BRIDGE
reader: “Adjacent Weil Detector Theorem,” “One Cycle K Generation Equivalence,”
and the explicit m=1 projector. The original source remains controlling.

The source fixes eta²−eta+1=0; the generic Hodge target is the known polarization
line plus a two-dimensional rational Weil space. Its displayed adjacent
parameter is (m+1)+m eta with m≥1. At m=1 the source already uses mu=2+eta,
norm seven, horizontal action 343 and an irreducible quadratic action on W.
It also supplies a polynomial projector on this restricted target. The new
rho=1+eta instance simplifies the projector when the corresponding action is
admitted; that additional action is explicit in the new theorem's assumptions.

| Formal object | Source meaning | Application status |
| --- | --- | --- |
| `Target = Q × Q²` | A chosen rational coordinate model of known line plus Weil plane | Verified as the formal domain; identifying a geometric target remains conditional on the source decomposition/action data. |
| `rhoAction`, `muAction` | Norm cubed on the known line, sixth-power multiplication on the plane | The coordinate equalities are new Lean theorems. No algebraic correspondence is constructed by them. |
| Submodule A | A candidate rational subspace; geometric application uses algebraic classes | The main theorem assumes the entire known line and stability under both stated actions. |
| `projector` | `(27 I − Fρ)/54` | Formula, pure image, nonzero map, idempotence and inherited stability proved. |
| `generator_cyclic` | Every nonzero seed and its G-image span the plane | Explicit determinant and Cramer reconstruction from the unchanged W00 core. |
| `projector_generator_complete_iff` | Concrete instance of the existing detector/generator equivalence | Verified by direct invocation of `Bridge.conditionalWeilDetector_iff`. |

## Primary-source overlap

1. **Harvard Math 23a, Fall 2002, Homework 7, problem 4(b)–(d), page 2.**
   [University-hosted assignment](https://people.math.harvard.edu/archive/23a_fall_02/hw7.pdf).
   It states the equivalence between projections and involutions and the ±1
   eigenspace decomposition as exercises. It does not provide a written proof
   there. The translation is U=Fρ/27 and P=(I−U)/2. The rational instance is
   proved directly in this Lean file. Overlap: **known after translation of
   notation**; it is not evidence of a novel projection principle.

2. **J.S. Milne, Fields and Galois Theory, v5.10 (September 2022), §1,
   construction (1.25), pages 16–18.**
   [Author's notes](https://www.jmilne.org/math/CourseNotes/FT.pdf).
   The text proves that the quotient by a monic irreducible degree-m polynomial
   is a field with the power basis. For a quadratic field, a nonscalar element
   supplies a two-element basis; multiplication by any nonzero seed transports
   it to another basis. Our coefficient 360 makes the chosen action nonscalar.
   Overlap: **formal corollary not stated** for this particular parameter pair.
   The Lean proof uses the stronger concrete reconstruction already in W00.

3. **Eyal Markman, Secant sheaves and Weil classes on abelian varieties,
   arXiv:2509.23403v2, §4, final paragraph before §5.**
   [Pinned primary version](https://arxiv.org/html/2509.23403v2#S4).
   The argument uses a nonzero algebraic Weil class, the algebraic K-action and
   a Weil space of dimension one over K to conclude algebraicity of every class
   in that space. BRIDGE itself cites this mechanism. Overlap: **formal corollary
   not stated** for our norm-three projector and norm-seven action. This reading
   verifies the overlap, not the construction of the required seed in every
   geometric component.

4. **Eyal Markman, Cycles on abelian 2n-folds of Weil type from secant sheaves on
   abelian n-folds, arXiv:2502.03415v2, Theorem 1.5.1.**
   [Pinned primary version](https://arxiv.org/html/2502.03415v2#S1.SS5).
   The statement concerns algebraicity on polarized Weil-type sixfolds with
   discriminant −1 for imaginary quadratic fields. Its full proof was not
   audited here. Overlap with this coordinate result: **partial or adjacent
   result only**. It is not licensed as a theorem about an arbitrary component
   merely because both texts discuss Weil classes.

The inherited repository theorem itself is an exact, already formalized
detector/generator interface; the new proof instantiates it. Thus the explicit
finite-dimensional connection is established, while a global novelty claim is
not established. A useful new implementation can be a corollary of known
mathematics.

## Search scope and limits

Two approaches were used: inspect the existing code/source bibliography, and
search the proposed formulas/mechanisms under older terminology. Queries
included involution/projector formulas; quadratic-field multiplication and
cyclic vectors; Eisenstein/Weil/projector with coefficients 27 and 54; the
rho/mu parameter pair; and six-line detector language. Web searches were in
English, checked on 29 October 2026. Secondary mirrors and irrelevant hits were
used only for discovery, not as proof sources. A Durham notes link returned 404
and was not relied on. The strongest primary overlaps above were read directly.

This same-reader second strategy is not independent review. No comprehensive
MathSciNet, zbMATH or citation-network sweep was performed, and unsuccessful
coefficient searches do not establish priority. No external full text was
copied into the tracked repository. The specific pairing's broader priority
remains unclaimed; the checked contribution here is the explicit formal adapter.
