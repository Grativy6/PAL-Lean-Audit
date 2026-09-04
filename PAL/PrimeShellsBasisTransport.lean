import PAL.PrimeShellsConditioning

/-!
# Basis uniqueness and characterized shell transport

This file closes two structural claims needed by the proposed Prime Shells
manuscript:

1. a ready conjugate pair is not only sufficient to reconstruct every planar
   vector; its two coefficients are unique;
2. the declared shell-to-shell transport is the unique map preserving linear
   combinations and sending the selected/reflected source pair to the
   selected/reflected target pair.

It also records the sharpness of the squared condition bound `3` against all
three unit-rotation choices at the ramified norm-3 shell.
-/

namespace PAL.PrimeShells

noncomputable section

/-- A ready conjugate pair is linearly independent. -/
theorem conjugate_references_independent (x : Point ℝ) (hx : FrameReady x)
    {c d : ℝ}
    (h : combine c d (scaledEmbed x) (scaledEmbed (conj x)) = origin) :
    c = 0 ∧ d = 0 := by
  rw [scaledEmbed_conj] at h
  have ha : c * xCoord x + d * xCoord x = 0 := by
    simpa [combine, scaledEmbed, origin] using congrArg Point.a h
  have hb : c * yCoord x + d * (-yCoord x) = 0 := by
    simpa [combine, scaledEmbed, origin] using congrArg Point.b h
  have hsumProduct : (c + d) * xCoord x = 0 := by
    calc
      (c + d) * xCoord x = c * xCoord x + d * xCoord x := by ring
      _ = 0 := ha
  have hdiffProduct : (c - d) * yCoord x = 0 := by
    calc
      (c - d) * yCoord x = c * yCoord x + d * (-yCoord x) := by ring
      _ = 0 := hb
  have hsum : c + d = 0 := (mul_eq_zero.mp hsumProduct).resolve_right hx.1
  have hdiff : c - d = 0 := (mul_eq_zero.mp hdiffProduct).resolve_right hx.2
  constructor <;> linarith

/-- The explicit conjugate-frame coordinates are unique. -/
theorem conjugate_reference_coefficients_unique (x v : Point ℝ) (hx : FrameReady x)
    {c d : ℝ}
    (h : combine c d (scaledEmbed x) (scaledEmbed (conj x)) = v) :
    c = plusCoefficient x v ∧ d = minusCoefficient x v := by
  have hcanonical := two_references_reconstruct x v hx
  have hzero :
      combine (c - plusCoefficient x v) (d - minusCoefficient x v)
        (scaledEmbed x) (scaledEmbed (conj x)) = origin := by
    apply Point.extensionality
    · change
        (c - plusCoefficient x v) * (scaledEmbed x).a +
            (d - minusCoefficient x v) * (scaledEmbed (conj x)).a = 0
      calc
        _ =
            (c * (scaledEmbed x).a + d * (scaledEmbed (conj x)).a) -
              (plusCoefficient x v * (scaledEmbed x).a +
                minusCoefficient x v * (scaledEmbed (conj x)).a) := by ring
        _ = v.a - v.a := by
          rw [show c * (scaledEmbed x).a + d * (scaledEmbed (conj x)).a = v.a by
                simpa [combine] using congrArg Point.a h,
              show plusCoefficient x v * (scaledEmbed x).a +
                  minusCoefficient x v * (scaledEmbed (conj x)).a = v.a by
                simpa [combine] using congrArg Point.a hcanonical]
        _ = 0 := sub_self v.a
    · change
        (c - plusCoefficient x v) * (scaledEmbed x).b +
            (d - minusCoefficient x v) * (scaledEmbed (conj x)).b = 0
      calc
        _ =
            (c * (scaledEmbed x).b + d * (scaledEmbed (conj x)).b) -
              (plusCoefficient x v * (scaledEmbed x).b +
                minusCoefficient x v * (scaledEmbed (conj x)).b) := by ring
        _ = v.b - v.b := by
          rw [show c * (scaledEmbed x).b + d * (scaledEmbed (conj x)).b = v.b by
                simpa [combine] using congrArg Point.b h,
              show plusCoefficient x v * (scaledEmbed x).b +
                  minusCoefficient x v * (scaledEmbed (conj x)).b = v.b by
                simpa [combine] using congrArg Point.b hcanonical]
        _ = 0 := sub_self v.b
  obtain ⟨hc, hd⟩ := conjugate_references_independent x hx hzero
  constructor <;> linarith

