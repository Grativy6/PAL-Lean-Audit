import Experiments.BridgeGeneratedRecovery

-- Exact signatures expose the unrestricted answer type.
#check @Experiments.BridgeGeneratedRecovery.generated_answer_decodable_iff
#check @Experiments.BridgeGeneratedRecovery.generated_decoder_unique

-- Regression boundary: the answer type has no additive or module instance.
example {k T R Q : Type*} [Field k] [AddCommGroup T] [Module k T]
    [AddCommGroup R] [Module k R] (B : Submodule k T) (r : T →ₗ[k] R)
    (a : B → Q) :
    (∃ d : LinearMap.range (r.comp B.subtype) → Q,
      d ∘ Experiments.BridgeGeneratedRecovery.generatedRangeReadout B r = a) ↔
      ∀ x y : B, r x.1 = r y.1 → a x = a y :=
  Experiments.BridgeGeneratedRecovery.generated_answer_decodable_iff_fiber B r a

#print axioms Experiments.BridgeGeneratedRecovery.generatedRangeReadout
#print axioms Experiments.BridgeGeneratedRecovery.generated_decoder_unique
#print axioms Experiments.BridgeGeneratedRecovery.generatedAmbientReadout
#print axioms Experiments.BridgeGeneratedRecovery.generated_answer_decodable_iff
#print axioms Experiments.BridgeGeneratedRecovery.generated_answer_decodable_iff_fiber
#print axioms Experiments.BridgeGeneratedRecovery.generated_linear_answer_decodable_iff
#print axioms Experiments.BridgeGeneratedRecovery.generated_identity_decoder_iff_injective
#print axioms Experiments.BridgeGeneratedRecovery.generated_full_identity_iff_collision_bot
#print axioms Experiments.BridgeGeneratedRecovery.generated_identity_answer_decodable_iff_collision_bot
#print axioms Experiments.BridgeGeneratedRecovery.generated_coarser_answer_countercase
#print axioms Experiments.BridgeGeneratedRecovery.generated_nonlinear_kernel_overclaim_countercase
#print axioms Experiments.BridgeGeneratedRecovery.generated_ambient_decoder_nonunique_countercase
