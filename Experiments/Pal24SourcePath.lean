import Mathlib.Data.List.Basic
/-! Bounded source-path replay realization for supplied identifiers, typed outcomes, and finite transitions. -/
namespace Experiments.Pal24SourcePath
inductive CheckResult where
  | yes
  | no (reason : String)
  | unknown (reason : String)
  deriving Repr, DecidableEq
structure PathRecord where
  sourceId : String
  channel : Nat
  taskId : String
  version : Nat
  eventCode : Nat
  eventId : Nat
  previous : Option Nat
  before : Nat
  value : Nat
  after : Nat
  evidence : CheckResult
  deriving Repr, DecidableEq
structure ChannelAdapter where
  suppliedSource : String
  inputChannel : Nat
  canonicalChannel : Nat
  version : Nat
  eventMap : List (Nat × Nat)
  deriving Repr, DecidableEq
structure ReplayContext where
  adapter : ChannelAdapter
  currentTask : String
  currentVersion : Nat
  currentChannel : Nat
  expectedEvents : List Nat
  initialState : Nat
  deriving Repr, DecidableEq

def knownStep (state value : Nat) : Nat := state + value
def adaptedEvent (a : ChannelAdapter) (code : Nat) : Option Nat :=
  (a.eventMap.find? (fun p => p.1 == code)).map Prod.snd
def contentCheck (r : PathRecord) : CheckResult :=
  if r.after = knownStep r.before r.value then .yes else .no "event content mismatch"
def associationCheck (a : ChannelAdapter) (r : PathRecord) : CheckResult :=
  if r.sourceId = a.suppliedSource ∧ r.channel = a.inputChannel ∧ r.version = a.version ∧
      adaptedEvent a r.eventCode = some r.eventId then .yes else .no "source/channel/version/event association mismatch"
def applicabilityCheck (c : ReplayContext) (r : PathRecord) : CheckResult :=
  if r.taskId = c.currentTask ∧ r.version = c.currentVersion ∧ c.adapter.canonicalChannel = c.currentChannel then .yes
  else .no "task/version/channel applicability mismatch"
def orderCheck (previous : Option Nat) (r : PathRecord) : CheckResult :=
  if r.previous = previous then .yes else .no "predecessor mismatch"
def transitionLinkCheck (expectedState : Nat) (r : PathRecord) : CheckResult :=
  if r.before = expectedState then .yes else .no "transition input state mismatch"
def admitted (checks : List CheckResult) : Bool := checks.all (· == .yes)
def recordChecks (c : ReplayContext) (previous : Option Nat) (expectedState : Nat) (r : PathRecord) : List CheckResult :=
  [orderCheck previous r, transitionLinkCheck expectedState r, contentCheck r,
    associationCheck c.adapter r, applicabilityCheck c r, r.evidence]
def historyChecksFrom (c : ReplayContext) (previous : Option Nat) (expectedState : Nat) :
    List PathRecord → List CheckResult
  | [] => []
  | r :: rs => recordChecks c previous expectedState r ++
      historyChecksFrom c (some r.eventId) r.after rs
def historyChecks (c : ReplayContext) (records : List PathRecord) : List CheckResult :=
  historyChecksFrom c none c.initialState records
def coverageCheck (c : ReplayContext) (records : List PathRecord) : CheckResult :=
  if records.map PathRecord.eventId = c.expectedEvents then .yes else .no "event coverage/order mismatch"
def fullAudit (c : ReplayContext) (records : List PathRecord) : List CheckResult :=
  historyChecks c records ++ [coverageCheck c records]
def replayStored (state : Nat) (records : List PathRecord) : Nat :=
  records.foldl (fun _ r => r.after) state

def checkedReplay (c : ReplayContext) (records : List PathRecord) : List CheckResult × CheckResult × Option Nat :=
  let checks := fullAudit c records
  if admitted checks then (checks, .yes, some (replayStored c.initialState records))
  else match checks.find? (· != .yes) with
       | some (.unknown reason) => (checks, .unknown reason, none)
       | some (.no reason) => (checks, .no reason, none)
       | _ => (checks, .no "no admission proof", none)
