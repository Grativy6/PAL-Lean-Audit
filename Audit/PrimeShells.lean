import PAL.PrimeShells

/-!
# Framed Prime Shells formalization dependency receipts

These commands expose the dependency sets of the theorem-bearing declarations
for the proposed manuscript *Framed Prime Shells*.

The receipts certify only the exact Lean statements under the pinned
Lean/Mathlib environment. They do not formalize the complete classical
representation-count theorem, establish novelty, amend PAL, or authorize
publication/adoption.

The original fast finite-decision versions of the modulo-three lemmas remain in
`PAL.PrimeShells` as historical development trace. Publication-facing receipts
for that seam live in `Audit.PrimeShellsModThreeKernel` and use the separately
proved kernel-reduced declarations.
-/

#print axioms PAL.PrimeShells.conj_involutive
#print axioms PAL.PrimeShells.rotate_six
#print axioms PAL.PrimeShells.eNorm_conj
#print axioms PAL.PrimeShells.eNorm_rotate
#print axioms PAL.PrimeShells.eNorm_mul
#print axioms PAL.PrimeShells.mul_conj_eq_scalar_norm
#print axioms PAL.PrimeShells.scaled_norm_identity
#print axioms PAL.PrimeShells.scaledEmbed_conj
#print axioms PAL.PrimeShells.conjugate_frame_det
#print axioms PAL.PrimeShells.rotate_fixed_iff_origin
#print axioms PAL.PrimeShells.no_positive_shell_rotation_fixed
#print axioms PAL.PrimeShells.eNorm_choosePoint
#print axioms PAL.PrimeShells.area_base
#print axioms PAL.PrimeShells.area_turn
#print axioms PAL.PrimeShells.area_turnTwice
#print axioms PAL.PrimeShells.three_area_square_sum
#print axioms PAL.PrimeShells.frame_gap_product
#print axioms PAL.PrimeShells.exists_robust_frame_choice
#print axioms PAL.PrimeShells.frameReady_of_robust
#print axioms PAL.PrimeShells.area_upper_bound
#print axioms PAL.PrimeShells.robust_strength_lower_bound
#print axioms PAL.PrimeShells.frameStrengthSq_le_one
#print axioms PAL.PrimeShells.prime_shell_has_robust_conjugate_frame
#print axioms PAL.PrimeShells.one_reference_is_insufficient
#print axioms PAL.PrimeShells.two_references_reconstruct
#print axioms PAL.PrimeShells.transport_selected
#print axioms PAL.PrimeShells.transport_reflected
#print axioms PAL.PrimeShells.transport_self
#print axioms PAL.PrimeShells.transport_compose
#print axioms PAL.PrimeShells.transport_inverse
