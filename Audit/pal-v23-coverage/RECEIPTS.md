# Receipt contract

The coverage receipt binds the three claim ledgers to exact Lean declarations, source paragraph excerpts, DOCX hashes, signatures, imported axioms, command logs, input hashes, the saved predecessor receipt, and checkout identity. Stored excerpt text is recomputed from its OOXML; when `--source-dir` is supplied, each stored XML paragraph is also matched to the original DOCX bytes and hash. CI checks committed snapshots and records that original DOCX verification was not performed there. CI labels and run identifiers are environment-supplied and are not independently attested by this runner.

The predecessor is the PAL v2.3 roundtrip receipt from merged PR 17. Its saved receipt is checked as preserved evidence; this lane does not claim to rerun that historical Lean audit. Failed attempts are retained in unique evidence directories and do not replace the last passing result.

Run locally with `python Audit/pal-v23-coverage/run.py --run --lake lake --source-dir <directory-containing-the-five-source-DOCX-files>`. Verify the saved receipt using `--check`; use `--replay --output-dir <new-directory>` for a separate replay.
