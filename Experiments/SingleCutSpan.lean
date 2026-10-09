import Mathlib

namespace Experiments.SingleCutSpan
open Finset

def hull (s : Finset ℕ) : Finset ℕ :=
  if h : s.Nonempty then Icc (s.min' h) (s.max' h) else ∅

def charge (s : Finset ℕ) : ℕ := (hull s \ s).card

theorem support_subset_hull (s : Finset ℕ) : s ⊆ hull s := by
  intro x hx
  have h : s.Nonempty := ⟨x, hx⟩
  simp only [hull, dif_pos h, mem_Icc]
  exact ⟨min'_le s x hx, le_max' s x hx⟩

theorem span_identity (s : Finset ℕ) (h : s.Nonempty) :
    charge s = s.max' h - s.min' h + 1 - s.card := by
  have hm := min'_le s (s.max' h) (max'_mem s h)
  rw [charge, card_sdiff_of_subset (support_subset_hull s), hull, dif_pos h, Nat.card_Icc]
  omega

theorem empty_charge : charge ∅ = 0 := by simp [charge, hull]

theorem singleton_charge (x : ℕ) : charge {x} = 0 := by simp [charge, hull]

theorem one_defect_criterion (s : Finset ℕ) : charge s ≤ 1 ↔
    hull s \ s = ∅ ∨ ∃ x, hull s \ s = {x} := by
  rw [charge, card_le_one_iff_subset_singleton]
  constructor
  · rintro ⟨a, ha⟩
    by_cases h : (hull s \ s).Nonempty
    · right
      obtain ⟨b, hb⟩ := h
      have he : b = a := mem_singleton.mp (ha hb)
      exact ⟨a, Subset.antisymm ha (by simpa only [singleton_subset_iff, ← he] using hb)⟩
    · exact Or.inl (not_nonempty_iff_eq_empty.mp h)
  · rintro (h | ⟨a, h⟩)
    · exact ⟨0, by simp [h]⟩
    · exact ⟨a, by simp [h]⟩

def rankedSupport {V : Type*} [DecidableEq V] {n : ℕ}
    (order : V ≃ Fin n) (s : Finset V) : Finset ℕ := s.image (fun v => (order v).val)

theorem bijective_order_preserves_support_size {V : Type*} [DecidableEq V] {n : ℕ}
    (order : V ≃ Fin n) (s : Finset V) : (rankedSupport order s).card = s.card := by
  apply card_image_of_injective
  exact Fin.val_injective.comp order.injective

theorem hull_positions_realized {V : Type*} [DecidableEq V] {n : ℕ}
    (order : V ≃ Fin n) (s : Finset V) (x : ℕ)
    (hx : x ∈ hull (rankedSupport order s)) : ∃ v, (order v).val = x := by
  by_cases h : (rankedSupport order s).Nonempty
  · have hx' : x ≤ (rankedSupport order s).max' h := by
      simpa only [hull, dif_pos h, mem_Icc] using (mem_Icc.mp (by
        simpa only [hull, dif_pos h] using hx)).2
    obtain ⟨v, hv, he⟩ := mem_image.mp (max'_mem (rankedSupport order s) h)
    have hn : x < n := lt_of_le_of_lt (he ▸ hx') (order v).isLt
    exact ⟨order.symm ⟨x, hn⟩, by simp⟩
  · simp [hull, h] at hx

theorem single_hole_is_two_blocks (a k b : ℕ) (ha : a < k) (hb : k < b) :
    Icc a b \ {k} = Icc a (k-1) ∪ Icc (k+1) b := by
  ext x
  simp only [mem_sdiff, mem_Icc, mem_singleton, mem_union]
  omega

def serial (e c : ℕ) (u : Finset ℕ) : Finset ℕ :=
  ({0} ∪ Icc (e+1) (e+c+1)) ∪ u.image (fun j => e+c+2+j)

theorem serial_nonempty (e c : ℕ) (u : Finset ℕ) : (serial e c u).Nonempty := by
  exact ⟨0, by simp [serial]⟩

theorem serial_min (e c : ℕ) (u : Finset ℕ) :
    (serial e c u).min' (serial_nonempty e c u) = 0 := by
  apply Nat.eq_zero_of_le_zero
  exact min'_le _ 0 (by simp [serial])

theorem serial_max (e c : ℕ) (u : Finset ℕ) (hu : u.Nonempty) :
    (serial e c u).max' (serial_nonempty e c u) = e+c+2+u.max' hu := by
  apply le_antisymm
  · apply max'_le
    intro x hx
    simp only [serial, mem_union, mem_singleton, mem_Icc, mem_image] at hx
    rcases hx with ((rfl | ⟨_, hx⟩) | ⟨j, hj, rfl⟩)
    · omega
    · omega
    · have := le_max' u j hj; omega
  · exact le_max' _ _ (by simp [serial, mem_image, max'_mem])

theorem serial_card (e c : ℕ) (u : Finset ℕ) :
    (serial e c u).card = c+2+u.card := by
  have h₁ : Disjoint ({0} : Finset ℕ) (Icc (e+1) (e+c+1)) := by
    simp
  have h₂ : Disjoint ({0} ∪ Icc (e+1) (e+c+1)) (u.image (fun j => e+c+2+j)) := by
    rw [disjoint_left]
    intro x hx hy
    simp only [mem_union, mem_singleton, mem_Icc] at hx
    obtain ⟨j, hj, rfl⟩ := mem_image.mp hy
    omega
  rw [serial, card_union_of_disjoint h₂, card_union_of_disjoint h₁]
  rw [card_singleton, Nat.card_Icc,
    card_image_of_injective _ (show Function.Injective (fun j : ℕ => e+c+2+j) from
      fun _ _ h => Nat.add_left_cancel h)]
  omega

theorem prefix_card_le (u : Finset ℕ) (hu : u.Nonempty) : u.card ≤ u.max' hu + 1 := by
  calc
    u.card ≤ (range (u.max' hu + 1)).card := card_le_card (by
      intro x hx; simp only [mem_range]; have := le_max' u x hx; omega)
    _ = u.max' hu + 1 := card_range _

theorem exact_endpoint_decomposition (e c : ℕ) (u : Finset ℕ) (hu : u.Nonempty) :
    charge (serial e c u) = e + (u.max' hu + 1 - u.card) := by
  rw [span_identity _ (serial_nonempty e c u), serial_min, serial_max e c u hu, serial_card]
  have := prefix_card_le u hu
  omega

end Experiments.SingleCutSpan
