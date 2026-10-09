import Experiments.Pal24Continuation

/-!
Explicit declaration inspection for the B1 target. Keep these pairs in the same
order as Audit/pal-v24-batches/B1/claims.json.
-/
set_option pp.fullNames true

#check @Experiments.Pal24Continuation.TransitionProfile
#print axioms Experiments.Pal24Continuation.TransitionProfile
#check @Experiments.Pal24Continuation.run
#print axioms Experiments.Pal24Continuation.run
#check @Experiments.Pal24Continuation.admissibleSuffix
#print axioms Experiments.Pal24Continuation.admissibleSuffix
#check @Experiments.Pal24Continuation.oneSuffixEquivalent
#print axioms Experiments.Pal24Continuation.oneSuffixEquivalent
#check @Experiments.Pal24Continuation.continuationEquivalent
#print axioms Experiments.Pal24Continuation.continuationEquivalent
#check @Experiments.Pal24Continuation.run_append
#print axioms Experiments.Pal24Continuation.run_append
#check @Experiments.Pal24Continuation.one_suffix_of_step_simulation
#print axioms Experiments.Pal24Continuation.one_suffix_of_step_simulation
#check @Experiments.Pal24Continuation.all_finite_suffixes_of_step_simulation
#print axioms Experiments.Pal24Continuation.all_finite_suffixes_of_step_simulation
#check @Experiments.Pal24Continuation.narrowAperture
#print axioms Experiments.Pal24Continuation.narrowAperture
#check @Experiments.Pal24Continuation.apertureStep
#print axioms Experiments.Pal24Continuation.apertureStep
#check @Experiments.Pal24Continuation.narrowProfile
#print axioms Experiments.Pal24Continuation.narrowProfile
#check @Experiments.Pal24Continuation.wideProfile
#print axioms Experiments.Pal24Continuation.wideProfile
#check @Experiments.Pal24Continuation.aperture_expansion_distinguishes_future
#print axioms Experiments.Pal24Continuation.aperture_expansion_distinguishes_future
