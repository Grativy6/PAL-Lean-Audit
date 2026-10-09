import Experiments.SingleCutSpan

namespace Experiments.SingleCutCorridor
open Finset Experiments.SingleCutSpan

theorem filled_corridor_invariant (e c d : ℕ) (u : Finset ℕ) (hu : u.Nonempty) :
    charge (serial e c u) = charge (serial e d u) := by
  rw [exact_endpoint_decomposition e c u hu, exact_endpoint_decomposition e d u hu]

theorem corridor_permutation (e c : ℕ) (p : Equiv.Perm (Fin (c+1))) :
    (univ.image (fun i : Fin (c+1) => e+1+(p i).val)) = Icc (e+1) (e+c+1) := by
  ext x
  simp only [mem_image, mem_univ, true_and, mem_Icc]
  constructor
  · rintro ⟨i, rfl⟩
    have := (p i).isLt
    omega
  · rintro ⟨hl, hr⟩
    have hx : x-(e+1) < c+1 := by omega
    refine ⟨p.symm ⟨x-(e+1), hx⟩, ?_⟩
    simp only [Equiv.apply_symm_apply]
    omega

theorem unit_admissible_iff (e c : ℕ) (he : e ≤ 1) (u : Finset ℕ) (hu : u.Nonempty) :
    charge (serial e c u) ≤ 1 ↔ u.max' hu+1-u.card ≤ 1-e := by
  rw [exact_endpoint_decomposition e c u hu]
  omega

theorem valid_unused_capacity (e s : ℕ) (h : e+s ≤ 1) :
    e+s+(1-e-s) = 1 := by omega

theorem invalid_truncation_does_not_close : 1+1+(1-1-1 : ℕ) ≠ 1 := by decide

theorem zero_slack_iff_exact_prefix (u : Finset ℕ) (hu : u.Nonempty) :
    u.max' hu+1-u.card = 0 ↔ u = range (u.max' hu+1) := by
  have hs : u ⊆ range (u.max' hu+1) := by
    intro x hx; simp only [mem_range]; have := le_max' u x hx; omega
  have hc := prefix_card_le u hu
  constructor
  · intro h
    apply eq_of_subset_of_card_le hs
    rw [card_range]; omega
  · intro h
    have hh := congrArg card h
    rw [card_range] at hh
    omega

theorem one_slack_iff_prefix_bound (u : Finset ℕ) (hu : u.Nonempty) :
    u.max' hu+1-u.card ≤ 1 ↔ u ⊆ range (u.card+1) := by
  have hc := prefix_card_le u hu
  constructor
  · intro h x hx
    simp only [mem_range]
    have := le_max' u x hx
    omega
  · intro h
    have := h (max'_mem u hu)
    simp only [mem_range] at this
    omega

theorem erased_interior_adds_one (s : Finset ℕ) (hs : s.Nonempty) (k : ℕ)
    (hk : k ∈ s) (hl : s.min' hs < k) (hr : k < s.max' hs) :
    charge (s.erase k) = charge s + 1 := by
  have hmin : s.min' hs ∈ s.erase k := mem_erase.mpr ⟨ne_of_lt hl, min'_mem s hs⟩
  have hmax : s.max' hs ∈ s.erase k := mem_erase.mpr ⟨ne_of_gt hr, max'_mem s hs⟩
  have he : (s.erase k).Nonempty := ⟨_, hmin⟩
  have emin : (s.erase k).min' he = s.min' hs := by
    apply (min'_eq_iff _ _ _).2
    exact ⟨hmin, fun b hb => min'_le s b (mem_of_mem_erase hb)⟩
  have emax : (s.erase k).max' he = s.max' hs := by
    apply (max'_eq_iff _ _ _).2
    exact ⟨hmax, fun b hb => le_max' s b (mem_of_mem_erase hb)⟩
  have hc : s.card ≤ s.max' hs-s.min' hs+1 := by
    have := card_le_card (support_subset_hull s)
    simp only [hull, dif_pos hs, Nat.card_Icc] at this
    have := min'_le_max' s hs
    omega
  have hp : 0 < s.card := card_pos.mpr hs
  rw [span_identity _ he, emin, emax, card_erase_of_mem hk, span_identity _ hs]
  omega

theorem inserted_corridor_puncture (e c : ℕ) (u : Finset ℕ) (hu : u.Nonempty) :
    charge ((serial e (c+1) u).erase (e+1)) = charge (serial e c u)+1 := by
  rw [erased_interior_adds_one _ (serial_nonempty _ _ _) (e+1)]
  · rw [filled_corridor_invariant e (c+1) c u hu]
  · simp [serial]
  · rw [serial_min]; omega
  · rw [serial_max e (c+1) u hu]; omega

theorem zero_slack_accepts_both (c : ℕ) :
    charge (serial 0 c {0}) ≤ 1 ∧ charge (serial 1 c {0}) ≤ 1 := by
  constructor <;> rw [exact_endpoint_decomposition _ c {0} (singleton_nonempty 0)] <;> simp

theorem full_target_has_no_slack (e c q : ℕ) :
    charge (serial e c (range (q+1))) = e := by
  have h : (range (q+1)).Nonempty := ⟨0, by simp⟩
  rw [exact_endpoint_decomposition e c _ h, card_range]
  have hm : (range (q+1)).max' h = q := by
    apply (max'_eq_iff _ _ _).2
    simp only [mem_range]
    exact ⟨by omega, fun b hb => by omega⟩
  simp [hm]

theorem slack_cannot_decode_orientation : ¬ ∃ decode : ℕ → Bool,
    decode 0 = false ∧ decode 0 = true := by
  rintro ⟨decode, hf, ht⟩
  have : (false : Bool) = true := hf.symm.trans ht
  cases this

theorem orientation_is_load_bearing (c : ℕ) :
    charge (serial 0 c {0}) ≠ charge (serial 1 c {0}) := by
  rw [exact_endpoint_decomposition _ c {0} (singleton_nonempty 0),
      exact_endpoint_decomposition _ c {0} (singleton_nonempty 0)]
  simp

theorem puncture_changes_feasibility :
    charge (serial 1 0 {0}) ≤ 1 ∧ ¬ charge ((serial 1 1 {0}).erase 2) ≤ 1 := by
  rw [inserted_corridor_puncture 1 0 {0} (singleton_nonempty 0)]
  rw [exact_endpoint_decomposition 1 0 {0} (singleton_nonempty 0)]
  simp

theorem separate_occurrence_budgets {I : Type*} (e s : I → ℕ)
    (valid : ∀ i, e i+s i ≤ 1) : ∀ i, e i+s i+(1-e i-s i) = 1 := by
  intro i; exact valid_unused_capacity _ _ (valid i)

end Experiments.SingleCutCorridor
