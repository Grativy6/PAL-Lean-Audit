import Mathlib.Data.Nat.Basic
import Mathlib.Data.Set.Image
import Mathlib.Tactic.Core

/-!
Supplementary finite and set-theoretic realizations for selected PAL v2.3 Atlas
cards.  Each theorem is limited to its declared Lean model; it neither adopts
PAL nor supplies persistence, totalization, or authority.
-/

namespace Experiments.Pal23Followup

def exchange (pair : Nat × Nat) : Nat × Nat :=
  if pair.1 < pair.2 then (pair.2, pair.1) else pair

def actionBit (pair : Nat × Nat) : Bool := decide (pair.1 < pair.2)

def repairedExchange (pair : Nat × Nat) : (Nat × Nat) × Bool :=
  (exchange pair, actionBit pair)

def restoreExchange (receipt : (Nat × Nat) × Bool) : Nat × Nat :=
  if receipt.2 then (receipt.1.2, receipt.1.1) else receipt.1

/-- A declared compare-exchange loses a concrete strict-pair distinction. -/
theorem exchange_has_two_point_collision :
    exchange (0, 1) = exchange (1, 0) ∧ (0, 1) ≠ (1, 0) := by
  decide

/-- The action bit is an explicit left-inverse witness for this one-step model. -/
theorem restore_repairedExchange (pair : Nat × Nat) :
    restoreExchange (repairedExchange pair) = pair := by
  by_cases h : pair.1 < pair.2
  · simp [restoreExchange, repairedExchange, exchange, actionBit, h]
  · simp [restoreExchange, repairedExchange, exchange, actionBit, h]

/-- The repaired one-step map is injective, unlike `exchange` alone. -/
theorem repairedExchange_injective : Function.Injective repairedExchange := by
  intro left right hreceipt
  have hrestored := congrArg restoreExchange hreceipt
  rw [restore_repairedExchange, restore_repairedExchange] at hrestored
  exact hrestored

/-- Reachable decoders satisfying the same answer equation are pointwise unique. -/
theorem reachable_decoder_unique {W T Q : Type} (trace : W → T) (answer : W → Q)
    (decode₁ decode₂ : Set.range trace → Q)
    (h₁ : ∀ w, decode₁ ⟨trace w, ⟨w, rfl⟩⟩ = answer w)
    (h₂ : ∀ w, decode₂ ⟨trace w, ⟨w, rfl⟩⟩ = answer w) :
    decode₁ = decode₂ := by
  funext point
  obtain ⟨w, hw⟩ := point.property
  have hpoint : (⟨trace w, ⟨w, rfl⟩⟩ : Set.range trace) = point :=
    Subtype.ext hw
  rw [← hpoint]
  exact (h₁ w).trans (h₂ w).symm

end Experiments.Pal23Followup
