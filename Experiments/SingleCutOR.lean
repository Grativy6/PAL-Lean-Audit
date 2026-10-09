import Experiments.SingleCutSpan
import Mathlib.Data.List.Permutation

namespace Experiments.SingleCutOR
open Finset Experiments.SingleCutSpan

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def orders : List (List ℕ) := (List.range 7).permutations'

def positions (p : List ℕ) (row : Finset ℕ) : Finset ℕ := row.image p.idxOf

def prefixSlack (p : List ℕ) (row : Finset ℕ) : ℕ :=
  (positions p row).sup (fun j => j+1) - row.card

theorem positions_card (p : List ℕ) (row : Finset ℕ)
    (hp : p.Perm (List.range 7)) (hr : ∀ x ∈ row, x < 7) :
    (positions p row).card = row.card := by
  apply card_image_iff.mpr
  intro a ha b hb he
  exact (List.idxOf_inj (hp.mem_iff.mpr (List.mem_range.mpr (hr a ha)))).mp he

theorem prefixSlack_counts_missing (p : List ℕ) (row : Finset ℕ)
    (hp : p.Perm (List.range 7)) (hr : ∀ x ∈ row, x < 7) :
    prefixSlack p row =
      ((range ((positions p row).sup (fun j => j+1))) \ positions p row).card := by
  have hs : positions p row ⊆ range ((positions p row).sup (fun j => j+1)) := by
    intro x hx
    simp only [mem_range]
    have : x+1 ≤ (positions p row).sup (fun j => j+1) := le_sup hx
    omega
  rw [card_sdiff_of_subset hs, card_range, positions_card p row hp hr]
  rfl

def viable (p : List ℕ) (a b c : Bool) : Bool := decide (
  charge (positions p {0,1,2}) ≤ 1 ∧
  charge (positions p {3,4}) ≤ 1 ∧
  charge (positions p {1,2,4,6}) ≤ 1 ∧
  prefixSlack p {0} ≤ (if a then 1 else 0) ∧
  prefixSlack p {0,1,2,3,4} ≤ (if b then 1 else 0) ∧
  prefixSlack p {0,1,2,3,4,5} ≤ (if c then 1 else 0))

def accepted (a b c : Bool) : Bool := orders.any (fun p => viable p a b c)

theorem enumerator_length : orders.length = 5040 := by
  change (List.range 7).permutations'.length = 5040
  rw [← (List.permutations_perm_permutations' (List.range 7)).length_eq]
  simp [List.length_permutations, Nat.factorial]

theorem enumerator_covers_exactly (p : List ℕ) : p ∈ orders ↔ p.Perm (List.range 7) := by
  exact List.mem_permutations'

theorem enumerator_has_no_duplicates : orders.Nodup :=
  (List.permutations_perm_permutations' _).nodup_iff.mp (List.nodup_permutations _ List.nodup_range)

theorem accepted_truth_table : ∀ a b c : Bool, accepted a b c = (a || b || c) := by
  decide +kernel

theorem local_OR (a b c : Bool) :
    (∃ p : List ℕ, p.Perm (List.range 7) ∧ viable p a b c = true) ↔
    (a || b || c) = true := by
  rw [← accepted_truth_table a b c]
  simp only [accepted, List.any_eq_true, enumerator_covers_exactly]

theorem supplied_witness_100 :
    [3,0,4,1,2,5,6] ∈ orders ∧ viable [3,0,4,1,2,5,6] true false false = true := by decide +kernel

theorem supplied_witness_010 :
    [0,5,1,2,3,4,6] ∈ orders ∧ viable [0,5,1,2,3,4,6] false true false = true := by decide +kernel

theorem supplied_witness_001 :
    [0,1,2,3,4,6,5] ∈ orders ∧ viable [0,1,2,3,4,6,5] false false true = true := by decide +kernel

end Experiments.SingleCutOR
