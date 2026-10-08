import Mathlib

namespace FrontLean
open Module
noncomputable section
variable {k T R : Type*} [Field k]
variable [AddCommGroup T] [Module k T] [AddCommGroup R] [Module k R]

def horizonKernel (L : Module.End k T) (r : T →ₗ[k] R) (n : ℕ) : Submodule k T :=
  ⨅ j < n, (r.comp (L ^ j)).ker

def infiniteKernel (L : Module.End k T) (r : T →ₗ[k] R) : Submodule k T :=
  ⨅ j : ℕ, (r.comp (L ^ j)).ker

theorem mem_horizon (L : Module.End k T) (r : T →ₗ[k] R) (n : ℕ) (x : T) :
    x ∈ horizonKernel L r n ↔ ∀ j < n, r ((L ^ j) x) = 0 := by
  simp [horizonKernel, LinearMap.mem_ker]

theorem mem_infinite (L : Module.End k T) (r : T →ₗ[k] R) (x : T) :
    x ∈ infiniteKernel L r ↔ ∀ j, r ((L ^ j) x) = 0 := by
  simp [infiniteKernel, LinearMap.mem_ker]

theorem horizon_antitone (L : Module.End k T) (r : T →ₗ[k] R) :
    Antitone (horizonKernel L r) := by
  intro n m h x hx
  rw [mem_horizon] at hx ⊢
  exact fun j hj => hx j (hj.trans_le h)

