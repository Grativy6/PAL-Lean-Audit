# BRIDGE v0.4 generated-span recovery bounded audit

**PASS_BRIDGE_GENERATED_RECOVERY**

One selected source clause: P0195 generated-span recovery, interpreted with P0107. This is not a coverage claim for all BRIDGE.

| Formal inventory classification | Declarations |
|---|---:|
| CONSISTENT_REALIZATION | 2 |
| COUNTERMODEL_TO_OVERCLAIM | 3 |
| PROVED_FROM_DECLARED_RULES | 7 |

Total: 12 declarations, including definitions, equivalent formulations and examples. They share dependencies and are not independent discoveries.

One additional unstructured-answer type-checking fixture in the axiom module guards the translation boundary; it is not an additional manuscript claim.

Receipt rejection guards: 17. These test the evidence checker and are not mathematical counterexamples.

The checked realization separates chosen-answer factorization from full identity recovery and records countercases independently from controller/tooling checks.

All 15 controller commands passed. The predecessor receipt is preserved by hash and checked through its saved receipt.

The DOCX and 95 preserved OOXML paragraphs are checked locally when supplied; CI checks committed snapshots only.

PAL obligations O04, O25 and D-FIRST-OCCURRENCE remain OPEN.

Reproduce: `python Audit/bridge-v04-generated-recovery/run.py --run --lake <lake> --source-file <BRIDGE_v0.4.docx>`; use `--check` for the saved receipt.
