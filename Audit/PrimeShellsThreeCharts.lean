import PAL.PrimeShellsThreeCharts

/-!
# Framed Prime Shells v0.2 three-chart dependency receipts

These commands expose the logical dependencies of the derived-axis,
independent-axis, stereographic-sphere, and shell-atlas declarations. They
certify only the exact Lean statements in the pinned environment. They do not
establish radio-frequency measurements, prime-shell physics, novelty, or
publication authority.
-/

#print axioms PAL.PrimeShells.derivedAxis_sameFiber
#print axioms PAL.PrimeShells.jointAxis_sameFiber
#print axioms PAL.PrimeShells.jointAxis_refines_left
#print axioms PAL.PrimeShells.derivedAxis_refinement_equiv
#print axioms PAL.PrimeShells.jointAxis_strictly_refines_of_witness
#print axioms PAL.PrimeShells.jointAxis_eq_derived
#print axioms PAL.PrimeShells.Point3.extensionality
#print axioms PAL.PrimeShells.smithDen_pos
#print axioms PAL.PrimeShells.normSq3_smithSphere
#print axioms PAL.PrimeShells.smithSphereBack_smithSphere
#print axioms PAL.PrimeShells.smithSphere_injective
#print axioms PAL.PrimeShells.smithSphere_sameFiber
#print axioms PAL.PrimeShells.normSq3_scale3
#print axioms PAL.PrimeShells.smithAtlasPoint_sameFiber
#print axioms PAL.PrimeShells.radialSmithShell_normSq
