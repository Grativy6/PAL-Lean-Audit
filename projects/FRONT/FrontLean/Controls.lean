import FrontLean.Answers
import FrontLean.Continuation
import FrontLean.Correction
import FrontLean.Linear
import FrontLean.Horizon

namespace FrontLean

/-- Losing the observation labels can erase the requested answer. -/
def unlabelled (x : Bool × Bool) : Multiset Bool := {x.1, x.2}

theorem lost_labels_counterexample :
    ¬ ∃ d : Multiset Bool → Bool, ∀ x : Bool × Bool, d (unlabelled x) = x.1 := by
  rintro ⟨d, h⟩
  have same : unlabelled (true, false) = unlabelled (false, true) := by decide
  have impossible : true = false := (h (true, false)).symm.trans
    ((congrArg d same).trans (h (false, true)))
  cases impossible

/-- SAT does not have the UNSAT core's direction of transfer. -/
theorem sat_does_not_transfer_to_strengthening :
    (∃ x : Bool, x = true) ∧ ¬ ∃ x : Bool, x = true ∧ x = false := by decide

/-- The simplest stale premise already blocks unconditional proof reuse. -/
theorem stale_premise_counterexample :
    Valid (Basis.mk (fun _ : Unit => True) (fun _ => False)) (Derivation.root ()) ∧
    ¬ Valid (Basis.mk (fun _ : Unit => False) (fun _ => False)) (Derivation.root ()) := by
  simp [Valid]

/-- A satisfactory changed candidate can still lack authorization. -/
theorem technically_valid_but_not_authorized :
    (scratchRepair (0 : ℕ) 1 False (fun _ => True) []).status = .notAuthorized ∧
    (scratchRepair (0 : ℕ) 1 False (fun _ => True) []).value = 0 := by
  simp [scratchRepair]

private def diagonal : Submodule ℚ (ℚ × ℚ) :=
  ((LinearMap.fst ℚ ℚ ℚ) - (LinearMap.snd ℚ ℚ ℚ)).ker

/-- Each per-view generated quotient is zero; the joint quotient still sees x-y. -/
theorem independent_baselines_lose_relation :
    diagonal.map (LinearMap.fst ℚ ℚ ℚ) = ⊤ ∧
    diagonal.map (LinearMap.snd ℚ ℚ ℚ) = ⊤ ∧ diagonal.mkQ (1, 0) ≠ 0 := by
  constructor
  · apply top_unique
    intro y _
    exact ⟨(y, y), by simp [diagonal, LinearMap.mem_ker], rfl⟩
  constructor
  · apply top_unique
    intro y _
    exact ⟨(y, y), by simp [diagonal, LinearMap.mem_ker], rfl⟩
  · change (Submodule.Quotient.mk (1, 0) : (ℚ × ℚ) ⧸ diagonal) ≠ 0
    rw [ne_eq, Submodule.Quotient.mk_eq_zero]
    norm_num [diagonal, LinearMap.mem_ker]

/-- Invariance is necessary even when the static quotient remains legitimate. -/
theorem quotient_update_can_fail :
    ¬ ∃ D : ((ℚ × ℚ) ⧸ diagonal) →ₗ[ℚ] ((ℚ × ℚ) ⧸ diagonal),
      D.comp diagonal.mkQ = diagonal.mkQ.comp
        ((LinearMap.fst ℚ ℚ ℚ).prod (0 : (ℚ × ℚ) →ₗ[ℚ] ℚ)) := by
  rw [quotient_update_iff]
  intro h
  have hh := h (1, 1) (by simp [diagonal, LinearMap.mem_ker])
  norm_num [diagonal, LinearMap.mem_ker] at hh

/-- Omitting the transport in the return law changes even this scalar result. -/
theorem untransported_return_wrong :
    ((2 : ℚ) ^ (1 + 1) - 1) ≠ (2 ^ 1 - 1) + (2 ^ 1 - 1) := by norm_num

end FrontLean
