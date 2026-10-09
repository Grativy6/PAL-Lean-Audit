import Mathlib.Data.List.Basic

/-! Finite binary nested-account realization for SC-22 / D42 / O65 / T75. -/
namespace Experiments.Pal24NestedAccount

inductive Unit where | credit | hour deriving DecidableEq, Repr
inductive Charge where | known (eventId amount : Nat) | unknown (eventId : Nat) deriving DecidableEq, Repr
inductive Account where
  | leaf (unit : Unit) (expectedChildren : Nat) (events : List Charge)
  | branch (unit : Unit) (expectedChildren : Nat) (events : List Charge) (left right : Account)
  deriving Repr

/-- The nested-account projection protected during a modeled administrative attempt. -/
structure AccountWork where
  account : Account
  deriving Repr

def chargeId : Charge → Nat | .known eventId _ => eventId | .unknown eventId => eventId
def chargeValue : Charge → Option Nat | .known _ amount => some amount | .unknown _ => none
def optionPlus : Option Nat → Option Nat → Option Nat
  | some left, some right => some (left + right) | _, _ => none
def aggregateEvents : List Charge → Option Nat
  | [] => some 0 | event :: events => optionPlus (chargeValue event) (aggregateEvents events)
def accountUnit : Account → Unit | .leaf unit _ _ => unit | .branch unit _ _ _ _ => unit
def flattenEvents : Account → List Charge
  | .leaf _ _ events => events
  | .branch _ _ events left right => events ++ flattenEvents left ++ flattenEvents right
def structuralAggregate : Account → Option Nat
  | .leaf _ _ events => aggregateEvents events
  | .branch _ _ events left right => optionPlus (aggregateEvents events) (optionPlus (structuralAggregate left) (structuralAggregate right))
def flattenedAggregate (account : Account) : Option Nat := aggregateEvents (flattenEvents account)
def eventIds (account : Account) : List Nat := (flattenEvents account).map chargeId
def noUnknown : Account → Bool
  | .leaf _ _ events => events.all (fun event => (chargeValue event).isSome)
  | .branch _ _ events left right => events.all (fun event => (chargeValue event).isSome) && noUnknown left && noUnknown right
def uniqueAttribution (account : Account) : Prop := (eventIds account).Nodup
def compatibleUnit : Account → Bool
  | .leaf _ _ _ => true
  | .branch unit _ _ left right => (accountUnit left == unit) && (accountUnit right == unit) && compatibleUnit left && compatibleUnit right
def completeChildren : Account → Bool
  | .leaf _ expectedChildren _ => expectedChildren == 0
  | .branch _ expectedChildren _ left right => (expectedChildren == 2) && completeChildren left && completeChildren right
def accepted (account : Account) : Prop := noUnknown account = true ∧ uniqueAttribution account ∧ compatibleUnit account = true ∧ completeChildren account = true
def appendOwn (charge : Charge) : Account → Account
  | .leaf unit expectedChildren events => .leaf unit expectedChildren (events ++ [charge])
  | .branch unit expectedChildren events left right => .branch unit expectedChildren (events ++ [charge]) left right
def linkedEpochAggregate (priorSpent : Nat) (linked : Bool) (account : Account) : Option Nat :=
  if linked then Option.map (priorSpent + ·) (structuralAggregate account) else none
def administrationCompletes (fuel requiredFuel : Nat) : Bool := requiredFuel <= fuel
def administrationAttempt (work : AccountWork) (fuel requiredFuel : Nat) : Bool × AccountWork :=
  if administrationCompletes fuel requiredFuel then (true, work) else (false, work)

theorem optionPlus_assoc (left middle right : Option Nat) : optionPlus (optionPlus left middle) right = optionPlus left (optionPlus middle right) := by
  cases left <;> cases middle <;> cases right <;> simp [optionPlus, Nat.add_assoc]
theorem aggregateEvents_append (left right : List Charge) : aggregateEvents (left ++ right) = optionPlus (aggregateEvents left) (aggregateEvents right) := by
  induction left with
  | nil =>
      cases h : aggregateEvents right <;> simp [aggregateEvents, optionPlus, h]
  | cons event left ih => simp [aggregateEvents, ih, optionPlus_assoc]
theorem structuralAggregate_eq_flattenedAggregate (account : Account) : structuralAggregate account = flattenedAggregate account := by
  induction account with
  | leaf unit expectedChildren events => simp [structuralAggregate, flattenedAggregate, flattenEvents]
  | branch unit expectedChildren events left right leftIh rightIh =>
      simp [structuralAggregate, flattenedAggregate, flattenEvents, aggregateEvents_append, leftIh, rightIh]
