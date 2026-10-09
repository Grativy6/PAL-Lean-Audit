import Experiments.AbstractLoopsPostprocessing
import Mathlib.Data.Set.Card
import Mathlib.Tactic

/-!
AL-A, Abstract Loops v1.0 P0014-P0026 and P0045-P0046.
Finite reachable images, not finite worlds; a fixed supplied schedule, no fresh input.
All capacities below count reachable values. No physical interpretation is inferred.
-/
namespace Experiments.AbstractLoopsFiniteImage

set_option autoImplicit false

open AbstractLoopsJoint AbstractLoopsPostprocessing

/-- Embed the reachable joint support into the product of reachable supports. -/
def jointSupportEmbedding {W A B : Type} (a : W → A) (b : W → B) :
    Reachable (jointTrace a b) → Reachable a × Reachable b := fun z =>
  (⟨z.val.1, by rcases z.property with ⟨w, hw⟩; exact ⟨w, congrArg Prod.fst hw⟩⟩,
   ⟨z.val.2, by rcases z.property with ⟨w, hw⟩; exact ⟨w, congrArg Prod.snd hw⟩⟩)

theorem joint_support_embedding_injective {W A B : Type} (a : W → A) (b : W → B) :
    Function.Injective (jointSupportEmbedding a b) := by
  intro x y h
  apply Subtype.ext
  exact Prod.ext (congrArg (fun z => z.1.val) h) (congrArg (fun z => z.2.val) h)

theorem joint_support_finite {W A B : Type} (a : W → A) (b : W → B)
    [Finite (Reachable a)] [Finite (Reachable b)] : Finite (Reachable (jointTrace a b)) :=
  Finite.of_injective _ (joint_support_embedding_injective a b)

theorem joint_capacity_bound {W A B : Type} (a : W → A) (b : W → B)
    [Finite (Reachable a)] [Finite (Reachable b)] :
    Nat.card (Reachable (jointTrace a b)) ≤ Nat.card (Reachable a) * Nat.card (Reachable b) := by
  simpa only [Nat.card_prod] using
    Nat.card_le_card_of_injective _ (joint_support_embedding_injective a b)

/-- A decoder on reachable traces induces a surjection onto reachable answers. -/
theorem certification_capacity {W T Q : Type} (q : W → Q) (t : W → T)
    [Finite (Reachable t)] (hc : Certifies q t) :
    Finite (Reachable q) ∧ Nat.card (Reachable q) ≤ Nat.card (Reachable t) := by
  classical
  rcases hc with ⟨d, hd⟩
  let answerMap : Reachable t → Reachable q := fun z =>
    ⟨d z, by
      rcases z.property with ⟨w, hw⟩
      refine ⟨w, ?_⟩
      have hz : (⟨t w, ⟨w, rfl⟩⟩ : Reachable t) = z := Subtype.ext hw
      rw [← hz, hd]⟩
  have hs : Function.Surjective answerMap := by
    rintro ⟨v, w, hw⟩
    refine ⟨⟨t w, ⟨w, rfl⟩⟩, Subtype.ext ?_⟩
    exact (hd w).trans hw
  exact ⟨Finite.of_surjective _ hs, Nat.card_le_card_of_surjective _ hs⟩

theorem certified_joint_capacity_chain {W A B Q : Type}
    (a : W → A) (b : W → B) (q : W → Q)
    [Finite (Reachable a)] [Finite (Reachable b)] (hc : Certifies q (jointTrace a b)) :
    Nat.card (Reachable q) ≤ Nat.card (Reachable (jointTrace a b)) ∧
      Nat.card (Reachable (jointTrace a b)) ≤ Nat.card (Reachable a) * Nat.card (Reachable b) := by
  letI := joint_support_finite a b
  exact ⟨(certification_capacity q _ hc).2, joint_capacity_bound a b⟩

theorem diagonal_support_omits_product_value :
    ¬ (false, true) ∈ Set.range (jointTrace (id : Bool → Bool) id) := by
  rintro ⟨w, h⟩
  cases w <;> simp [jointTrace] at h

