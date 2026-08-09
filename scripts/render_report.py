#!/usr/bin/env python3
"""Render deterministic Markdown and SVG views of the PAL claim ledger."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections import Counter
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = ROOT / "Audit" / "claim-ledger.json"
SUMMARY = ROOT / "docs" / "generated" / "summary.md"
CHART = ROOT / "docs" / "generated" / "outcomes.svg"
STATUSES = ["PROVED", "COUNTERMODEL", "EXPECTED_REJECTION", "OPEN", "NOT_FORMALIZED"]
COLORS = {
    "PROVED": "#2f855a",
    "COUNTERMODEL": "#2b6cb0",
    "EXPECTED_REJECTION": "#805ad5",
    "OPEN": "#d69e2e",
    "NOT_FORMALIZED": "#718096",
}


def load_ledger() -> dict:
    with LEDGER.open(encoding="utf-8") as handle:
        data = json.load(handle)
    unknown = sorted({claim["status"] for claim in data["claims"]} - set(STATUSES))
    if unknown:
        raise ValueError(f"Unknown status values: {unknown}")
    return data


def render_summary(data: dict, counts: Counter) -> str:
    lines = [
        "# Generated audit status",
        "",
        f"- Run: {data['run_id']}",
        f"- Controlling release: {data['controlling_release']}",
        f"- DOI: [{data['controlling_doi']}](https://doi.org/{data['controlling_doi']})",
        f"- Run receipt: [{data['run_receipt']}](../../{data['run_receipt']})",
        f"- Authority ceiling: {data['authority_ceiling']}",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| {status} | {counts[status]} |" for status in STATUSES)
    lines.extend(
        [
            "",
            "_Counts cover the ten selected T-targets only; the separate O04/O25 first-occurrence debt remains OPEN._",
            "",
            "## Claim ledger",
            "",
            "| Test | Target | Status | Evidence |",
            "|---|---|---|---|",
        ]
    )
    for claim in data["claims"]:
        lines.append(
            f"| {claim['id']} | {claim['title']} | **{claim['status']}** | {claim['evidence']} |"
        )
    lines.extend(["", "_Generated from Audit/claim-ledger.json; do not edit by hand._", ""])
    return "\n".join(lines)


def render_svg(data: dict, counts: Counter) -> str:
    width, height = 920, 390
    left, top, row_height, max_bar = 220, 82, 52, 590
    maximum = max(max(counts.values()), 1)
    rows: list[str] = []
    for index, status in enumerate(STATUSES):
        y = top + index * row_height
        bar_width = round(max_bar * counts[status] / maximum)
        rows.extend(
            [
                f'<text x="{left - 16}" y="{y + 22}" text-anchor="end" class="label">{escape(status)}</text>',
                f'<rect x="{left}" y="{y}" width="{bar_width}" height="30" rx="5" fill="{COLORS[status]}"/>',
                f'<text x="{left + bar_width + 12}" y="{y + 22}" class="count">{counts[status]}</text>',
            ]
        )
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" viewBox="0 0 {width} {height}">',
            f'<title id="title">PAL Lean Audit outcomes for {escape(data["run_id"])}</title>',
            '<desc id="desc">Horizontal bars count the ten selected T-targets by audit status; O04/O25 is tracked separately and remains open.</desc>',
            '<rect width="100%" height="100%" fill="#f7fafc"/>',
            '<style>.title{font:700 24px system-ui,sans-serif;fill:#1a202c}.sub{font:14px system-ui,sans-serif;fill:#4a5568}.label{font:600 14px ui-monospace,monospace;fill:#2d3748}.count{font:700 15px system-ui,sans-serif;fill:#1a202c}</style>',
            '<text x="28" y="36" class="title">PAL Lean Audit — outcome counts</text>',
            f'<text x="28" y="60" class="sub">{escape(data["run_id"])} · bounded results only; O04/O25 remains OPEN</text>',
            *rows,
            "</svg>",
            "",
        ]
    )


def write_or_check(path: pathlib.Path, content: str, check: bool) -> bool:
    if check:
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if actual != content:
            print(f"Generated file is stale: {path.relative_to(ROOT)}", file=sys.stderr)
            return False
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated files are stale")
    args = parser.parse_args()
    data = load_ledger()
    counts = Counter(claim["status"] for claim in data["claims"])
    ok = write_or_check(SUMMARY, render_summary(data, counts), args.check)
    ok = write_or_check(CHART, render_svg(data, counts), args.check) and ok
    if ok:
        action = "Verified" if args.check else "Rendered"
        print(f"{action} {SUMMARY.relative_to(ROOT)} and {CHART.relative_to(ROOT)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
