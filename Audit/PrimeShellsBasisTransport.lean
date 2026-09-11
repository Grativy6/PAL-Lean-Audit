import PAL.PrimeShellsBasisTransport

/-!
# Prime-shell basis and transport dependency receipts

These commands expose the dependency sets of the uniqueness and sharpness
claims. They certify only the exact Lean declarations in the pinned
environment; they do not formalize the classical split-prime shell-count
input, establish priority, amend PAL, or authorize publication.
-/

#print axioms PAL.PrimeShells.conjugate_references_independent
#print axioms PAL.PrimeShells.conjugate_reference_coefficients_unique
#print axioms PAL.PrimeShells.transport_combine
#print axioms PAL.PrimeShells.transport_preservesCombinations
#print axioms PAL.PrimeShells.transport_unique
#print axioms PAL.PrimeShells.ramified_no_condition_bound_below_three
#print axioms PAL.PrimeShells.universal_condition_constant_three_is_sharp
