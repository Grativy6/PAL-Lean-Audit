import Mathlib.Data.List.Basic
import Experiments.Pal23Followup

/-! Finite retained-trace realization for the declared known-schedule model.
    A checked schedule shape is not a storage-integrity or A2 admission proof. -/
namespace Experiments.Pal23TraceReplay

/-- Execute a finite schedule and retain `(step, action)` tags chronologically. -/
def runFinite {I : Type u} {S : Type v} {B : Type w} (step : I → S → S × B) : List I → S → S × List (I × B)
  | [], state => (state, [])
  | site :: sites, state =>
      let first := step site state
      let (final, receipts) := runFinite step sites first.1
      (final, (site, first.2) :: receipts)

/-- Apply inverse actions from the final state in reverse receipt order. -/
def undoFinite {I : Type u} {S : Type v} {B : Type w} (undo : I → S → B → S) : List (I × B) → S → S
  | [], state => state
  | (site, bit) :: receipts, state =>
      undo site (undoFinite undo receipts state) bit

/-- A one-step left inverse yields full reversal for every finite known schedule. -/
theorem undoFinite_runFinite {I : Type u} {S : Type v} {B : Type w} (step : I → S → S × B)
    (undo : I → S → B → S)
    (leftInverse : ∀ site state, undo site (step site state).1 (step site state).2 = state)
    (schedule : List I) (state : S) :
    undoFinite undo (runFinite step schedule state).2 (runFinite step schedule state).1 = state := by
  induction schedule generalizing state with
  | nil => rfl
  | cons site sites ih =>
      simp [runFinite, undoFinite, ih, leftInverse]

/-- The retained receipt tags preserve exactly the supplied schedule. -/
theorem runFinite_tags {I : Type u} {S : Type v} {B : Type w} (step : I → S → S × B)
    (schedule : List I) (state : S) :
    (runFinite step schedule state).2.map Prod.fst = schedule := by
  induction schedule generalizing state with
  | nil => rfl
  | cons site sites ih =>
      simp [runFinite, ih]

/-- Reject absent or differently tagged receipt entries before restoration. -/
def checkedUndo {I : Type u} {S : Type v} {B : Type w} (undo : I → S → B → S) [DecidableEq I]
    (schedule : List I) (receipts : List (I × B)) (final : S) : Option S :=
  if receipts.map Prod.fst = schedule then some (undoFinite undo receipts final) else none

/-- A generated receipt passes the supplied-schedule check and restores its input. -/
theorem checkedUndo_generated {I : Type u} {S : Type v} {B : Type w} [DecidableEq I] (step : I → S → S × B)
    (undo : I → S → B → S)
    (leftInverse : ∀ site state, undo site (step site state).1 (step site state).2 = state)
    (schedule : List I) (state : S) :
    checkedUndo undo schedule (runFinite step schedule state).2
      (runFinite step schedule state).1 = some state := by
  have htags := runFinite_tags step schedule state
  have hrestore := undoFinite_runFinite step undo leftInverse schedule state
  unfold checkedUndo
  rw [if_pos htags, hrestore]

/-- Apply the source compare-exchange/action-bit lift at pair site `false` (01) or `true` (12). -/
def tripleStep (site : Bool) (state : Nat × Nat × Nat) : (Nat × Nat × Nat) × Bool :=
  if site then
    let lifted := Experiments.Pal23Followup.repairedExchange (state.2.1, state.2.2)
    ((state.1, lifted.1.1, lifted.1.2), lifted.2)
  else
    let lifted := Experiments.Pal23Followup.repairedExchange (state.1, state.2.1)
    ((lifted.1.1, lifted.1.2, state.2.2), lifted.2)

