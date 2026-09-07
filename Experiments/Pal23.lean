import Mathlib.Data.Bool.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Data.Set.Image
import Mathlib.Logic.Function.Iterate
import Mathlib.Tactic.Core

/-!
Conditional set-theoretic and finite-fixture Lean realizations for selected PAL v2.3 Atlas cards.
They check only the declarations in their theorem statements.
-/

namespace Experiments.Pal23

theorem reachable_decoder_iff {W T Q : Type} (trace : W → T) (answer : W → Q) :
    (∃ decode : Set.range trace → Q,
      ∀ w, decode ⟨trace w, ⟨w, rfl⟩⟩ = answer w) ↔
      ∀ ⦃w w' : W⦄, trace w = trace w' → answer w = answer w' := by
  constructor
  · rintro ⟨decode, hdecode⟩ w w' htrace
    have hsub : (⟨trace w, ⟨w, rfl⟩⟩ : Set.range trace) =
        ⟨trace w', ⟨w', rfl⟩⟩ := Subtype.ext htrace
    rw [← hdecode w, ← hdecode w', hsub]
  · intro hconstant
    let decode : Set.range trace → Q := fun t => answer (Classical.choose t.property)
    refine ⟨decode, ?_⟩
    intro w
    let point : Set.range trace := ⟨trace w, ⟨w, rfl⟩⟩
    change answer (Classical.choose point.property) = answer w
    apply hconstant
    exact point.property.choose_spec

theorem collision_prevents_reachable_decoder {W T Q : Type} (trace : W → T) (answer : W → Q)
    {w w' : W} (htrace : trace w = trace w') (hanswer : answer w ≠ answer w') :
    ¬ ∃ decode : Set.range trace → Q,
      ∀ x, decode ⟨trace x, ⟨x, rfl⟩⟩ = answer x := by
  intro hdecoder
  have hconstant := (reachable_decoder_iff trace answer).mp hdecoder
  exact hanswer (hconstant htrace)

theorem no_total_decoder_empty_source_nonempty_ambient :
    ¬ ∃ (trace : Empty → Bool) (answer : Empty → Empty) (decode : Bool → Empty),
      ∀ source, decode (trace source) = answer source := by
  rintro ⟨_, _, decode, _⟩
  exact Empty.elim (decode false)

theorem freeze_injective {Work Capsule : Type} (freeze : Work → Capsule) (thaw : Capsule → Work)
    (hroundtrip : ∀ work, thaw (freeze work) = work) : Function.Injective freeze := by
  intro left right heq
  rw [← hroundtrip left, ← hroundtrip right, heq]

theorem suffix_preserved {Work Capsule Terminal : Type} (freeze : Work → Capsule)
    (thaw : Capsule → Work) (suffix : Work → Terminal)
    (hroundtrip : ∀ work, thaw (freeze work) = work) (work : Work) :
    suffix (thaw (freeze work)) = suffix work := by
  rw [hroundtrip]

theorem bool_capsule_roundtrip (work : Bool) : (id (id work)) = work := rfl

structure HeartbeatState where
  work : Bool
  audit : Nat
  spent : Nat
  grantLive : Bool
deriving DecidableEq, Repr

def heartbeat (state : HeartbeatState) : HeartbeatState :=
  { state with audit := state.audit + 1, spent := state.spent + 1, grantLive := false }

def progress (state : HeartbeatState) : Nat := if state.work then 1 else 0

def idle : HeartbeatState := ⟨false, 0, 5, true⟩

theorem heartbeat_work_stutter : (heartbeat idle).work = idle.work := rfl

theorem heartbeat_hidden_motion : heartbeat idle ≠ idle := by decide

theorem heartbeat_not_progress (state : HeartbeatState) :
    progress (heartbeat state) = progress state := by
  cases state
  rfl

theorem heartbeat_loop_no_progress (n : Nat) (state : HeartbeatState) :
    progress ((heartbeat^[n]) state) = progress state := by
  induction n generalizing state with
  | zero => rfl
  | succ n ih =>
      rw [Function.iterate_succ_apply, ih]
      exact heartbeat_not_progress state

def restoreWork (before after : HeartbeatState) : HeartbeatState :=
  { after with work := before.work }

theorem restore_work_not_restore_budget_or_grant :
    let restored := restoreWork idle (heartbeat idle)
    restored.work = idle.work ∧ restored.spent ≠ idle.spent ∧ restored.grantLive ≠ idle.grantLive := by
  decide

theorem restore_work_is_not_total_state_recovery :
    restoreWork idle (heartbeat idle) ≠ idle := by decide

end Experiments.Pal23
