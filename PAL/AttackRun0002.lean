import PAL.AttackRun0001

/-!
# Attack Run 0002: first-cut receipt and source-open countermodels

Controlling release during this candidate run: PAL v2.0,
DOI 10.5281/zenodo.21754097. The five exact source identities and hashes are
recorded in `Audit/source-manifest.yaml`. Candidate statements C21-01 through
C21-08 remain noncanonical and do not amend those sources or close O04/O25.

Checked environment: Lean 4.32.1 and Mathlib v4.32.1. This module uses only
bounded source fibers, supplied cut witnesses, finite account records, and
finite history witnesses. Unresolved possibility remains metalinguistic and
has no object-language type, value, constructor, set, envelope, or residue.

The occurrence model is deliberately later-witnessed: an A0 `CutReceipt` alone
is not an occurrence receipt. Account order and event time are distinct fields.
Positive inquiry construction requires a supplied inquiry witness. Later
witnessing retains the complete earlier receipt and therefore cannot rewrite
its cost, authority, provenance, or other fields.
-/

namespace PAL.AttackRun0002

open PAL.AttackRun0001

universe u v w x

/-! ## Source fibers -/

/-- Two admitted source candidates for a finite countermodel. -/
inductive BoundedSource where
  | sourceA
  | sourceB
  deriving DecidableEq, Repr

/-- The one accessible cut in the finite source-fiber countermodel. -/
inductive AccessibleCut where
  | shared
  deriving DecidableEq, Repr

/-- A bounded source-to-cut map; it is not an exhaustive source domain. -/
def sigma : BoundedSource -> AccessibleCut
  | .sourceA => .shared
  | .sourceB => .shared

/--
AR2-01 / C21-06 — COUNTERMODEL.

Source route: candidate workflow §3.1 and Gate 3; PAL v2.0 Spine SC-01/L05;
Atlas M-A0-CUT; Ledger D14/O04/O25; Tests T15. Assumptions: only the two
finite inductive types and the displayed `sigma`; no source-uniqueness premise.
Axiom receipt: `Audit/AttackRun0002.lean`. Authority ceiling: this establishes
noninjectivity only in the displayed bounded model and makes no ultimate-source
or global-priority claim. Predecessor/countercase: the stronger injectivity
claim is rejected by `sourceA` and `sourceB` sharing one cut. Versions: Lean
4.32.1, Mathlib v4.32.1. Reopening: C21-06, D14, O04, O25.
-/
theorem sourceFiberCountermodel :
    ∃ s₁ s₂ : BoundedSource, s₁ ≠ s₂ ∧ sigma s₁ = sigma s₂ := by
  refine ⟨.sourceA, .sourceB, ?_, rfl⟩
  decide

/--
AR2-02 / C21-06 — PROVED.

Source route: candidate workflow §3.1 and Gate 3; PAL v2.0 Spine SC-01/L05;
Atlas M-A0-CUT; Ledger D14/O04/O25; Tests T15. Assumptions: arbitrary supplied
functions `sigma` and `downstream`, plus an explicit equality of their two cut
inputs. Axiom receipt: `Audit/AttackRun0002.lean`. Authority ceiling: result
equality after the cut does not imply source equality or injectivity.
Predecessor/countercase: AR2-01 supplies the noninjective predecessor model.
Versions: Lean 4.32.1, Mathlib v4.32.1. Reopening: C21-06, O04, O25.
-/
theorem downstreamCannotDistinguishSameCut
    {Source : Type u} {Cut : Type v} {Result : Type w}
    (sigma : Source -> Cut) (downstream : Cut -> Result)
    {s₁ s₂ : Source} (sameCut : sigma s₁ = sigma s₂) :
    downstream (sigma s₁) = downstream (sigma s₂) :=
  congrArg downstream sameCut

/-! ## Supplied cut and later-witnessed occurrence model -/

/-- A bounded model envelope reused from Attack Run 0001. -/
def boundedModel : ModelEnvelope where
  Carrier := Unit
  inhabited := ⟨()⟩
  scopeId := 21
  entryCost := 0

