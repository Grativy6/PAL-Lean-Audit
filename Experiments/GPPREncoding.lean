import Mathlib

namespace Experiments.GPPREncoding
open Polynomial Function

noncomputable def weightedPoly {I K : Type*} [CommRing K]
    (address : I → ℕ) (weight : I → K) (v : I →₀ ℤ) : K[X] :=
  v.sum (fun i e => monomial (address i) ((e : K)*weight i))

theorem weighted_coeff {I K : Type*} [CommRing K]
    (address : I ↪ ℕ) (weight : I → K) (v : I →₀ ℤ) (i : I) :
    (weightedPoly address weight v).coeff (address i) = (v i : K)*weight i := by
  classical
  simp only [weightedPoly,Finsupp.sum,finsetSum_coeff,coeff_monomial]
  rw [Finset.sum_eq_single i]
  · simp
  · intro j _ hji
    simp [show address j ≠ address i from fun h => hji (address.injective h)]
  · intro hi
    simp [Finsupp.notMem_support_iff.mp hi]

theorem weighted_add {I K : Type*} [CommRing K]
    (address : I → ℕ) (weight : I → K) (v w : I →₀ ℤ) :
    weightedPoly address weight (v+w) = weightedPoly address weight v + weightedPoly address weight w := by
  classical
  exact Finsupp.sum_add_index' (by intro i; simp) (by intro i a b; simp [add_mul])

theorem weighted_injective {I K : Type*} [CommRing K] [IsDomain K] [CharZero K]
    (address : I ↪ ℕ) (weight : I → K) (hw : ∀ i, weight i ≠ 0) :
    Injective (weightedPoly address weight) := by
  intro v w h
  ext i
  have hc := congrArg (fun p : K[X] => p.coeff (address i)) h
  rw [weighted_coeff,weighted_coeff] at hc
  exact_mod_cast mul_right_cancel₀ (hw i) hc

noncomputable def code {I K : Type*} [CommRing K] [Algebra K ℂ]
    (address : I → ℕ) (weight : I → K) (z : ℂ) (v : I →₀ ℤ) : ℂ :=
  aeval z (weightedPoly address weight v)

theorem exact_code_injective {I K : Type*} [CommRing K] [IsDomain K] [CharZero K] [Algebra K ℂ]
    (address : I ↪ ℕ) (weight : I → K) (hw : ∀ i, weight i ≠ 0)
    (z : ℂ) (hz : Transcendental K z) : Injective (code address weight z) := by
  intro v w h
  exact weighted_injective address weight hw (transcendental_iff_injective.mp hz h)

theorem algebraic_weight_code_injective {I K : Type*} [CommRing K] [IsDomain K] [CharZero K]
    [Algebra ℚ K] [Algebra K ℂ] [IsScalarTower ℚ K ℂ] [Algebra.IsAlgebraic ℚ K]
    (address : I ↪ ℕ) (weight : I → K) (hw : ∀ i, weight i ≠ 0)
    (z : ℂ) (hz : Transcendental ℚ z) : Injective (code address weight z) :=
  exact_code_injective address weight hw z (hz.extendScalars K)

theorem code_add {I K : Type*} [CommRing K] [Algebra K ℂ]
    (address : I → ℕ) (weight : I → K) (z : ℂ) (v w : I →₀ ℤ) :
    code address weight z (v+w) = code address weight z v + code address weight z w := by
  simp [code,weighted_add]

theorem code_single {I K : Type*} [CommRing K] [Algebra K ℂ]
    (address : I → ℕ) (weight : I → K) (z : ℂ) (i : I) (e : ℤ) :
    code address weight z (Finsupp.single i e) = (e:ℂ) * algebraMap K ℂ (weight i) * z^(address i) := by
  classical
  simp [code,weightedPoly,aeval_monomial]

theorem code_zero {I K : Type*} [CommRing K] [Algebra K ℂ]
    (address : I → ℕ) (weight : I → K) (z : ℂ) : code address weight z 0 = 0 := by
  simp [code,weightedPoly]

