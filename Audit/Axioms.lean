import FrontLean

-- Signatures and transitive axioms for every public authored/inherited declaration.
#check @APCILeanAudit.FiberConstant
#print axioms APCILeanAudit.FiberConstant
#check @APCILeanAudit.ExactCertificate
#print axioms APCILeanAudit.ExactCertificate
#check @APCILeanAudit.Reachable
#print axioms APCILeanAudit.Reachable
#check @APCILeanAudit.ExactOnReachable
#print axioms APCILeanAudit.ExactOnReachable
#check @APCILeanAudit.exactCertificate_implies_fiberConstant
#print axioms APCILeanAudit.exactCertificate_implies_fiberConstant
#check @APCILeanAudit.exactOnReachable_implies_fiberConstant
#print axioms APCILeanAudit.exactOnReachable_implies_fiberConstant
#check @APCILeanAudit.fiberConstant_implies_exactOnReachable
#print axioms APCILeanAudit.fiberConstant_implies_exactOnReachable
#check @APCILeanAudit.exactOnReachable_iff_fiberConstant
#print axioms APCILeanAudit.exactOnReachable_iff_fiberConstant
#check @APCILeanAudit.exactCertificate_iff_fiberConstant_and_decoderSpaceNonempty
#print axioms APCILeanAudit.exactCertificate_iff_fiberConstant_and_decoderSpaceNonempty
#check @APCILeanAudit.exactCertificate_iff_fiberConstant
#print axioms APCILeanAudit.exactCertificate_iff_fiberConstant
#check @APCILeanAudit.leftInverse_implies_injective
#print axioms APCILeanAudit.leftInverse_implies_injective
#check @APCILeanAudit.collision_persists_under_postprocessing
#print axioms APCILeanAudit.collision_persists_under_postprocessing
#check @Experiments.BridgeFourSector.generatedCollision
#print axioms Experiments.BridgeFourSector.generatedCollision
#check @Experiments.BridgeFourSector.hiddenCollision
#print axioms Experiments.BridgeFourSector.hiddenCollision
#check @Experiments.BridgeFourSector.generatedVisible
#print axioms Experiments.BridgeFourSector.generatedVisible
#check @Experiments.BridgeFourSector.hidden
#print axioms Experiments.BridgeFourSector.hidden
#check @Experiments.BridgeFourSector.defect
#print axioms Experiments.BridgeFourSector.defect
#check @Experiments.BridgeFourSector.visible
#print axioms Experiments.BridgeFourSector.visible
#check @Experiments.BridgeFourSector.hiddenRawToDefect
#print axioms Experiments.BridgeFourSector.hiddenRawToDefect
#check @Experiments.BridgeFourSector.collisionToKernel
#print axioms Experiments.BridgeFourSector.collisionToKernel
#check @Experiments.BridgeFourSector.hiddenToDefect
#print axioms Experiments.BridgeFourSector.hiddenToDefect
#check @Experiments.BridgeFourSector.defectToVisible
#print axioms Experiments.BridgeFourSector.defectToVisible
#check @Experiments.BridgeFourSector.swappedVisibleEquiv
#print axioms Experiments.BridgeFourSector.swappedVisibleEquiv
#check @Experiments.BridgeFourSector.rightColumnToVisible
#print axioms Experiments.BridgeFourSector.rightColumnToVisible
#check @Experiments.BridgeFourSector.ker_hiddenRawToDefect
#print axioms Experiments.BridgeFourSector.ker_hiddenRawToDefect
#check @Experiments.BridgeFourSector.hiddenToDefect_injective
#print axioms Experiments.BridgeFourSector.hiddenToDefect_injective
#check @Experiments.BridgeFourSector.defectToVisible_surjective
#print axioms Experiments.BridgeFourSector.defectToVisible_surjective
#check @Experiments.BridgeFourSector.generated_row_exact
#print axioms Experiments.BridgeFourSector.generated_row_exact
#check @Experiments.BridgeFourSector.kernel_row_exact
#print axioms Experiments.BridgeFourSector.kernel_row_exact
#check @Experiments.BridgeFourSector.defect_column_exact
#print axioms Experiments.BridgeFourSector.defect_column_exact
#check @Experiments.BridgeFourSector.left_column_exact
#print axioms Experiments.BridgeFourSector.left_column_exact
#check @Experiments.BridgeFourSector.upper_left_square_commutes
#print axioms Experiments.BridgeFourSector.upper_left_square_commutes
#check @Experiments.BridgeFourSector.lower_left_square_commutes
#print axioms Experiments.BridgeFourSector.lower_left_square_commutes
#check @Experiments.BridgeFourSector.residual_exact
#print axioms Experiments.BridgeFourSector.residual_exact
#check @Experiments.BridgeFourSector.right_column_exact
#print axioms Experiments.BridgeFourSector.right_column_exact
#check @Experiments.BridgeFourSector.ker_readoutOnGenerated
#print axioms Experiments.BridgeFourSector.ker_readoutOnGenerated
#check @Experiments.BridgeFourSector.generatedVisibleEquivRange
#print axioms Experiments.BridgeFourSector.generatedVisibleEquivRange
#check @Experiments.BridgeFourSector.no_direct_complement_countercase
#print axioms Experiments.BridgeFourSector.no_direct_complement_countercase
#check @Experiments.BridgeReadout.generatedReadout
#print axioms Experiments.BridgeReadout.generatedReadout
#check @Experiments.BridgeReadout.rawReadoutToVisible
#print axioms Experiments.BridgeReadout.rawReadoutToVisible
#check @Experiments.BridgeReadout.residualReadout
#print axioms Experiments.BridgeReadout.residualReadout
#check @Experiments.BridgeReadout.rawReadoutToVisible_surjective
#print axioms Experiments.BridgeReadout.rawReadoutToVisible_surjective
#check @Experiments.BridgeReadout.ker_rawReadoutToVisible
#print axioms Experiments.BridgeReadout.ker_rawReadoutToVisible
#check @Experiments.BridgeReadout.visibleEquivReadout
#print axioms Experiments.BridgeReadout.visibleEquivReadout
#check @Experiments.BridgeReadout.visibleEquivReadout_apply_mk
#print axioms Experiments.BridgeReadout.visibleEquivReadout_apply_mk
#check @Experiments.BridgeReadout.residualReadout_compatibility
#print axioms Experiments.BridgeReadout.residualReadout_compatibility
#check @Experiments.BridgeReadout.generated_directions_required_countercase
#print axioms Experiments.BridgeReadout.generated_directions_required_countercase
#check @Experiments.BridgeReadout.generated_component_required_countercase
#print axioms Experiments.BridgeReadout.generated_component_required_countercase
#check @Experiments.BridgeRecovery.residualTarget
#print axioms Experiments.BridgeRecovery.residualTarget
#check @Experiments.BridgeRecovery.residualReadout_surjective
#print axioms Experiments.BridgeRecovery.residualReadout_surjective
#check @Experiments.BridgeRecovery.ker_residualReadout
#print axioms Experiments.BridgeRecovery.ker_residualReadout
#check @Experiments.BridgeRecovery.residualQuotientEquiv
#print axioms Experiments.BridgeRecovery.residualQuotientEquiv
#check @Experiments.BridgeRecovery.answerDecoder
#print axioms Experiments.BridgeRecovery.answerDecoder
#check @Experiments.BridgeRecovery.answerDecoder_comp_residualReadout
#print axioms Experiments.BridgeRecovery.answerDecoder_comp_residualReadout
#check @Experiments.BridgeRecovery.answer_decodable_iff
#print axioms Experiments.BridgeRecovery.answer_decodable_iff
#check @Experiments.BridgeRecovery.residual_identity_decoder_iff_injective
#print axioms Experiments.BridgeRecovery.residual_identity_decoder_iff_injective
#check @Experiments.BridgeRecovery.full_residual_identity_recovery_iff_hidden_subsingleton
#print axioms Experiments.BridgeRecovery.full_residual_identity_recovery_iff_hidden_subsingleton
#check @Experiments.BridgeRecovery.full_residual_identity_recovery_iff_kernel_le
#print axioms Experiments.BridgeRecovery.full_residual_identity_recovery_iff_kernel_le
#check @Experiments.BridgeRecovery.residual_identity_decoder_iff_kernel_le
#print axioms Experiments.BridgeRecovery.residual_identity_decoder_iff_kernel_le
#check @Experiments.BridgeRecovery.coarser_answer_decodable_without_identity_countercase
#print axioms Experiments.BridgeRecovery.coarser_answer_decodable_without_identity_countercase
#check @Experiments.BridgeDimension.generatedCollision_finrank
#print axioms Experiments.BridgeDimension.generatedCollision_finrank
#check @Experiments.BridgeDimension.hiddenCollision_finrank
#print axioms Experiments.BridgeDimension.hiddenCollision_finrank
#check @Experiments.BridgeDimension.generatedVisible_finrank_add_collision
#print axioms Experiments.BridgeDimension.generatedVisible_finrank_add_collision
#check @Experiments.BridgeDimension.hidden_finrank_add_collision
#print axioms Experiments.BridgeDimension.hidden_finrank_add_collision
#check @Experiments.BridgeDimension.visible_finrank_add_sup
#print axioms Experiments.BridgeDimension.visible_finrank_add_sup
#check @Experiments.BridgeDimension.bridge_four_sector_finrank
#print axioms Experiments.BridgeDimension.bridge_four_sector_finrank
#check @Experiments.BridgeDimension.four_sector_finrank_requires_finite_dimensional_countercase
#print axioms Experiments.BridgeDimension.four_sector_finrank_requires_finite_dimensional_countercase
#check @FrontLean.answer_sufficiency
#print axioms FrontLean.answer_sufficiency
#check @FrontLean.joint_equality
#print axioms FrontLean.joint_equality
#check @FrontLean.joint_sufficiency
#print axioms FrontLean.joint_sufficiency
#check @FrontLean.common_action_iff
#print axioms FrontLean.common_action_iff
#check @FrontLean.coordinate_bit_bound
#print axioms FrontLean.coordinate_bit_bound
#check @FrontLean.answer_does_not_recover_history
#print axioms FrontLean.answer_does_not_recover_history
#check @FrontLean.absent_reading_is_not_content
#print axioms FrontLean.absent_reading_is_not_content
#check @FrontLean.runWord
#print axioms FrontLean.runWord
#check @FrontLean.FutureEq
#print axioms FrontLean.FutureEq
#check @FrontLean.future_output_preservation
#print axioms FrontLean.future_output_preservation
#check @FrontLean.online_update_iff
#print axioms FrontLean.online_update_iff
#check @FrontLean.future_eq_is_right_congruence
#print axioms FrontLean.future_eq_is_right_congruence
#check @FrontLean.admitted_outputs_sufficiency
#print axioms FrontLean.admitted_outputs_sufficiency
#check @FrontLean.output_sufficient_without_online_update
#print axioms FrontLean.output_sufficient_without_online_update
#check @FrontLean.reuse_cheaper_iff
#print axioms FrontLean.reuse_cheaper_iff
#check @FrontLean.no_saving_when_reuse_is_costlier
#print axioms FrontLean.no_saving_when_reuse_is_costlier
#check @FrontLean.descending_rank_bounds_steps
#print axioms FrontLean.descending_rank_bounds_steps
#check @FrontLean.total_cost_bound
#print axioms FrontLean.total_cost_bound
#check @FrontLean.polynomial_accounting
#print axioms FrontLean.polynomial_accounting
#check @FrontLean.shared_diamond_cost
#print axioms FrontLean.shared_diamond_cost
#check @FrontLean.Valid
#print axioms FrontLean.Valid
#check @FrontLean.UsesRoot
#print axioms FrontLean.UsesRoot
#check @FrontLean.UsesRule
#print axioms FrontLean.UsesRule
#check @FrontLean.derivation_sound
#print axioms FrontLean.derivation_sound
#check @FrontLean.premise_substitution
#print axioms FrontLean.premise_substitution
#check @FrontLean.valid_under_unchanged_basis
#print axioms FrontLean.valid_under_unchanged_basis
#check @FrontLean.increasing_depth_no_cycle
#print axioms FrontLean.increasing_depth_no_cycle
#check @FrontLean.negative_core_transfer
#print axioms FrontLean.negative_core_transfer
#check @FrontLean.hornStep
#print axioms FrontLean.hornStep
#check @FrontLean.mem_hornStep
#print axioms FrontLean.mem_hornStep
#check @FrontLean.hornStep_inflationary
#print axioms FrontLean.hornStep_inflationary
#check @FrontLean.hornStep_monotone
#print axioms FrontLean.hornStep_monotone
#check @FrontLean.rounds
#print axioms FrontLean.rounds
#check @FrontLean.rounds_seed
#print axioms FrontLean.rounds_seed
#check @FrontLean.stable_round_persists
#print axioms FrontLean.stable_round_persists
#check @FrontLean.finite_stabilization
#print axioms FrontLean.finite_stabilization
#check @FrontLean.rounds_le_closed
#print axioms FrontLean.rounds_le_closed
#check @FrontLean.horn_least_closure
#print axioms FrontLean.horn_least_closure
#check @FrontLean.horn_rounds_sound
#print axioms FrontLean.horn_rounds_sound
#check @FrontLean.empty_seed_stays_empty
#print axioms FrontLean.empty_seed_stays_empty
#check @FrontLean.wake_decomposition
#print axioms FrontLean.wake_decomposition
#check @FrontLean.redundant_seed
#print axioms FrontLean.redundant_seed
#check @FrontLean.RecordedSupport
#print axioms FrontLean.RecordedSupport
#check @FrontLean.recorded_support_sound
#print axioms FrontLean.recorded_support_sound
#check @FrontLean.unchanged_alternative_survives
#print axioms FrontLean.unchanged_alternative_survives
#check @FrontLean.scratchRepair
#print axioms FrontLean.scratchRepair
#check @FrontLean.scratch_commit_iff
#print axioms FrontLean.scratch_commit_iff
#check @FrontLean.failed_scratch_keeps_original
#print axioms FrontLean.failed_scratch_keeps_original
#check @FrontLean.HistoryPrefix
#print axioms FrontLean.HistoryPrefix
#check @FrontLean.history_prefix_refl
#print axioms FrontLean.history_prefix_refl
#check @FrontLean.history_prefix_trans
#print axioms FrontLean.history_prefix_trans
#check @FrontLean.scratch_preserves_history
#print axioms FrontLean.scratch_preserves_history
#check @FrontLean.finite_history_preservation
#print axioms FrontLean.finite_history_preservation
#check @FrontLean.failed_secondary_condition_is_recorded
#print axioms FrontLean.failed_secondary_condition_is_recorded
#check @FrontLean.independent_answer_invalid_receipt
#print axioms FrontLean.independent_answer_invalid_receipt
#check @FrontLean.missing_conjunct_is_rejected
#print axioms FrontLean.missing_conjunct_is_rejected
#check @FrontLean.no_recorded_proof_is_not_negation
#print axioms FrontLean.no_recorded_proof_is_not_negation
#check @FrontLean.unchanged_does_not_require_mutation_grant
#print axioms FrontLean.unchanged_does_not_require_mutation_grant
#check @FrontLean.linear_factorization
#print axioms FrontLean.linear_factorization
#check @FrontLean.joint_kernel
#print axioms FrontLean.joint_kernel
#check @FrontLean.kernel_refinement
#print axioms FrontLean.kernel_refinement
#check @FrontLean.joint_residual_short_exact
#print axioms FrontLean.joint_residual_short_exact
#check @FrontLean.joint_visible_equiv
#print axioms FrontLean.joint_visible_equiv
#check @FrontLean.joint_sector_dimensions
#print axioms FrontLean.joint_sector_dimensions
#check @FrontLean.visibleRefinement
#print axioms FrontLean.visibleRefinement
#check @FrontLean.refinement_commutes
#print axioms FrontLean.refinement_commutes
#check @FrontLean.quotient_update_iff
#print axioms FrontLean.quotient_update_iff
#check @FrontLean.transported_return
#print axioms FrontLean.transported_return
#check @FrontLean.side_trace_decodable
#print axioms FrontLean.side_trace_decodable
#check @FrontLean.query_rank_le
#print axioms FrontLean.query_rank_le
#check @FrontLean.side_trace_rank_lower_bound
#print axioms FrontLean.side_trace_rank_lower_bound
#check @FrontLean.minimum_side_trace
#print axioms FrontLean.minimum_side_trace
#check @FrontLean.side_trace_capacity
#print axioms FrontLean.side_trace_capacity
#check @FrontLean.side_trace_capacity_injection
#print axioms FrontLean.side_trace_capacity_injection
#check @FrontLean.residual_query_criterion
#print axioms FrontLean.residual_query_criterion
#check @FrontLean.residual_debt_image
#print axioms FrontLean.residual_debt_image
#check @FrontLean.residual_side_trace_capacity
#print axioms FrontLean.residual_side_trace_capacity
#check @FrontLean.horizonKernel
#print axioms FrontLean.horizonKernel
#check @FrontLean.infiniteKernel
#print axioms FrontLean.infiniteKernel
#check @FrontLean.mem_horizon
#print axioms FrontLean.mem_horizon
#check @FrontLean.mem_infinite
#print axioms FrontLean.mem_infinite
#check @FrontLean.horizon_antitone
#print axioms FrontLean.horizon_antitone
#check @FrontLean.invariant_kernel_iff
#print axioms FrontLean.invariant_kernel_iff
#check @FrontLean.infinite_invariant
#print axioms FrontLean.infinite_invariant
#check @FrontLean.all_outputs_equal_iff
#print axioms FrontLean.all_outputs_equal_iff
#check @FrontLean.finite_horizon_closure
#print axioms FrontLean.finite_horizon_closure
#check @FrontLean.finite_subfamily_inside
#print axioms FrontLean.finite_subfamily_inside
#check @FrontLean.finite_readout_subfamily
#print axioms FrontLean.finite_readout_subfamily
#check @FrontLean.unlabelled
#print axioms FrontLean.unlabelled
#check @FrontLean.lost_labels_counterexample
#print axioms FrontLean.lost_labels_counterexample
#check @FrontLean.sat_does_not_transfer_to_strengthening
#print axioms FrontLean.sat_does_not_transfer_to_strengthening
#check @FrontLean.stale_premise_counterexample
#print axioms FrontLean.stale_premise_counterexample
#check @FrontLean.technically_valid_but_not_authorized
#print axioms FrontLean.technically_valid_but_not_authorized
#check @FrontLean.independent_baselines_lose_relation
#print axioms FrontLean.independent_baselines_lose_relation
#check @FrontLean.quotient_update_can_fail
#print axioms FrontLean.quotient_update_can_fail
#check @FrontLean.untransported_return_wrong
#print axioms FrontLean.untransported_return_wrong
