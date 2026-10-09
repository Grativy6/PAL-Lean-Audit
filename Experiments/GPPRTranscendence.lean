import Mathlib

namespace Experiments.GPPRTranscendence
open Polynomial

noncomputable def phi : ℝ := (1 + Real.sqrt 5) / 2
noncomputable def beta : ℝ := (phi ^ 2)⁻¹
noncomputable def delta : ℝ := 3 - Real.sqrt 5
noncomputable def zeta : ℂ := Complex.exp (2 * Real.pi * Complex.I * (beta : ℂ))
noncomputable def minusOneLog : ℂ := Real.pi * Complex.I

theorem phi_positive : 0 < phi := by dsimp [phi]; positivity

theorem beta_exact : beta = (3 - Real.sqrt 5)/2 := by
  have hs := Real.sq_sqrt (show (0:ℝ) ≤ 5 by norm_num)
  have hp : phi^2 = (3+Real.sqrt 5)/2 := by dsimp [phi]; nlinarith
  rw [beta,hp]
  apply inv_eq_of_mul_eq_one_left
  nlinarith

theorem exponent_exact : 2*beta = delta := by rw [beta_exact]; dsimp [delta]; ring

theorem delta_irrational : Irrational delta := by
  dsimp [delta]
  exact (show Irrational (Real.sqrt 5) from by simpa using (show Nat.Prime 5 by decide).irrational_sqrt).natCast_sub 3

theorem delta_algebraic : IsAlgebraic ℚ delta := by
  refine ⟨X^2 - C 6 * X + C 4, ?_, ?_⟩
  · intro h
    have hc := congrArg (fun p : ℚ[X] => p.coeff 2) h
    norm_num at hc
  · simp [delta,aeval_def]
    nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ 5 by norm_num)]

theorem chosen_logarithm : Complex.exp minusOneLog = -1 := Complex.exp_pi_mul_I

theorem golden_branch_identity : Complex.exp ((delta : ℂ)*minusOneLog) = zeta := by
  congr 1
  rw [← exponent_exact]
  simp only [Complex.ofReal_mul,Complex.ofReal_ofNat,minusOneLog]
  ring

def GelfondSchneiderRealExponent : Prop :=
  ∀ (a : ℂ) (b : ℝ) (l : ℂ), IsAlgebraic ℚ a → a ≠ 0 → a ≠ 1 →
    IsAlgebraic ℚ b → Irrational b → Complex.exp l = a →
    Transcendental ℚ (Complex.exp ((b : ℂ)*l))

theorem golden_transcendence_conditional (gs : GelfondSchneiderRealExponent) :
    Transcendental ℚ zeta := by
  rw [← golden_branch_identity]
  exact gs (-1) delta minusOneLog (isAlgebraic_one.neg) (by norm_num) (by norm_num)
    delta_algebraic delta_irrational chosen_logarithm

theorem golden_polynomial_evaluation_conditional (hz : Transcendental ℚ zeta) :
    Function.Injective (Polynomial.aeval zeta : ℚ[X] →ₐ[ℚ] ℂ) :=
  transcendental_iff_injective.mp hz

end Experiments.GPPRTranscendence
