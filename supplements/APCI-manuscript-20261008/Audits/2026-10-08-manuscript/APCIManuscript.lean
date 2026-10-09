import APCILeanAudit

/-
APCI v1.0.0 source supplement, 2026-10-08.
This file is separate from the frozen fifteen-declaration development.
The one new coverage item is the written corollary in section 4.1.
The remaining declarations are explicitly boundary controls.
-/

namespace APCIManuscript

open APCILeanAudit

universe uW uT uQ

/-- At most n actual reachable traces, regardless of the ambient trace type. -/
def ReachableCapacity {W : Type uW} {T : Type uT}
    (trace : W → T) (n : Nat) : Prop :=
  ∃ label : Reachable trace → Fin n, Function.Injective label

/-- Section 4.1, DOCX P0072-P0073: even just these witnesses cannot be decoded. -/
theorem no_exact_on_witness_of_capacity
    {W : Type uW} {T : Type uT} {Q : Type uQ}
    (trace : W → T) (answer : W → Q) (n : Nat)
    (witness : Fin (n + 1) → W)
    (capacity : ReachableCapacity trace n)
    (distinctAnswers : Function.Injective (answer ∘ witness)) :
    ¬ ExactOnReachable (trace ∘ witness) (answer ∘ witness) := by
  rcases capacity with ⟨label, label_injective⟩
  let encode : Fin (n + 1) → Fin n :=
    fun i => label ⟨trace (witness i), ⟨witness i, rfl⟩⟩
  rcases fin_succ_has_collision n encode with ⟨i, j, different, sameCode⟩
  have sameReachable :
      (⟨trace (witness i), ⟨witness i, rfl⟩⟩ : Reachable trace) =
      ⟨trace (witness j), ⟨witness j, rfl⟩⟩ := label_injective sameCode
  have sameTrace : (trace ∘ witness) i = (trace ∘ witness) j :=
    congrArg Subtype.val sameReachable
  intro exactWitnesses
  exact different (distinctAnswers
    (exactOnReachable_implies_fiberConstant exactWitnesses sameTrace))

/-- Sections 2 and 7.1: infinite worlds and collisions do not obstruct a constant answer. -/
theorem infinite_world_constant_property :
    (¬ Function.Injective (fun _ : Nat => ())) ∧
    ExactCertificate (fun _ : Nat => ()) (fun _ => false) := by
  constructor
  · intro h
    have impossible : (0 : Nat) = 1 := h rfl
    cases impossible
  · exact ⟨fun _ => false, fun _ => rfl⟩

/-- Sections 2 and 7.3: an added bit changes the interface and can restore identity. -/
theorem side_information_changes_interface :
    (¬ ExactCertificate (fun _ : Bool => ()) (fun b => b)) ∧
    ExactCertificate (fun b : Bool => ((), b)) (fun b => b) := by
  constructor
  · intro h
    have impossible : false = true :=
      exactCertificate_implies_fiberConstant h (x := false) (y := true) rfl
    cases impossible
  · exact ⟨fun t => t.2, fun _ => rfl⟩

/-- Section 3.1: an inhabited answer is sufficient, but is not necessary. -/
theorem empty_trace_allows_empty_answer :
    ExactCertificate (fun x : Empty => x) (fun x => x) := by
  exact ⟨fun x => x, fun _ => rfl⟩

end APCIManuscript

#print axioms APCIManuscript.no_exact_on_witness_of_capacity
#print axioms APCIManuscript.infinite_world_constant_property
#print axioms APCIManuscript.side_information_changes_interface
#print axioms APCIManuscript.empty_trace_allows_empty_answer