theorem accepted_aggregate_matches_flattening_with_unique_ids (account : Account) (h : accepted account) :
    structuralAggregate account = flattenedAggregate account ∧ (eventIds account).Nodup := by
  exact ⟨structuralAggregate_eq_flattenedAggregate account, h.2.1⟩
theorem aggregateEvents_append_known (events : List Charge) (eventId amount : Nat) :
    aggregateEvents (events ++ [.known eventId amount]) =
      Option.map (fun total => total + amount) (aggregateEvents events) := by
  rw [aggregateEvents_append]
  cases aggregateEvents events <;>
    simp [aggregateEvents, chargeValue, optionPlus]
theorem optionPlus_map_add_left (amount : Nat) (left right : Option Nat) :
    optionPlus (Option.map (fun total => total + amount) left) right =
      Option.map (fun total => total + amount) (optionPlus left right) := by
  cases left <;> cases right <;> simp [optionPlus, Nat.add_comm, Nat.add_left_comm]
theorem appendOwn_known_monotone (account : Account) (eventId amount : Nat) : structuralAggregate (appendOwn (.known eventId amount) account) = Option.map (fun total => total + amount) (structuralAggregate account) := by
  cases account with
  | leaf unit expectedChildren events =>
      simp only [appendOwn, structuralAggregate]
      exact aggregateEvents_append_known events eventId amount
  | branch unit expectedChildren events left right =>
      simp only [appendOwn, structuralAggregate]
      rw [aggregateEvents_append_known]
      exact optionPlus_map_add_left amount (aggregateEvents events)
        (optionPlus (structuralAggregate left) (structuralAggregate right))
theorem linked_epoch_preserves_old_spend (priorSpent total : Nat) (account : Account) : structuralAggregate account = some total → linkedEpochAggregate priorSpent true account = some (priorSpent + total) := by
  intro h; simp [linkedEpochAggregate, h]
theorem unknown_is_not_resolved_zero (eventId : Nat) : chargeValue (.unknown eventId) ≠ some 0 := by simp [chargeValue]

def twoLevel : Account := .branch .credit 2 [.known 1 3] (.leaf .credit 0 [.known 2 5]) (.leaf .credit 0 [.known 3 7])
def threeLevel : Account := .branch .credit 2 [.known 1 2] (.branch .credit 2 [.known 2 3] (.leaf .credit 0 [.known 3 4]) (.leaf .credit 0 [.known 4 5])) (.leaf .credit 0 [.known 5 6])
def missingPromisedChild : Account := .leaf .credit 1 [.known 1 3]
def duplicateAttribution : Account := .leaf .credit 0 [.known 1 3, .known 1 5]
def duplicateParentChildAttribution : Account :=
  .branch .credit 2 [.known 1 3] (.leaf .credit 0 [.known 2 5]) (.leaf .credit 0 [.known 1 7])
def incompatibleUnit : Account := .branch .credit 2 [.known 1 3] (.leaf .hour 0 [.known 2 5]) (.leaf .credit 0 [.known 3 7])
def unknownRequired : Account := .leaf .credit 0 [.unknown 1]
def unrecordedReset : Option Nat := linkedEpochAggregate 7 false (.leaf .credit 0 [.known 2 1])
theorem twoLevel_accepted : accepted twoLevel := by
  simp [accepted, twoLevel, noUnknown, uniqueAttribution, eventIds, flattenEvents,
    compatibleUnit, completeChildren, chargeValue, chargeId, accountUnit]
theorem threeLevel_total : structuralAggregate threeLevel = some 20 := by rfl
theorem missing_promised_child_rejected : completeChildren missingPromisedChild = false := by rfl
theorem duplicate_attribution_rejected : ¬ uniqueAttribution duplicateAttribution := by
  simp [uniqueAttribution, duplicateAttribution, eventIds, flattenEvents, chargeId]
theorem parent_child_duplicate_attribution_rejected : ¬ uniqueAttribution duplicateParentChildAttribution := by
  simp [uniqueAttribution, duplicateParentChildAttribution, eventIds, flattenEvents, chargeId]
theorem incompatible_unit_rejected : compatibleUnit incompatibleUnit = false := by rfl
theorem unknown_required_rejected : noUnknown unknownRequired = false := by rfl
theorem unrecorded_reset_rejected : unrecordedReset = none := by rfl
theorem insufficient_administrative_fuel_preserves_account_work (work : AccountWork)
    (fuel requiredFuel : Nat) (h : requiredFuel > fuel) :
    administrationAttempt work fuel requiredFuel = (false, work) := by
  simp [administrationAttempt, administrationCompletes, Nat.not_le_of_gt h]
end Experiments.Pal24NestedAccount

