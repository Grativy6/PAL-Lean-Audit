import Mathlib.Algebra.Exact.Basic
import Mathlib.LinearAlgebra.Prod
import Mathlib.LinearAlgebra.Isomorphisms

/-!
# BRIDGE v0.4 four-sector endpoint calculus

This is a bounded translation of selected quotient maps in BRIDGE v0.4
P0108--P0199. It audits the residual sequence; top, middle, and left quotient
sequences; the right sequence after an explicit `B`/`K` exchange; and two
left squares. It does not claim the complete displayed 3x3 diagram, chosen
complements, frame morphisms, Hodge geometry, or source adoption.
-/

namespace Experiments.BridgeFourSector

noncomputable section

variable {k T R : Type*} [Field k]
variable [AddCommGroup T] [Module k T]
variable [AddCommGroup R] [Module k R]

/-- P0115: generated-and-invisible directions, represented inside `B`. -/
def generatedCollision (B K : Submodule k T) : Submodule k B := K.comap B.subtype

/-- P0121: ungenerated-and-invisible directions, represented inside `K`. -/
def hiddenCollision (B K : Submodule k T) : Submodule k K := B.comap K.subtype

/-- P0118: the generated-visible quotient. -/
abbrev generatedVisible (B K : Submodule k T) := B ⧸ generatedCollision B K

/-- P0121: the hidden quotient. -/
abbrev hidden (B K : Submodule k T) := K ⧸ hiddenCollision B K

/-- P0167: the total generative defect quotient. -/
abbrev defect (B : Submodule k T) := T ⧸ B

/-- P0124: the ungenerated-visible quotient. -/
abbrev visible (B K : Submodule k T) := T ⧸ (B ⊔ K)

/-- The inclusion of `K` followed by the quotient by `B`. -/
def hiddenRawToDefect (B K : Submodule k T) : K →ₗ[k] defect B :=
  B.mkQ.comp K.subtype

/-- The source's left-column inclusion from the intersection presentation into `K`. -/
def collisionToKernel (B K : Submodule k T) : generatedCollision B K →ₗ[k] K where
  toFun x := ⟨x.1.1, x.2⟩
  map_add' _ _ := rfl
  map_smul' _ _ := rfl

/-- The canonical map from `H` to `D`, well-defined because its collision maps to zero. -/
def hiddenToDefect (B K : Submodule k T) : hidden B K →ₗ[k] defect B :=
  (hiddenCollision B K).liftQ (hiddenRawToDefect B K) (by
    intro x hx
    change B.mkQ x.1 = 0
    simpa [hiddenCollision] using hx)

/-- The canonical quotient map from `D` to `V`. -/
def defectToVisible (B K : Submodule k T) : defect B →ₗ[k] visible B K :=
  B.liftQ (B ⊔ K).mkQ (by
    rw [Submodule.ker_mkQ]
    exact le_sup_left)

/-- Canonical transport from the swapped right-column quotient to the source order. -/
noncomputable def swappedVisibleEquiv (B K : Submodule k T) :
    visible K B ≃ₗ[k] visible B K :=
  Submodule.quotEquivOfEq _ _ (sup_comm K B)

/-- The source-ordered right-column map, after transport along `B ⊔ K = K ⊔ B`. -/
def rightColumnToVisible (B K : Submodule k T) : defect K →ₗ[k] visible B K :=
  (swappedVisibleEquiv B K).toLinearMap.comp (defectToVisible K B)

/-- P0192: the raw hidden-to-defect map has exactly the stated collision kernel. -/
theorem ker_hiddenRawToDefect (B K : Submodule k T) :
    (hiddenRawToDefect B K).ker = hiddenCollision B K := by
  rw [hiddenRawToDefect, LinearMap.ker_comp, Submodule.ker_mkQ]
  rfl

/-- P0192: quotienting by the collision makes the canonical hidden map injective. -/
theorem hiddenToDefect_injective (B K : Submodule k T) :
    Function.Injective (hiddenToDefect B K) := by
  rw [← LinearMap.ker_eq_bot]
  apply Submodule.ker_liftQ_eq_bot
  · rw [ker_hiddenRawToDefect]

/-- P0192: every visible quotient class has a representative from the defect quotient. -/
theorem defectToVisible_surjective (B K : Submodule k T) :
    Function.Surjective (defectToVisible B K) := by
  intro v
  obtain ⟨t, rfl⟩ := (B ⊔ K).mkQ_surjective v
  refine ⟨Submodule.Quotient.mk t, ?_⟩
  rfl

