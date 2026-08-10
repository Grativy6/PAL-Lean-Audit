import PAL.AttackRun0001

/-!
# Attack Run 0003: published controlling PAL v2.1 routes

Controlling release: published PAL v2.1, DOI 10.5281/zenodo.21864767.

This module is a bounded realization of SC-19.1--SC-19.8, D16--D23,
T33--T40, M-A0-SCOPED-FIRST, M-A0-CUT, M-SOURCE-FIBER, M-A2-HISTORY,
M-A15-CHECK, and M-INQUIRY-APPEND. Unresolved possibility remains wholly
metalinguistic: no object-language type, value, constructor, or identifier
represents it here.

All stronger conclusions are parameterized by supplied evidence. The module
does not close O04, O25, or the global first-occurrence debt.
-/

namespace PAL.AttackRun0003

open PAL.AttackRun0001

universe u v

structure AccountId where value : Nat deriving DecidableEq, Repr
structure CutIdentity where value : Nat deriving DecidableEq, Repr
structure ScopeId where value : Nat deriving DecidableEq, Repr
structure BoundaryId where value : Nat deriving DecidableEq, Repr
structure WitnessProvenance where value : Nat deriving DecidableEq, Repr
structure CutCost where value : Nat deriving DecidableEq, Repr
structure AdmissionTrace where value : Nat deriving DecidableEq, Repr
structure AuthorityCeiling where value : Nat deriving DecidableEq, Repr
structure ResidualRecord where value : Nat deriving DecidableEq, Repr
structure ReopeningCondition where value : Nat deriving DecidableEq, Repr

/-- A cut admission keeps its witness, indexed cost, authority, residue, and reopening data typed. -/
structure AccountCutReceipt (CutWitness : Type u) where
  account : AccountId
  admissionOrder : Nat
  cutIdentity : CutIdentity
  scope : ScopeId
  boundary : BoundaryId
  suppliedWitness : CutWitness
  provenance : WitnessProvenance
  cutIndexedCost : CutCost
  carriedAdmissionTrace : AdmissionTrace
  authorityCeiling : AuthorityCeiling
  priorAuthority : AuthoritySnapshot
  residual : ResidualRecord
  reopening : ReopeningCondition
  deriving DecidableEq, Repr

def admitCut (account : AccountId) (admissionOrder : Nat)
    (cutIdentity : CutIdentity) (scope : ScopeId) (boundary : BoundaryId)
    (witness : CutWitness) (provenance : WitnessProvenance) (cost : CutCost)
    (trace : AdmissionTrace) (ceiling : AuthorityCeiling)
    (priorAuthority : AuthoritySnapshot) (residual : ResidualRecord)
    (reopening : ReopeningCondition) : AccountCutReceipt CutWitness where
  account := account
  admissionOrder := admissionOrder
  cutIdentity := cutIdentity
  scope := scope
  boundary := boundary
  suppliedWitness := witness
  provenance := provenance
  cutIndexedCost := cost
  carriedAdmissionTrace := trace
  authorityCeiling := ceiling
  priorAuthority := priorAuthority
  residual := residual
  reopening := reopening

def baseAuthority : AuthoritySnapshot where
  identityId := 1
  evidenceId := 2
  consentRecorded := false
  standingRecorded := false
  uncertaintyId := 3
  authorityId := 4

def baseCost : CutCost := { value := 7 }

def baseCutReceipt : AccountCutReceipt Unit :=
  admitCut { value := 10 } 0 { value := 20 } { value := 30 } { value := 40 }
    () { value := 50 } baseCost { value := 60 } { value := 70 }
    baseAuthority { value := 80 } { value := 90 }

/-- A finite comparison scope and its supplied precedence decision. -/
structure ScopedComparison (Event : Type u) where
  scope : List Event
  precedes : Event -> Event -> Bool

def IsFirstIn {Event : Type u} (comparison : ScopedComparison Event)
    (candidate : Event) : Prop :=
  candidate ∈ comparison.scope ∧
    ∀ event ∈ comparison.scope, comparison.precedes event candidate = false

inductive ScopedEvent where
  | priorOutside
  | admitted
  deriving DecidableEq, Repr

def scopedPrecedes : ScopedEvent -> ScopedEvent -> Bool
  | .priorOutside, .admitted => true
  | _, _ => false

def accountScope : ScopedComparison ScopedEvent where
  scope := [.admitted]
  precedes := scopedPrecedes

def expandedScope : ScopedComparison ScopedEvent where
  scope := [.priorOutside, .admitted]
  precedes := scopedPrecedes

/-- A stronger primacy receipt must retain the supplied comparison evidence. -/
structure PrimacyReceipt (Event : Type u) (ComparisonWitness : Type v) where
  comparison : ScopedComparison Event
  candidate : Event
  suppliedComparisonWitness : ComparisonWitness
  firstInDeclaredScope : IsFirstIn comparison candidate
  authorityCeiling : AuthorityCeiling

