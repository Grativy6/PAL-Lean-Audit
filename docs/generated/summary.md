# Generated audit status

- Run: attack-0001
- Controlling release: PAL v2.0
- DOI: [10.5281/zenodo.21754097](https://doi.org/10.5281/zenodo.21754097)
- Run receipt: [Audit/attack-run-0001-receipt.json](../../Audit/attack-run-0001-receipt.json)
- Authority ceiling: Lean-checked bounded receipt models, countermodels, and policy fixtures only; no claim that mathematics contains PAL, no semantic proof against differently named surrogates for unresolved possibility, and no closure of O04/O25.

## Selected T-target outcomes

| Outcome status | Count |
|---|---:|
| PROVED | 6 |
| COUNTERMODEL | 3 |
| EXPECTED_REJECTION | 1 |
| OPEN | 0 |
| NOT_FORMALIZED | 0 |

_These counts cover selected test outcomes only._

## Open PAL-source obligations (separate population)

| Obligation | Interfaces | Status | Reason |
|---|---|---|---|
| D-FIRST-OCCURRENCE | O04, O25 | **OPEN** | A local supplied witness constructs only a conditional receipt; the certificate grammar does not supply its own ontic witness. |

_Selected-test OPEN outcomes and open PAL-source obligations are distinct metrics and are never summed._

## Claim ledger

| Test | Target | Status | Evidence |
|---|---|---|---|
| T05 | Literal Omega-identifier firewall | **EXPECTED_REJECTION** | The lexical policy rejects standalone `Omega` and `Ω` identifiers in scanned Lean code and both fixtures receive the stable T05 diagnostic. This does not detect differently named semantic surrogates. |
| T06 | A0 cut | **PROVED** | noCutWithoutWitness; CutReceipt is witness-parameterized and distinct from optional ModelEnvelope scaffolding. |
| T07 | Omega-star reflection | **PROVED** | reflectionForgetsToIndexedCut and cutAddressNeReflectionAddress; no canonical reflection law is selected. |
| T09 | Theta authority and nonimplication | **COUNTERMODEL** | thetaDoesNotProvideReadable: an inhabited Boolean nonidentity turn with an empty readout-witness type. |
| T10 | Primitive placement | **PROVED** | primitivePlacement and floorChainReturnsCut enforce the dependent cut-reflection-turn-readable route. |
| T11 | A0-A1-A2 separation | **COUNTERMODEL** | thetaDoesNotProvideReadable and readableDoesNotProvideTrace separate turn, readability, and recoverability witnesses. |
| T14 | Predecessor strictness | **COUNTERMODEL** | allLayersHaveStrictPredecessor conditionally gives a bounded A1-A15 predecessor family from an externally supplied witness, with forgetful recovery. |
| T15 | Witness nonmanufacture | **PROVED** | missingWitnessYieldsNoOutput plus NoWitness theorems cover every explicit-witness-field constructor in this bounded run; O04/O25 remains OPEN. |
| T16 | Trace recovery and immutability | **PROVED** | routePreservesProtectedTrace and authorizedCompressionRestores preserve the original protected receipt through the bounded route. |
| T17 | No authority backflow | **PROVED** | noAuthorityBackflow preserves the exact earlier authority snapshot for every modeled later-result kind. |

_Generated from Audit/claim-ledger.json; do not edit by hand._
