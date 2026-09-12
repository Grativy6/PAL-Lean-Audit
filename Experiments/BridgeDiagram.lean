import Experiments.BridgeFourSector

/-!
# BRIDGE v0.4 complete four-sector diagram

This module completes the displayed quotient diagram from BRIDGE v0.4
P0127--P0192 in the local submodule realization.  It is a formal audit of
the named maps only; it does not assert source adoption or a chosen splitting.
-/

namespace Experiments.BridgeDiagram

open Experiments.BridgeFourSector

noncomputable section

variable {k T : Type*} [Field k]
variable [AddCommGroup T] [Module k T]

/-- A bounded short-exactness package for two consecutive linear maps. -/
def ShortExact {X Y Z : Type*} [AddCommGroup X] [Module k X]
    [AddCommGroup Y] [Module k Y] [AddCommGroup Z] [Module k Z]
    (f : X →ₗ[k] Y) (g : Y →ₗ[k] Z) : Prop :=
  Function.Injective f ∧ Function.Exact f g ∧ Function.Surjective g

/-- The top-right vertical map: `B / (B ∩ K) → T / K`. -/
def generatedVisibleToKernelQuotient (B K : Submodule k T) :
    generatedVisible B K →ₗ[k] defect K :=
  (generatedCollision B K).liftQ (K.mkQ.comp B.subtype) (by
    intro x hx
    change K.mkQ x.1 = 0
    rw [← LinearMap.mem_ker, Submodule.ker_mkQ]
    exact hx)

/-- The top-left endpoint map is injective. -/
theorem collisionToKernel_injective (B K : Submodule k T) :
    Function.Injective (collisionToKernel B K) := by
  intro x y h
  apply Subtype.ext
  apply Subtype.ext
  exact congrArg (fun z : K => z.val) h

/-- The left-column quotient endpoint is surjective. -/
theorem hiddenCollision_mkQ_surjective (B K : Submodule k T) :
    Function.Surjective (hiddenCollision B K).mkQ :=
  (hiddenCollision B K).mkQ_surjective

/-- The middle-column inclusion endpoint is injective. -/
theorem B_subtype_injective (B : Submodule k T) :
    Function.Injective B.subtype := B.subtype_injective

/-- The middle-column quotient endpoint is surjective. -/
theorem B_mkQ_surjective (B : Submodule k T) :
    Function.Surjective B.mkQ := B.mkQ_surjective

/-- The top-right quotient endpoint is injective. -/
theorem generatedVisibleToKernelQuotient_injective (B K : Submodule k T) :
    Function.Injective (generatedVisibleToKernelQuotient B K) := by
  rw [← LinearMap.ker_eq_bot]
  apply Submodule.ker_liftQ_eq_bot
  rw [LinearMap.ker_comp, Submodule.ker_mkQ]
  rfl

/-- The source-ordered bottom endpoint is surjective. -/
theorem rightColumnToVisible_surjective (B K : Submodule k T) :
    Function.Surjective (rightColumnToVisible B K) := by
  intro v
  obtain ⟨d, hd⟩ := (defectToVisible_surjective (B := K) (K := B))
    ((swappedVisibleEquiv B K).symm v)
  exact ⟨d, by simpa [rightColumnToVisible] using congrArg (swappedVisibleEquiv B K) hd⟩

/-- The source-ordered right column is exact with its displayed `Gv` map. -/
theorem generatedVisible_right_column_exact (B K : Submodule k T) :
    Function.Exact (generatedVisibleToKernelQuotient B K) (rightColumnToVisible B K) := by
  change Function.Exact (hiddenToDefect K B) (rightColumnToVisible B K)
  exact right_column_exact B K

/-- The upper-right square is induced by the quotient of `B → T / K`. -/
theorem upper_right_square_commutes (B K : Submodule k T) :
    (generatedVisibleToKernelQuotient B K).comp (generatedCollision B K).mkQ =
      K.mkQ.comp B.subtype := by
  ext x
  rfl

