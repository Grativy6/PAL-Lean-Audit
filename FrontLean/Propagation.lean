import Mathlib

namespace FrontLean

structure Rule (α : Type*) where
  body : Finset α
  head : α
  deriving DecidableEq

structure Basis (α : Type*) where
  root : α → Prop
  rule : Rule α → Prop

/-- A finite rooted derivation. Every conjunctive parent has its own child proof.
    A finite DAG can share these subderivations; unfolding sharing leaves validity unchanged. -/
inductive Derivation (α : Type*) : α → Type _ where
  | root (a : α) : Derivation α a
  | step (r : Rule α) (children : ∀ a, a ∈ r.body → Derivation α a) :
      Derivation α r.head

def Valid {α : Type*} (b : Basis α) {q : α} : Derivation α q → Prop
  | .root a => b.root a
  | .step r ds => b.rule r ∧ ∀ a ha, Valid b (ds a ha)

def UsesRoot {α : Type*} {q : α} : Derivation α q → α → Prop
  | .root a, x => x = a
  | .step _ ds, x => ∃ a ha, UsesRoot (ds a ha) x

def UsesRule {α : Type*} {q : α} : Derivation α q → Rule α → Prop
  | .root _, _ => False
  | .step r ds, s => s = r ∨ ∃ a ha, UsesRule (ds a ha) s

/-- Propositions 7B/7D's proof-composition core, conditional on the declared interpretation. -/
theorem derivation_sound {α : Type*} (b : Basis α) (truth : α → Prop)
    (root_sound : ∀ a, b.root a → truth a)
    (rule_sound : ∀ r, b.rule r → (∀ a, a ∈ r.body → truth a) → truth r.head)
    {q : α} (d : Derivation α q) (valid : Valid b d) : truth q := by
  induction d with
  | root a => exact root_sound a valid
  | step r ds ih =>
    exact rule_sound r valid.1 (fun a ha => ih a ha (valid.2 a ha))

/-- Proposition 1 realized in an explicit finitary rule calculus with premise substitution.
    This does not represent all possible monotone calculi. -/
theorem premise_substitution {α : Type*} (Γ Δ : α → Prop) (R : Rule α → Prop)
    (premises : ∀ a, Γ a → ∃ d : Derivation α a, Valid ⟨Δ, R⟩ d)
    {q : α} (d : Derivation α q) (valid : Valid ⟨Γ, R⟩ d) :
    ∃ e : Derivation α q, Valid ⟨Δ, R⟩ e := by
  classical
  induction d with
  | root a => exact premises a valid
  | step r ds ih =>
    have hc : ∀ a ha, ∃ e : Derivation α a, Valid ⟨Δ, R⟩ e :=
      fun a ha => ih a ha (valid.2 a ha)
    exact ⟨.step r (fun a ha => Classical.choose (hc a ha)),
      valid.1, fun a ha => Classical.choose_spec (hc a ha)⟩

