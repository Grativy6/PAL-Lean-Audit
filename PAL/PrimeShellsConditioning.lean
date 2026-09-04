import PAL.PrimeShells

/-!
# Sharp conditioning for conjugate-pair shell frames

This file strengthens the existence theorem in `PAL.PrimeShells` with an
exact axis-balance statement.  The two energy coordinates are the diagonal
entries of the conjugate-pair frame operator up to a common positive factor.
The predicate `ConditionBoundSq C x` is the division-free statement that the
larger axis energy is at most `C` times the smaller one.

For the three antipodally distinct unit rotations, one choice always satisfies
`ConditionBoundSq 3`; the constant is sharp at the ramified norm-3 shell.
In ordinary Euclidean matrix language this is the squared 2-norm condition
number bound `κ₂² ≤ 3`, hence `κ₂ ≤ √3`.
-/

namespace PAL.PrimeShells

noncomputable section

/-- Horizontal energy in the conjugation-symmetric coordinate. -/
def horizontalFrameEnergy (x : Point ℝ) : ℝ := xCoord x ^ 2

/-- Vertical energy in the conjugation-antisymmetric Euclidean coordinate. -/
def verticalFrameEnergy (x : Point ℝ) : ℝ := 3 * yCoord x ^ 2

/-- Division-free squared conditioning bound for the two frame axes. -/
def ConditionBoundSq (C : ℝ) (x : Point ℝ) : Prop :=
  horizontalFrameEnergy x ≤ C * verticalFrameEnergy x ∧
    verticalFrameEnergy x ≤ C * horizontalFrameEnergy x

/-- The determinant test is exactly the two-nonzero-axis test. -/
theorem frameReady_iff_conjugate_det_ne_zero (x : Point ℝ) :
    FrameReady x ↔ pairDet (scaledEmbed x) (scaledEmbed (conj x)) ≠ 0 := by
  rw [conjugate_frame_det]
  simp [FrameReady, areaCoordinate]

/-- The robust determinant inequality forces the exact squared-axis interval
`Y² ≤ X² ≤ 9Y²`. -/
theorem robust_axis_balance {x : Point ℝ}
    (hRobust : eNorm x ^ 2 ≤ areaCoordinate x ^ 2) :
    yCoord x ^ 2 ≤ xCoord x ^ 2 ∧
      xCoord x ^ 2 ≤ 9 * yCoord x ^ 2 := by
  have hscaled :
      xCoord x ^ 2 + 3 * yCoord x ^ 2 = 4 * eNorm x :=
    scaled_norm_identity x
  have hsquare :
      (xCoord x ^ 2 + 3 * yCoord x ^ 2) ^ 2 = 16 * eNorm x ^ 2 := by
    calc
      (xCoord x ^ 2 + 3 * yCoord x ^ 2) ^ 2 = (4 * eNorm x) ^ 2 :=
        congrArg (fun t : ℝ => t ^ 2) hscaled
      _ = 16 * eNorm x ^ 2 := by ring
  have hRobust' :
      eNorm x ^ 2 ≤ (xCoord x * yCoord x) ^ 2 := by
    simpa [areaCoordinate] using hRobust
  have hfactor :
      (xCoord x ^ 2 - yCoord x ^ 2) *
          (xCoord x ^ 2 - 9 * yCoord x ^ 2) ≤ 0 := by
    calc
      (xCoord x ^ 2 - yCoord x ^ 2) *
          (xCoord x ^ 2 - 9 * yCoord x ^ 2) =
          (xCoord x ^ 2 + 3 * yCoord x ^ 2) ^ 2 -
            16 * (xCoord x * yCoord x) ^ 2 := by ring
      _ = 16 * eNorm x ^ 2 - 16 * (xCoord x * yCoord x) ^ 2 := by
        rw [hsquare]
      _ ≤ 0 := by nlinarith
  constructor
  · by_contra h
    have hlt : xCoord x ^ 2 < yCoord x ^ 2 := lt_of_not_ge h
    have hy2 : 0 ≤ yCoord x ^ 2 := sq_nonneg (yCoord x)
    have hlt9 : xCoord x ^ 2 < 9 * yCoord x ^ 2 := by nlinarith
    have hpositive :
        0 < (xCoord x ^ 2 - yCoord x ^ 2) *
          (xCoord x ^ 2 - 9 * yCoord x ^ 2) :=
      mul_pos_of_neg_of_neg (sub_neg.mpr hlt) (sub_neg.mpr hlt9)
    linarith
  · by_contra h
    have hlt9 : 9 * yCoord x ^ 2 < xCoord x ^ 2 := lt_of_not_ge h
    have hy2 : 0 ≤ yCoord x ^ 2 := sq_nonneg (yCoord x)
    have hlt : yCoord x ^ 2 < xCoord x ^ 2 := by nlinarith
    have hpositive :
        0 < (xCoord x ^ 2 - yCoord x ^ 2) *
          (xCoord x ^ 2 - 9 * yCoord x ^ 2) :=
      mul_pos (sub_pos.mpr hlt) (sub_pos.mpr hlt9)
    linarith

/-- The selected conjugate frame has squared condition bound three. -/
theorem robust_condition_bound_three {x : Point ℝ}
    (hRobust : eNorm x ^ 2 ≤ areaCoordinate x ^ 2) :
    ConditionBoundSq 3 x := by
  obtain ⟨hlower, hupper⟩ := robust_axis_balance hRobust
  constructor
  · dsimp [horizontalFrameEnergy, verticalFrameEnergy]
    nlinarith
  · dsimp [horizontalFrameEnergy, verticalFrameEnergy]
    nlinarith

