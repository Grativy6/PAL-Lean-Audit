import Mathlib.Tactic.Ring
import Mathlib.Data.Int.Basic

/-!
# Bounded CHARTER coordinate-algebra follow-up

These declarations realize only the integer coordinate operations displayed in
CHARTER v1.0 Proposition 2.1.  They do not establish shell occupancy,
primality, frame quality, or any systems interpretation.
-/

namespace Experiments.CharterFollowup

/-- The source's `(1, η)` coordinate multiplication. -/
def coordMul (x y : ℤ × ℤ) : ℤ × ℤ :=
  (x.1 * y.1 - x.2 * y.2, x.1 * y.2 + x.2 * y.1 + x.2 * y.2)

/-- The source's arithmetic conjugation in coordinates. -/
def coordConj (x : ℤ × ℤ) : ℤ × ℤ := (x.1 + x.2, -x.2)

/-- Multiplication by the displayed sixty-degree unit. -/
def coordRotate (x : ℤ × ℤ) : ℤ × ℤ := (-x.2, x.1 + x.2)

/-- The displayed Eisenstein-coordinate norm. -/
def coordNorm (x : ℤ × ℤ) : ℤ := x.1 ^ 2 + x.1 * x.2 + x.2 ^ 2

/-- Proposition 2.1: coordinate norm is multiplicative for the declared product. -/
theorem coordNorm_mul (x y : ℤ × ℤ) :
    coordNorm (coordMul x y) = coordNorm x * coordNorm y := by
  rcases x with ⟨a, b⟩
  rcases y with ⟨c, d⟩
  simp [coordNorm, coordMul]
  ring

/-- Proposition 2.1: arithmetic conjugation preserves the coordinate norm. -/
theorem coordNorm_conj (x : ℤ × ℤ) :
    coordNorm (coordConj x) = coordNorm x := by
  rcases x with ⟨a, b⟩
  simp [coordNorm, coordConj]
  ring

/-- Proposition 2.1: the declared unit rotation preserves the coordinate norm. -/
theorem coordNorm_rotate (x : ℤ × ℤ) :
    coordNorm (coordRotate x) = coordNorm x := by
  rcases x with ⟨a, b⟩
  simp [coordNorm, coordRotate]
  ring

/-- The source's fixed-point calculation: full unit rotation fixes only the origin. -/
theorem coordRotate_fixed_iff (x : ℤ × ℤ) :
    coordRotate x = x ↔ x = (0, 0) := by
  rcases x with ⟨a, b⟩
  simp [coordRotate]
  constructor
  · rintro ⟨h₁, h₂⟩
    constructor <;> omega
  · rintro ⟨rfl, rfl⟩
    simp

end Experiments.CharterFollowup
