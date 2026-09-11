# Framed Prime Shells claim ledger

**Working title:** *Framed Prime Shells: Minimal Reference Data, Sharp Conditioning, and Composable Transport in the Eisenstein Lattice*  
**Reserved record:** `10.5281/zenodo.22288471`  
**Author / steward / adoption authority:** Christopher D. Pang  
**Branch:** `agent/prime-shells-conjugate-frames`  
**Status:** formal working package; draft PR; not merged, adopted, peer reviewed, or published

## Verification boundary

- Formal-source freeze: `56574e76c111204c8e33b468e48ea0e6af8ff4de`
- Complete receipt-gate commit: `2d830794ac34b38bf9a541293afecccaaf93486c`
- Lean: `4.32.1`
- Mathlib release: `v4.32.1`
- Mathlib manifest revision: `520045ab14e26149ee970e2e617ca04b09bde5d6`
- Dedicated workflow: `Prime Shells Lean`, run `33820043692`
- Result: `SUCCESS`
- Formal inventory: `62` unique publication-facing declarations in `5` required receipt files
- Allowed logical dependencies: `propext`, `Classical.choice`, `Quot.sound`
- Receipt artifact: ID `9917985202`
- Receipt artifact SHA-256: `a7aa5c917d59b6e0a1d7397aa2644b4b5d612ccef33f1af8bf5888ebb7365ce5`
- Repository proof-hole policy: passed for `21` Lean files

A green receipt establishes only the exact declarations under the pinned environment. It does not establish source adequacy, mathematical priority, author adoption, peer review, physical meaning, or the imported classical shell classification.

## Claim table

