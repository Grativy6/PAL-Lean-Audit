# BRIDGE v0.4 residual recovery review

Source basis: supplied `BRIDGE_v0.4.docx`, SHA-256 `a13d91a728ab6da2a5654b3263a595242397d7fb8edb17cffafdcf32036a2470`; selected original OOXML paragraphs P0195-P0199 in `Audit/bridge-v04-four-sector/source-excerpts.json`.

The audited linear realization keeps `H = ker(r)/(B∩ker(r))` typed as a quotient. The phrase `H⊆ker(a)` is realized as `range(hiddenToDefect B (ker r))≤ker(a)`, where `hiddenToDefect` is the pre-existing named injection into `D=T/B`. No ambient-submodule identification, complement, representative choice, geometric interpretation, PAL adoption, or source amendment is asserted.

Checked results establish the actual residual readout's surjectivity and kernel, linear answer factorization exactly through that map, and an explicit left-inverse decoder for residual identity exactly when `ker(r)≤B`. The rational `fst` countercase demonstrates an induced first-coordinate answer that decodes although full identity does not.

P0195's separate generated-span statement about `r|B` has not been rephrased as a second decoder theorem here. It remains `OPEN_MANUAL` in `recovery-claims.json`; this preserves the distinction between the checked residual criterion and the unimplemented generated-span clause. Finite-dimensional accounting belongs to the sibling dimension lane.
