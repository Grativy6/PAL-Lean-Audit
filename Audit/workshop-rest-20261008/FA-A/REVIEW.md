# FA-A self-review

Primary verdict: **proved for the explicitly labeled coverage/quantifier controls**. These are models illustrating the synthesis's distinctions, not formalization of RH or the definitions of P and NP. Eleven declarations include ten theorems and one record constructor function. Build, exact statement/axiom inspection, bundled kernel replay and saved receipt validation passed.

Both a finite prefix and an arbitrary finite tested subset of natural numbers admit a predicate which holds on every tested case and fails outside it. No inference is made about an arbitrary specific predicate with an independent coverage theorem. The positive induction proves the sum of the first n odd numbers is n^2 for all natural n.

The quantifier control is (forall n, exists b, n<b) versus (exists b, forall n, n<b). It concerns a single bound; the same relation has an explicit uniform witness function n+1. The audit does not incorrectly deny choice functions or infer computational complexity from this elementary distinction.

The min(n,N) interface has a supplied requested answer n and an actual collision between N and N+1. Only then is the existing reachable-fiber criterion applied to block exact identity recovery. That criterion is reused from AbstractLoopsJoint, with the same domain/map mechanism as APCI; it is not an independently rediscovered theorem. AbstractLoopsFiniteImage.certification_capacity remains the existing finite-capacity receipt, not a new count in this batch.

A unary List Unit record of length n is finite for each n, injective over all natural n, and has no uniform length bound. An explicit reachable decoder returns its length. This formalizes why variable-length carriers cannot be treated as one fixed finite-capacity alphabet without an additional premise.

No manuscript correction surfaced. The paper already states these distinctions at P0009-P0025 and disclaims a reduction, solution, impossibility or independence claim at P0033-P0037. This is self-review; only standard Lean axioms occur. No philosophical paragraph was given an artificial PROVED label.