/-- An earlier authority snapshot; later results may only carry it forward. -/
def boundedAuthority : AuthoritySnapshot where
  identityId := 210
  evidenceId := 211
  consentRecorded := false
  standingRecorded := false
  uncertaintyId := 212
  authorityId := 213

/-- The supplied A0 receipt. Its cost field is accounting data, not a cause. -/
def sharedSuppliedCut : CutReceipt boundedModel Unit where
  boundaryId := 42
  scopeId := boundedModel.scopeId
  witness := ()
  admissionBasisId := 214
  cost := 7

/-- A supplied cut with account order kept separate from event time. -/
structure AddressedCut
    (model : ModelEnvelope) (CutWitness : Type u) (Cut : Type v) where
  supplied : CutReceipt model CutWitness
  accessible : Cut
  accountId : Nat
  accountOrder : Nat
  eventTime : Nat
  authority : AuthoritySnapshot

/-- The first address in one declared account, recorded after an earlier event. -/
def localFirstCut : AddressedCut boundedModel Unit AccessibleCut where
  supplied := sharedSuppliedCut
  accessible := .shared
  accountId := 300
  accountOrder := 0
  eventTime := 10
  authority := boundedAuthority

/-- A separate supplied cut used only as the earlier temporal countercase. -/
def earlierSuppliedCut : CutReceipt boundedModel Unit where
  boundaryId := 41
  scopeId := boundedModel.scopeId
  witness := ()
  admissionBasisId := 215
  cost := 4

/-- An event outside the local account whose event time is earlier. -/
def earlierExternalCut : AddressedCut boundedModel Unit AccessibleCut where
  supplied := earlierSuppliedCut
  accessible := .shared
  accountId := 301
  accountOrder := 5
  eventTime := 3
  authority := boundedAuthority

/-- The exact two instants admitted by the bounded history model. -/
inductive HistoryTime where
  | occurred
  | recovered
  deriving DecidableEq, Repr

/-- Numeric order is supplied only for the two admitted history instants. -/
def historyTimeIndex : HistoryTime -> Nat
  | .occurred => 0
  | .recovered => 1

/-- A two-instant activity history: active first and inactive second. -/
def pulseActivity : HistoryTime -> Bool
  | .occurred => true
  | .recovered => false

/--
An occurrence receipt is a distinct, later-witnessed stage over a supplied cut.
The activity proof and trace address make the past occurrence recoverable; the
structure has no causal-source or source-uniqueness field.
-/
structure OccurrenceReceipt
    {model : ModelEnvelope} {CutWitness : Type u}
    (Cut : Type v) (LaterWitness : Type w) where
  cut : AddressedCut model CutWitness Cut
  witness : LaterWitness
  activity : HistoryTime -> Bool
  occurredAt : HistoryTime
  recoveredAt : HistoryTime
  recoveredAfter : historyTimeIndex occurredAt ≤ historyTimeIndex recoveredAt
  activeAtOccurrence : activity occurredAt = true
  traceAddress : Nat
  occurrenceId : Nat

/-- A later-witnessed occurrence over the shared cut. -/
def sharedOccurrence :
    OccurrenceReceipt (model := boundedModel) (CutWitness := Unit)
      AccessibleCut Unit where
  cut := localFirstCut
  witness := ()
  activity := pulseActivity
  occurredAt := .occurred
  recoveredAt := .recovered
  recoveredAfter := by decide
  activeAtOccurrence := rfl
  traceAddress := 500
  occurrenceId := 501

/--
AR2-03 / C21-03,C21-05,C21-06 — COUNTERMODEL.

