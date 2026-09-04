import PAL.PrimeShellsConditionNumber

/-!
# Three chart roles for framed prime shells

Version 0.2 separates three mathematically different uses of an added axis:

1. a derived spherical state chart, which redraws the same two-dimensional
   state without adding a distinction;
2. an independently indexed shell atlas, whose joint fibers intersect the
   fibers of the original state and the added condition; and
3. a route object through that atlas, developed in `PrimeShellsRibbons`.

The Smith-sphere formulas below are an external geometric realization of this
separation. They do not import radio-frequency measurements into the arithmetic
prime-shell theorem and they do not make a physical claim about prime shells.
-/

namespace PAL.PrimeShells

noncomputable section

section FiberGeometry

universe u v w x

variable {W : Type u} {T : Type v} {A : Type w} {B : Type x}

/-- Two underlying alternatives occupy the same fiber of a declared trace. -/
def SameFiber (f : W → T) (p q : W) : Prop := f p = f q

/-- `fine` refines `coarse` when every collision of `fine` is already a
collision of `coarse`. -/
def Refines (fine : W → A) (coarse : W → T) : Prop :=
  ∀ ⦃p q : W⦄, fine p = fine q → coarse p = coarse q

/-- Strict refinement adds at least one distinction while retaining all
coarse distinctions. -/
def StrictlyRefines (fine : W → A) (coarse : W → T) : Prop :=
  Refines fine coarse ∧ ¬ Refines coarse fine

/-- Add an axis computed entirely from the original trace. -/
def derivedAxis (trace : W → T) (axis : T → A) : W → T × A :=
  fun p => (trace p, axis (trace p))

/-- Add a separately supplied observable or condition. -/
def jointAxis (trace : W → T) (axis : W → A) : W → T × A :=
  fun p => (trace p, axis p)

/-- A derived axis has exactly the same fibers as the original trace. -/
theorem derivedAxis_sameFiber (trace : W → T) (axis : T → A) (p q : W) :
    SameFiber (derivedAxis trace axis) p q ↔ SameFiber trace p q := by
  constructor
  · intro h
    exact congrArg Prod.fst h
  · intro h
    apply Prod.ext
    · exact h
    · exact congrArg axis h

/-- A genuinely joint chart retains exactly the intersection of the two
component fiber relations. -/
theorem jointAxis_sameFiber (trace : W → T) (axis : W → A) (p q : W) :
    SameFiber (jointAxis trace axis) p q ↔
      SameFiber trace p q ∧ SameFiber axis p q := by
  constructor
  · intro h
    exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩
  · rintro ⟨hTrace, hAxis⟩
    exact Prod.ext hTrace hAxis

/-- The joint chart always refines either component. -/
theorem jointAxis_refines_left (trace : W → T) (axis : W → A) :
    Refines (jointAxis trace axis) trace := by
  intro p q h
  exact congrArg Prod.fst h

/-- A deterministic decoration and its source trace refine one another. -/
theorem derivedAxis_refinement_equiv (trace : W → T) (axis : T → A) :
    Refines (derivedAxis trace axis) trace ∧
      Refines trace (derivedAxis trace axis) := by
  constructor
  · exact jointAxis_refines_left trace (fun p => axis (trace p))
  · intro p q h
    apply Prod.ext
    · exact h
    · exact congrArg axis h

/-- A separately retained axis strictly refines a trace as soon as it separates
one pair that the trace collapses. -/
theorem jointAxis_strictly_refines_of_witness
    (trace : W → T) (axis : W → A) {p q : W}
    (hTrace : trace p = trace q) (hAxis : axis p ≠ axis q) :
    StrictlyRefines (jointAxis trace axis) trace := by
  constructor
  · exact jointAxis_refines_left trace axis
  · intro hBack
    have hPair : jointAxis trace axis p = jointAxis trace axis q := hBack hTrace
    exact hAxis (congrArg Prod.snd hPair)

/-- When the new coordinate factors through the old trace, the nominal joint
chart is definitionally a derived chart. -/
theorem jointAxis_eq_derived (trace : W → T) (axis : T → A) :
    jointAxis trace (fun p => axis (trace p)) = derivedAxis trace axis := rfl

end FiberGeometry

section SmithSphere

/-- A small carrier for exact three-coordinate formulas. -/
structure Point3 (R : Type*) where
  x : R
  y : R
  z : R
  deriving DecidableEq, Repr

@[ext]
theorem Point3.extensionality {R : Type*} {p q : Point3 R}
    (hx : p.x = q.x) (hy : p.y = q.y) (hz : p.z = q.z) : p = q := by
  cases p
  cases q
  simp_all

/-- Coordinate scaling in three dimensions. -/
def scale3 {R : Type*} [Mul R] (r : R) (p : Point3 R) : Point3 R :=
  ⟨r * p.x, r * p.y, r * p.z⟩

