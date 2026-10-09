import Mathlib.Data.Set.Function
import Mathlib.Tactic

namespace Experiments.CompactificationProfile
open Set Function

def Lost {W T Q : Type*} (trace : W → T) (answer : W → Q) : Set (W × W) :=
  {p | trace p.1 = trace p.2 ∧ answer p.1 ≠ answer p.2}

theorem refinement_exact {W T S Q : Type*} (t : W → T) (s : W → S) (q : W → Q) :
    Lost (fun w => (t w,s w)) q = Lost t q ∩ {p | s p.1 = s p.2} := by
  ext p; simp only [Lost, mem_setOf_eq, mem_inter_iff, Prod.mk.injEq]; tauto

theorem derived_side_changes_no_loss {W T S Q : Type*} (t : W → T) (s : T → S) (q : W → Q) :
    Lost (fun w => (t w,s (t w))) q = Lost t q := by
  ext p
  simp only [Lost, mem_setOf_eq, Prod.mk.injEq]
  exact ⟨fun h => ⟨h.1.1,h.2⟩,fun h => ⟨⟨h.1,congrArg s h.1⟩,h.2⟩⟩

theorem postprocessing_inclusion {W T S Q : Type*} (t : W → T) (p : T → S) (q : W → Q) :
    Lost t q ⊆ Lost (p ∘ t) q := fun _ h => ⟨congrArg p h.1,h.2⟩

theorem postprocessing_equality {W T S Q : Type*} (t : W → T) (p : T → S) (q : W → Q)
    (hp : Set.InjOn p (range t)) : Lost (p ∘ t) q = Lost t q := by
  apply Subset.antisymm
  · intro a h; exact ⟨hp (mem_range_self _) (mem_range_self _) h.1,h.2⟩
  · exact postprocessing_inclusion t p q

theorem question_coarsening {W T Q Q' : Type*} (t : W → T) (q : W → Q) (h : Q → Q') :
    Lost t (h ∘ q) ⊆ Lost t q := by
  intro a ha
  exact ⟨ha.1,fun he => ha.2 (congrArg h he)⟩

theorem question_injective_equality {W T Q Q' : Type*} (t : W → T) (q : W → Q) (h : Q → Q')
    (hh : Set.InjOn h (range q)) : Lost t (h ∘ q) = Lost t q := by
  apply Subset.antisymm (question_coarsening t q h)
  intro a ha
  exact ⟨ha.1,fun he => ha.2 (hh (mem_range_self _) (mem_range_self _) he)⟩

theorem strict_loss_controls :
    Lost (id : Bool → Bool) id = ∅ ∧
    (false,true) ∈ Lost (fun _ : Bool => ()) id ∧
    Lost (fun _ : Bool => ()) (fun _ => ()) = ∅ := by
  simp [Lost, Set.ext_iff]

@[reducible]
def Extension {A S : Type*} (restrict : A → S) (admissible : A → Prop) (base : S) :=
  {a : A // admissible a ∧ restrict a = base}

theorem quotient_descent_iff {A D : Type*} (r : Setoid A) (f : A → D) :
    (∀ a b, r a b → f a = f b) ↔
      ∃! d : Quotient r → D, ∀ a, d (Quotient.mk r a) = f a := by
  constructor
  · intro hf
    refine ⟨Quotient.lift f hf, fun _ => rfl, ?_⟩
    intro d hd
    funext q
    induction q using Quotient.inductionOn with
    | h a => exact hd a
  · rintro ⟨d,hd,_⟩ a b hab
    rw [← hd a, ← hd b, Quotient.sound hab]

def extensionEquiv {A B S : Type*} (e : A ≃ B) (rA : A → S) (rB : B → S)
    (aA : A → Prop) (aB : B → Prop) (base : S)
    (adm : ∀ a, aB (e a) ↔ aA a) (res : ∀ a, rB (e a) = rA a) :
    Extension rA aA base ≃ Extension rB aB base where
  toFun a := ⟨e a.val, (adm a.val).2 a.property.1, (res a.val).trans a.property.2⟩
  invFun b := ⟨e.symm b.val, by
    constructor
    · apply (adm (e.symm b.val)).1; simpa using b.property.1
    · rw [← res, e.apply_symm_apply]; exact b.property.2⟩
  left_inv a := Subtype.ext (e.symm_apply_apply a.val)
  right_inv b := Subtype.ext (e.apply_symm_apply b.val)

theorem extension_existence_preserved {A B : Type*} (e : A ≃ B) : Nonempty A ↔ Nonempty B := by
  constructor
  · rintro ⟨a⟩; exact ⟨e a⟩
  · rintro ⟨b⟩; exact ⟨e.symm b⟩

theorem detector_image_transport {A B D : Type*} (e : A ≃ B)
    (dA : A → D) (dB : B → D) (hd : ∀ a, dB (e a) = dA a) : range dA = range dB := by
  ext d
  constructor
  · rintro ⟨a,rfl⟩; exact ⟨e a,hd a⟩
  · rintro ⟨b,rfl⟩; exact ⟨e.symm b,by simpa using (hd (e.symm b)).symm⟩

theorem loss_transport {A B T Q : Type*} (e : A ≃ B)
    (tA : A → T) (tB : B → T) (qA : A → Q) (qB : B → Q)
    (ht : ∀ a, tB (e a) = tA a) (hq : ∀ a, qB (e a) = qA a) :
    Lost tA qA = (fun p : A × A => (e p.1,e p.2)) ⁻¹' Lost tB qB := by
  ext p; simp [Lost,ht,hq]

theorem empty_extensions_vacuous_decoder :
    (∀ a b : Empty, (fun _ : Empty => ()) a = (fun _ => ()) b → a = b) ∧
    ¬ Nonempty Empty := by
  constructor
  · intro a; exact nomatch a
  · rintro ⟨a⟩; exact nomatch a

theorem undefined_is_not_zero : (none : Option ℤ) ≠ some 0 := by decide

theorem empty_reachable_decoder :
    ∃ d : Set.range (fun _ : Empty => ()) → Bool,
      ∀ a : Empty, d ⟨(), ⟨a,rfl⟩⟩ = false := by
  exact ⟨fun _ => false, fun a => nomatch a⟩

theorem compatible_restriction_telescope {A B C G : Type*} [AddCommGroup G]
    (rAB : A → B) (rBC : B → C) (iA : A → G) (iB : B → G) (iC : C → G) (a : A) :
    iA a-iC (rBC (rAB a)) =
      (iA a-iB (rAB a)) + (iB (rAB a)-iC (rBC (rAB a))) := by abel

theorem equivalent_carriers_do_not_force_detector_agreement :
    ∃ (e : Bool ≃ Bool) (dA dB : Bool → Bool), range dA ≠ range dB := by
  refine ⟨Equiv.refl _, fun _ => false, fun _ => true, ?_⟩
  simp

end Experiments.CompactificationProfile
