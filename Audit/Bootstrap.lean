import PAL

/-!
The bootstrap receipt deliberately prints the axiom dependencies of the smoke
theorem. Attack runs will add one `#print axioms` receipt per adopted theorem.
-/

#print axioms PAL.bootstrapCompiles