def runKnown : List Nat → Nat → Nat
  | [], state => state
  | value :: values, state => runKnown values (knownStep state value)
def transitionChain (state : Nat) : List PathRecord → Prop
  | [] => True
  | r :: rs => transitionLinkCheck state r = .yes ∧ contentCheck r = .yes ∧ transitionChain r.after rs
theorem content_chain_replay (state : Nat) (records : List PathRecord)
    (hchain : transitionChain state records) :
    replayStored state records = runKnown (records.map PathRecord.value) state := by
  induction records generalizing state with
  | nil => rfl
  | cons r rs ih =>
      simp only [transitionChain] at hchain
      rcases hchain with ⟨hlink, hcontent, htail⟩
      have hbefore : r.before = state := by
        simp [transitionLinkCheck] at hlink
        exact hlink
      have hafter : r.after = knownStep state r.value := by
        have hv : r.after = knownStep r.before r.value := by
          by_cases heq : r.after = knownStep r.before r.value
          · exact heq
          · simp [contentCheck, heq] at hcontent
        simpa [hbefore] using hv
      change replayStored r.after rs = runKnown (List.map PathRecord.value rs) (knownStep state r.value)
      rw [← hafter, ih r.after htail]

theorem history_yes_chain (c : ReplayContext) (previous : Option Nat) (expectedState : Nat)
    (records : List PathRecord)
    (hall : ∀ check, check ∈ historyChecksFrom c previous expectedState records → check = .yes) :
    transitionChain expectedState records := by
  induction records generalizing previous expectedState with
  | nil => simp [transitionChain]
  | cons r rs ih =>
      have hlink : transitionLinkCheck expectedState r = .yes := by
        apply hall
        simp [historyChecksFrom, recordChecks]
      have hcontent : contentCheck r = .yes := by
        apply hall
        simp [historyChecksFrom, recordChecks]
      have htail : transitionChain r.after rs := by
        apply ih (some r.eventId) r.after
        intro check hmem
        apply hall check
        simp [historyChecksFrom, List.mem_append, hmem]
      exact ⟨hlink, hcontent, htail⟩

theorem admitted_fullAudit_implies_transitionChain (c : ReplayContext) (records : List PathRecord)
    (hadmitted : admitted (fullAudit c records) = true) :
    transitionChain c.initialState records := by
  have hall : ∀ check, check ∈ fullAudit c records → check = .yes := by
    simpa [admitted] using hadmitted
  apply history_yes_chain c none c.initialState records
  intro check hmem
  apply hall check
  simp [fullAudit, historyChecks, List.mem_append, hmem]

theorem checkedReplay_success_matches_runKnown (c : ReplayContext) (records : List PathRecord)
    (output : Nat)
    (hresult : (checkedReplay c records).2.1 = .yes)
    (houtput : (checkedReplay c records).2.2 = some output) :
    output = runKnown (records.map PathRecord.value) c.initialState := by
  cases hadmitted : admitted (fullAudit c records) with
  | false =>
      cases hfind : (fullAudit c records).find? (· != .yes) with
      | none => simp [checkedReplay, hadmitted, hfind] at hresult
      | some result => cases result <;> simp [checkedReplay, hadmitted, hfind] at hresult
  | true =>
      have hchain := admitted_fullAudit_implies_transitionChain c records hadmitted
      have hout : output = replayStored c.initialState records := by
        simpa [checkedReplay, hadmitted] using houtput.symm
      calc
        output = replayStored c.initialState records := hout
        _ = runKnown (records.map PathRecord.value) c.initialState :=
          content_chain_replay c.initialState records hchain