/--
Route: SC-19.1 / D16 / T33 / M-A0-SCOPED-FIRST.
Hypotheses: the declared account scope and precedence table above.
Positive claim: the admitted event is first inside that finite account scope.
Overclaim not established: global, ontological, or source-absolute firstness.
Authority ceiling: this result classifies only the supplied comparison model.
Retained evidence: the scope membership and every checked predecessor edge.
Reopening burden: enlarge the scope or supply a conflicting predecessor.
-/
theorem scopedAccountFirstRealization : IsFirstIn accountScope .admitted := by
  simp [IsFirstIn, accountScope, scopedPrecedes]

/--
Route: SC-19.1 / D16 / T33 / M-A0-SCOPED-FIRST.
Hypotheses: the two explicit finite scopes and one supplied predecessor edge.
Positive claim: local firstness and failure of expanded-scope firstness coexist.
Overclaim not established: that every larger scope contains such a predecessor.
Authority ceiling: a bounded countermodel refutes only the generic implication.
Retained evidence: both event lists and the full precedence decision remain inspectable.
Reopening burden: supply a scope bridge proving local-to-global exhaustiveness.
-/
theorem localFirstGlobalFirstCountermodel :
    IsFirstIn accountScope .admitted ∧ Not (IsFirstIn expandedScope .admitted) := by
  simp [IsFirstIn, accountScope, expandedScope, scopedPrecedes]

/--
Route: SC-19.4 / D19 / T36 / M-A0-SCOPED-FIRST.
Hypotheses: a comparison witness and an explicit proof of firstness in its scope.
Positive claim: those supplied materials construct a bounded primacy receipt.
Overclaim not established: the evidence is not manufactured and its scope is not enlarged.
Authority ceiling: the receipt says no more than its indexed comparison.
Retained evidence: witness, scope, candidate, proof, and ceiling stay together.
Reopening burden: challenge the evidence or provide a wider comparison scope.
-/
theorem strongerPrimacyAssumptionBound {Event : Type u} {ComparisonWitness : Type v}
    (comparison : ScopedComparison Event) (candidate : Event)
    (witness : ComparisonWitness) (evidence : IsFirstIn comparison candidate)
    (ceiling : AuthorityCeiling) :
    ∃ receipt : PrimacyReceipt Event ComparisonWitness,
      receipt.comparison = comparison ∧ receipt.candidate = candidate := by
  exact ⟨⟨comparison, candidate, witness, evidence, ceiling⟩, rfl, rfl⟩

/--
Route: SC-19.2 / D17 / T34 / M-A0-CUT.
Hypotheses: separately supplied account, cut, scope, witness, cost, trace, and limits.
Positive claim: admission preserves the typed cost and its distinct supporting fields.
Overclaim not established: cost is not cause, truth, energy, permission, consent, standing, or authority.
Authority ceiling: construction records ledger admission only.
Retained evidence: witness provenance, prior authority, residue, and reopening condition.
Reopening burden: dispute any supplied field or the account-relative admission rule.
-/
theorem typedCostBearingAdmission (account : AccountId) (cutIdentity : CutIdentity)
    (scope : ScopeId) (boundary : BoundaryId) (witness : CutWitness)
    (provenance : WitnessProvenance) (cost : CutCost) (trace : AdmissionTrace)
    (ceiling : AuthorityCeiling) (prior : AuthoritySnapshot)
    (residual : ResidualRecord) (reopening : ReopeningCondition) :
    let receipt := admitCut account 0 cutIdentity scope boundary witness provenance
      cost trace ceiling prior residual reopening
    receipt.cutIndexedCost = cost ∧ receipt.carriedAdmissionTrace = trace ∧
      receipt.priorAuthority = prior := by
  simp [admitCut]

inductive ClaimKind where
  | causalSource
  | truth
  | energy
  | permission
  | consent
  | standing
  | authority
  deriving DecidableEq, Repr

/-- A claim receipt requires evidence separate from a cut's typed cost. -/
structure ClaimReceipt (kind : ClaimKind) (ClaimWitness : Type u) where
  witness : ClaimWitness
  claimId : Nat

/--
Route: SC-19.2 / D17 / T34 / M-A0-CUT.
Hypotheses: the inhabited base cut with positive typed cost and an empty claim-witness type.
Positive claim: all seven stronger claim kinds still lack receipts in this model.
Overclaim not established: no substantive claim kind is declared impossible in every model.
Authority ceiling: the countermodel separates ledger cost from seven named promotions only.
Retained evidence: the positive cost and exhaustive finite claim-kind index are preserved.
Reopening burden: supply an independent witness for the particular promoted claim.
-/
theorem costCannotSupplyClaimReceipts :
    0 < baseCutReceipt.cutIndexedCost.value ∧
      ∀ kind : ClaimKind, IsEmpty (ClaimReceipt kind NoWitness) := by
  constructor
  · decide
  · intro kind
    exact ⟨fun receipt => nomatch receipt.witness⟩

