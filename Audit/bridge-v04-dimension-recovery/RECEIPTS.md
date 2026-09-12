# BRIDGE finite-dimensional and recovery receipt account

This lane audits only the declared linear realization for BRIDGE v0.4 P0193-P0199. It records finite-dimensional assumptions, the named embedding of the abstract hidden quotient into the defect space, and factorization/recovery statements. It does not amend the manuscript, adopt PAL claims, close PAL obligations, or establish geometric, Hodge, or frame-morphism results.

`run.py --check` validates the saved local receipt. `--replay` creates fresh evidence. Supplying `--source-file` separately verifies the supplied DOCX bytes and all 95 retained OOXML paragraphs; CI replays committed source excerpts and Lean declarations without claiming access to that raw DOCX.

PR14 is replayed only from its pinned historical checkout (`1babbcd19b51bba46dc9a51365dcadbe31bf1763`). The helper records that checkout and its own replay output, so new files cannot silently widen historical coverage.

The failure probe retains a missing executable, a nonzero command, and a timeout as tooling evidence only. These receipts do not count as theorem results or mathematical countercases.
