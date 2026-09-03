# Prime Shells claim ledger

**Working title:** *Framed Prime Shells: Minimal Reference Data, Sharp Conditioning, and Composable Transport in the Eisenstein Lattice*  
**Reserved record:** `10.5281/zenodo.22288471`  
**Author / steward / adoption authority:** Christopher D. Pang  
**Branch status:** proposal under formal audit; not adopted, merged, or published

| ID | Claim | Current class | Evidence / source | Ceiling or open burden |
|---|---|---|---|---|
| PS-01 | The coordinate operations for `η² = η - 1` give the displayed Eisenstein multiplication, conjugation, and sixty-degree unit rotation. | `LEAN_PROVED` | `PAL.PrimeShells.mul`, `conj`, `rotate`; direct identities in `PAL/PrimeShells.lean` | Coordinate realization only; no new algebraic-number-theory classification. |
| PS-02 | `N(xy)=N(x)N(y)`, `N(conj x)=N(x)`, `N(Rx)=N(x)`, and `x·conj(x)=N(x)`. | `LEAN_PROVED` | `eNorm_mul`, `eNorm_conj`, `eNorm_rotate`, `mul_conj_eq_scalar_norm` | Exact in the declared coordinate ring. |
| PS-03 | `X²+3Y²=4N` and conjugation fixes `X` while reversing `Y`. | `LEAN_PROVED` | `scaled_norm_identity`, `scaledEmbed_conj`, `conjugate_frame_det` | Scaled-coordinate identity; the ordinary Euclidean `√3/2` normalization is manuscript algebra. |
| PS-04 | The norm form never takes residue `2 mod 3`; hence an integer shell at such a level is empty. | `LEAN_PROVED_WITH_FINITE_DECISION` | `norm_mod_three`, `no_integer_shell_of_mod_three_two`, `shell_seventeen_empty` | Current dependency receipt exposes `native_decide` certificates. Replacing these with kernel-reduced finite cases is a pre-release cleanup target. |
| PS-05 | For rational primes: `p=3` gives six points, `p≡1 mod 3` gives twelve points in two conjugate unit orbits, and `p≡2 mod 3` gives no points. | `CLASSICAL_IMPORTED` | Nair; Marmon; PAL v2.3-M source map | The present branch does not yet formalize the arbitrary split-prime existence/count theorem in Lean. |
| PS-06 | One reference vector cannot span the plane. | `LEAN_PROVED` | `one_reference_is_insufficient` | Relative to a two-dimensional real carrier without an imported orientation operator. |
| PS-07 | A ready selected/conjugate pair reconstructs every planar vector. | `LEAN_PROVED` | `two_references_reconstruct` | Requires nonzero symmetric and antisymmetric coordinates. |
| PS-08 | Those two coefficients are unique; equivalently, a ready conjugate pair is linearly independent. | `LEAN_PROVED_PENDING_LATEST_CI` | `conjugate_references_independent`, `conjugate_reference_coefficients_unique` | Do not promote until the branch-head workflow and dependency receipts pass. |
| PS-09 | The three determinant coordinates satisfy `A₀²+A₁²+A₂²=2N²`. | `LEAN_PROVED` | `three_area_square_sum` | Exact polynomial identity. |
| PS-10 | Their three shortfalls have the displayed negative square-product factorization. | `LEAN_PROVED` | `frame_gap_product` | Exact polynomial identity; no priority claim yet. |
| PS-11 | One of the three antipodally distinct unit choices satisfies `N²≤A_k²`. | `LEAN_PROVED` | `exists_robust_frame_choice` | Selector exists; no canonical tie-break is supplied. |
| PS-12 | The selected pair has squared normalized area at least `3/4`, with universal upper bound `1`. | `LEAN_PROVED` | `robust_strength_lower_bound`, `frameStrengthSq_le_one` | `frameStrengthSq` is the exact algebraic normalized-area quantity in the declared Euclidean interpretation. |
| PS-13 | The robust choice obeys `Y²≤X²≤9Y²`. | `LEAN_PROVED` | `robust_axis_balance` | Exact division-free coordinate bound. |
| PS-14 | The symmetric/antisymmetric axis energies differ by at most a factor of `3`. | `LEAN_PROVED` | `robust_condition_bound_three`, `exists_sharply_conditioned_frame_choice` | The identification with the standard matrix 2-norm condition number is exact manuscript algebra but awaits its own matrix-level Lean declaration. |
| PS-15 | The constants `3/4` and `3` are sharp at the norm-`3` shell. | `LEAN_PROVED_PENDING_LATEST_CI` | `strength_three_quarters_is_sharp`, `ramified_no_condition_bound_below_three`, `universal_condition_constant_three_is_sharp` | Sharp for the stated three-choice selector, not a claim about every alternative framing rule. |
| PS-16 | A supplied prime representation inherits the sharp frame selector. | `LEAN_PROVED` | `prime_shell_has_robust_conjugate_frame`, `prime_shell_has_sharply_conditioned_frame` | Conditional on the exact supplied representation `p=a²+ab+b²`; it does not produce that representation. |
| PS-17 | The declared diagonal transport sends selected and reflected source references to the corresponding target references. | `LEAN_PROVED` | `transport_selected`, `transport_reflected` | Ready source frame required. |
| PS-18 | Transport obeys identity, inverse, and composition. | `LEAN_PROVED` | `transport_self`, `transport_inverse`, `transport_compose` | Algebraic transport only; no physical path or temporal process. |
| PS-19 | Transport is the unique linear-combination-preserving map with the two declared reference images. | `LEAN_PROVED_PENDING_LATEST_CI` | `transport_combine`, `transport_preservesCombinations`, `transport_unique` | Do not promote until branch-head CI passes. The linearity contract is explicitly declared. |
| PS-20 | The displayed `2×2` Euclidean frame operator is diagonal in symmetric/antisymmetric coordinates. | `MANUSCRIPT_EXACT / LEAN_OPEN` | Direct matrix multiplication in manuscript skeleton | Add a matrix-level Lean module before release or label the interpretation separately. |
| PS-21 | The exact new theorem package is globally novel. | `OPEN_PRIORITY_REVIEW` | Initial search found nearby shell/angular and lattice literature but not this exact package | No priority claim until a systematic literature review and expert review. |
| PS-22 | The construction advances RH, prime-gap bounds, or a physical theory. | `EXCLUDED` | No supporting bridge | Must remain absent from theorem claims. |

## Formal receipt state

The dedicated `Prime Shells Lean` workflow has already passed for the coordinate, robust-selection, conditioning, and first transport modules at an earlier branch head. The newest basis-uniqueness, characterized-transport, and all-choice sharpness module remains `PENDING_LATEST_CI` until the exact current branch head reports success and its artifact is inspected.

A passing workflow proves only that the named Lean declarations compile under the pinned environment and that the repository policy accepts the checked source. It does not establish source adequacy, classical-prime classification, novelty, author adoption, peer review, or publication.