/-- A2 occurrence keeps an explicitly linked, scoped, prefix-protected A1/A2 history. -/
structure OccurrenceRecord (CutWitness : Type u) (A1Witness : Type v)
    (A2Witness : Type v) where
  cut : AccountCutReceipt CutWitness
  a1ReadableWitness : A1Witness
  a1ReadableCriterion : A1Witness -> Prop
  a1IsReadable : a1ReadableCriterion a1ReadableWitness
  a1ReceiptId : Nat
  a2RecoveryWitness : A2Witness
  a2RecoveryCriterion : A2Witness -> A1Witness -> Prop
  a2RecoversA1Witness : a2RecoveryCriterion a2RecoveryWitness a1ReadableWitness
  a2RecoveryId : Nat
  a2RecoveredA1Id : Nat
  a2TargetsA1 : a2RecoveredA1Id = a1ReceiptId
  a1PrecedesA2 : a1ReceiptId ≤ a2RecoveryId
  occurrenceId : Nat
  occurrenceScope : ScopeId
  scopeMatchesCut : occurrenceScope = cut.scope
  priorHistory : List Nat
  recoverableHistory : List Nat
  preservesPriorHistory : List.IsPrefix priorHistory recoverableHistory
  storesA1Receipt : a1ReceiptId ∈ recoverableHistory
  storesA2Recovery : a2RecoveryId ∈ recoverableHistory
  storesOccurrence : occurrenceId ∈ recoverableHistory

def buildOccurrence (cut : AccountCutReceipt CutWitness) (a1 : A1Witness)
    (a1Criterion : A1Witness -> Prop) (a1Valid : a1Criterion a1)
    (a1ReceiptId : Nat) (a2 : A2Witness)
    (a2Criterion : A2Witness -> A1Witness -> Prop) (a2Valid : a2Criterion a2 a1)
    (a2RecoveryId a2RecoveredA1Id : Nat)
    (targetsA1 : a2RecoveredA1Id = a1ReceiptId)
    (ordered : a1ReceiptId ≤ a2RecoveryId) (occurrenceId : Nat)
    (scope : ScopeId) (scopeMatches : scope = cut.scope)
    (priorHistory history : List Nat) (protectedPrefix : List.IsPrefix priorHistory history)
    (storesA1 : a1ReceiptId ∈ history) (storesA2 : a2RecoveryId ∈ history)
    (storesOccurrence : occurrenceId ∈ history) :
    OccurrenceRecord CutWitness A1Witness A2Witness where
  cut := cut
  a1ReadableWitness := a1
  a1ReadableCriterion := a1Criterion
  a1IsReadable := a1Valid
  a1ReceiptId := a1ReceiptId
  a2RecoveryWitness := a2
  a2RecoveryCriterion := a2Criterion
  a2RecoversA1Witness := a2Valid
  a2RecoveryId := a2RecoveryId
  a2RecoveredA1Id := a2RecoveredA1Id
  a2TargetsA1 := targetsA1
  a1PrecedesA2 := ordered
  occurrenceId := occurrenceId
  occurrenceScope := scope
  scopeMatchesCut := scopeMatches
  priorHistory := priorHistory
  recoverableHistory := history
  preservesPriorHistory := protectedPrefix
  storesA1Receipt := storesA1
  storesA2Recovery := storesA2
  storesOccurrence := storesOccurrence

/--
Route: SC-19.3 / D18 / T35 / M-A2-HISTORY.
Hypotheses: an admitted A0 receipt; declared A1 readability and A2-to-A1 recovery
predicates with proofs; linked ordered ids; matching scope; and protected history proofs.
Positive claim: the valid staged A1-to-A2 lineage constructs a scoped recoverable occurrence.
Overclaim not established: construction does not establish firstness or ultimate source.
Authority ceiling: the result is one supplied, account-relative occurrence realization.
Retained evidence: the cut, stage witnesses and ids, recovery target, scope, and protected history.
Reopening burden: challenge either stage witness or append later recoverable history.
-/
theorem occurrenceRecordFromSuppliedA1A2 (cut : AccountCutReceipt CutWitness)
    (a1 : A1Witness) (a1Criterion : A1Witness -> Prop)
    (a1Valid : a1Criterion a1) (a1ReceiptId : Nat) (a2 : A2Witness)
    (a2Criterion : A2Witness -> A1Witness -> Prop) (a2Valid : a2Criterion a2 a1)
    (a2RecoveryId a2RecoveredA1Id : Nat)
    (targetsA1 : a2RecoveredA1Id = a1ReceiptId)
    (ordered : a1ReceiptId ≤ a2RecoveryId) (occurrenceId : Nat)
    (scope : ScopeId) (scopeMatches : scope = cut.scope)
    (priorHistory history : List Nat) (protectedPrefix : List.IsPrefix priorHistory history)
    (storesA1 : a1ReceiptId ∈ history) (storesA2 : a2RecoveryId ∈ history)
    (storesOccurrence : occurrenceId ∈ history) :
    ∃ occurrence : OccurrenceRecord CutWitness A1Witness A2Witness,
      occurrence.cut = cut ∧ occurrence.a1ReadableWitness = a1 ∧
        occurrence.a2RecoveryWitness = a2 ∧ occurrence.occurrenceScope = scope ∧
        List.IsPrefix priorHistory occurrence.recoverableHistory := by
  exact ⟨buildOccurrence cut a1 a1Criterion a1Valid a1ReceiptId a2 a2Criterion
    a2Valid a2RecoveryId a2RecoveredA1Id targetsA1 ordered occurrenceId scope
    scopeMatches priorHistory history protectedPrefix storesA1 storesA2 storesOccurrence,
    rfl, rfl, rfl, rfl, protectedPrefix⟩

