import Mathlib.Data.List.Basic

import Experiments.MindContinuation
import Experiments.Pal23Roundtrip

/-!
# PAL v2.4 B1: continuation profile

This is a generic deterministic transition model with a declared input aperture.
It proves an observation-preservation result from a step-preserving relation for
all finite admitted suffixes. It does not model physical persistence, source
authenticity, operational resources, contextual authority, or full PAL/MIND.
-/
namespace Experiments.Pal24Continuation

/-- A declared state, observation, transition rule, and admitted-input aperture. -/
structure TransitionProfile where
  State : Type
  Input : Type
  Answer : Type
  observe : State → Answer
  step : State → Input → State
  admits : Input → Prop

/-- Apply one fixed finite input suffix using the profile's deterministic step. -/
def run (p : TransitionProfile) : p.State → List p.Input → p.State
  | state, [] => state
  | state, input :: suffix => run p (p.step state input) suffix

/-- Every input in the suffix lies in the profile's declared aperture. -/
def admissibleSuffix (p : TransitionProfile) (suffix : List p.Input) : Prop :=
  ∀ input, input ∈ suffix → p.admits input

/-- The observations agree after one selected suffix. -/
def oneSuffixEquivalent (p : TransitionProfile) (left right : p.State)
    (suffix : List p.Input) : Prop :=
  p.observe (run p left suffix) = p.observe (run p right suffix)

/-- The observations agree after every finite suffix in the declared aperture. -/
def continuationEquivalent (p : TransitionProfile) (left right : p.State) : Prop :=
  ∀ suffix, admissibleSuffix p suffix → oneSuffixEquivalent p left right suffix

/-- Runs split compositionally at the boundary between two suffixes. -/
theorem run_append (p : TransitionProfile) (state : p.State)
    (first second : List p.Input) :
    run p state (first ++ second) = run p (run p state first) second := by
  induction first generalizing state with
  | nil => rfl
  | cons input first ih => exact ih (p.step state input)

/-- A relation preserved by each admitted step preserves observations along one suffix. -/
theorem one_suffix_of_step_simulation (p : TransitionProfile)
    (related : p.State → p.State → Prop)
    (hObserve : ∀ left right, related left right → p.observe left = p.observe right)
    (hStep : ∀ input, p.admits input → ∀ left right,
      related left right → related (p.step left input) (p.step right input))
    {left right : p.State} (hRelated : related left right)
    (suffix : List p.Input) (hAdmissible : admissibleSuffix p suffix) :
    oneSuffixEquivalent p left right suffix := by
  induction suffix generalizing left right with
  | nil =>
      exact hObserve left right hRelated
  | cons input suffix ih =>
      apply ih
      · exact hStep input (hAdmissible input (by simp)) left right hRelated
      · intro next hMem
        exact hAdmissible next (by simp [hMem])

/-- Step simulation gives equivalence for all finite suffixes admitted by the profile. -/
theorem all_finite_suffixes_of_step_simulation (p : TransitionProfile)
    (related : p.State → p.State → Prop)
    (hObserve : ∀ left right, related left right → p.observe left = p.observe right)
    (hStep : ∀ input, p.admits input → ∀ left right,
      related left right → related (p.step left input) (p.step right input))
    {left right : p.State} (hRelated : related left right) :
    continuationEquivalent p left right := by
  intro suffix hAdmissible
  exact one_suffix_of_step_simulation p related hObserve hStep hRelated suffix hAdmissible

/-- A test aperture admits only `false`; `true` is a newly added continuation input. -/
def narrowAperture : Bool → Prop := fun input => input = false

/-- The transition increments the answer only when both the event and retained rule are true. -/
def apertureStep (state : Nat × Bool) (input : Bool) : Nat × Bool :=
  (if input && state.2 then state.1 + 1 else state.1, state.2)

/-- Two profiles share state and transition semantics but declare different apertures. -/
def narrowProfile : TransitionProfile where
  State := Nat × Bool
  Input := Bool
  Answer := Nat
  observe := Prod.fst
  step := apertureStep
  admits := narrowAperture

def wideProfile : TransitionProfile where
  State := Nat × Bool
  Input := Bool
  Answer := Nat
  observe := Prod.fst
  step := apertureStep
  admits := fun _ => True

/-- Equal selected answers do not establish exact state recovery. The two
fixture states agree on every narrow-aperture finite suffix and on the selected
wide suffix `[false]`, but the added wide input `[true]` distinguishes them. -/
theorem aperture_expansion_distinguishes_future :
    (narrowProfile.observe (0, true) = narrowProfile.observe (0, false)) ∧
    (((0, true) : Nat × Bool) ≠ ((0, false) : Nat × Bool)) ∧
    continuationEquivalent narrowProfile (0, true) (0, false) ∧
    oneSuffixEquivalent wideProfile (0, true) (0, false) [false] ∧
    ¬ continuationEquivalent wideProfile (0, true) (0, false) := by
  refine ⟨rfl, by decide, ?_, rfl, ?_⟩
  · apply all_finite_suffixes_of_step_simulation narrowProfile
      (fun left right : Nat × Bool => left.1 = right.1)
    · intro left right h
      exact h
    · intro input hAdmits left right hRelated
      simp [narrowProfile, narrowAperture] at hAdmits
      subst input
      change (if false && left.2 then left.1 + 1 else left.1) =
        (if false && right.2 then right.1 + 1 else right.1)
      simpa using hRelated
    · rfl
  · intro hAll
    have hSuffix := hAll [true] (by
      intro input hMem
      simp at hMem
      subst input
      exact True.intro)
    change (narrowProfile.observe (apertureStep (0, true) true) =
      narrowProfile.observe (apertureStep (0, false) true)) at hSuffix
    simp [narrowProfile, apertureStep] at hSuffix
end Experiments.Pal24Continuation








