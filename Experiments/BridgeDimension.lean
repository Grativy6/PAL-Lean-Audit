import Experiments.BridgeReadout
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas

/-!
# BRIDGE v0.4 finite four-sector account

This module audits the finite-dimensional equality in BRIDGE v0.4 P0193--P0194
for the existing quotient-sector realization.  It adds a finite-dimensional
hypothesis explicitly; it does not supply a geometric interpretation, a
splitting, or source adoption.
-/

namespace Experiments.BridgeDimension

open Experiments.BridgeFourSector
open Module

noncomputable section

variable {k T : Type*} [Field k]
variable [AddCommGroup T] [Module k T]

/-- The collision subtype in `B` has the dimension of `B ∩ K`. -/
theorem generatedCollision_finrank (B K : Submodule k T) :
    finrank k (generatedCollision B K) = finrank k (B ⊓ K : Submodule k T) :=
  by
    have hEq : generatedCollision B K = (B ⊓ K).comap B.subtype := by
      ext x
      simp [generatedCollision]
    rw [hEq]
    exact
      (Submodule.comapSubtypeEquivOfLe (p := B ⊓ K) (q := B) inf_le_left).finrank_eq

/-- The collision subtype in `K` has the dimension of `B ∩ K`. -/
theorem hiddenCollision_finrank (B K : Submodule k T) :
    finrank k (hiddenCollision B K) = finrank k (B ⊓ K : Submodule k T) :=
  by
    have hEq : hiddenCollision B K = (B ⊓ K).comap K.subtype := by
      ext x
      simp [hiddenCollision]
    rw [hEq]
    exact
      (Submodule.comapSubtypeEquivOfLe (p := B ⊓ K) (q := K) inf_le_right).finrank_eq

/-- Rank-nullity for the generated-visible quotient. -/
theorem generatedVisible_finrank_add_collision [FiniteDimensional k T] (B K : Submodule k T) :
    finrank k (generatedVisible B K) + finrank k (generatedCollision B K) = finrank k B :=
  Submodule.finrank_quotient_add_finrank (generatedCollision B K)

/-- Rank-nullity for the hidden quotient. -/
theorem hidden_finrank_add_collision [FiniteDimensional k T] (B K : Submodule k T) :
    finrank k (hidden B K) + finrank k (hiddenCollision B K) = finrank k K :=
  Submodule.finrank_quotient_add_finrank (hiddenCollision B K)

/-- Rank-nullity for the visible quotient. -/
theorem visible_finrank_add_sup [FiniteDimensional k T] (B K : Submodule k T) :
    finrank k (visible B K) + finrank k (B ⊔ K : Submodule k T) = finrank k T :=
  Submodule.finrank_quotient_add_finrank (B ⊔ K)

/-- The finite-dimensional four-sector account stated in P0193--P0194. -/
theorem bridge_four_sector_finrank [FiniteDimensional k T] (B K : Submodule k T) :
    finrank k (generatedCollision B K) + finrank k (generatedVisible B K) +
        finrank k (hidden B K) + finrank k (visible B K) = finrank k T := by
  have hB := generatedVisible_finrank_add_collision B K
  have hK := hidden_finrank_add_collision B K
  have hV := visible_finrank_add_sup B K
  rw [generatedCollision_finrank] at hB ⊢
  rw [hiddenCollision_finrank] at hK
  have hSup := Submodule.finrank_sup_add_finrank_inf_eq B K
  omega

