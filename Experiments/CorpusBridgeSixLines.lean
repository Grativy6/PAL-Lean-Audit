import Mathlib.Tactic

/-!
# W00-T1: the six-line arithmetic bridge

Source: Christopher D. Pang, CHARTER v1.0, sections 2, 5, 7.2;
BRIDGE v0.4, Adjacent Weil Detector / One Cycle K Generation;
BRIDGE v0.6 section 12 retains that geometric source by reference.
Claude's 2026-10-28 cross-corpus report proposes the general-parameter link.

This module proves coordinate arithmetic and rational-plane statements.
It does not construct an abelian variety, an algebraic cycle, or a Hodge class.
The second-operator result separates same-operator cyclicity from recovery
using another admitted algebraic action. See the source correspondence note.
-/

namespace Experiments.CorpusBridgeSixLines

section Arithmetic
variable {R : Type*} [CommRing R]

/-- Multiplication in the basis (1, eta), eta^2 = eta - 1. -/
def emul (x y : R × R) : R × R :=
  (x.1 * y.1 - x.2 * y.2, x.1 * y.2 + x.2 * y.1 + x.2 * y.2)

def enorm (x : R × R) : R := x.1 ^ 2 + x.1 * x.2 + x.2 ^ 2

def cube (x : R × R) : R × R := emul (emul x x) x

def sixth (x : R × R) : R × R := emul (cube x) (cube x)

/-- Imaginary-coordinate factor of the cube. -/
def bFactor (a b : R) : R := 3 * a * b * (a + b)

/-- Twice the real part of the cube in the specified complex embedding. -/
def tFactor (a b : R) : R := (a - b) * (2 * a + b) * (a + 2 * b)

def det2 (x y : R × R) : R := x.1 * y.2 - x.2 * y.1

/-- Multiplication coefficient for F_lambda - N(lambda)^3 I. -/
def remainder (x : R × R) : R × R :=
  ((sixth x).1 - (enorm x) ^ 3, (sixth x).2)

theorem cube_coordinates (a b : R) :
    cube (a, b) = (a ^ 3 - 3 * a * b ^ 2 - b ^ 3, bFactor a b) := by
  apply Prod.ext <;> dsimp [cube, emul, bFactor] <;> ring

theorem cube_twice_real (a b : R) :
    2 * (cube (a, b)).1 + (cube (a, b)).2 = tFactor a b := by
  dsimp [cube, emul, tFactor]
  ring

theorem cube_norm_identity (a b : R) :
    (tFactor a b) ^ 2 + 3 * (bFactor a b) ^ 2 = 4 * (enorm (a, b)) ^ 3 := by
  dsimp [tFactor, bFactor, enorm]
  ring

theorem sixth_eta_factorization (a b : R) :
    (sixth (a, b)).2 = bFactor a b * tFactor a b := by
  dsimp [sixth, cube, emul, bFactor, tFactor]
  ring

/-- Exact connection to the three CHARTER determinant coordinates. -/
theorem sixth_charter_product (a b : R) :
    (sixth (a, b)).2 =
      -3 * (b * (2 * a + b)) * (a ^ 2 - b ^ 2) * (-a * (a + 2 * b)) := by
  dsimp [sixth, cube, emul]
  ring

theorem sixth_real_shift (a b : R) :
    2 * (sixth (a, b)).1 + (sixth (a, b)).2 - 2 * (enorm (a, b)) ^ 3 =
      -3 * (bFactor a b) ^ 2 := by
  dsimp [sixth, cube, emul, enorm, bFactor]
  ring

theorem norm_mul (x y : R × R) :
    enorm (emul x y) = enorm x * enorm y := by
  dsimp [enorm, emul]
  ring

theorem multiplication_determinant (x : R × R) :
    det2 (emul x (1, 0)) (emul x (0, 1)) = enorm x := by
  dsimp [det2, emul, enorm]
  ring

/-- The determinant of the two-dimensional detector, not a cycle-existence claim. -/
theorem detector_norm (a b : R) :
    enorm (remainder (a, b)) = 3 * (enorm (a, b)) ^ 3 * (bFactor a b) ^ 2 := by
  dsimp [enorm, remainder, sixth, cube, emul, bFactor]
  ring

theorem cyclic_determinant (a b : R) (w : R × R) :
    det2 w (emul (sixth (a, b)) w) = bFactor a b * tFactor a b * enorm w := by
  dsimp [det2, sixth, cube, emul, bFactor, tFactor, enorm]
  ring

/-- A fixed auxiliary action has nonreal sixth power (-323 + 360 eta). -/
theorem fixed_auxiliary_coordinates :
    sixth ((2 : R), 1) = (-323, 360) := by
  apply Prod.ext <;> dsimp [sixth, cube, emul] <;> ring

theorem auxiliary_determinant (w : R × R) :
    det2 w (emul (sixth ((2 : R), 1)) w) = 360 * enorm w := by
  dsimp [det2, sixth, cube, emul, enorm]
  ring