/-- Even two reachable labels for two answers do not fix misaligned fibers. -/
theorem sufficient_label_count_not_certification :
    Function.Surjective xorFirst ∧ Function.Surjective xorAnswer ∧
      ¬ Certifies xorAnswer xorFirst := by
  refine ⟨?_, ?_, xor_first_insufficient⟩
  · intro b; exact ⟨(b, false), rfl⟩
  · intro b; cases b <;> [exact ⟨(false, false), rfl⟩; exact ⟨(false, true), rfl⟩]

/-- Factor the whole evolution through the initial reachable values. -/
theorem evolution_factors_initial {W S : Type} (step : Nat → S → S) (initial : W → S)
    (n : Nat) (w : W) :
    scheduledIteration step initial n w =
      scheduledIteration step (fun z : Set.range initial => z.val) n ⟨initial w, ⟨w, rfl⟩⟩ := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [scheduledIteration, ih]

theorem finite_initial_image_kernel_stabilizes {W S : Type}
    (step : Nat → S → S) (initial : W → S) (hf : (Set.range initial).Finite) :
    ∃ start, ∀ n, start ≤ n → ∀ u v,
      (scheduledIteration step initial start u = scheduledIteration step initial start v ↔
       scheduledIteration step initial n u = scheduledIteration step initial n v) := by
  classical
  letI : Fintype (Set.range initial) := hf.fintype
  obtain ⟨start, hs⟩ := finite_scheduled_partition_stabilizes step
    (fun z : Set.range initial => z.val)
  refine ⟨start, fun n hn u v => ?_⟩
  have hm := congrArg (fun p =>
    (⟨initial u, ⟨u, rfl⟩⟩, ⟨initial v, ⟨v, rfl⟩⟩) ∈ p) (hs n hn)
  simpa only [kernelPairs, Finset.mem_filter, Finset.mem_univ, true_and,
    ← evolution_factors_initial, eq_iff_iff] using hm

theorem finite_trace_initialized_kernel_stabilizes {W T S : Type}
    (trace : W → T) (init : Set.range trace → S) (step : Nat → S → S)
    (hf : (Set.range trace).Finite) :
    ∃ start, ∀ n, start ≤ n → ∀ u v,
      (scheduledIteration step (fun w => init ⟨trace w, ⟨w, rfl⟩⟩) start u =
        scheduledIteration step (fun w => init ⟨trace w, ⟨w, rfl⟩⟩) start v ↔
       scheduledIteration step (fun w => init ⟨trace w, ⟨w, rfl⟩⟩) n u =
        scheduledIteration step (fun w => init ⟨trace w, ⟨w, rfl⟩⟩) n v) := by
  classical
  letI : Fintype (Set.range trace) := hf.fintype
  apply finite_initial_image_kernel_stabilizes
  apply (Set.finite_range init).subset
  rintro _ ⟨w, rfl⟩
  exact ⟨⟨trace w, ⟨w, rfl⟩⟩, rfl⟩