def sampleAdapter : ChannelAdapter := ⟨"source-A", 11, 19, 4, [(5, 50), (6, 60)]⟩
def sampleContext : ReplayContext := ⟨sampleAdapter, "task-A", 4, 19, [50, 60], 0⟩
def sampleFirst : PathRecord := ⟨"source-A", 11, "task-A", 4, 5, 50, none, 0, 2, 2, .yes⟩
def sampleSecond : PathRecord := ⟨"source-A", 11, "task-A", 4, 6, 60, some 50, 2, 3, 5, .yes⟩
def sampleRecords : List PathRecord := [sampleFirst, sampleSecond]
theorem positive_history_admitted : admitted (fullAudit sampleContext sampleRecords) = true := by
  decide +kernel
theorem positive_history_replay :
    checkedReplay sampleContext sampleRecords = (fullAudit sampleContext sampleRecords, .yes, some 5) := by
  decide +kernel
def replacedSourceRecord : PathRecord := { sampleFirst with sourceId := "source-B" }
theorem unchanged_channel_replaced_source_rejected : associationCheck sampleAdapter replacedSourceRecord = .no "source/channel/version/event association mismatch" := by
  simp [associationCheck, adaptedEvent, replacedSourceRecord, sampleFirst, sampleAdapter]
def staleVersionRecord : PathRecord := { sampleFirst with version := 3 }
theorem stale_version_rejected : applicabilityCheck sampleContext staleVersionRecord = .no "task/version/channel applicability mismatch" := by
  simp [applicabilityCheck, staleVersionRecord, sampleFirst, sampleContext, sampleAdapter]
theorem reordered_history_rejected : coverageCheck sampleContext sampleRecords.reverse = .no "event coverage/order mismatch" := by
  simp [coverageCheck, sampleRecords, sampleFirst, sampleSecond, sampleContext, sampleAdapter]
theorem missing_history_rejected : coverageCheck sampleContext [sampleFirst] = .no "event coverage/order mismatch" := by
  simp [coverageCheck, sampleFirst, sampleContext, sampleAdapter]
def alteredValueRecord : PathRecord := { sampleFirst with value := 3 }
theorem altered_value_rejected : contentCheck alteredValueRecord = .no "event content mismatch" := by
  simp [contentCheck, alteredValueRecord, sampleFirst, knownStep]
def wrongEventBindingRecord : PathRecord := { sampleFirst with eventId := 60 }
theorem consistent_content_wrong_event_binding : contentCheck wrongEventBindingRecord = .yes ∧ associationCheck sampleAdapter wrongEventBindingRecord = .no "source/channel/version/event association mismatch" := by
  simp [contentCheck, associationCheck, adaptedEvent, wrongEventBindingRecord, sampleFirst, sampleAdapter, knownStep]
def wrongTaskRecord : PathRecord := { sampleFirst with taskId := "task-B" }
theorem task_mismatch_rejected : applicabilityCheck sampleContext wrongTaskRecord = .no "task/version/channel applicability mismatch" := by
  simp [applicabilityCheck, wrongTaskRecord, sampleFirst, sampleContext, sampleAdapter]
def unknownEvidenceRecord : PathRecord := { sampleFirst with evidence := .unknown "signature check unavailable" }
theorem unknown_is_retained_and_fails_closed : (recordChecks sampleContext none 0 unknownEvidenceRecord).getLast? = some (.unknown "signature check unavailable") ∧ admitted (recordChecks sampleContext none 0 unknownEvidenceRecord) = false := by
  simp [recordChecks, orderCheck, contentCheck, associationCheck, adaptedEvent, applicabilityCheck, unknownEvidenceRecord, sampleFirst, sampleAdapter, sampleContext, knownStep, admitted]
theorem unknown_evidence_declines_with_reason :
    (checkedReplay sampleContext [unknownEvidenceRecord]).2.1 = .unknown "signature check unavailable" ∧
      (checkedReplay sampleContext [unknownEvidenceRecord]).2.2 = none ∧
      (checkedReplay sampleContext [unknownEvidenceRecord]).1.contains (.unknown "signature check unavailable") := by
  decide +kernel
theorem unknown_not_equal_no : CheckResult.unknown "x" ≠ CheckResult.no "x" := by decide
theorem unknown_not_equal_yes : CheckResult.unknown "x" ≠ CheckResult.yes := by decide

end Experiments.Pal24SourcePath

