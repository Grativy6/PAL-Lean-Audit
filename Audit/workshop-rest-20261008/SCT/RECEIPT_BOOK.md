# Single-Cut Transport: local proof receipts

**All three selected batches passed.** Source: SCT v0.1, retained exact DOCX identified by the [source manifest](../source-manifest.json). Manuscript unchanged.

| Batch | Result | Evidence |
| --- | --- | --- |
| SCT-A | The actual hull-minus-support count gives the span identity and exact endpoint decomposition for arbitrary finite supports and nonempty clause subsets. | [Review](../SCT-A/REVIEW.md), [receipt](../SCT-A/results.json) |
| SCT-B | Every finite filled corridor has the same charge at fixed endpoints. An inserted unselected interior column adds one; zero slack cannot decode orientation. | [Review](../SCT-B/REVIEW.md), [receipt](../SCT-B/results.json) |
| SCT-C | The seven-column gadget accepts exactly OR. Every one of the 5040 permutations is covered without duplication. | [Review](../SCT-C/REVIEW.md), [Lean receipt](../SCT-C/results.json), [computation pointer](../SCT-C/computation-pointer.json) |

The exact order counts match the manuscript: `000:0, 001:8, 010:4, 011:28, 100:2, 101:12, 110:14, 111:50`. The Python record covers all 40,320 order/truth pairs. The local OR theorem has its own Lean proof and bundled kernel receipt; the count table is separately labeled computational evidence.

No new mathematical defect appeared in these selected claims. The filled-corridor, orientation and valid-budget assumptions do real work, exactly where the paper says they do. The non-decoding and per-occurrence limits survive formalization.

The model identifies named columns with ranks through a supplied bijection. General natural endpoint charge is a labeled extension; the source Boolean statement uses charges 0 and 1. Proofs do not derive the supplied cut or orientation. No global NP-completeness reduction, gadget minimality, novelty, physical transport or PAL adoption is established.

Verification: module builds, every explicit declaration's exact type and axiom inventory, forbidden-proof-escape scan, source hashes, bundled kernel replay and saved receipt checks. Review is self-review; bundled Lean is not an independent kernel implementation. Existing source lineage is retained.

Editable proofs: [span](../../../Experiments/SingleCutSpan.lean), [corridor](../../../Experiments/SingleCutCorridor.lean), [OR](../../../Experiments/SingleCutOR.lean).
