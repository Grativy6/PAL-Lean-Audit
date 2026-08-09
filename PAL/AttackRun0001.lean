import Mathlib.Data.List.Basic

/-!
# Attack Run 0001: bounded primitive-floor and trace realizations

Controlling release: PAL v2.0, DOI 10.5281/zenodo.21754097.

This module mechanically realizes only the named source cards and conformance
targets recorded beside each declaration. Unresolved possibility remains a
metalinguistic boundary: the object language below contains no corresponding
type, value, constructor argument, set, model, residue, or envelope.

The structures are deliberately witness-parameterized. Constructing a local
receipt demonstrates only the conditional instance supplied to Lean; it does
not discharge the open first-occurrence debt O04/O25.
-/

namespace PAL.AttackRun0001

universe u v w

/-- A universe-polymorphic empty type used only for missing-witness checks. -/
inductive NoWitness.{z} : Type z

/-! ## T15: witness-source honesty -/

/--
A bounded crossing rule can use a supplied witness but has no witness-producing
field of its own. Source routing: T15; spine law L05; O04/O05/O25/O26.
-/
structure Crossing (Input : Type u) (Witness : Type v) (Output : Type w) where
  apply : Input -> Witness -> Output

/-- Attempt a crossing only when its witness is externally present. -/
def Crossing.attempt {Input : Type u} {Witness : Type v} {Output : Type w}
    (crossing : Crossing Input Witness Output) (input : Input) :
    Option Witness -> Option Output
  | none => none
  | some witness => some (crossing.apply input witness)

/--
T15 bounded realization: a missing witness produces no output object.
This theorem governs only rules represented by `Crossing`.
-/
@[simp] theorem missingWitnessYieldsNoOutput
    {Input : Type u} {Witness : Type v} {Output : Type w}
    (crossing : Crossing Input Witness Output) (input : Input) :
    crossing.attempt input none = none := rfl

/-! ## T06-T11: primitive-floor dependency route -/

/--
The optional pre-cut model envelope M0 is scaffolding, not A0.
Source routing: M-M0; D03; O02.
-/
structure ModelEnvelope where
  Carrier : Type u
  inhabited : Nonempty Carrier
  scopeId : Nat
  entryCost : Nat

/--
T06 bounded realization of A0 as a supplied cut receipt over an optional M0.
The witness type is an external parameter and is not manufactured here.
Source routing: SC-01; D03; O02; M-A0-CUT.
-/
structure CutReceipt (model : ModelEnvelope) (CutWitness : Type v) where
  boundaryId : Nat
  scopeId : Nat
  witness : CutWitness
  admissionBasisId : Nat
  cost : Nat

/-- Forgetting the cut returns the separate M0 scaffolding unchanged. -/
def CutReceipt.forgetModel {model : ModelEnvelope} {CutWitness : Type v}
    (_receipt : CutReceipt model CutWitness) : ModelEnvelope := model

/-- A pre-cut model envelope cannot supply an A0 receipt without a witness. -/
theorem noCutWithoutWitness (model : ModelEnvelope) :
    IsEmpty (CutReceipt model NoWitness) :=
  ⟨fun receipt => nomatch receipt.witness⟩

/--
T07 bounded realization of the cut-indexed reflection receipt. No particular
reflection, involution, exchange law, or tolerance is made canonical.
Source routing: SC-02; D04; O02/O29; M-ΩSTAR.
-/
structure ReflectionReceipt {model : ModelEnvelope} {CutWitness : Type v}
    (cut : CutReceipt model CutWitness) (ReflectionWitness : Type w) where
  witness : ReflectionWitness
  ruleId : Nat
  cost : Nat

/-- T15 coverage: a reflection receipt cannot exist with an empty witness type. -/
theorem noReflectionWithoutWitness
    {model : ModelEnvelope} {CutWitness : Type v}
    (cut : CutReceipt model CutWitness) :
    IsEmpty (ReflectionReceipt cut NoWitness) :=
  ⟨fun receipt => nomatch receipt.witness⟩

/-- Forgetting a reflection returns the exact cut that indexed it. -/
def ReflectionReceipt.forgetCut
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    (_receipt : ReflectionReceipt cut ReflectionWitness) :
    CutReceipt model CutWitness := cut

@[simp] theorem reflectionForgetsToIndexedCut
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    (receipt : ReflectionReceipt cut ReflectionWitness) :
    receipt.forgetCut = cut := rfl