Source route: candidate workflow §§3.1,3.3 and Gate 3; PAL v2.0 Spine
SC-01/SC-05/L04/L05; Atlas M-A0-CUT/M-A2-STORE; Ledger D14/O04/O25;
Tests T11/T15/T16. Assumptions: the supplied A0 receipt, an explicit later
occurrence witness, finite history, and the bounded `sigma`. Axiom receipt:
`Audit/AttackRun0002.lean`. Authority ceiling: occurrence recovery neither
identifies a unique source nor manufactures the later witness; O04/O25 remain
open. Predecessor/countercase: an A0 receipt with the empty later-witness type
cannot form an occurrence, while the witnessed occurrence coexists with a
noninjective source map. Versions: Lean 4.32.1, Mathlib v4.32.1. Reopening:
C21-03, C21-05, C21-06, D14, O04, O25.
-/
theorem occurrenceDoesNotIdentifySource :
    Nonempty
        (OccurrenceReceipt (model := boundedModel) (CutWitness := Unit)
          AccessibleCut Unit) ∧
      IsEmpty
        (OccurrenceReceipt (model := boundedModel) (CutWitness := Unit)
          AccessibleCut NoWitness) ∧
      ¬ Function.Injective sigma := by
  constructor
  · exact ⟨sharedOccurrence⟩
  constructor
  · exact ⟨fun receipt => nomatch receipt.witness⟩
  · intro injective
    have collapsed : BoundedSource.sourceA = BoundedSource.sourceB :=
      injective rfl
    exact (by decide : BoundedSource.sourceA ≠ BoundedSource.sourceB) collapsed

/-- A causal-source claim requires its own externally supplied witness. -/
structure CausalSourceReceipt (Source : Type u) (SourceWitness : Type v) where
  source : Source
  witness : SourceWitness
  claimId : Nat

/--
AR2-04 / C21-02 — COUNTERMODEL.

Source route: candidate workflow Gate 3; PAL v2.0 Spine SC-01/L01/L05; Atlas
M-A0-CUT; Ledger D14/O04/O25; Tests T06/T15. `M-A4-DEBT` is not a controlling
premise for A0 in this model. Assumptions: the already supplied A0 cut and an
empty causal-witness type; cost is the existing `CutReceipt.cost : Nat` field.
Axiom receipt: `Audit/AttackRun0002.lean`. Authority ceiling: a populated cost
field is ledger data only and proves neither cause nor truth. Predecessor/
countercase: the cost-bearing cut type is inhabited while the causal-source
receipt is empty. Versions: Lean 4.32.1, Mathlib v4.32.1. Reopening: C21-02,
O04, O25, and any later Atlas cost-carrier decision.
-/
theorem costDoesNotImplyCause :
    Nonempty (CutReceipt boundedModel Unit) ∧
      IsEmpty (CausalSourceReceipt BoundedSource NoWitness) := by
  constructor
  · exact ⟨sharedSuppliedCut⟩
  · exact ⟨fun receipt => nomatch receipt.witness⟩

/--
AR2-05 / C21-03,C21-04,C21-08 — COUNTERMODEL.

Source route: candidate workflow §3.3 and Gate 3; PAL v2.0 Spine SC-05/L04/L08;
Atlas M-A2-STORE; Tests T11/T16. Assumptions: the finite `pulseActivity`, a
supplied later witness, a trace address, and the displayed time-order proof.
Axiom receipt: `Audit/AttackRun0002.lean`. Authority ceiling: historical
recoverability is not continuous activity and says nothing about ultimate
source or global priority. Predecessor/countercase: the stronger identification
of current activity with past occurrence fails at recovery time one. Versions:
Lean 4.32.1, Mathlib v4.32.1. Reopening: C21-03, C21-04, C21-08, O04.
-/
theorem historicalPersistence :
    ∃ receipt :
        OccurrenceReceipt (model := boundedModel) (CutWitness := Unit)
          AccessibleCut Unit,
      historyTimeIndex receipt.occurredAt <
          historyTimeIndex receipt.recoveredAt ∧
        receipt.activity receipt.recoveredAt = false := by
  exact ⟨sharedOccurrence, by decide, rfl⟩

/-! ## Account-relative order -/

