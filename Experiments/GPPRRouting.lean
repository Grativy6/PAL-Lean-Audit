import Experiments.GPPREncoding
import Experiments.GPPRTranscendence

namespace Experiments.GPPRRouting
open Function Polynomial

theorem golden_code_conditional (gs : GPPRTranscendence.GelfondSchneiderRealExponent)
    (address : Nat.Primes ↪ ℕ) :
    Set.InjOn (fun n => GPPREncoding.code address (fun _ => (1:ℚ))
      GPPRTranscendence.zeta (GPPREncoding.valuation n)) {n | n ≠ 0} :=
  GPPREncoding.integer_code_injective address GPPRTranscendence.zeta
    (GPPRTranscendence.golden_transcendence_conditional gs)

theorem golden_vogel_conditional (gs : GPPRTranscendence.GelfondSchneiderRealExponent) :
    Injective (GPPREncoding.code (fun j : ℕ+ => (j:ℕ)) GPPREncoding.vogelWeight GPPRTranscendence.zeta) :=
  GPPREncoding.vogel_code_injective GPPRTranscendence.zeta
    (GPPRTranscendence.golden_transcendence_conditional gs)

def legacy (z : ℂ) (events : List ℕ) : ℂ := z ^ events.sum
def endpoint (z : ℂ) (events : List ℕ) : ℂ := (events.map (fun j => z^j)).sum
def path (z : ℂ) (events : List ℕ) : List ℂ := events.scanl (fun a j => a+z^j) 0

noncomputable def eventVector (events : List ℕ) : ℕ →₀ ℤ :=
  (events.map (fun j => Finsupp.single j (1:ℤ))).sum

theorem complete_event_endpoint (z : ℂ) (events : List ℕ) :
    GPPREncoding.code id (fun _ => (1:ℚ)) z (eventVector events) = endpoint z events := by
  induction events with
  | nil => simp [eventVector,endpoint,GPPREncoding.code_zero]
  | cons j rest ih =>
    change GPPREncoding.code id (fun _ => (1:ℚ)) z (Finsupp.single j 1 + eventVector rest) = _
    rw [GPPREncoding.code_add,GPPREncoding.code_single,ih]
    simp [endpoint]

theorem legacy_three_four_collision (z : ℂ) : legacy z [2] = legacy z [1,1] := by
  simp [legacy]

theorem repaired_endpoints_distinct (z : ℂ) (hz : Transcendental ℚ z) : z^2 ≠ 2*z := by
  intro h
  have hp : (X^2 : ℚ[X]) = C 2 * X := (transcendental_iff_injective.mp hz) (by simpa using h)
  have hc := congrArg (fun p : ℚ[X] => p.coeff 2) hp
  norm_num at hc

theorem endpoint_permutation (z : ℂ) {a b : List ℕ} (h : a.Perm b) : endpoint z a = endpoint z b :=
  (h.map _).sum_eq

theorem consecutive_powers_distinct (z : ℂ) (hz : Transcendental ℚ z) : z ≠ z^2 := by
  intro h
  have hp : (X : ℚ[X]) = X^2 := (transcendental_iff_injective.mp hz) (by simpa using h)
  have hc := congrArg (fun p : ℚ[X] => p.coeff 1) hp
  norm_num at hc

theorem shared_endpoint_distinct_paths (z : ℂ) (hz : Transcendental ℚ z) :
    endpoint z [1,2] = endpoint z [2,1] ∧ path z [1,2] ≠ path z [2,1] := by
  constructor
  · simp [endpoint,add_comm]
  · intro h
    have hh := congrArg (fun l : List ℂ => l[1]?) h
    have he : z = z^2 := by simpa [path] using hh
    exact consecutive_powers_distinct z hz he

theorem roots_need_a_condition :
    ∃ root : List ℕ → Bool, [1,2] ≠ [2,1] ∧ root [1,2] = root [2,1] := by
  exact ⟨fun _ => false,by decide,rfl⟩

theorem root_pair_condition {H : Type*} (root : List ℕ → H)
    (hinj : Set.InjOn root ({[1,2],[2,1]} : Set (List ℕ))) : root [1,2] ≠ root [2,1] := by
  intro h
  have he := hinj (by simp) (by simp) h
  contradiction

theorem finite_roots_cannot_encode_all_histories {H : Type*} [Finite H] (root : List ℕ → H) :
    ∃ a b, a ≠ b ∧ root a = root b := Finite.exists_ne_map_eq_of_infinite root

structure FactorRecord where
  magnitude : ℕ
  knownProduct : ℕ
  residual : ℕ
  exact : magnitude = knownProduct * residual

def completeRecord (r : FactorRecord) : Prop := r.residual = 1

theorem retained_residual_needed (r : FactorRecord) (hk : r.knownProduct ≠ 0) :
    r.magnitude = r.knownProduct ↔ completeRecord r := by
  rw [r.exact]
  dsimp [completeRecord]
  constructor
  · intro h
    exact Nat.eq_of_mul_eq_mul_left (Nat.pos_of_ne_zero hk) (by simpa using h)
  · intro h; rw [h,Nat.mul_one]

theorem partial_record_fixture : ∃ r : FactorRecord,
    r.magnitude = 30 ∧ r.knownProduct = 6 ∧ r.residual = 5 ∧ ¬ completeRecord r := by
  exact ⟨⟨30,6,5,by decide⟩,rfl,rfl,rfl,by norm_num [completeRecord]⟩

