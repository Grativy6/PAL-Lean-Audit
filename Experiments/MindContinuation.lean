import Mathlib.Data.List.Basic

/-!
# MIND v0.4 bounded continuation experiment

A finite deterministic evidence queue is processed under an explicit rule and
fuel budget. A checkpoint protects the declared Work record and its source
context; restoration checks the supplied current context and takes fresh fuel
and administrative state. This reduced model does not represent authority,
full MIND, scheduler fairness, or empirical understanding.
-/
namespace Experiments.MindContinuation

/-- One already-admitted event has a supplied identifier and Boolean content value. -/
structure Evidence where
  id : Nat
  value : Bool
  deriving DecidableEq, Repr

/-- A retained transition receipt records the count before/after and its input and rule. -/
structure Receipt where
  before : Nat
  event : Evidence
  rule : Bool
  after : Nat
  deriving DecidableEq, Repr

/-- Receipt arithmetic agrees with the model's deterministic acceptance rule. -/
def receiptConsistent (r : Receipt) : Prop :=
  r.after = if r.event.value = r.rule then r.before + 1 else r.before

/-- The protected substantive continuation: account, pending evidence, rule, and retained history. -/
structure Work where
  account : Nat
  pending : List Evidence
  rule : Bool
  receipts : List Receipt
  deriving DecidableEq, Repr

/-- Operational state adds a current fuel budget, context version, and administrative activity. -/
structure OperationalState where
  work : Work
  fuel : Nat
  context : Nat
  adminCount : Nat
  deriving DecidableEq, Repr

/-- A pure record checkpoint carries the declared Work record and its source context. -/
structure Capsule where
  work : Work
  sourceContext : Nat
  deriving DecidableEq, Repr

/-- Queue length is the operational progress coordinate; it is not knowledge growth. -/
def queueProgress (s : OperationalState) : Nat := s.work.pending.length

/-- Save the protected continuation and its context, excluding fuel and admin count. -/
def checkpoint (s : OperationalState) : Capsule :=
  ⟨s.work, s.context⟩

/-- Pure record restoration checks one supplied context dependency and takes new operational fields. -/
def restore (c : Capsule) (currentContext freshFuel freshAdmin : Nat) : Option OperationalState :=
  if c.sourceContext = currentContext then
    some ⟨c.work, freshFuel, currentContext, freshAdmin⟩
  else
    none

/-- Process one queue head when fuel is available; preserve the event receipt even on no account change. -/
def productiveStep (s : OperationalState) : Option OperationalState :=
  match s.fuel with
  | 0 => none
  | fuel + 1 =>
    match s.work.pending with
    | [] => none
    | event :: remaining =>
      let after := if event.value = s.work.rule then s.work.account + 1 else s.work.account
      let receipt : Receipt := ⟨s.work.account, event, s.work.rule, after⟩
      some ⟨⟨after, remaining, s.work.rule, s.work.receipts ++ [receipt]⟩,
        fuel, s.context, s.adminCount⟩

/-- One administrative stutter spends fuel and changes only the admin counter. -/
def adminStep (s : OperationalState) : Option OperationalState :=
  match s.fuel with
  | 0 => none
  | fuel + 1 => some ⟨s.work, fuel, s.context, s.adminCount + 1⟩

/-- Run productive processing for at most the supplied number of step attempts, with no admin interleaving. -/
def runProductive : Nat → OperationalState → OperationalState
  | 0, s => s
  | n + 1, s =>
    match productiveStep s with
    | none => s
    | some next => runProductive n next

/-- A run with no available productive step leaves its state unchanged for any step bound. -/
theorem runProductive_stable (s : OperationalState) (n : Nat)
    (hstep : productiveStep s = none) : runProductive n s = s := by
  induction n with
  | zero => rfl
  | succ n ih => simp [runProductive, hstep]

/-- Consecutive bounded productive runs compose, including early termination when no step is available. -/
theorem runProductive_add (k n : Nat) (s : OperationalState) :
    runProductive (k + n) s = runProductive n (runProductive k s) := by
  induction k generalizing s with
  | zero => simp [runProductive]
  | succ k ih =>
      cases hstep : productiveStep s with
      | none =>
          simp only [Nat.succ_add, runProductive, hstep]
          rw [runProductive_stable s n hstep]
      | some next =>
          rw [Nat.succ_add, runProductive, hstep, runProductive, hstep]
          exact ih next