noncomputable def valuation (n : ℕ) : Nat.Primes →₀ ℤ :=
  (n.factorization.subtypeDomain Nat.Prime).mapRange (fun e : ℕ => (e : ℤ)) (by simp)

theorem valuation_apply (n : ℕ) (p : Nat.Primes) : valuation n p = n.factorization p := rfl

theorem valuation_mul {m n : ℕ} (hm : m ≠ 0) (hn : n ≠ 0) :
    valuation (m*n) = valuation m + valuation n := by
  ext p
  simp [valuation_apply,Nat.factorization_mul hm hn]

theorem valuation_injective : Set.InjOn valuation {n | n ≠ 0} := by
  intro m hm n hn h
  apply Nat.factorization_inj hm hn
  ext p
  by_cases hp : p.Prime
  · have he := congrArg (fun v : Nat.Primes →₀ ℤ => v ⟨p,hp⟩) h
    simpa [valuation_apply] using he
  · simp [Nat.factorization_eq_zero_of_not_prime _ hp]

theorem valuation_unit : valuation 1 = 0 := by ext p; simp [valuation_apply]

theorem valuation_prime_power (p : Nat.Primes) (k : ℕ) :
    valuation (p.val^k) = Finsupp.single p (k : ℤ) := by
  ext q
  simp only [valuation_apply,Nat.Prime.factorization_pow p.property,Finsupp.single_apply]
  by_cases h : p = q
  · subst q; simp
  · have hv : p.val ≠ q.val := fun he => h (Subtype.ext he)
    simp [h,hv]

theorem integer_code_injective (address : Nat.Primes ↪ ℕ) (z : ℂ) (hz : Transcendental ℚ z) :
    Set.InjOn (fun n => code address (fun _ => (1:ℚ)) z (valuation n)) {n | n ≠ 0} := by
  intro m hm n hn h
  exact valuation_injective hm hn (exact_code_injective address _ (by simp) z hz h)

theorem integer_product_to_sum (address : Nat.Primes → ℕ) (z : ℂ) {m n : ℕ}
    (hm : m ≠ 0) (hn : n ≠ 0) :
    code address (fun _ => (1:ℚ)) z (valuation (m*n)) =
      code address (fun _ => (1:ℚ)) z (valuation m) + code address (fun _ => (1:ℚ)) z (valuation n) := by
  rw [valuation_mul hm hn,code_add]