/-- Scoped A15 closure is a later, separately witnessed receipt. -/
structure ScopedClosureReceipt (CutWitness : Type u) (A1Witness : Type v)
    (A2Witness : Type v) (A15Witness : Type u) where
  occurrence : OccurrenceRecord CutWitness A1Witness A2Witness
  a15Witness : A15Witness
  closureScope : ScopeId
  retainedOccurrenceId : Nat
  retainsOccurrence : retainedOccurrenceId = occurrence.occurrenceId
  reopening : ReopeningCondition

/--
Route: SC-19.3 / D18 / T35 / M-A2-HISTORY.
Hypotheses: an admitted cut but an empty A1 type, or an empty A2 type.
Positive claim: either missing stage blocks the staged occurrence record.
Overclaim not established: the theorem does not deny that supplied A1 and A2 witnesses can exist.
Authority ceiling: this is dependency typing, not a global first-occurrence result.
Retained evidence: the A0, A1, and A2 addresses remain structurally distinct.
Reopening burden: provide both separately sourced stage witnesses.
-/
theorem occurrenceRequiresA1A2Witnesses :
    IsEmpty (OccurrenceRecord Unit NoWitness Unit) ∧
      IsEmpty (OccurrenceRecord Unit Unit NoWitness) := by
  constructor
  · exact ⟨fun receipt => nomatch receipt.a1ReadableWitness⟩
  · exact ⟨fun receipt => nomatch receipt.a2RecoveryWitness⟩

/--
Route: SC-19.3 / D18 / T35 / M-A15-CHECK.
Hypotheses: an occurrence record and an empty A15 closure-witness type.
Positive claim: occurrence alone cannot construct scoped closure.
Overclaim not established: no claim about ultimate or globally exhaustive closure is made.
Authority ceiling: only CLOSED_IN_SCOPE would be licensed by a supplied A15 witness.
Retained evidence: occurrence history and reopening data are not rewritten.
Reopening burden: supply a distinct closure witness and declared scope.
-/
theorem a15RequiredSeparatelyForScopedClosure
    (_occurrence : OccurrenceRecord CutWitness A1Witness A2Witness) :
    IsEmpty (ScopedClosureReceipt CutWitness A1Witness A2Witness NoWitness) :=
  ⟨fun receipt => nomatch receipt.a15Witness⟩

/--
Route: SC-19.3 / D18 / T35 / M-A0-CUT and M-A2-HISTORY.
Hypotheses: the concrete inhabited A0 receipt and empty later-stage witness types.
Positive claim: a cut can be admitted while no A1/A2 occurrence record is constructible.
Overclaim not established: this model does not decide O04, O25, or ultimate source primacy.
Authority ceiling: the countermodel refutes only an A0-to-occurrence implication.
Retained evidence: the complete typed cut receipt remains available.
Reopening burden: append independently witnessed A1 and A2 receipts.
-/
theorem a0OnlyCountermodel :
    Nonempty (AccountCutReceipt Unit) ∧
      IsEmpty (OccurrenceRecord Unit NoWitness NoWitness) := by
  constructor
  · exact ⟨baseCutReceipt⟩
  · exact ⟨fun receipt => nomatch receipt.a1ReadableWitness⟩

def Occurred (active recoverable : Nat -> Prop) (time : Nat) : Prop :=
  ∃ earlier, earlier ≤ time ∧ active earlier ∧ recoverable earlier

/--
Route: SC-19.3 / D18 / T35 / M-A2-HISTORY.
Hypotheses: an earlier recoverable occurrence and an ordered later observation time.
Positive claim: the existential history fact persists at the later time.
Overclaim not established: persistence does not imply continuing activity or source primacy.
Authority ceiling: this result concerns the bounded history predicate only.
Retained evidence: the same earlier time, activity fact, and recovery fact are reused.
Reopening burden: challenge recoverability or the supplied time order.
-/
theorem occurrenceHistoryMonotone {active recoverable : Nat -> Prop} {time later : Nat}
    (history : Occurred active recoverable time) (ordered : time ≤ later) :
    Occurred active recoverable later := by
  rcases history with ⟨earlier, before, activeThen, recoverableThen⟩
  exact ⟨earlier, Nat.le_trans before ordered, activeThen, recoverableThen⟩

def pulseActive (time : Nat) : Prop := time = 0
def pulseRecoverable (time : Nat) : Prop := time = 0

/--
Route: SC-19.3 / D18 / T35 / M-A2-HISTORY.
Hypotheses: the explicit one-step pulse model with a recoverable time-zero trace.
Positive claim: occurrence history can remain true after current activity becomes false.
Overclaim not established: the example proves neither immortality nor infinite storage.
Authority ceiling: it is a two-time bounded countermodel to history-equals-activity.
Retained evidence: the time-zero witness remains the recovery basis.
Reopening burden: require a semantics that identifies occurrence with current activity.
-/
theorem historyOutlastsActivityCountermodel :
    Occurred pulseActive pulseRecoverable 1 ∧ Not (pulseActive 1) := by
  constructor
  · exact ⟨0, by decide, rfl, rfl⟩
  · simp [pulseActive]

