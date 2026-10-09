# C6 independent review — task-relative history quotient

**Normalized claim:** For histories represented by all finite lists over an arbitrary supplied alphabet, with all finite lists admissible as continuations and a total deterministic observation `observe`, define `h ~ h'` iff every finite common suffix yields equal observations. This relation is an equivalence and a right congruence; the current observation is well-defined on its quotient. Under a restricted suffix predicate, right congruence is proved only with explicit prefix-closure under the newly appended symbol.

**Primary verdict: proved as written for the declared list model; the staged code and ledger are source-faithful within that scope.** I did not run Lean. One requested adversarial fixture is not present: the aperture theorem states the necessary closure premise, but the batch has no checked countercase showing failure when that premise is removed. I supply a minimal countercase below as a recommended addition, not as a defect in the conditional theorem.

## Dependency and mathematical checks

The unrestricted theorem at `artifacts/pal-v24-c6-staging/Experiments/Pal24HistoryQuotient.lean:37-42` has the correct right-congruence orientation. Given `h ~ h'`, for arbitrary resulting suffix `s`, the original hypothesis applies to `extension ++ s`; associativity identifies the observations of `(h ++ extension) ++ s` and `(h' ++ extension) ++ s`. This is exactly post-appending a shared continuation, not left congruence or an unproved closure assertion.

The equivalence laws at lines 17-34 are pointwise equality reflexivity, symmetry, and transitivity. `futureSetoid`, the quotient constructor, and the class equality characterization at lines 44-77 correctly package that relation. `quotientObservation` at lines 59-83 is well-defined because empty suffix is admitted, so future-equivalent histories agree on the current observation. This is only a quotient-descending current-observation function; it does not establish a reachable-image decoder with PAL's broader dependency or class-separation conditions. The notes and ledger expressly preserve that ceiling.

The aperture theorem at lines 85-107 has the correct closure direction: `aperture suffix → aperture (task :: suffix)`. That gives the original restricted-equivalence premise access to the shifted suffix needed to show equivalence after appending `task`. The premise is explicit and no universal closure is inferred for arbitrary apertures.

A small semantic countercase confirms why the premise matters. Let `Alphabet = Bool`, `aperture z := z = []`, `observe z := z = [false]`, `left := []`, `right := [true]`, and append `task := false`. Initially the restricted relation holds, since both observations at the only admitted suffix `[]` are false. But after appending `false`, the observations at suffix `[]` are `true` for `[false]` and `false` for `[true,false]`; right congruence fails. The aperture is not closed under prefixing `false`. This fixture is not in the staged declarations or ledger, so the comment at lines 91-95 is supported by direct reasoning but not by an included Lean countercase.

The task/usefulness fixtures are correctly scoped. `constantTask_one_class` and `constantTask_quotient_subsingleton` (lines 109-124) show the quotient can collapse all histories; since the history type is nonempty, “subsingleton” amounts to exactly one quotient class. Nothing in this proves useful work, and ledger/notes explicitly deny that inference. The `headTask` fixture distinguishes `[]` from `[false]` at the empty suffix (126-131); the task-mutation conjunction compares that same pair under two different observation functions (133-135). This shows quotient dependence on the supplied task semantics, not automatic task-version tracking or real task adequacy.

## Source correspondence and accounting

The C6 excerpts contain each cited paragraph P0807–P0821, and the local extracted Atlas text (`artifacts/pal-v23-charter-2026-09-07/sources/PAL_v2.3-M_Mathematical_Realization_Atlas.txt`) matches the operative formulations: P0809 defines equivalence by all continuations and P0817 warns that a one-class quotient still needs nontrivial work if usefulness is claimed. The implementation realizes those formulas with `List Alphabet`, list append, and a supplied total observation function. It is an abstract model of all finite lists/all finite continuations; it does not establish source adequacy, restricted history-indexed semantics, or Myhill–Nerode minimality. The staged notes and manual dispositions say so.

The inventory is internally complete for the Lean file: 18 declarations (7 definitions, 11 theorems) are represented in `claims.json`; the axioms file has an ordered `#check`/`#print axioms` pair for each declaration at lines 3-38. I have not independently checked those outputs. The ledger classifications total 9 `PROVED_FROM_DECLARED_RULES`, 5 `CONSISTENT_REALIZATION`, and 4 `COUNTERMODEL_TO_OVERCLAIM`; these fit the distinction between universal list-level facts and the finite Boolean illustrative/counter fixtures.

## Obligation status and remaining gap

- Unrestricted right congruence and quotient descent: **passed** under the stated all-finite-list continuation model.
- Restricted-aperture right congruence: **passed conditionally** on the exact displayed closure hypothesis.
- Why that aperture hypothesis is needed: **not addressed by a checked negative fixture**; the concrete countercase above is the smallest useful addition.
- Quotient minimality, reachable-image decoder/totalization/class separation, and actual task usefulness: **out of scope**, as disclosed.

The strongest warranted conclusion remains the generic right-congruence and quotient facts for this explicit list semantics, plus aperture right congruence only for apertures closed under prefixing the appended symbol. The cheapest strengthening of coverage is to add the Bool countercase above as a theorem asserting initial aperture-equivalence and failure after the append, then inventory it in `claims.json` and the axioms file. No change to the existing conditional theorem is needed.
## 2026-09-22 addendum — aperture-closure counterfixture

The promoted module now has 19 explicit declarations, including 12 theorems;
the C6 ledger inventories the same 19 declarations. This addendum reviews
only the added `aperture_closure_is_load_bearing` fixture requested by the
staged review, without repeating its general proof review.

The fixture corresponds to the source's explicit continuation-closure
requirement at Atlas P0813 and its aperture-stability test requirement at
P0821. Its aperture admits exactly the empty suffix. It therefore fails the
prefix-closure premise for `false`, because the empty suffix is admitted while
`false :: []` is not. For observation `history.length / 2`, histories `[]`
and `[false]` agree on the only admitted suffix: both observations are zero.
After appending the same `[false]`, the empty suffix still lies in the aperture,
but the histories `[false]` and `[false, false]` have observations zero and
one. Thus restricted future-equivalence is not right-congruent when the
closure premise is omitted.

Scoped pass for the added fixture. It closes the prior missing-countercase
suggestion and accurately preserves the ceiling: this finite Boolean/list
example does not challenge all-finite-suffix right congruence, establish
aperture closure for arbitrary tasks, or supply the source's decoder,
minimality, decidability, or usefulness claims.