/-- The declared transport preserves arbitrary two-vector linear combinations. -/
theorem transport_combine (x y u v : Point ℝ) (c d : ℝ) :
    transport x y (combine c d u v) =
      combine c d (transport x y u) (transport x y v) := by
  apply Point.extensionality <;> simp [transport, combine] <;> ring

/-- Minimal linearity contract used to characterize the transport map. -/
def PreservesCombinations (f : Point ℝ → Point ℝ) : Prop :=
  ∀ c d : ℝ, ∀ u v : Point ℝ,
    f (combine c d u v) = combine c d (f u) (f v)

/-- The declared shell transport satisfies the linearity contract. -/
theorem transport_preservesCombinations (x y : Point ℝ) :
    PreservesCombinations (transport x y) := by
  intro c d u v
  exact transport_combine x y u v c d

/-- A linear-combination-preserving map is uniquely determined by where it sends
one ready conjugate reference pair. -/
theorem transport_unique (x y : Point ℝ) (hx : FrameReady x)
    (f : Point ℝ → Point ℝ) (hf : PreservesCombinations f)
    (hSelected : f (scaledEmbed x) = scaledEmbed y)
    (hReflected : f (scaledEmbed (conj x)) = scaledEmbed (conj y)) :
    f = transport x y := by
  funext v
  let c := plusCoefficient x v
  let d := minusCoefficient x v
  have hv : combine c d (scaledEmbed x) (scaledEmbed (conj x)) = v := by
    simpa [c, d] using two_references_reconstruct x v hx
  calc
    f v = f (combine c d (scaledEmbed x) (scaledEmbed (conj x))) := by rw [hv]
    _ = combine c d (f (scaledEmbed x)) (f (scaledEmbed (conj x))) :=
      hf c d (scaledEmbed x) (scaledEmbed (conj x))
    _ = combine c d (scaledEmbed y) (scaledEmbed (conj y)) := by
      rw [hSelected, hReflected]
    _ = combine c d (transport x y (scaledEmbed x))
          (transport x y (scaledEmbed (conj x))) := by
      rw [transport_selected x y hx, transport_reflected x y hx]
    _ = transport x y (combine c d (scaledEmbed x) (scaledEmbed (conj x))) := by
      symm
      exact transport_combine x y (scaledEmbed x) (scaledEmbed (conj x)) c d
    _ = transport x y v := by rw [hv]

/-- No squared conditioning constant below `3` works for any of the three
unit-rotation choices at the ramified norm-3 shell. -/
theorem ramified_no_condition_bound_below_three (C : ℝ) (hC : C < 3)
    (k : FrameChoice) :
    ¬ ConditionBoundSq C (choosePoint k ramifiedFramePoint) := by
  intro h
  cases k with
  | base =>
      have hfirst := h.1
      norm_num [ConditionBoundSq, horizontalFrameEnergy, verticalFrameEnergy,
        ramifiedFramePoint, choosePoint, rotate, xCoord, yCoord] at hfirst
      nlinarith
  | turn =>
      have hsecond := h.2
      norm_num [ConditionBoundSq, horizontalFrameEnergy, verticalFrameEnergy,
        ramifiedFramePoint, choosePoint, rotate, xCoord, yCoord] at hsecond
  | turnTwice =>
      have hfirst := h.1
      norm_num [ConditionBoundSq, horizontalFrameEnergy, verticalFrameEnergy,
        ramifiedFramePoint, choosePoint, rotate, xCoord, yCoord] at hfirst
      nlinarith

/-- The universal squared conditioning constant `3` is attained and cannot be
lowered, even when the selector may choose among all three unit rotations. -/
theorem universal_condition_constant_three_is_sharp :
    (∀ x : Point ℝ, eNorm x ≠ 0 →
      ∃ k : FrameChoice, ConditionBoundSq 3 (choosePoint k x)) ∧
    (∃ x : Point ℝ, eNorm x = 3 ∧
      ∀ C : ℝ, C < 3 →
        ∀ k : FrameChoice, ¬ ConditionBoundSq C (choosePoint k x)) := by
  constructor
  · intro x hNorm
    obtain ⟨k, -, -, hCondition⟩ :=
      exists_sharply_conditioned_frame_choice x hNorm
    exact ⟨k, hCondition⟩
  · exact ⟨ramifiedFramePoint, eNorm_ramifiedFramePoint,
      ramified_no_condition_bound_below_three⟩

end

end PAL.PrimeShells