structure Question where
  questionId : Nat
  scope : ScopeId
  deriving DecidableEq, Repr

/-- An inquiry append retains independent event and cost witnesses plus protected prior fields. -/
structure InquiryEventReceipt (InquiryWitness : Type u) (InquiryCostWitness : Type v) where
  eventId : Nat
  question : Question
  suppliedInquiryWitness : InquiryWitness
  suppliedCostWitness : InquiryCostWitness
  witnessProvenance : WitnessProvenance
  inquiryCost : CutCost
  linkedParent : Option Nat
  authorityCeiling : AuthorityCeiling
  carriedTrace : AdmissionTrace
  authoritySnapshot : AuthoritySnapshot
  residual : ResidualRecord
  reopening : ReopeningCondition
  retainedPriorIds : List Nat

def admitInquiry (eventId : Nat) (question : Question) (witness : InquiryWitness)
    (costWitness : InquiryCostWitness) (provenance : WitnessProvenance)
    (cost : CutCost) (parent : Option Nat) (ceiling : AuthorityCeiling)
    (trace : AdmissionTrace) (authority : AuthoritySnapshot)
    (residual : ResidualRecord) (reopening : ReopeningCondition)
    (retained : List Nat) : InquiryEventReceipt InquiryWitness InquiryCostWitness where
  eventId := eventId
  question := question
  suppliedInquiryWitness := witness
  suppliedCostWitness := costWitness
  witnessProvenance := provenance
  inquiryCost := cost
  linkedParent := parent
  authorityCeiling := ceiling
  carriedTrace := trace
  authoritySnapshot := authority
  residual := residual
  reopening := reopening
  retainedPriorIds := retained

/--
Route: SC-19.5 / D20 / T37 / M-INQUIRY-APPEND.
Hypotheses: a question; independent event and cost witnesses; and complete protected metadata.
Positive claim: those inputs construct a present inquiry receipt retaining both witnesses.
Overclaim not established: asking the question does not manufacture its witness or answer.
Authority ceiling: admission records inquiry only, not truth, permission, or authorization.
Retained evidence: provenance, cost, trace, authority, residual, reopening, link, and prior ids.
Reopening burden: challenge the witness basis or append a linked later inquiry.
-/
theorem inquiryReceiptFromSuppliedWitness (question : Question)
    (witness : InquiryWitness) (costWitness : InquiryCostWitness)
    (provenance : WitnessProvenance) (cost : CutCost) (ceiling : AuthorityCeiling)
    (trace : AdmissionTrace) (authority : AuthoritySnapshot)
    (residual : ResidualRecord) (reopening : ReopeningCondition) :
    ∃ receipt : InquiryEventReceipt InquiryWitness InquiryCostWitness,
      receipt.suppliedInquiryWitness = witness ∧
        receipt.suppliedCostWitness = costWitness ∧ receipt.inquiryCost = cost := by
  exact ⟨admitInquiry 1 question witness costWitness provenance cost none ceiling trace
    authority residual reopening [], rfl, rfl, rfl⟩

/--
Route: SC-19.5 and SC-19.7 / D20 and D22 / T37 and T39 / M-INQUIRY-APPEND.
Hypotheses: an ordinary question and an empty external inquiry-event witness type.
Positive claim: the question alone cannot self-fill the event witness required by any inquiry receipt.
Overclaim not established: present or further inquiry remains permitted with an independent witness.
Authority ceiling: this establishes event-witness nonmanufacture, not a status or ontology result.
Retained evidence: the question remains distinct from receipt witness, provenance, and append history.
Reopening burden: provide an independently sourced event witness for the particular inquiry receipt.
-/
theorem questionDoesNotSelfCertify (_question : Question) :
    IsEmpty (InquiryEventReceipt NoWitness Unit) :=
  ⟨fun receipt => nomatch receipt.suppliedInquiryWitness⟩

inductive InquirerClaimKind where
  | ontology
  | consciousness
  | standing
  | ultimateSource
  | globalPriority
  | originalCutCausalSource
  deriving DecidableEq, Repr

/-- A promoted inquirer claim requires evidence separate from the question and inquiry witness. -/
structure InquirerClaimReceipt (kind : InquirerClaimKind) (ClaimWitness : Type u) where
  suppliedClaimWitness : ClaimWitness
  claimId : Nat
  authorityCeiling : AuthorityCeiling

/--
Route: SC-19.5 / D20 / T37 / M-INQUIRY-APPEND.
Hypotheses: an admitted inquiry receipt and an empty independent claim-witness type.
Positive claim: the receipt self-supplies none of six inquirer or original-source claims.
Overclaim not established: ontology, consciousness, standing, source, and priority remain open to evidence.
Authority ceiling: inquiry admission cannot promote the six claims or witness the original cut's source.
Retained evidence: the finite claim-kind distinction and separate witness address remain explicit.
Reopening burden: supply independent evidence and authority for the particular claim.
-/
theorem questionCannotSupplyInquirerClaims
    (_inquiry : InquiryEventReceipt InquiryWitness InquiryCostWitness) :
    ∀ kind : InquirerClaimKind, IsEmpty (InquirerClaimReceipt kind NoWitness) := by
  intro kind
  exact ⟨fun receipt => nomatch receipt.suppliedClaimWitness⟩