/-- P0126--P0192: the top quotient row is exact in its declared `B` realization. -/
theorem generated_row_exact (B K : Submodule k T) :
    Function.Exact (generatedCollision B K).subtype (generatedCollision B K).mkQ :=
  LinearMap.exact_subtype_mkQ (generatedCollision B K)

/-- P0126--P0192: the middle kernel quotient row is exact. -/
theorem kernel_row_exact (K : Submodule k T) :
    Function.Exact K.subtype K.mkQ :=
  LinearMap.exact_subtype_mkQ K

/-- P0126--P0192: the middle defect quotient column is exact. -/
theorem defect_column_exact (B : Submodule k T) :
    Function.Exact B.subtype B.mkQ :=
  LinearMap.exact_subtype_mkQ B

/-- P0126--P0192: the left column is exact in the two subtype presentations of `B∩K`. -/
theorem left_column_exact (B K : Submodule k T) :
    Function.Exact (collisionToKernel B K) (hiddenCollision B K).mkQ := by
  rw [LinearMap.exact_iff, Submodule.ker_mkQ]
  ext x
  constructor
  · intro hx
    let y : generatedCollision B K := ⟨⟨x.1, by simpa [hiddenCollision] using hx⟩, x.2⟩
    refine ⟨y, ?_⟩
    rfl
  · rintro ⟨y, rfl⟩
    exact y.1.property

/-- P0126--P0192: the upper-left inclusion square commutes. -/
theorem upper_left_square_commutes (B K : Submodule k T) :
    B.subtype.comp (generatedCollision B K).subtype =
      K.subtype.comp (collisionToKernel B K) := by
  ext x
  rfl

/-- P0126--P0192: quotienting `K` then mapping to `D` agrees with the raw map. -/
theorem lower_left_square_commutes (B K : Submodule k T) :
    (hiddenToDefect B K).comp (hiddenCollision B K).mkQ = hiddenRawToDefect B K := by
  ext x
  rfl

/-- P0190--P0192: the audited bottom residual sequence is exact. -/
theorem residual_exact (B K : Submodule k T) :
    Function.Exact (hiddenToDefect B K) (defectToVisible B K) := by
  rw [LinearMap.exact_iff, defectToVisible, Submodule.ker_liftQ,
    Submodule.ker_mkQ, hiddenToDefect, Submodule.range_liftQ,
    hiddenRawToDefect, LinearMap.range_comp, Submodule.range_subtype,
    Submodule.map_sup]
  simp

/-- P0126--P0192: the right column is the residual sequence with `B` and `K` exchanged. -/
theorem right_column_exact (B K : Submodule k T) :
    Function.Exact (hiddenToDefect K B) (rightColumnToVisible B K) :=
  (swappedVisibleEquiv B K).postcomp_exact_iff_exact.mpr (residual_exact K B)

/-- P0118: restricting the readout to `B` has the generated collision kernel. -/
theorem ker_readoutOnGenerated (B : Submodule k T) (r : T →ₗ[k] R) :
    (r.comp B.subtype).ker = generatedCollision B r.ker := by
  ext x
  simp [generatedCollision, LinearMap.ker_comp]

/-- P0118: first isomorphism theorem for the generated-visible sector. -/
noncomputable def generatedVisibleEquivRange (B : Submodule k T) (r : T →ₗ[k] R) :
    generatedVisible B r.ker ≃ₗ[k] LinearMap.range (r.comp B.subtype) :=
  (Submodule.quotEquivOfEq _ _ (ker_readoutOnGenerated B r).symm).trans
    (r.comp B.subtype).quotKerEquivRange

/-- A concrete two-coordinate countercase to a direct-complement reading. -/
theorem no_direct_complement_countercase :
    ¬ Disjoint (⊤ : Submodule ℚ (ℚ × ℚ)) ⊤ := by
  intro h
  have hv : ((1, 0) : ℚ × ℚ) ∈ (⊤ ⊓ ⊤ : Submodule ℚ (ℚ × ℚ)) := by simp
  have hz : ((1, 0) : ℚ × ℚ) ∈ (⊥ : Submodule ℚ (ℚ × ℚ)) := h.le_bot hv
  norm_num at hz

end

end Experiments.BridgeFourSector