/-- Residue is indexed to an admitted cut, never to the metalinguistic floor. -/
structure ResidueReceipt {model : ModelEnvelope} {CutWitness : Type v}
    (cut : CutReceipt model CutWitness) where
  accountId : Nat
  residualId : Nat

/-- Primitive-floor addresses admitted to the bounded object language. -/
inductive PrimitiveStage where
  | a0
  | reflection
  | theta
  | a1
  | a2
  deriving DecidableEq, Repr

def PrimitiveStage.rank : PrimitiveStage -> Nat
  | .a0 => 0
  | .reflection => 1
  | .theta => 2
  | .a1 => 3
  | .a2 => 4

/-- T07: the cut and its reflection have distinct formal addresses. -/
theorem cutAddressNeReflectionAddress :
    PrimitiveStage.a0 ≠ PrimitiveStage.reflection := by
  decide

/--
T09 bounded realization of a trace-bearing nonidentity turn. It records a
predecessor and successor but contains no side or readout field.
Source routing: SC-03; D06; O03/O29; M-THETA.
-/
structure TurnReceipt
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    (reflection : ReflectionReceipt cut ReflectionWitness)
    (OrientationState : Type u) (TurnWitness : Type v) where
  predecessor : OrientationState
  successor : OrientationState
  changed : predecessor ≠ successor
  witness : TurnWitness
  actionId : Nat
  cost : Nat

/-- Forgetting a turn returns the exact reflection that indexed it. -/
def TurnReceipt.forgetReflection
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    {reflection : ReflectionReceipt cut ReflectionWitness}
    {OrientationState : Type u} {TurnWitness : Type v}
    (_receipt : TurnReceipt reflection OrientationState TurnWitness) :
    ReflectionReceipt cut ReflectionWitness := reflection

@[simp] theorem turnForgetsToIndexedReflection
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    {reflection : ReflectionReceipt cut ReflectionWitness}
    {OrientationState : Type u} {TurnWitness : Type v}
    (receipt : TurnReceipt reflection OrientationState TurnWitness) :
    receipt.forgetReflection = reflection := rfl

/-- T15 coverage: a turn receipt cannot exist with an empty witness type. -/
theorem noTurnWithoutWitness
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    (reflection : ReflectionReceipt cut ReflectionWitness)
    (OrientationState : Type u) :
    IsEmpty (TurnReceipt reflection OrientationState NoWitness) :=
  ⟨fun receipt => nomatch receipt.witness⟩

/--
T11 bounded realization of A1. Readability requires a separately supplied
readout witness and inherits orientation from the indexed turn.
Source routing: SC-04; D07; O05/O26; M-A1-APART.
-/
structure ReadableReceipt
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    {reflection : ReflectionReceipt cut ReflectionWitness}
    {OrientationState : Type u} {TurnWitness : Type v}
    (turn : TurnReceipt reflection OrientationState TurnWitness)
    (ReadoutWitness : Type w) (Side : Type u) where
  witness : ReadoutWitness
  negativeSide : Side
  positiveSide : Side
  separated : negativeSide ≠ positiveSide
  tolerance : Nat
  residualId : Nat
  provenanceId : Nat

/-- T15 coverage: a readable receipt cannot exist with an empty readout witness type. -/
theorem noReadableWithoutWitness
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    {reflection : ReflectionReceipt cut ReflectionWitness}
    {OrientationState : Type u} {TurnWitness : Type v}
    (turn : TurnReceipt reflection OrientationState TurnWitness)
    (Side : Type u) :
    IsEmpty (ReadableReceipt turn NoWitness Side) :=
  ⟨fun receipt => nomatch receipt.witness⟩

/-- Forgetting A1 returns the complete turn receipt without selecting either state. -/
def ReadableReceipt.forgetTurn
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    {reflection : ReflectionReceipt cut ReflectionWitness}
    {OrientationState : Type u} {TurnWitness : Type v}
    {turn : TurnReceipt reflection OrientationState TurnWitness}
    {ReadoutWitness : Type w} {Side : Type u}
    (_receipt : ReadableReceipt turn ReadoutWitness Side) :
    TurnReceipt reflection OrientationState TurnWitness := turn

@[simp] theorem readableForgetsToIndexedTurn
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    {reflection : ReflectionReceipt cut ReflectionWitness}
    {OrientationState : Type u} {TurnWitness : Type v}
    {turn : TurnReceipt reflection OrientationState TurnWitness}
    {ReadoutWitness : Type w} {Side : Type u}
    (receipt : ReadableReceipt turn ReadoutWitness Side) :
    receipt.forgetTurn = turn := rfl

