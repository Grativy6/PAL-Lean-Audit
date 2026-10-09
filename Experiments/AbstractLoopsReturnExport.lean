import Experiments.AbstractLoopsPostprocessing
import Mathlib.Tactic

/-!
AL-C, Abstract Loops v1.0 P0081-P0107. Finite mathematical fixtures only.
Carrier qualification is a proposed source criterion. The model below supplies
an explicit identity, coordinate cut, persistence rule, and source-copy provenance;
checking this fixture does not establish any physical carrier-generation claim.
-/
namespace Experiments.AbstractLoopsReturnExport

set_option autoImplicit false

open AbstractLoopsJoint AbstractLoopsPostprocessing

def ReadableIdentity {A O : Type} (before after : A → O) : Prop := ∀ a, after a = before a
def DirectResidual {A O : Type} (before after : A → O) : Prop := ∃ a, after a ≠ before a
def CandidatePresent {A C : Type} (emit : A → Option C) : Prop := ∃ a, emit a ≠ none

theorem no_direct_residual_iff_readable_identity {A O : Type} (before after : A → O) :
    ¬ DirectResidual before after ↔ ReadableIdentity before after := by
  simp [DirectResidual, ReadableIdentity]

/-- A typed return can change an unobserved coordinate while its chosen readout is identity. -/
def hiddenReturn (a : Bool × Bool) : Bool × Bool := (a.1, !a.2)

theorem hidden_motion_readable_identity :
    ReadableIdentity Prod.fst (Prod.fst ∘ hiddenReturn) ∧
    hiddenReturn (false, false) ≠ (false, false) := by
  exact ⟨fun _ => rfl, by decide⟩

/-- Distinct roster components carry different payload types, in one common ambient space. -/
inductive RosterState where
  | original (a b : Bool)
  | extended (a b c : Bool)
  deriving DecidableEq

def contributors : RosterState → Bool × Bool
  | .original a b => (a, b)
  | .extended a b _ => (a, b)

def candidate : RosterState → Option Bool
  | .original _ _ => none
  | .extended _ _ c => some c

def addresses : RosterState → Finset Nat
  | .original _ _ => {0, 1}
  | .extended _ _ _ => {0, 1, 2}

/-- A supplied intervention witness for the addressable new coordinate. -/
def writeCandidate (value : Bool) : RosterState → RosterState
  | .original a b => .original a b
  | .extended a b _ => .extended a b value

theorem declared_cut_witness (a b c value : Bool) :
    contributors (writeCandidate value (.extended a b c)) = (a, b) ∧
      candidate (writeCandidate value (.extended a b c)) = some value := by
  exact ⟨rfl, rfl⟩

/-- A single closure may change the A readout and independently export a source-derived C. -/
def closure (direct exported : Bool) (input : Bool × Bool) : RosterState :=
  let a := if direct then !input.1 else input.1
  if exported then .extended a input.2 input.2 else .original a input.2

theorem all_four_return_export_combinations (direct exported : Bool) :
    (ReadableIdentity id (contributors ∘ closure direct exported) ↔ direct = false) ∧
      (DirectResidual id (contributors ∘ closure direct exported) ↔ direct = true) ∧
      (CandidatePresent (candidate ∘ closure direct exported) ↔ exported = true) := by
  unfold ReadableIdentity DirectResidual CandidatePresent
  cases direct <;> cases exported <;>
    decide

/-- Coupled and baseline updates are endomaps on the very same roster space. -/
def coupledStep (direct exported : Bool) : RosterState → RosterState
  | .original a b => closure direct exported (a, b)
  | .extended a b c => .extended a b c

def baselineStep : RosterState → RosterState := id

def coupledHistory (direct : Bool) (input : Bool × Bool) (n : Nat) : RosterState :=
  scheduledIteration (fun _ => coupledStep direct true) (fun _ : Unit =>
    RosterState.original input.1 input.2) n ()

def baselineHistory (input : Bool × Bool) (n : Nat) : RosterState :=
  scheduledIteration (fun _ => baselineStep) (fun _ : Unit =>
    RosterState.original input.1 input.2) n ()

theorem coupled_history_after_entry (direct : Bool) (input : Bool × Bool) (n : Nat) :
    coupledHistory direct input (n + 1) = closure direct true input := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change coupledStep direct true (coupledHistory direct input (n + 1)) = _
    rw [ih]
    simp [closure, coupledStep]

theorem baseline_keeps_original_roster (input : Bool × Bool) (n : Nat) :
    baselineHistory input n = .original input.1 input.2 := by
  induction n with
  | zero => rfl
  | succ n ih => exact ih

/-- Identity, source-copy provenance, persistence at every positive time, and baseline exclusion. -/
theorem generated_fixture_receipt (input : Bool × Bool) (n : Nat) :
    2 ∈ addresses (coupledHistory false input (n + 1)) ∧
    2 ∉ addresses (baselineHistory input n) ∧
    candidate (coupledHistory false input (n + 1)) = some input.2 ∧
    candidate (baselineHistory input n) = none ∧
    contributors (coupledHistory false input (n + 1)) = input := by
  simp [coupled_history_after_entry, baseline_keeps_original_roster, closure,
    addresses, candidate, contributors]

/-- Merely seeing a new address says nothing about whether a supplied next step preserves it. -/
theorem roster_tag_without_persistence :
    2 ∈ addresses (.extended false false true) ∧
      2 ∉ addresses ((fun _ : RosterState => RosterState.original false false)
        (.extended false false true)) := by
  simp [addresses]

/-- Neither a roster tag nor contributor readouts certify the declared source-copy provenance. -/
theorem roster_tag_without_source_copy :
    2 ∈ addresses (.extended false false true) ∧
    contributors (.extended false false true) = contributors (.original false false) ∧
    candidate (.extended false false true) ≠ some (contributors (.original false false)).2 := by
  simp [addresses, contributors, candidate]

theorem export_respects_complete_initializer {W I C : Type}
    (initializer : W → I) (emit : I → Option C) (u v : W)
    (h : initializer u = initializer v) : emit (initializer u) = emit (initializer v) :=
  postprocess_preserves_kernel emit initializer u v h

/-- The second input is varying environmental information omitted by the first-coordinate trace. -/
theorem varying_environment_defeats_narrow_ceiling :
    Certifies (fun w : Bool × Bool => some w.2) id ∧
      ¬ Certifies (fun w : Bool × Bool => some w.2) Prod.fst := by
  refine ⟨⟨fun z => some z.val.2, fun _ => rfl⟩, ?_⟩
  intro hc
  have h := (reachable_certifies_iff_kernel_subset (fun w : Bool × Bool => some w.2)
    Prod.fst).mp hc (false, false) (false, true) rfl
  cases h

theorem fixed_environment_restores_trace_factorization {W T E C : Type}
    (trace : W → T) (environment : E) (emit : T × E → Option C) :
    Certifies (fun w => emit (trace w, environment)) trace := by
  exact ⟨fun z => emit (z.val, environment), fun _ => rfl⟩

end Experiments.AbstractLoopsReturnExport
