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
DEFAULT_LEDGER = ROOT / "Audit" / "claim-ledger.json"
DEFAULT_SUMMARY = ROOT / "docs" / "generated" / "summary.md"
DEFAULT_CHART = ROOT / "docs" / "generated" / "outcomes.svg"
STATUSES = ["PROVED", "COUNTERMODEL", "EXPECTED_REJECTION", "OPEN", "NOT_FORMALIZED"]
COLORS = {
    "PROVED": "#2f855a",
    "COUNTERMODEL": "#2b6cb0",
    "EXPECTED_REJECTION": "#805ad5",
    "OPEN": "#d69e2e",
    "NOT_FORMALIZED": "#718096",
}


def load_ledger(ledger_path: pathlib.Path) -> dict:
    with ledger_path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    unknown = sorted({claim["status"] for claim in data["claims"]} - set(STATUSES))
    if unknown:
        raise ValueError(f"Unknown status values: {unknown}")
    unknown_negative = sorted(
        {fixture["status"] for fixture in data.get("negative_fixtures", [])}
        - set(STATUSES)
    )
    if unknown_negative:
        raise ValueError(f"Unknown negative-fixture status values: {unknown_negative}")
    if "open_source_obligations" not in data:
        raise ValueError("claim ledger must declare open_source_obligations, even when empty")
    invalid_obligations = [
        obligation["id"]
        for obligation in data["open_source_obligations"]
        if obligation.get("status") != "OPEN"
    ]
    if invalid_obligations:
        raise ValueError(
            "open_source_obligations must retain OPEN status: "
            f"{invalid_obligations}"
        )
    receipt_path = ROOT / data["run_receipt"]
    with receipt_path.open(encoding="utf-8") as handle:
        receipt = json.load(handle)
    identity_fields = ["run_id", "controlling_release", "controlling_doi"]
    if data.get("strict_receipt_consistency"):
        identity_fields.append("authority_ceiling")
    for field in identity_fields:
        if data.get(field) != receipt.get(field):
            raise ValueError(f"claim-ledger {field} does not match the run receipt")
    ledger_claim_statuses = {
        claim["id"]: claim["status"] for claim in data["claims"]
    }
    receipt_claim_statuses = {
        claim["id"]: claim["result"] for claim in receipt["claims"]
    }
    if len(ledger_claim_statuses) != len(data["claims"]):
        raise ValueError("claim ledger contains duplicate claim ids")
    if len(receipt_claim_statuses) != len(receipt["claims"]):
        raise ValueError("run receipt contains duplicate claim ids")
    if ledger_claim_statuses != receipt_claim_statuses:
        raise ValueError("claim-ledger outcomes do not match the run receipt")
    if data.get("strict_receipt_consistency"):
        def normalized_claim(claim: dict) -> dict:
            normalized = dict(claim)
            normalized.pop("evidence", None)
            if "status" in normalized:
                normalized["result"] = normalized.pop("status")
            return normalized

        ledger_claims = sorted(
            (normalized_claim(claim) for claim in data["claims"]),
            key=lambda claim: claim["id"],
        )
        receipt_claims = sorted(
            (normalized_claim(claim) for claim in receipt["claims"]),
            key=lambda claim: claim["id"],
        )
        if ledger_claims != receipt_claims:
            raise ValueError("claim-ledger claim records do not match the run receipt")

    def rows(value: object) -> list[dict]:
        if value is None:
            return []
        if isinstance(value, dict):
            return [value]
        if isinstance(value, list):
            return value
        raise ValueError("receipt comparison block must be an object or array")

    for field in (
        "candidate_adoption_statuses",
        "manual_source_review_controls",
        "negative_fixtures",
    ):
        ledger_rows = sorted(rows(data.get(field)), key=lambda item: item["id"])
        receipt_rows = sorted(rows(receipt.get(field)), key=lambda item: item["id"])
        if ledger_rows != receipt_rows:
            raise ValueError(f"claim-ledger {field} do not match the run receipt")
    for field in ("input_lock", "formal_environment"):
        ledger_block = data.get(field, {})
        receipt_block = receipt.get(field, {})
        if any(receipt_block.get(key) != value for key, value in ledger_block.items()):
            raise ValueError(f"claim-ledger {field} does not match the run receipt")
    if "source_hashes_verified" in data and data["source_hashes_verified"] != receipt.get(
        "source_hashes_verified", {}
    ):
        raise ValueError("claim-ledger source hashes do not match the run receipt")
    data["_receipt_run_status"] = receipt.get("run_status")
    data["_receipt_status"] = receipt.get("receipt_status")
    data["_human_decision_status"] = receipt.get("human_decision_status")
    ledger_obligations = sorted(
        (
            obligation["id"],
            tuple(obligation["interfaces"]),
            obligation["status"],
            obligation["reason"],
        )
        for obligation in data["open_source_obligations"]
    )
    receipt_obligations = sorted(
        (
            obligation["address"],
            tuple(obligation["interfaces"]),
            obligation["status"],
            obligation["reason"],
        )
        for obligation in receipt.get("open_burdens", [])
    )
    if ledger_obligations != receipt_obligations:
        raise ValueError("claim-ledger source obligations do not match the run receipt")
    return data


