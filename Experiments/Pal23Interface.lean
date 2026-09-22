import Mathlib.Data.Bool.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Set.Basic

/-!
# PAL v2.3 M-INTERFACE-FIBER coverage

Set-theoretic relations for lost distinctions, auxiliary labels, trace
postprocessing, question coarsening, joint traces, and a finite label bound.
These declarations test only their stated functions and finite model.
-/
namespace Experiments.Pal23Interface

universe uW uT uQ uS uA

/-- Source pairs that collide under a trace but differ on the requested answer. -/
def lostDistinctions {W : Type uW} {T : Type uT} {Q : Type uQ}
    (trace : W → T) (answer : W → Q) : Set (W × W) :=
  {p | trace p.1 = trace p.2 ∧ answer p.1 ≠ answer p.2}

/-- Source pairs that collide under an auxiliary label. -/
def labelKernel {W : Type uW} {S : Type uS} (label : W → S) : Set (W × W) :=
  {p | label p.1 = label p.2}

/-- A joint trace loses exactly the distinctions lost by both components. -/
theorem joint_label_lost_eq_intersection {W : Type uW} {T : Type uT} {Q : Type uQ} {S : Type uS}
    (trace : W → T) (label : W → S) (answer : W → Q) :
    lostDistinctions (fun w => (trace w, label w)) answer =
      lostDistinctions trace answer ∩ labelKernel label := by
  ext p
  simp only [lostDistinctions, labelKernel, Set.mem_setOf_eq,
    Set.mem_inter_iff, Prod.mk.injEq, and_assoc]
  constructor
  · rintro ⟨htrace, hlabel, hanswer⟩
    exact ⟨htrace, hanswer, hlabel⟩
  · rintro ⟨htrace, hanswer, hlabel⟩
    exact ⟨htrace, hlabel, hanswer⟩

/-- Deterministic trace postprocessing preserves old lost distinctions and may add new ones. -/
theorem trace_postprocess_lost_subset {W : Type uW} {T : Type uT} {U : Type uS} {Q : Type uQ}
    (trace : W → T) (postprocess : T → U) (answer : W → Q) :
    lostDistinctions trace answer ⊆ lostDistinctions (postprocess ∘ trace) answer := by
  intro p hp
  exact ⟨congrArg postprocess hp.1, hp.2⟩

/-- Appending a deterministic restatement of a trace leaves its lost distinctions unchanged. -/
theorem redundant_trace_restatement_lost_eq {W : Type uW} {T : Type uT} {U : Type uS} {Q : Type uQ}
    (trace : W → T) (restate : T → U) (answer : W → Q) :
    lostDistinctions (fun w => (trace w, restate (trace w))) answer =
      lostDistinctions trace answer := by
  ext p
  simp only [lostDistinctions, Set.mem_setOf_eq, Prod.mk.injEq, and_assoc]
  constructor
  · rintro ⟨htrace, _, hanswer⟩
    exact ⟨htrace, hanswer⟩
  · rintro ⟨htrace, hanswer⟩
    exact ⟨htrace, congrArg restate htrace, hanswer⟩

/-- Postprocessing the answer can only remove lost distinctions. -/
theorem question_coarsening_lost_subset {W : Type uW} {T : Type uT} {Q : Type uQ} {R : Type uS}
    (trace : W → T) (answer : W → Q) (coarsen : Q → R) :
    lostDistinctions trace (coarsen ∘ answer) ⊆ lostDistinctions trace answer := by
  intro p hp
  refine ⟨hp.1, ?_⟩
  intro heq
  exact hp.2 (congrArg coarsen heq)

/-- A concrete strict coarsening: the identity question loses a pair, the constant question does not. -/
theorem question_coarsening_strict_countercase :
    let trace : Bool → Unit := fun _ => ()
    let answer : Bool → Bool := id
    let coarsen : Bool → Bool := fun _ => false
    ((false, true) : Bool × Bool) ∈ lostDistinctions trace answer ∧
      lostDistinctions trace (coarsen ∘ answer) = ∅ := by
  simp [lostDistinctions]

/-- Each XOR projection has a lost distinction, while their joint trace decodes the answer. -/
theorem xor_joint_trace_strict_sufficiency_fixture :
    let answer : Bool × Bool → Bool := fun p => if p.1 then !p.2 else p.2
    let first : Bool × Bool → Bool := Prod.fst
    let second : Bool × Bool → Bool := Prod.snd
    let joint : Bool × Bool → Bool × Bool := fun p => (p.1, p.2)
    let decode : Bool × Bool → Bool := fun p => if p.1 then !p.2 else p.2
    ((false, false), (false, true)) ∈ lostDistinctions first answer ∧
      ((false, false), (true, false)) ∈ lostDistinctions second answer ∧
      ∀ p, decode (joint p) = answer p := by
  simp [lostDistinctions]

/-- Any label sufficient for a finite family of pairwise answer-distinct states in one trace fiber is injective on that family. -/
theorem finite_label_lower_bound {A : Type uA} {W : Type uW} {T : Type uT} {Q : Type uQ}
    {S : Type uS} [Fintype A] [Fintype S]
    (states : A → W) (trace : W → T) (answer : W → Q) (label : W → S)
    (sameTrace : ∀ a b, trace (states a) = trace (states b))
    (answerSeparates : ∀ {a b}, answer (states a) = answer (states b) → a = b)
    (jointSufficient : ∀ {a b},
      trace (states a) = trace (states b) → label (states a) = label (states b) →
        answer (states a) = answer (states b)) :
    Fintype.card A ≤ Fintype.card S := by
  apply Fintype.card_le_of_injective (fun a => label (states a))
  intro a b hlabel
  apply answerSeparates
  exact jointSufficient (sameTrace a b) hlabel

end Experiments.Pal23Interface
