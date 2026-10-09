import Experiments.AbstractLoopsFiniteImage
import Mathlib.Tactic

namespace Experiments.FiniteAbstractionControls
open Experiments.AbstractLoopsJoint

theorem finite_prefix_does_not_cover (N : ℕ) :
    ∃ P : ℕ → Prop, (∀ n ≤ N, P n) ∧ ¬ ∀ n, P n := by
  refine ⟨fun n => n ≤ N, by simp, ?_⟩
  intro h
  have := h (N+1)
  omega

theorem finite_set_does_not_cover (tested : Finset ℕ) :
    ∃ P : ℕ → Prop, (∀ n ∈ tested, P n) ∧ ¬ ∀ n, P n := by
  refine ⟨fun n => n ≤ tested.sup id, ?_, ?_⟩
  · intro n hn; exact Finset.le_sup (f := id) hn
  · intro h; have := h (tested.sup id + 1); omega

theorem induction_has_unbounded_reach (n : ℕ) :
    ∑ i ∈ Finset.range n, (2*i+1) = n^2 := by
  induction n with
  | zero => simp
  | succ n ih => rw [Finset.sum_range_succ,ih]; ring

theorem pointwise_bounds_without_constant_bound :
    (∀ n : ℕ, ∃ b : ℕ, n < b) ∧ ¬ (∃ b : ℕ, ∀ n : ℕ, n < b) := by
  constructor
  · intro n; exact ⟨n+1,by omega⟩
  · rintro ⟨b,h⟩; exact (Nat.lt_irrefl b) (h b)

theorem a_uniform_construction_still_exists :
    ∃ f : ℕ → ℕ, ∀ n, n < f n := ⟨fun n => n+1,fun _ => Nat.lt_succ_self _⟩

theorem prefix_interface_loses_identity (N : ℕ) :
    ¬ Certifies (id : ℕ → ℕ) (fun n => min n N) := by
  intro h
  have hc := (reachable_certifies_iff_kernel_subset id (fun n => min n N)).mp h N (N+1)
  have he : min N N = min (N+1) N := by omega
  have := hc he
  simp only [id_eq] at this
  omega

def unaryRecord (n : ℕ) : List Unit := List.replicate n ()

theorem variable_finite_records_recover (n : ℕ) : (unaryRecord n).length = n := by
  simp [unaryRecord]

theorem variable_finite_records_injective : Function.Injective unaryRecord := by
  intro a b h
  simpa [unaryRecord] using congrArg List.length h

theorem variable_finite_records_unbounded : ¬ ∃ B, ∀ n, (unaryRecord n).length ≤ B := by
  simp only [variable_finite_records_recover]
  rintro ⟨B,h⟩
  have := h (B+1)
  omega

theorem variable_record_certifies_identity : Certifies (id : ℕ → ℕ) unaryRecord :=
  ⟨fun r => r.val.length,variable_finite_records_recover⟩

end Experiments.FiniteAbstractionControls
