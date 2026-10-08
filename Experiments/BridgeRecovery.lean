import Experiments.BridgeReadout

/-!
# BRIDGE v0.4 residual recovery

This bounded file formalizes P0195--P0199 in the declared linear realization.
The hidden quotient is used through its named injection into the defect quotient;
it is never identified with an ambient submodule by notation alone.
-/

namespace Experiments.BridgeRecovery

noncomputable section

variable {k T R A : Type*} [Field k]
variable [AddCommGroup T] [Module k T]
variable [AddCommGroup R] [Module k R]
variable [AddCommGroup A] [Module k A]

open Experiments

/-- P0196's actual residual target. -/
abbrev residualTarget (B : Submodule k T) (r : T →ₗ[k] R) :=
  (LinearMap.range r) ⧸ BridgeReadout.generatedReadout B r

/-- The residual map is surjective onto its declared target. -/
theorem residualReadout_surjective (B : Submodule k T) (r : T →ₗ[k] R) :
    Function.Surjective (BridgeReadout.residualReadout B r) := by
  rw [BridgeReadout.residualReadout_compatibility]
  exact (BridgeReadout.visibleEquivReadout B r).surjective.comp
    (BridgeFourSector.defectToVisible_surjective B r.ker)

/-- P0196--P0198: the kernel is the range of the named hidden-sector injection. -/
theorem ker_residualReadout (B : Submodule k T) (r : T →ₗ[k] R) :
    (BridgeReadout.residualReadout B r).ker =
      (BridgeFourSector.hiddenToDefect B r.ker).range := by
  rw [BridgeReadout.residualReadout_compatibility]
  have hexact : Function.Exact (BridgeFourSector.hiddenToDefect B r.ker)
      ((BridgeReadout.visibleEquivReadout B r).toLinearMap.comp
        (BridgeFourSector.defectToVisible B r.ker)) :=
    LinearEquiv.postcomp_exact_iff_exact.mpr
      (BridgeFourSector.residual_exact B r.ker)
  exact hexact.linearMap_ker_eq

/-- The canonical quotient equivalence used to descend decodable answers. -/
noncomputable def residualQuotientEquiv (B : Submodule k T) (r : T →ₗ[k] R) :
    (BridgeFourSector.defect B ⧸ (BridgeReadout.residualReadout B r).ker) ≃ₗ[k]
      residualTarget B r :=
  (BridgeReadout.residualReadout B r).quotKerEquivRange.trans
    (LinearEquiv.ofTop _ (LinearMap.range_eq_top.mpr (residualReadout_surjective B r)))

/-- A requested answer descends through the residual readout when it kills its kernel. -/
noncomputable def answerDecoder (B : Submodule k T) (r : T →ₗ[k] R)
    (a : BridgeFourSector.defect B →ₗ[k] A)
    (h : (BridgeReadout.residualReadout B r).ker ≤ a.ker) :
    residualTarget B r →ₗ[k] A :=
  ((BridgeReadout.residualReadout B r).ker).liftQ a h |>.comp
    (residualQuotientEquiv B r).symm.toLinearMap

theorem answerDecoder_comp_residualReadout (B : Submodule k T) (r : T →ₗ[k] R)
    (a : BridgeFourSector.defect B →ₗ[k] A)
    (h : (BridgeReadout.residualReadout B r).ker ≤ a.ker) :
    (answerDecoder B r a h).comp (BridgeReadout.residualReadout B r) = a := by
  apply LinearMap.ext
  rintro ⟨x⟩
  change ((BridgeReadout.residualReadout B r).ker).liftQ a h
    ((residualQuotientEquiv B r).symm
      (BridgeReadout.residualReadout B r (Submodule.Quotient.mk x))) =
      a (Submodule.Quotient.mk x)
  have he : residualQuotientEquiv B r
      (Submodule.Quotient.mk (Submodule.Quotient.mk x)) =
        BridgeReadout.residualReadout B r (Submodule.Quotient.mk x) := by
    simp [residualQuotientEquiv, LinearMap.quotKerEquivRange_apply_mk]
  rw [← he, (residualQuotientEquiv B r).symm_apply_apply]
  simp

