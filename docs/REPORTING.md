# Audit reporting rules

The claim ledger is the source of chart data. Generated graphics are explanatory views, not independent evidence.

## Status rules

- `PROVED` requires a compiling theorem, an exact statement, and a dependency receipt.
- `COUNTERMODEL` requires a compiling construction that addresses the stated stronger claim.
- `EXPECTED_REJECTION` requires an intentional negative fixture with a stable expected diagnostic.
- `OPEN` records an attempted but unclosed burden without treating failure as refutation.
- `NOT_FORMALIZED` records that no adequate Lean statement has been adopted.

## Benchmark rules

Build duration, memory, cache behavior, and runner identity are measurements of a particular execution environment. They are not evidence that a theorem is stronger, more important, or more ontologically accurate.

No benchmark baseline may be invented. Missing data remains missing.

## Regeneration

Run:

```bash
python3 scripts/render_report.py
```

CI uses `--check` to ensure the committed SVG and Markdown receipt match `Audit/claim-ledger.json`.
