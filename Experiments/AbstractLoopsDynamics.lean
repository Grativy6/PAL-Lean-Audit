import Experiments.AbstractLoopsJoint
import Mathlib.Tactic

/-!
AL-B, Abstract Loops v1.0 P0048-P0062. Supplied protocols, supports and run classes.
Runs carry explicit finite or infinite time domains. Fairness is not assumed implicitly.
-/
namespace Experiments.AbstractLoopsDynamics

set_option autoImplicit false

open AbstractLoopsJoint

theorem uniform_trace_protocol_certifies {W T Choice Q : Type}
    (trace : W → T) (q : W → Q) (strategy : T → Choice) (read : T → Choice → Q)
    (correct : ∀ w, read (trace w) (strategy (trace w)) = q w) : Certifies q trace := by
  exact ⟨fun z => read z.val (strategy z.val), correct⟩

/-- A trace-indexed nondeterministic protocol also suffices when every allowed output is correct
and at least one output is available at every reachable trace. -/
theorem uniform_nondeterministic_protocol_certifies {W T Q : Type}
    (trace : W → T) (q : W → Q) (outputs : T → Set Q)
    (live : ∀ w, (outputs (trace w)).Nonempty)
    (correct : ∀ w o, o ∈ outputs (trace w) → o = q w) : Certifies q trace := by
  apply (reachable_certifies_iff_kernel_subset q trace).mpr
  intro u v h
  change trace u = trace v at h
  obtain ⟨o, ho⟩ := live u
  have hov : o ∈ outputs (trace v) := by rw [← h]; exact ho
  exact (correct u o ho).symm.trans (correct v o hov)

/-- An oracle selecting the favorable branch separately at each world is not a trace decoder. -/
theorem pointwise_branch_not_certification :
    (∀ w : Bool, ∃ choice : Bool, choice = w) ∧
      ¬ Certifies (id : Bool → Bool) (fun _ => ()) := by
  refine ⟨fun w => ⟨w, rfl⟩, ?_⟩
  intro h
  have hc := (reachable_certifies_iff_kernel_subset id (fun _ : Bool => ())).mp h
    false true rfl
  cases hc

theorem independent_branch_label_not_world_information (choice : Bool) :
    ¬ Certifies (id : Bool → Bool) (fun _ => ((), choice)) := by
  intro h
  have hc := (reachable_certifies_iff_kernel_subset id
    (fun _ : Bool => ((), choice))).mp h false true rfl
  cases hc

/-- A constant-true answer has a decoder, but a machine restricted to false cannot implement it. -/
theorem certification_not_implementation :
    Certifies (fun _ : Unit => true) (fun _ => ()) ∧
      ¬ ∃ output : Unit → Bool, (∀ t, output t = false) ∧ (∀ _w : Unit, output () = true) := by
  refine ⟨⟨fun _ => true, fun _ => rfl⟩, ?_⟩
  rintro ⟨output, allowed, correct⟩
  have h := (allowed ()).symm.trans (correct ())
  cases h

def surplus {S : Type} (coupled baseline : Set S) : Set S := coupled \ baseline

def observableSurplus {S O : Type} (read : S → O) (coupled baseline : Set S) : Set O :=
  read '' coupled \ read '' baseline

/-- The finite supports used below arise from an actual transition relation and common initializer. -/
theorem one_jump_reachable_support {S : Type} (start finish : S) :
    {s | Relation.ReflTransGen (fun x y => x = start ∧ y = finish) start s} =
      ({start, finish} : Set S) := by
  ext s
  constructor
  · intro h
    induction h with
    | refl => exact Or.inl rfl
    | tail _ hstep _ => exact Or.inr hstep.2
  · intro h
    rcases h with h | h
    · subst s; exact .refl
    · change s = finish at h
      subst s
      exact .single ⟨rfl, rfl⟩

theorem observable_surplus_requires_raw_surplus {S O : Type}
    (read : S → O) (coupled baseline : Set S)
    (h : (observableSurplus read coupled baseline).Nonempty) :
    (surplus coupled baseline).Nonempty := by
  rcases h with ⟨o, ⟨s, hsc, rfl⟩, hnot⟩
  refine ⟨s, hsc, ?_⟩
  intro hsb
  exact hnot ⟨s, hsb, rfl⟩

theorem surplus_does_not_mean_enlargement :
    (surplus ({0, 1} : Set (Fin 3)) {0, 2}).Nonempty ∧
    (surplus ({0, 2} : Set (Fin 3)) {0, 1}).Nonempty ∧
    ¬ ({0, 1} : Set (Fin 3)) ⊆ {0, 2} ∧ ¬ ({0, 2} : Set (Fin 3)) ⊆ {0, 1} := by
  refine ⟨⟨1, by simp [surplus]⟩, ⟨2, by simp [surplus]⟩, ?_, ?_⟩
  · intro h; have := h (by simp : (1 : Fin 3) ∈ ({0, 1} : Set (Fin 3))); simp at this
  · intro h; have := h (by simp : (2 : Fin 3) ∈ ({0, 2} : Set (Fin 3))); simp at this

