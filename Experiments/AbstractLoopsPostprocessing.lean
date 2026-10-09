import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Powerset
import Mathlib.Data.Fintype.Prod
import Mathlib.Order.OrderIsoNat
import Experiments.AbstractLoopsJoint

/-!
# C5: bounded postprocessing and finite partition stabilization

This is a function-level realization for a finite alternative domain.  It makes
no physical claim about annihilation, storage, or loop behavior.
-/
namespace Experiments.AbstractLoopsPostprocessing

/-- A deterministic map applied after a trace, with no additional observation. -/
def postprocess {α Trace Output : Type} (c : Trace → Output) (trace : α → Trace) : α → Output :=
  fun alternative => c (trace alternative)

/-- Equality of earlier trace values remains equality after deterministic postprocessing. -/
theorem postprocess_preserves_kernel {α Trace Output : Type} (c : Trace → Output)
    (trace : α → Trace) (first second : α) :
    trace first = trace second → postprocess c trace first = postprocess c trace second := by
  intro h
  exact congrArg c h

/-- A new XOR coordinate makes the answer certifiable where the first coordinate alone does not. -/
theorem fresh_xor_observation_changes_aperture :
    ¬ Experiments.AbstractLoopsJoint.Certifies Experiments.AbstractLoopsJoint.xorAnswer
        Experiments.AbstractLoopsJoint.xorFirst ∧
      Experiments.AbstractLoopsJoint.Certifies Experiments.AbstractLoopsJoint.xorAnswer
        (Experiments.AbstractLoopsJoint.jointTrace Experiments.AbstractLoopsJoint.xorFirst
          Experiments.AbstractLoopsJoint.xorSecond) := by
  exact ⟨Experiments.AbstractLoopsJoint.xor_first_insufficient,
    Experiments.AbstractLoopsJoint.xor_pair_certifies⟩

/-- The added XOR coordinate cannot be represented as closed postprocessing of the old coordinate. -/
theorem fresh_xor_pair_not_closed_postprocess (c : Bool → Bool × Bool) :
    postprocess c Experiments.AbstractLoopsJoint.xorFirst ≠
      Experiments.AbstractLoopsJoint.jointTrace Experiments.AbstractLoopsJoint.xorFirst
        Experiments.AbstractLoopsJoint.xorSecond := by
  intro h
  have h₀ := congrFun h (false, false)
  have h₁ := congrFun h (false, true)
  change c false = (false, false) at h₀
  change c false = (false, true) at h₁
  have hpair : (false, false) = (false, true) := h₀.symm.trans h₁
  cases hpair

/-- State-only evolution with an explicitly supplied update schedule. -/
def scheduledIteration {World State : Type} (step : Nat → State → State)
    (initial : World → State) : Nat → World → State
  | 0 => initial
  | n + 1 => fun world => step n (scheduledIteration step initial n world)

/-- Every update in the schedule is deterministic postprocessing of its preceding state. -/
theorem scheduled_iteration_preserves_kernel {World State : Type}
    (step : Nat → State → State) (initial : World → State) (n : Nat)
    (first second : World) :
    scheduledIteration step initial n first = scheduledIteration step initial n second →
      scheduledIteration step initial (n + 1) first = scheduledIteration step initial (n + 1) second := by
  intro h
  simpa [scheduledIteration] using congrArg (step n) h

/-- Encode the kernel relation of a state observation on a finite alternative domain. -/
noncomputable def kernelPairs {World State : Type} [Fintype World] [DecidableEq World]
    [DecidableEq State] (observe : World → State) : Finset (World × World) := by
  classical
  exact Finset.univ.filter (fun pair => observe pair.1 = observe pair.2)

/--
Any inclusion-monotone chain of relations on a finite carrier eventually stabilizes.
The proof uses the well-founded strict order on the finite type of finite subsets,
so it needs no assumed stabilization index and no bound on when merges occur.
-/
theorem finite_relation_chain_stabilizes {α : Type} [Fintype α] [DecidableEq α]
    (relations : Nat → Finset α)
    (hmerge : ∀ n, relations n ⊆ relations (n + 1)) :
    ∃ start, ∀ n, start ≤ n → relations start = relations n := by
  classical
  have hmono : Monotone relations := by
    intro i j hij
    induction j, hij using Nat.le_induction with
    | base => exact Finset.Subset.rfl
    | succ j hij ih => exact Finset.Subset.trans ih (hmerge j)
  letI : WellFoundedGT (Finset α) := Finite.to_wellFoundedGT
  let sequence : Nat →o Finset α := ⟨relations, hmono⟩
  exact WellFoundedGT.monotone_chain_condition sequence

/-- Kernel partitions from deterministic scheduled processing stabilize on a finite domain. -/
theorem finite_scheduled_partition_stabilizes {State World : Type} [Fintype World]
    [DecidableEq World] [DecidableEq State]
    (step : Nat → State → State) (initial : World → State) :
    ∃ start, ∀ n, start ≤ n →
      kernelPairs (scheduledIteration step initial start) =
        kernelPairs (scheduledIteration step initial n) := by
  apply finite_relation_chain_stabilizes
  intro n pair hpair
  simp only [kernelPairs, Finset.mem_filter, Finset.mem_univ, true_and] at hpair ⊢
  exact scheduled_iteration_preserves_kernel step initial n pair.1 pair.2 hpair

/-- A bijective state relabeling can change state values while preserving the kernel. -/
def booleanSwap (value : Bool) : Bool := !value

theorem boolean_swap_kernel_unchanged :
    kernelPairs booleanSwap = kernelPairs id := by
  ext pair
  cases pair with
  | mk left right => cases left <;> cases right <;> simp [kernelPairs, booleanSwap]

theorem boolean_swap_has_two_cycle (value : Bool) :
    booleanSwap (booleanSwap value) = value := by
  cases value <;> rfl

end Experiments.AbstractLoopsPostprocessing