/-- P0197--P0198: an answer is endpoint-decodable exactly when it kills hidden directions. -/
theorem answer_decodable_iff (B : Submodule k T) (r : T →ₗ[k] R)
    (a : BridgeFourSector.defect B →ₗ[k] A) :
    (∃ d : residualTarget B r →ₗ[k] A,
      d.comp (BridgeReadout.residualReadout B r) = a) ↔
      (BridgeFourSector.hiddenToDefect B r.ker).range ≤ a.ker := by
  constructor
  · rintro ⟨d, hd⟩ y hy
    rcases hy with ⟨x, rfl⟩
    change a (BridgeFourSector.hiddenToDefect B r.ker x) = 0
    rw [← LinearMap.congr_fun hd]
    have hz : BridgeReadout.residualReadout B r
        (BridgeFourSector.hiddenToDefect B r.ker x) = 0 := by
      change (BridgeFourSector.hiddenToDefect B r.ker x) ∈
        (BridgeReadout.residualReadout B r).ker
      rw [ker_residualReadout]
      exact ⟨x, rfl⟩
    simp [hz]
  · intro h
    refine ⟨answerDecoder B r a ?_, answerDecoder_comp_residualReadout B r a ?_⟩
    · rw [ker_residualReadout]
      exact h
    · rw [ker_residualReadout]
      exact h

/-- P0199 stated as an actual left-inverse decoder for residual identity. -/
theorem residual_identity_decoder_iff_injective (B : Submodule k T)
    (r : T →ₗ[k] R) :
    (∃ d : residualTarget B r →ₗ[k] BridgeFourSector.defect B,
      d.comp (BridgeReadout.residualReadout B r) = LinearMap.id) ↔
      Function.Injective (BridgeReadout.residualReadout B r) := by
  constructor
  · rintro ⟨d, hd⟩ x y hxy
    let ident : BridgeFourSector.defect B →ₗ[k] BridgeFourSector.defect B := LinearMap.id
    calc
      x = ident x := rfl
      _ = d (BridgeReadout.residualReadout B r x) := by
        simpa [ident] using (LinearMap.congr_fun hd x).symm
      _ = d (BridgeReadout.residualReadout B r y) := by rw [hxy]
      _ = ident y := by simpa [ident] using LinearMap.congr_fun hd y
      _ = y := rfl
  · intro hinj
    have hker : (BridgeReadout.residualReadout B r).ker ≤
        (LinearMap.id : BridgeFourSector.defect B →ₗ[k] BridgeFourSector.defect B).ker := by
      intro x hx
      rw [LinearMap.ker_eq_bot.mpr hinj] at hx
      simpa using hx
    exact ⟨answerDecoder B r LinearMap.id hker,
      answerDecoder_comp_residualReadout B r LinearMap.id hker⟩

/-- The named hidden injection makes subsingleton hidden sector equivalent to full recovery. -/
theorem full_residual_identity_recovery_iff_hidden_subsingleton (B : Submodule k T)
    (r : T →ₗ[k] R) :
    Function.Injective (BridgeReadout.residualReadout B r) ↔
      Subsingleton (BridgeFourSector.hidden B r.ker) := by
  constructor
  · intro hinj
    constructor
    intro x y
    apply BridgeFourSector.hiddenToDefect_injective B r.ker
    apply hinj
    have hz (z : BridgeFourSector.hidden B r.ker) :
        BridgeReadout.residualReadout B r (BridgeFourSector.hiddenToDefect B r.ker z) = 0 := by
      change (BridgeFourSector.hiddenToDefect B r.ker z) ∈
        (BridgeReadout.residualReadout B r).ker
      rw [ker_residualReadout]
      exact ⟨z, rfl⟩
    rw [hz x, hz y]
  · intro h
    apply LinearMap.ker_eq_bot.mp
    rw [ker_residualReadout]
    apply bot_unique
    intro x hx
    rcases hx with ⟨y, rfl⟩
    have hy : y = 0 := Subsingleton.elim _ _
    simp [hy]

