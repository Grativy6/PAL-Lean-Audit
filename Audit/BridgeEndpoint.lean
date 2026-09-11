import Mathlib.LinearAlgebra.Dual.Lemmas
import Mathlib.LinearAlgebra.Basis.VectorSpace
import Mathlib.Tactic

noncomputable section

/-!
# BRIDGE endpoint calculus — bounded Lean realization

Controlling source: Christopher D. Pang, *BRIDGE: Binding Residue and Information
Dynamics of Generative Export*, v0.2, reserved DOI 10.5281/zenodo.22699551.

This module checks the exact linear-algebraic spine used by the manuscript:
readout collisions, common-kernel repair by an appended trace, dual detection of
generative defect, uniqueness after a surjective bridge, one-scalar separation
of a hidden line, and the four-sector dimension account.

The authority ceiling is the displayed theorem statements. In particular, this
module does not encode Hodge structures, algebraic cycles, or the geometric
hypotheses of the manuscript's conditional Weil-class detector.
-/

namespace Bridge

open Module

section Endpoint

variable {𝕜 G T R S A : Type*}
variable [Field 𝕜]
variable [AddCommGroup G] [Module 𝕜 G]
variable [AddCommGroup T] [Module 𝕜 T]
variable [AddCommGroup R] [Module 𝕜 R]
variable [AddCommGroup S] [Module 𝕜 S]
variable [AddCommGroup A] [Module 𝕜 A]

/-- The dual collisions of a generator are exactly the probes annihilating its range. -/
theorem dualCollisionSpace (e : G →ₗ[𝕜] T) :
    LinearMap.ker e.dualMap = (LinearMap.range e).dualAnnihilator :=
  LinearMap.ker_dualMap_eq_dualAnnihilator_range e

/--
The quotient defect dual is linearly equivalent to the collision space of
pulled-back probes. This is the exact BRIDGE identity
`(T / range e)∗ ≃ ker (e∗)`.
-/
noncomputable def quotientDualEquivDualCollision (e : G →ₗ[𝕜] T) :
    Module.Dual 𝕜 (T ⧸ LinearMap.range e) ≃ₗ[𝕜]
      LinearMap.ker e.dualMap :=
  (LinearMap.range e).dualQuotEquivDualAnnihilator.trans
    (LinearEquiv.ofEq _ _
      (LinearMap.ker_dualMap_eq_dualAnnihilator_range e).symm)

/-- A generator misses part of its target exactly when pullback on dual probes collides. -/
theorem generativeDefect_iff_dualCollision (e : G →ₗ[𝕜] T) :
    ¬ Function.Surjective e ↔ ¬ Function.Injective e.dualMap :=
  (not_congr (LinearMap.dualMap_injective_iff (f := e))).symm

/-- Two target states have the same readout exactly when their difference is invisible. -/
theorem readoutCollision_iff_differenceInKernel
    (r : T →ₗ[𝕜] R) (x y : T) :
    r x = r y ↔ x - y ∈ LinearMap.ker r := by
  rw [LinearMap.mem_ker, map_sub, sub_eq_zero]

/--
An appended trace determines every value of an authority map exactly when the
common invisible sector lies in that authority map's kernel.
-/
theorem appendedTrace_determines_iff
    (r : T →ₗ[𝕜] R) (σ : T →ₗ[𝕜] S) (a : T →ₗ[𝕜] A) :
    (∀ x y, r x = r y → σ x = σ y → a x = a y) ↔
      LinearMap.ker r ⊓ LinearMap.ker σ ≤ LinearMap.ker a := by
  constructor
  · intro h z hz
    rw [Submodule.mem_inf] at hz
    rcases hz with ⟨hr, hσ⟩
    rw [LinearMap.mem_ker] at hr hσ ⊢
    have ha := h z 0 (by simpa using hr) (by simpa using hσ)
    simpa using ha
  · intro h x y hr hσ
    apply (readoutCollision_iff_differenceInKernel a x y).2
    apply h
    exact ⟨(readoutCollision_iff_differenceInKernel r x y).1 hr,
      (readoutCollision_iff_differenceInKernel σ x y).1 hσ⟩

/--
Once a bridge map is surjective, a downstream deterministic translator is
uniquely determined by its values before the bridge ends.
-/
theorem deterministicTranslator_unique
    (q : T →ₗ[𝕜] R) (hq : Function.Surjective q)
    (a b : R →ₗ[𝕜] A) (h : a.comp q = b.comp q) :
    a = b := by
  ext y
  obtain ⟨x, rfl⟩ := hq y
  exact congrArg (fun f : T →ₗ[𝕜] A => f x) h

