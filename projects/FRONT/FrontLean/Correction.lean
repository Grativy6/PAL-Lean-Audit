import FrontLean.Propagation

namespace FrontLean

/-- C1: existence in the finite recorded set; no completeness for truth is asserted. -/
def RecordedSupport {α : Type*} (b : Basis α) {q : α} {n : ℕ}
    (recorded : Fin n → Derivation α q) : Prop := ∃ i, Valid b (recorded i)

/-- Proposition 7E's truth clause follows through the actual returned derivation. -/
theorem recorded_support_sound {α : Type*} (b : Basis α) (truth : α → Prop)
    (roots : ∀ a, b.root a → truth a)
    (rules : ∀ r, b.rule r → (∀ a ∈ r.body, truth a) → truth r.head)
    {q : α} {n : ℕ} (recorded : Fin n → Derivation α q)
    (h : RecordedSupport b recorded) : truth q := by
  obtain ⟨i, hi⟩ := h
  exact derivation_sound b truth roots rules (recorded i) hi

theorem unchanged_alternative_survives {α : Type*} {q : α} {n : ℕ}
    (b b' : Basis α) (recorded : Fin n → Derivation α q) (i : Fin n)
    (hi : Valid b (recorded i))
    (hr : ∀ a, UsesRoot (recorded i) a → (b.root a ↔ b'.root a))
    (hs : ∀ r, UsesRule (recorded i) r → (b.rule r ↔ b'.rule r)) :
    RecordedSupport b' recorded :=
  ⟨i, (valid_under_unchanged_basis (recorded i) b b' hr hs).mp hi⟩

inductive RepairStatus where
  | unchangedSupported | notAuthorized | committed | unresolved
  deriving DecidableEq, Repr

inductive RepairEvent (σ : Type*) where
  | proposed (candidate : σ)
  | appliedScratch (candidate : σ)
  | failedRevalidation (candidate : σ)
  | rollback (original : σ)
  | committed (candidate : σ)
  | returned (status : RepairStatus)
  deriving DecidableEq, Repr

structure RepairResult (σ : Type*) where
  value : σ
  history : List (RepairEvent σ)
  status : RepairStatus

/-- Explicit pure scratch transition matching the paper's four outcome branches.
    Grant and postcondition refer to this fixed call; no concurrency or external effects. -/
noncomputable def scratchRepair {σ : Type*} (original candidate : σ)
    (grant : Prop) (post : σ → Prop) (history : List (RepairEvent σ)) : RepairResult σ := by
  classical
  let start := history ++ [.proposed candidate]
  exact if candidate = original then
    if post original then ⟨original, start ++ [.returned .unchangedSupported], .unchangedSupported⟩
    else ⟨original, start ++ [.returned .unresolved], .unresolved⟩
  else if grant then
    if post candidate then
      ⟨candidate, start ++ [.appliedScratch candidate, .committed candidate, .returned .committed], .committed⟩
    else
      ⟨original, start ++ [.appliedScratch candidate, .failedRevalidation candidate,
        .rollback original, .returned .unresolved], .unresolved⟩
  else ⟨original, start ++ [.returned .notAuthorized], .notAuthorized⟩

/-- 7E: a modeled changed-state commit has both guards. -/
theorem scratch_commit_iff {σ : Type*} (original candidate : σ)
    (grant : Prop) (post : σ → Prop) (history : List (RepairEvent σ)) :
    (scratchRepair original candidate grant post history).status = .committed ↔
      candidate ≠ original ∧ grant ∧ post candidate := by
  classical
  simp only [scratchRepair]
  split_ifs <;> simp_all

theorem failed_scratch_keeps_original {σ : Type*} (original candidate : σ)
    (grant : Prop) (post : σ → Prop) (history : List (RepairEvent σ))
    (hn : (scratchRepair original candidate grant post history).status ≠ .committed) :
    (scratchRepair original candidate grant post history).value = original := by
  classical
  unfold scratchRepair at *
  split_ifs at * <;> simp_all

def HistoryPrefix {E : Type*} (old new : List E) : Prop := ∃ suffix, new = old ++ suffix

theorem history_prefix_refl {E : Type*} (h : List E) : HistoryPrefix h h :=
  ⟨[], (List.append_nil h).symm⟩

theorem history_prefix_trans {E : Type*} {a b c : List E}
    (hab : HistoryPrefix a b) (hbc : HistoryPrefix b c) : HistoryPrefix a c := by
  obtain ⟨x, rfl⟩ := hab
  obtain ⟨y, rfl⟩ := hbc
  exact ⟨x ++ y, List.append_assoc _ _ _⟩

/-- Both successful and unsuccessful transitions retain their complete original prefix. -/
theorem scratch_preserves_history {σ : Type*} (original candidate : σ)
    (grant : Prop) (post : σ → Prop) (history : List (RepairEvent σ)) :
    HistoryPrefix history (scratchRepair original candidate grant post history).history := by
  classical
  unfold scratchRepair
  split_ifs <;> exact ⟨_, List.append_assoc _ _ _⟩

/-- 7E's finite transition induction, without assuming that every attempt succeeded. -/
theorem finite_history_preservation {E : Type*} (history : ℕ → List E) (n : ℕ)
    (steps : ∀ i, i < n → HistoryPrefix (history i) (history (i + 1))) :
    HistoryPrefix (history 0) (history n) := by
  induction n with
  | zero => exact history_prefix_refl _
  | succ n ih =>
    exact history_prefix_trans (ih (fun i hi => steps i (by omega))) (steps n (by omega))

/-- A revalidated candidate may fail an additional protected constraint. -/
theorem failed_secondary_condition_is_recorded {σ : Type*} (original candidate : σ)
    (post : σ → Prop) (history : List (RepairEvent σ))
    (different : candidate ≠ original) (failed : ¬ post candidate) :
    (scratchRepair original candidate True post history).value = original ∧
    RepairEvent.failedRevalidation candidate ∈
      (scratchRepair original candidate True post history).history := by
  simp [scratchRepair, different, failed]

inductive TestAtom where
  | p | a | b | q
  deriving DecidableEq, Fintype

private def oldRoute : Derivation TestAtom .q :=
  .step (⟨{TestAtom.p}, TestAtom.q⟩ : Rule TestAtom) (fun atom _ => .root atom)
private def alternativeRoute : Derivation TestAtom .q :=
  .step (⟨{TestAtom.a, TestAtom.b}, TestAtom.q⟩ : Rule TestAtom) (fun atom _ => .root atom)
private def correctedBasis : Basis TestAtom :=
  ⟨fun atom => atom = .a ∨ atom = .b, fun _ => True⟩

/-- A supported conclusion does not repair the old invalid receipt for it. -/
theorem independent_answer_invalid_receipt :
    ¬ Valid correctedBasis oldRoute ∧ Valid correctedBasis alternativeRoute := by
  simp [Valid, oldRoute, alternativeRoute, correctedBasis]

/-- Every AND parent matters, even when the alternative's head matches the requested answer. -/
theorem missing_conjunct_is_rejected :
    ¬ Valid (Basis.mk (fun atom : TestAtom => atom = .a) (fun _ => True)) alternativeRoute := by
  simp [Valid, alternativeRoute]

/-- A finite recorded set can be exhausted while a true query lies outside it. -/
theorem no_recorded_proof_is_not_negation :
    ∃ (truth : Unit → Prop) (b : Basis Unit) (r : Fin 0 → Derivation Unit ()),
      ¬ RecordedSupport b r ∧ truth () := by
  refine ⟨fun _ => True, ⟨fun _ => False, fun _ => False⟩, Fin.elim0, ?_, trivial⟩
  simp [RecordedSupport]

/-- An unchanged supported state needs no mutation grant. -/
theorem unchanged_does_not_require_mutation_grant {σ : Type*} (s : σ)
    (post : σ → Prop) (h : post s) (history : List (RepairEvent σ)) :
    (scratchRepair s s False post history).status = .unchangedSupported := by
  simp [scratchRepair, h]

end FrontLean
