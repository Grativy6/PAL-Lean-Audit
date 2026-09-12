# PAL CHARTER and BRIDGE bounded Lean audit

Local execution: **PASS_LOCAL_BOUNDED_CHECKS**. Source identity: all seven supplied DOCX files verified by SHA256.

This is a finite supplement to the 2026-09-07 experiments. Historical Attack Runs 0001-0003 keep their original release scope. The user-selected PAL v2.3, CHARTER v1.0 and BRIDGE v0.4 documents control this supplement only.

| Work | New checked declarations | Classifications |
|---|---:|---|
| PAL | 4 | COUNTERMODEL_TO_OVERCLAIM: 1; PROVED_FROM_DECLARED_RULES: 3 |
| CHARTER | 4 | PROVED_FROM_DECLARED_RULES: 4 |
| BRIDGE | 5 | COUNTERMODEL_TO_OVERCLAIM: 1; PROVED_FROM_DECLARED_RULES: 4 |

Counts are theorem declarations, not independent scientific findings or full source conformance. The preserved 27-declaration PAL/CHARTER replay is a separate population. Each named module passed the bundled Lean kernel checker; exact dependencies appear in results.json.

## PAL

- **PAL23-SUP-01: Concrete compare-exchange collision** (COUNTERMODEL_TO_OVERCLAIM). Comparator and coordinate semantics are fixed to this Lean definition.
- **PAL23-SUP-02: Action-bit left inverse** (PROVED_FROM_DECLARED_RULES). No storage, binding, schedule, or recovery evidence is modeled.
- **PAL23-SUP-03: Repaired compare-exchange injectivity** (PROVED_FROM_DECLARED_RULES). The proof does not establish retention, storage integrity, or multi-step replay.
- **PAL23-SUP-04: Uniqueness of a reachable decoder** (PROVED_FROM_DECLARED_RULES). Existence, totalization, and decoder classes remain separately scoped.

Manual dispositions (not Lean results):

- {"id": "PAL-SUP-M01", "classification": "OPEN_MANUAL", "disposition": "Source-to-model review remains local and provisional. Multi-step schedule storage, A2 persistence, ambient decoder totalization, and multi-parent lineage are outside this batch; O04/O25 and D-FIRST-OCCURRENCE remain OPEN."}

## CHARTER

- **CHARTER-SUPPLEMENT-C01: Declared coordinate norm is multiplicative** (PROVED_FROM_DECLARED_RULES). The source's identification with Eisenstein integers is represented by declared coordinates rather than a library isomorphism.
- **CHARTER-SUPPLEMENT-C02: Declared conjugation preserves coordinate norm** (PROVED_FROM_DECLARED_RULES). No connection to the manuscript's Euclidean embedding is formalized.
- **CHARTER-SUPPLEMENT-C03: Declared unit rotation preserves coordinate norm** (PROVED_FROM_DECLARED_RULES). The sixth-power rotation law is not included in this supplementary lane.
- **CHARTER-SUPPLEMENT-C04: Full coordinate rotation has only the origin as a fixed point** (PROVED_FROM_DECLARED_RULES). No norm-positivity bridge from nonzero coordinates is included.

Manual dispositions (not Lean results):

- {"id": "CHARTER-SUPPLEMENT-M01", "classification": "OPEN_MANUAL", "disposition": "The manuscript's notation identifies coordinates with Eisenstein integers; this lane uses an explicit integer-pair realization and does not claim a library-level identity with a canonical Eisenstein type."}

## BRIDGE

- **BRIDGE-L01: Zero residue iff readout-kernel membership** (PROVED_FROM_DECLARED_RULES). No quotient construction or measurement-uncertainty policy is formalized.
- **BRIDGE-L02: Zero residue yields equality of readout values** (PROVED_FROM_DECLARED_RULES). The source's quotient-class presentation is represented here by equal readout values.
- **BRIDGE-L03: Uniform equality iff the admitted-difference kernel is trivial** (PROVED_FROM_DECLARED_RULES). The stated injectivity reformulation is not separately represented.
- **BRIDGE-L04: Reachable decoder iff fiber-constant answer** (PROVED_FROM_DECLARED_RULES). No linear-sector or finite-capacity result is formalized here.
- **BRIDGE-L05: Explicit hidden-difference countermodel** (COUNTERMODEL_TO_OVERCLAIM). It is a minimal algebraic example, not a model of the document's Hodge setting.

Manual dispositions (not Lean results):

- {"id": "BRIDGE-M01", "classification": "OPEN_MANUAL", "subject": "Hodge, Weil-type, cycle-class, and boundary-lifting claims", "reason": "Excluded by this lane's grant; no external theorem verification or geometry formalization was performed.", "source_refs": ["P0005-P0010"]}
- {"id": "BRIDGE-M02", "classification": "OPEN_MANUAL", "subject": "P0073 quotient/intersection/injectivity equivalence", "reason": "The admitted-image criterion is formalized elementwise. The quotient isomorphism and the subspace injectivity extension are not formalized in this batch.", "source_refs": ["P0071-P0073"]}

## Evidence and limits

- [Exact statements and PAL source mapping](pal-claims.json), [CHARTER mapping](charter-claims.json), [BRIDGE mapping](bridge-claims.json).
- [Execution receipt](results.json), [source lock](source-manifest.json), and [source correspondence review](REVIEW.md).
- Reproduce with `python Audit/recent-work-20260911/run.py --run`; verify with `--check`. Pass `--lake` if the pinned Lake executable is not on PATH.
- Repository input digests normalize CRLF to LF; original DOCX and log digests are byte exact. Missing source files stop local verification.
- PAL: Omega remains metalinguistic. O04 and O25 remain separate OPEN interfaces to D-FIRST-OCCURRENCE; multi-parent lineage remains OPEN. Finite administrative or algebraic models confer no actual authority.
- BRIDGE: this batch does not verify the Hodge conjecture reduction, cycle construction, Markman coverage, monodromy, or the branch-aware boundary-lifting protocol.
- Source correspondence is a review judgment; matching quotations and successful Lean checks do not prove that an encoding fully captures its prose source.
- Local Windows execution only. CI was not run; no publication, source adoption, or canon amendment occurred. Historical release archive bytes were not reread.
- No benchmark comparison or numerical correctness score is claimed.
