import Mathlib

/-!
# Prime shells and conjugate frames

A bounded formal core for Eisenstein norm shells, conjugate reference frames,
frame conditioning, and shell-to-shell transport.

Controlling mathematical source for the shell vocabulary: PAL v2.3-M,
RAINBOW / M-RNBW-SHELL and M-RNBW-FRAME, DOI 10.5281/zenodo.22240134.
Reserved manuscript record: 10.5281/zenodo.22288471.

The formalization proves the coordinate algebra and the new frame/transport
results stated below. It does not formalize the full classical representation
count for `a^2 + a*b + b^2`; that theorem remains a separately cited input.
No theorem here makes PAL canon, physics, or an RH claim.
-/

namespace PAL.PrimeShells

noncomputable section

/-- Coordinates for `a + bη`, where the intended generator satisfies `η² = η - 1`. -/
structure Point (R : Type*) where
  a : R
  b : R
  deriving DecidableEq, Repr

@[ext]
theorem Point.extensionality {R : Type*} {x y : Point R}
    (ha : x.a = y.a) (hb : x.b = y.b) : x = y := by
  cases x
  cases y
  simp_all

section CoordinateAlgebra

variable {R : Type*} [CommRing R]

/-- The origin in Eisenstein coordinates. -/
def origin : Point R := ⟨0, 0⟩

/-- A scalar, embedded as `r + 0η`. -/
def scalar (r : R) : Point R := ⟨r, 0⟩

/-- Coordinate addition. -/
def add (x y : Point R) : Point R := ⟨x.a + y.a, x.b + y.b⟩

/-- Coordinate scaling. -/
def scale (r : R) (x : Point R) : Point R := ⟨r * x.a, r * x.b⟩

/-- Multiplication induced by `η² = η - 1`. -/
def mul (x y : Point R) : Point R :=
  ⟨x.a * y.a - x.b * y.b, x.a * y.b + x.b * y.a + x.b * y.b⟩

/-- Complex conjugation in the `1,η` coordinate basis. -/
def conj (x : Point R) : Point R := ⟨x.a + x.b, -x.b⟩

/-- Multiplication by the sixth root `η`. -/
def rotate (x : Point R) : Point R := ⟨-x.b, x.a + x.b⟩

/-- The Eisenstein norm form `a² + ab + b²`. -/
def eNorm (x : Point R) : R := x.a ^ 2 + x.a * x.b + x.b ^ 2

/-- The integer-linear horizontal coordinate `2a+b`. -/
def xCoord (x : Point R) : R := 2 * x.a + x.b

/-- The vertical coefficient coordinate `b`. -/
def yCoord (x : Point R) : R := x.b

/-- The scaled planar coordinate `(2a+b,b)`. -/
def scaledEmbed (x : Point R) : Point R := ⟨xCoord x, yCoord x⟩

/-- Determinant of two coordinate vectors. -/
def pairDet (u v : Point R) : R := u.a * v.b - u.b * v.a

/-- The product controlling the area of a point with its conjugate. -/
def areaCoordinate (x : Point R) : R := xCoord x * yCoord x

/-- Linear combination of two coordinate vectors. -/
def combine (c d : R) (u v : Point R) : Point R :=
  ⟨c * u.a + d * v.a, c * u.b + d * v.b⟩

@[simp] theorem conj_involutive (x : Point R) : conj (conj x) = x := by
  rcases x with ⟨a, b⟩
  ext <;> simp [conj]

@[simp] theorem rotate_six (x : Point R) :
    rotate (rotate (rotate (rotate (rotate (rotate x))))) = x := by
  rcases x with ⟨a, b⟩
  ext <;> simp [rotate]

@[simp] theorem eNorm_conj (x : Point R) : eNorm (conj x) = eNorm x := by
  rcases x with ⟨a, b⟩
  simp [eNorm, conj]
  ring

@[simp] theorem eNorm_rotate (x : Point R) : eNorm (rotate x) = eNorm x := by
  rcases x with ⟨a, b⟩
  simp [eNorm, rotate]
  ring

@[simp] theorem eNorm_mul (x y : Point R) : eNorm (mul x y) = eNorm x * eNorm y := by
  rcases x with ⟨a, b⟩
  rcases y with ⟨c, d⟩
  simp [eNorm, mul]
  ring