/-- First means address zero in the entry's declared account only. -/
def IsLocalFirst
    {model : ModelEnvelope} {CutWitness : Type u} {Cut : Type v}
    (entry : AddressedCut model CutWitness Cut) : Prop :=
  entry.accountOrder = 0

/-- A separate temporal predicate relative to an explicitly supplied history. -/
def IsGlobalFirstIn
    {model : ModelEnvelope} {CutWitness : Type u} {Cut : Type v}
    (entry : AddressedCut model CutWitness Cut)
    (history : List (AddressedCut model CutWitness Cut)) : Prop :=
  ∀ other ∈ history, entry.eventTime ≤ other.eventTime

/--
AR2-06 / C21-01,C21-04 — COUNTERMODEL.

Source route: candidate workflow Gate 3; PAL v2.0 Spine SC-01 and account scope;
Atlas M-A0-CUT; Ledger D14/O04/O25; Tests T04/T06/T15. Assumptions: one local
account position and one explicitly supplied external history entry. Axiom
receipt: `Audit/AttackRun0002.lean`. Authority ceiling: account address order
does not determine temporal order, a global event order, or a source order.
Predecessor/countercase: `localFirstCut` has account order zero but event time
ten, while `earlierExternalCut` has event time three. Versions: Lean 4.32.1,
Mathlib v4.32.1. Reopening: C21-01, C21-04, D14, O04, O25.
-/
theorem noGlobalFirstFromLocalFirst :
    IsLocalFirst localFirstCut ∧
      ¬ IsGlobalFirstIn localFirstCut [earlierExternalCut] := by
  constructor
  · rfl
  · intro promoted
    have impossible : localFirstCut.eventTime ≤ earlierExternalCut.eventTime :=
      promoted earlierExternalCut (List.Mem.head [])
    exact
      (by decide : ¬ localFirstCut.eventTime ≤ earlierExternalCut.eventTime)
        impossible

/-! ## Finite source inquiry -/

/--
One finite inquiry step carries its prior cut and a newly supplied cut receipt.
The new `CutReceipt` itself carries the inquiry witness and its own cost.
-/
structure InquiryReceipt
    {model : ModelEnvelope} (PriorReceipt : Type u) (InquiryWitness : Type v) where
  prior : PriorReceipt
  newCut : CutReceipt model InquiryWitness
  parentBoundaryId : Nat
  inquiryId : Nat

/-- Append exactly one supplied inquiry cut to a finite receipt prefix. -/
def appendInquiry
    {model : ModelEnvelope} {PriorReceipt : Type u} {InquiryWitness : Type v}
    (prior : PriorReceipt) (inquiryWitness : InquiryWitness) (inquiryCost : Nat)
    (parentBoundaryId inquiryId : Nat) :
    InquiryReceipt (model := model) PriorReceipt InquiryWitness where
  prior := prior
  newCut :=
    { boundaryId := parentBoundaryId + 1
      scopeId := model.scopeId
      witness := inquiryWitness
      admissionBasisId := inquiryId
      cost := inquiryCost }
  parentBoundaryId := parentBoundaryId
  inquiryId := inquiryId

/--
AR2-07 / C21-05,C21-07 — PROVED.

Source route: candidate workflow Gate 3 and finite-prefix route; PAL v2.0 Spine
SC-01/L01/L05/L08; Atlas M-A0-CUT; Ledger D14/O04/O25; Tests T15/T16.
Assumptions: an externally supplied `inquiryWitness` and supplied `inquiryCost`;
only one finite append is constructed. Axiom receipt: `Audit/AttackRun0002.lean`.
Authority ceiling: the inquiry receipt proves only its own present cut and cost;
it neither witnesses the original cause nor proves an infinite source chain.
Predecessor/countercase: with an empty inquiry-witness type no call can supply
the required argument; the positive result below exposes that argument.
Versions: Lean 4.32.1, Mathlib v4.32.1. Reopening: C21-05, C21-07, O04, O25.
-/
theorem inquiryCreatesNewReceipt
    {InquiryWitness : Type u} (inquiryWitness : InquiryWitness)
    (inquiryCost : Nat) :
    ∃ receipt :
        InquiryReceipt (model := boundedModel)
          (AddressedCut boundedModel Unit AccessibleCut) InquiryWitness,
      receipt.prior = localFirstCut ∧
        receipt.newCut.boundaryId = localFirstCut.supplied.boundaryId + 1 ∧
        receipt.newCut.witness = inquiryWitness ∧
        receipt.newCut.cost = inquiryCost := by
  refine
    ⟨appendInquiry (model := boundedModel) localFirstCut inquiryWitness inquiryCost
      localFirstCut.supplied.boundaryId 600, ?_⟩
  exact ⟨rfl, rfl, rfl, rfl⟩