/-- P0199: full recovery occurs exactly when the supplied kernel lies in the generated sector. -/
theorem full_residual_identity_recovery_iff_kernel_le (B : Submodule k T)
    (r : T →ₗ[k] R) :
    Function.Injective (BridgeReadout.residualReadout B r) ↔ r.ker ≤ B := by
  constructor
  · intro h x hx
    have hq : Subsingleton (BridgeFourSector.hidden B r.ker) :=
      full_residual_identity_recovery_iff_hidden_subsingleton B r |>.mp h
    have htop : BridgeFourSector.hiddenCollision B r.ker = ⊤ :=
      Submodule.Quotient.subsingleton_iff.mp hq
    have hmem : (⟨x, hx⟩ : r.ker) ∈ BridgeFourSector.hiddenCollision B r.ker := by
      rw [htop]
      simp
    exact hmem
  · intro h
    apply full_residual_identity_recovery_iff_hidden_subsingleton B r |>.mpr
    apply Submodule.Quotient.subsingleton_iff.mpr
    apply top_unique
    intro x hx
    change (x : T) ∈ B
    exact h x.property

/-- P0199 combines the explicit decoder criterion with the supplied-kernel criterion. -/
theorem residual_identity_decoder_iff_kernel_le (B : Submodule k T)
    (r : T →ₗ[k] R) :
    (∃ d : residualTarget B r →ₗ[k] BridgeFourSector.defect B,
      d.comp (BridgeReadout.residualReadout B r) = LinearMap.id) ↔ r.ker ≤ B :=
  residual_identity_decoder_iff_injective B r |>.trans
    (full_residual_identity_recovery_iff_kernel_le B r)

/-- A nondegenerate checked boundary case: first-coordinate answers decode although identity does not. -/
theorem coarser_answer_decodable_without_identity_countercase :
    let B : Submodule ℚ (ℚ × ℚ) := ⊥
    let r : (ℚ × ℚ) →ₗ[ℚ] ℚ := LinearMap.fst ℚ ℚ ℚ
    let a : BridgeFourSector.defect B →ₗ[ℚ] ℚ := B.liftQ r (by
      intro x hx
      change x ∈ (⊥ : Submodule ℚ (ℚ × ℚ)) at hx
      have hzero : x = 0 := by simpa using hx
      simp [hzero])
    (∃ d : residualTarget B r →ₗ[ℚ] ℚ,
      d.comp (BridgeReadout.residualReadout B r) = a) ∧
      ¬ Function.Injective (BridgeReadout.residualReadout B r) := by
  dsimp
  constructor
  · apply (answer_decodable_iff (A := ℚ)
      (⊥ : Submodule ℚ (ℚ × ℚ)) (LinearMap.fst ℚ ℚ ℚ)
      ((⊥ : Submodule ℚ (ℚ × ℚ)).liftQ (LinearMap.fst ℚ ℚ ℚ) (by
        intro x hx
        change x ∈ (⊥ : Submodule ℚ (ℚ × ℚ)) at hx
        have hzero : x = 0 := by simpa using hx
        simp [hzero]))).mpr
    intro z hz
    rcases hz with ⟨x, rfl⟩
    refine Submodule.Quotient.induction_on _ x (fun y => ?_)
    change LinearMap.fst ℚ ℚ ℚ y.1 = 0
    exact y.property
  · intro hinj
    have hle := full_residual_identity_recovery_iff_kernel_le
      (⊥ : Submodule ℚ (ℚ × ℚ)) (LinearMap.fst ℚ ℚ ℚ) |>.mp hinj
    have hmem : ((0, 1) : ℚ × ℚ) ∈ (LinearMap.fst ℚ ℚ ℚ).ker := by norm_num
    have := hle hmem
    norm_num at this

end

end Experiments.BridgeRecovery
