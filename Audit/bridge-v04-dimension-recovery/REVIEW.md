# Controller audit review

Normalized claim: over a field, the actual BRIDGE four-sector quotients satisfy dim T = dim C + dim Gv + dim H + dim V when T is finite-dimensional. For the actual residual readout s: T/B -> range(r)/r(B), a linear answer a factors as d composed with s exactly when range(hiddenToDefect B (ker r)) is contained in ker(a). An identity decoder exists exactly when the hidden quotient is subsingleton, equivalently ker(r) is contained in B.

**Primary verdict: proved as written**, for these normalized, explicitly typed linear-algebra claims. This verdict applies to the selected finite-accounting and residual-recovery claims, not to all of BRIDGE or every sentence in P0193-P0199.

The controller executed the frozen implementation at checkout 9a061b96247491d7004554756db4e834f9d78619 with candidate files present. Execution finished 2026-09-12T06:47:33.020813+00:00: PASS_BRIDGE_DIMENSION_RECOVERY. All sixteen current commands passed, including two new module builds, exact axiom inventories, bundled kernel checks, repository policy/migration/report checks, and a preserved-tree replay. The latter independently executed the previous eighteen-command procedure at 1babbcd19b51bba46dc9a51365dcadbe31bf1763. That historical checkout is a separate identity, not current-head coverage or an independent mathematical lineage.

Dependency graph: inherited quotient definitions and named maps -> collision subtype equivalences and quotient rank-nullity -> four-sector dimension formula. Inherited residual exactness and canonical readout comparison -> actual residual kernel and surjectivity -> quotient decoder construction -> answer factorization criterion -> identity decoder, hidden-zero and kernel-containment equivalences. The countercases use the same explicit definitions and rational vector spaces.

| Obligation | Disposition | Evidence |
|---|---|---|
| Actual C, Gv, H, V quotient definitions | Passed | BridgeDimension uses the inherited submodule and quotient types |
| Finite-dimensional hypothesis in the sum | Passed | bridge_four_sector_finrank |
| Dropping that hypothesis for natural-number finrank | Refuted overclaim | four_sector_finrank_requires_finite_dimensional_countercase |
| H used through its injection into D | Passed | ker_residualReadout |
| Both directions of the requested-answer criterion | Passed | answer_decodable_iff and answerDecoder_comp_residualReadout |
| Actual identity decoder, H zero, and ker(r) <= B | Passed | residual_identity_decoder_iff_injective, full_residual_identity_recovery_iff_hidden_subsingleton, residual_identity_decoder_iff_kernel_le |
| Coarser answer does not imply full identity recovery | Checked countercase | Rational first-coordinate example with B = bottom |
| Exact source bytes and original OOXML | Passed locally | DOCX SHA256 and 95 exact retained paragraphs |
| Separate generated-span answer factorization in P0195 | OPEN_MANUAL | Explicit recovery ledger disposition |
| Frame morphisms, return dynamics, geometry and Hodge applications | Out of scope | No such theorem is asserted |

The infinite-dimensional countercase uses T = Q times finitely supported rational sequences, B = range(inl), K = bottom. Its natural-number finrank sector sum is one while ambient finrank is zero under Lean's infinite-dimensional convention. This does not refute a cardinal-dimension formula. The recovery countercase decodes a nonzero first-coordinate answer while losing the second coordinate. No effective reconstruction procedure or physical storage claim follows from a noncomputable linear decoder.

There are eighteen new entries: {'PROVED_FROM_DECLARED_RULES': 14, 'COUNTERMODEL_TO_OVERCLAIM': 2, 'CONSISTENT_REALIZATION': 2}. The nineteen prior diagram/readout entries and fourteen prior four-sector entries are separate populations. Helpers and aggregate statements share dependencies. Eighteen altered-receipt guards rejected their mutations after the baseline validated. Three real missing-executable/nonzero-exit/timeout probes passed as tooling tests, not mathematical countercases. Nested historical command logs, inputs, axiom inventories, and receipt hashes are verified as well as the new outputs.

Source review corrected a nonliteral ellipsis quotation, incomplete recovery ledger rows, and a predecessor workflow hash that had been taken from the wrong working state. The final record uses literal source excerpts, one row per inventoried declaration, and predecessor hashes read from the exact Git object. Historical receipts and source claims were not rewritten. The first two dimension helper declarations are valid more generally than the conservative finite-dimensional context listed in their ledger rows.

Receiver-local selection: Hearthline selects the dimension and recovery Keepers' exact observations about quotient correspondence, both decoder implications, and the two valid countercases as review evidence within this candidate audit. The controller checked the code and actual execution; this selection grants no transitive authority, source adoption, or merge permission. Source correspondence and agent review remain distinct from kernel checking. Open PAL obligations O04, O25 and D-FIRST-OCCURRENCE remain OPEN.

Publication and CI are a separate subsequent receipt. Reopen for changed source bytes, definitions, assumptions, dependency/toolchain identities, code or receipts. The strongest safe result is this selected linear realization; the next source-specific gap is P0195's direct generated-span answer criterion.

`MODEL_NOTE provenance: supplied BRIDGE-v0.4, frozen worker files, paired source reviews, controller execution; producer: Hearthline controller; bundle: BRIDGE-RECOVERY-20260912-01; receiver: Christopher D. Pang; formation_timing: AFTER_NEW_STEERING; steering_trace: user merged PR14 and asked to keep going; work_summary: Eighteen new declarations passed local source, build, axiom, kernel and preserved-tree replay checks; review: finite accounting and residual recovery are checked within their explicit linear assumptions; uncertainty: CI is a separate subsequent receipt and the generated-span criterion remains open; suggestion: NONE; authority_status: UNPROMOTED; promotion_rule: RECEIVER_ONLY_LOCAL_NON_TRANSITIVE`
