import Experiments.BridgeFourSector

/-!
# BRIDGE v0.4 generated-span factorization

This file audits the first clause of P0195 directly.  The unrestricted
answer is a function on the generated sector `B`; the readout is the actual
restriction `r.comp B.subtype`, with codomain restricted to its reachable
range.  The linear kernel criterion is recorded separately.
-/

namespace Experiments.BridgeGeneratedRecovery

noncomputable section

variable {k T R A : Type*} [Field k]
variable [AddCommGroup T] [Module k T]
variable [AddCommGroup R] [Module k R]
variable [AddCommGroup A] [Module k A]

open Experiments

abbrev generatedRangeReadout (B : Submodule k T) (r : T →ₗ[k] R) :
    B →ₗ[k] LinearMap.range (r.comp B.subtype) :=
  (r.comp B.subtype).rangeRestrict

theorem generated_decoder_unique {Q : Type*} (B : Submodule k T) (r : T →ₗ[k] R)
    (a : B → Q) (d₁ d₂ : LinearMap.range (r.comp B.subtype) → Q)
    (h₁ : d₁ ∘ generatedRangeReadout B r = a)
    (h₂ : d₂ ∘ generatedRangeReadout B r = a) : d₁ = d₂ := by
  funext z
  obtain ⟨x, hx⟩ := z.property
  have hz : generatedRangeReadout B r x = z := by
    apply Subtype.ext
    exact hx
  calc
    d₁ z = d₁ (generatedRangeReadout B r x) := by rw [hz]
    _ = a x := congrFun h₁ x
    _ = d₂ (generatedRangeReadout B r x) := (congrFun h₂ x).symm
    _ = d₂ z := by rw [hz]

def generatedAmbientReadout (B : Submodule k T) (r : T →ₗ[k] R) : B →ₗ[k] R :=
  r.comp B.subtype

theorem generated_answer_decodable_iff {Q : Type*} (B : Submodule k T) (r : T →ₗ[k] R)
    (a : B → Q) :
    (∃ d : LinearMap.range (r.comp B.subtype) → Q,
      d ∘ generatedRangeReadout B r = a) ↔
      ∀ x y : B, generatedRangeReadout B r x = generatedRangeReadout B r y →
        a x = a y := by
  constructor
  · rintro ⟨d, hd⟩ x y hxy
    rw [← congrFun hd x, ← congrFun hd y]
    exact congrArg d hxy
  · intro h
    let d : LinearMap.range (r.comp B.subtype) → Q := fun z =>
      a (Classical.choose z.property)
    refine ⟨d, ?_⟩
    funext x
    apply h
    exact Subtype.ext (Classical.choose_spec (generatedRangeReadout B r x).property)

theorem generated_answer_decodable_iff_fiber {Q : Type*} (B : Submodule k T)
    (r : T →ₗ[k] R) (a : B → Q) :
    (∃ d : LinearMap.range (r.comp B.subtype) → Q,
      d ∘ generatedRangeReadout B r = a) ↔
      ∀ x y : B, r x.1 = r y.1 → a x = a y := by
  rw [generated_answer_decodable_iff]
  constructor
  · intro h x y hxy
    apply h
    exact Subtype.ext hxy
  · intro h x y hxy
    apply h x y
    exact congrArg Subtype.val hxy