/-- Persistent invisibility on the full difference domain, not sampled equality. -/
theorem invariant_kernel_iff (L : Module.End k T) (r : T →ₗ[k] R) :
    (∀ x ∈ r.ker, L x ∈ r.ker) ↔ ∀ x ∈ r.ker, ∀ j : ℕ, r ((L ^ j) x) = 0 := by
  constructor
  · intro h x hx j
    induction j with
    | zero => simpa using hx
    | succ j ih => simpa [pow_succ', Module.End.mul_apply] using h ((L ^ j) x) ih
  · intro h x hx
    simpa using h x hx 1

theorem infinite_invariant (L : Module.End k T) (r : T →ₗ[k] R) :
    ∀ x ∈ infiniteKernel L r, L x ∈ infiniteKernel L r := by
  intro x hx
  rw [mem_infinite] at hx ⊢
  intro j
  simpa [pow_succ, Module.End.mul_apply] using hx (j + 1)

theorem all_outputs_equal_iff (L : Module.End k T) (r : T →ₗ[k] R) (x y : T) :
    (∀ j : ℕ, r ((L ^ j) x) = r ((L ^ j) y)) ↔ x - y ∈ infiniteKernel L r := by
  simp [mem_infinite, map_sub, sub_eq_zero]

private theorem stable_horizon_invariant (L : Module.End k T) (r : T →ₗ[k] R) (n : ℕ)
    (hn : horizonKernel L r n = horizonKernel L r (n + 1)) :
    ∀ x ∈ horizonKernel L r n, L x ∈ horizonKernel L r n := by
  intro x hx
  have hx' : x ∈ horizonKernel L r (n + 1) := hn ▸ hx
  rw [mem_horizon] at hx' ⊢
  intro j hj
  simpa [pow_succ, Module.End.mul_apply] using hx' (j + 1) (by omega)

private theorem stable_horizon_equals_infinite (L : Module.End k T) (r : T →ₗ[k] R)
    (n : ℕ) (hn : horizonKernel L r n = horizonKernel L r (n + 1)) :
    horizonKernel L r n = infiniteKernel L r := by
  apply le_antisymm
  · intro x hx
    have inv := stable_horizon_invariant L r n hn
    have power : ∀ j : ℕ, (L ^ j) x ∈ horizonKernel L r n := by
      intro j
      induction j with
      | zero => simpa using hx
      | succ j ih => simpa [pow_succ', Module.End.mul_apply] using inv _ ih
    rw [mem_infinite]
    intro j
    have hj : (L ^ j) x ∈ horizonKernel L r (n + 1) := hn ▸ power j
    simpa using (mem_horizon L r (n + 1) _).mp hj 0 (by omega)
  · intro x hx
    rw [mem_horizon]
    exact fun j _ => (mem_infinite L r x).mp hx j

/-- Finite-dimensional stabilization by strict dimension drop. This proves the same
    n-step bound as the paper's Cayley-Hamilton proof by a different elementary route. -/
theorem finite_horizon_closure [FiniteDimensional k T] (L : Module.End k T)
    (r : T →ₗ[k] R) : horizonKernel L r (finrank k T) = infiniteKernel L r := by
  let n := finrank k T
  have stable : ∃ j ≤ n, horizonKernel L r j = horizonKernel L r (j + 1) := by
    by_contra! h
    have drop : ∀ j ≤ n + 1, finrank k (horizonKernel L r j) + j ≤ n := by
      intro j hj
      induction j with
      | zero => simpa [n] using (horizonKernel L r 0).finrank_le
      | succ j ih =>
        have ih' := ih (by omega)
        have strict : horizonKernel L r (j + 1) < horizonKernel L r j := by
          refine lt_iff_le_and_ne.mpr ⟨horizon_antitone L r (by omega), ?_⟩
          exact fun heq => h j (by omega) heq.symm
        have hd := Submodule.finrank_lt_finrank_of_lt strict
        omega
    have impossible := drop (n + 1) le_rfl
    omega
  obtain ⟨j, hj, hs⟩ := stable
  have heq := stable_horizon_equals_infinite L r j hs
  apply le_antisymm
  · exact (horizon_antitone L r hj).trans heq.le
  · intro x hx
    rw [mem_horizon]
    exact fun j _ => (mem_infinite L r x).mp hx j

/-- A finite subfamily of arbitrary subspaces preserves the common intersection.
    This is stronger than the readout-kernel instance; it does not find the witnesses. -/
theorem finite_subfamily_inside [FiniteDimensional k T] {ι : Type*}
    (U : ι → Submodule k T) (S : Submodule k T) :
    ∃ s : Finset ι, s.card ≤ finrank k S ∧
      S ⊓ (⨅ i ∈ s, U i) = S ⊓ ⨅ i, U i := by
  classical
  have go : ∀ n : ℕ, ∀ S : Submodule k T, finrank k S = n →
      ∃ s : Finset ι, s.card ≤ n ∧ S ⊓ (⨅ i ∈ s, U i) = S ⊓ ⨅ i, U i := by
    intro n
    induction n using Nat.strong_induction_on with
    | h n ih =>
      intro S hdim
      by_cases h : S ≤ ⨅ i, U i
      · exact ⟨∅, by simp, by simpa using (inf_eq_left.mpr h).symm⟩
      · have ex : ∃ i, ¬ S ≤ U i := by simpa only [le_iInf_iff, not_forall] using h
        obtain ⟨i, hi⟩ := ex
        have hstrict : S ⊓ U i < S := by
          refine lt_iff_le_and_ne.mpr ⟨inf_le_left, ?_⟩
          intro heq
          exact hi (heq ▸ (inf_le_right : S ⊓ U i ≤ U i))
        have hd := Submodule.finrank_lt_finrank_of_lt hstrict
        obtain ⟨s, hs, heq⟩ := ih (finrank k ↥(S ⊓ U i)) (by omega) (S ⊓ U i) rfl
        refine ⟨insert i s, ?_, ?_⟩
        · have hc := Finset.card_insert_le i s
          omega
        · calc
            S ⊓ (⨅ j ∈ insert i s, U j) = (S ⊓ U i) ⊓ (⨅ j ∈ s, U j) := by
              ext x
              simp only [Submodule.mem_inf, Submodule.mem_iInf, Finset.mem_insert]
              aesop
            _ = (S ⊓ U i) ⊓ ⨅ j, U j := heq
            _ = S ⊓ ⨅ j, U j := by
              rw [inf_assoc, inf_eq_right.mpr (iInf_le U i)]
  exact go (finrank k S) S rfl

/-- Proposition 5C, allowing any family and even infinite-dimensional codomains. -/
theorem finite_readout_subfamily [FiniteDimensional k T] {ι : Type*}
    {V : ι → Type*} [∀ i, AddCommGroup (V i)] [∀ i, Module k (V i)]
    (r : ∀ i, T →ₗ[k] V i) :
    ∃ s : Finset ι, s.card ≤ finrank k T ∧ (⨅ i ∈ s, (r i).ker) = ⨅ i, (r i).ker := by
  simpa using finite_subfamily_inside (fun i => (r i).ker) ⊤

end
end FrontLean