/-- Removing finite dimension makes the four-sector finrank equality false. -/
theorem four_sector_finrank_requires_finite_dimensional_countercase :
    let B : Submodule ℚ (ℚ × (ℕ →₀ ℚ)) := LinearMap.range (LinearMap.inl ℚ ℚ (ℕ →₀ ℚ))
    let K : Submodule ℚ (ℚ × (ℕ →₀ ℚ)) := ⊥
    ¬ (finrank ℚ (generatedCollision B K) + finrank ℚ (generatedVisible B K) +
        finrank ℚ (hidden B K) + finrank ℚ (visible B K) = finrank ℚ (ℚ × (ℕ →₀ ℚ))) := by
  dsimp
  let B : Submodule ℚ (ℚ × (ℕ →₀ ℚ)) := LinearMap.range (LinearMap.inl ℚ ℚ (ℕ →₀ ℚ))
  have hBker : B = (LinearMap.snd ℚ ℚ (ℕ →₀ ℚ)).ker := by
    ext x
    constructor
    · rintro ⟨a, rfl⟩
      simp
    · intro hx
      refine ⟨x.1, ?_⟩
      apply Prod.ext
      · rfl
      · simpa [LinearMap.mem_ker] using hx.symm
  have hBfinite : FiniteDimensional ℚ B := by
    exact (LinearEquiv.ofInjective (LinearMap.inl ℚ ℚ (ℕ →₀ ℚ))
      (by intro x y h; exact congrArg Prod.fst h)).finiteDimensional
  have hBfinrank : finrank ℚ B = 1 := by
    simpa using (LinearEquiv.ofInjective (LinearMap.inl ℚ ℚ (ℕ →₀ ℚ))
      (by intro x y h; exact congrArg Prod.fst h)).finrank_eq.symm
  have hTnot : ¬ FiniteDimensional ℚ (ℚ × (ℕ →₀ ℚ)) := by
    intro h
    have hW : FiniteDimensional ℚ (ℕ →₀ ℚ) :=
      FiniteDimensional.of_surjective (LinearMap.snd ℚ ℚ (ℕ →₀ ℚ)) (by
        intro w
        exact ⟨(0, w), rfl⟩)
    letI : FiniteDimensional ℚ (ℕ →₀ ℚ) := hW
    letI : Finite ℕ := Module.Finite.finite_basis (Finsupp.basisSingleOne (R := ℚ))
    exact Infinite.false (inferInstance : Infinite ℕ)
  have hVnot : ¬ FiniteDimensional ℚ ((ℚ × (ℕ →₀ ℚ)) ⧸ B) := by
    rw [hBker]
    intro h
    have hRange : FiniteDimensional ℚ (LinearMap.range (LinearMap.snd ℚ ℚ (ℕ →₀ ℚ))) :=
      (LinearMap.snd ℚ ℚ (ℕ →₀ ℚ)).quotKerEquivRange.finiteDimensional
    have hTop : (LinearMap.range (LinearMap.snd ℚ ℚ (ℕ →₀ ℚ))) = ⊤ :=
      LinearMap.range_eq_top.mpr (by
        intro w
        exact ⟨(0, w), rfl⟩)
    rw [hTop] at hRange
    letI : FiniteDimensional ℚ (⊤ : Submodule ℚ (ℕ →₀ ℚ)) := hRange
    have hFinsupp : FiniteDimensional ℚ (ℕ →₀ ℚ) :=
      (LinearEquiv.ofTop (⊤ : Submodule ℚ (ℕ →₀ ℚ)) rfl).finiteDimensional
    letI : FiniteDimensional ℚ (ℕ →₀ ℚ) := hFinsupp
    letI : Finite ℕ := Module.Finite.finite_basis (Finsupp.basisSingleOne (R := ℚ))
    exact Infinite.false (inferInstance : Infinite ℕ)
  have hC : generatedCollision B (⊥ : Submodule ℚ (ℚ × (ℕ →₀ ℚ))) = ⊥ := by
    ext x
    simp [generatedCollision]
  have hCfin : finrank ℚ (generatedCollision B (⊥ : Submodule ℚ (ℚ × (ℕ →₀ ℚ)))) = 0 := by
    simp [hC]
  have hGsum : finrank ℚ (generatedVisible B (⊥ : Submodule ℚ (ℚ × (ℕ →₀ ℚ)))) +
      finrank ℚ (generatedCollision B (⊥ : Submodule ℚ (ℚ × (ℕ →₀ ℚ)))) = finrank ℚ B :=
    Submodule.finrank_quotient_add_finrank (generatedCollision B (⊥ : Submodule ℚ (ℚ × (ℕ →₀ ℚ))))
  have hG : finrank ℚ (generatedVisible B (⊥ : Submodule ℚ (ℚ × (ℕ →₀ ℚ)))) = 1 := by
    omega
  have hHfin : finrank ℚ (BridgeFourSector.hidden B (⊥ : Submodule ℚ (ℚ × (ℕ →₀ ℚ)))) = 0 := by
    exact finrank_eq_zero_of_subsingleton ℚ (BridgeFourSector.hidden B (⊥ : Submodule ℚ (ℚ × (ℕ →₀ ℚ))))
  have hVnot' : ¬ FiniteDimensional ℚ (visible B (⊥ : Submodule ℚ (ℚ × (ℕ →₀ ℚ)))) := by
    intro h
    letI : FiniteDimensional ℚ (visible B (⊥ : Submodule ℚ (ℚ × (ℕ →₀ ℚ)))) := h
    apply hVnot
    exact (Submodule.quotEquivOfEq _ _ (by simp : B ⊔ (⊥ : Submodule ℚ (ℚ × (ℕ →₀ ℚ))) = B)).finiteDimensional
  rw [hCfin, hG, hHfin, Module.finrank_of_infinite_dimensional hVnot',
    Module.finrank_of_infinite_dimensional hTnot]
  omega

end

end Experiments.BridgeDimension
