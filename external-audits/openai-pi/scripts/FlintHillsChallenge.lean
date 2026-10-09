import Mathlib

namespace OAI.PiExponent

-- Audit-authored target for the separate corollary, not a proposed proof.
theorem flint_hills_summable :
    Summable (fun n : ℕ =>
      1 / (((n + 1 : ℕ) : ℝ) ^ 3 * Real.sin (n + 1 : ℕ) ^ 2)) := by
  sorry

end OAI.PiExponent
