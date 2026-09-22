import Experiments.Pal23Roundtrip

/-- Regression fixture: the answer codomain has no required structure. -/
example {W : Type u} {C : Type v} {Q : Type w}
    (freeze : W → C) (thaw : C → W)
    (hreachable : ∀ x, freeze (thaw (freeze x)) = freeze x)
    (answer : W → Q) :
    (∀ x, answer (thaw (freeze x)) = answer x) ↔
      ∀ ⦃x y⦄, freeze x = freeze y → answer x = answer y :=
  Experiments.Pal23Roundtrip.chosen_answer_preserved_iff_fiber_constant
    freeze thaw hreachable answer

#check @Experiments.Pal23Roundtrip.replayWork
#check @Experiments.Pal23Roundtrip.capsule_cycle_idempotent
#check @Experiments.Pal23Roundtrip.work_roundtrip_iff_freeze_injective
#check @Experiments.Pal23Roundtrip.source_roundtrip_freeze_injective
#check @Experiments.Pal23Roundtrip.source_roundtrip_preserves_answer
#check @Experiments.Pal23Roundtrip.same_suffix_under_work_roundtrip
#check @Experiments.Pal23Roundtrip.chosen_answer_preserved_iff_fiber_constant
#check @Experiments.Pal23Roundtrip.natBoolFreeze
#check @Experiments.Pal23Roundtrip.natBoolThaw
#check @Experiments.Pal23Roundtrip.natBool_capsule_roundtrip
#check @Experiments.Pal23Roundtrip.natBool_stable_but_not_recovered
#check @Experiments.Pal23Roundtrip.natBool_no_full_work_decoder
#check @Experiments.Pal23Roundtrip.natBool_first_answer_preserved
#check @Experiments.Pal23Roundtrip.natBool_second_answer_not_preserved
#check @Experiments.Pal23Roundtrip.natBool_chosen_suffix_vs_other_suffix
#check @Experiments.Pal23Roundtrip.exact_work_roundtrip_not_ambient_capsule_roundtrip

#print axioms Experiments.Pal23Roundtrip.replayWork
#print axioms Experiments.Pal23Roundtrip.capsule_cycle_idempotent
#print axioms Experiments.Pal23Roundtrip.work_roundtrip_iff_freeze_injective
#print axioms Experiments.Pal23Roundtrip.source_roundtrip_freeze_injective
#print axioms Experiments.Pal23Roundtrip.source_roundtrip_preserves_answer
#print axioms Experiments.Pal23Roundtrip.same_suffix_under_work_roundtrip
#print axioms Experiments.Pal23Roundtrip.chosen_answer_preserved_iff_fiber_constant
#print axioms Experiments.Pal23Roundtrip.natBoolFreeze
#print axioms Experiments.Pal23Roundtrip.natBoolThaw
#print axioms Experiments.Pal23Roundtrip.natBool_capsule_roundtrip
#print axioms Experiments.Pal23Roundtrip.natBool_stable_but_not_recovered
#print axioms Experiments.Pal23Roundtrip.natBool_no_full_work_decoder
#print axioms Experiments.Pal23Roundtrip.natBool_first_answer_preserved
#print axioms Experiments.Pal23Roundtrip.natBool_second_answer_not_preserved
#print axioms Experiments.Pal23Roundtrip.natBool_chosen_suffix_vs_other_suffix
#print axioms Experiments.Pal23Roundtrip.exact_work_roundtrip_not_ambient_capsule_roundtrip

#check @Experiments.Pal23Roundtrip.fiber_constant_does_not_validate_faulty_thaw
#print axioms Experiments.Pal23Roundtrip.fiber_constant_does_not_validate_faulty_thaw