theorem evolution_range_finite {W S : Type} (step : Nat → S → S) (initial : W → S)
    (hf : (Set.range initial).Finite) (n : Nat) :
    (Set.range (scheduledIteration step initial n)).Finite := by
  induction n with
  | zero => exact hf
  | succ n ih =>
    change (Set.range (fun w => step n (scheduledIteration step initial n w))).Finite
    rw [Set.range_comp']
    exact ih.image _

/-- Each strict kernel merge strictly reduces the reachable image cardinality. -/
theorem merge_iff_capacity_drop {W S : Type} (f : W → S) (c : S → S)
    (hf : (Set.range f).Finite) :
    (∃ u v, f u ≠ f v ∧ c (f u) = c (f v)) ↔
      (Set.range (c ∘ f)).ncard < (Set.range f).ncard := by
  rw [Set.range_comp]
  have hle : (c '' Set.range f).ncard ≤ (Set.range f).ncard := Set.ncard_image_le hf
  constructor
  · rintro ⟨u, v, huv, hc⟩
    apply lt_of_le_of_ne hle
    intro heq
    exact huv ((Set.injOn_of_ncard_image_eq heq hf) ⟨u, rfl⟩ ⟨v, rfl⟩ hc)
  · intro hlt
    by_contra h
    push Not at h
    have hi : Set.InjOn c (Set.range f) := by
      rintro _ ⟨u, rfl⟩ _ ⟨v, rfl⟩ hc
      by_contra hne
      exact h u v hne hc
    have heq := hi.ncard_image
    omega

theorem scheduled_merge_iff_capacity_drop {W S : Type}
    (step : Nat → S → S) (initial : W → S) (hf : (Set.range initial).Finite) (n : Nat) :
    (∃ u v, scheduledIteration step initial n u ≠ scheduledIteration step initial n v ∧
      scheduledIteration step initial (n + 1) u = scheduledIteration step initial (n + 1) v) ↔
    (Set.range (scheduledIteration step initial (n + 1))).ncard <
      (Set.range (scheduledIteration step initial n)).ncard := by
  simpa only [scheduledIteration, Function.comp_def] using
    merge_iff_capacity_drop (scheduledIteration step initial n) (step n)
      (evolution_range_finite step initial hf n)

/-- Number of strict drops in the first n updates; this counts events, not elapsed time. -/
def dropCount (capacity : Nat → Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => dropCount capacity n + if capacity (n + 1) < capacity n then 1 else 0

theorem strict_drop_budget (capacity : Nat → Nat)
    (hc : ∀ n, capacity (n + 1) ≤ capacity n) (n : Nat) :
    dropCount capacity n + capacity n ≤ capacity 0 := by
  induction n with
  | zero => simp [dropCount]
  | succ n ih =>
    have hn := hc n
    simp only [dropCount]
    split_ifs <;> omega

theorem finite_image_merge_budget {W S : Type} [Nonempty W]
    (step : Nat → S → S) (initial : W → S) (hf : (Set.range initial).Finite) (n : Nat) :
    dropCount (fun k => (Set.range (scheduledIteration step initial k)).ncard) n ≤
      (Set.range initial).ncard - 1 := by
  have hmono : ∀ k, (Set.range (scheduledIteration step initial (k + 1))).ncard ≤
      (Set.range (scheduledIteration step initial k)).ncard := by
    intro k
    change (Set.range (fun w => step k (scheduledIteration step initial k w))).ncard ≤ _
    rw [Set.range_comp']
    exact Set.ncard_image_le (evolution_range_finite step initial hf k)
  have hb := strict_drop_budget
    (fun k => (Set.range (scheduledIteration step initial k)).ncard) hmono n
  have hp : 0 < (Set.range (scheduledIteration step initial n)).ncard :=
    (Set.ncard_pos (evolution_range_finite step initial hf n)).mpr (Set.range_nonempty _)
  change _ + _ ≤ (Set.range initial).ncard at hb
  omega

def delayedStep (delay n : Nat) (b : Bool) : Bool := if n = delay then false else b

theorem delayed_evolution (delay n : Nat) (b : Bool) :
    scheduledIteration (delayedStep delay) id n b = if n ≤ delay then b else false := by
  induction n with
  | zero => simp [scheduledIteration]
  | succ n ih =>
    simp only [scheduledIteration, delayedStep, ih]
    split_ifs <;> first | rfl | omega

theorem merge_can_be_arbitrarily_late (delay : Nat) :
    (∀ n ≤ delay, scheduledIteration (delayedStep delay) id n false ≠
      scheduledIteration (delayedStep delay) id n true) ∧
    scheduledIteration (delayedStep delay) id (delay + 1) false =
      scheduledIteration (delayedStep delay) id (delay + 1) true := by
  simp [delayed_evolution]

/-- Natural-number predecessor repeatedly merges another pair, with infinite initial image. -/
theorem predecessor_evolution (n w : Nat) :
    scheduledIteration (fun _ k : Nat => k - 1) id n w = w - n := by
  induction n with
  | zero => simp [scheduledIteration]
  | succ n ih => simp only [scheduledIteration, ih]; omega

theorem infinite_image_never_stabilizes :
    (Set.range (id : Nat → Nat)).Infinite ∧
    ¬ ∃ start, ∀ n, start ≤ n → ∀ u v,
      (scheduledIteration (fun _ k : Nat => k - 1) id start u =
        scheduledIteration (fun _ k : Nat => k - 1) id start v ↔
       scheduledIteration (fun _ k : Nat => k - 1) id n u =
        scheduledIteration (fun _ k : Nat => k - 1) id n v) := by
  refine ⟨Set.infinite_range_of_injective Function.injective_id, ?_⟩
  rintro ⟨start, hs⟩
  have h := hs (start + 1) (by omega) start (start + 1)
  simp [predecessor_evolution] at h

end Experiments.AbstractLoopsFiniteImage
