import Experiments.CorpusBridgeSixLines
import Audit.BridgeEndpoint

/-!
# W00: the norm-three projector with a separately admitted generator

Source: CHARTER v1.0 and BRIDGE v0.4, retained by BRIDGE v0.6 §12.
This extends PR #21's checked coordinate core. The supplied W00 ZIP suggests
the norm-three projector; its uncompiled replacement core is not imported.

The target is a rational line plus an explicit rational plane. The final
theorem instantiates the existing conditional Weil detector theorem. Geometric
actions, algebraicity preservation and an actual algebraic seed are not
constructed by naming this coordinate model.
-/

namespace Experiments.CorpusBridgeProjector

open Experiments.CorpusBridgeSixLines

abbrev Plane := ℚ × ℚ
abbrev Target := ℚ × Plane

/-- The existing Eisenstein multiplication, packaged as a rational linear map. -/
def multiplier (z : Plane) : Plane →ₗ[ℚ] Plane where
  toFun w := emul z w
  map_add' x y := by
    apply Prod.ext <;> dsimp [emul] <;> ring
  map_smul' a x := by
    apply Prod.ext <;> dsimp [emul] <;> ring

/-- The action at rho = 1 + eta on the declared line-plus-plane target. -/
def rhoAction : Target →ₗ[ℚ] Target where
  toFun x := (27 * x.1, (-27 * x.2.1, -27 * x.2.2))
  map_add' x y := by
    ext <;> dsimp <;> ring
  map_smul' a x := by
    ext <;> dsimp <;> ring

/-- The fixed norm-seven generator uses the already checked sixth-power map. -/
def generator : Plane →ₗ[ℚ] Plane := multiplier (sixth ((2 : ℚ), 1))

/-- Whole-space action at mu = 2 + eta, with norm cubed 343 on the known line. -/
def muAction : Target →ₗ[ℚ] Target where
  toFun x := (343 * x.1, generator x.2)
  map_add' x y := by
    apply Prod.ext
    · dsimp
      ring
    · exact generator.map_add x.2 y.2
  map_smul' a x := by
    apply Prod.ext
    · dsimp
      ring
    · exact generator.map_smul a x.2

/-- Spectral projector, defined from the action rather than from its desired output. -/
def projector : Target →ₗ[ℚ] Target :=
  (1 / 54 : ℚ) • ((27 : ℚ) • LinearMap.id - rhoAction)

theorem rhoAction_matches_eisenstein (x : Target) :
    rhoAction x =
      ((CorpusBridgeSixLines.enorm ((1 : ℚ), 1)) ^ 3 * x.1,
        emul (sixth ((1 : ℚ), 1)) x.2) := by
  rcases x with ⟨h, u, v⟩
  ext <;> norm_num [rhoAction, CorpusBridgeSixLines.enorm, emul, sixth, cube]

theorem muAction_matches_eisenstein (x : Target) :
    muAction x =
      ((CorpusBridgeSixLines.enorm ((2 : ℚ), 1)) ^ 3 * x.1,
        emul (sixth ((2 : ℚ), 1)) x.2) := by
  rcases x with ⟨h, u, v⟩
  ext <;> norm_num [muAction, generator, multiplier, CorpusBridgeSixLines.enorm]

theorem projector_formula (x : Target) : projector x = (0, x.2) := by
  rcases x with ⟨h, u, v⟩
  ext <;> simp [projector, rhoAction, smul_eq_mul] <;> ring

theorem projector_idempotent (x : Target) :
    projector (projector x) = projector x := by
  simp only [projector_formula]

theorem projector_pure (x : Target) : (projector x).1 = 0 := by
  simp only [projector_formula]

theorem projector_nonzero : projector ≠ 0 := by
  intro hp
  have h := congrArg (fun f : Target →ₗ[ℚ] Target => f (0, (1, 0))) hp
  norm_num [projector_formula] at h

/-- Stability under rho already supplies stability under its rational projector. -/
theorem projector_preserves (A : Submodule ℚ Target)
    (hρ : ∀ x : Target, x ∈ A → rhoAction x ∈ A)
    (x : Target) (hx : x ∈ A) : projector x ∈ A := by
  change (1 / 54 : ℚ) • ((27 : ℚ) • x - rhoAction x) ∈ A
  exact A.smul_mem _ (A.sub_mem (A.smul_mem _ hx) (hρ x hx))

theorem generator_preserves_pure (A : Submodule ℚ Target)
    (hμ : ∀ x : Target, x ∈ A → muAction x ∈ A)
    (w : Plane) (hw : (0, w) ∈ A) : (0, generator w) ∈ A := by
  have h := hμ (0, w) hw
  simpa [muAction] using h