theorem hidden_coordinate_surplus :
    (surplus ({(false, false), (false, true)} : Set (Bool × Bool)) {(false, false)}).Nonempty ∧
    observableSurplus Prod.fst ({(false, false), (false, true)} : Set (Bool × Bool))
      {(false, false)} = ∅ := by
  constructor
  · exact ⟨(false, true), by simp [surplus]⟩
  · simp [observableSurplus, Set.image_insert_eq]

/-- A finite run includes its last state; no values outside its finite index type exist. -/
inductive Run (S : Type) where
  | infinite (stateAt : Nat → S)
  | finite (last : Nat) (stateAt : Fin (last + 1) → S)

def Visits {S : Type} (failure : S → Prop) : Run S → Prop
  | .infinite stateAt => ∃ n, failure (stateAt n)
  | .finite _ stateAt => ∃ n, failure (stateAt n)

/-- Finite completeness here means a maximal finite path, ending with no outgoing transition. -/
def Complete {S : Type} (step : S → S → Prop) (initial : S) : Run S → Prop
  | .infinite stateAt => stateAt 0 = initial ∧ ∀ n, step (stateAt n) (stateAt (n + 1))
  | .finite last stateAt =>
      stateAt ⟨0, by omega⟩ = initial ∧
      (∀ n (hn : n < last), step (stateAt ⟨n, by omega⟩) (stateAt ⟨n + 1, by omega⟩)) ∧
      ¬ ∃ next, step (stateAt ⟨last, by omega⟩) next

def Possible {S : Type} (runs : Set (Run S)) (failure : S → Prop) : Prop :=
  ∃ run ∈ runs, Visits failure run

def Inevitable {S : Type} (runs : Set (Run S)) (failure : S → Prop) : Prop :=
  ∀ run ∈ runs, Visits failure run

theorem nonempty_inevitable_implies_possible {S : Type}
    (runs : Set (Run S)) (failure : S → Prop)
    (hne : runs.Nonempty) (hi : Inevitable runs failure) : Possible runs failure := by
  rcases hne with ⟨r, hr⟩
  exact ⟨r, hr, hi r hr⟩

theorem empty_run_class_is_vacuous :
    Inevitable (∅ : Set (Run Bool)) (fun b => b = true) ∧
    ¬ Possible (∅ : Set (Run Bool)) (fun b => b = true) := by
  simp [Inevitable, Possible]

def forkStep (a b : Bool) : Prop := a = false ∨ b = true
def waitingRun : Run Bool := .infinite (fun _ => false)
def failingRun : Run Bool := .infinite (fun n => if n = 0 then false else true)
def forkRuns : Set (Run Bool) := {waitingRun, failingRun}

theorem fork_runs_are_complete_and_nonempty :
    forkRuns.Nonempty ∧ ∀ r ∈ forkRuns, Complete forkStep false r := by
  refine ⟨⟨waitingRun, by simp [forkRuns]⟩, ?_⟩
  intro r hr
  simp only [forkRuns, Set.mem_insert_iff, Set.mem_singleton_iff] at hr
  rcases hr with rfl | rfl
  · simp [Complete, waitingRun, forkStep]
  · simp [Complete, failingRun, forkStep]

theorem possible_not_inevitable :
    Possible forkRuns (fun b => b = true) ∧ ¬ Inevitable forkRuns (fun b => b = true) := by
  constructor
  · refine ⟨failingRun, by simp [forkRuns], ?_⟩
    exact ⟨1, rfl⟩
  · intro hi
    have h := hi waitingRun (by simp [forkRuns])
    simp [Visits, waitingRun] at h

/-- Removing the permanently waiting path is an explicit run-class restriction. -/
theorem restricted_run_class_changes_inevitability :
    ({failingRun} : Set (Run Bool)).Nonempty ∧
      Inevitable {failingRun} (fun b => b = true) := by
  refine ⟨⟨failingRun, rfl⟩, ?_⟩
  intro r hr
  have heq : r = failingRun := hr
  subst r
  exact ⟨1, rfl⟩

theorem absorbing_failure_persists {S : Type} (step : S → S → Prop) (failure : S → Prop)
    (absorbing : ∀ a b, failure a → step a b → failure b)
    (stateAt : Nat → S) (valid : ∀ n, step (stateAt n) (stateAt (n + 1)))
    (n : Nat) (entered : failure (stateAt n)) : ∀ k, failure (stateAt (n + k)) := by
  intro k
  induction k with
  | zero => simpa using entered
  | succ k ih => exact absorbing _ _ ih (valid (n + k))

theorem transient_visit_need_not_persist :
    Complete (fun _ _ : Bool => True) true (.infinite (fun n => n == 0)) ∧
    Visits (fun b => b = true) (.infinite (fun n => n == 0)) ∧
      (fun n : Nat => n == 0) 1 = false := by
  exact ⟨⟨rfl, fun _ => trivial⟩, ⟨0, rfl⟩, rfl⟩

/-- A one-state deadlock is a complete finite run, with no fictional later observations. -/
theorem maximal_finite_run_fixture :
    Complete (fun _ _ : Bool => False) false (.finite 0 (fun _ => false)) ∧
      ¬ Visits (fun b => b = true) (.finite 0 (fun _ : Fin 1 => false)) := by
  simp [Complete, Visits]

end Experiments.AbstractLoopsDynamics
