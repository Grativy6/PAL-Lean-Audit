import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Tactic.NormNum.Prime
import Mathlib.Tactic.Order
import Mathlib.Tactic.Ring

/-!
# Bounded CHARTER arithmetic realization

This file formalizes selected integer- and natural-number arithmetic in
CHARTER v1.0, especially P0600--P0621. `primeShellIndex` is a declared
coordinate calculation. The three finite primality checks are exact; they do
not establish a prime-valued family, performance, or any systems conclusion.
The source BPS subclass requires `m ≥ 1`; the algebraic Nat identities here
also admit `m = 0` and make no BPS claim at that extension point.
-/

namespace Experiments.Charter

/-- The CHARTER norm coordinate has its stated integer-lattice domain. -/
def Q (a b : ℤ) : ℤ := a ^ 2 + a * b + b ^ 2

/-- Nonnegative specialization used by the finite bank arithmetic. -/
def natQ (a b : Nat) : Nat := a ^ 2 + a * b + b ^ 2

def bankTotal (m : Nat) : Nat := 2 * m + 1

def primeShellIndex (m : Nat) : Nat := natQ (m + 1) m

/-- P0612--P0618: the elementary norm decomposition for the integer lattice. -/
theorem four_Q_identity (a b : ℤ) :
    4 * Q a b = 3 * (a + b) ^ 2 + (a - b) ^ 2 := by
  simp [Q]
  ring

/-- The direct polynomial expansion, used without interpreting the coordinate as a prime. -/
theorem adjacent_index_formula (m : Nat) :
    primeShellIndex m = 3 * m ^ 2 + 3 * m + 1 := by
  simp [primeShellIndex, natQ]
  ring

/-- P0019 after substituting the odd total. -/
theorem four_adjacent_index_formula (m : Nat) :
    4 * primeShellIndex m = 3 * bankTotal m ^ 2 + 1 := by
  simp [primeShellIndex, bankTotal, natQ]
  ring

/-- P0016: the adjacent banks have the declared odd total. -/
theorem adjacent_banks_total (m : Nat) :
    (m + 1) + m = bankTotal m := by
  simp [bankTotal]
  omega

/-- P0016: adjacent banks are ordered and distinct. -/
theorem adjacent_banks_ordered_distinct (m : Nat) : m < m + 1 := by omega

/-- P0016: a closest ordered split is uniquely determined once its gap is one. -/
theorem closest_ordered_distinct_split_unique {m a b : Nat}
    (total : a + b = bankTotal m) (gap : a - b = 1) (ordered : b < a) :
    a = m + 1 ∧ b = m := by
  simp [bankTotal] at total
  omega

/-- P0016: any ordered distinct Nat split has a positive gap. -/
theorem ordered_distinct_gap_positive {a b : Nat} (ordered : b < a) : 0 < a - b := by
  omega

/-- P0016: among ordered distinct Nat splits of this odd total, the adjacent split minimizes Q. -/
theorem adjacent_banks_minimize_Q {m a b : Nat}
    (total : a + b = bankTotal m) (ordered : b < a) :
    primeShellIndex m ≤ natQ a b := by
  rw [adjacent_index_formula]
  have hb : b ≤ m := by
    simp [bankTotal] at total
    omega
  obtain ⟨c, hc⟩ := Nat.exists_eq_add_of_le hb
  have ha : a = b + 2 * c + 1 := by
    simp [bankTotal] at total
    omega
  subst a
  subst m
  calc
    3 * (b + c) ^ 2 + 3 * (b + c) + 1 ≤
        3 * (b + c) ^ 2 + 3 * (b + c) + 1 + (c ^ 2 + c) :=
      Nat.le_add_right (3 * (b + c) ^ 2 + 3 * (b + c) + 1) (c ^ 2 + c)
    _ = natQ (b + 2 * c + 1) b := by
      simp [natQ]
      ring

/-- P0020: the stated concrete composite shell index. -/
theorem index_five_is_ninety_one : primeShellIndex 5 = 91 := by norm_num [primeShellIndex, natQ]

/-- P0020: 91 has the displayed nontrivial factorization. -/
theorem ninety_one_factorization : 91 = 7 * 13 := by norm_num

/-- P0020: an infinite indexed subfamily has an explicit nontrivial factor. -/
theorem composite_subfamily_factorization (k : Nat) :
    primeShellIndex (7 * k + 5) = 7 * (21 * k ^ 2 + 33 * k + 13) := by
  simp [primeShellIndex, natQ]
  ring

/-- P0020: every member of the displayed subfamily is composite by its supplied factorization. -/
theorem composite_subfamily (k : Nat) :
    ¬ Nat.Prime (primeShellIndex (7 * k + 5)) := by
  rw [composite_subfamily_factorization]
  apply Nat.not_prime_mul
  norm_num
  omega

/-- Exact small primality check; it does not generalize to the full sequence. -/
theorem index_one_prime : Nat.Prime (primeShellIndex 1) := by norm_num [primeShellIndex, natQ]

/-- Exact small primality check; it does not generalize to the full sequence. -/
theorem index_two_prime : Nat.Prime (primeShellIndex 2) := by norm_num [primeShellIndex, natQ]

/-- Exact small primality check; it does not generalize to the full sequence. -/
theorem index_three_prime : Nat.Prime (primeShellIndex 3) := by norm_num [primeShellIndex, natQ]

end Experiments.Charter
