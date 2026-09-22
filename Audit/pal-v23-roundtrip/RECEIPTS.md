# Receipt contract

The run receipt preserves the exact source snapshot hashes, theorem inventory, per-declaration signature and axiom outputs, input hashes before and after execution, command identities and log hashes, predecessor saved-receipt hash, CI head/merge/run identity, and the authority ceiling. The five original DOCX files and all 151 indexed Atlas paragraphs are checked only when `--source-dir` is supplied locally. CI checks committed snapshots and records no original DOCX verification.

The saved predecessor audit is validated through its own `--check` command. This lane does not claim that preserving its prior receipt freshly replays it. Failed attempts keep their command output in a unique evidence directory and do not replace the last passing result.

Run locally with `python Audit/pal-v23-roundtrip/run.py --run --lake lake --source-dir <directory-containing-the-five-source-DOCX-files>`. Verify the saved receipt using `--check`; create a separate replay using `--replay --output-dir <new-directory>`.
