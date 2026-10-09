import Experiments.Pal24SourcePath

namespace Experiments.Pal24SourcePath

set_option pp.fullNames true

#check @Experiments.Pal24SourcePath.CheckResult
#print axioms Experiments.Pal24SourcePath.CheckResult

#check @Experiments.Pal24SourcePath.PathRecord
#print axioms Experiments.Pal24SourcePath.PathRecord

#check @Experiments.Pal24SourcePath.ChannelAdapter
#print axioms Experiments.Pal24SourcePath.ChannelAdapter

#check @Experiments.Pal24SourcePath.ReplayContext
#print axioms Experiments.Pal24SourcePath.ReplayContext

#check @Experiments.Pal24SourcePath.knownStep
#print axioms Experiments.Pal24SourcePath.knownStep

#check @Experiments.Pal24SourcePath.adaptedEvent
#print axioms Experiments.Pal24SourcePath.adaptedEvent

#check @Experiments.Pal24SourcePath.contentCheck
#print axioms Experiments.Pal24SourcePath.contentCheck

#check @Experiments.Pal24SourcePath.associationCheck
#print axioms Experiments.Pal24SourcePath.associationCheck

#check @Experiments.Pal24SourcePath.applicabilityCheck
#print axioms Experiments.Pal24SourcePath.applicabilityCheck

#check @Experiments.Pal24SourcePath.orderCheck
#print axioms Experiments.Pal24SourcePath.orderCheck

#check @Experiments.Pal24SourcePath.transitionLinkCheck
#print axioms Experiments.Pal24SourcePath.transitionLinkCheck

#check @Experiments.Pal24SourcePath.admitted
#print axioms Experiments.Pal24SourcePath.admitted

#check @Experiments.Pal24SourcePath.recordChecks
#print axioms Experiments.Pal24SourcePath.recordChecks

#check @Experiments.Pal24SourcePath.historyChecksFrom
#print axioms Experiments.Pal24SourcePath.historyChecksFrom

#check @Experiments.Pal24SourcePath.historyChecks
#print axioms Experiments.Pal24SourcePath.historyChecks

#check @Experiments.Pal24SourcePath.coverageCheck
#print axioms Experiments.Pal24SourcePath.coverageCheck

#check @Experiments.Pal24SourcePath.fullAudit
#print axioms Experiments.Pal24SourcePath.fullAudit

#check @Experiments.Pal24SourcePath.replayStored
#print axioms Experiments.Pal24SourcePath.replayStored

#check @Experiments.Pal24SourcePath.checkedReplay
#print axioms Experiments.Pal24SourcePath.checkedReplay

#check @Experiments.Pal24SourcePath.runKnown
#print axioms Experiments.Pal24SourcePath.runKnown

#check @Experiments.Pal24SourcePath.transitionChain
#print axioms Experiments.Pal24SourcePath.transitionChain

#check @Experiments.Pal24SourcePath.content_chain_replay
#print axioms Experiments.Pal24SourcePath.content_chain_replay

#check @Experiments.Pal24SourcePath.history_yes_chain
#print axioms Experiments.Pal24SourcePath.history_yes_chain

#check @Experiments.Pal24SourcePath.admitted_fullAudit_implies_transitionChain
#print axioms Experiments.Pal24SourcePath.admitted_fullAudit_implies_transitionChain

#check @Experiments.Pal24SourcePath.checkedReplay_success_matches_runKnown
#print axioms Experiments.Pal24SourcePath.checkedReplay_success_matches_runKnown

#check @Experiments.Pal24SourcePath.sampleAdapter
#print axioms Experiments.Pal24SourcePath.sampleAdapter

#check @Experiments.Pal24SourcePath.sampleContext
#print axioms Experiments.Pal24SourcePath.sampleContext

#check @Experiments.Pal24SourcePath.sampleFirst
#print axioms Experiments.Pal24SourcePath.sampleFirst

#check @Experiments.Pal24SourcePath.sampleSecond
#print axioms Experiments.Pal24SourcePath.sampleSecond

#check @Experiments.Pal24SourcePath.sampleRecords
#print axioms Experiments.Pal24SourcePath.sampleRecords

#check @Experiments.Pal24SourcePath.positive_history_admitted
#print axioms Experiments.Pal24SourcePath.positive_history_admitted

#check @Experiments.Pal24SourcePath.positive_history_replay
#print axioms Experiments.Pal24SourcePath.positive_history_replay

#check @Experiments.Pal24SourcePath.replacedSourceRecord
#print axioms Experiments.Pal24SourcePath.replacedSourceRecord

#check @Experiments.Pal24SourcePath.unchanged_channel_replaced_source_rejected
#print axioms Experiments.Pal24SourcePath.unchanged_channel_replaced_source_rejected

#check @Experiments.Pal24SourcePath.staleVersionRecord
#print axioms Experiments.Pal24SourcePath.staleVersionRecord

#check @Experiments.Pal24SourcePath.stale_version_rejected
#print axioms Experiments.Pal24SourcePath.stale_version_rejected

#check @Experiments.Pal24SourcePath.reordered_history_rejected
#print axioms Experiments.Pal24SourcePath.reordered_history_rejected

#check @Experiments.Pal24SourcePath.missing_history_rejected
#print axioms Experiments.Pal24SourcePath.missing_history_rejected

#check @Experiments.Pal24SourcePath.alteredValueRecord
#print axioms Experiments.Pal24SourcePath.alteredValueRecord

#check @Experiments.Pal24SourcePath.altered_value_rejected
#print axioms Experiments.Pal24SourcePath.altered_value_rejected

#check @Experiments.Pal24SourcePath.wrongEventBindingRecord
#print axioms Experiments.Pal24SourcePath.wrongEventBindingRecord

#check @Experiments.Pal24SourcePath.consistent_content_wrong_event_binding
#print axioms Experiments.Pal24SourcePath.consistent_content_wrong_event_binding

#check @Experiments.Pal24SourcePath.wrongTaskRecord
#print axioms Experiments.Pal24SourcePath.wrongTaskRecord

#check @Experiments.Pal24SourcePath.task_mismatch_rejected
#print axioms Experiments.Pal24SourcePath.task_mismatch_rejected

#check @Experiments.Pal24SourcePath.unknownEvidenceRecord
#print axioms Experiments.Pal24SourcePath.unknownEvidenceRecord

#check @Experiments.Pal24SourcePath.unknown_is_retained_and_fails_closed
#print axioms Experiments.Pal24SourcePath.unknown_is_retained_and_fails_closed

#check @Experiments.Pal24SourcePath.unknown_evidence_declines_with_reason
#print axioms Experiments.Pal24SourcePath.unknown_evidence_declines_with_reason

#check @Experiments.Pal24SourcePath.unknown_not_equal_no
#print axioms Experiments.Pal24SourcePath.unknown_not_equal_no

#check @Experiments.Pal24SourcePath.unknown_not_equal_yes
#print axioms Experiments.Pal24SourcePath.unknown_not_equal_yes

end Experiments.Pal24SourcePath
