# PAL v2.3 and CHARTER publication account

Christopher D. Pang authorized publication of the proofs and receipts in
PAL-Lean-Audit and a short summary/link in Hearthline after the local checks.
The proposal is published through a draft pull request; merge and PAL adoption
remain separate. No supplied DOCX is redistributed by this change.

The [local report](../../docs/generated/pal-v23-charter-local-checks.md) and
[original execution receipt](results.json) describe the completed Windows
execution. Their LOCAL_ONLY and CI NOT_RUN fields describe that earlier capture,
not the later state of this pull request. Original attempt directories remain
unchanged, including the attempt rejected when report metadata changed mid-run.

The [publication input lock](publication-inputs.json) binds the same inputs
using canonical LF text hashes. This accounts only for Git's CRLF/LF checkout
conversion. The original raw input hashes, raw DOCX hashes, log hashes, and
dependency receipts remain preserved. The lock is same-branch provenance and
becomes externally addressable with its commit; it is not an authenticity or
adoption authority.

From a fresh checkout with the pinned Lean/Mathlib environment:

```text
python3 Audit/pal-v23-charter/check_publication.py --check
python3 Audit/pal-v23-charter/check_publication.py --replay --lake lake
```

The first command verifies the preserved evidence and generated report. The
second actually rebuilds the declared experimental library, executes all 27
axiom reports, compares their exact names and dependencies with the local
receipt, and runs the bundled kernel checker. It writes a new execution receipt
under artifacts/pal23-charter-replay without replacing the original local run.

Neither command claims to reread missing DOCX files. Optional byte verification
uses `--source-dir <directory>` containing the six supplied filenames from
[source-manifest.json](source-manifest.json). That directory is supplied by the
caller, so no machine-specific E: path is required for publication replay. Source
paragraph extracts can be reconstructed locally; they are not required for
Lean compilation and are not silently substituted for source documents.

The dedicated GitHub workflow uploads `execution.json`, the exact axiom output,
and kernel output. Its receipt records the proposed PR head separately from the
checked-out synthetic merge commit and tree. The historical Lean audit workflow
continues to run independently. CI replay does not turn partial source coverage
into full conformance, independent scientific confirmation, or source adoption.