@[simp] theorem mul_conj_eq_scalar_norm (x : Point R) : mul x (conj x) = scalar (eNorm x) := by
  rcases x with ⟨a, b⟩
  ext <;> simp [mul, conj, scalar, eNorm] <;> ring

@[simp] theorem scaled_norm_identity (x : Point R) :
    xCoord x ^ 2 + 3 * yCoord x ^ 2 = 4 * eNorm x := by
  rcases x with ⟨a, b⟩
  simp [xCoord, yCoord, eNorm]
  ring

@[simp] theorem scaledEmbed_conj (x : Point R) :
    scaledEmbed (conj x) = ⟨xCoord x, -yCoord x⟩ := by
  rcases x with ⟨a, b⟩
  ext <;> simp [scaledEmbed, xCoord, yCoord, conj] <;> ring

@[simp] theorem conjugate_frame_det (x : Point R) :
    pairDet (scaledEmbed x) (scaledEmbed (conj x)) = -2 * areaCoordinate x := by
  rcases x with ⟨a, b⟩
  simp [pairDet, scaledEmbed, xCoord, yCoord, conj, areaCoordinate]
  ring

@[simp] theorem rotate_fixed_iff_origin (x : Point R) : rotate x = x ↔ x = origin := by
  constructor
  · intro h
    rcases x with ⟨a, b⟩
    have hfirst : -b = a := congrArg Point.a h
    have hsecond : a + b = b := congrArg Point.b h
    have ha : a = 0 := by
      calc
        a = (a + b) - b := by ring
        _ = b - b := by rw [hsecond]
        _ = 0 := sub_self b
    have hneg : -b = 0 := hfirst.trans ha
    have hb : b = 0 := neg_eq_zero.mp hneg
    ext <;> simp [origin, ha, hb]
  · rintro rfl
    simp [rotate, origin]

/-- A positive shell cannot carry a point fixed by the full sixty-degree rotation. -/
theorem no_positive_shell_rotation_fixed (x : Point ℝ) (hx : 0 < eNorm x) : rotate x ≠ x := by
  intro h
  have hzero : x = origin := (rotate_fixed_iff_origin x).mp h
  subst hzero
  norm_num [eNorm, origin] at hx

end CoordinateAlgebra

/-- The exact norm shell at level `n`. -/
def Shell {R : Type*} [CommRing R] (n : R) : Set (Point R) := {x | eNorm x = n}

section ModThree

/-- Modulo three, the Eisenstein norm assumes only `0` or `1`. -/
theorem norm_mod_three (a b : ZMod 3) :
    a ^ 2 + a * b + b ^ 2 = 0 ∨ a ^ 2 + a * b + b ^ 2 = 1 := by
  revert a b
  native_decide

/-- A shell whose level is `2` modulo three has no integer point. -/
theorem no_integer_shell_of_mod_three_two {n : ℤ} (hn : (n : ZMod 3) = 2) :
    ¬ ∃ x : Point ℤ, eNorm x = n := by
  rintro ⟨x, hx⟩
  have hmod := norm_mod_three (x.a : ZMod 3) (x.b : ZMod 3)
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

/-- The norm-17 shell is empty. -/
theorem shell_seventeen_empty : ¬ ∃ x : Point ℤ, eNorm x = 17 := by
  apply no_integer_shell_of_mod_three_two
  native_decide

end ModThree

section ThreeCandidateFrames

/-- Three antipodally distinct unit rotations suffice for conjugate-frame selection. -/
inductive FrameChoice where
  | base
  | turn
  | turnTwice
  deriving DecidableEq, Repr, Fintype

/-- Select one of the three candidate representatives. The other three unit rotations are negatives. -/
def choosePoint (k : FrameChoice) {R : Type*} [CommRing R] (x : Point R) : Point R :=
  match k with
  | .base => x
  | .turn => rotate x
  | .turnTwice => rotate (rotate x)

@[simp] theorem eNorm_choosePoint {R : Type*} [CommRing R]
    (k : FrameChoice) (x : Point R) : eNorm (choosePoint k x) = eNorm x := by
  cases k <;> simp [choosePoint]

@[simp] theorem area_base {R : Type*} [CommRing R] (x : Point R) :
    areaCoordinate (choosePoint .base x) = x.b * (2 * x.a + x.b) := by
  simp [choosePoint, areaCoordinate, xCoord, yCoord, mul_comm]

