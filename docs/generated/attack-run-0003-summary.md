# Attack Run 0003 — PAL-led realization audit

PAL v2.1 audited the declared Lean realizations in this run. Lean did not redefine, adopt, or prove PAL.

- Controlling release: **PAL v2.1**
- DOI: [10.5281/zenodo.21864767](https://doi.org/10.5281/zenodo.21864767)
- Run status: **LOCAL_VALIDATION_PASSED_CI_PENDING**
- Authority ceiling: PAL v2.1 controls the distinctions, invariants, and conformance conditions. Lean checks only the declared objects and dependencies; it does not redefine, adopt, uniquely validate, or prove PAL and cannot close a PAL obligation.
- Exact formal-target source: `PAL/AttackRun0003.lean` at canonical-LF SHA-256 `0225fe8a13702e020ae368697937cfe373761888cbcdc257a19399f5a6e0c34f`.
- Exact negative-fixture identities: **4** path/hash/diagnostic receipts.
- Open burden: **D-FIRST-OCCURRENCE** remains one **OPEN** debt with **O04** and **O25** as two separately preserved **OPEN** interfaces.
- Terminology: “occurrence-closed, source-open” is explanatory shorthand, not a primitive or PAL status.

## Formal and control classifications (n=24)

| Classification | Count |
|---|---:|
| `PROVED_FROM_DECLARED_RULES` | 8 |
| `CONSISTENT_REALIZATION` | 2 |
| `ASSUMPTION_BOUND` | 2 |
| `COUNTERMODEL_TO_OVERCLAIM` | 9 |
| `EXPECTED_REJECTION` | 3 |

_These counts cover formal results and expected policy rejections only._

## Required overclaim controls (overlapping evidence; n=10)

| Control | Attempted overclaim | Disposition | Existing result evidence |
|---|---|---|---|
| `AR3-N01` | A0 is globally or causally first. | `COUNTERMODEL_TO_OVERCLAIM` | AR3-02 |
| `AR3-N02` | A recorded cost proves source, truth, energy, permission, consent, standing, or authority. | `COUNTERMODEL_TO_OVERCLAIM` | AR3-05 |
| `AR3-N03` | An A0 receipt alone proves occurrence closure. | `COUNTERMODEL_TO_OVERCLAIM` | AR3-09 |
| `AR3-N04` | A later witness retroactively creates an earlier witness or payment. | `PROVED_FROM_DECLARED_RULES` | AR3-20 |
| `AR3-N05` | A cut-only interface uniquely identifies its source without injectivity or discriminating evidence. | `COUNTERMODEL_TO_OVERCLAIM` | AR3-16; AR3-17 |
| `AR3-N06` | Asking or producing its receipt proves the inquirer’s ontology, consciousness, standing, ultimate source, or global priority, or witnesses the original cut’s causal source. | `COUNTERMODEL_TO_OVERCLAIM` | AR3-13; AR3-14 |
| `AR3-N07` | Reopenable inquiry proves an actually infinite causal ontology. | `COUNTERMODEL_TO_OVERCLAIM` | AR3-19 |
| `AR3-N08` | Appending evidence permits alteration of the earlier receipt or authority snapshot. | `COUNTERMODEL_TO_OVERCLAIM` | AR3-20; AR3-21 |
| `AR3-N09` | Occurrence-closed, source-open functions as a primitive PAL status. | `EXPECTED_REJECTION` | AR3-23; AR3-25 |
| `AR3-N10` | A formal proof closes O04, O25, or D-FIRST-OCCURRENCE. | `EXPECTED_REJECTION` | AR3-24 |

_These ten controls reuse classified result evidence and are not added to the formal/control denominator._

## Additional T39 conformance controls (overlapping evidence; n=2)

| Control | PAL route | Attempted nonconformance | Disposition | Existing result evidence |
|---|---|---|---|---|
| `AR3-T39-MISSING-WITNESS` | D22; SC-19.7; M-INQUIRY-APPEND; T39 | A further inquiry receipt is admitted without its own independent event witness. | `COUNTERMODEL_TO_OVERCLAIM` | AR3-13 |
| `AR3-T39-MISSING-COST` | D22; SC-19.7; M-INQUIRY-APPEND; T39 | A further inquiry receipt is admitted without its own independent cost witness. | `PROVED_FROM_DECLARED_RULES` | AR3-18 |

_These T39 controls make the separately required missing-event-witness and missing-cost cases explicit; they reuse AR3-13 and AR3-18 and are not added to any classification denominator._

## Manual and translation dispositions (separate population; n=1)

| Disposition | Count |
|---|---:|
| `OPEN_MANUAL` | 1 |
| `TRANSLATION_AMBIGUITY` | 0 |

_Formal/control classifications, manual/translation dispositions, PAL-source obligations, and benchmarks are not summed. None is a PAL correctness score._

## PAL-source obligations (separate population; n=1)

| Obligation | State | Preserved interfaces | Debt count |
|---|---|---|---:|
| `D-FIRST-OCCURRENCE` | `OPEN` | O04 OPEN; O25 OPEN | 1 |

## Benchmark measurements (separate population; n=10)

| Measurement | Actual value | Unit |
|---|---:|---|
| Build wall time | 3.060529 | seconds |
| Checked declarations | 73 | declarations |
| Empty axiom receipts | 61 | declarations |
| Nonempty axiom receipts | 12 | declarations |
| propext-only receipts | 7 | declarations |
| propext + Quot.sound receipts | 5 | declarations |
| Formal result rows | 21 | results |
| Adversarial/negative controls | 10 | controls |
| Policy fixtures | 4 | fixtures |
| Repository checks | 10 | checks |

The detailed benchmark receipt records command, environment, cache state, repetition method, and missing data. These measurements are not a PAL correctness score.

## Result table

| ID | PAL address | Lean declaration | Class | Explicit hypotheses or axioms | Positive claim established | Overclaim not established | Authority ceiling | Retained evidence | Reopening or unresolved burden |
|---|---|---|---|---|---|---|---|---|---|
| AR3-01 | D16; SC-19.1; M-A0-SCOPED-FIRST; T33 | PAL.AttackRun0003.scopedAccountFirstRealization | `CONSISTENT_REALIZATION` | hypotheses: the declared finite account scope; the displayed precedence relation<br>axioms: propext; Quot.sound | The admitted event is first in the declared account scope. | No temporal, ontic, causal, or global primacy follows. | Only the displayed finite account comparison is realized. | Scope membership and predecessor decisions remain inspectable. | Reopen on a wider comparison scope or conflicting predecessor. |
| AR3-02 | D16; SC-19.1; M-A0-SCOPED-FIRST; T33 | PAL.AttackRun0003.localFirstGlobalFirstCountermodel | `COUNTERMODEL_TO_OVERCLAIM` | hypotheses: the local and expanded finite scopes; one supplied predecessor edge<br>axioms: propext; Quot.sound | Local firstness coexists with failure of firstness in an expanded scope. | A0 is not established as globally or causally first. | The construction refutes only an unqualified local-to-global promotion. | Both scopes and the predecessor edge are retained. | Reopen with evidence that the declared scope is globally or causally exhaustive. |
| AR3-03 | D19; SC-19.4; M-A0-SCOPED-FIRST; T36 | PAL.AttackRun0003.strongerPrimacyAssumptionBound | `ASSUMPTION_BOUND` | hypotheses: a supplied comparison scope; a comparison witness; the conclusion-shaped firstness evidence; an authority ceiling<br>axioms: None | Supplied comparison evidence constructs a primacy receipt in its declared scope. | The cut or trace does not manufacture stronger primacy evidence. | The conclusion is bounded by the supplied evidence and comparison scope. | The witness, scope, proof, candidate, and ceiling remain in the receipt. | Challenge the supplied evidence or provide a wider comparison scope. |
| AR3-04 | D17; SC-19.2; M-A0-CUT; T34 | PAL.AttackRun0003.typedCostBearingAdmission | `CONSISTENT_REALIZATION` | hypotheses: separately supplied account, cut, scope, boundary, witness, cost, trace, ceiling, authority, residual, and reopening fields<br>axioms: propext | Admission preserves the typed cost beside distinct trace and authority fields. | Cost is not thereby source, truth, energy, permission, consent, standing, or authority. | This realizes one typed ledger admission only. | All separately typed receipt fields are retained. | Reopen by disputing a supplied field or the account-relative admission rule. |
| AR3-05 | D17; SC-19.2; M-A0-CUT; T34 | PAL.AttackRun0003.costCannotSupplyClaimReceipts | `COUNTERMODEL_TO_OVERCLAIM` | hypotheses: the inhabited positive-cost cut; an empty independent claim-witness type<br>axioms: None | A positive typed cost coexists with absence of all seven promoted claim receipts. | Recorded cost does not prove causal source, truth, energy, permission, consent, standing, or authority. | The countermodel separates the named claim kinds; it does not make them universally impossible. | The positive cost and exhaustive finite claim-kind index remain explicit. | Supply an independent witness for the particular promoted claim. |
| AR3-06 | D18; SC-19.3; M-A2-HISTORY; T35 | PAL.AttackRun0003.occurrenceRecordFromSuppliedA1A2 | `PROVED_FROM_DECLARED_RULES` | hypotheses: an admitted cut; a supplied A1 witness with a declared readability predicate and proof; a supplied A2 witness with a declared A2-to-A1 recovery predicate and proof; linked and ordered A1/A2 receipt identifiers; a declared occurrence scope equal to the cut scope; a prior history and recoverable history with prefix and membership proofs<br>axioms: None | The earned A1-to-A2 lineage constructs a scoped occurrence record with protected recoverable history. | The result does not identify ultimate source, global primacy, or scoped closure. | It proves only the supplied account-relative lineage, scope, and protected-history realization. | The cut, A1 readability proof, A2 recovery proof and target, ordered ids, scope equality, prior prefix, and stored A1/A2/occurrence ids remain explicit. | Reopen by challenging either stage criterion, lineage link, order, account scope, or protected history. |
| AR3-07 | D18; SC-19.3; M-A2-HISTORY; T35 | PAL.AttackRun0003.occurrenceRequiresA1A2Witnesses | `PROVED_FROM_DECLARED_RULES` | hypotheses: an empty A1 type in one control; an empty A2 type in the other control<br>axioms: None | Either missing stage makes the staged occurrence record uninhabited. | The theorem does not deny that valid A1 and A2 witnesses may be supplied. | This is a dependency result, not closure of first-occurrence debt. | A0, A1, and A2 remain structurally distinct. | Reopen by supplying both independently sourced witnesses. |
| AR3-08 | D18; SC-19.3; M-A2-HISTORY; T35; M-A15-CHECK | PAL.AttackRun0003.a15RequiredSeparatelyForScopedClosure | `PROVED_FROM_DECLARED_RULES` | hypotheses: an occurrence record; an empty A15 closure-witness type<br>axioms: None | Occurrence alone cannot inhabit the separately typed scoped-closure receipt. | Occurrence evidence does not by itself yield CLOSED_IN_SCOPE or global closure. | The result concerns the declared closure type only. | The occurrence history and reopening data remain unchanged. | Supply a distinct A15 witness and declared scope; O04/O25 remain open. |
| AR3-09 | D18; SC-19.3; M-A2-HISTORY; T35 | PAL.AttackRun0003.a0OnlyCountermodel | `COUNTERMODEL_TO_OVERCLAIM` | hypotheses: the inhabited A0 cut receipt; empty A1 and A2 witness types<br>axioms: None | An A0 receipt can exist while no occurrence record is constructible. | An A0 receipt alone does not prove occurrence closure. | The model does not decide ultimate source or first occurrence. | The complete typed cut receipt remains available. | Append separately witnessed A1 and A2 stages; D-FIRST-OCCURRENCE stays open. |
| AR3-10 | D18; SC-19.3; M-A2-HISTORY; T35 | PAL.AttackRun0003.occurrenceHistoryMonotone | `PROVED_FROM_DECLARED_RULES` | hypotheses: a recoverable earlier occurrence; an explicit order from observation time to a later time<br>axioms: None | The same recoverable history witness establishes the bounded predicate later. | History persistence does not imply continuing activity, source identity, or primacy. | The theorem concerns only the declared existential history predicate. | The same earlier time, activity fact, and recoverability fact are reused. | Challenge recoverability or the supplied time order. |
| AR3-11 | D18; SC-19.3; M-A2-HISTORY; T35 | PAL.AttackRun0003.historyOutlastsActivityCountermodel | `COUNTERMODEL_TO_OVERCLAIM` | hypotheses: the explicit two-time pulse model<br>axioms: propext | Recoverable occurrence history is true at time one while current activity is false. | Historical occurrence is not identical to ongoing activity or an infinite persistence claim. | This is a bounded two-time countermodel. | The time-zero trace remains the recovery basis. | Reopen under a different declared activity/history semantics. |
| AR3-12 | D20; SC-19.5; M-INQUIRY-APPEND; T37 | PAL.AttackRun0003.inquiryReceiptFromSuppliedWitness | `PROVED_FROM_DECLARED_RULES` | hypotheses: a question; an externally supplied inquiry-event witness; an independently supplied cost witness and typed cost; provenance, trace, authority snapshot and ceiling, residual, and reopening data<br>axioms: None | The supplied event and cost witnesses plus protected metadata construct one typed present inquiry receipt. | Asking does not manufacture the witness or establish truth, permission, or authority. | The receipt records the admitted inquiry event only. | Question, event witness, cost witness and value, provenance, trace, authority snapshot and ceiling, residual, and reopening data are retained. | Challenge the witness basis or append a separately witnessed later inquiry. |
| AR3-13 | D20; SC-19.5; D22; SC-19.7; M-INQUIRY-APPEND; T37; T39 | PAL.AttackRun0003.questionDoesNotSelfCertify | `COUNTERMODEL_TO_OVERCLAIM` | hypotheses: an ordinary question; an empty inquiry-event witness type<br>axioms: None | The question remains available while an inquiry receipt with an empty event-witness type is uninhabited, including for a further inquiry append. | Asking alone does not manufacture the event witness required by a present or further inquiry receipt. | The countermodel blocks event-witness self-certification only. | The question remains distinct from receipt witness, provenance, and append history. | Supply an independent event witness for the particular inquiry receipt. |
| AR3-14 | D20; SC-19.5; M-INQUIRY-APPEND; T37 | PAL.AttackRun0003.questionCannotSupplyInquirerClaims | `COUNTERMODEL_TO_OVERCLAIM` | hypotheses: an admitted inquiry receipt with independent event and cost witnesses; empty independent witnesses for six promoted claim kinds<br>axioms: None | The admitted inquiry receipt coexists with absence of ontology, consciousness, standing, ultimate-source, global-priority, and original-cut causal-source claim receipts. | Neither asking nor receipt production proves the inquirer claims or witnesses the original cut’s causal source. | The finite six-kind model does not settle whether any such evidence could exist independently. | The admitted receipt and six separately typed promoted-claim addresses remain distinct. | Supply independent evidence and authority for the particular promoted claim. |
| AR3-15 | D21; SC-19.6; M-SOURCE-FIBER; T38 | PAL.AttackRun0003.cutOnlyCongruence | `PROVED_FROM_DECLARED_RULES` | hypotheses: two source-indexed receipts; equality of their cut fields<br>axioms: None | Equal cut fields yield equal cut-only projections. | Projection equality does not identify upstream sources. | The theorem is restricted to the cut-only interface. | Both source fields remain outside the projection. | Supply a discriminating witness or justified injectivity. |
| AR3-16 | D21; SC-19.6; M-SOURCE-FIBER; T38 | PAL.AttackRun0003.noninjectiveSourceFiberCountermodel | `COUNTERMODEL_TO_OVERCLAIM` | hypotheses: the explicit two-source, one-cut finite map<br>axioms: None | Distinct sources have the same accessible cut value. | A cut-only interface does not uniquely identify its source. | The countermodel does not claim every source map is noninjective. | Both source constructors and the shared image remain explicit. | Add discriminating evidence or a justified injectivity premise. |
| AR3-17 | D21; SC-19.6; M-SOURCE-FIBER; T38 | PAL.AttackRun0003.injectiveSourceIdentificationAssumptionBound | `ASSUMPTION_BOUND` | hypotheses: a supplied source map; an explicit injectivity proof; equality of two cut images<br>axioms: None | Source identity follows under the supplied injectivity premise. | Injectivity is not derived from PAL or from cut equality. | Identification is conditional on the disclosed premise. | The map, injectivity proof, and equality witness remain required. | Challenge injectivity or exhibit a nontrivial source fiber. |
| AR3-18 | D22; SC-19.7; M-INQUIRY-APPEND; T39 | PAL.AttackRun0003.witnessedInquiryAppendPreservesPrefix | `PROVED_FROM_DECLARED_RULES` | hypotheses: an existing finite inquiry ledger; one independently event- and cost-witnessed inquiry receipt; a link to an existing parent; exact retention of prior event ids; a fresh appended event id<br>axioms: propext | The proof-gated append preserves every prior entry as a prefix, includes the fresh linked receipt, retains all prior ids, and separately blocks a missing cost witness. | One witnessed append does not imply another or an infinite causal ontology. | The theorem concerns finite list extension only. | All prior entries and ids plus the new event witness, cost witness and value, provenance, parent link, and fresh id remain. | Every further inquiry requires independent event and cost witnesses, an existing parent link, retained ids, freshness, and an append proof. |
| AR3-19 | D22; SC-19.7; M-INQUIRY-APPEND; T39 | PAL.AttackRun0003.finiteTerminalCountermodel | `COUNTERMODEL_TO_OVERCLAIM` | hypotheses: an explicit one-entry parent ledger; an independently event- and cost-witnessed linked child with retained prior ids and a fresh id; the resulting two-entry state marked reopened and then terminal<br>axioms: propext; Quot.sound | A genuine linked parent-to-child append preserves the parent prefix and then terminates with no further step or unbounded support. | Reopenability does not prove an actually infinite causal ontology. | The construction is a finite countermodel, not an ontology theorem. | The exact parent prefix, child link, event and cost witnesses, retained ids, fresh id, and two-entry finite ledger remain intact. | Append a new independently event- and cost-witnessed, linked, fresh receipt to reopen this terminal state. |
| AR3-20 | D23; SC-19.8; M-INQUIRY-APPEND; T40 | PAL.AttackRun0003.laterEvidenceAppendPreservesPrior | `PROVED_FROM_DECLARED_RULES` | hypotheses: a prior inquiry ledger and an existing parent membership proof; a fresh later record linked to the parent and retaining all prior ids; a separately supplied later recovery witness and evidence id<br>axioms: propext | The linked recovery record is appended to account history while the earlier receipt’s witness, cost, trace, and authority snapshot are recovered fieldwise unchanged. | A later witness cannot retroactively create earlier witness, payment, consent, standing, or authority. | The theorem governs only the displayed parent-membership, linkage, retained-id, freshness, and append constructor. | The exact prior history, parent fields, membership proof, link, retained ids, fresh later record, and recovery witness are retained. | Contest parent membership, linkage, retained ids, freshness, or append another independently sourced recovery record. |
| AR3-21 | D23; SC-19.8; M-INQUIRY-APPEND; T40 | PAL.AttackRun0003.overwriteIsNotAppendCountermodel | `COUNTERMODEL_TO_OVERCLAIM` | hypotheses: the concrete one-entry ledger; a replacement receipt with rewritten cost<br>axioms: propext; Quot.sound | Destructive head replacement erases the original and fails prefix preservation. | Appending evidence does not permit alteration of the earlier receipt or authority snapshot. | The countermodel distinguishes the displayed overwrite operation from licensed append. | Original and mutated receipts remain separately inspectable. | Use a linked append and prove preservation of the prior receipt. |
| AR3-22 | PAL-v2.1-Spine L05; PAL-v2.1-T T05 | None | `EXPECTED_REJECTION` | hypotheses: the two unchanged T05 lexical fixtures; the bounded standalone-identifier scanner<br>axioms: None | Both literal standalone identifier fixtures receive the stable lexical rejection. | The lexical rule does not prove that differently named semantic surrogates are absent. | This is a bounded naming firewall; unresolved possibility remains metalinguistic by source review. | The exact ASCII and symbol fixtures and diagnostics are retained. | Semantic-surrogate review remains OPEN_MANUAL. |
| AR3-23 | D18; SC-19.3; M-A2-HISTORY; T35 | None | `EXPECTED_REJECTION` | hypotheses: the AR3 explanatory-shorthand fixture; the bounded selected-spelling declaration guard<br>axioms: None | The attempted object-language shorthand status receives the expected policy rejection. | The naming guard is not a complete semantic proof against every surrogate. | The source, not the fixture scanner, establishes that the phrase is explanatory only. | The fixture and exact stable diagnostic are retained. | Differently named semantic promotion remains OPEN_MANUAL review. |
| AR3-24 | D-FIRST-OCCURRENCE; O04; O25; PAL-v2.1-T T35 | None | `EXPECTED_REJECTION` | hypotheses: the AR3 first-occurrence-closure fixture; the bounded selected-spelling debt-closure guard<br>axioms: None | The attempted formal closure declaration receives the expected policy rejection. | The fixture does not turn a naming rule into PAL adoption authority. | Lean and repository policy cannot close O04, O25, or D-FIRST-OCCURRENCE. | The fixture, diagnostic, and separate OPEN burden receipt are retained. | D-FIRST-OCCURRENCE remains OPEN through O04 and O25. |
| AR3-25 | PAL-v2.1-Spine L05; PAL-v2.1-T T05; PAL-v2.1-L O04/O25 | None | `OPEN_MANUAL` | hypotheses: manual review of names, types, constructors, comments, receipts, and authority claims<br>axioms: None | No literal forbidden identifier occurs in scanned Lean object language, and the declared namespace was manually reviewed. | Automation does not establish semantic completeness or discharge source/authority burdens. | Manual review is a control, not a formal theorem or adoption decision. | Policy output, source review notes, and the complete declaration inventory are retained. | Review reopens on any new declaration, semantic surrogate, or authority claim. |

## Manual review

The lexical policy fixtures are bounded guards only. Semantic-surrogate review remains manual, and unresolved possibility remains outside Lean’s object language.

_Generated from `Audit/attack-run-0003-claim-ledger.json` and `Audit/attack-run-0003-receipt.json`; do not edit by hand._