/-- Cramer's reconstruction from the checked core discharges the cyclic premise. -/
theorem generator_cyclic (seed : Plane) (hs : seed ≠ 0) (w : Plane) :
    ∃ a b : ℚ, w = a • seed + b • generator seed := by
  have hn : CorpusBridgeSixLines.enorm seed ≠ 0 :=
    fun h => hs ((rational_norm_zero_iff seed).mp h)
  have hd : det2 seed (generator seed) ≠ 0 := by
    change det2 seed (emul (sixth ((2 : ℚ), 1)) seed) ≠ 0
    rw [auxiliary_determinant]
    exact mul_ne_zero (by norm_num) hn
  refine ⟨det2 w (generator seed) / det2 seed (generator seed),
    det2 seed w / det2 seed (generator seed), ?_⟩
  have h := reconstruct_from_pair seed (generator seed) w hd
  exact h.symm

/-- The concrete consumer: the inherited theorem now has explicit P and G inputs. -/
theorem projector_generator_complete_iff (A : Submodule ℚ Target)
    (horizontal : ∀ h : ℚ, (h, 0) ∈ A)
    (hρ : ∀ x : Target, x ∈ A → rhoAction x ∈ A)
    (hμ : ∀ x : Target, x ∈ A → muAction x ∈ A) :
    A = ⊤ ↔ ∃ c : Target, c ∈ A ∧ projector c ≠ 0 := by
  exact Bridge.conditionalWeilDetector_iff A projector generator horizontal
    (projector_preserves A hρ) projector_pure projector_nonzero
    (generator_preserves_pure A hμ) generator_cyclic

/-- A proper plane containing the known line and only one exceptional direction. -/
def scalarCounterspace : Submodule ℚ Target where
  carrier := {x | x.2.2 = 0}
  zero_mem' := rfl
  add_mem' := by
    intro x y hx hy
    change x.2.2 + y.2.2 = 0
    change x.2.2 = 0 at hx
    change y.2.2 = 0 at hy
    rw [hx, hy]
    ring
  smul_mem' := by
    intro a x hx
    change a * x.2.2 = 0
    change x.2.2 = 0 at hx
    rw [hx]
    ring

theorem scalarCounterspace_horizontal (h : ℚ) : (h, 0) ∈ scalarCounterspace := rfl

theorem scalarCounterspace_rho (x : Target) (hx : x ∈ scalarCounterspace) :
    rhoAction x ∈ scalarCounterspace := by
  change -27 * x.2.2 = 0
  change x.2.2 = 0 at hx
  rw [hx]
  ring

theorem scalarCounterspace_seed :
    ((0, (1, 0)) : Target) ∈ scalarCounterspace ∧
      projector (0, (1, 0)) ≠ 0 := by
  constructor
  · rfl
  · simp [projector_formula]

theorem scalarCounterspace_proper : scalarCounterspace ≠ ⊤ := by
  intro h
  have hm : ((0, (0, 1)) : Target) ∈ scalarCounterspace := by
    rw [h]
    trivial
  change (1 : ℚ) = 0 at hm
  norm_num at hm

theorem scalarCounterspace_not_mu_stable :
    muAction (0, (1, 0)) ∉ scalarCounterspace := by
  change (generator (1, 0)).2 ≠ 0
  norm_num [generator, multiplier, sixth, cube, emul]

/-- Without the second stability hypothesis, the conclusion is false. -/
theorem dropping_generator_stability_fails :
    (∀ h : ℚ, (h, 0) ∈ scalarCounterspace) ∧
    (∀ x : Target, x ∈ scalarCounterspace → rhoAction x ∈ scalarCounterspace) ∧
    (∃ c : Target, c ∈ scalarCounterspace ∧ projector c ≠ 0) ∧
    scalarCounterspace ≠ ⊤ := by
  exact ⟨scalarCounterspace_horizontal, scalarCounterspace_rho,
    ⟨(0, (1, 0)), scalarCounterspace_seed⟩, scalarCounterspace_proper⟩

/-- Extra mixed action from the ZIP's domain countermodel. -/
def mixedAction : Plane →ₗ[ℚ] Plane := multiplier (-27, 27)

def mixedProjector : Plane →ₗ[ℚ] Plane :=
  (1 / 54 : ℚ) • ((27 : ℚ) • LinearMap.id - mixedAction)

theorem mixedProjector_not_idempotent :
    mixedProjector (mixedProjector (1, 0)) ≠ mixedProjector (1, 0) := by
  norm_num [mixedProjector, mixedAction, multiplier, emul, Prod.mk.injEq]

end Experiments.CorpusBridgeProjector
