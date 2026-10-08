import Mathlib
import Experiments.BridgeRecovery
import Experiments.BridgeDimension

namespace FrontLean
open Module

noncomputable section
variable {k T R Q E : Type*} [Field k]
variable [AddCommGroup T] [Module k T] [AddCommGroup R] [Module k R]
variable [AddCommGroup Q] [Module k Q] [AddCommGroup E] [Module k E]

/-- Proposition 3B: the decoder is on the actual image, including zero spaces. -/
theorem linear_factorization (J : T →ₗ[k] R) (q : T →ₗ[k] Q) :
    (∃ d : J.range →ₗ[k] Q, d.comp J.rangeRestrict = q) ↔ J.ker ≤ q.ker := by
  constructor
  · rintro ⟨d, hd⟩ x hx
    have hz : J.rangeRestrict x = 0 := Subtype.ext hx
    change q x = 0
    rw [← LinearMap.congr_fun hd]
    simp [hz]
  · intro h
    refine ⟨(J.ker.liftQ q h).comp J.quotKerEquivRange.symm.toLinearMap, ?_⟩
    ext x
    change (J.ker.liftQ q h) (J.quotKerEquivRange.symm ⟨J x, J.mem_range_self x⟩) = q x
    rw [LinearMap.quotKerEquivRange_symm_apply_image]
    rfl

/-- Linear Proposition 5A: the joint map keeps its actual index labels. -/
theorem joint_kernel {ι : Type*} {V : ι → Type*}
    [∀ i, AddCommGroup (V i)] [∀ i, Module k (V i)] (J : ∀ i, T →ₗ[k] V i) :
    (LinearMap.pi J).ker = ⨅ i, (J i).ker := by
  ext x
  simp [LinearMap.mem_ker, funext_iff]

theorem kernel_refinement {ι : Type*} (J : ι → T →ₗ[k] R) (s t : Set ι) (h : s ⊆ t) :
    (⨅ i ∈ t, (J i).ker) ≤ ⨅ i ∈ s, (J i).ker := by
  exact le_iInf₂ (fun i hi => iInf₂_le_of_le i (h hi) le_rfl)

open Experiments.BridgeFourSector Experiments.BridgeReadout Experiments.BridgeRecovery

/-- Proposition 5D: the actual short exact sequence, specialized to any joint J. -/
theorem joint_residual_short_exact (B : Submodule k T) (J : T →ₗ[k] R) :
    Function.Injective (hiddenToDefect B J.ker) ∧
    Function.Exact (hiddenToDefect B J.ker) (residualReadout B J) ∧
    Function.Surjective (residualReadout B J) := by
  refine ⟨hiddenToDefect_injective B J.ker, ?_, residualReadout_surjective B J⟩
  rw [residualReadout_compatibility]
  exact LinearEquiv.postcomp_exact_iff_exact.mpr (residual_exact B J.ker)

/-- The inherited visible equivalence retains its actual quotient target. -/
def joint_visible_equiv (B : Submodule k T) (J : T →ₗ[k] R) :
    visible B J.ker ≃ₗ[k] residualTarget B J := visibleEquivReadout B J

theorem joint_sector_dimensions [FiniteDimensional k T] (B : Submodule k T)
    (J : T →ₗ[k] R) :
    finrank k (generatedCollision B J.ker) + finrank k (generatedVisible B J.ker) +
      finrank k (hidden B J.ker) + finrank k (visible B J.ker) = finrank k T :=
  Experiments.BridgeDimension.bridge_four_sector_finrank B J.ker

/-- Readout refinement compares quotients using the same generated baseline. -/
def visibleRefinement (B Ksmall Klarge : Submodule k T) (h : Ksmall ≤ Klarge) :
    visible B Ksmall →ₗ[k] visible B Klarge :=
  (B ⊔ Ksmall).mapQ (B ⊔ Klarge) LinearMap.id (by simpa using sup_le_sup_left h B)

theorem refinement_commutes (B Ksmall Klarge : Submodule k T) (h : Ksmall ≤ Klarge) :
    (visibleRefinement B Ksmall Klarge h).comp (defectToVisible B Ksmall) =
      defectToVisible B Klarge := by
  ext x
  rfl