/-! ## Later witnessing without retroactive rewrite -/

/-- A later witness is appended beside the complete earlier occurrence receipt. -/
structure LaterWitnessReceipt
    {model : ModelEnvelope} {CutWitness : Type u} {Cut : Type v}
    (OccurrenceWitness : Type w) (LaterWitness : Type x) where
  prior : OccurrenceReceipt (model := model) (CutWitness := CutWitness)
    Cut OccurrenceWitness
  witness : LaterWitness
  recoveryAddress : Nat
  laterTime : Nat
  laterAfterPrior : historyTimeIndex prior.recoveredAt ≤ laterTime

/-- Append a supplied later witness without rebuilding the prior receipt. -/
def appendLaterWitness
    {model : ModelEnvelope} {CutWitness : Type u} {Cut : Type v}
    {OccurrenceWitness : Type w} {LaterWitness : Type x}
    (prior : OccurrenceReceipt (model := model) (CutWitness := CutWitness)
      Cut OccurrenceWitness)
    (laterWitness : LaterWitness) (recoveryAddress laterTime : Nat)
    (laterAfterPrior : historyTimeIndex prior.recoveredAt ≤ laterTime) :
    LaterWitnessReceipt (model := model) (CutWitness := CutWitness)
      (Cut := Cut) OccurrenceWitness LaterWitness where
  prior := prior
  witness := laterWitness
  recoveryAddress := recoveryAddress
  laterTime := laterTime
  laterAfterPrior := laterAfterPrior

/--
AR2-08 / C21-08 — PROVED.

Source route: candidate workflow Gate 3; PAL v2.0 Spine L04/L05/L08; Atlas
M-A2-STORE/M-A15-CHECK; Ledger D14/O04/O25; Tests T15/T16/T17. Assumptions:
the complete earlier occurrence receipt, a supplied later witness, and an
explicit time-order proof. Axiom receipt: `Audit/AttackRun0002.lean`. Authority
ceiling: later recovery adds no earlier occurrence, witness, source, cost, or
authority. Predecessor/countercase: the full prior receipt is retained by exact
equality, so a constructor that retroactively replaces any prior field is not
this bounded append operation. Versions: Lean 4.32.1, Mathlib v4.32.1.
Reopening: C21-08, L08, O04, O25.
-/
theorem noRetroactivePayment
    {model : ModelEnvelope} {CutWitness : Type u} {Cut : Type v}
    {OccurrenceWitness : Type w} {LaterWitness : Type x}
    (prior : OccurrenceReceipt (model := model) (CutWitness := CutWitness)
      Cut OccurrenceWitness)
    (laterWitness : LaterWitness) (recoveryAddress laterTime : Nat)
    (laterAfterPrior : historyTimeIndex prior.recoveredAt ≤ laterTime) :
    let later :=
      appendLaterWitness prior laterWitness recoveryAddress laterTime laterAfterPrior
    later.prior = prior ∧
      later.prior.cut.supplied.cost = prior.cut.supplied.cost ∧
      later.prior.cut.authority = prior.cut.authority := by
  dsimp [appendLaterWitness]
  exact ⟨rfl, rfl, rfl⟩

end PAL.AttackRun0002
