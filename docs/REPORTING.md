# Audit reporting rules

The claim ledger is the source of chart data. Generated graphics are explanatory views, not independent evidence.

## Status rules

- `PROVED` requires a compiling theorem, an exact statement, and a dependency receipt.
- `COUNTERMODEL` requires a compiling construction that addresses the stated stronger claim.
- `EXPECTED_REJECTION` requires an intentional negative fixture with a stable expected diagnostic.
- `OPEN` records an attempted but unclosed burden without treating failure as refutation.
- `NOT_FORMALIZED` records that no adequate Lean statement has been adopted.

`EXPECTED_REJECTION` inherits the scope of its fixture. T05 is a lexical check
for the literal standalone identifiers `Omega` and `Ω`; it is not a semantic
proof that differently named surrogates are absent.

Attack Run 0002 adds a second status dimension: every C21 proposition remains
`CANDIDATE` even when its exact bounded Lean target is `PROVED` or a stronger
claim receives a checked `COUNTERMODEL`. Formal status is evidence for Gate 4;
it is not canonical adoption.

## Metric separation

Selected-test outcomes and source obligations are different populations. The
outcome table may therefore report `OPEN = 0` while the source ledger retains
an open obligation. Reports and charts must show these counts separately and
must not add them into one total.

For Attack Run 0001, O04 and O25 are two interfaces to one shared open source
obligation, `D-FIRST-OCCURRENCE`; the source-obligation count is therefore one.
The report generator verifies that this separate ledger population exactly
matches the open burdens retained in the detailed run receipt.

Attack Run 0002 retains the same one open source obligation in a separate
candidate ledger. Counts from the two attack runs are not combined, and neither
run may relabel O04/O25 as a closed selected-test outcome.

Attack Run 0002 also records semantic-surrogate review as a third, manual
population. It is not a Lean result and not a PAL-source obligation. Reports
must show it separately so a passing lexical identifier check cannot be read as
semantic discharge.

Required negative guards form a fourth disposition table. A guard may reuse a
selected countermodel, preservation theorem, or the same open manual semantic
review; that overlap must be stated, and negative-guard rows are never summed as
independent claims.

## Version-control identity receipts

Pull-request runs must record the proposed `pr_head_sha` separately from the
`tested_merge_sha` checked out by GitHub Actions. The final merge commit, if one
is later adopted, is a third identity and may be recorded by an explicit
post-run amendment; it must not be substituted retroactively for either value.

Before CI runs, candidate receipts leave live pull-request identities null and
route them to the uploaded environment artifact. They must not guess a future
head or synthetic merge commit and thereby invalidate their own receipt.

Checker or exporter incompatibilities are tooling results, not PAL results. They must be retained in the run receipts and may not be reported as proofs, countermodels, or expected rejections.

## Benchmark rules

Build duration, memory, cache behavior, and runner identity are measurements of a particular execution environment. They are not evidence that a theorem is stronger, more important, or more ontologically accurate.

No benchmark baseline may be invented. Missing data remains missing.

## Regeneration

Run:

```bash
python3 scripts/render_report.py

python3 scripts/render_report.py \
  --ledger Audit/attack-run-0002-claim-ledger.json \
  --summary docs/generated/attack-run-0002-summary.md \
  --chart docs/generated/attack-run-0002-outcomes.svg
```

CI uses `--check` for both commands to ensure each committed SVG and Markdown
receipt matches its own ledger.