/-- Proposition 5F, with a commuting map rather than an untyped quotient formula. -/
theorem quotient_update_iff (B : Submodule k T) (L : T →ₗ[k] T) :
    (∃ D : (T ⧸ B) →ₗ[k] (T ⧸ B), D.comp B.mkQ = B.mkQ.comp L) ↔
      ∀ x ∈ B, L x ∈ B := by
  constructor
  · rintro ⟨D, hD⟩ x hx
    have hh := LinearMap.congr_fun hD x
    have hz : B.mkQ x = 0 := (Submodule.Quotient.mk_eq_zero B).mpr hx
    have hL : B.mkQ (L x) = 0 := by simpa [hz] using hh.symm
    exact (Submodule.Quotient.mk_eq_zero B).mp hL
  · intro h
    refine ⟨B.liftQ (B.mkQ.comp L) ?_, ?_⟩
    · intro x hx
      exact (Submodule.Quotient.mk_eq_zero B).mpr (h x hx)
    · ext x
      simp

/-- Equation 20m; the second return is transported through the earlier update. -/
theorem transported_return (M : Module.End k T) (α : T) (i j : ℕ) :
    (M ^ (i + j)) α - α = ((M ^ i) α - α) + (M ^ i) ((M ^ j) α - α) := by
  rw [pow_add, Module.End.mul_apply, map_sub]
  abel

/-- Equation 20k covers state queries. Residual queries use the quotient as T. -/
theorem side_trace_decodable (J : T →ₗ[k] R) (q : T →ₗ[k] Q) (s : T →ₗ[k] E) :
    (∃ d : (J.prod s).range →ₗ[k] Q, d.comp (J.prod s).rangeRestrict = q) ↔
      J.ker ⊓ s.ker ≤ q.ker := by
  rw [linear_factorization, LinearMap.ker_prod]

/-- Rank comparison for a factorable query, in a finite-dimensional input space. -/
theorem query_rank_le [FiniteDimensional k T] (f : T →ₗ[k] R) (q : T →ₗ[k] Q)
    (h : f.ker ≤ q.ker) : finrank k q.range ≤ finrank k f.range := by
  have hker := Submodule.finrank_mono h
  have hf := f.finrank_range_add_finrank_ker
  have hq := q.finrank_range_add_finrank_ker
  omega

theorem side_trace_rank_lower_bound [FiniteDimensional k T]
    (J : T →ₗ[k] R) (q : T →ₗ[k] Q) (s : T →ₗ[k] E)
    (h : J.ker ⊓ s.ker ≤ q.ker) :
    finrank k (q.domRestrict J.ker).range ≤ finrank k s.range := by
  have hker : (s.domRestrict J.ker).ker ≤ (q.domRestrict J.ker).ker := by
    intro x hx
    exact h ⟨x.property, hx⟩
  exact (query_rank_le (s.domRestrict J.ker) (q.domRestrict J.ker) hker).trans
    (Submodule.finrank_mono (by rintro y ⟨x, rfl⟩; exact ⟨x.val, rfl⟩))

/-- Proposition 5E: an injection of the query image into E constructs an attaining trace.
    Extension is noncanonical; it provides no algorithm or acquisition-cost bound. -/
theorem minimum_side_trace [FiniteDimensional k T]
    (J : T →ₗ[k] R) (q : T →ₗ[k] Q)
    (e : (q.domRestrict J.ker).range →ₗ[k] E) (he : Function.Injective e) :
    ∃ s : T →ₗ[k] E, J.ker ⊓ s.ker ≤ q.ker ∧
      finrank k s.range = finrank k (q.domRestrict J.ker).range := by
  obtain ⟨a, ha⟩ := (q.domRestrict J.ker).rangeRestrict.exists_extend
  let s := e.comp a
  have h : J.ker ⊓ s.ker ≤ q.ker := by
    intro x hx
    let xK : J.ker := ⟨x, hx.1⟩
    have heq : a x = (q.domRestrict J.ker).rangeRestrict xK := LinearMap.congr_fun ha xK
    have hz : e (a x) = e 0 := by simpa [s] using hx.2
    have zero := he hz
    rw [heq] at zero
    exact congrArg Subtype.val zero
  refine ⟨s, h, le_antisymm ?_ (side_trace_rank_lower_bound J q s h)⟩
  have hle : s.range ≤ e.range := by
    rintro y ⟨x, rfl⟩
    exact ⟨a x, rfl⟩
  exact (Submodule.finrank_mono hle).trans_eq (LinearMap.finrank_range_of_inj he)

