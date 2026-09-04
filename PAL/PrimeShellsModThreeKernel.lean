import PAL.PrimeShells

/-!
# Kernel-reduced modulo-three shell obstruction

`PAL.PrimeShells.norm_mod_three` was first discharged with `native_decide`,
which is an appropriate finite certificate but appears explicitly in Lean's
dependency receipt. This file supplies an equivalent kernel-reduced finite
proof using ordinary `decide`, together with downstream shell-exclusion
theorems. The manuscript should cite these declarations when it wants the
narrower logical dependency record.
-/

namespace PAL.PrimeShells

/-- Kernel-reduced proof that the Eisenstein norm assumes only residues zero
or one modulo three. -/
theorem norm_mod_three_kernel (a b : ZMod 3) :
    a ^ 2 + a * b + b ^ 2 = 0 ∨ a ^ 2 + a * b + b ^ 2 = 1 := by
  revert a b
  decide

/-- Kernel-reduced shell exclusion for levels congruent to two modulo three. -/
theorem no_integer_shell_of_mod_three_two_kernel {n : ℤ} (hn : (n : ZMod 3) = 2) :
    ¬ ∃ x : Point ℤ, eNorm x = n := by
  rintro ⟨x, hx⟩
  have hmod := norm_mod_three_kernel (x.a : ZMod 3) (x.b : ZMod 3)
  have hcast :
      ((eNorm x : ℤ) : ZMod 3) =
        (x.a : ZMod 3) ^ 2 + (x.a : ZMod 3) * (x.b : ZMod 3) + (x.b : ZMod 3) ^ 2 := by
    simp [eNorm]
  have htwo : ((eNorm x : ℤ) : ZMod 3) = 2 := by
    rw [hx]
    exact hn
  rw [hcast] at htwo
  rcases hmod with hzero | hone
  · rw [hzero] at htwo
    exact (by decide : (0 : ZMod 3) ≠ 2) htwo
  · rw [hone] at htwo
    exact (by decide : (1 : ZMod 3) ≠ 2) htwo

/-- Kernel-reduced proof that the norm-17 shell is empty. -/
theorem shell_seventeen_empty_kernel : ¬ ∃ x : Point ℤ, eNorm x = 17 := by
  apply no_integer_shell_of_mod_three_two_kernel
  decide

end PAL.PrimeShells
