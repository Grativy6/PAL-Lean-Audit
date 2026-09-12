# BRIDGE v0.4 four-sector audit

Execution: **PASS_BOUNDED_FOUR_SECTOR**. Audited declarations: 14.

Source: the supplied BRIDGE v0.4 manuscript, Four Sector Endpoint Theorem, OOXML paragraphs P0108-P0199. The preserved source excerpt contains the original mathematical XML as well as readable paragraph text.

The earlier v0.2 four-sector dimension identity remains prior evidence. This batch checks the declarations listed below; broader diagram coverage is described in SOURCE-REVIEW.md.

| ID | Checked content | Classification |
|---|---|---|
| FS-01 | Raw hidden map kernel | PROVED_FROM_DECLARED_RULES |
| FS-02 | Hidden map is injective | PROVED_FROM_DECLARED_RULES |
| FS-03 | Defect-to-visible map is surjective | PROVED_FROM_DECLARED_RULES |
| FS-04 | Generated quotient row exactness | PROVED_FROM_DECLARED_RULES |
| FS-05 | Kernel quotient row exactness | PROVED_FROM_DECLARED_RULES |
| FS-06 | Defect quotient column exactness | PROVED_FROM_DECLARED_RULES |
| FS-07 | Residual sequence exactness | PROVED_FROM_DECLARED_RULES |
| FS-08 | Right-column exactness | PROVED_FROM_DECLARED_RULES |
| FS-09 | Generated-visible first-isomorphism equivalence | CONSISTENT_REALIZATION |
| FS-09K | Restricted-readout kernel | PROVED_FROM_DECLARED_RULES |
| FS-10 | Left-column exactness | PROVED_FROM_DECLARED_RULES |
| FS-11 | Upper-left square commutes | PROVED_FROM_DECLARED_RULES |
| FS-12 | Lower-left square commutes | PROVED_FROM_DECLARED_RULES |
| FS-13 | Concrete non-complement countercase | COUNTERMODEL_TO_OVERCLAIM |

## Boundaries and evidence

- [Exact claims, hypotheses and source mappings](claims.json).
- [Source correspondence and diagram coverage](SOURCE-REVIEW.md).
- [Execution, dependencies and log hashes](results.json).
- [Source identity](source-manifest.json).
- Formal statements have only their recorded scope. No Hodge or Weil result, geometric application, canon adoption, or PAL obligation closure is claimed.
- Local Windows execution; CI and publication for this new batch are not claimed.
- Counts are declarations and may share dependencies. The v0.2 dimension result is not an independent new discovery.

Manual dispositions:

- id: FS-M01 classification: OPEN_MANUAL subject: Remaining 3x3 commutative squares and vertical maps source_refs: ['P0126-P0192'] reason: This lane checks only the upper-left and lower-left squares; it does not claim the complete displayed diagram. reopening: Name each remaining source arrow and prove its corresponding commutation separately.
- id: FS-M03 classification: OPEN_MANUAL subject: Visible-sector readout quotient equivalence source_refs: ['P0123-P0124'] reason: The source's V ≅ rT/rB presentation is not formalized in this lane. reopening: Add a source-bounded quotient-of-range construction with its exact assumptions.
- id: FS-M04 classification: OPEN_MANUAL subject: Finite-dimensional account and residual recovery criterion source_refs: ['P0193-P0199'] reason: The prior v0.2 dimension identity remains separate; this v0.4 map audit does not formalize finrank accounting or H=0 iff K⊆B. reopening: Commission a separately source-mapped finite-dimensional and recovery lane.

Reproduce with `python Audit/bridge-v04-four-sector/run.py --run --lake <lake>`. Add `--source-file <BRIDGE_v0.4.docx>` to reread original source bytes. Verify the saved bundle with `--check`.