/-- A successful administrative step preserves the complete protected Work record. -/
theorem adminStep_preserves_work {s next : OperationalState}
    (h : adminStep s = some next) : next.work = s.work := by
  cases hfuel : s.fuel with
  | zero => simp [adminStep, hfuel] at h
  | succ n =>
    simp [adminStep, hfuel] at h
    cases h
    rfl

/-- Thus administrative stuttering also preserves the queue-progress coordinate. -/
theorem adminStep_preserves_queueProgress {s next : OperationalState}
    (h : adminStep s = some next) : queueProgress next = queueProgress s := by
  unfold queueProgress
  rw [adminStep_preserves_work h]

/-- Every successful productive step consumes one unit of fuel. -/
theorem productiveStep_consumes_fuel {s next : OperationalState}
    (h : productiveStep s = some next) : next.fuel + 1 = s.fuel := by
  cases hfuel : s.fuel with
  | zero => simp [productiveStep, hfuel] at h
  | succ n =>
    cases hpending : s.work.pending with
    | nil => simp [productiveStep, hfuel, hpending] at h
    | cons event remaining =>
      simp [productiveStep, hfuel, hpending] at h
      cases h
      rfl

/-- Every successful productive step removes exactly one pending event. -/
theorem productiveStep_decreases_queueProgress {s next : OperationalState}
    (h : productiveStep s = some next) : queueProgress next + 1 = queueProgress s := by
  cases hfuel : s.fuel with
  | zero => simp [productiveStep, hfuel] at h
  | succ n =>
    cases hpending : s.work.pending with
    | nil => simp [productiveStep, hfuel, hpending] at h
    | cons event remaining =>
      simp [productiveStep, hfuel, hpending] at h
      cases h
      simp [queueProgress, hpending]

/-- A successful step appends one attributable receipt with the processed event and count transition. -/
theorem productiveStep_retains_receipt {s next : OperationalState}
    (h : productiveStep s = some next) :
    ∃ event remaining receipt,
      s.work.pending = event :: remaining ∧
      next.work.pending = remaining ∧
      next.work.receipts = s.work.receipts ++ [receipt] ∧
      receipt.before = s.work.account ∧ receipt.event = event ∧
      receipt.rule = s.work.rule ∧ receipt.after = next.work.account ∧
      receiptConsistent receipt := by
  cases hfuel : s.fuel with
  | zero => simp [productiveStep, hfuel] at h
  | succ n =>
    cases hpending : s.work.pending with
    | nil => simp [productiveStep, hfuel, hpending] at h
    | cons event remaining =>
      simp [productiveStep, hfuel, hpending] at h
      cases h
      refine ⟨event, remaining, ⟨s.work.account, event, s.work.rule,
        if event.value = s.work.rule then s.work.account + 1 else s.work.account⟩,
        rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