/-- Undo one named triple-coordinate action using the source pair left inverse. -/
def tripleUndo (site : Bool) (state : Nat × Nat × Nat) (bit : Bool) : Nat × Nat × Nat :=
  if site then
    let restored := Experiments.Pal23Followup.restoreExchange ((state.2.1, state.2.2), bit)
    (state.1, restored.1, restored.2)
  else
    let restored := Experiments.Pal23Followup.restoreExchange ((state.1, state.2.1), bit)
    (restored.1, restored.2, state.2.2)

/-- Receipt length is conserved exactly for each finite schedule. -/
theorem runFinite_length {I : Type u} {S : Type v} {B : Type w}
    (step : I → S → S × B) (schedule : List I) (state : S) :
    (runFinite step schedule state).2.length = schedule.length := by
  have h := congrArg List.length (runFinite_tags step schedule state)
  simpa using h

/-- The source pair left inverse applies at either declared site on every triple. -/
theorem triple_left_inverse : ∀ site state,
    tripleUndo site (tripleStep site state).1 (tripleStep site state).2 = state := by
  intro site state
  rcases state with ⟨x, y, z⟩
  cases site with
  | false =>
    by_cases h : x < y <;>
      simp [tripleStep, tripleUndo, Experiments.Pal23Followup.restoreExchange,
        Experiments.Pal23Followup.repairedExchange,
        Experiments.Pal23Followup.exchange, Experiments.Pal23Followup.actionBit, h]
  | true =>
    by_cases h : y < z <;>
      simp [tripleStep, tripleUndo, Experiments.Pal23Followup.restoreExchange,
        Experiments.Pal23Followup.repairedExchange,
        Experiments.Pal23Followup.exchange, Experiments.Pal23Followup.actionBit, h]

/-- Every finite schedule over the concrete source-backed triple operation reverses. -/
theorem triple_finite_replay (schedule : List Bool) (state : Nat × Nat × Nat) :
    undoFinite tripleUndo (runFinite tripleStep schedule state).2
      (runFinite tripleStep schedule state).1 = state := by
  exact undoFinite_runFinite tripleStep tripleUndo triple_left_inverse schedule state
/-- The fixture schedule `[false, true]` maps `(0,1,2)` to `(1,2,0)` with `[true,true]`. -/
theorem triple_fixture_receipt :
    runFinite tripleStep [false, true] (0, 1, 2) = ((1, 2, 0), [(false, true), (true, true)]) := by
  decide

/-- The concrete source lift's one-step inverse gives the fixture's full replay. -/
theorem triple_fixture_replay :
    undoFinite tripleUndo [(false, true), (true, true)] (1, 2, 0) = (0, 1, 2) := by
  simpa [triple_fixture_receipt] using triple_finite_replay [false, true] (0, 1, 2)
/-- Reversed tags are rejected even when the receipt length is unchanged. -/
theorem triple_wrong_order_rejected :
    checkedUndo tripleUndo [false, true] [(true, true), (false, true)] (1, 2, 0) = none := by
  simp [checkedUndo]

/-- A missing receipt entry is rejected by exact tag/schedule shape checking. -/
theorem triple_missing_receipt_rejected :
    checkedUndo tripleUndo [false, true] [(false, true)] (1, 2, 0) = none := by
  simp [checkedUndo]

/-- A corrupted bit preserves the tag shape; shape checking alone accepts it. -/
theorem triple_corrupt_bit_shape_accepted :
    ([(false, false), (true, true)] : List (Bool × Bool)).map Prod.fst = [false, true] := by
  decide

/-- The accepted corrupted bit produces an incorrect recovered triple. -/
theorem triple_corrupt_bit_wrong_recovery :
    checkedUndo tripleUndo [false, true] [(false, false), (true, true)] (1, 2, 0) =
      some (1, 0, 2) ∧ (1, 0, 2) ≠ (0, 1, 2) := by
  decide

/-- Omitting the entire retained trace cannot pass a nonempty schedule check. -/
theorem triple_lost_trace_rejected :
    checkedUndo tripleUndo [false, true] [] (1, 2, 0) = none := by
  simp [checkedUndo]

end Experiments.Pal23TraceReplay