def render_summary(data: dict, counts: Counter) -> str:
    target_population_label = data.get(
        "target_population_label", "Selected T-target outcomes"
    )
    generated_source_note = data.get(
        "generated_source_note", "Audit/claim-ledger.json"
    )
    manual_controls = data.get("manual_source_review_controls", [])
    if isinstance(manual_controls, dict):
        manual_controls = [manual_controls]
    negative_fixtures = data.get("negative_fixtures", [])
    lines = [
        "# Generated audit status",
        "",
        f"- Run: {data['run_id']}",
        f"- Controlling release: {data['controlling_release']}",
        f"- DOI: [{data['controlling_doi']}](https://doi.org/{data['controlling_doi']})",
        f"- Run receipt: [{data['run_receipt']}](../../{data['run_receipt']})",
    ]
    if data.get("_receipt_run_status"):
        lines.append(f"- Run status: **{data['_receipt_run_status']}**")
    if data.get("_receipt_status"):
        lines.append(f"- Receipt status: **{data['_receipt_status']}**")
    candidate_rows = data.get("candidate_adoption_statuses", [])
    if candidate_rows:
        candidate_ids = ", ".join(row["id"] for row in candidate_rows)
        adoption_states = {row["adoption_status"] for row in candidate_rows}
        adoption_summary = (
            adoption_states.pop() if len(adoption_states) == 1 else "MIXED"
        )
        lines.append(
            f"- Candidate adoption: **{adoption_summary}** for {candidate_ids}"
        )
    if data.get("_human_decision_status"):
        lines.append(f"- Human decision: **{data['_human_decision_status']}**")
    lines.extend(
        [
            f"- Authority ceiling: {data['authority_ceiling']}",
            "",
            f"## {target_population_label}",
            "",
            "| Outcome status | Count |",
            "|---|---:|",
        ]
    )
    lines.extend(f"| {status} | {counts[status]} |" for status in STATUSES)
    lines.extend(
        [
            "",
            "_These counts cover selected test outcomes only._",
            "",
            "## Open PAL-source obligations (separate population)",
            "",
            "| Obligation | Interfaces | Status | Reason |",
            "|---|---|---|---|",
        ]
    )
    for obligation in data["open_source_obligations"]:
        lines.append(
            f"| {obligation['id']} | {', '.join(obligation['interfaces'])} | "
            f"**{obligation['status']}** | {obligation['reason']} |"
        )
    lines.extend(
        [
            "",
            "_Selected-test OPEN outcomes and open PAL-source obligations are distinct metrics and are never summed._",
        ]
    )
    if manual_controls:
        lines.extend(
            [
                "",
                "## Open manual review controls (separate population)",
                "",
                "| Control | Type | Status | Scope |",
                "|---|---|---|---|",
            ]
        )
        for control in manual_controls:
            lines.append(
                f"| {control['id']} | {control['control_type']} | "
                f"**{control['status']}** | {control['scope']} |"
            )
        lines.extend(
            [
                "",
                "_Manual review controls are neither formal outcomes nor PAL-source obligations._",
            ]
        )
    if negative_fixtures:
        lines.extend(
            [
                "",
                "## Required negative-guard dispositions (separate population)",
                "",
                "| Fixture | Guard | Disposition | Control | Evidence or diagnostic |",
                "|---|---|---|---|---|",
            ]
        )
        for fixture in negative_fixtures:
            lines.append(
                f"| {fixture['id']} | {fixture['title']} | **{fixture['status']}** | "
                f"{fixture['control_type']} | {fixture['evidence_or_diagnostic']} |"
            )
        lines.extend(
            [
                "",
                "_Negative guards may reuse selected-target evidence or an open manual control. They are dispositions, not additional independent claims, and are not summed with the other populations._",
            ]
        )
    lines.extend(
        [
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
    lines.extend(
        ["", f"_Generated from {generated_source_note}; do not edit by hand._", ""]
    )
    return "\n".join(lines)


def render_svg(data: dict, counts: Counter) -> str:
    manual_controls = data.get("manual_source_review_controls", [])
    if isinstance(manual_controls, dict):
        manual_controls = [manual_controls]
    open_manual_controls = [
        control for control in manual_controls if control.get("status") == "OPEN"
    ]
    open_manual_count = len(open_manual_controls)
    negative_fixtures = data.get("negative_fixtures", [])
    negative_counts = Counter(fixture["status"] for fixture in negative_fixtures)
    negative_total = sum(negative_counts.values())
    width, height = 920, 610 if open_manual_controls else 500
    left, top, row_height, max_bar = 220, 106, 50, 590
    selected_target_count = sum(counts.values())
    target_population_label = data.get(
        "target_population_label", "Selected T-target outcomes"
    )
    target_population_description = data.get(
        "target_population_description", "selected T-target outcomes"
    )
    open_obligations = [
        obligation
        for obligation in data["open_source_obligations"]
        if obligation["status"] == "OPEN"
    ]
    open_obligation_count = len(open_obligations)
    obligation_note = " · ".join(
        f"{obligation['id']} (interfaces {', '.join(obligation['interfaces'])})"
        for obligation in open_obligations
    ) or "No open PAL-source obligations recorded"
    obligation_noun = "obligation" if open_obligation_count == 1 else "obligations"
    manual_noun = "control" if open_manual_count == 1 else "controls"
    maximum = max(
        max(counts.values()),
        open_obligation_count,
        open_manual_count,
        max(negative_counts.values(), default=0),
        1,
    )
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
    obligation_y = 414
    obligation_width = round(max_bar * open_obligation_count / maximum)
    manual_description = (
        f" A third lower bar counts {open_manual_count} open manual review "
        f"{manual_noun}."
        if open_manual_controls
        else ""
    )
    negative_description = (
        f" A {'fourth' if open_manual_controls else 'third'} section counts "
        f"{negative_total} required negative-guard dispositions; evidence may "
        "overlap the other populations."
        if negative_fixtures
        else ""
    )
    subtitle = (
        f'{escape(data["run_id"])} · audit populations and overlapping evidence are kept separate'
        if open_manual_controls or negative_fixtures
        else f'{escape(data["run_id"])} · selected-test outcomes and PAL-source obligations are not summed'
    )
    manual_section: list[str] = []
    if open_manual_controls:
        manual_y = 528
        manual_width = round(max_bar * open_manual_count / maximum)
        manual_note = " · ".join(control["id"] for control in open_manual_controls)
        manual_section = [
            '<line x1="28" y1="492" x2="892" y2="492" stroke="#cbd5e0" stroke-width="1"/>',
            '<text x="28" y="518" class="section">Open manual review controls (separate population)</text>',
            f'<text x="{left - 16}" y="{manual_y + 22}" text-anchor="end" class="label">OPEN MANUAL</text>',
            f'<rect x="{left}" y="{manual_y}" width="{manual_width}" height="30" rx="5" fill="#805ad5"/>',
            f'<text x="{left + manual_width + 12}" y="{manual_y + 22}" class="count">{open_manual_count}</text>',
            f'<text x="220" y="586" class="note">{escape(manual_note)}</text>',
        ]
    negative_section: list[str] = []
    if negative_fixtures:
        divider_y = 606 if open_manual_controls else 492
        heading_y = divider_y + 26
        negative_top = divider_y + 42
        negative_row_height = 38
        negative_rows: list[str] = []
        for index, status in enumerate(STATUSES):
            y = negative_top + index * negative_row_height
            bar_width = round(max_bar * negative_counts[status] / maximum)
            negative_rows.extend(
                [
                    f'<text x="{left - 16}" y="{y + 18}" text-anchor="end" class="label">NEG {escape(status)}</text>',
                    f'<rect x="{left}" y="{y}" width="{bar_width}" height="24" rx="5" fill="{COLORS[status]}"/>',
                    f'<text x="{left + bar_width + 12}" y="{y + 18}" class="count">{negative_counts[status]}</text>',
                ]
            )
        negative_note_y = negative_top + len(STATUSES) * negative_row_height + 14
        height = negative_note_y + 24
        negative_section = [
            f'<line x1="28" y1="{divider_y}" x2="892" y2="{divider_y}" stroke="#cbd5e0" stroke-width="1"/>',
            f'<text x="28" y="{heading_y}" class="section">Required negative-guard dispositions (n={negative_total}; separate population)</text>',
            *negative_rows,
            f'<text x="220" y="{negative_note_y}" class="note">Evidence and manual controls may overlap; dispositions are not summed.</text>',
        ]
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" viewBox="0 0 {width} {height}">',
            f'<title id="title">PAL Lean Audit separated counts for {escape(data["run_id"])}</title>',
            f'<desc id="desc">The upper group counts {selected_target_count} {escape(target_population_description)}. A separate lower bar counts {open_obligation_count} open PAL-source {obligation_noun}.{manual_description}{negative_description}</desc>',
            '<rect width="100%" height="100%" fill="#f7fafc"/>',
            '<style>.title{font:700 24px system-ui,sans-serif;fill:#1a202c}.sub{font:14px system-ui,sans-serif;fill:#4a5568}.section{font:700 15px system-ui,sans-serif;fill:#2d3748}.label{font:600 14px ui-monospace,monospace;fill:#2d3748}.count{font:700 15px system-ui,sans-serif;fill:#1a202c}.note{font:13px system-ui,sans-serif;fill:#4a5568}</style>',
            '<text x="28" y="36" class="title">PAL Lean Audit — separated counts</text>',
            f'<text x="28" y="60" class="sub">{subtitle}</text>',
            f'<text x="28" y="90" class="section">{escape(target_population_label)} (n={selected_target_count})</text>',
            *rows,
            '<line x1="28" y1="378" x2="892" y2="378" stroke="#cbd5e0" stroke-width="1"/>',
            '<text x="28" y="404" class="section">Open PAL-source obligations (separate population)</text>',
            f'<text x="{left - 16}" y="{obligation_y + 22}" text-anchor="end" class="label">OPEN PAL-SOURCE</text>',
            f'<rect x="{left}" y="{obligation_y}" width="{obligation_width}" height="30" rx="5" fill="#c05621"/>',
            f'<text x="{left + obligation_width + 12}" y="{obligation_y + 22}" class="count">{open_obligation_count}</text>',
            f'<text x="220" y="472" class="note">{escape(obligation_note)}</text>',
            *manual_section,
            *negative_section,
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
    parser.add_argument(
        "--ledger",
        type=pathlib.Path,
        default=DEFAULT_LEDGER,
        help="claim ledger path (default: Audit/claim-ledger.json)",
    )
    parser.add_argument(
        "--summary",
        type=pathlib.Path,
        default=DEFAULT_SUMMARY,
        help="Markdown output path (default: docs/generated/summary.md)",
    )
    parser.add_argument(
        "--chart",
        type=pathlib.Path,
        default=DEFAULT_CHART,
        help="SVG output path (default: docs/generated/outcomes.svg)",
    )
    args = parser.parse_args()
    ledger_path = args.ledger if args.ledger.is_absolute() else ROOT / args.ledger
    summary_path = args.summary if args.summary.is_absolute() else ROOT / args.summary
    chart_path = args.chart if args.chart.is_absolute() else ROOT / args.chart
    data = load_ledger(ledger_path)
    counts = Counter(claim["status"] for claim in data["claims"])
    ok = write_or_check(summary_path, render_summary(data, counts), args.check)
    ok = write_or_check(chart_path, render_svg(data, counts), args.check) and ok
    if ok:
        action = "Verified" if args.check else "Rendered"
        print(
            f"{action} {summary_path.relative_to(ROOT)} and "
            f"{chart_path.relative_to(ROOT)}"
        )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
