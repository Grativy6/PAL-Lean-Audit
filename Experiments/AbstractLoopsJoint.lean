import Mathlib.Data.Set.Basic

/-!
Bounded function-level realization of Abstract Loops v1.0 P0014--P0026.
It proves only reachable-interface factorization and finite Boolean fixtures.
-/
namespace Experiments.AbstractLoopsJoint

def kernel {World Trace : Type} (trace : World → Trace) : World → World → Prop :=
  fun left right => trace left = trace right

def jointTrace {World Left Right : Type} (left : World → Left) (right : World → Right) : World → Left × Right :=
  fun world => (left world, right world)

def Reachable {World Trace : Type} (trace : World → Trace) :=
  { value : Trace // ∃ world, trace world = value }

def Certifies {World Trace Answer : Type} (answer : World → Answer) (trace : World → Trace) : Prop :=
  ∃ decode : Reachable trace → Answer, ∀ world, decode ⟨trace world, ⟨world, rfl⟩⟩ = answer world

theorem joint_kernel_eq_intersection {World Left Right : Type}
    (left : World → Left) (right : World → Right) :
    kernel (jointTrace left right) = fun first second => kernel left first second ∧ kernel right first second := by
  funext first second
  simp [kernel, jointTrace]

theorem reachable_certifies_iff_kernel_subset {World Trace Answer : Type}
    (answer : World → Answer) (trace : World → Trace) :
    Certifies answer trace ↔ ∀ first second, kernel trace first second → answer first = answer second := by
  constructor
  · rintro ⟨decode, hdecode⟩ first second hkernel
    have hreachable : (⟨trace first, ⟨first, rfl⟩⟩ : Reachable trace) =
        ⟨trace second, ⟨second, rfl⟩⟩ := Subtype.ext hkernel
    calc
      answer first = decode ⟨trace first, ⟨first, rfl⟩⟩ := (hdecode first).symm
      _ = decode ⟨trace second, ⟨second, rfl⟩⟩ := congrArg decode hreachable
      _ = answer second := hdecode second
  · intro h
    classical
    refine ⟨fun reachable => answer (Classical.choose reachable.property), ?_⟩
    intro world
    let witness : ∃ candidate : World, trace candidate = trace world := ⟨world, rfl⟩
    exact h (Classical.choose witness) world (Classical.choose_spec witness)

theorem common_collision_blocks_joint_certification {World Left Right Answer : Type}
    (left : World → Left) (right : World → Right) (answer : World → Answer) (first second : World)
    (leftCollision : left first = left second) (rightCollision : right first = right second)
    (answerConflict : answer first ≠ answer second) :
    ¬ Certifies answer (jointTrace left right) := by
  intro certified
  have hsubset := (reachable_certifies_iff_kernel_subset answer (jointTrace left right)).mp certified
  apply answerConflict
  apply hsubset first second
  simp [kernel, jointTrace, leftCollision, rightCollision]

def xorAnswer : Bool × Bool → Bool := fun pair => pair.1 != pair.2
def xorFirst : Bool × Bool → Bool := Prod.fst
def xorSecond : Bool × Bool → Bool := Prod.snd
def xorPair : Bool × Bool → Bool × Bool := fun pair => (pair.1, pair.2)

theorem xor_first_insufficient : ¬ Certifies xorAnswer xorFirst := by
  intro certified
  have hsubset := (reachable_certifies_iff_kernel_subset xorAnswer xorFirst).mp certified
  have conflict := hsubset (false, false) (false, true) (by rfl)
  simp [xorAnswer] at conflict

theorem xor_second_insufficient : ¬ Certifies xorAnswer xorSecond := by
  intro certified
  have hsubset := (reachable_certifies_iff_kernel_subset xorAnswer xorSecond).mp certified
  have conflict := hsubset (false, false) (true, false) (by rfl)
  simp [xorAnswer] at conflict

theorem xor_pair_certifies : Certifies xorAnswer xorPair := by
  refine ⟨fun reachable => xorAnswer reachable.1, ?_⟩
  intro pair
  rfl

theorem xor_strict_joint_sufficiency :
    Certifies xorAnswer xorPair ∧ ¬ Certifies xorAnswer xorFirst ∧ ¬ Certifies xorAnswer xorSecond := by
  exact ⟨xor_pair_certifies, xor_first_insufficient, xor_second_insufficient⟩

def collapsedTrace : Bool × Bool → Bool := fun _ => false
def firstBitAnswer : Bool × Bool → Bool := Prod.fst

theorem common_collision_negative_fixture :
    kernel collapsedTrace (false, false) (true, false) ∧
      firstBitAnswer (false, false) ≠ firstBitAnswer (true, false) := by
  simp [kernel, collapsedTrace, firstBitAnswer]

theorem common_collision_negative_blocks_joint :
    ¬ Certifies firstBitAnswer (jointTrace collapsedTrace collapsedTrace) := by
  exact common_collision_blocks_joint_certification collapsedTrace collapsedTrace firstBitAnswer
    (false, false) (true, false) rfl rfl (by simp [firstBitAnswer])

end Experiments.AbstractLoopsJoint
