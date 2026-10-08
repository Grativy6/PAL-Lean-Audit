# Publication concordance

The clean manuscript preserves all 58 display expressions, all inline mathematical expressions, and the mathematics in all 21 headed proposition sections of the audited Markdown. The source concordance records the exact hashes and the permitted prose edits. The original proof inputs and receipts remain unchanged.

The native Word export required presentation repairs: three diameter characters were restored to the source's empty-set symbol; stars and set-difference signs received equivalent mathematical Unicode glyphs; restriction bars were marked literal; an invisible layout character was removed; and equations 9a and C2 received export-safe row layouts. These repairs retain expression order and meaning. The helper `normalize_omml.py` makes the transformations inspectable. The concordance records every affected native math object, its before/after hashes, and the operation performed.

The 56 source equation labels were restored, the contents page was rebuilt with internal links, and the wide policy comparison was transposed without changing its values. All 56 rendered pages were inspected. `visual-review.json` binds that review to the final PDF and Word bytes. This is same-assistant editorial QA, not independent scientific review.

The manuscript's new section 17.2 reports the completed Lean coverage and preserves the four explicit formalization limits. No new theorem, adopted axiom, experimental measurement, implementation-refinement claim, or independent-review claim was added.