@[simp] theorem area_turn {R : Type*} [CommRing R] (x : Point R) :
    areaCoordinate (choosePoint .turn x) = x.a ^ 2 - x.b ^ 2 := by
  rcases x with ⟨a, b⟩
  simp [choosePoint, rotate, areaCoordinate, xCoord, yCoord]
  ring

@[simp] theorem area_turnTwice {R : Type*} [CommRing R] (x : Point R) :
    areaCoordinate (choosePoint .turnTwice x) = -x.a * (x.a + 2 * x.b) := by
  rcases x with ⟨a, b⟩
  simp [choosePoint, rotate, areaCoordinate, xCoord, yCoord]
  ring

/-- The three squared conjugate-frame area coordinates have fixed total `2 N(x)^2`. -/
theorem three_area_square_sum {R : Type*} [CommRing R] (x : Point R) :
    areaCoordinate (choosePoint .base x) ^ 2 +
      areaCoordinate (choosePoint .turn x) ^ 2 +
      areaCoordinate (choosePoint .turnTwice x) ^ 2 =
        2 * eNorm x ^ 2 := by
  rcases x with ⟨a, b⟩
  simp [choosePoint, rotate, areaCoordinate, xCoord, yCoord, eNorm]
  ring

/-- A nonnegative square product used by the robust-frame proof. -/
def frameObstruction (x : Point ℝ) : ℝ :=
  x.a ^ 2 * x.b ^ 2 * (x.a - x.b) ^ 2 * (x.a + x.b) ^ 2 *
    (x.a + 2 * x.b) ^ 2 * (2 * x.a + x.b) ^ 2

/-- Exact factorization of the three candidate shortfalls. -/
theorem frame_gap_product (x : Point ℝ) :
    (eNorm x ^ 2 - areaCoordinate (choosePoint .base x) ^ 2) *
      (eNorm x ^ 2 - areaCoordinate (choosePoint .turn x) ^ 2) *
      (eNorm x ^ 2 - areaCoordinate (choosePoint .turnTwice x) ^ 2) =
        -frameObstruction x := by
  rcases x with ⟨a, b⟩
  simp [choosePoint, rotate, areaCoordinate, xCoord, yCoord, eNorm, frameObstruction]
  ring

/-- Every nonzero hexagonal-lattice direction has a unit-rotated conjugate pair whose
normalized squared determinant is at least `3/4`. The division-free core is
`N(x)^2 ≤ areaCoordinate^2`. -/
theorem exists_robust_frame_choice (x : Point ℝ) :
    ∃ k : FrameChoice,
      eNorm x ^ 2 ≤ areaCoordinate (choosePoint k x) ^ 2 := by
  by_cases h0 : eNorm x ^ 2 ≤ areaCoordinate (choosePoint .base x) ^ 2
  · exact ⟨.base, h0⟩
  by_cases h1 : eNorm x ^ 2 ≤ areaCoordinate (choosePoint .turn x) ^ 2
  · exact ⟨.turn, h1⟩
  by_cases h2 : eNorm x ^ 2 ≤ areaCoordinate (choosePoint .turnTwice x) ^ 2
  · exact ⟨.turnTwice, h2⟩
  have h0' : 0 < eNorm x ^ 2 - areaCoordinate (choosePoint .base x) ^ 2 :=
    sub_pos.mpr (lt_of_not_ge h0)
  have h1' : 0 < eNorm x ^ 2 - areaCoordinate (choosePoint .turn x) ^ 2 :=
    sub_pos.mpr (lt_of_not_ge h1)
  have h2' : 0 < eNorm x ^ 2 - areaCoordinate (choosePoint .turnTwice x) ^ 2 :=
    sub_pos.mpr (lt_of_not_ge h2)
  have hproduct :
      0 <
        (eNorm x ^ 2 - areaCoordinate (choosePoint .base x) ^ 2) *
          (eNorm x ^ 2 - areaCoordinate (choosePoint .turn x) ^ 2) *
          (eNorm x ^ 2 - areaCoordinate (choosePoint .turnTwice x) ^ 2) :=
    mul_pos (mul_pos h0' h1') h2'
  rw [frame_gap_product] at hproduct
  have hnonneg : 0 ≤ frameObstruction x := by
    unfold frameObstruction
    positivity
  linarith