theorem generated_linear_answer_decodable_iff (B : Submodule k T)
    (r : T →ₗ[k] R) (a : B →ₗ[k] A) :
    (∃ d : LinearMap.range (r.comp B.subtype) →ₗ[k] A,
      d.comp (generatedRangeReadout B r) = a) ↔
      BridgeFourSector.generatedCollision B r.ker ≤ a.ker := by
  let q : B →ₗ[k] R := r.comp B.subtype
  rw [show generatedRangeReadout B r = q.rangeRestrict by rfl]
  constructor
  · rintro ⟨d, hd⟩ x hx
    have hzero : q x = 0 := by
      rw [show q = r.comp B.subtype by rfl]
      apply LinearMap.mem_ker.mp
      simpa [BridgeFourSector.generatedCollision, q] using hx
    have hread : q.rangeRestrict x = 0 := by
      apply Subtype.ext
      exact hzero
    have hdx : d (q.rangeRestrict x) = a x := by
      simpa only [LinearMap.comp_apply] using LinearMap.congr_fun hd x
    calc
      a x = d (q.rangeRestrict x) := hdx.symm
      _ = d 0 := by rw [hread]
      _ = 0 := map_zero d
  · intro h
    have hC : BridgeFourSector.generatedCollision B r.ker = q.ker := by
      rw [BridgeFourSector.ker_readoutOnGenerated]
    rw [hC] at h
    let d : LinearMap.range q →ₗ[k] A :=
      (q.ker.liftQ a h).comp q.quotKerEquivRange.symm.toLinearMap
    refine ⟨d, ?_⟩
    apply LinearMap.ext
    intro x
    change (q.ker.liftQ a h)
      (q.quotKerEquivRange.symm (q.rangeRestrict x)) = a x
    have he : q.quotKerEquivRange (Submodule.Quotient.mk x) = q.rangeRestrict x := by
      apply Subtype.ext
      exact LinearMap.quotKerEquivRange_apply_mk q x
    rw [← he, q.quotKerEquivRange.symm_apply_apply]
    simp

theorem generated_identity_decoder_iff_injective (B : Submodule k T)
    (r : T →ₗ[k] R) :
    (∃ d : LinearMap.range (r.comp B.subtype) →ₗ[k] B,
      d.comp (generatedRangeReadout B r) = LinearMap.id) ↔
      Function.Injective (generatedRangeReadout B r) := by
  constructor
  · rintro ⟨d, hd⟩ x y hxy
    calc
      x = (LinearMap.id : B →ₗ[k] B) x := rfl
      _ = d (generatedRangeReadout B r x) := by
        simpa using (LinearMap.congr_fun hd x).symm
      _ = d (generatedRangeReadout B r y) := by rw [hxy]
      _ = (LinearMap.id : B →ₗ[k] B) y := by
        simpa using LinearMap.congr_fun hd y
      _ = y := rfl
  · intro hinj
    apply (generated_linear_answer_decodable_iff B r (LinearMap.id)).mpr
    rw [show (LinearMap.id : B →ₗ[k] B).ker = ⊥ by simp]
    rw [show BridgeFourSector.generatedCollision B r.ker = (r.comp B.subtype).ker by
      symm
      exact BridgeFourSector.ker_readoutOnGenerated B r]
    simpa [generatedRangeReadout] using (LinearMap.ker_eq_bot.mpr hinj).le

theorem generated_full_identity_iff_collision_bot (B : Submodule k T)
    (r : T →ₗ[k] R) :
    Function.Injective (generatedRangeReadout B r) ↔
      BridgeFourSector.generatedCollision B r.ker = ⊥ := by
  rw [← LinearMap.ker_eq_bot]
  rw [show (generatedRangeReadout B r).ker = (r.comp B.subtype).ker by
    ext x
    simp [generatedRangeReadout]]
  rw [← BridgeFourSector.ker_readoutOnGenerated B r]

/-- The identity criterion also holds when the decoder is merely a function. -/
theorem generated_identity_answer_decodable_iff_collision_bot (B : Submodule k T)
    (r : T →ₗ[k] R) :
    (∃ d : LinearMap.range (r.comp B.subtype) → B,
      d ∘ generatedRangeReadout B r = id) ↔
      BridgeFourSector.generatedCollision B r.ker = ⊥ := by
  rw [generated_answer_decodable_iff]
  exact generated_full_identity_iff_collision_bot B r