/--
T11 bounded realization of A2 as recoverable consequence. The original A1
receipt is an index, while recovery requires a new supplied witness and address.
Source routing: SC-05; D08; O06; M-A2-STORE.
-/
structure TraceReceipt
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    {reflection : ReflectionReceipt cut ReflectionWitness}
    {OrientationState : Type u} {TurnWitness : Type v}
    {turn : TurnReceipt reflection OrientationState TurnWitness}
    {ReadoutWitness : Type w} {Side : Type u}
    (readable : ReadableReceipt turn ReadoutWitness Side)
    (RecoveryWitness : Type v) (Address : Type w) where
  witness : RecoveryWitness
  address : Address
  occurrenceId : Nat
  storeVersion : Nat

/-- T15 coverage: a trace receipt cannot exist with an empty recovery witness type. -/
theorem noTraceWithoutWitness
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    {reflection : ReflectionReceipt cut ReflectionWitness}
    {OrientationState : Type u} {TurnWitness : Type v}
    {turn : TurnReceipt reflection OrientationState TurnWitness}
    {ReadoutWitness : Type w} {Side : Type u}
    (readable : ReadableReceipt turn ReadoutWitness Side)
    (Address : Type w) :
    IsEmpty (TraceReceipt readable NoWitness Address) :=
  ⟨fun receipt => nomatch receipt.witness⟩

/-- A2 recovers the exact A1 receipt that it extends. -/
def TraceReceipt.forgetReadable
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    {reflection : ReflectionReceipt cut ReflectionWitness}
    {OrientationState : Type u} {TurnWitness : Type v}
    {turn : TurnReceipt reflection OrientationState TurnWitness}
    {ReadoutWitness : Type w} {Side : Type u}
    {readable : ReadableReceipt turn ReadoutWitness Side}
    {RecoveryWitness : Type v} {Address : Type w}
    (_receipt : TraceReceipt readable RecoveryWitness Address) :
    ReadableReceipt turn ReadoutWitness Side := readable

@[simp] theorem traceForgetsToIndexedReadable
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    {reflection : ReflectionReceipt cut ReflectionWitness}
    {OrientationState : Type u} {TurnWitness : Type v}
    {turn : TurnReceipt reflection OrientationState TurnWitness}
    {ReadoutWitness : Type w} {Side : Type u}
    {readable : ReadableReceipt turn ReadoutWitness Side}
    {RecoveryWitness : Type v} {Address : Type w}
    (receipt : TraceReceipt readable RecoveryWitness Address) :
    receipt.forgetReadable = readable := rfl

/-- T10: the explicit primitive-floor order is part of the bounded model. -/
theorem primitivePlacement :
    PrimitiveStage.rank .a0 < PrimitiveStage.rank .reflection ∧
    PrimitiveStage.rank .reflection < PrimitiveStage.rank .theta ∧
    PrimitiveStage.rank .theta < PrimitiveStage.rank .a1 := by
  decide

/-- T10: following the dependent chain back returns the supplied cut. -/
theorem floorChainReturnsCut
    {model : ModelEnvelope} {CutWitness : Type v}
    {cut : CutReceipt model CutWitness} {ReflectionWitness : Type w}
    {reflection : ReflectionReceipt cut ReflectionWitness}
    {OrientationState : Type u} {TurnWitness : Type v}
    {turn : TurnReceipt reflection OrientationState TurnWitness}
    {ReadoutWitness : Type w} {Side : Type u}
    (readable : ReadableReceipt turn ReadoutWitness Side) :
    readable.forgetTurn.forgetReflection.forgetCut = cut := rfl

/-! ### Licensed predecessor countermodels for T09 and T11 -/

def countermodelEnvelope : ModelEnvelope where
  Carrier := Unit
  inhabited := ⟨()⟩
  scopeId := 1
  entryCost := 0

def countermodelCut : CutReceipt countermodelEnvelope Unit where
  boundaryId := 1
  scopeId := 1
  witness := ()
  admissionBasisId := 1
  cost := 1

def countermodelReflection : ReflectionReceipt countermodelCut Unit where
  witness := ()
  ruleId := 1
  cost := 1

def countermodelTurn :
    TurnReceipt countermodelReflection Bool Unit where
  predecessor := false
  successor := true
  changed := by decide
  witness := ()
  actionId := 1
  cost := 1

/-- T09 countermodel: a valid nonidentity turn is inhabited. -/
theorem turnCountermodelIsInhabited :
    Nonempty (TurnReceipt countermodelReflection Bool Unit) :=
  ⟨countermodelTurn⟩