/-- A conjugate frame is algebraically ready exactly when its two scaled axes are nonzero. -/
def FrameReady (x : Point ℝ) : Prop := xCoord x ≠ 0 ∧ yCoord x ≠ 0

/-- A robust choice at nonzero norm is automatically a genuine two-reference frame. -/
theorem frameReady_of_robust {x : Point ℝ}
    (hNorm : eNorm x ≠ 0)
    (hRobust : eNorm x ^ 2 ≤ areaCoordinate x ^ 2) : FrameReady x := by
  have hNormSq : 0 < eNorm x ^ 2 := sq_pos_of_ne_zero hNorm
  have hAreaSq : 0 < areaCoordinate x ^ 2 := lt_of_lt_of_le hNormSq hRobust
  have hArea : areaCoordinate x ≠ 0 := by
    intro h
    rw [h] at hAreaSq
    norm_num at hAreaSq
  constructor
  · intro hx
    apply hArea
    simp [areaCoordinate, hx]
  · intro hy
    apply hArea
    simp [areaCoordinate, hy]

/-- Squared normalized area of the Euclidean conjugate frame, written without square roots. -/
def frameStrengthSq (x : Point ℝ) : ℝ :=
  3 * areaCoordinate x ^ 2 / (4 * eNorm x ^ 2)

/-- Every conjugate frame has normalized squared area at most one. -/
theorem area_upper_bound (x : Point ℝ) :
    3 * areaCoordinate x ^ 2 ≤ 4 * eNorm x ^ 2 := by
  rcases x with ⟨a, b⟩
  simp [areaCoordinate, xCoord, yCoord, eNorm]
  nlinarith [sq_nonneg ((2 * a + b) ^ 2 - 3 * b ^ 2)]

/-- A robust choice attains squared normalized area at least `3/4`. -/
theorem robust_strength_lower_bound {x : Point ℝ}
    (hNorm : eNorm x ≠ 0)
    (hRobust : eNorm x ^ 2 ≤ areaCoordinate x ^ 2) :
    (3 : ℝ) / 4 ≤ frameStrengthSq x := by
  have hden : 0 < 4 * eNorm x ^ 2 := by
    have hsquare : 0 < eNorm x ^ 2 := sq_pos_of_ne_zero hNorm
    nlinarith
  rw [frameStrengthSq]
  apply (le_div_iff₀ hden).2
  nlinarith

/-- A nonzero conjugate frame has squared normalized area at most one. -/
theorem frameStrengthSq_le_one {x : Point ℝ} (hNorm : eNorm x ≠ 0) :
    frameStrengthSq x ≤ 1 := by
  have hden : 0 < 4 * eNorm x ^ 2 := by
    have hsquare : 0 < eNorm x ^ 2 := sq_pos_of_ne_zero hNorm
    nlinarith
  rw [frameStrengthSq]
  apply (div_le_iff₀ hden).2
  nlinarith [area_upper_bound x]

/-- Prime-shell corollary: any supplied integer representative of a rational prime shell
admits a uniformly robust conjugate frame after one of three unit rotations. -/
theorem prime_shell_has_robust_conjugate_frame {p : ℕ} (hp : p.Prime)
    {a b : ℤ} (hShell : a ^ 2 + a * b + b ^ 2 = (p : ℤ)) :
    ∃ k : FrameChoice,
      let x : Point ℝ := ⟨a, b⟩
      let y := choosePoint k x
      FrameReady y ∧ (3 : ℝ) / 4 ≤ frameStrengthSq y := by
  let x : Point ℝ := ⟨a, b⟩
  have hNormEq : eNorm x = (p : ℝ) := by
    dsimp [x, eNorm]
    exact_mod_cast hShell
  have hNorm : eNorm x ≠ 0 := by
    rw [hNormEq]
    exact_mod_cast hp.ne_zero
  obtain ⟨k, hk⟩ := exists_robust_frame_choice x
  have hNormChoice : eNorm (choosePoint k x) ≠ 0 := by
    simpa using hNorm
  refine ⟨k, ?_⟩
  dsimp
  constructor
  · exact frameReady_of_robust hNormChoice (by simpa using hk)
  · exact robust_strength_lower_bound hNormChoice (by simpa using hk)

end ThreeCandidateFrames