theorem rational_valuation_equality {a b c d : ℕ}
    (ha : a ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0) (hd : d ≠ 0) :
    valuation a - valuation b = valuation c - valuation d ↔ (a : ℚ)/b = (c : ℚ)/d := by
  rw [sub_eq_sub_iff_add_eq_add]
  rw [← valuation_mul ha hd, ← valuation_mul hc hb]
  rw [div_eq_div_iff (by exact_mod_cast hb : (b:ℚ) ≠ 0) (by exact_mod_cast hd : (d:ℚ) ≠ 0)]
  constructor
  · intro h
    exact_mod_cast valuation_injective (mul_ne_zero ha hd) (mul_ne_zero hc hb) h
  · intro h
    have h' : a*d = c*b := by exact_mod_cast h
    rw [h']

theorem positive_rational_representation (q : ℚ) (hq : 0 < q) :
    ∃ a b : ℕ, a ≠ 0 ∧ b ≠ 0 ∧ q = (a:ℚ)/b := by
  refine ⟨q.num.natAbs,q.den,?_,q.den_ne_zero,?_⟩
  · exact Int.natAbs_ne_zero.mpr (ne_of_gt (Rat.num_pos.mpr hq))
  · have h : (q.num.natAbs : ℤ) = q.num := Int.natAbs_of_nonneg (Rat.num_pos.mpr hq).le
    calc
      q = (q.num:ℚ)/q.den := q.num_div_den.symm
      _ = (q.num.natAbs:ℚ)/q.den := congrArg (fun a : ℚ => a/q.den)
        (by simpa only [Int.cast_natCast] using congrArg (fun z : ℤ => (z:ℚ)) h.symm)

theorem rational_code_descends_and_separates (address : Nat.Primes ↪ ℕ)
    (z : ℂ) (hz : Transcendental ℚ z) {a b c d : ℕ}
    (ha : a ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0) (hd : d ≠ 0) :
    code address (fun _ => (1:ℚ)) z (valuation a - valuation b) =
      code address (fun _ => (1:ℚ)) z (valuation c - valuation d) ↔ (a:ℚ)/b = (c:ℚ)/d := by
  rw [(exact_code_injective address _ (by simp) z hz).eq_iff]
  exact rational_valuation_equality ha hb hc hd

theorem rational_product_valuations {a b c d : ℕ}
    (ha : a ≠ 0) (hb : b ≠ 0) (hc : c ≠ 0) (hd : d ≠ 0) :
    valuation (a*c) - valuation (b*d) =
      (valuation a - valuation b) + (valuation c - valuation d) := by
  rw [valuation_mul ha hc,valuation_mul hb hd]
  abel

theorem sqrt_weight_algebraic (j : ℕ) : IsAlgebraic ℚ ((Real.sqrt j : ℝ) : ℂ) := by
  refine ⟨X^2 - C (j:ℚ), ?_, ?_⟩
  · intro h
    have hc := congrArg (fun p : ℚ[X] => p.coeff 2) h
    norm_num at hc
  · simp only [map_sub,map_pow,aeval_X,aeval_C,eq_ratCast]
    norm_cast
    have h := Real.sq_sqrt (Nat.cast_nonneg j : (0:ℝ) ≤ j)
    exact sub_eq_zero.mpr (by exact_mod_cast h)

noncomputable def vogelWeight (j : ℕ+) : Subalgebra.algebraicClosure ℚ ℂ :=
  ⟨((Real.sqrt (j:ℕ) : ℝ) : ℂ),sqrt_weight_algebraic j⟩

theorem vogel_weight_nonzero (j : ℕ+) : vogelWeight j ≠ 0 := by
  intro h
  have h' := congrArg (fun x : Subalgebra.algebraicClosure ℚ ℂ => (x:ℂ)) h
  have hj : (0:ℝ) < (j:ℕ) := by exact_mod_cast j.pos
  have hn : Real.sqrt (j:ℕ) ≠ 0 := ne_of_gt (Real.sqrt_pos.mpr hj)
  exact hn (by simpa [vogelWeight] using h')

theorem vogel_code_injective (z : ℂ) (hz : Transcendental ℚ z) :
    Injective (code (fun j : ℕ+ => (j:ℕ)) vogelWeight z) :=
  algebraic_weight_code_injective (⟨(fun j : ℕ+ => (j:ℕ)),Subtype.val_injective⟩ : ℕ+ ↪ ℕ) vogelWeight
    vogel_weight_nonzero z hz

theorem repeated_address_collision :
    weightedPoly (fun _ : Bool => 1) (fun _ => (1:ℚ)) (Finsupp.single false 1) =
    weightedPoly (fun _ : Bool => 1) (fun _ => (1:ℚ)) (Finsupp.single true 1) ∧
    (Finsupp.single false 1 : Bool →₀ ℤ) ≠ Finsupp.single true 1 := by
  constructor
  · simp [weightedPoly]
  · intro h; have h' := congrArg (fun v : Bool →₀ ℤ => v false) h; norm_num at h'

theorem zero_weight_collision :
    weightedPoly (fun _ : Unit => 1) (fun _ => (0:ℚ)) (Finsupp.single () 1) =
    weightedPoly (fun _ : Unit => 1) (fun _ => (0:ℚ)) 0 := by simp [weightedPoly]

end Experiments.GPPREncoding