/-- Every nonzero point has a unit-rotated conjugate-pair frame with the sharp
area and conditioning bounds simultaneously. -/
theorem exists_sharply_conditioned_frame_choice (x : Point ℝ)
    (hNorm : eNorm x ≠ 0) :
    ∃ k : FrameChoice,
      let y := choosePoint k x
      FrameReady y ∧
        (3 : ℝ) / 4 ≤ frameStrengthSq y ∧
        ConditionBoundSq 3 y := by
  obtain ⟨k, hRobust⟩ := exists_robust_frame_choice x
  have hNormChoice : eNorm (choosePoint k x) ≠ 0 := by
    simpa using hNorm
  refine ⟨k, ?_⟩
  dsimp
  exact ⟨frameReady_of_robust hNormChoice (by simpa using hRobust),
    robust_strength_lower_bound hNormChoice (by simpa using hRobust),
    robust_condition_bound_three (by simpa using hRobust)⟩

/-- Ramified norm-3 point used to certify sharpness. -/
def ramifiedFramePoint : Point ℝ := ⟨1, 1⟩

@[simp] theorem eNorm_ramifiedFramePoint : eNorm ramifiedFramePoint = 3 := by
  norm_num [ramifiedFramePoint, eNorm]

/-- No unit choice beats squared normalized area `3/4` at the ramified point. -/
theorem ramified_strength_upper (k : FrameChoice) :
    frameStrengthSq (choosePoint k ramifiedFramePoint) ≤ (3 : ℝ) / 4 := by
  cases k <;>
    norm_num [ramifiedFramePoint, frameStrengthSq, choosePoint, rotate,
      areaCoordinate, xCoord, yCoord, eNorm]

/-- The squared normalized area bound is attained at the ramified point. -/
theorem ramified_strength_attained :
    frameStrengthSq ramifiedFramePoint = (3 : ℝ) / 4 := by
  norm_num [ramifiedFramePoint, frameStrengthSq, areaCoordinate, xCoord, yCoord, eNorm]

/-- The squared conditioning constant three is attained at the ramified point. -/
theorem ramified_condition_ratio_attained :
    horizontalFrameEnergy ramifiedFramePoint =
      3 * verticalFrameEnergy ramifiedFramePoint := by
  norm_num [ramifiedFramePoint, horizontalFrameEnergy, verticalFrameEnergy,
    xCoord, yCoord]

/-- The constant `3` in the division-free squared conditioning bound is sharp. -/
theorem condition_bound_three_is_sharp :
    ConditionBoundSq 3 ramifiedFramePoint ∧
      ∀ C : ℝ, C < 3 → ¬ ConditionBoundSq C ramifiedFramePoint := by
  constructor
  · norm_num [ConditionBoundSq, ramifiedFramePoint, horizontalFrameEnergy,
      verticalFrameEnergy, xCoord, yCoord]
  · intro C hC hBound
    have hfirst := hBound.1
    norm_num [horizontalFrameEnergy, verticalFrameEnergy, ramifiedFramePoint,
      xCoord, yCoord] at hfirst
    nlinarith

/-- The universal squared area lower bound `3/4` is sharp. -/
theorem strength_three_quarters_is_sharp :
    (∀ x : Point ℝ, eNorm x ≠ 0 →
      ∃ k : FrameChoice,
        (3 : ℝ) / 4 ≤ frameStrengthSq (choosePoint k x)) ∧
    (∃ x : Point ℝ, eNorm x = 3 ∧
      ∀ k : FrameChoice,
        frameStrengthSq (choosePoint k x) ≤ (3 : ℝ) / 4) := by
  constructor
  · intro x hNorm
    obtain ⟨k, hRobust⟩ := exists_robust_frame_choice x
    have hNormChoice : eNorm (choosePoint k x) ≠ 0 := by
      simpa using hNorm
    exact ⟨k, robust_strength_lower_bound hNormChoice (by simpa using hRobust)⟩
  · exact ⟨ramifiedFramePoint, eNorm_ramifiedFramePoint, ramified_strength_upper⟩

/-- Prime-shell specialization of the sharp frame theorem, conditional only on
an exact supplied norm representation of the prime. -/
theorem prime_shell_has_sharply_conditioned_frame {p : ℕ} (hp : p.Prime)
    {a b : ℤ} (hShell : a ^ 2 + a * b + b ^ 2 = (p : ℤ)) :
    ∃ k : FrameChoice,
      let x : Point ℝ := ⟨a, b⟩
      let y := choosePoint k x
      FrameReady y ∧
        (3 : ℝ) / 4 ≤ frameStrengthSq y ∧
        ConditionBoundSq 3 y := by
  let x : Point ℝ := ⟨a, b⟩
  have hNormEq : eNorm x = (p : ℝ) := by
    dsimp [x, eNorm]
    exact_mod_cast hShell
  have hNorm : eNorm x ≠ 0 := by
    rw [hNormEq]
    exact_mod_cast hp.ne_zero
  obtain ⟨k, hReady, hStrength, hCondition⟩ :=
    exists_sharply_conditioned_frame_choice x hNorm
  refine ⟨k, ?_⟩
  dsimp
  exact ⟨hReady, hStrength, hCondition⟩

end

end PAL.PrimeShells