section MinimalReferenceAndTransport

/-- One vector never spans the entire real plane. -/
theorem one_reference_is_insufficient (u : Point ℝ) :
    ∃ v : Point ℝ, ¬ ∃ c : ℝ, scale c u = v := by
  by_cases hu : u.a = 0
  · refine ⟨⟨1, 0⟩, ?_⟩
    rintro ⟨c, h⟩
    have hfirst := congrArg Point.a h
    simp [scale, hu] at hfirst
  · refine ⟨⟨0, 1⟩, ?_⟩
    rintro ⟨c, h⟩
    have hfirst := congrArg Point.a h
    have hsecond := congrArg Point.b h
    simp [scale] at hfirst hsecond
    have hc : c = 0 := hfirst.resolve_right hu
    rw [hc] at hsecond
    norm_num at hsecond

/-- Coefficient of the selected reference in the conjugate-frame decomposition. -/
def plusCoefficient (x v : Point ℝ) : ℝ :=
  v.a / (2 * xCoord x) + v.b / (2 * yCoord x)

/-- Coefficient of the reflected reference in the conjugate-frame decomposition. -/
def minusCoefficient (x v : Point ℝ) : ℝ :=
  v.a / (2 * xCoord x) - v.b / (2 * yCoord x)

/-- Two nonparallel conjugate references reconstruct every point of the plane. -/
theorem two_references_reconstruct (x v : Point ℝ) (hx : FrameReady x) :
    combine (plusCoefficient x v) (minusCoefficient x v)
      (scaledEmbed x) (scaledEmbed (conj x)) = v := by
  rw [scaledEmbed_conj]
  ext <;>
    simp [combine, plusCoefficient, minusCoefficient, scaledEmbed] <;>
    field_simp [hx.1, hx.2] <;>
    ring

/-- Diagonal shell-to-shell transport in the conjugation eigen-coordinates. -/
def transport (x y v : Point ℝ) : Point ℝ :=
  ⟨(xCoord y / xCoord x) * v.a, (yCoord y / yCoord x) * v.b⟩

/-- Transport sends the selected reference of one frame to that of another. -/
theorem transport_selected (x y : Point ℝ) (hx : FrameReady x) :
    transport x y (scaledEmbed x) = scaledEmbed y := by
  ext <;> simp [transport, scaledEmbed, hx.1, hx.2]

/-- Transport also sends the reflected reference to the reflected reference. -/
theorem transport_reflected (x y : Point ℝ) (hx : FrameReady x) :
    transport x y (scaledEmbed (conj x)) = scaledEmbed (conj y) := by
  rw [scaledEmbed_conj, scaledEmbed_conj]
  ext <;> simp [transport, hx.1, hx.2]

/-- Identity transport. -/
theorem transport_self (x v : Point ℝ) (hx : FrameReady x) :
    transport x x v = v := by
  ext <;> simp [transport, hx.1, hx.2]

/-- Composition is exact: shell transport forms a cocycle/groupoid law on ready frames. -/
theorem transport_compose (x y z v : Point ℝ)
    (hx : FrameReady x) (hy : FrameReady y) :
    transport y z (transport x y v) = transport x z v := by
  ext <;>
    simp [transport] <;>
    field_simp [hx.1, hx.2, hy.1, hy.2] <;>
    ring

/-- Reversing the shell transport recovers the starting vector. -/
theorem transport_inverse (x y v : Point ℝ)
    (hx : FrameReady x) (hy : FrameReady y) :
    transport y x (transport x y v) = v := by
  rw [transport_compose x y x v hx hy]
  exact transport_self x v hx

end MinimalReferenceAndTransport

section Fixtures

/-- The ramified shell has the familiar norm-3 point. -/
example : eNorm (Point.mk 1 1 : Point ℤ) = 3 := by norm_num [eNorm]

/-- First split-prime fixture. -/
example : eNorm (Point.mk 2 1 : Point ℤ) = 7 := by norm_num [eNorm]

/-- Second split-prime fixture. -/
example : eNorm (Point.mk 3 1 : Point ℤ) = 13 := by norm_num [eNorm]

/-- A further split-prime fixture. -/
example : eNorm (Point.mk 3 2 : Point ℤ) = 19 := by norm_num [eNorm]

end Fixtures

end

end PAL.PrimeShells
