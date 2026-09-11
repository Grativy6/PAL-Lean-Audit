import PAL.PrimeShellsConditionNumber

/-!
# Prime-shell condition-number dependency receipts

These commands expose the dependency sets of the Euclidean frame-row and
condition-number statements. They certify only the exact Lean declarations in
the pinned environment.
-/

#print axioms PAL.PrimeShells.conjugate_frame_rows_orthogonal
#print axioms PAL.PrimeShells.symmetric_row_energy
#print axioms PAL.PrimeShells.antisymmetric_row_energy
#print axioms PAL.PrimeShells.horizontalFrameEnergy_pos
#print axioms PAL.PrimeShells.verticalFrameEnergy_pos
#print axioms PAL.PrimeShells.frameConditionNumberSq_le_of_conditionBound
#print axioms PAL.PrimeShells.exists_frameConditionNumberSq_le_three
#print axioms PAL.PrimeShells.ramified_frameConditionNumberSq
#print axioms PAL.PrimeShells.ramified_ready_frameConditionNumberSq
#print axioms PAL.PrimeShells.frameConditionNumberSq_three_is_sharp
#print axioms PAL.PrimeShells.prime_shell_has_conditionNumberSq_le_three
