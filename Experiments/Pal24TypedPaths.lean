import Mathlib.Data.List.Basic

/-! Reduced typed directed-path realization for PAL v2.3-M P0627--P0641. -/
namespace Experiments.Pal24TypedPaths

inductive Vertex where | a | b | c deriving DecidableEq, Repr
inductive RelationKind where | link | support deriving DecidableEq, Repr
inductive EvidenceKind where | receipt | unverified deriving DecidableEq, Repr

structure Edge where
  source : Vertex
  target : Vertex
  relation : RelationKind
  evidence : EvidenceKind
  deriving DecidableEq, Repr

structure PathRecord where
  start : Vertex
  finish : Vertex
  edges : List Edge
  deriving Repr

def follow : Vertex → List Edge → Option Vertex
  | current, [] => some current
  | current, edge :: rest =>
      if edge.source = current ∧ edge.evidence = .receipt then follow edge.target rest else none

def pathValid (path : PathRecord) : Prop :=
  follow path.start path.edges = some path.finish

def checkedAppend (path : PathRecord) (edge : Edge) : Option PathRecord :=
  if follow path.start path.edges = some path.finish then
    if edge.source = path.finish ∧ edge.evidence = .receipt then
      some { start := path.start, finish := edge.target, edges := path.edges ++ [edge] }
    else none
  else none

def deleteLastEdges (path : PathRecord) : List Edge :=
  path.edges.dropLast

def coOccur (roster : List Vertex) (left right : Vertex) : Prop :=
  left ∈ roster ∧ right ∈ roster

def noEdgeBetween (edges : List Edge) (left right : Vertex) : Prop :=
  ∀ edge, edge ∈ edges → ¬ (edge.source = left ∧ edge.target = right)

theorem follow_append_edge (start middle : Vertex) (edges : List Edge) (edge : Edge)
    (hfollow : follow start edges = some middle)
    (hsource : edge.source = middle) (hevidence : edge.evidence = .receipt) :
    follow start (edges ++ [edge]) = some edge.target := by
  induction edges generalizing start with
  | nil =>
      simp [follow] at hfollow
      subst middle
      simp [follow, hevidence, hfollow.symm]
  | cons head tail ih =>
      by_cases hhead : head.source = start ∧ head.evidence = .receipt
      · simp [follow, hhead] at hfollow ⊢
        exact ih head.target hfollow
      · simp [follow, hhead] at hfollow

theorem checkedAppend_valid (path : PathRecord) (edge : Edge) (result : PathRecord)
    (happend : checkedAppend path edge = some result) :
    pathValid result := by
  unfold checkedAppend at happend
  split at happend
  · rename_i hvalid
    split at happend
    · rename_i hcheck
      injection happend with hresult
      subst result
      exact follow_append_edge path.start path.finish path.edges edge hvalid hcheck.1 hcheck.2
    · simp at happend
  · simp at happend

theorem delete_appended_edge_recovers_predecessor (edges : List Edge) (edge : Edge) :
    (edges ++ [edge]).dropLast = edges := by
  simp

def ab : Edge := { source := .a, target := .b, relation := .link, evidence := .receipt }
def bc : Edge := { source := .b, target := .c, relation := .support, evidence := .receipt }
def wrongEndpoint : Edge := { source := .a, target := .c, relation := .link, evidence := .receipt }
def wrongEvidence : Edge := { source := .b, target := .c, relation := .link, evidence := .unverified }
def emptyAtA : PathRecord := { start := .a, finish := .a, edges := [] }
def pathAB : PathRecord := { start := .a, finish := .b, edges := [ab] }
def malformedAtB : PathRecord := { start := .a, finish := .b, edges := [] }
def cooccurringRoster : List Vertex := [.a, .b]
def noEdges : List Edge := []

theorem empty_path_valid : pathValid emptyAtA := by rfl

theorem append_ab_creates_valid_path :
    checkedAppend emptyAtA ab = some pathAB ∧ pathValid pathAB := by
  have happend : checkedAppend emptyAtA ab = some pathAB := by
    simp [checkedAppend, follow, emptyAtA, pathAB, ab]
  exact ⟨happend, checkedAppend_valid emptyAtA ab pathAB happend⟩

theorem append_bc_preserves_ordered_history :
    ∃ result, checkedAppend pathAB bc = some result ∧ pathValid result ∧ result.edges = [ab, bc] := by
  let result : PathRecord := { start := .a, finish := .c, edges := [ab, bc] }
  have happend : checkedAppend pathAB bc = some result := by
    simp [result, checkedAppend, follow, pathAB, ab, bc]
  refine ⟨result, happend, checkedAppend_valid pathAB bc result happend, rfl⟩

theorem mismatched_endpoint_rejected : checkedAppend pathAB wrongEndpoint = none := by
  simp [checkedAppend, follow, pathAB, ab, wrongEndpoint]

theorem unverified_evidence_rejected : checkedAppend pathAB wrongEvidence = none := by
  simp [checkedAppend, follow, pathAB, ab, wrongEvidence]

theorem malformed_prefix_rejected : checkedAppend malformedAtB bc = none := by
  simp [checkedAppend, follow, malformedAtB]

theorem cooccurrence_without_edge_countermodel :
    coOccur cooccurringRoster .a .b ∧ noEdgeBetween noEdges .a .b := by
  constructor
  · simp [coOccur, cooccurringRoster]
  · intro edge h
    simp [noEdges] at h

end Experiments.Pal24TypedPaths