theorem side_trace_capacity [FiniteDimensional k T] [FiniteDimensional k E]
    (J : T →ₗ[k] R) (q : T →ₗ[k] Q) :
    (∃ s : T →ₗ[k] E, J.ker ⊓ s.ker ≤ q.ker) ↔
      finrank k (q.domRestrict J.ker).range ≤ finrank k E := by
  constructor
  · rintro ⟨s, hs⟩
    exact (side_trace_rank_lower_bound J q s hs).trans s.range.finrank_le
  · intro h
    obtain ⟨e, he⟩ := finrank_le_iff_exists_linearMap.mp h
    obtain ⟨s, hs, _⟩ := minimum_side_trace J q e he
    exact ⟨s, hs⟩

/-- The capacity criterion without assuming finite dimension of the side space.
    Capacity means an injective linear copy of the required finite query image. -/
theorem side_trace_capacity_injection [FiniteDimensional k T]
    (J : T →ₗ[k] R) (q : T →ₗ[k] Q) :
    (∃ s : T →ₗ[k] E, J.ker ⊓ s.ker ≤ q.ker) ↔
      ∃ e : (q.domRestrict J.ker).range →ₗ[k] E, Function.Injective e := by
  constructor
  · rintro ⟨s, hs⟩
    obtain ⟨e, he⟩ := finrank_le_iff_exists_linearMap.mp (side_trace_rank_lower_bound J q s hs)
    exact ⟨s.range.subtype.comp e, Subtype.val_injective.comp he⟩
  · rintro ⟨e, he⟩
    obtain ⟨s, hs, _⟩ := minimum_side_trace J q e he
    exact ⟨s, hs⟩

/-- For a residual query the hidden obstruction is the image of the named injection. -/
theorem residual_query_criterion (B : Submodule k T) (J : T →ₗ[k] R)
    (qD : defect B →ₗ[k] Q) (sD : defect B →ₗ[k] E) :
    (∃ d : ((residualReadout B J).prod sD).range →ₗ[k] Q,
      d.comp ((residualReadout B J).prod sD).rangeRestrict = qD) ↔
      (hiddenToDefect B J.ker).range ⊓ sD.ker ≤ qD.ker := by
  rw [side_trace_decodable, ker_residualReadout]

/-- The two ways of writing the residual debt have the same image, not merely a name. -/
theorem residual_debt_image (B : Submodule k T) (J : T →ₗ[k] R) (qD : defect B →ₗ[k] Q) :
    (qD.domRestrict (residualReadout B J).ker).range =
      (qD.comp (hiddenToDefect B J.ker)).range := by
  rw [ker_residualReadout]
  ext y
  constructor
  · rintro ⟨⟨x, z, hz⟩, hx⟩
    exact ⟨z, by simpa [hz] using hx⟩
  · rintro ⟨z, hz⟩
    exact ⟨⟨hiddenToDefect B J.ker z, z, rfl⟩, hz⟩

theorem residual_side_trace_capacity [FiniteDimensional k T] [FiniteDimensional k E]
    (B : Submodule k T) (J : T →ₗ[k] R) (qD : defect B →ₗ[k] Q) :
    (∃ sD : defect B →ₗ[k] E, (hiddenToDefect B J.ker).range ⊓ sD.ker ≤ qD.ker) ↔
      finrank k (qD.comp (hiddenToDefect B J.ker)).range ≤ finrank k E := by
  rw [← residual_debt_image]
  simpa only [ker_residualReadout] using side_trace_capacity (E := E) (residualReadout B J) qD

end
end FrontLean