/-- Under adequate fuel and step bound, deterministic productive processing empties the queue. -/
theorem runProductive_completes_aux (n : Nat) (s : OperationalState)
    (hbound : s.work.pending.length ≤ n) (hfuel : s.fuel ≥ s.work.pending.length) :
    (runProductive n s).work.pending = [] := by
  induction n generalizing s with
  | zero =>
    cases hpending : s.work.pending with
    | nil => exact hpending
    | cons event remaining => simp [hpending] at hbound
  | succ n ih =>
    cases hpending : s.work.pending with
    | nil =>
      cases hf : s.fuel <;> simp [runProductive, productiveStep, hpending, hf]
    | cons event remaining =>
      have hbound' : Nat.succ remaining.length ≤ Nat.succ n := by
        simpa [hpending, List.length_cons] using hbound
      have hremaining : remaining.length ≤ n :=
        Nat.le_of_succ_le_succ (by simpa using hbound')
      cases hf : s.fuel with
      | zero =>
        have hfalse : False := by
          simp [hpending, hf] at hfuel
        exact hfalse.elim
      | succ fuel =>
        have hfuel' : remaining.length ≤ fuel := by
          apply Nat.le_of_succ_le_succ
          simpa [hpending, hf, List.length_cons] using hfuel
        let after := if event.value = s.work.rule then s.work.account + 1 else s.work.account
        let receipt : Receipt := ⟨s.work.account, event, s.work.rule, after⟩
        let next : OperationalState :=
          ⟨⟨after, remaining, s.work.rule, s.work.receipts ++ [receipt]⟩,
            fuel, s.context, s.adminCount⟩
        have hstep : productiveStep s = some next := by
          simp [productiveStep, hpending, hf, next, receipt, after]
        have hnext : next.work.pending.length ≤ n := by
          simpa [next] using hremaining
        have hnextFuel : next.fuel ≥ next.work.pending.length := by
          simpa [next] using hfuel'
        rw [runProductive, hstep]
        exact ih next hnext hnextFuel

/-- Two runs from the same protected Work agree when each has enough fuel to process its queue. -/
theorem runProductive_work_independent_aux (n : Nat) (s t : OperationalState)
    (hwork : s.work = t.work) (hlen : s.work.pending.length ≤ n)
    (hfuelS : s.fuel ≥ s.work.pending.length)
    (hfuelT : t.fuel ≥ t.work.pending.length) :
    (runProductive n s).work = (runProductive n t).work := by
  induction n generalizing s t with
  | zero =>
      cases hpending : s.work.pending with
      | nil =>
          have ht : t.work.pending = [] := by simpa [hwork] using hpending
          simpa [runProductive, hpending, ht] using hwork
      | cons e rest => simp [hpending, List.length_cons] at hlen
  | succ n ih =>
      cases hpending : s.work.pending with
      | nil =>
          have ht : t.work.pending = [] := by simpa [hwork] using hpending
          cases hsFuel : s.fuel <;> cases htFuel : t.fuel <;>
            simp [runProductive, productiveStep, hpending, ht, hsFuel, htFuel]
          all_goals exact hwork
      | cons event remaining =>
          have htPending : t.work.pending = event :: remaining := by
            simpa [hwork] using hpending
          have hlen' : remaining.length ≤ n := by
            apply Nat.le_of_succ_le_succ
            simpa [hpending, List.length_cons] using hlen
          cases hsFuel : s.fuel with
          | zero => simp [hsFuel, hpending, List.length_cons] at hfuelS
          | succ fuelS =>
              cases htFuel : t.fuel with
              | zero => simp [htFuel, htPending, List.length_cons] at hfuelT
              | succ fuelT =>
                  have hfuelS' : remaining.length ≤ fuelS := by
                    apply Nat.le_of_succ_le_succ
                    simpa [hsFuel, hpending, List.length_cons] using hfuelS
                  have hfuelT' : remaining.length ≤ fuelT := by
                    apply Nat.le_of_succ_le_succ
                    simpa [htFuel, htPending, hwork, List.length_cons] using hfuelT
                  let after := if event.value = s.work.rule then s.work.account + 1 else s.work.account
                  let receipt : Receipt := ⟨s.work.account, event, s.work.rule, after⟩
                  let nextS : OperationalState :=
                    ⟨⟨after, remaining, s.work.rule, s.work.receipts ++ [receipt]⟩,
                      fuelS, s.context, s.adminCount⟩
                  let nextT : OperationalState :=
                    ⟨⟨after, remaining, s.work.rule, s.work.receipts ++ [receipt]⟩,
                      fuelT, t.context, t.adminCount⟩
                  have hstepS : productiveStep s = some nextS := by
                    simp [productiveStep, hsFuel, hpending, nextS, after, receipt]
                  have hstepT : productiveStep t = some nextT := by
                    simp [productiveStep, htFuel, htPending, hwork, nextT, after, receipt]
                  have hnextWork : nextS.work = nextT.work := by rfl
                  have hnextS : nextS.work.pending.length ≤ n := by
                    simpa [nextS] using hlen'
                  have hnextFuelS : nextS.fuel ≥ nextS.work.pending.length := by
                    simpa [nextS] using hfuelS'
                  have hnextFuelT : nextT.fuel ≥ nextT.work.pending.length := by
                    simpa [nextT] using hfuelT'
                  rw [runProductive, hstepS, runProductive, hstepT]
                  exact ih nextS nextT hnextWork hnextS hnextFuelS hnextFuelT

/-- Productive processing retains adequate fuel relative to the remaining queue. -/
theorem runProductive_preserves_sufficient_fuel (k : Nat) (s : OperationalState)
    (hfuel : s.fuel ≥ s.work.pending.length) :
    (runProductive k s).fuel ≥ (runProductive k s).work.pending.length := by
  induction k generalizing s with
  | zero => simpa [runProductive] using hfuel
  | succ k ih =>
      cases hstep : productiveStep s with
      | none => simpa [runProductive, hstep] using hfuel
      | some next =>
          have hnextFuel : next.fuel ≥ next.work.pending.length := by
            apply Nat.le_of_succ_le_succ
            calc
              Nat.succ next.work.pending.length = s.work.pending.length := by
                simpa [queueProgress] using (productiveStep_decreases_queueProgress hstep)
              _ ≤ s.fuel := hfuel
              _ = Nat.succ next.fuel := by
                simpa using (productiveStep_consumes_fuel hstep).symm
          rw [runProductive, hstep]
          exact ih next hnextFuel

/-- The explicit run bound equal to the initial queue length suffices when fuel covers it. -/
theorem runProductive_completes (s : OperationalState)
    (hfuel : s.fuel ≥ s.work.pending.length) :
    (runProductive s.work.pending.length s).work.pending = [] := by
  exact runProductive_completes_aux s.work.pending.length s (Nat.le_refl _) hfuel

/-- A matching checkpoint restores identical Work while using the caller's fresh fuel/admin values. -/
theorem checkpoint_restore_matching_context (s : OperationalState) (freshFuel freshAdmin : Nat) :
    restore (checkpoint s) s.context freshFuel freshAdmin =
      some ⟨s.work, freshFuel, s.context, freshAdmin⟩ := by
  simp [restore, checkpoint]

/-- A checkpoint rejects restoration under a different current context. -/
theorem checkpoint_restore_rejects_context_mismatch (s : OperationalState)
    (currentContext freshFuel freshAdmin : Nat) (h : s.context ≠ currentContext) :
    restore (checkpoint s) currentContext freshFuel freshAdmin = none := by
  simp [restore, checkpoint, h]

/-- Checkpoint then context-valid restore preserves the whole bounded continuation result when both runs have sufficient fuel. -/
theorem checkpoint_resume_preserves_continuation (s : OperationalState)
    (freshFuel freshAdmin : Nat) (hfuel : s.fuel ≥ s.work.pending.length)
    (hfresh : freshFuel ≥ s.work.pending.length) :
    (runProductive s.work.pending.length s).work.pending = [] ∧
      (restore (checkpoint s) s.context freshFuel freshAdmin).map
        (fun resumed => (runProductive s.work.pending.length resumed).work) =
        some (runProductive s.work.pending.length s).work := by
  constructor
  · exact runProductive_completes s hfuel
  · rw [checkpoint_restore_matching_context]
    simp only [Option.map_some]
    apply congrArg some
    exact (runProductive_work_independent_aux s.work.pending.length s
      ⟨s.work, freshFuel, s.context, freshAdmin⟩ rfl (Nat.le_refl _)
      hfuel hfresh).symm

/-- A checkpoint after any bounded prefix resumes to the uninterrupted final Work when both budgets suffice. -/
theorem prefix_checkpoint_resume (k : Nat) (s : OperationalState)
    (freshFuel freshAdmin : Nat) (horiginal : s.fuel ≥ s.work.pending.length)
    (hfresh : freshFuel ≥ (runProductive k s).work.pending.length) :
    let mid := runProductive k s
    let n := mid.work.pending.length
    (runProductive (k + n) s).work.pending = [] ∧
      (restore (checkpoint mid) mid.context freshFuel freshAdmin).map
        (fun resumed => (runProductive n resumed).work) =
        some (runProductive (k + n) s).work := by
  dsimp
  let mid := runProductive k s
  let n := mid.work.pending.length
  have hmidFuel : mid.fuel ≥ mid.work.pending.length := by
    exact runProductive_preserves_sufficient_fuel k s horiginal
  have hcontinued : runProductive (k + n) s = runProductive n mid := by
    simpa [mid, n] using runProductive_add k n s
  constructor
  · rw [hcontinued]
    exact runProductive_completes mid hmidFuel
  · rw [checkpoint_restore_matching_context]
    simp only [Option.map_some]
    have hwork : (runProductive n
        ⟨mid.work, freshFuel, mid.context, freshAdmin⟩).work =
        (runProductive n mid).work := by
      exact (runProductive_work_independent_aux n mid
        ⟨mid.work, freshFuel, mid.context, freshAdmin⟩ rfl (Nat.le_refl _)
        hmidFuel hfresh).symm
    rw [hcontinued]
    exact congrArg some hwork

/-- A mismatching event leaves the account unchanged but is removed and retained in history. -/
theorem nonmatching_evidence_fixture :
    let start : OperationalState :=
      ⟨⟨4, [⟨7, false⟩], true, []⟩, 1, 3, 0⟩
    productiveStep start =
      some ⟨⟨4, [], true, [⟨4, ⟨7, false⟩, true, 4⟩]⟩, 0, 3, 0⟩ := by
  rfl

/-- A receipt claiming no increment for a matching event fails the declared update rule. -/
theorem inconsistent_receipt_delta_fixture :
    let impossible : Receipt := ⟨4, ⟨7, true⟩, true, 4⟩
    ¬ receiptConsistent impossible := by
  simp [receiptConsistent]

/-- Same account and pending event, different rule: continuation outcomes differ. -/
theorem dropping_rule_changes_continuation_fixture :
    let matching : OperationalState := ⟨⟨0, [⟨1, true⟩], true, []⟩, 1, 5, 0⟩
    let nonmatching : OperationalState := ⟨⟨0, [⟨1, true⟩], false, []⟩, 1, 5, 0⟩
    matching.work.account = nonmatching.work.account ∧
      matching.work.pending = nonmatching.work.pending ∧
      (runProductive 1 matching).work.account = 1 ∧
      (runProductive 1 nonmatching).work.account = 0 := by
  decide

/-- An account-only summary merges works whose pending evidence yields different continuations. -/
theorem dropping_pending_from_capsule_changes_continuation_fixture :
    let pending : OperationalState := ⟨⟨0, [⟨2, true⟩], true, []⟩, 1, 4, 0⟩
    let empty : OperationalState := ⟨⟨0, [], true, []⟩, 1, 4, 0⟩
    pending.work.account = empty.work.account ∧
      (runProductive 1 pending).work.account = 1 ∧
      (runProductive 1 empty).work.account = 0 := by
  decide

/-- Equal capsules can arise from operational states with distinct fuel and admin history. -/
theorem capsule_omits_operational_state_fixture :
    let work : Work := ⟨2, [⟨3, true⟩], true, []⟩
    let first : OperationalState := ⟨work, 1, 10, 0⟩
    let second : OperationalState := ⟨work, 8, 10, 5⟩
    checkpoint first = checkpoint second ∧ first ≠ second := by
  decide

/-- A concrete old context cannot restore a checkpoint into a changed current context. -/
theorem stale_context_rejected_fixture :
    let start : OperationalState := ⟨⟨2, [], true, []⟩, 6, 10, 3⟩
    restore (checkpoint start) 11 6 3 = none := by
  decide

/-- One admin step can spend the last fuel and leave productive evidence unprocessed. -/
theorem admin_exhausts_fuel_and_starves_fixture :
    let start : OperationalState := ⟨⟨0, [⟨3, true⟩], true, []⟩, 1, 8, 0⟩
    ∃ afterAdmin,
      adminStep start = some afterAdmin ∧
      afterAdmin.work = start.work ∧ afterAdmin.fuel = 0 ∧
      productiveStep afterAdmin = none := by
  refine ⟨⟨⟨0, [⟨3, true⟩], true, []⟩, 0, 8, 1⟩, ?_, rfl, rfl, rfl⟩
  rfl

/-- Insufficient fuel for a two-event queue leaves a deterministic remainder. -/
theorem insufficient_fuel_leaves_pending_fixture :
    let start : OperationalState := ⟨⟨0, [⟨1, true⟩, ⟨2, true⟩], true, []⟩, 1, 2, 0⟩
    (runProductive 2 start).work.pending = [⟨2, true⟩] ∧
      (runProductive 2 start).work.account = 1 := by
  decide

end Experiments.MindContinuation