def EntireCell {X C : Type*} (partition : X → C) (enclosure : Set X) (cell : C) : Prop :=
  ∀ x ∈ enclosure, partition x = cell

theorem certified_route_sound {X C : Type*} (p : X → C) (B : Set X) (c : C)
    (h : EntireCell p B c) (x : X) (hx : x ∈ B) : p x = c := h x hx

theorem route_unique {X C : Type*} (p : X → C) (B : Set X) (hne : B.Nonempty)
    (a b : C) (ha : EntireCell p B a) (hb : EntireCell p B b) : a = b := by
  obtain ⟨x,hx⟩ := hne
  exact (ha x hx).symm.trans (hb x hx)

theorem crossing_enclosure_unresolved {X C : Type*} (p : X → C) (B : Set X)
    (x y : X) (hx : x ∈ B) (hy : y ∈ B) (hxy : p x ≠ p y) : ¬ ∃ c, EntireCell p B c := by
  rintro ⟨c,hc⟩
  exact hxy ((hc x hx).trans (hc y hy).symm)

theorem interval_crossing_fixture : ¬ ∃ c : Bool,
    EntireCell (fun x : ℚ => decide (0 ≤ x)) (Set.Icc (-1) 1) c := by
  exact crossing_enclosure_unresolved _ _ (-1) 1 (by norm_num) (by norm_num) (by decide)

theorem empty_enclosure_is_not_a_unique_certificate :
    EntireCell (id : Bool → Bool) ∅ false ∧ EntireCell id ∅ true := by simp [EntireCell]

def VersionCompatible {I V : Type*} (old new : I → V) (oldVersion newVersion : ℕ) : Prop :=
  oldVersion = newVersion → old = new

theorem changed_registry_requires_version {I V : Type*} (old new : I → V) (a b : ℕ)
    (changed : old ≠ new) (valid : VersionCompatible old new a b) : a ≠ b := by
  exact fun h => changed (valid h)

def invalidateAfterAddition {A : Type*} (_old : Option A) : Option A := none

theorem magnitude_addition_is_not_code_addition (z : ℂ) (hz : Transcendental ℚ z) : z^3 ≠ z+z^2 := by
  intro h
  have hp : (X^3 : ℚ[X]) = X+X^2 := (transcendental_iff_injective.mp hz) (by simpa using h)
  have hc := congrArg (fun p : ℚ[X] => p.coeff 3) hp
  norm_num [Polynomial.coeff_X] at hc

theorem addition_invalidates_endpoint {A : Type*} (old : Option A) : invalidateAfterAddition old = none := rfl

theorem exact_fallback_preserves_identity {W A E : Type*} (approx : W → A) (exactRecord : W → E)
    (he : Injective exactRecord) : Injective (fun w => (approx w,exactRecord w)) := by
  intro a b h
  exact he (congrArg Prod.snd h)

theorem distinct_axis_powers (z : ℂ) (hz : Transcendental ℚ z) : Injective (fun n : ℕ => z^(n+1)) := by
  intro a b h
  have hp : (X^(a+1) : ℚ[X]) = X^(b+1) := (transcendental_iff_injective.mp hz) (by simpa using h)
  have hd := congrArg Polynomial.natDegree hp
  simp only [natDegree_X_pow] at hd
  omega

theorem finite_rounding_collision {R : Type*} [Finite R] (round : ℂ → R)
    (z : ℂ) (hz : Transcendental ℚ z) :
    ∃ a b : ℕ, z^(a+1) ≠ z^(b+1) ∧ round (z^(a+1)) = round (z^(b+1)) := by
  obtain ⟨a,b,hab,hr⟩ := Finite.exists_ne_map_eq_of_infinite (fun n : ℕ => round (z^(n+1)))
  exact ⟨a,b,fun h => hab (distinct_axis_powers z hz h),hr⟩

theorem finite_reachable_rounding_collision {R : Type*} (round : ℂ → R)
    (z : ℂ) (hz : Transcendental ℚ z)
    (hf : (Set.range (fun n : ℕ => round (z^(n+1)))).Finite) :
    ∃ a b : ℕ, z^(a+1) ≠ z^(b+1) ∧ round (z^(a+1)) = round (z^(b+1)) := by
  letI := hf.fintype
  let f : ℕ → Set.range (fun n : ℕ => round (z^(n+1))) :=
    fun n => ⟨round (z^(n+1)),⟨n,rfl⟩⟩
  obtain ⟨a,b,hab,hr⟩ := Finite.exists_ne_map_eq_of_infinite f
  exact ⟨a,b,fun h => hab (distinct_axis_powers z hz h),congrArg Subtype.val hr⟩

inductive Claim where
  | exactRepresentation | declaredCell | goldenOptimality | factorDiscovery
  deriving DecidableEq

def withinClaimCeiling (claim : Claim) : Bool := match claim with
  | .exactRepresentation | .declaredCell => true
  | .goldenOptimality | .factorDiscovery => false

theorem unsupported_promotions_rejected :
    withinClaimCeiling .goldenOptimality = false ∧ withinClaimCeiling .factorDiscovery = false := by decide

end Experiments.GPPRRouting
