# Receipt contract

`run.py` records a bounded local or GitHub replay receipt for the generated-span factorisation lane. Its fixed input set includes the predecessor lock, the committed source snapshots and audit documents, the generated-span Lean modules and claims, and this lane's workflow. It does not glob the repository and does not rerun the historical replay.

The DOCX and its 95 preserved OOXML paragraphs are checked only when `--source-file` is supplied locally. CI checks the committed source snapshots and records `performed: false` for the absent local DOCX. A passing receipt reports the exact command identities, log hashes, input hashes, declaration inventory, allowed imported axioms, open obligations, and clean-tree status.