/-- A source-indexed cut keeps source identity outside the cut-only projection. -/
structure SourceIndexedCut (Source : Type u) where
  source : Source
  cut : CutIdentity

def cutOnlyView {Source : Type u} (receipt : SourceIndexedCut Source) : CutIdentity :=
  receipt.cut

/--
Route: SC-19.6 / D21 / T38 / M-SOURCE-FIBER.
Hypotheses: two source-indexed receipts whose cut fields are equal.
Positive claim: their cut-only projections are congruent.
Overclaim not established: equality of projections does not identify the sources.
Authority ceiling: the conclusion is restricted to the cut-only interface.
Retained evidence: both source fields remain present outside that projection.
Reopening burden: supply a source-discriminating witness or injectivity premise.
-/
theorem cutOnlyCongruence {Source : Type u} (left right : SourceIndexedCut Source)
    (equalCuts : left.cut = right.cut) : cutOnlyView left = cutOnlyView right := by
  simpa [cutOnlyView] using equalCuts

inductive FiberSource where | left | right deriving DecidableEq, Repr
inductive FiberCut where | shared deriving DecidableEq, Repr

def boundedSourceMap : FiberSource -> FiberCut
  | .left => .shared
  | .right => .shared

/--
Route: SC-19.6 / D21 / T38 / M-SOURCE-FIBER.
Hypotheses: the explicit two-source, one-cut bounded map.
Positive claim: distinct sources can have an equal cut-only image.
Overclaim not established: no assertion is made that every source map is noninjective.
Authority ceiling: this countermodel refutes generic source identification from equal cuts.
Retained evidence: both source constructors and the shared image remain explicit.
Reopening burden: add a discriminating witness or assume and justify injectivity.
-/
theorem noninjectiveSourceFiberCountermodel :
    FiberSource.left ≠ FiberSource.right ∧
      boundedSourceMap .left = boundedSourceMap .right := by
  decide

/--
Route: SC-19.6 / D21 / T38 / M-SOURCE-FIBER.
Hypotheses: a supplied source map, its injectivity proof, and equality of two cut images.
Positive claim: under that explicit premise, the two bounded sources are equal.
Overclaim not established: injectivity is not derived from PAL or from cut equality.
Authority ceiling: identification is conditional on the supplied comparison assumption.
Retained evidence: the map, injectivity premise, and equality witness remain required.
Reopening burden: challenge injectivity or exhibit a nontrivial source fiber.
-/
theorem injectiveSourceIdentificationAssumptionBound {Source : Type u} {Cut : Type v}
    (sourceMap : Source -> Cut) (injective : Function.Injective sourceMap)
    {left right : Source} (equalCuts : sourceMap left = sourceMap right) :
    left = right :=
  injective equalCuts

/-- A ledger is an ordered list of independently event- and cost-witnessed receipts. -/
structure InquiryLedger (InquiryWitness : Type u) (InquiryCostWitness : Type v) where
  entries : List (InquiryEventReceipt InquiryWitness InquiryCostWitness)

def appendReceipt (ledger : InquiryLedger InquiryWitness InquiryCostWitness)
    (receipt : InquiryEventReceipt InquiryWitness InquiryCostWitness)
    (_linked : ∃ parent ∈ ledger.entries,
      receipt.linkedParent = some parent.eventId)
    (_retains : receipt.retainedPriorIds =
      ledger.entries.map (fun prior => prior.eventId))
    (_fresh : receipt.eventId ∉ ledger.entries.map (fun prior => prior.eventId)) :
    InquiryLedger InquiryWitness InquiryCostWitness where
  entries := ledger.entries ++ [receipt]

/--
Route: SC-19.7 / D22 / T39 / M-INQUIRY-APPEND.
Hypotheses: an existing ledger; independent event and cost witnesses; an existing
parent link; exact retention of prior identifiers; and a fresh appended event id.
Positive claim: linked append preserves the prior exactly, while a missing cost witness blocks receipt.
Overclaim not established: one append does not imply another or an infinite inquiry ontology.
Authority ceiling: the result concerns finite list extension only.
Retained evidence: every prior entry and id plus both witnesses, cost, provenance, and link.
Reopening burden: each further inquiry needs independent event and cost witnesses and an append proof.
-/
theorem witnessedInquiryAppendPreservesPrefix
    (ledger : InquiryLedger InquiryWitness InquiryCostWitness)
    (receipt : InquiryEventReceipt InquiryWitness InquiryCostWitness)
    (linked : ∃ parent ∈ ledger.entries,
      receipt.linkedParent = some parent.eventId)
    (retains : receipt.retainedPriorIds =
      ledger.entries.map (fun prior => prior.eventId))
    (fresh : receipt.eventId ∉ ledger.entries.map (fun prior => prior.eventId)) :
    List.IsPrefix ledger.entries (appendReceipt ledger receipt linked retains fresh).entries ∧
      receipt ∈ (appendReceipt ledger receipt linked retains fresh).entries ∧
      receipt.retainedPriorIds = ledger.entries.map (fun prior => prior.eventId) ∧
      receipt.eventId ∉ ledger.entries.map (fun prior => prior.eventId) ∧
      IsEmpty (InquiryEventReceipt InquiryWitness NoWitness) := by
  constructor
  · exact ⟨[receipt], rfl⟩
  constructor
  · simp [appendReceipt]
  constructor
  · exact retains
  constructor
  · exact fresh
  · exact ⟨fun missingCost => nomatch missingCost.suppliedCostWitness⟩