/--
T09 countermodel to a generic turn-to-A1 implication: the turn is inhabited
while the selected readout-witness type is empty.
-/
theorem thetaDoesNotProvideReadable :
    IsEmpty (ReadableReceipt countermodelTurn Empty Bool) :=
  ⟨fun receipt => nomatch receipt.witness⟩

def countermodelReadable : ReadableReceipt countermodelTurn Unit Bool where
  witness := ()
  negativeSide := false
  positiveSide := true
  separated := by decide
  tolerance := 0
  residualId := 7
  provenanceId := 11

/-- T11 countermodel: A1 does not supply A2's recovery witness. -/
theorem readableDoesNotProvideTrace :
    IsEmpty (TraceReceipt countermodelReadable Empty Nat) :=
  ⟨fun receipt => nomatch receipt.witness⟩

/-! ## T14: bounded predecessor strictness for A1-A15 -/

/-- The one new mechanical capability named by each extension card. -/
inductive Capability where
  | readable
  | recoverable
  | relation
  | transport
  | feedback
  | organization
  | access
  | response
  | taskCenter
  | comparison
  | couplingOrJointness
  | reentry
  | cadence
  | slack
  | closure
  deriving DecidableEq, Repr

/-- Spine order A1 through A15, used only by the bounded strictness model. -/
def Capability.rank : Capability -> Nat
  | .readable => 1
  | .recoverable => 2
  | .relation => 3
  | .transport => 4
  | .feedback => 5
  | .organization => 6
  | .access => 7
  | .response => 8
  | .taskCenter => 9
  | .comparison => 10
  | .couplingOrJointness => 11
  | .reentry => 12
  | .cadence => 13
  | .slack => 14
  | .closure => 15

/-- A capability view; it does not identify the full content of any PAL card. -/
structure CapabilityState where
  earned : Capability -> Prop

/-- The canonical predecessor view contains exactly the earlier capabilities. -/
def predecessorState (target : Capability) : CapabilityState where
  earned candidate := candidate.rank < target.rank

/--
A bounded extension carries its predecessor and one separately supplied witness
for the named capability. The structure has no default witness constructor.
-/
structure LayerExtension (target : Capability) (NewCapabilityWitness : Type u) where
  predecessor : CapabilityState
  predecessorIsCanonical : predecessor = predecessorState target
  witness : NewCapabilityWitness

/-- T15 coverage: no layer extension exists with an empty capability witness type. -/
theorem noLayerExtensionWithoutWitness (target : Capability) :
    IsEmpty (LayerExtension target NoWitness) :=
  ⟨fun extension => nomatch extension.witness⟩

/-- The extension adds only its target capability to the predecessor view. -/
def LayerExtension.extendedState {target : Capability} {NewCapabilityWitness : Type u}
    (extension : LayerExtension target NewCapabilityWitness) : CapabilityState where
  earned candidate := extension.predecessor.earned candidate ∨ candidate = target

/-- Forgetting the new witness returns the inherited state unchanged. -/
def LayerExtension.forget {target : Capability} {NewCapabilityWitness : Type u}
    (extension : LayerExtension target NewCapabilityWitness) : CapabilityState :=
  extension.predecessor

/-- A canonical bounded extension exists only when its witness is externally supplied. -/
def suppliedExtension (target : Capability) {NewCapabilityWitness : Type u}
    (witness : NewCapabilityWitness) : LayerExtension target NewCapabilityWitness where
  predecessor := predecessorState target
  predecessorIsCanonical := rfl
  witness := witness

/-- T14: every A1-A15 predecessor view lacks its named new capability. -/
theorem predecessorLacksNewCapability (target : Capability) :
    ¬((predecessorState target).earned target) :=
  Nat.lt_irrefl target.rank

/-- T14: the bounded extension supplies the named new capability. -/
theorem extensionAddsNewCapability
    {target : Capability} {NewCapabilityWitness : Type u}
    (extension : LayerExtension target NewCapabilityWitness) :
    (extension.extendedState.earned target) :=
  Or.inr rfl

/-- T14: every inherited capability remains present after extension. -/
theorem extensionPreservesInheritedCapability
    {target : Capability} {NewCapabilityWitness : Type u}
    (extension : LayerExtension target NewCapabilityWitness) (candidate : Capability)
    (inherited : extension.predecessor.earned candidate) :
    extension.extendedState.earned candidate :=
  Or.inl inherited