/-- Squared Euclidean radius. -/
def normSq3 (p : Point3 ℝ) : ℝ := p.x ^ 2 + p.y ^ 2 + p.z ^ 2

/-- Denominator of the stereographic Smith-sphere lift. -/
def smithDen (p : Point ℝ) : ℝ := 1 + p.a ^ 2 + p.b ^ 2

/-- Stereographic lift of a planar reflection-coefficient coordinate to the
unit sphere. The third coordinate is derived from the first two. -/
def smithSphere (p : Point ℝ) : Point3 ℝ :=
  let d := smithDen p
  ⟨2 * p.a / d, 2 * p.b / d, (1 - p.a ^ 2 - p.b ^ 2) / d⟩

/-- The stereographic denominator is always positive. -/
theorem smithDen_pos (p : Point ℝ) : 0 < smithDen p := by
  unfold smithDen
  nlinarith [sq_nonneg p.a, sq_nonneg p.b]

/-- The Smith-sphere lift lands exactly on the unit sphere. -/
theorem normSq3_smithSphere (p : Point ℝ) : normSq3 (smithSphere p) = 1 := by
  rcases p with ⟨u, v⟩
  have hd : 1 + u ^ 2 + v ^ 2 ≠ 0 := by
    nlinarith [sq_nonneg u, sq_nonneg v]
  simp [normSq3, smithSphere, smithDen]
  field_simp [hd]
  ring

/-- Planar coordinate recovered from every point in the image of the
stereographic lift. -/
def smithSphereBack (p : Point3 ℝ) : Point ℝ :=
  ⟨p.x / (1 + p.z), p.y / (1 + p.z)⟩

/-- The sphere lift has an exact left inverse on its image. -/
theorem smithSphereBack_smithSphere (p : Point ℝ) :
    smithSphereBack (smithSphere p) = p := by
  rcases p with ⟨u, v⟩
  have hd : 1 + u ^ 2 + v ^ 2 ≠ 0 := by
    nlinarith [sq_nonneg u, sq_nonneg v]
  apply Point.extensionality
  · simp [smithSphereBack, smithSphere, smithDen]
    field_simp [hd]
    ring
  · simp [smithSphereBack, smithSphere, smithDen]
    field_simp [hd]
    ring

/-- The derived spherical state chart is injective. -/
theorem smithSphere_injective : Function.Injective smithSphere :=
  (fun p => smithSphereBack_smithSphere p).injective

/-- Equality on the spherical chart is exactly equality on the planar chart. -/
theorem smithSphere_sameFiber (p q : Point ℝ) :
    smithSphere p = smithSphere q ↔ p = q := by
  constructor
  · exact smithSphere_injective
  · intro h
    exact congrArg smithSphere h

/-- Squared radius scales quadratically. -/
theorem normSq3_scale3 (r : ℝ) (p : Point3 ℝ) :
    normSq3 (scale3 r p) = r ^ 2 * normSq3 p := by
  rcases p with ⟨x, y, z⟩
  simp [normSq3, scale3]
  ring

/-- Exact product carrier for a spherical Smith state together with a separately
retained condition. -/
abbrev SmithShellAtlas (A : Type*) := Point3 ℝ × A

/-- Exact atlas point: spherical state plus independent condition label. -/
def smithAtlasPoint {W A : Type*}
    (state : W → Point ℝ) (axis : W → A) (p : W) : SmithShellAtlas A :=
  (smithSphere (state p), axis p)

/-- The exact atlas fibers are the intersection of planar-state and condition
fibers. -/
theorem smithAtlasPoint_sameFiber {W A : Type*}
    (state : W → Point ℝ) (axis : W → A) (p q : W) :
    smithAtlasPoint state axis p = smithAtlasPoint state axis q ↔
      state p = state q ∧ axis p = axis q := by
  constructor
  · intro h
    have hSphere := congrArg Prod.fst h
    have hAxis := congrArg Prod.snd h
    exact ⟨smithSphere_injective hSphere, hAxis⟩
  · rintro ⟨hState, hAxis⟩
    apply Prod.ext
    · exact congrArg smithSphere hState
    · exact hAxis

/-- Radial visualization of an indexed spherical state. This is a rendering of
an exact product atlas, not the definition of its information content. -/
def radialSmithShell {W A : Type*}
    (radius : A → ℝ) (state : W → Point ℝ) (axis : W → A) (p : W) : Point3 ℝ :=
  scale3 (radius (axis p)) (smithSphere (state p))

/-- Every fixed independent-axis value is rendered on its declared spherical
radius. -/
theorem radialSmithShell_normSq {W A : Type*}
    (radius : A → ℝ) (state : W → Point ℝ) (axis : W → A) (p : W) :
    normSq3 (radialSmithShell radius state axis p) = radius (axis p) ^ 2 := by
  rw [radialSmithShell, normSq3_scale3, normSq3_smithSphere]
  ring

end SmithSphere

end

end PAL.PrimeShells