structure InquiryState (InquiryWitness : Type u) (InquiryCostWitness : Type v) where
  ledger : InquiryLedger InquiryWitness InquiryCostWitness
  wasReopened : Bool
  admitsFurther : Bool

def terminalQuestion : Question := { questionId := 1, scope := { value := 1 } }

def terminalInquiryReceipt : InquiryEventReceipt Unit Unit :=
  admitInquiry 1 terminalQuestion () () { value := 2 } { value := 2 } (some 0)
    { value := 2 } { value := 2 } baseAuthority { value := 2 } { value := 2 } [0]

def terminalInquiryLedger : InquiryLedger Unit Unit :=
  { entries := [admitInquiry 0 terminalQuestion () () { value := 1 } { value := 1 }
      none { value := 1 } { value := 1 } baseAuthority { value := 1 }
      { value := 1 } []] }

def terminalInquiryState : InquiryState Unit Unit where
  ledger := appendReceipt terminalInquiryLedger terminalInquiryReceipt
    (by simp [terminalInquiryLedger, terminalInquiryReceipt, admitInquiry])
    (by simp [terminalInquiryLedger, terminalInquiryReceipt, admitInquiry])
    (by simp [terminalInquiryLedger, terminalInquiryReceipt, admitInquiry])
  wasReopened := true
  admitsFurther := false

def SupportsUnboundedInquiry
    (state : InquiryState InquiryWitness InquiryCostWitness) : Prop :=
  ∀ bound : Nat, ∃ receipt ∈ state.ledger.entries, bound < receipt.eventId

/--
Route: SC-19.7 / D22 / T39 / M-INQUIRY-APPEND.
Hypotheses: one protected parent plus an independently witnessed and cost-bearing linked child.
Positive claim: the explicit linked reopen/append preserves its parent and then terminates finitely.
Overclaim not established: other ledgers may continue; finitude is not an ontology theorem.
Authority ceiling: this is a bounded countermodel to inference from inquiry to infinity.
Retained evidence: parent prefix and id, child link and witnesses, costs, and finite history.
Reopening burden: append a new independently witnessed event and change the terminal flag.
-/
theorem finiteTerminalCountermodel :
    terminalInquiryState.ledger.entries.length = 2 ∧
      List.IsPrefix terminalInquiryLedger.entries terminalInquiryState.ledger.entries ∧
      terminalInquiryReceipt ∈ terminalInquiryState.ledger.entries ∧
      terminalInquiryReceipt.linkedParent = some 0 ∧
      terminalInquiryReceipt.retainedPriorIds = [0] ∧
      terminalInquiryReceipt.eventId ∉
        terminalInquiryLedger.entries.map (fun receipt => receipt.eventId) ∧
      terminalInquiryState.wasReopened = true ∧
      terminalInquiryState.admitsFurther = false ∧
      Not (SupportsUnboundedInquiry terminalInquiryState) := by
  constructor
  · rfl
  constructor
  · exact ⟨[terminalInquiryReceipt], rfl⟩
  constructor
  · simp [terminalInquiryState, appendReceipt]
  constructor
  · rfl
  constructor
  · rfl
  constructor
  · simp [terminalInquiryLedger, terminalInquiryReceipt, admitInquiry]
  constructor
  · rfl
  constructor
  · rfl
  · intro unbounded
    rcases unbounded 1 with ⟨receipt, member, greater⟩
    have eventMember : receipt.eventId ∈
        terminalInquiryState.ledger.entries.map (fun entry => entry.eventId) :=
      List.mem_map_of_mem member
    have bounded : receipt.eventId = 0 ∨ receipt.eventId = 1 := by
      simpa [terminalInquiryState, terminalInquiryLedger, terminalInquiryReceipt,
        appendReceipt, admitInquiry] using eventMember
    omega

/-- A linked later recovery record carries both the prior and actual appended histories. -/
structure LaterEvidenceReceipt (PriorWitness : Type u) (PriorCostWitness : Type v)
    (LaterWitness : Type u) where
  prior : InquiryLedger PriorWitness PriorCostWitness
  parent : InquiryEventReceipt PriorWitness PriorCostWitness
  parentPresent : parent ∈ prior.entries
  laterRecord : InquiryEventReceipt PriorWitness PriorCostWitness
  linkedToParent : laterRecord.linkedParent = some parent.eventId
  retainsPriorIds : laterRecord.retainedPriorIds =
    prior.entries.map (fun receipt => receipt.eventId)
  freshLaterId : laterRecord.eventId ∉
    prior.entries.map (fun receipt => receipt.eventId)
  laterRecoveryWitness : LaterWitness
  laterEvidenceId : Nat
  history : InquiryLedger PriorWitness PriorCostWitness
  historyIsAppend : history.entries = prior.entries ++ [laterRecord]

