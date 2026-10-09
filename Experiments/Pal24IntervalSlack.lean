import Mathlib

/-!
# PAL v2.4 C2: interval slack classification

Exact rational realization of the v2.3 Atlas interval predicates. Validity
(order) and nonnegative tolerance are explicit theorem assumptions. Units,
measurement, evaluator correctness, grants, and authority are not modeled.
-/
namespace Experiments.Pal24IntervalSlack

/-- Source-named interval outcomes. -/
inductive SlackClass where
  | feasible
  | violated
  | contact
  | unresolved
  deriving DecidableEq, Repr

/-- A raw closed interval in one exact ordered scalar codomain. -/
structure SlackInterval where
  lower : ℚ
  upper : ℚ
  deriving DecidableEq, Repr

/-- Interval validity means its endpoints are ordered. -/
def validInterval (i : SlackInterval) : Prop := i.lower ≤ i.upper

/-- Negating a constraint interval reverses and negates its endpoints. -/
def constraintToSlack (constraint : SlackInterval) : SlackInterval :=
  ⟨-constraint.upper, -constraint.lower⟩

/-- The lower slack endpoint strictly clears the declared tolerance. -/
def feasible (tolerance : ℚ) (slack : SlackInterval) : Prop :=
  slack.lower > tolerance

/-- The upper slack endpoint lies strictly below negative tolerance. -/
def violated (tolerance : ℚ) (slack : SlackInterval) : Prop :=
  slack.upper < -tolerance

/-- The entire slack interval lies in the closed tolerance band. -/
def contact (tolerance : ℚ) (slack : SlackInterval) : Prop :=
  -tolerance ≤ slack.lower ∧ slack.upper ≤ tolerance

/-- Apply the Atlas predicates in order; the remaining case is UNRESOLVED. -/
noncomputable def classify (tolerance : ℚ) (slack : SlackInterval) : SlackClass := by
  classical
  exact if feasible tolerance slack then .feasible
    else if violated tolerance slack then .violated
    else if contact tolerance slack then .contact
    else .unresolved

/-- Negating an ordered constraint interval yields an ordered slack interval. -/
theorem constraintToSlack_valid (constraint : SlackInterval)
    (hValid : validInterval constraint) : validInterval (constraintToSlack constraint) := by
  dsimp [validInterval, constraintToSlack] at *
  linarith

/-- For valid input and nonnegative tolerance, feasible and violated are disjoint. -/
theorem feasible_not_violated (tolerance : ℚ) (slack : SlackInterval)
    (hTolerance : 0 ≤ tolerance) (hValid : validInterval slack) :
    ¬ (feasible tolerance slack ∧ violated tolerance slack) := by
  rintro ⟨hFeasible, hViolated⟩
  dsimp [feasible, violated, validInterval] at *
  linarith

/-- Ordered endpoints make feasible and contact disjoint. -/
theorem feasible_not_contact (tolerance : ℚ) (slack : SlackInterval)
    (hValid : validInterval slack) :
    ¬ (feasible tolerance slack ∧ contact tolerance slack) := by
  rintro ⟨hFeasible, hContact⟩
  dsimp [feasible, contact, validInterval] at *
  linarith

/-- Valid input and nonnegative tolerance make violated and contact disjoint. -/
theorem violated_not_contact (tolerance : ℚ) (slack : SlackInterval)
    (hValid : validInterval slack) :
    ¬ (violated tolerance slack ∧ contact tolerance slack) := by
  rintro ⟨hViolated, hContact⟩
  dsimp [violated, contact, validInterval] at *
  linarith

/-- The first classifier outcome is equivalent to the feasible predicate. -/
theorem feasible_iff_classified (tolerance : ℚ) (slack : SlackInterval) :
    classify tolerance slack = .feasible ↔ feasible tolerance slack := by
  constructor
  · intro hClass
    unfold classify at hClass
    split_ifs at hClass <;> simp_all
  · intro hFeasible
    simp [classify, hFeasible]

/-- The second classifier outcome is equivalent to the violated predicate. -/
theorem violated_iff_classified (tolerance : ℚ) (slack : SlackInterval)
    (hTolerance : 0 ≤ tolerance) (hValid : validInterval slack) :
    classify tolerance slack = .violated ↔ violated tolerance slack := by
  constructor
  · intro hClass
    unfold classify at hClass
    split_ifs at hClass <;> simp_all
  · intro hViolated
    by_cases hFeasible : feasible tolerance slack
    · exact False.elim ((feasible_not_violated tolerance slack hTolerance hValid) ⟨hFeasible, hViolated⟩)
    · simp [classify, hFeasible, hViolated]

/-- The third classifier outcome is equivalent to the contact predicate. -/
theorem contact_iff_classified (tolerance : ℚ) (slack : SlackInterval)
    (hValid : validInterval slack) :
    classify tolerance slack = .contact ↔ contact tolerance slack := by
  constructor
  · intro hClass
    unfold classify at hClass
    split_ifs at hClass <;> simp_all
  · intro hContact
    by_cases hFeasible : feasible tolerance slack
    · exact False.elim ((feasible_not_contact tolerance slack hValid) ⟨hFeasible, hContact⟩)
    · by_cases hViolated : violated tolerance slack
      · exact False.elim ((violated_not_contact tolerance slack hValid) ⟨hViolated, hContact⟩)
      · simp [classify, hFeasible, hViolated, hContact]

