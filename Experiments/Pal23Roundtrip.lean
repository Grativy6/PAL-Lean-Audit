/-!
# PAL v2.3 A12 capsule round-trip audit

The generic claims use only functions and equality over unstructured types. The
Nat × Bool fixture is an explicit model separating capsule re-entry from work
recovery. The source work round-trip and the additional capsule-cycle law are
distinct assumptions.
-/
namespace Experiments.Pal23Roundtrip

universe uW uC uQ
variable {W : Type uW} {C : Type uC} {Q : Type uQ}

/-- The work state obtained by freezing and thawing. -/
def replayWork (freeze : W → C) (thaw : C → W) : W → W := thaw ∘ freeze

/-- The additional capsule-cycle assumption makes replay idempotent. -/
theorem capsule_cycle_idempotent (freeze : W → C) (thaw : C → W)
    (hcapsule : ∀ c, freeze (thaw c) = c) (w : W) :
    replayWork freeze thaw (replayWork freeze thaw w) = replayWork freeze thaw w := by
  change thaw (freeze (thaw (freeze w))) = thaw (freeze w)
  exact congrArg thaw (hcapsule (freeze w))

/-- With the additional capsule-cycle assumption, exact work replay is equivalent to freeze injectivity. -/
theorem work_roundtrip_iff_freeze_injective (freeze : W → C) (thaw : C → W)
    (hcapsule : ∀ c, freeze (thaw c) = c) :
    (∀ w, replayWork freeze thaw w = w) ↔ Function.Injective freeze := by
  constructor
  · intro hround x y hxy
    calc
      x = thaw (freeze x) := (hround x).symm
      _ = thaw (freeze y) := congrArg thaw hxy
      _ = y := hround y
  · intro hinj w
    change thaw (freeze w) = w
    apply hinj
    rw [hcapsule]

/-- The Atlas work round-trip law forces freeze injectivity. -/
theorem source_roundtrip_freeze_injective (freeze : W → C) (thaw : C → W)
    (hwork : ∀ w, thaw (freeze w) = w) : Function.Injective freeze := by
  intro x y hxy
  rw [← hwork x, ← hwork y, hxy]

/-- The Atlas work round-trip law preserves any selected answer on work. -/
theorem source_roundtrip_preserves_answer (freeze : W → C) (thaw : C → W)
    (hwork : ∀ w, thaw (freeze w) = w) (answer : W → Q) (w : W) :
    answer (replayWork freeze thaw w) = answer w := by
  change answer (thaw (freeze w)) = answer w
  rw [hwork]

/-- The Atlas work round-trip law preserves the output of any fixed suffix. -/
theorem same_suffix_under_work_roundtrip (freeze : W → C) (thaw : C → W)
    (hwork : ∀ w, replayWork freeze thaw w = w) (suffix : W → Q) (w : W) :
    suffix (replayWork freeze thaw w) = suffix w := by
  rw [hwork]

/-- If the capsule-cycle law holds on the reachable freeze image, answer preservation is equivalent to constancy on freeze fibers. -/
theorem chosen_answer_preserved_iff_fiber_constant (freeze : W → C) (thaw : C → W)
    (hreachable : ∀ w, freeze (thaw (freeze w)) = freeze w) (answer : W → Q) :
    (∀ w, answer (replayWork freeze thaw w) = answer w) ↔
      ∀ ⦃w w'⦄, freeze w = freeze w' → answer w = answer w' := by
  constructor
  · intro h w w' hfreeze
    calc
      answer w = answer (replayWork freeze thaw w) := (h w).symm
      _ = answer (replayWork freeze thaw w') := by
        change answer (thaw (freeze w)) = answer (thaw (freeze w'))
        rw [hfreeze]
      _ = answer w' := h w'
  · intro hfiber w
    apply hfiber
    change freeze (thaw (freeze w)) = freeze w
    exact hreachable w

/-- Fiber constancy alone does not make a faulty thaw preserve an answer. -/
theorem fiber_constant_does_not_validate_faulty_thaw :
    let freeze : Nat → Nat := id
    let thaw : Nat → Nat := fun _ => 0
    let answer : Nat → Nat := id
    (∀ ⦃n m : Nat⦄, freeze n = freeze m → answer n = answer m) ∧
      answer (replayWork freeze thaw 1) ≠ answer 1 := by
  exact ⟨by intro n m h; exact h, by decide⟩

/-- Freeze drops the Boolean work coordinate. -/
def natBoolFreeze : Nat × Bool → Nat := Prod.fst

/-- Thaw chooses `false` for the dropped Boolean coordinate. -/
def natBoolThaw : Nat → Nat × Bool := fun n => (n, false)

/-- This fixture satisfies the capsule cycle exactly. -/
theorem natBool_capsule_roundtrip (n : Nat) :
    natBoolFreeze (natBoolThaw n) = n := rfl

/-- Replay is stable, yet the explicit input `(0, true)` is not recovered. -/
theorem natBool_stable_but_not_recovered :
    (∀ w, replayWork natBoolFreeze natBoolThaw (replayWork natBoolFreeze natBoolThaw w) =
      replayWork natBoolFreeze natBoolThaw w) ∧
      replayWork natBoolFreeze natBoolThaw (0, true) ≠ (0, true) := by
  constructor
  · intro w
    cases w with
    | mk n b => cases b <;> rfl
  · decide

/-- No total decoder from the Nat capsule can recover every Nat × Bool work state. -/
theorem natBool_no_full_work_decoder :
    ¬ ∃ decode : Nat → Nat × Bool, ∀ w, decode (natBoolFreeze w) = w := by
  rintro ⟨decode, hdecode⟩
  have hfalse := hdecode (0, false)
  have htrue := hdecode (0, true)
  have : (0, false) = (0, true) := hfalse.symm.trans htrue
  cases this

/-- The first-coordinate answer is preserved by the chosen thaw. -/
theorem natBool_first_answer_preserved (w : Nat × Bool) :
    (replayWork natBoolFreeze natBoolThaw w).1 = w.1 := by
  cases w
  rfl

/-- The second-coordinate answer fails preservation at `(0, true)`. -/
theorem natBool_second_answer_not_preserved :
    (replayWork natBoolFreeze natBoolThaw (0, true)).2 ≠ true := by decide

/-- A chosen suffix reading the first coordinate survives; an arbitrary suffix need not. -/
theorem natBool_chosen_suffix_vs_other_suffix :
    (fun w : Nat × Bool => w.1) (replayWork natBoolFreeze natBoolThaw (0, true)) =
      (fun w : Nat × Bool => w.1) (0, true) ∧
    (fun w : Nat × Bool => w.2) (replayWork natBoolFreeze natBoolThaw (0, true)) ≠
      (fun w : Nat × Bool => w.2) (0, true) := by
  decide

/-- Work round-trip does not entail an ambient capsule cycle: capsule zero is unreachable. -/
theorem exact_work_roundtrip_not_ambient_capsule_roundtrip :
    (∀ n : Nat, Nat.pred (n + 1) = n) ∧ Nat.succ (Nat.pred 0) ≠ 0 := by
  constructor
  · intro n
    simp
  · decide

end Experiments.Pal23Roundtrip