theorem generated_coarser_answer_countercase :
    let B : Submodule ℚ (ℚ × ℚ) := ⊤
    let r : (ℚ × ℚ) →ₗ[ℚ] ℚ := LinearMap.fst ℚ ℚ ℚ
    let a : B → ℚ := fun x => x.1.1
    (∃ d : LinearMap.range (r.comp B.subtype) → ℚ,
      d ∘ generatedRangeReadout B r = a) ∧
      ¬ Function.Injective (generatedRangeReadout B r) := by
  dsimp
  constructor
  · apply (generated_answer_decodable_iff_fiber
      (⊤ : Submodule ℚ (ℚ × ℚ)) (LinearMap.fst ℚ ℚ ℚ)
      (fun x : (⊤ : Submodule ℚ (ℚ × ℚ)) => x.1.1)).mpr
    intro x y hxy
    exact hxy
  · intro hinj
    have hxy : generatedRangeReadout
        (⊤ : Submodule ℚ (ℚ × ℚ)) (LinearMap.fst ℚ ℚ ℚ) ⟨(0, 0), by simp⟩ =
        generatedRangeReadout
        (⊤ : Submodule ℚ (ℚ × ℚ)) (LinearMap.fst ℚ ℚ ℚ) ⟨(0, 1), by simp⟩ := by
      apply Subtype.ext
      rfl
    have := hinj hxy
    have hzero : (0 : ℚ) = 1 := by simpa using congrArg (fun x => x.1.2) this
    norm_num at hzero

theorem generated_nonlinear_kernel_overclaim_countercase :
    let B : Submodule ℚ (ℚ × ℚ) := ⊤
    let r : (ℚ × ℚ) →ₗ[ℚ] ℚ := LinearMap.fst ℚ ℚ ℚ
    let a : B → ℚ := fun x => x.1.1 * x.1.2
    (∀ c : B, c ∈ BridgeFourSector.generatedCollision B r.ker → a c = a 0) ∧
      ¬ (∃ d : LinearMap.range (r.comp B.subtype) → ℚ,
        d ∘ generatedRangeReadout B r = a) := by
  dsimp
  constructor
  · intro c hc
    have hc0 : c.1.1 = 0 := by
      simpa [BridgeFourSector.generatedCollision] using hc
    simp [hc0]
  · intro h
    rcases (generated_answer_decodable_iff_fiber
      (⊤ : Submodule ℚ (ℚ × ℚ)) (LinearMap.fst ℚ ℚ ℚ)
      (fun x : (⊤ : Submodule ℚ (ℚ × ℚ)) => x.1.1 * x.1.2)).mp h with hfiber
    have heq : generatedRangeReadout
        (⊤ : Submodule ℚ (ℚ × ℚ)) (LinearMap.fst ℚ ℚ ℚ) ⟨(1, 0), by simp⟩ =
        generatedRangeReadout
        (⊤ : Submodule ℚ (ℚ × ℚ)) (LinearMap.fst ℚ ℚ ℚ) ⟨(1, 1), by simp⟩ := by
      apply Subtype.ext
      rfl
    have hv := hfiber ⟨(1, 0), by simp⟩ ⟨(1, 1), by simp⟩
      (congrArg Subtype.val heq)
    norm_num at hv

theorem generated_ambient_decoder_nonunique_countercase :
    let B : Submodule ℚ (ℚ × ℚ) := ⊤
    let r : (ℚ × ℚ) →ₗ[ℚ] (ℚ × ℚ) :=
      LinearMap.prod (LinearMap.fst ℚ ℚ ℚ) (0 : (ℚ × ℚ) →ₗ[ℚ] ℚ)
    let a : B → ℚ := fun x => x.1.1
    let d₁ : (ℚ × ℚ) → ℚ := fun z => z.1
    let d₂ : (ℚ × ℚ) → ℚ := fun z => z.1 + z.2
    (d₁ ∘ generatedAmbientReadout B r = a) ∧
      (d₂ ∘ generatedAmbientReadout B r = a) ∧ d₁ ≠ d₂ := by
  dsimp [generatedAmbientReadout]
  constructor
  · funext x
    rfl
  constructor
  · funext x
    simp
  · intro heq
    have := congrFun heq (0, 1)
    norm_num at this

end

end Experiments.BridgeGeneratedRecovery
