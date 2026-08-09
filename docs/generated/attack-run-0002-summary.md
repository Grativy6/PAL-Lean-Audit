# Generated audit status

- Run: attack-0002
- Controlling release: PAL v2.0
- DOI: [10.5281/zenodo.21754097](https://doi.org/10.5281/zenodo.21754097)
- Run receipt: [Audit/attack-run-0002-receipt.json](../../Audit/attack-run-0002-receipt.json)
- Run status: **PROVISIONAL_CI_PENDING**
- Receipt status: **CANDIDATE_NONCANONICAL**
- Candidate adoption: **CANDIDATE** for C21-01, C21-02, C21-03, C21-04, C21-05, C21-06, C21-07, C21-08
- Human decision: **PENDING_GATE_4**
- Authority ceiling: Attack Run 0002 contains bounded Lean realizations and countermodels controlled by PAL v2.0. It does not adopt any C21 statement, amend PAL canon, make unresolved possibility an object, derive a supplied witness or ultimate source, identify a globally first event, equate cost with cause, prove an infinite ontology, create ethical or decision authority, or close D-FIRST-OCCURRENCE, O04, or O25.

## Attack Run 0002 targets

| Outcome status | Count |
|---|---:|
| PROVED | 3 |
| COUNTERMODEL | 5 |
| EXPECTED_REJECTION | 0 |
| OPEN | 0 |
| NOT_FORMALIZED | 0 |

_These counts cover selected test outcomes only._

## Open PAL-source obligations (separate population)

| Obligation | Interfaces | Status | Reason |
|---|---|---|---|
| D-FIRST-OCCURRENCE | O04, O25 | **OPEN** | The bounded models use supplied or model-specific witnesses. They neither supply the ontic inhabitance/source witness governed by O04 nor allow a certificate or revocation grammar to invent the witness governed by O25. |

_Selected-test OPEN outcomes and open PAL-source obligations are distinct metrics and are never summed._

## Open manual review controls (separate population)

| Control | Type | Status | Scope |
|---|---|---|---|
| AR2-MANUAL-SEMANTIC-SURROGATE | MANUAL_SOURCE_REVIEW | **OPEN** | Review the final Lean declarations and their uses for any differently named object-language surrogate that is asked to stand for or exhaust unresolved possibility. The T05 literal-identifier scan cannot decide this semantic question. |

_Manual review controls are neither formal outcomes nor PAL-source obligations._

## Required negative-guard dispositions (separate population)

| Fixture | Guard | Disposition | Control | Evidence or diagnostic |
|---|---|---|---|---|
| AR2-N01 | Object-language Omega or semantic surrogate | **OPEN** | MANUAL_SOURCE_REVIEW | scripts/check_policy.py passes the literal T05 identifier scan for the final Lean roots. AR2-MANUAL-SEMANTIC-SURROGATE remains OPEN because differently named semantic surrogates require manual source review and are not a Lean result. |
| AR2-N02 | Source injectivity without assumption | **COUNTERMODEL** | CHECKED_COUNTERMODEL | PAL.AttackRun0002.sourceFiberCountermodel is an inhabited noninjective source-to-cut model; PAL.AttackRun0002.downstreamCannotDistinguishSameCut proves Cut-only congruence. Both report axioms []. |
| AR2-N03 | Asker as original causal-source witness | **OPEN** | MANUAL_SOURCE_REVIEW_WITH_CHECKED_BOUNDS | PAL.AttackRun0002.occurrenceDoesNotIdentifySource checks the source ceiling and PAL.AttackRun0002.inquiryCreatesNewReceipt requires a supplied inquiry witness, but no separate asker-as-source rejection theorem or fixture is claimed. Manual source review remains OPEN. |
| AR2-N04 | Later success manufactures earlier warrant | **OPEN** | MANUAL_SOURCE_REVIEW_WITH_CHECKED_PRESERVATION_BOUND | PAL.AttackRun0002.noRetroactivePayment preserves the complete prior receipt, its cost, and its authority snapshot by exact equality with axioms []. The aggregate guard remains OPEN because arbitrary later proof, success, wording, consent, or standing is outside appendLaterWitness. |
| AR2-N05 | Indefinite inquiry implies infinite ontology | **OPEN** | MANUAL_SOURCE_REVIEW_WITH_FINITE_CHECKED_MODEL | PAL.AttackRun0002.inquiryCreatesNewReceipt constructs exactly one supplied finite inquiry step. It does not formalize indefinite continuation or an infinite ontology, so the broader semantic guard remains OPEN to source review. |
| AR2-N06 | Cost field absorbs the receipt | **OPEN** | MANUAL_TYPED_FIELD_REVIEW_WITH_CHECKED_COUNTERMODEL | PAL.AttackRun0002.costDoesNotImplyCause checks that a populated CutReceipt cost does not inhabit a separately witnessed causal-source receipt. The broader field-separation control remains OPEN for manual review; no rejection fixture path is invented. |
| AR2-N07 | A0 alone closes occurrence | **OPEN** | MANUAL_SOURCE_REVIEW_WITH_CHECKED_CONSTRUCTOR_SEPARATION | PAL.AttackRun0002.occurrenceDoesNotIdentifySource makes the bounded occurrence structure empty when the distinct later-witness type is NoWitness while the supplied A0 cut remains available, with axioms []. The aggregate guard remains OPEN because canonical A1/A2/A15 and CLOSED_IN_SCOPE emission are not formalized here. |
| AR2-N08 | Local first becomes global first | **COUNTERMODEL** | CHECKED_COUNTERMODEL | PAL.AttackRun0002.noGlobalFirstFromLocalFirst exhibits an account-order-zero entry that is not first in the supplied finite temporal history; axiom receipt []. |
| AR2-N09 | Prior receipt preservation under later witness | **PROVED** | CHECKED_BOUNDED_PRESERVATION | PAL.AttackRun0002.noRetroactivePayment returns the exact prior receipt and preserves its cost and authority snapshot; axiom receipt []. |
| AR2-N10 | Cost implies cause, truth, or physical energy | **OPEN** | CHECKED_CAUSE_COUNTERMODEL_PLUS_MANUAL_SCOPE_REVIEW | PAL.AttackRun0002.costDoesNotImplyCause checks the cause component with axioms []. Truth and physical-energy claims are not modeled, so their semantic exclusion remains OPEN for manual source review rather than being reported as a formal result. |
| AR2-N11 | Generated self-description has privileged standing | **OPEN** | MANUAL_SOURCE_REVIEW | No generated-self-description theorem or fixture is claimed. Manual source review remains OPEN and the bounded AR2 models contain no field granting consciousness, ontology, consent, standing, or authority from generated output. |

_Negative guards may reuse selected-target evidence or an open manual control. They are dispositions, not additional independent claims, and are not summed with the other populations._

## Claim ledger

| Test | Target | Status | Evidence |
|---|---|---|---|
| AR2-01 | Source-fiber countermodel | **COUNTERMODEL** | PAL.AttackRun0002.sourceFiberCountermodel in PAL/AttackRun0002.lean; axiom output routed to artifacts/attack-run-0002-axioms.txt. |
| AR2-02 | Downstream cut congruence | **PROVED** | PAL.AttackRun0002.downstreamCannotDistinguishSameCut in PAL/AttackRun0002.lean; axiom output routed to artifacts/attack-run-0002-axioms.txt. |
| AR2-03 | Occurrence does not identify source | **COUNTERMODEL** | PAL.AttackRun0002.occurrenceDoesNotIdentifySource in PAL/AttackRun0002.lean; axiom output routed to artifacts/attack-run-0002-axioms.txt. |
| AR2-04 | Cost does not imply cause | **COUNTERMODEL** | PAL.AttackRun0002.costDoesNotImplyCause in PAL/AttackRun0002.lean; axiom output routed to artifacts/attack-run-0002-axioms.txt. |
| AR2-05 | Historical persistence without ongoing activity | **COUNTERMODEL** | PAL.AttackRun0002.historicalPersistence in PAL/AttackRun0002.lean; axiom output routed to artifacts/attack-run-0002-axioms.txt. |
| AR2-06 | Local first does not imply global first | **COUNTERMODEL** | PAL.AttackRun0002.noGlobalFirstFromLocalFirst in PAL/AttackRun0002.lean; axiom output routed to artifacts/attack-run-0002-axioms.txt. |
| AR2-07 | Admitted inquiry creates one receipt | **PROVED** | PAL.AttackRun0002.inquiryCreatesNewReceipt in PAL/AttackRun0002.lean; axiom output routed to artifacts/attack-run-0002-axioms.txt. |
| AR2-08 | No retroactive payment or authority rewrite | **PROVED** | PAL.AttackRun0002.noRetroactivePayment in PAL/AttackRun0002.lean; axiom output routed to artifacts/attack-run-0002-axioms.txt. |

_Generated from Audit/attack-run-0002-claim-ledger.json; do not edit by hand._