/-- UNRESOLVED is exactly the complement of the three source predicates, without input-validity assumptions. -/
theorem unresolved_iff_classified (tolerance : ℚ) (slack : SlackInterval) :
    classify tolerance slack = .unresolved ↔
      ¬ feasible tolerance slack ∧ ¬ violated tolerance slack ∧ ¬ contact tolerance slack := by
  constructor
  · intro hClass
    unfold classify at hClass
    split_ifs at hClass <;> simp_all
  · rintro ⟨hFeasible, hViolated, hContact⟩
    simp [classify, hFeasible, hViolated, hContact]

/-- On the declared valid domain, the three predicates are pairwise disjoint. -/
theorem source_regions_pairwise_disjoint (tolerance : ℚ) (slack : SlackInterval)
    (hTolerance : 0 ≤ tolerance) (hValid : validInterval slack) :
    ¬ (feasible tolerance slack ∧ violated tolerance slack) ∧
    ¬ (feasible tolerance slack ∧ contact tolerance slack) ∧
    ¬ (violated tolerance slack ∧ contact tolerance slack) := by
  exact ⟨feasible_not_violated tolerance slack hTolerance hValid,
    feasible_not_contact tolerance slack hValid,
    violated_not_contact tolerance slack hValid⟩

/-- Every raw interval is in one of the three source regions or their residual. -/
theorem source_regions_cover (tolerance : ℚ) (slack : SlackInterval) :
    feasible tolerance slack ∨ violated tolerance slack ∨ contact tolerance slack ∨
      (¬ feasible tolerance slack ∧ ¬ violated tolerance slack ∧ ¬ contact tolerance slack) := by
  by_cases hf : feasible tolerance slack
  · exact Or.inl hf
  · by_cases hv : violated tolerance slack
    · exact Or.inr (Or.inl hv)
    · by_cases hc : contact tolerance slack
      · exact Or.inr (Or.inr (Or.inl hc))
      · exact Or.inr (Or.inr (Or.inr ⟨hf, hv, hc⟩))

/-- The classifier always returns exactly one of four tags for every raw input. -/
theorem classification_total_exclusive (tolerance : ℚ) (slack : SlackInterval) :
    (classify tolerance slack = .feasible ∨ classify tolerance slack = .violated ∨
      classify tolerance slack = .contact ∨ classify tolerance slack = .unresolved) ∧
    ¬ (classify tolerance slack = .feasible ∧ classify tolerance slack = .violated) ∧
    ¬ (classify tolerance slack = .feasible ∧ classify tolerance slack = .contact) ∧
    ¬ (classify tolerance slack = .violated ∧ classify tolerance slack = .contact) := by
  constructor
  · cases classify tolerance slack <;> simp
  · refine ⟨?_, ?_, ?_⟩ <;> simp_all

/-- Endpoint equations for negating an interval. -/
theorem constraintToSlack_endpoints (constraint : SlackInterval) :
    (constraintToSlack constraint).lower = -constraint.upper ∧
      (constraintToSlack constraint).upper = -constraint.lower := by
  constructor <;> rfl

/-- The exact positive tolerance endpoint is CONTACT. -/
theorem positive_tolerance_boundary_is_contact (tolerance : ℚ)
    (hTolerance : 0 ≤ tolerance) :
    classify tolerance ⟨tolerance, tolerance⟩ = .contact := by
  apply (contact_iff_classified tolerance ⟨tolerance, tolerance⟩ (by simp [validInterval])).2
  constructor <;> dsimp [contact] <;> linarith

/-- The exact negative tolerance endpoint is CONTACT. -/
theorem negative_tolerance_boundary_is_contact (tolerance : ℚ)
    (hTolerance : 0 ≤ tolerance) :
    classify tolerance ⟨-tolerance, -tolerance⟩ = .contact := by
  apply (contact_iff_classified tolerance ⟨-tolerance, -tolerance⟩ (by simp [validInterval])).2
  constructor <;> dsimp [contact] <;> linarith

/-- A valid interval spanning beyond both sides of the tolerance band is UNRESOLVED. -/
theorem cross_regime_interval_is_unresolved :
    classify (1 : ℚ) ⟨-2, 2⟩ = .unresolved := by
  norm_num [classify, feasible, violated, contact]

/-- With positive tolerance and invalid endpoint order, the source regions overlap. -/
theorem invalid_interval_overlap_counterexample :
    validInterval ⟨2, -2⟩ = False ∧
    feasible (1 : ℚ) ⟨2, -2⟩ ∧ violated (1 : ℚ) ⟨2, -2⟩ ∧
    contact (1 : ℚ) ⟨2, -2⟩ := by
  norm_num [validInterval, feasible, violated, contact]

/-- Budget slack is budget minus cumulative consumption within the epoch. -/
def budgetSlack (budget cumulative : ℚ) : ℚ := budget - cumulative

/-- Nondecreasing consumption makes fixed-epoch budget slack nonincreasing. -/
theorem budget_slack_antitone (budget earlier later : ℚ)
    (hConsumption : earlier ≤ later) :
    budgetSlack budget later ≤ budgetSlack budget earlier := by
  dsimp [budgetSlack]
  linarith

end Experiments.Pal24IntervalSlack


