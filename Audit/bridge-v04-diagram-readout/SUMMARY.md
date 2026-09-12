# BRIDGE diagram and readout bounded audit

Execution: **PASS_BRIDGE_DIAGRAM_READOUT**.

| Lane | Declarations |
|---|---:|
| diagram | 12 |
| readout | 7 |
| Prerequisite four-sector batch (separate prior evidence) | 14 |

The new diagram aggregate certifies six short-exact sequences, including endpoints, and all four commuting squares. The readout equivalence sends [t] to [r(t)] and agrees with the induced residual map. Three checked countercases constrain overclaims. Helpers and aggregates share dependencies; counts are not independent discoveries.

[Source correspondence and diagram](SOURCE-CORRESPONDENCE.md) · [Diagram claims](diagram-claims.json) · [Readout claims](readout-claims.json) · [Execution, axioms and hashes](results.json)

Selected source scope is P0108-P0192 within the retained P0108-P0199 snapshot. Three additional context paragraphs identify the field and linear-instance hypotheses. The local DOCX check verifies its original bytes and all 95 preserved OOXML paragraphs. CI replays the committed excerpts and Lean declarations without claiming absent DOCX bytes were reread.

FS-M01 and FS-M03 are addressed by new bounded evidence; their historical OPEN_MANUAL records are preserved. FS-M04, finite-dimensional/recovery claims, frame morphisms, Hodge/Weil and geometric applications remain outside this batch. PAL obligations remain OPEN. No source adoption or merge is performed.

Receipt guards: 16 expected rejections, separate from theorem and fixture counts.

Reproduce with `python Audit/bridge-v04-diagram-readout/run.py --run --lake <lake> --source-file <BRIDGE_v0.4.docx>`. Verify the saved evidence with `--check`; create a fresh replay with `--replay --output-dir <new-directory>`.
