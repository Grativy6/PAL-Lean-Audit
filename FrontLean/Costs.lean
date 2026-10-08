import Mathlib

namespace FrontLean

/-- Proposition 7: all quantities use a common unit; this is algebra, not a speed measurement. -/
theorem reuse_cheaper_iff (D B R : ℝ) (m : ℕ) :
    D + B + ((m : ℝ) - 1) * R < (m : ℝ) * D ↔
      ((m : ℝ) - 1) * (D - R) > B := by
  constructor <;> intro h <;> nlinarith

theorem no_saving_when_reuse_is_costlier (D B R : ℝ) (m : ℕ)
    (hm : 1 ≤ m) (hB : 0 ≤ B) (hDR : D ≤ R) :
    (m : ℝ) * D ≤ D + B + ((m : ℝ) - 1) * R := by
  have hm' : (1 : ℝ) ≤ m := by exact_mod_cast hm
  nlinarith [mul_nonneg (sub_nonneg.mpr hm') (sub_nonneg.mpr hDR)]

/-- The finite nonterminal step bound used in Proposition 8. -/
theorem descending_rank_bounds_steps (rank : ℕ → ℕ) (k : ℕ)
    (desc : ∀ i, i < k → rank (i + 1) < rank i) : k ≤ rank 0 := by
  have aux : ∀ i, i ≤ k → rank i + i ≤ rank 0 := by
    intro i
    induction i with
    | zero => intro _; omega
    | succ i ih =>
      intro hi
      have hp := ih (by omega)
      have hd := desc i (by omega)
      omega
  have h := aux k le_rfl
  omega

/-- Equation 24's explicit accounting, including one terminal step.
    Sound SAT decisions, uniform construction and polynomial hypotheses remain supplied.
    No formal P=NP conclusion is asserted by this numerical lemma. -/
theorem total_cost_bound (rank : ℕ → ℕ) (k initial p₀ p₁ p₂ : ℕ)
    (cost : Fin (k + 1) → ℕ)
    (desc : ∀ i, i < k → rank (i + 1) < rank i)
    (hr : rank 0 ≤ p₁) (hi : initial ≤ p₀)
    (hc : ∀ i, cost i ≤ p₂) :
    initial + ∑ i, cost i ≤ p₀ + (p₁ + 1) * p₂ := by
  have hk := (descending_rank_bounds_steps rank k desc).trans hr
  have hs : (∑ i, cost i) ≤ (k + 1) * p₂ := by
    calc
      (∑ i, cost i) ≤ ∑ _ : Fin (k + 1), p₂ := Finset.sum_le_sum (fun i _ => hc i)
      _ = (k + 1) * p₂ := by simp
  exact Nat.add_le_add hi (hs.trans (Nat.mul_le_mul_right p₂ (by omega)))

/-- Explicit bound for supplied polynomial cost functions, not a constructed SAT decider. -/
theorem polynomial_accounting (p₀ p₁ p₂ : Polynomial ℕ) (n k initial : ℕ)
    (rank : ℕ → ℕ) (cost : Fin (k + 1) → ℕ)
    (desc : ∀ i, i < k → rank (i + 1) < rank i)
    (hr : rank 0 ≤ p₁.eval n) (hi : initial ≤ p₀.eval n)
    (hc : ∀ i, cost i ≤ p₂.eval n) :
    initial + ∑ i, cost i ≤ (p₀ + (p₁ + 1) * p₂).eval n := by
  simpa using total_cost_bound rank k initial (p₀.eval n) (p₁.eval n) (p₂.eval n)
    cost desc hr hi hc

/-- The paper's stipulated shared-acquisition diamond: 15 actual units, 27 if repeated in accounting. -/
theorem shared_diamond_cost :
    (12 + 1 + 1 + 1 : ℕ) = 15 ∧ (12 + 1 + (12 + 1) + 1 : ℕ) = 27 := by
  norm_num

end FrontLean