/-- The lower-right square agrees after the explicit `B ⊔ K = K ⊔ B` transport. -/
theorem lower_right_square_commutes (B K : Submodule k T) :
    (rightColumnToVisible B K).comp K.mkQ =
      (defectToVisible B K).comp B.mkQ := by
  ext x
  rfl

/-- A commuting square alone does not entail exactness of its rows. -/
theorem commuting_square_not_exact_countercase :
    let z : ℚ →ₗ[ℚ] ℚ := 0
    z.comp z = z.comp z ∧ ¬ Function.Exact z z := by
  dsimp
  constructor
  · rfl
  · simp [LinearMap.exact_iff]

/-- Each displayed short exact sequence has its required endpoint map property. -/
theorem diagram_endpoint_maps (B K : Submodule k T) :
    Function.Injective (generatedCollision B K).subtype ∧
    Function.Surjective (generatedCollision B K).mkQ ∧
    Function.Injective K.subtype ∧ Function.Surjective K.mkQ ∧
    Function.Injective (hiddenToDefect B K) ∧
    Function.Surjective (defectToVisible B K) ∧
    Function.Injective (collisionToKernel B K) ∧
    Function.Surjective (hiddenCollision B K).mkQ ∧
    Function.Injective B.subtype ∧ Function.Surjective B.mkQ ∧
    Function.Injective (generatedVisibleToKernelQuotient B K) ∧
    Function.Surjective (rightColumnToVisible B K) := by
  exact ⟨(generatedCollision B K).subtype_injective,
    (generatedCollision B K).mkQ_surjective, K.subtype_injective, K.mkQ_surjective,
    hiddenToDefect_injective B K, defectToVisible_surjective B K,
    collisionToKernel_injective B K, hiddenCollision_mkQ_surjective B K,
    B_subtype_injective B, B_mkQ_surjective B,
    generatedVisibleToKernelQuotient_injective B K, rightColumnToVisible_surjective B K⟩

/-- The complete 3x3 audit: six short-exact sequences and four named squares. -/
theorem complete_diagram_certified (B K : Submodule k T) :
    ShortExact (generatedCollision B K).subtype (generatedCollision B K).mkQ ∧
    ShortExact K.subtype K.mkQ ∧
    ShortExact (hiddenToDefect B K) (defectToVisible B K) ∧
    ShortExact (collisionToKernel B K) (hiddenCollision B K).mkQ ∧
    ShortExact B.subtype B.mkQ ∧
    ShortExact (generatedVisibleToKernelQuotient B K) (rightColumnToVisible B K) ∧
    B.subtype.comp (generatedCollision B K).subtype =
      K.subtype.comp (collisionToKernel B K) ∧
    (hiddenToDefect B K).comp (hiddenCollision B K).mkQ = hiddenRawToDefect B K ∧
    (generatedVisibleToKernelQuotient B K).comp (generatedCollision B K).mkQ =
      K.mkQ.comp B.subtype ∧
    (rightColumnToVisible B K).comp K.mkQ =
      (defectToVisible B K).comp B.mkQ := by
  rcases diagram_endpoint_maps B K with
    ⟨hCinj, hGsurj, hKinj, hTKsurj, hHinj, hVsurj,
      hCtoKinj, hHsurj, hBinj, hDsurj, hGinj, hRsurj⟩
  exact ⟨⟨hCinj, generated_row_exact B K, hGsurj⟩,
    ⟨hKinj, kernel_row_exact K, hTKsurj⟩,
    ⟨hHinj, residual_exact B K, hVsurj⟩,
    ⟨hCtoKinj, left_column_exact B K, hHsurj⟩,
    ⟨hBinj, defect_column_exact B, hDsurj⟩,
    ⟨hGinj, generatedVisible_right_column_exact B K, hRsurj⟩,
    upper_left_square_commutes B K, lower_left_square_commutes B K,
    upper_right_square_commutes B K, lower_right_square_commutes B K⟩

end

end Experiments.BridgeDiagram
