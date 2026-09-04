import PAL.PrimeShellsBasisTransport

/-!
# Exact conjugate-frame condition number

The associated Euclidean frame has columns

`(X, √3 Y)/2` and `(X, -√3 Y)/2`.

Its symmetric and antisymmetric row energies are proportional to `X²` and
`3Y²`.  This file defines their exact ratio as the squared frame condition
number, proves the universal bound `≤ 3` for the selected unit rotation, and
proves sharpness at the ramified norm-3 shell.
-/

namespace PAL.PrimeShells

noncomputable section

/-- The two Euclidean frame rows are orthogonal. -/
theorem conjugate_frame_rows_orthogonal (x : Point ℝ) :
    xCoord x * (Real.sqrt 3 * yCoord x) +
      xCoord x * (-(Real.sqrt 3 * yCoord x)) = 0 := by
  ring

/-- Energy of the symmetric row of the doubled Euclidean frame. -/
theorem symmetric_row_energy (x : Point ℝ) :
    xCoord x ^ 2 + xCoord x ^ 2 = 2 * horizontalFrameEnergy x := by
  simp [horizontalFrameEnergy]
  ring

/-- Energy of the antisymmetric row of the doubled Euclidean frame. -/
theorem antisymmetric_row_energy (x : Point ℝ) :
    (Real.sqrt 3 * yCoord x) ^ 2 +
      (-(Real.sqrt 3 * yCoord x)) ^ 2 =
        2 * verticalFrameEnergy x := by
  rw [neg_sq]
  rw [mul_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 3)]
  simp [verticalFrameEnergy]
  ring

/-- Squared spectral condition number after the exact symmetric/antisymmetric
row diagonalization.  Ready frames make the denominator positive. -/
def frameConditionNumberSq (x : Point ℝ) : ℝ :=
  max (horizontalFrameEnergy x) (verticalFrameEnergy x) /
    min (horizontalFrameEnergy x) (verticalFrameEnergy x)

/-- Horizontal energy is positive for a ready frame. -/
theorem horizontalFrameEnergy_pos {x : Point ℝ} (hx : FrameReady x) :
    0 < horizontalFrameEnergy x := by
  exact sq_pos_of_ne_zero hx.1

/-- Vertical energy is positive for a ready frame. -/
theorem verticalFrameEnergy_pos {x : Point ℝ} (hx : FrameReady x) :
    0 < verticalFrameEnergy x := by
  have hy : 0 < yCoord x ^ 2 := sq_pos_of_ne_zero hx.2
  dsimp [verticalFrameEnergy]
  nlinarith

/-- A division-free mutual energy bound controls the squared condition number. -/
theorem frameConditionNumberSq_le_of_conditionBound {C : ℝ} {x : Point ℝ}
    (hx : FrameReady x) (hBound : ConditionBoundSq C x) :
    frameConditionNumberSq x ≤ C := by
  unfold frameConditionNumberSq
  rcases le_total (horizontalFrameEnergy x) (verticalFrameEnergy x) with hHV | hVH
  · rw [max_eq_right hHV, min_eq_left hHV]
    exact (div_le_iff₀ (horizontalFrameEnergy_pos hx)).2 hBound.2
  · rw [max_eq_left hVH, min_eq_right hVH]
    exact (div_le_iff₀ (verticalFrameEnergy_pos hx)).2 hBound.1

/-- The selected unit rotation has squared Euclidean condition number at most three. -/
theorem exists_frameConditionNumberSq_le_three (x : Point ℝ)
    (hNorm : eNorm x ≠ 0) :
    ∃ k : FrameChoice,
      let y := choosePoint k x
      FrameReady y ∧ frameConditionNumberSq y ≤ 3 := by
  obtain ⟨k, hReady, -, hBound⟩ :=
    exists_sharply_conditioned_frame_choice x hNorm
  exact ⟨k, hReady, frameConditionNumberSq_le_of_conditionBound hReady hBound⟩

/-- The norm-3 reference frame attains squared condition number three. -/
theorem ramified_frameConditionNumberSq :
    frameConditionNumberSq ramifiedFramePoint = 3 := by
  norm_num [frameConditionNumberSq, horizontalFrameEnergy, verticalFrameEnergy,
    ramifiedFramePoint, xCoord, yCoord]

/-- Every ready unit-rotation choice at the ramified shell has squared condition
number exactly three; the remaining choice is singular. -/
theorem ramified_ready_frameConditionNumberSq (k : FrameChoice)
    (hk : FrameReady (choosePoint k ramifiedFramePoint)) :
    frameConditionNumberSq (choosePoint k ramifiedFramePoint) = 3 := by
  cases k with
  | base =>
      exact ramified_frameConditionNumberSq
  | turn =>
      exfalso
      norm_num [FrameReady, ramifiedFramePoint, choosePoint, rotate,
        xCoord, yCoord] at hk
  | turnTwice =>
      norm_num [frameConditionNumberSq, horizontalFrameEnergy, verticalFrameEnergy,
        ramifiedFramePoint, choosePoint, rotate, xCoord, yCoord]

/-- The universal squared condition-number bound `3` is sharp when the selector
is required to return a ready conjugate frame. -/
theorem frameConditionNumberSq_three_is_sharp :
    (∀ x : Point ℝ, eNorm x ≠ 0 →
      ∃ k : FrameChoice,
        let y := choosePoint k x
        FrameReady y ∧ frameConditionNumberSq y ≤ 3) ∧
    (∃ x : Point ℝ, eNorm x = 3 ∧
      ∀ C : ℝ, C < 3 →
        ∀ k : FrameChoice,
          FrameReady (choosePoint k x) →
            ¬ frameConditionNumberSq (choosePoint k x) ≤ C) := by
  constructor
  · exact exists_frameConditionNumberSq_le_three
  · refine ⟨ramifiedFramePoint, eNorm_ramifiedFramePoint, ?_⟩
    intro C hC k hk hle
    rw [ramified_ready_frameConditionNumberSq k hk] at hle
    linarith

/-- Prime-shell specialization, conditional on an exact supplied norm
representation. -/
theorem prime_shell_has_conditionNumberSq_le_three {p : ℕ} (hp : p.Prime)
    {a b : ℤ} (hShell : a ^ 2 + a * b + b ^ 2 = (p : ℤ)) :
    ∃ k : FrameChoice,
      let x : Point ℝ := ⟨a, b⟩
      let y := choosePoint k x
      FrameReady y ∧ frameConditionNumberSq y ≤ 3 := by
  let x : Point ℝ := ⟨a, b⟩
  have hNormEq : eNorm x = (p : ℝ) := by
    dsimp [x, eNorm]
    exact_mod_cast hShell
  have hNorm : eNorm x ≠ 0 := by
    rw [hNormEq]
    exact_mod_cast hp.ne_zero
  obtain ⟨k, hReady, hCondition⟩ :=
    exists_frameConditionNumberSq_le_three x hNorm
  exact ⟨k, hReady, hCondition⟩

end

end PAL.PrimeShells