| ID | Claim | Current class | Evidence / declaration | Ceiling or residual |
|---|---|---|---|---|
| PS-01 | The coordinate operations for `eta^2 = eta - 1` give the displayed Eisenstein multiplication, conjugation, and sixty-degree unit rotation. | `LEAN_PROVED` | `mul`, `conj`, `rotate`, `conj_involutive`, `rotate_six` | Coordinate realization only; no new classification of algebraic integers. |
| PS-02 | `N(xy)=N(x)N(y)`, `N(conj x)=N(x)`, `N(Rx)=N(x)`, and `x*conj(x)=N(x)`. | `LEAN_PROVED` | `eNorm_mul`, `eNorm_conj`, `eNorm_rotate`, `mul_conj_eq_scalar_norm` | Exact in the declared coordinate ring. |
| PS-03 | `X^2+3Y^2=4N`; conjugation fixes `X`, reverses `Y`, and the conjugate-pair determinant is `-2XY` in scaled coordinates. | `LEAN_PROVED` | `scaled_norm_identity`, `scaledEmbed_conj`, `conjugate_frame_det` | The ordinary Euclidean `sqrt(3)/2` embedding is a declared coordinate interpretation. |
| PS-04 | The only point fixed by the sixty-degree unit rotation is the origin; no positive shell contains such a fixed point. | `LEAN_PROVED` | `rotate_fixed_iff_origin`, `no_positive_shell_rotation_fixed` | Local rotation statement only. |
| PS-05 | The norm form takes only residues `0` or `1 mod 3`; hence every integer shell at level `2 mod 3` is empty. | `LEAN_PROVED_KERNEL_REDUCED` | `norm_mod_three_kernel`, `no_integer_shell_of_mod_three_two_kernel`, `shell_seventeen_empty_kernel` | Ordinary `decide` proof; no native-decision dependency in the publication receipt surface. |
| PS-06 | For rational primes, `p=3` gives six points, `p=1 mod 3` gives twelve points in two conjugate unit orbits, and `p=2 mod 3` gives no points. | `CLASSICAL_IMPORTED` | Nair and Marmon; PAL v2.3-M source map | The present branch does not yet formalize arbitrary split-prime existence or the full orbit count end to end. |
| PS-07 | One reference vector cannot span the real plane. | `LEAN_PROVED` | `one_reference_is_insufficient` | Relative to a two-dimensional real carrier without an already supplied second direction. |
| PS-08 | A ready selected/conjugate pair reconstructs every planar vector. | `LEAN_PROVED` | `two_references_reconstruct` | Requires nonzero symmetric and antisymmetric coordinates. |
| PS-09 | The reconstruction coefficients are unique; equivalently, a ready conjugate pair is linearly independent. | `LEAN_PROVED` | `conjugate_references_independent`, `conjugate_reference_coefficients_unique` | Basis statement inside the declared carrier. |
| PS-10 | The three antipodally distinct unit choices have determinant coordinates `A0=b(2a+b)`, `A1=a^2-b^2`, and `A2=-a(a+2b)`. | `LEAN_PROVED` | `area_base`, `area_turn`, `area_turnTwice` | Exact coordinate identities. |
| PS-11 | `A0^2+A1^2+A2^2=2N^2`. | `LEAN_PROVED` | `three_area_square_sum` | Exact polynomial identity; priority not yet established. |
| PS-12 | The product of the three shortfalls equals the stated negative product of six squares. | `LEAN_PROVED` | `frame_gap_product` | Exact polynomial identity; priority not yet established. |
| PS-13 | One of the three antipodal unit choices satisfies `N^2 <= A_k^2`. | `LEAN_PROVED` | `exists_robust_frame_choice` | Existence only; no canonical tie-break rule is supplied. |
| PS-14 | At nonzero norm, a robust choice is a genuine two-reference frame. | `LEAN_PROVED` | `frameReady_of_robust`, `frameReady_iff_conjugate_det_ne_zero` | Readiness is algebraic nonparallelity, not physical stability. |
| PS-15 | The selected pair has squared normalized Euclidean area at least `3/4`, while every pair has value at most `1`. | `LEAN_PROVED` | `robust_strength_lower_bound`, `frameStrengthSq_le_one` | Exact normalized-area quantity in the declared Euclidean embedding. |
| PS-16 | The robust choice obeys `Y^2 <= X^2 <= 9Y^2`. | `LEAN_PROVED` | `robust_axis_balance` | Division-free coordinate balance. |
| PS-17 | Its conjugation-eigenmode energies `H=X^2` and `V=3Y^2` differ by at most a factor of `3`. | `LEAN_PROVED` | `robust_condition_bound_three`, `exists_sharply_conditioned_frame_choice` | Exact energy-ratio statement. |
| PS-18 | The Euclidean frame rows are orthogonal, with energies proportional to `X^2` and `3Y^2`. | `LEAN_PROVED` | `conjugate_frame_rows_orthogonal`, `symmetric_row_energy`, `antisymmetric_row_energy` | Exact row-level matrix interpretation. |
| PS-19 | The squared frame condition number, defined as `max(H,V)/min(H,V)`, is at most `3` for one of the three choices. | `LEAN_PROVED` | `frameConditionNumberSq_le_of_conditionBound`, `exists_frameConditionNumberSq_le_three` | For ready frames; equivalently `kappa_2 <= sqrt(3)` in the displayed Euclidean frame. |
| PS-20 | The constants `3/4` for squared normalized area and `3` for squared conditioning are sharp at the norm-`3` shell. | `LEAN_PROVED` | `ramified_strength_upper`, `strength_three_quarters_is_sharp`, `ramified_no_condition_bound_below_three`, `universal_condition_constant_three_is_sharp`, `ramified_frameConditionNumberSq`, `frameConditionNumberSq_three_is_sharp` | Sharp for the stated three-choice ready-frame selector, not every possible external framing convention. |
| PS-21 | A supplied exact prime representation inherits the robust area and condition-number bounds. | `LEAN_PROVED_CONDITIONAL` | `prime_shell_has_robust_conjugate_frame`, `prime_shell_has_sharply_conditioned_frame`, `prime_shell_has_conditionNumberSq_le_three` | Consumes `p=a^2+ab+b^2`; it does not find or prove that representation for every split prime. |
| PS-22 | The declared diagonal transport maps selected and reflected source references to their target counterparts. | `LEAN_PROVED` | `transport_selected`, `transport_reflected` | Ready source frame required. |
| PS-23 | Transport preserves arbitrary real linear combinations. | `LEAN_PROVED` | `transport_combine`, `transport_preservesCombinations` | Linear carrier only. |
| PS-24 | The two reference images uniquely characterize the transport map. | `LEAN_PROVED` | `transport_unique` | Uniqueness among maps satisfying the declared combination-preservation contract. |
| PS-25 | Transport obeys exact identity, inverse, and composition laws. | `LEAN_PROVED` | `transport_self`, `transport_inverse`, `transport_compose` | Coordinate groupoid/cocycle law; no physical trajectory or causal transport follows. |
| PS-26 | The integrated sharp selector and transport package is globally novel. | `OPEN_PRIORITY_REVIEW` | Targeted search found neighboring shell, angle, lattice-reduction, and frame literature, but not the exact package | Requires systematic database searching, citation chaining, and expert review. |
| PS-27 | The construction advances RH, a prime-gap bound, or a physical theory. | `EXCLUDED` | No supporting bridge | Must remain outside theorem claims. |

## Formal files

The publication-facing theorem surface is:

```text
PAL/PrimeShells.lean
PAL/PrimeShellsModThreeKernel.lean
PAL/PrimeShellsConditioning.lean
PAL/PrimeShellsBasisTransport.lean
PAL/PrimeShellsConditionNumber.lean
```

The corresponding dependency receipts are:

```text
Audit/PrimeShells.lean
Audit/PrimeShellsModThreeKernel.lean
Audit/PrimeShellsConditioning.lean
Audit/PrimeShellsBasisTransport.lean
Audit/PrimeShellsConditionNumber.lean
```

## Remaining publication burdens

1. Christopher's intuitive geometry and figures.
2. Systematic literature and priority review.
3. Independent mathematical review.
4. Final manuscript editing, citations, and release manifest.
5. Optional later Lean reconstruction of the complete classical split-prime representation and shell-count theorem.

The draft PR remains open and unmerged so none of these statuses are silently promoted.