/-- Every nonzero hidden direction admits one scalar probe that separates its line. -/
theorem oneScalarProbe_separatesHiddenLine (w : T) (hw : w ≠ 0) :
    ∃ σ : Module.Dual 𝕜 T,
      σ w = 1 ∧ ∀ c d : 𝕜, σ (c • w) = σ (d • w) → c = d := by
  obtain ⟨σ, hσ⟩ := Module.Projective.exists_dual_eq_one 𝕜 hw
  refine ⟨σ, hσ, ?_⟩
  intro c d hcd
  simpa only [map_smul, hσ, smul_eq_mul, mul_one] using hcd

/-- A scalar probe vanishing on a nonzero direction cannot separate that line. -/
theorem zeroProbe_notInjectiveOnHiddenLine
    (σ : Module.Dual 𝕜 T) (w : T) (_hw : w ≠ 0) (hσ : σ w = 0) :
    ¬ Function.Injective (fun c : 𝕜 => σ (c • w)) := by
  intro hinj
  have hzeroone : (0 : 𝕜) = 1 := hinj (by simp [hσ])
  exact zero_ne_one hzeroone

end Endpoint

section FourSectorAccount

variable {𝕜 T : Type*}
variable [Field 𝕜] [AddCommGroup T] [Module 𝕜 T]
variable [FiniteDimensional 𝕜 T]

/--
The four actual quotient sectors, rather than only their subtraction-defined
dimensions, account for the finite target.
-/
theorem fourSector_quotient_finrank (B K : Submodule 𝕜 T) :
    finrank 𝕜 ↥(B ⊓ K : Submodule 𝕜 T) +
        finrank 𝕜 (B ⧸ (B ⊓ K : Submodule 𝕜 T).comap B.subtype) +
        finrank 𝕜 (K ⧸ (B ⊓ K : Submodule 𝕜 T).comap K.subtype) +
        finrank 𝕜 (T ⧸ (B ⊔ K : Submodule 𝕜 T)) =
      finrank 𝕜 T := by
  have hCB :
      finrank 𝕜 ((B ⊓ K : Submodule 𝕜 T).comap B.subtype) =
        finrank 𝕜 ↥(B ⊓ K : Submodule 𝕜 T) :=
    (Submodule.comapSubtypeEquivOfLe
      (p := B ⊓ K) (q := B) inf_le_left).finrank_eq
  have hCK :
      finrank 𝕜 ((B ⊓ K : Submodule 𝕜 T).comap K.subtype) =
        finrank 𝕜 ↥(B ⊓ K : Submodule 𝕜 T) :=
    (Submodule.comapSubtypeEquivOfLe
      (p := B ⊓ K) (q := K) inf_le_right).finrank_eq
  have hB :
      finrank 𝕜 (B ⧸ (B ⊓ K : Submodule 𝕜 T).comap B.subtype) +
          finrank 𝕜 ((B ⊓ K : Submodule 𝕜 T).comap B.subtype) =
        finrank 𝕜 B :=
    Submodule.finrank_quotient_add_finrank
      ((B ⊓ K : Submodule 𝕜 T).comap B.subtype)
  have hK :
      finrank 𝕜 (K ⧸ (B ⊓ K : Submodule 𝕜 T).comap K.subtype) +
          finrank 𝕜 ((B ⊓ K : Submodule 𝕜 T).comap K.subtype) =
        finrank 𝕜 K :=
    Submodule.finrank_quotient_add_finrank
      ((B ⊓ K : Submodule 𝕜 T).comap K.subtype)
  have hT :
      finrank 𝕜 (T ⧸ (B ⊔ K : Submodule 𝕜 T)) +
          finrank 𝕜 ↥(B ⊔ K : Submodule 𝕜 T) =
        finrank 𝕜 T :=
    Submodule.finrank_quotient_add_finrank (B ⊔ K)
  have hSup :
      finrank 𝕜 ↥(B ⊔ K : Submodule 𝕜 T) +
          finrank 𝕜 ↥(B ⊓ K : Submodule 𝕜 T) =
        finrank 𝕜 B + finrank 𝕜 K :=
    Submodule.finrank_sup_add_finrank_inf_eq B K
  rw [hCB] at hB
  rw [hCK] at hK
  omega

end FourSectorAccount

end Bridge

#print axioms Bridge.dualCollisionSpace
#print axioms Bridge.quotientDualEquivDualCollision
#print axioms Bridge.generativeDefect_iff_dualCollision
#print axioms Bridge.readoutCollision_iff_differenceInKernel
#print axioms Bridge.appendedTrace_determines_iff
#print axioms Bridge.deterministicTranslator_unique
#print axioms Bridge.oneScalarProbe_separatesHiddenLine
#print axioms Bridge.zeroProbe_notInjectiveOnHiddenLine
#print axioms Bridge.fourSector_quotient_finrank
