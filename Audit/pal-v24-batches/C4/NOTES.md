# C4 — Admitted-domain feedback dependence

This batch gives a bounded extensional realization of PAL-v2.3-M Atlas paragraphs P0687–P0701, whose exact source identity is recorded in `claims.json` and whose literal excerpts are in `source-excerpts.json`.

`RetainedOutput` carries a value and explicit lineage field; `LaterSuccessor` does the same. The certificate demands two admitted retained records at a common input and action, distinct as full records, whose later successors are unequal as full records. `AdmittedVariation` states that same witness condition. The theorem `feedback_certificate_iff_admitted_variation` proves the witness/predicate correspondence. The generic predecessor theorem shows that an update independent of the retained-output argument cannot satisfy the certificate.

The finite Bool fixture demonstrates both sides of the admitted-domain boundary. `boolEcho` is nonconstant across the full ambient Bool output type, but `restrictedAdmission` admits only false-valued records, so there is no distinct admitted pair and no admitted variation. Under `allBoolOutputsAdmitted`, the false/true pair yields a positive finite certificate. The lineage lemma checks only that this fixture copies its lineage field.

These are ordinary function and equality facts for supplied types, `Adm`, and `F`. Ambient nonconstancy is not a certificate on a restricted domain. A certificate proves an extensional difference between successors for one admitted pair; it does not prove intervention causality, reachable influence, stability, agency, intent, or any physical mechanism. The batch does not model noise, reachable-state semantics, or forget-to-A4 behavior; those remain open as recorded in `claims.json`.

No final batch receipt or candidate-source freeze is claimed here. The parent workflow must perform its source freeze and final receipt protocol separately.
