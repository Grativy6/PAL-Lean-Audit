# C2 interval-slack batch notes

This batch formalizes the PAL v2.3 Mathematical Realization Atlas interval rules at P1047–P1067 over exact rational intervals. The source defines slack as `[-c_hi,-c_lo]`, requires `ε ≥ 0`, classifies the strict positive/negative regions as FEASIBLE/VIOLATED, assigns the closed band to CONTACT, and calls the residual UNRESOLVED. For ordered intervals and nonnegative tolerance, the three named regions are disjoint and their residual covers the remaining cases. Thus no in-domain gap or overlap was found in these inequalities.

The model keeps endpoint validity explicit. A checked counterexample uses malformed interval `[2,-2]` with `ε=1`: all three predicates hold, but the interval is unordered. This is outside the source's ordered-interval conditions and demonstrates why that condition must remain attached to partition claims. The equality fixtures at `s=ε` and `s=-ε` are CONTACT, consistent with strict FEASIBLE/VIOLATED inequalities and the closed CONTACT band. A straddling interval `[-2,2]` at `ε=1` is UNRESOLVED.

The optional budget branch is limited to a fixed budget within one grant epoch: for `s_k=B-c_k`, nondecreasing cumulative consumption makes slack nonincreasing. It does not model top-ups or epoch transitions. The rational encoding does not establish units, evaluator correctness, interval calibration, empirical measurement, permission, or authority; the source itself lists these as assumptions or ceilings.

Source input: `PAL_v2.3-M_Mathematical_Realization_Atlas.docx`, SHA-256 `c053292376363edd6fc743f0f2e31e3bb3850edc78ade3a289bbb07e7e8452c5`. Exact paragraphs are preserved in `source-excerpts.json`. This is a bounded v2.3-source realization; it does not adopt or amend PAL v2.4.

