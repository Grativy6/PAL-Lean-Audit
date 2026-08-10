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

Attack Runs 0001 and 0002 retain this PAL v2.0-scoped vocabulary and history.
Do not relabel their claims under PAL v2.1. Every new run is controlled by PAL
v2.1, DOI [`10.5281/zenodo.21864767`](https://doi.org/10.5281/zenodo.21864767),
with source identity routed through the published
[`Audit/releases/pal-v2.1-source-manifest.json`](../Audit/releases/pal-v2.1-source-manifest.json).

## Attack Run 0003 classifications

Attack Run 0003 is a PAL-led audit of declared Lean realizations. It is not
Lean proving PAL, a canon amendment, adoption authority, or obligation closure.
Its eight clarification routes are `D16`-`D23`, paired respectively with
`SC-19.1`-`SC-19.8` and `T33`-`T40`.

Use exactly these seven classifications:

- `PROVED_FROM_DECLARED_RULES` - the exact theorem follows from recorded rules, definitions, assumptions, and dependencies.
- `CONSISTENT_REALIZATION` - the declared bounded realization is instantiated in the audited environment, without claiming PAL or meta-consistency has been proved.
- `ASSUMPTION_BOUND` - disclosed assumptions materially limit the result's transfer beyond the model.
- `COUNTERMODEL_TO_OVERCLAIM` - a checked construction defeats a stronger unlicensed claim without refuting PAL.
- `EXPECTED_REJECTION` - an intentional negative fixture receives its recorded diagnostic.
- `OPEN_MANUAL` - human source or semantic review remains open; this is not a Lean result.
- `TRANSLATION_AMBIGUITY` - materially different formal translations remain live and no unique encoding is claimed.

Each classified target must record the controlling PAL route, exact formal
statement or fixture, assumptions, dependencies and imported axioms, evidence,
authority ceiling, residual, and reopening address. Formal evidence is not
human adoption authority.

Omega remains metalinguistic unresolved possibility. O04 and O25 remain
separate `OPEN` interfaces to the one `D-FIRST-OCCURRENCE` debt. The phrase
`occurrence-closed, source-open` is explanatory shorthand only; it is not a
primitive, layer, or PAL status.

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

Attack Run 0003 must keep at least four populations distinct:

1. machine and fixture classifications (`PROVED_FROM_DECLARED_RULES`, `CONSISTENT_REALIZATION`, `ASSUMPTION_BOUND`, `COUNTERMODEL_TO_OVERCLAIM`, and `EXPECTED_REJECTION`);
2. manual and translation dispositions (`OPEN_MANUAL` and `TRANSLATION_AMBIGUITY`);
3. PAL-source obligations, including the one `D-FIRST-OCCURRENCE` debt exposed through O04 and O25; and
4. benchmark measurements.

Each population has its own denominator and count table. Do not sum across
populations, convert an overlap into an independent success, or combine the
Attack Run 0003 counts with either historical run.

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

Attack Run 0003 benchmark reports must contain actual measurements together
with the command, environment and runner identity, tool versions, repetition
method, units, and missing-data account. Numerical correctness scores are
prohibited: correctness is represented by exact statements, checks, receipts,
and classifications, not an invented percentage or composite score.

## Attack Run 0003 files

- [PAL v2.1 source manifest](../Audit/releases/pal-v2.1-source-manifest.json)
- [PAL v2.1 adoption receipt](../Audit/releases/pal-v2.1-adoption-receipt.json)
- [PAL v2.0-to-v2.1 migration receipt](../Audit/migrations/pal-v2.0-to-v2.1-migration-receipt.json)
- [Attack Run 0003 receipt](../Audit/attack-run-0003-receipt.json)
- [Attack Run 0003 claim ledger](../Audit/attack-run-0003-claim-ledger.json)
- [Attack Run 0003 summary](generated/attack-run-0003-summary.md)
- [Attack Run 0003 classifications chart](generated/attack-run-0003-classifications.svg)
- [Attack Run 0003 dependency chart](generated/attack-run-0003-dependencies.svg)
- [Attack Run 0003 benchmarks](generated/attack-run-0003-benchmarks.md)

These paths are generated or machine-readable receipts. Their exact contents,
not their filenames, carry the branch-local evidence and authority ceilings.

## Regeneration

Run:

```bash
python3 scripts/render_report.py

python3 scripts/render_report.py \
  --ledger Audit/attack-run-0002-claim-ledger.json \
  --summary docs/generated/attack-run-0002-summary.md \
  --chart docs/generated/attack-run-0002-outcomes.svg

python3 scripts/render_migration_report.py
python3 scripts/collect_attack_run_0003_benchmarks.py \
  --published-zip /path/to/PAL_v2.1_Zenodo_Release.zip
python3 scripts/render_attack_run_0003.py
```

The collector performs the measured build, dependency capture, source/migration
verification, historical regressions, policy checks, report checks, and
blocking `leanchecker` receipt before writing the benchmark/evidence bundle.
CI uses `--check` for every generator to ensure each committed SVG and Markdown
receipt matches its own machine source.