/-- Proposition 7D and 7E's independent-basis clause. Only used roots/rules must agree. -/
theorem valid_under_unchanged_basis {α : Type*} {q : α} (d : Derivation α q)
    (b b' : Basis α)
    (roots : ∀ a, UsesRoot d a → (b.root a ↔ b'.root a))
    (rules : ∀ r, UsesRule d r → (b.rule r ↔ b'.rule r)) :
    Valid b d ↔ Valid b' d := by
  induction d with
  | root a => exact roots a rfl
  | step r ds ih =>
    have hr := rules r (Or.inl rfl)
    have hc : ∀ a ha, Valid b (ds a ha) ↔ Valid b' (ds a ha) := by
      intro a ha
      exact ih a ha
        (fun x hx => roots x ⟨a, ha, hx⟩)
        (fun s hs => rules s (Or.inr ⟨a, ha, hs⟩))
    exact and_congr hr (forall_congr' fun a => forall_congr' fun ha => hc a ha)

/-- A strict discovery ranking rules out a nonempty directed cycle. -/
theorem increasing_depth_no_cycle {V : Type*} (edge : V → V → Prop) (depth : V → ℕ)
    (inc : ∀ a b, edge a b → depth a < depth b) (v : V) :
    ¬ Relation.TransGen edge v v := by
  intro h
  have lift : ∀ {a b}, Relation.TransGen edge a b → depth a < depth b := by
    intro a b h
    induction h with
    | single hab => exact inc _ _ hab
    | tail hab hbc ih => exact lt_trans ih (inc _ _ hbc)
  exact (Nat.lt_irrefl (depth v)) (lift h)

/-- Proposition 2, expressed by satisfaction of every clause in the supplied sets. -/
theorem negative_core_transfer {V C : Type*} (sat : V → C → Prop)
    (core formula : Set C) (hsub : core ⊆ formula)
    (unsat : ¬ ∃ v, ∀ c ∈ core, sat v c) :
    ¬ ∃ v, ∀ c ∈ formula, sat v c := by
  rintro ⟨v, hv⟩
  exact unsat ⟨v, fun c hc => hv c (hsub hc)⟩

noncomputable def hornStep {α : Type*} (rs : Finset (Rule α)) (s : Finset α) : Finset α := by
  classical
  exact s ∪ (rs.filter (fun r => r.body ⊆ s)).image Rule.head

theorem mem_hornStep {α : Type*} (rs : Finset (Rule α)) (s : Finset α) (a : α) :
    a ∈ hornStep rs s ↔ a ∈ s ∨ ∃ r ∈ rs, r.body ⊆ s ∧ r.head = a := by
  classical
  simp only [hornStep, Finset.mem_union, Finset.mem_image, Finset.mem_filter]
  aesop

theorem hornStep_inflationary {α : Type*} (rs : Finset (Rule α)) (s : Finset α) :
    s ⊆ hornStep rs s := by
  intro a ha
  exact (mem_hornStep rs s a).2 (Or.inl ha)

theorem hornStep_monotone {α : Type*} (rs : Finset (Rule α)) : Monotone (hornStep rs) := by
  intro s t h a ha
  rcases (mem_hornStep rs s a).1 ha with ha | ⟨r, hr, hb, he⟩
  · exact (mem_hornStep rs t a).2 (Or.inl (h ha))
  · exact (mem_hornStep rs t a).2 (Or.inr ⟨r, hr, hb.trans h, he⟩)

def rounds {α : Type*} (f : Finset α → Finset α) (E : Finset α) : ℕ → Finset α
  | 0 => E
  | n + 1 => f (rounds f E n)

theorem rounds_seed {α : Type*} (f : Finset α → Finset α) (E : Finset α)
    (hi : ∀ s, s ⊆ f s) (n : ℕ) : E ⊆ rounds f E n := by
  induction n with
  | zero => exact le_rfl
  | succ n ih => exact ih.trans (hi _)

theorem stable_round_persists {α : Type*} (f : Finset α → Finset α) (E : Finset α)
    (k : ℕ) (h : rounds f E (k + 1) = rounds f E k) :
    ∀ j, rounds f E (k + j) = rounds f E k := by
  intro j
  induction j with
  | zero => simp
  | succ j ih =>
    change f (rounds f E (k + j)) = rounds f E k
    rw [ih]
    exact h

/-- Proposition 7A: a finite inflationary process has a stable round within N-|E|.
    Determinism makes that equality persist; the result does not count all operations. -/
theorem finite_stabilization {α : Type*} [Fintype α] (f : Finset α → Finset α)
    (E : Finset α) (hi : ∀ s, s ⊆ f s) :
    ∃ k ≤ Fintype.card α - E.card, rounds f E (k + 1) = rounds f E k := by
  classical
  have dichotomy : ∀ n,
      (∃ k ≤ n, rounds f E (k + 1) = rounds f E k) ∨
      E.card + n + 1 ≤ (rounds f E (n + 1)).card := by
    intro n
    induction n with
    | zero =>
      by_cases he : f E = E
      · exact Or.inl ⟨0, le_rfl, he⟩
      · right
        have hc := Finset.card_lt_card (show E ⊂ f E from
          (Finset.ssubset_iff_subset_ne).2 ⟨hi E, Ne.symm he⟩)
        simpa [rounds] using hc
    | succ n ih =>
      rcases ih with ⟨k, hk, he⟩ | hg
      · exact Or.inl ⟨k, by omega, he⟩
      · by_cases he : rounds f E (n + 1 + 1) = rounds f E (n + 1)
        · exact Or.inl ⟨n + 1, le_rfl, he⟩
        · right
          have hc := Finset.card_lt_card (show rounds f E (n + 1) ⊂ rounds f E (n + 1 + 1) from
            (Finset.ssubset_iff_subset_ne).2 ⟨hi _, Ne.symm he⟩)
          omega
  rcases dichotomy (Fintype.card α - E.card) with h | h
  · exact h
  · have he := Finset.card_le_univ E
    have hn := Finset.card_le_univ (rounds f E (Fintype.card α - E.card + 1))
    omega

/-- Leastness: every round lies in every closed superset of its seed. -/
theorem rounds_le_closed {α : Type*} (f : Finset α → Finset α) (E T : Finset α)
    (mono : Monotone f) (hET : E ⊆ T) (closed : f T = T) (n : ℕ) :
    rounds f E n ⊆ T := by
  induction n with
  | zero => exact hET
  | succ n ih =>
    change f (rounds f E n) ⊆ T
    rw [← closed]
    exact mono ih

/-- Propositions 7A/7B: specialized Horn closure has the bound and leastness. -/
theorem horn_least_closure {α : Type*} [Fintype α] (rs : Finset (Rule α)) (E : Finset α) :
    ∃ k ≤ Fintype.card α - E.card,
      let C := rounds (hornStep rs) E k
      E ⊆ C ∧ hornStep rs C = C ∧
        ∀ T, E ⊆ T → hornStep rs T = T → C ⊆ T := by
  obtain ⟨k, hk, he⟩ := finite_stabilization (hornStep rs) E (hornStep_inflationary rs)
  exact ⟨k, hk, rounds_seed _ _ (hornStep_inflationary rs) k, he,
    fun T hT hc => rounds_le_closed _ _ _ (hornStep_monotone rs) hT hc k⟩

theorem horn_rounds_sound {α : Type*} (rs : Finset (Rule α)) (E : Finset α)
    (truth : α → Prop) (hE : ∀ a ∈ E, truth a)
    (hR : ∀ r ∈ rs, (∀ a ∈ r.body, truth a) → truth r.head) :
    ∀ n a, a ∈ rounds (hornStep rs) E n → truth a := by
  intro n
  induction n with
  | zero => exact hE
  | succ n ih =>
    intro a ha
    rcases (mem_hornStep _ _ _).1 ha with ha | ⟨r, hr, hb, rfl⟩
    · exact ih a ha
    · exact hR r hr (fun p hp => ih p (hb hp))

/-- No unsupported cycle starts positive Horn propagation without a seed or empty-body rule. -/
theorem empty_seed_stays_empty {α : Type*} (rs : Finset (Rule α))
    (nonempty : ∀ r ∈ rs, r.body.Nonempty) :
    ∀ n, rounds (hornStep rs) ∅ n = ∅ := by
  have hf : hornStep rs ∅ = ∅ := by
    apply Finset.eq_empty_iff_forall_notMem.mpr
    intro a ha
    rcases (mem_hornStep _ _ _).1 ha with ha | ⟨r, hr, hb, _⟩
    · exact Finset.notMem_empty a ha
    · obtain ⟨p, hp⟩ := nonempty r hr
      exact Finset.notMem_empty p (hb hp)
  intro n
  induction n with
  | zero => rfl
  | succ n ih => simp [rounds, ih, hf]

/-- Proposition 7C's disjoint wake decomposition, for E ⊆ B ⊆ S. -/
theorem wake_decomposition {α : Type*} [DecidableEq α] (E B S : Finset α) (d : α)
    (hEB : E ⊆ B) (hBS : B ⊆ S) :
    S \ (E ∪ {d}) = ((B \ E) \ {d}) ∪ ((S \ B) \ {d}) ∧
    Disjoint ((B \ E) \ {d}) ((S \ B) \ {d}) := by
  constructor
  · ext a
    have he := @hEB a
    have hb := @hBS a
    simp only [Finset.mem_sdiff, Finset.mem_union, Finset.mem_singleton]
    tauto
  · apply Finset.disjoint_left.mpr
    intro a h₁ h₂
    exact (Finset.mem_sdiff.mp (Finset.mem_sdiff.mp h₂).1).2
      (Finset.mem_sdiff.mp (Finset.mem_sdiff.mp h₁).1).1

/-- If the seed is already in a least closed extension, adding it changes no closure. -/
theorem redundant_seed {α : Type*} [DecidableEq α]
    (f : Finset α → Finset α) (E B S : Finset α) (d : α)
    (hEB : E ⊆ B) (hd : d ∈ B) (hBC : f B = B) (hSC : f S = S)
    (hES : E ∪ {d} ⊆ S)
    (leastB : ∀ T, E ⊆ T → f T = T → B ⊆ T)
    (leastS : ∀ T, E ∪ {d} ⊆ T → f T = T → S ⊆ T) : S = B := by
  apply Finset.Subset.antisymm
  · exact leastS B (Finset.union_subset hEB (Finset.singleton_subset_iff.mpr hd)) hBC
  · exact leastB S ((Finset.subset_union_left).trans hES) hSC

end FrontLean
