import Mathlib.LinearAlgebra.Prod
import Mathlib.Data.Set.Image
import Mathlib.Tactic.NormNum

/-!
# Bounded BRIDGE endpoint-calculus realization

This file formalizes five elementary, source-bound claims from the exact
algebraic endpoint lane of BRIDGE v0.4.  It does not formalize the document's
Hodge, geometric, or external-reference claims.  In particular, the kernel
condition below is a declared linear realization of the stated endpoint
calculus, rather than a claim about every BRIDGE application.
-/

namespace Experiments.Bridge

section LinearEndpoint

variable {k X Y R : Type*} [Field k]
variable [AddCommGroup X] [Module k X]
variable [AddCommGroup Y] [Module k Y]
variable [AddCommGroup R] [Module k R]

/-- P0054: the frame-relative residue in the bounded linear realization. -/
def residue (readout : Y →ₗ[k] R) (actual comparison : X →ₗ[k] Y) (x : X) : R :=
  readout (actual x - comparison x)

/-- P0066: zero residue is exactly membership in the readout kernel. -/
theorem zero_residue_iff_kernel (readout : Y →ₗ[k] R) (actual comparison : X →ₗ[k] Y)
    (x : X) :
    residue readout actual comparison x = 0 ↔ actual x - comparison x ∈ readout.ker := by
  rfl

/-- P0071: zero exact residue proves equality of the two observable readouts. -/
theorem zero_residue_implies_observable_equality (readout : Y →ₗ[k] R)
    (actual comparison : X →ₗ[k] Y) {x : X}
    (hzero : residue readout actual comparison x = 0) :
    readout (actual x) = readout (comparison x) := by
  rw [residue, map_sub] at hzero
  exact sub_eq_zero.mp hzero

/-- P0073: uniform full equality is equivalent to trivial kernel intersection on admitted differences. -/
theorem uniform_equality_iff_kernel_trivial_on_admitted_differences
    (readout : Y →ₗ[k] R) (actual comparison : X →ₗ[k] Y) (admitted : Set X) :
    (∀ x, x ∈ admitted → residue readout actual comparison x = 0 → actual x = comparison x) ↔
      ∀ y, y ∈ (fun x => actual x - comparison x) '' admitted → y ∈ readout.ker → y = 0 := by
  constructor
  · intro huniform y hy hkernel
    rcases hy with ⟨x, hx, rfl⟩
    exact sub_eq_zero.mpr (huniform x hx
      ((zero_residue_iff_kernel readout actual comparison x).mpr hkernel))
  · intro htrivial x hx hzero
    apply sub_eq_zero.mp
    apply htrivial (actual x - comparison x)
    · exact ⟨x, hx, rfl⟩
    · exact (zero_residue_iff_kernel readout actual comparison x).mp hzero

end LinearEndpoint

/-- P0105--P0107: a reachable decoder exists exactly when the answer is constant on fibers. -/
theorem reachable_decoder_iff_fiber_constant {W S Q : Type} (interface : W → S) (answer : W → Q) :
    (∃ decode : Set.range interface → Q,
      ∀ w, decode ⟨interface w, ⟨w, rfl⟩⟩ = answer w) ↔
      ∀ ⦃w w' : W⦄, interface w = interface w' → answer w = answer w' := by
  constructor
  · rintro ⟨decode, hdecode⟩ w w' hinterface
    have hsub : (⟨interface w, ⟨w, rfl⟩⟩ : Set.range interface) =
        ⟨interface w', ⟨w', rfl⟩⟩ := Subtype.ext hinterface
    rw [← hdecode w, ← hdecode w', hsub]
  · intro hconstant
    let decode : Set.range interface → Q := fun s => answer (Classical.choose s.property)
    refine ⟨decode, ?_⟩
    intro w
    let point : Set.range interface := ⟨interface w, ⟨w, rfl⟩⟩
    change answer (Classical.choose point.property) = answer w
    apply hconstant
    exact point.property.choose_spec

/-- P0073 and P0269: an explicit hidden difference defeats unqualified full recovery. -/
theorem hidden_difference_countermodel :
    let readout : ℚ × ℚ → ℚ := Prod.fst
    let actual : ℚ × ℚ := (0, 1)
    let comparison : ℚ × ℚ := (0, 0)
    readout (actual - comparison) = 0 ∧ actual ≠ comparison := by
  norm_num

end Experiments.Bridge
