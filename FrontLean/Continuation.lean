import FrontLean.Answers

namespace FrontLean
open APCILeanAudit

def runWord {S A : Type*} (δ : S → A → S) (s : S) (w : List A) : S :=
  w.foldl δ s

def FutureEq {S A Y : Type*} (δ : S → A → S) (o : S → Y) (s t : S) : Prop :=
  ∀ w, o (runWord δ s w) = o (runWord δ t w)

/-- Proposition 5: every word has its own reachable-image decoder. -/
theorem future_output_preservation {S A Y Z : Type*}
    (δ : S → A → S) (o : S → Y) (c : S → Z) :
    (∀ w, ExactOnReachable c (fun s => o (runWord δ s w))) ↔
      ∀ s t, c s = c t → FutureEq δ o s t := by
  simp only [answer_sufficiency, FutureEq]
  constructor
  · intro h s t hst w
    exact h w s t hst
  · intro h w s t hst
    exact h s t hst w

/-- Equation 19: factorization for updating the same selected representation. -/
theorem online_update_iff {S A Z : Type*} (δ : S → A → S) (c : S → Z) :
    (∃ update : Z → A → Z, ∀ s a, update (c s) a = c (δ s a)) ↔
      ∀ s t a, c s = c t → c (δ s a) = c (δ t a) := by
  classical
  constructor
  · rintro ⟨update, hu⟩ s t a hst
    rw [← hu s a, ← hu t a, hst]
  · intro h
    let update : Z → A → Z := fun z a =>
      if hz : ∃ s, c s = z then c (δ (Classical.choose hz) a) else z
    refine ⟨update, ?_⟩
    intro s a
    have hs : ∃ t, c t = c s := ⟨s, rfl⟩
    simp only [update, dif_pos hs]
    exact h _ s a (Classical.choose_spec hs)

theorem future_eq_is_right_congruence {S A Y : Type*} (δ : S → A → S)
    (o : S → Y) {s t : S} (h : FutureEq δ o s t) (a : A) :
    FutureEq δ o (δ s a) (δ t a) := by
  intro w
  exact h (a :: w)

/-- Proposition 5A in its set form. I can be the subtype of admitted pairs;
    it is not enlarged to all frame/continuation combinations. -/
theorem admitted_outputs_sufficiency {S Z I : Type*} {Y : I → Type*}
    (c : S → Z) (observed : (i : I) → S → Y i) :
    (∀ i, ExactOnReachable c (observed i)) ↔
      ∀ s t, c s = c t → ∀ i, observed i s = observed i t := by
  simp only [answer_sufficiency]
  constructor
  · intro h s t he i
    exact h i s t he
  · intro h i s t he
    exact h s t he i

private def counterCode (s : Fin 3) : Bool := s == 2
private def counterStep (s : Fin 3) (_ : Unit) : Fin 3 := if s == 0 then 0 else 2

/-- Manuscript §9 counterexample: protected outputs suffice while code updates fail. -/
theorem output_sufficient_without_online_update :
    (∀ w : List Unit, ExactOnReachable counterCode
      (fun s => (fun _ : Fin 3 => false) (runWord counterStep s w))) ∧
    ¬ (∃ update : Bool → Unit → Bool,
      ∀ s a, update (counterCode s) a = counterCode (counterStep s a)) := by
  constructor
  · intro w
    rw [answer_sufficiency]
    intros
    rfl
  · rw [online_update_iff]
    intro h
    have bad := h 0 1 () (by decide)
    change false = true at bad
    cases bad

end FrontLean