/--
T14 bounded countermodel family: for every A1-A15 capability, an externally
supplied witness yields an inherited state lacking it and a preserving extension
that adds it. This theorem does not manufacture the witness.
-/
theorem allLayersHaveStrictPredecessor
    (target : Capability) {NewCapabilityWitness : Type u}
    (witness : NewCapabilityWitness) :
    ∃ extension : LayerExtension target NewCapabilityWitness,
      ¬(extension.predecessor.earned target) ∧
      extension.extendedState.earned target ∧
      extension.forget = predecessorState target := by
  refine ⟨suppliedExtension target witness, ?_, extensionAddsNewCapability _, rfl⟩
  exact predecessorLacksNewCapability target

/-! ## T16: protected trace recovery through a bounded route -/

/-- The protected A1/A2 data that later receipts must not rewrite. -/
structure ProtectedTrace where
  boundaryId : Nat
  orientationId : Nat
  tolerance : Nat
  residualId : Nat
  provenanceId : Nat
  occurrenceId : Nat
  deriving DecidableEq, Repr

structure RelationStage (Witness : Type u) where
  trace : ProtectedTrace
  witness : Witness

/-- T15 coverage: the modeled trace route cannot begin without its witness. -/
theorem noRelationStageWithoutWitness : IsEmpty (RelationStage NoWitness) :=
  ⟨fun stage => nomatch stage.witness⟩

structure TransportStage (Witness : Type u) where
  prior : RelationStage Witness
  transportId : Nat

structure AccessStage (Witness : Type u) where
  prior : TransportStage Witness
  accessId : Nat

structure InterpretationStage (Witness : Type u) where
  prior : AccessStage Witness
  interpretationId : Nat

structure ClosureStage (Witness : Type u) where
  prior : InterpretationStage Witness
  closureId : Nat

def walkTraceRoute {Witness : Type u} (trace : ProtectedTrace)
    (witness : Witness) (transportId accessId interpretationId closureId : Nat) :
    ClosureStage Witness :=
  { prior :=
      { prior :=
          { prior :=
              { prior := { trace := trace, witness := witness }
                transportId := transportId }
            accessId := accessId }
        interpretationId := interpretationId }
    closureId := closureId }

def ClosureStage.recoverProtected {Witness : Type u}
    (receipt : ClosureStage Witness) : ProtectedTrace :=
  receipt.prior.prior.prior.prior.trace

/--
T16 bounded realization: relation, transport, access, interpretation, and
closure retain the exact protected trace, including original tolerance and
residual identifiers.
-/
@[simp] theorem routePreservesProtectedTrace {Witness : Type u}
    (trace : ProtectedTrace) (witness : Witness)
    (transportId accessId interpretationId closureId : Nat) :
    (walkTraceRoute trace witness transportId accessId interpretationId closureId).recoverProtected =
      trace := rfl

/-- Authorized compression must carry an exact restoration receipt. -/
structure RestorationReceipt (Original : Type u) (Compressed : Type v) where
  compress : Original -> Compressed
  restore : Compressed -> Original
  restores : ∀ original, restore (compress original) = original

/-- T16: a declared restoration receipt recovers its original input. -/
theorem authorizedCompressionRestores
    {Original : Type u} {Compressed : Type v}
    (receipt : RestorationReceipt Original Compressed) (original : Original) :
    receipt.restore (receipt.compress original) = original :=
  receipt.restores original

/-! ## T17: no authority backflow -/

/-- Earlier authority-relevant fields protected from later promotion. -/
structure AuthoritySnapshot where
  identityId : Nat
  evidenceId : Nat
  consentRecorded : Bool
  standingRecorded : Bool
  uncertaintyId : Nat
  authorityId : Nat
  deriving DecidableEq, Repr

/-- Later result kinds remain typed and do not coerce into earlier authority. -/
inductive LaterKind where
  | proof
  | prediction
  | ethicsReview
  | interpretation
  deriving DecidableEq, Repr

/-- A later result appends beside an unchanged earlier snapshot. -/
structure LaterReceipt where
  prior : AuthoritySnapshot
  kind : LaterKind
  resultId : Nat

def appendLaterResult (prior : AuthoritySnapshot) (kind : LaterKind)
    (resultId : Nat) : LaterReceipt :=
  { prior := prior, kind := kind, resultId := resultId }

/--
T17 bounded realization: proof, prediction, ethical review, or interpretation
adds a receipt without rewriting earlier identity, evidence, consent, standing,
uncertainty, or authority.
-/
@[simp] theorem noAuthorityBackflow (prior : AuthoritySnapshot)
    (kind : LaterKind) (resultId : Nat) :
    (appendLaterResult prior kind resultId).prior = prior := rfl

end PAL.AttackRun0001
