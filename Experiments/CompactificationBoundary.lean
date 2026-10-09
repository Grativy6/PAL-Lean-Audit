import Mathlib.Topology.DenseEmbedding
import Mathlib.Topology.Separation.Hausdorff
import Mathlib.Tactic

namespace Experiments.CompactificationBoundary
open Set Filter Topology Function

@[reducible]
def Boundary {X Y : Type*} (r : X → Y) := {y : Y // y ∉ range r}

theorem interior_fiber_unique {X Y Z : Type*}
    [TopologicalSpace X] [TopologicalSpace Y] [TopologicalSpace Z] [T2Space Y]
    (j : X → Z) (r : X → Y) (k : Y → Z)
    (hj : IsEmbedding j) (hr : IsEmbedding r) (hd : DenseRange r)
    (hk : Continuous k) (comm : ∀ x, k (r x) = j x)
    (y : Y) (x : X) (hy : k y = j x) : y = r x := by
  let l : Filter X := comap r (𝓝 y)
  let di : IsDenseInducing r := ⟨hr.isInducing, hd⟩
  haveI : l.NeBot := di.comap_nhds_neBot y
  have h₁ : Tendsto r l (𝓝 y) := map_comap_le
  have h₂ : Tendsto (k ∘ r) l (𝓝 (j x)) := by
    rw [← hy]
    exact hk.continuousAt.tendsto.comp h₁
  have hid : Tendsto (id : X → X) l (𝓝 x) := by
    apply hj.tendsto_nhds_iff.mpr
    convert h₂ using 1
    funext a
    exact (comm a).symm
  have h₃ : Tendsto r l (𝓝 (r x)) := hr.continuous.continuousAt.tendsto.comp hid
  exact tendsto_nhds_unique h₁ h₃

theorem boundary_preserved {X Y Z : Type*}
    [TopologicalSpace X] [TopologicalSpace Y] [TopologicalSpace Z] [T2Space Y]
    (j : X → Z) (r : X → Y) (k : Y → Z)
    (hj : IsEmbedding j) (hr : IsEmbedding r) (hd : DenseRange r)
    (hk : Continuous k) (comm : ∀ x, k (r x) = j x) :
    MapsTo k (range r)ᶜ (range j)ᶜ := by
  intro y hy h
  obtain ⟨x, hx⟩ := h
  exact hy ⟨x, (interior_fiber_unique j r k hj hr hd hk comm y x hx.symm).symm⟩

theorem boundary_onto {X Y Z : Type*}
    [TopologicalSpace X] [TopologicalSpace Y] [TopologicalSpace Z] [T2Space Y]
    (j : X → Z) (r : X → Y) (k : Y → Z)
    (hj : IsEmbedding j) (hr : IsEmbedding r) (hd : DenseRange r)
    (hk : Continuous k) (comm : ∀ x, k (r x) = j x) (hs : Surjective k) :
    k '' (range r)ᶜ = (range j)ᶜ := by
  apply Subset.antisymm
  · rintro z ⟨y, hy, rfl⟩
    exact boundary_preserved j r k hj hr hd hk comm hy
  · intro z hz
    obtain ⟨y, rfl⟩ := hs z
    refine ⟨y, ?_, rfl⟩
    rintro ⟨x, rfl⟩
    exact hz ⟨x, (comm x).symm⟩

def boundaryMap {X Y Z : Type*} (j : X → Z) (r : X → Y) (k : Y → Z)
    (h : MapsTo k (range r)ᶜ (range j)ᶜ) : Boundary r → Boundary j :=
  fun y => ⟨k y.val, h y.property⟩

theorem boundary_map_continuous {X Y Z : Type*}
    [TopologicalSpace X] [TopologicalSpace Y] [TopologicalSpace Z]
    (j : X → Z) (r : X → Y) (k : Y → Z)
    (h : MapsTo k (range r)ᶜ (range j)ᶜ) (hk : Continuous k) :
    Continuous (boundaryMap j r k h) :=
  (hk.comp continuous_subtype_val).subtype_mk _

theorem boundary_map_surjective {X Y Z : Type*} (j : X → Z) (r : X → Y) (k : Y → Z)
    (h : MapsTo k (range r)ᶜ (range j)ᶜ) (hs : Surjective k)
    (comm : ∀ x, k (r x) = j x) : Surjective (boundaryMap j r k h) := by
  intro z
  obtain ⟨y, hy⟩ := hs z.val
  have hb : y ∈ (range r)ᶜ := by
    rintro ⟨x, rfl⟩
    exact z.property ⟨x, (comm x).symm.trans hy⟩
  exact ⟨⟨y,hb⟩, Subtype.ext hy⟩

theorem compact_surjection_is_quotient {A B : Type*}
    [TopologicalSpace A] [TopologicalSpace B] [CompactSpace A] [T2Space B]
    (f : A → B) (hc : Continuous f) (hs : Surjective f) : IsQuotientMap f :=
  hc.isClosedMap.isQuotientMap hc hs

theorem quotient_continuous_decoder {A B D : Type*}
    [TopologicalSpace A] [TopologicalSpace B] [TopologicalSpace D]
    (f : A → B) (hf : IsQuotientMap f) (u : A → D) (hu : Continuous u)
    (constant : ∀ a a', f a = f a' → u a = u a') :
    ∃! d : B → D, Continuous d ∧ ∀ a, d (f a) = u a := by
  classical
  let d : B → D := fun b => u (Classical.choose (hf.surjective b))
  have hd : ∀ a, d (f a) = u a := by
    intro a
    apply constant
    exact Classical.choose_spec (hf.surjective (f a))
  have heq : d ∘ f = u := funext hd
  refine ⟨d, ⟨hf.continuous_iff.mpr (heq.symm ▸ hu), hd⟩, ?_⟩
  intro d' hd'
  funext b
  obtain ⟨a,rfl⟩ := hf.surjective b
  exact (hd'.2 a).trans (hd a).symm

theorem strict_boundary_decoder {X Y Z D : Type*}
    [TopologicalSpace X] [TopologicalSpace Y] [TopologicalSpace Z] [TopologicalSpace D]
    [CompactSpace Y] [T2Space Y] [T2Space Z]
    (j : X → Z) (r : X → Y) (k : Y → Z)
    (hj : IsEmbedding j) (hr : IsOpenEmbedding r) (hd : DenseRange r)
    (hk : Continuous k) (comm : ∀ x, k (r x) = j x) (hs : Surjective k)
    (u : Boundary r → D) (hu : Continuous u)
    (constant : ∀ a a' : Boundary r, k a.val = k a'.val → u a = u a') :
    ∃! d : Boundary j → D, Continuous d ∧ ∀ a : Boundary r,
      d ⟨k a.val, boundary_preserved j r k hj hr.isEmbedding hd hk comm a.property⟩ = u a := by
  haveI : CompactSpace (Boundary r) := isCompact_iff_compactSpace.mp hr.isOpen_range.isClosed_compl.isCompact
  let f := boundaryMap j r k (boundary_preserved j r k hj hr.isEmbedding hd hk comm)
  have hq : IsQuotientMap f := compact_surjection_is_quotient f
    (boundary_map_continuous j r k _ hk) (boundary_map_surjective j r k _ hs comm)
  exact quotient_continuous_decoder f hq u hu (fun a a' h => constant a a' (congrArg Subtype.val h))

end Experiments.CompactificationBoundary
