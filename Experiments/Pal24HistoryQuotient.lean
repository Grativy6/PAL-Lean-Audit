import Mathlib.Data.List.Basic

set_option pp.fullNames true

/-!
# C6: task-relative right-congruence of history equivalence

The model uses all finite lists as histories and all finite lists as continuations.
Restricted continuation apertures are modeled separately and require an explicit
prefix-closure hypothesis for right congruence.
-/
namespace Experiments.Pal24HistoryQuotient

/-- Two histories are equivalent when every finite continuation yields the same task observation. -/
def futureEquivalent {Alphabet Observation : Type}
    (observe : List Alphabet → Observation) (left right : List Alphabet) : Prop :=
  ∀ suffix : List Alphabet, observe (left ++ suffix) = observe (right ++ suffix)

theorem futureEquivalent_refl {Alphabet Observation : Type}
    (observe : List Alphabet → Observation) (history : List Alphabet) :
    futureEquivalent observe history history := by
  intro suffix
  rfl

theorem futureEquivalent_symm {Alphabet Observation : Type}
    (observe : List Alphabet → Observation) {left right : List Alphabet} :
    futureEquivalent observe left right → futureEquivalent observe right left := by
  intro h suffix
  exact (h suffix).symm

theorem futureEquivalent_trans {Alphabet Observation : Type}
    (observe : List Alphabet → Observation) {first second third : List Alphabet} :
    futureEquivalent observe first second →
      futureEquivalent observe second third → futureEquivalent observe first third := by
  intro h₁ h₂ suffix
  exact (h₁ suffix).trans (h₂ suffix)

/-- Future-task equivalence is preserved by appending any common finite task suffix. -/
theorem futureEquivalent_right_congruent {Alphabet Observation : Type}
    (observe : List Alphabet → Observation) {left right : List Alphabet}
    (h : futureEquivalent observe left right) (extension : List Alphabet) :
    futureEquivalent observe (left ++ extension) (right ++ extension) := by
  intro suffix
  simpa [List.append_assoc] using h (extension ++ suffix)

def futureSetoid {Alphabet Observation : Type}
    (observe : List Alphabet → Observation) : Setoid (List Alphabet) where
  r := futureEquivalent observe
  iseqv := {
    refl := by
      intro history
      exact futureEquivalent_refl observe history
    symm := by
      intro left right h
      exact futureEquivalent_symm observe h
    trans := by
      intro first second third h₁ h₂
      exact futureEquivalent_trans observe h₁ h₂
  }

theorem futureEquivalent_implies_current_observation {Alphabet Observation : Type}
    (observe : List Alphabet → Observation) {left right : List Alphabet}
    (h : futureEquivalent observe left right) : observe left = observe right := by
  simpa [futureEquivalent] using h []

/-- The canonical class assigned to each history in the task-relative quotient. -/
def historyClass {Alphabet Observation : Type}
    (observe : List Alphabet → Observation) (history : List Alphabet) :
    Quotient (futureSetoid observe) :=
  Quotient.mk (futureSetoid observe) history

theorem historyClass_eq_iff_futureEquivalent {Alphabet Observation : Type}
    (observe : List Alphabet → Observation) (left right : List Alphabet) :
    historyClass observe left = historyClass observe right ↔ futureEquivalent observe left right := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- The task observation descends to future-equivalence classes. -/
def quotientObservation {Alphabet Observation : Type}
    (observe : List Alphabet → Observation) :
    Quotient (futureSetoid observe) → Observation :=
  Quotient.lift observe (fun _ _ h => futureEquivalent_implies_current_observation observe h)

/-- A restricted continuation aperture is a supplied predicate on finite suffixes. -/
def futureEquivalentOnAperture {Alphabet Observation : Type}
    (aperture : List Alphabet → Prop) (observe : List Alphabet → Observation)
    (left right : List Alphabet) : Prop :=
  ∀ suffix, aperture suffix → observe (left ++ suffix) = observe (right ++ suffix)

/--
Right congruence under a restricted aperture explicitly requires closure under
prefixing the newly appended task symbol. Without this closure, the old
future-equivalence premise may not cover the shifted suffix.
-/
theorem apertureFutureEquivalent_right_congruent {Alphabet Observation : Type}
    (aperture : List Alphabet → Prop) (observe : List Alphabet → Observation)
    {left right : List Alphabet} (h : futureEquivalentOnAperture aperture observe left right)
    (task : Alphabet)
    (continuationClosed : ∀ suffix, aperture suffix → aperture (task :: suffix)) :
    futureEquivalentOnAperture aperture observe (left ++ [task]) (right ++ [task]) := by
  intro suffix hsuffix
  have shifted := h (task :: suffix) (continuationClosed suffix hsuffix)
  calc
    observe ((left ++ [task]) ++ suffix) = observe (left ++ (task :: suffix)) := by simp [List.append_assoc]
    _ = observe (right ++ (task :: suffix)) := shifted
    _ = observe ((right ++ [task]) ++ suffix) := by simp [List.append_assoc]

def constantTask : List Bool → Bool := fun _ => false

def headTask : List Bool → Option Bool := List.head?

theorem constantTask_one_class :
    ∀ left right : List Bool, futureEquivalent constantTask left right := by
  intro left right suffix
  rfl

theorem constantTask_quotient_subsingleton :
    Subsingleton (Quotient (futureSetoid constantTask)) := by
  constructor
  intro left right
  refine Quotient.inductionOn₂ left right ?_
  intro h₁ h₂
  exact Quotient.sound (constantTask_one_class h₁ h₂)

theorem headTask_distinguishes_histories :
    ¬ futureEquivalent headTask [] [false] := by
  intro h
  have hnow := h []
  change none = some false at hnow
  cases hnow

theorem task_mutation_changes_future_equivalence :
    futureEquivalent constantTask [] [false] ∧ ¬ futureEquivalent headTask [] [false] := by
  exact ⟨constantTask_one_class [] [false], headTask_distinguishes_histories⟩

/--
An aperture admitting only the empty suffix is not closed under prefixing `false`.
For `observe xs = xs.length / 2`, the histories `[]` and `[false]` agree on that
aperture (0/2 = 1/2 = 0), but after common extension `[false]`, the resulting
lengths 1 and 2 have observations 0 and 1. Thus restricted right congruence
fails when its displayed closure premise is omitted.
-/
theorem aperture_closure_is_load_bearing :
    (¬ ∀ suffix : List Bool, suffix = [] → false :: suffix = []) ∧
      futureEquivalentOnAperture (fun suffix : List Bool => suffix = [])
        (fun history : List Bool => history.length / 2) [] [false] ∧
      ¬ futureEquivalentOnAperture (fun suffix : List Bool => suffix = [])
        (fun history : List Bool => history.length / 2) [false] [false, false] := by
  constructor
  · intro h
    have notEmpty : false :: ([] : List Bool) ≠ [] := by decide
    exact notEmpty (h [] rfl)
  constructor
  · intro suffix hsuffix
    subst suffix
    rfl
  · intro h
    have hzero := h [] rfl
    have hne : (1 : Nat) / 2 ≠ 2 / 2 := by decide
    exact hne hzero

end Experiments.Pal24HistoryQuotient
