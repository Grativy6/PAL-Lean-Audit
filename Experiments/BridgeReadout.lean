import Experiments.BridgeFourSector

/-!
# BRIDGE v0.4 visible readout quotient

This bounded lane realizes the source's visible-sector comparison using the
actual induced readout map into `range r / r(B)`.  Here `r(B)` is represented
as the range of `r` restricted to `B`, so it is a submodule of `range r`.
-/

namespace Experiments.BridgeReadout

noncomputable section

variable {k T R : Type*} [Field k]
variable [AddCommGroup T] [Module k T]
variable [AddCommGroup R] [Module k R]

/-- The generated readout submodule, represented inside the full readout range. -/
def generatedReadout (B : Submodule k T) (r : T →ₗ[k] R) : Submodule k (LinearMap.range r) :=
  (r.rangeRestrict.domRestrict B).range

/-- The actual map `t ↦ [r(t)]` into `range r / r(B)`. -/
def rawReadoutToVisible (B : Submodule k T) (r : T →ₗ[k] R) :
    T →ₗ[k] ((LinearMap.range r) ⧸ generatedReadout B r) :=
  (generatedReadout B r).mkQ.comp r.rangeRestrict

/-- The readout map descended from the defect quotient `T / B`. -/
def residualReadout (B : Submodule k T) (r : T →ₗ[k] R) :
    Experiments.BridgeFourSector.defect B →ₗ[k] ((LinearMap.range r) ⧸ generatedReadout B r) :=
  B.liftQ (rawReadoutToVisible B r) (by
    intro b hb
    change (generatedReadout B r).mkQ (r.rangeRestrict b) = 0
    change r.rangeRestrict b ∈ (generatedReadout B r).mkQ.ker
    rw [Submodule.ker_mkQ]
    exact ⟨⟨b, hb⟩, rfl⟩)

theorem rawReadoutToVisible_surjective (B : Submodule k T) (r : T →ₗ[k] R) :
    Function.Surjective (rawReadoutToVisible B r) := by
  intro q
  obtain ⟨y, rfl⟩ := (generatedReadout B r).mkQ_surjective q
  rcases y.property with ⟨t, ht⟩
  refine ⟨t, ?_⟩
  have hty : r.rangeRestrict t = y := Subtype.ext ht
  rw [rawReadoutToVisible, LinearMap.comp_apply, hty]

theorem ker_rawReadoutToVisible (B : Submodule k T) (r : T →ₗ[k] R) :
    (rawReadoutToVisible B r).ker = B ⊔ r.ker := by
  ext t
  constructor
  · intro ht
    change (generatedReadout B r).mkQ (r.rangeRestrict t) = 0 at ht
    have hker : r.rangeRestrict t ∈ (generatedReadout B r).mkQ.ker := ht
    rw [Submodule.ker_mkQ] at hker
    have hmem : r.rangeRestrict t ∈ generatedReadout B r := hker
    rcases hmem with ⟨b, hb⟩
    refine (Submodule.mem_sup).mpr ⟨b.1, b.2, t - b.1, ?_, ?_⟩
    · change r (t - b.1) = 0
      rw [map_sub]
      have hr : r b.1 = r t := congrArg Subtype.val hb
      rw [hr, sub_self]
    · exact (sub_eq_iff_eq_add' (a := t) (b := b.1) (c := t - b.1)).mp rfl |>.symm
  · rintro ht
    rcases (Submodule.mem_sup.mp ht) with ⟨b, hb, z, hz, hsum⟩
    change (generatedReadout B r).mkQ (r.rangeRestrict t) = 0
    have hzero : (generatedReadout B r).mkQ (r.rangeRestrict b) = 0 := by
      change r.rangeRestrict b ∈ (generatedReadout B r).mkQ.ker
      rw [Submodule.ker_mkQ]
      exact ⟨⟨b, hb⟩, rfl⟩
    have hrz : r z = 0 := hz
    have : r t = r b := by
      rw [← hsum, map_add, hrz, add_zero]
    rw [show r.rangeRestrict t = r.rangeRestrict b by ext; exact this]
    exact hzero

/-- The canonical visible-sector comparison `T/(B + ker r) ≃ range(r)/r(B)`. -/
noncomputable def visibleEquivReadout (B : Submodule k T) (r : T →ₗ[k] R) :
    Experiments.BridgeFourSector.visible B r.ker ≃ₗ[k]
      ((LinearMap.range r) ⧸ generatedReadout B r) :=
  (Submodule.quotEquivOfEq _ _ (ker_rawReadoutToVisible B r).symm).trans
    ((rawReadoutToVisible B r).quotKerEquivRange.trans
      (LinearEquiv.ofTop _ (LinearMap.range_eq_top.mpr (rawReadoutToVisible_surjective B r))))

/-- The comparison sends the visible class of `t` to the actual class `[r(t)]`. -/
theorem visibleEquivReadout_apply_mk (B : Submodule k T) (r : T →ₗ[k] R) (t : T) :
    visibleEquivReadout B r (Submodule.Quotient.mk t) = rawReadoutToVisible B r t := by
  rfl

/-- The residual readout agrees with the canonical comparison after `defectToVisible`. -/
theorem residualReadout_compatibility (B : Submodule k T) (r : T →ₗ[k] R) :
    residualReadout B r = (visibleEquivReadout B r).toLinearMap.comp
      (Experiments.BridgeFourSector.defectToVisible B r.ker) := by
  ext x
  rfl

/-- A checked countercase: omitting `ker r` from the kernel formula is invalid. -/
theorem generated_directions_required_countercase :
    let B : Submodule ℚ (ℚ × ℚ) := ⊥
    let r : (ℚ × ℚ) →ₗ[ℚ] ℚ := LinearMap.fst ℚ ℚ ℚ
    ((0, 1) : ℚ × ℚ) ∈ (rawReadoutToVisible B r).ker ∧
      ((0, 1) : ℚ × ℚ) ∉ B := by
  dsimp
  constructor
  · rw [ker_rawReadoutToVisible]
    apply (Submodule.mem_sup).mpr
    refine ⟨0, by simp, (0, 1), ?_, by norm_num⟩
    norm_num
  · simp

/-- A checked countercase: omitting `B` from the kernel formula is invalid. -/
theorem generated_component_required_countercase :
    let B : Submodule ℚ ℚ := ⊤
    let r : ℚ →ₗ[ℚ] ℚ := LinearMap.id
    (1 : ℚ) ∈ (rawReadoutToVisible B r).ker ∧ (1 : ℚ) ∉ r.ker := by
  dsimp
  constructor
  · rw [ker_rawReadoutToVisible]
    exact (Submodule.mem_sup).mpr ⟨1, by simp, 0, by simp, by norm_num⟩
  · norm_num

end

end Experiments.BridgeReadout
