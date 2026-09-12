# PAL, CHARTER, and BRIDGE 13-declaration publication account

This directory carries a reproducible publication supplement for the completed
local audit, not a replacement receipt. It records four PAL v2.3, four
CHARTER v1.0, and five BRIDGE v0.4 declarations. The source mappings are
bounded realizations; they neither adopt the documents nor prove full source
conformance, scientific results, or external theorem coverage.

The original local run remains in [results.json](results.json). Its raw source
DOCX hashes, raw execution logs, command order, 13-declaration axiom inventory,
and source obligations are verified without modification. The only historical
input that later changed is `Audit.lean`: [publication-inputs.json](publication-inputs.json)
checks its historical `e00ffc6` bytes through Git and checks the inherited
`06ad391` `Audit.lean` and `Audit/BridgeEndpoint.lean` bytes separately.

The tracked [selected excerpts](source-excerpts.json) are only the quotations
referenced by the 13 claim mappings. They are not an extracted corpus and do
not silently stand in for the seven supplied DOCX files.

From a fresh checkout with the pinned Lean environment:

```text
python3 Audit/recent-work-20260911/check_publication.py --check
python3 Audit/recent-work-20260911/check_publication_guards.py --output artifacts/recent-work-20260911-guards/publication-guard-results.json
python3 Audit/recent-work-20260911/check_publication.py --replay --lake lake --output-dir artifacts/recent-work-20260911-replay
```

The first command validates preserved local evidence and selected excerpts. The
second proves the checker rejects missing or duplicate commands and claims,
changed logs, inputs, axioms, source excerpts, and an improperly closed source
obligation. The replay writes a fresh receipt; it never overwrites the local
receipt. It rebuilds `Pal23Followup`, `CharterFollowup`, and `Bridge`, records
their exact `#print axioms` outputs, compares them to the original dependency
inventory, and invokes the bundled Lean kernel checker for each module.

GitHub CI needs no local document path. Its receipt records the checked-out
merge commit, PR head SHA, GitHub run ID, and clean-worktree status. To verify
the original supplied DOCX bytes as a separate local action, pass a directory
containing the seven manifest filenames:

```text
python3 Audit/recent-work-20260911/check_publication.py --check --source-dir D:\\source-docx
```

That optional check reports raw document identity only. It does not elevate
source correspondence from review to proof. PAL open obligations O04, O25,
and D-FIRST-OCCURRENCE remain open; BRIDGE's Hodge and geometric claims remain
outside this batch.
