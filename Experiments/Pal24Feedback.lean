import Mathlib.Data.Bool.Basic

/-! PAL v2.4 candidate batch C4: a bounded extensional realization of PAL-v2.3-M
P0687--P0701 (Atlas SHA-256 c053292376363edd6fc743f0f2e31e3bb3850edc78ade3a289bbb07e7e8452c5).
Lineage is carried as explicit data. Dependence is only an admitted-domain function
property; no causal interpretation is encoded.
-/
namespace Experiments.Pal24Feedback

universe uX uU uY uL uS

structure RetainedOutput (Y : Type uY) (Lineage : Type uL) where
  value : Y
  lineage : Lineage
  deriving DecidableEq, Repr

structure LaterSuccessor (State : Type uS) (Lineage : Type uL) where
  state : State
  lineage : Lineage
  deriving DecidableEq, Repr

structure FeedbackCertificate
    {X : Type uX} {U : Type uU} {Y : Type uY} {Lineage : Type uL} {State : Type uS}
    (Adm : X → U → RetainedOutput Y Lineage → Prop)
    (F : X → U → RetainedOutput Y Lineage → LaterSuccessor State Lineage) where
  input : X
  action : U
  first : RetainedOutput Y Lineage
  second : RetainedOutput Y Lineage
  first_admitted : Adm input action first
  second_admitted : Adm input action second
  retained_distinct : first ≠ second
  successors_distinct : F input action first ≠ F input action second

def AdmittedVariation
    {X : Type uX} {U : Type uU} {Y : Type uY} {Lineage : Type uL} {State : Type uS}
    (Adm : X → U → RetainedOutput Y Lineage → Prop)
    (F : X → U → RetainedOutput Y Lineage → LaterSuccessor State Lineage) : Prop :=
  ∃ x u first second,
    Adm x u first ∧ Adm x u second ∧ first ≠ second ∧ F x u first ≠ F x u second

theorem feedback_certificate_iff_admitted_variation
    {X : Type uX} {U : Type uU} {Y : Type uY} {Lineage : Type uL} {State : Type uS}
    (Adm : X → U → RetainedOutput Y Lineage → Prop)
    (F : X → U → RetainedOutput Y Lineage → LaterSuccessor State Lineage) :
    Nonempty (FeedbackCertificate Adm F) ↔ AdmittedVariation Adm F := by
  constructor
  · rintro ⟨certificate⟩
    exact ⟨certificate.input, certificate.action, certificate.first, certificate.second,
      certificate.first_admitted, certificate.second_admitted,
      certificate.retained_distinct, certificate.successors_distinct⟩
  · rintro ⟨input, action, first, second, hfirst, hsecond, hdistinct, hsuccessors⟩
    exact ⟨{
      input := input
      action := action
      first := first
      second := second
      first_admitted := hfirst
      second_admitted := hsecond
      retained_distinct := hdistinct
      successors_distinct := hsuccessors
    }⟩

theorem y_independence_forbids_feedback_certificate
    {X : Type uX} {U : Type uU} {Y : Type uY} {Lineage : Type uL} {State : Type uS}
    (Adm : X → U → RetainedOutput Y Lineage → Prop)
    (F : X → U → RetainedOutput Y Lineage → LaterSuccessor State Lineage)
    (hIndependent : ∀ x u first second, F x u first = F x u second) :
    ¬ Nonempty (FeedbackCertificate Adm F) := by
  rintro ⟨certificate⟩
  exact certificate.successors_distinct
    (hIndependent certificate.input certificate.action certificate.first certificate.second)

def boolRetainedFalse : RetainedOutput Bool Unit := ⟨false, ()⟩

def boolRetainedTrue : RetainedOutput Bool Unit := ⟨true, ()⟩

def boolEcho : Unit → Unit → RetainedOutput Bool Unit → LaterSuccessor Bool Unit :=
  fun _ _ retained => ⟨retained.value, retained.lineage⟩

def restrictedAdmission : Unit → Unit → RetainedOutput Bool Unit → Prop :=
  fun _ _ retained => retained.value = false

theorem bool_echo_nonconstant_on_full_domain :
    boolEcho () () boolRetainedFalse ≠ boolEcho () () boolRetainedTrue := by
  decide

theorem restricted_admitted_domain_has_no_feedback_variation :
    ¬ AdmittedVariation restrictedAdmission boolEcho := by
  rintro ⟨input, action, ⟨firstValue, firstLineage⟩, ⟨secondValue, secondLineage⟩,
    hfirst, hsecond, hdistinct, _⟩
  dsimp [restrictedAdmission] at hfirst hsecond
  subst firstValue
  subst secondValue
  cases firstLineage
  cases secondLineage
  exact hdistinct rfl

def allBoolOutputsAdmitted : Unit → Unit → RetainedOutput Bool Unit → Prop :=
  fun _ _ _ => True

theorem finite_positive_feedback_fixture :
    Nonempty (FeedbackCertificate allBoolOutputsAdmitted boolEcho) := by
  apply (feedback_certificate_iff_admitted_variation allBoolOutputsAdmitted boolEcho).2
  exact ⟨(), (), boolRetainedFalse, boolRetainedTrue, trivial, trivial, by decide, by decide⟩

theorem bool_echo_preserves_lineage
    (input action : Unit) (retained : RetainedOutput Bool Unit) :
    (boolEcho input action retained).lineage = retained.lineage := rfl

end Experiments.Pal24Feedback