/-- An explicit two-operator determinant; works even on the detecting scalar lines. -/
theorem repaired_determinant (a b : R) (w : R × R) :
    det2 (emul (remainder (a, b)) w)
      (emul (sixth ((2 : R), 1)) (emul (remainder (a, b)) w)) =
        1080 * (enorm (a, b)) ^ 3 * (bFactor a b) ^ 2 * enorm w := by
  rw [auxiliary_determinant, norm_mul, detector_norm]
  ring

end Arithmetic

/-- CHARTER's six lines, including the origin. -/
theorem integer_six_lines (a b : ℤ) :
    (sixth (a, b)).2 = 0 ↔
      a = 0 ∨ b = 0 ∨ a + b = 0 ∨ a - b = 0 ∨ 2 * a + b = 0 ∨ a + 2 * b = 0 := by
  simp [sixth_eta_factorization, bFactor, tFactor, mul_eq_zero, or_assoc]

section RationalPlane

/-- Positivity is specific to the rational/real Eisenstein norm, not an arbitrary field. -/
theorem rational_norm_nonneg (w : ℚ × ℚ) : 0 ≤ enorm w := by
  dsimp [enorm]
  nlinarith [sq_nonneg (2 * w.1 + w.2), sq_nonneg w.2]

theorem rational_norm_zero_iff (w : ℚ × ℚ) : enorm w = 0 ↔ w = (0, 0) := by
  constructor
  · intro h
    have hs : w.2 ^ 2 = 0 := by
      dsimp [enorm] at h
      nlinarith [sq_nonneg (2 * w.1 + w.2), sq_nonneg w.2]
    have hb : w.2 = 0 := (sq_eq_zero_iff).mp hs
    have hs' : w.1 ^ 2 = 0 := by simpa [enorm, hb] using h
    have ha : w.1 = 0 := (sq_eq_zero_iff).mp hs'
    exact Prod.ext ha hb
  · rintro rfl
    norm_num [enorm]

theorem detector_nonzero_iff (a b : ℚ) :
    enorm (remainder (a, b)) ≠ 0 ↔ bFactor a b ≠ 0 := by
  rw [detector_norm]
  constructor
  · intro h hz
    simp [hz] at h
  · intro h
    have hq : enorm (a, b) ≠ 0 := by
      intro hz
      have hp := (rational_norm_zero_iff (a, b)).mp hz
      have ha : a = 0 := congrArg Prod.fst hp
      exact h (by simp [bFactor, ha])
    exact mul_ne_zero (mul_ne_zero (by norm_num) (pow_ne_zero _ hq)) (pow_ne_zero _ h)

theorem same_operator_cyclic_iff (a b : ℚ) (w : ℚ × ℚ) (hw : w ≠ (0, 0)) :
    det2 w (emul (sixth (a, b)) w) ≠ 0 ↔ bFactor a b ≠ 0 ∧ tFactor a b ≠ 0 := by
  have hn : enorm w ≠ 0 := fun h => hw ((rational_norm_zero_iff w).mp h)
  rw [cyclic_determinant]
  simp [mul_ne_zero_iff, hn]

/-- Explicit independent pair using the detector plus the fixed norm-seven action. -/
theorem repaired_pair_nonzero (a b : ℚ) (w : ℚ × ℚ)
    (hb : bFactor a b ≠ 0) (hw : w ≠ (0, 0)) :
    det2 (emul (remainder (a, b)) w)
      (emul (sixth ((2 : ℚ), 1)) (emul (remainder (a, b)) w)) ≠ 0 := by
  rw [auxiliary_determinant, norm_mul]
  have hr : enorm (remainder (a, b)) ≠ 0 := (detector_nonzero_iff a b).mpr hb
  have hn : enorm w ≠ 0 := fun h => hw ((rational_norm_zero_iff w).mp h)
  exact mul_ne_zero (by norm_num) (mul_ne_zero hr hn)

/-- Cramer's rule supplies the actual reconstruction from any determinant-certified pair. -/
def combine (r : ℚ) (x : ℚ × ℚ) (s : ℚ) (y : ℚ × ℚ) : ℚ × ℚ :=
  (r * x.1 + s * y.1, r * x.2 + s * y.2)

theorem reconstruct_from_pair (x y t : ℚ × ℚ) (hd : det2 x y ≠ 0) :
    combine (det2 t y / det2 x y) x (det2 x t / det2 x y) y = t := by
  apply Prod.ext <;> dsimp [combine, det2] at * <;> field_simp <;> ring

/-- Exact counterexample to 'detecting implies cyclic under that same operator'. -/
theorem scalar_detection_counterexample :
    enorm (remainder ((1 : ℚ), 1)) = 2916 ∧
      det2 ((1 : ℚ), 0) (emul (sixth ((1 : ℚ), 1)) (1, 0)) = 0 ∧
      det2 (emul (remainder ((1 : ℚ), 1)) (1, 0))
        (emul (sixth ((2 : ℚ), 1)) (emul (remainder ((1 : ℚ), 1)) (1, 0))) = 1049760 := by
  norm_num [enorm, remainder, det2, sixth, cube, emul]

/-- The unit eta's induced sixth-power action is the identity, not an auxiliary rotation. -/
theorem eta_sixth_is_identity : sixth ((0 : ℚ), 1) = (1, 0) := by
  norm_num [sixth, cube, emul]

end RationalPlane
end Experiments.CorpusBridgeSixLines
