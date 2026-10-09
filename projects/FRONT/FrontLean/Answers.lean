import Mathlib
import APCILeanAudit.Interface

/-! FRONT §§7–8, 9.1. The generic fiber theorem is reused verbatim from APCI. -/
namespace FrontLean
open APCILeanAudit

universe u v w

/-- Proposition 3. The decoder's domain is the reachable image, including empty cases. -/
theorem answer_sufficiency {H : Type u} {Z : Type v} {Y : Type w}
    (τ : H → Z) (q : H → Y) :
    ExactOnReachable τ q ↔ ∀ x y, τ x = τ y → q x = q y :=
  exactOnReachable_iff_fiberConstant

/-- Proposition 3A: labels are part of the joint interface. -/
theorem joint_equality {H : Type u} {I : Type v} {Y : I → Type w}
    (o : (i : I) → H → Y i) (x y : H) :
    (fun i => o i x) = (fun i => o i y) ↔ ∀ i, o i x = o i y := by
  exact ⟨fun h i => congrFun h i, fun h => funext h⟩

theorem joint_sufficiency {H : Type u} {I : Type v} {Y : I → Type w}
    {Q : Type*} (o : (i : I) → H → Y i) (q : H → Q) :
    ExactOnReachable (fun x i => o i x) q ↔
      ∀ x y, (∀ i, o i x = o i y) → q x = q y := by
  rw [answer_sufficiency]
  constructor
  · intro h x y hxy
    exact h x y (funext hxy)
  · intro h x y hxy
    exact h x y (fun i => congrFun hxy i)

/-- Proposition 4. Choice on each reachable fiber; finite cases are included.
    The theorem does not supply or compute the adequate-action predicate G. -/
theorem common_action_iff {H Z A : Type*} (τ : H → Z) (G : H → A → Prop) :
    (∃ p : Reachable τ → A, ∀ h, G h (p ⟨τ h, ⟨h, rfl⟩⟩)) ↔
    ∀ z : Reachable τ, ∃ a, ∀ h, τ h = z.val → G h a := by
  classical
  constructor
  · rintro ⟨p, hp⟩ z
    refine ⟨p z, ?_⟩
    intro h hz
    have he : (⟨τ h, ⟨h, rfl⟩⟩ : Reachable τ) = z := Subtype.ext hz
    simpa only [he] using hp h
  · intro h
    refine ⟨fun z => Classical.choose (h z), ?_⟩
    intro x
    exact Classical.choose_spec (h ⟨τ x, ⟨x, rfl⟩⟩) x rfl

/-- Proposition 6: fixed-length exact coordinate encodings, with no external rereading. -/
theorem coordinate_bit_bound (d b : ℕ) (encode : (Fin d → Bool) → (Fin b → Bool))
    (decode : (Fin b → Bool) → Fin d → Bool)
    (correct : ∀ x i, decode (encode x) i = x i) : d ≤ b := by
  have inj : Function.Injective encode := by
    intro x y h
    funext i
    calc
      x i = decode (encode x) i := (correct x i).symm
      _ = decode (encode y) i := congrArg (fun z => decode z i) h
      _ = y i := correct y i
  have hc : 2 ^ d ≤ (2 : ℕ) ^ b := by
    simpa using Fintype.card_le_of_injective encode inj
  exact (Nat.pow_le_pow_iff_right (by decide : 1 < (2 : ℕ))).mp hc

/-- Same answer, different ancestry: the answer-only carrier cannot recover provenance. -/
theorem answer_does_not_recover_history :
    ¬ ExactOnReachable (fun _ : Bool => ()) (fun h : Bool => h) := by
  rw [answer_sufficiency]
  intro h
  have bad := h false true rfl
  cases bad

/-- A retained label `none` is a status; it need not determine the omitted content. -/
theorem absent_reading_is_not_content :
    ¬ ExactOnReachable (fun _ : Bool => (none : Option Bool)) (fun h : Bool => h) := by
  rw [answer_sufficiency]
  intro h
  have bad := h false true rfl
  cases bad

end FrontLean