def appendLaterEvidence (prior : InquiryLedger PriorWitness PriorCostWitness)
    (parent : InquiryEventReceipt PriorWitness PriorCostWitness)
    (parentPresent : parent ∈ prior.entries)
    (laterRecord : InquiryEventReceipt PriorWitness PriorCostWitness)
    (linked : laterRecord.linkedParent = some parent.eventId)
    (retains : laterRecord.retainedPriorIds =
      prior.entries.map (fun receipt => receipt.eventId))
    (fresh : laterRecord.eventId ∉
      prior.entries.map (fun receipt => receipt.eventId))
    (witness : LaterWitness) (evidenceId : Nat) :
    LaterEvidenceReceipt PriorWitness PriorCostWitness LaterWitness where
  prior := prior
  parent := parent
  parentPresent := parentPresent
  laterRecord := laterRecord
  linkedToParent := linked
  retainsPriorIds := retains
  freshLaterId := fresh
  laterRecoveryWitness := witness
  laterEvidenceId := evidenceId
  history := appendReceipt prior laterRecord
    ⟨parent, parentPresent, linked⟩ retains fresh
  historyIsAppend := rfl

/--
Route: SC-19.8 / D23 / T40 / M-INQUIRY-APPEND.
Hypotheses: an existing parent, membership proof, linked fresh later record,
retained ids, and a separately supplied later recovery witness.
Positive claim: actual history append preserves the parent's witness, cost, trace, and authority.
Overclaim not established: later evidence cannot create earlier payment, warrant, or standing.
Authority ceiling: fieldwise equality governs this proof-gated append constructor only.
Retained evidence: exact prior history, parent fields, link, later record, and recovery witness.
Reopening burden: challenge parent membership/linkage or append another witnessed record.
-/
theorem laterEvidenceAppendPreservesPrior
    (prior : InquiryLedger PriorWitness PriorCostWitness)
    (parent : InquiryEventReceipt PriorWitness PriorCostWitness)
    (parentPresent : parent ∈ prior.entries)
    (laterRecord : InquiryEventReceipt PriorWitness PriorCostWitness)
    (linked : laterRecord.linkedParent = some parent.eventId)
    (retains : laterRecord.retainedPriorIds =
      prior.entries.map (fun receipt => receipt.eventId))
    (fresh : laterRecord.eventId ∉
      prior.entries.map (fun receipt => receipt.eventId))
    (witness : LaterWitness) (evidenceId : Nat) :
    let appended := appendLaterEvidence prior parent parentPresent laterRecord linked
      retains fresh witness evidenceId
    List.IsPrefix prior.entries appended.history.entries ∧
      parent ∈ appended.history.entries ∧ laterRecord ∈ appended.history.entries ∧
      laterRecord.eventId ∉ prior.entries.map (fun receipt => receipt.eventId) ∧
      ∃ preserved ∈ appended.history.entries,
        preserved.eventId = parent.eventId ∧
        preserved.suppliedInquiryWitness = parent.suppliedInquiryWitness ∧
        preserved.inquiryCost = parent.inquiryCost ∧
        preserved.carriedTrace = parent.carriedTrace ∧
        preserved.authoritySnapshot = parent.authoritySnapshot := by
  dsimp [appendLaterEvidence]
  constructor
  · exact ⟨[laterRecord], rfl⟩
  constructor
  · exact List.mem_append_left [laterRecord] parentPresent
  constructor
  · simp [appendReceipt]
  constructor
  · exact fresh
  · exact ⟨parent, List.mem_append_left [laterRecord] parentPresent,
      rfl, rfl, rfl, rfl, rfl⟩

def mutatedBaseCutReceipt : AccountCutReceipt Unit :=
  { baseCutReceipt with cutIndexedCost := { value := 8 } }

def overwriteHead (ledger : List (AccountCutReceipt Unit))
    (replacement : AccountCutReceipt Unit) : List (AccountCutReceipt Unit) :=
  replacement :: ledger.drop 1

/--
Route: SC-19.8 / D23 / T40 / M-INQUIRY-APPEND.
Hypotheses: the concrete one-entry ledger and a replacement with rewritten cost.
Positive claim: overwrite can erase the original instead of preserving it as an append prefix.
Overclaim not established: this countermodel does not accuse every update of overwriting.
Authority ceiling: it distinguishes one destructive operation from the licensed append route.
Retained evidence: original and mutated receipts remain separately inspectable in the theorem.
Reopening burden: use a linked append and prove preservation of the prior receipt.
-/
theorem overwriteIsNotAppendCountermodel :
    Not (List.IsPrefix [baseCutReceipt]
      (overwriteHead [baseCutReceipt] mutatedBaseCutReceipt)) ∧
      baseCutReceipt ∉ overwriteHead [baseCutReceipt] mutatedBaseCutReceipt := by
  decide

end PAL.AttackRun0003
