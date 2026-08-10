#!/usr/bin/env python3
"""Render and validate Attack Run 0003 reports from machine receipts."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys
import textwrap
from collections import Counter
from xml.sax.saxutils import escape


ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = ROOT / "Audit" / "attack-run-0003-claim-ledger.json"
RECEIPT = ROOT / "Audit" / "attack-run-0003-receipt.json"
BENCHMARKS = ROOT / "Audit" / "attack-run-0003-benchmarks.json"
SUMMARY = ROOT / "docs" / "generated" / "attack-run-0003-summary.md"
CHART = ROOT / "docs" / "generated" / "attack-run-0003-classifications.svg"
DIAGRAM = ROOT / "docs" / "generated" / "attack-run-0003-dependencies.svg"
BENCHMARK_TABLE = ROOT / "docs" / "generated" / "attack-run-0003-benchmarks.md"

FORMAL_STATUSES = (
    "PROVED_FROM_DECLARED_RULES",
    "CONSISTENT_REALIZATION",
    "ASSUMPTION_BOUND",
    "COUNTERMODEL_TO_OVERCLAIM",
    "EXPECTED_REJECTION",
)
DISPOSITION_STATUSES = (
    "OPEN_MANUAL",
    "TRANSLATION_AMBIGUITY",
)
STATUSES = FORMAL_STATUSES + DISPOSITION_STATUSES
COLORS = {
    "PROVED_FROM_DECLARED_RULES": "#2f855a",
    "CONSISTENT_REALIZATION": "#2b6cb0",
    "ASSUMPTION_BOUND": "#6b46c1",
    "COUNTERMODEL_TO_OVERCLAIM": "#c05621",
    "EXPECTED_REJECTION": "#805ad5",
    "OPEN_MANUAL": "#d69e2e",
    "TRANSLATION_AMBIGUITY": "#718096",
}
REQUIRED_CLAIM_FIELDS = {
    "id",
    "title",
    "classification",
    "pal_addresses",
    "lean_declarations",
    "explicit_hypotheses",
    "axioms",
    "positive_claim_established",
    "overclaim_not_established",
    "authority_ceiling",
    "retained_evidence",
    "reopening_or_unresolved_burden",
}
EXPECTED_ROUTE_BY_DECISION = {
    "D16": {"D16", "SC-19.1", "M-A0-SCOPED-FIRST", "T33"},
    "D17": {"D17", "SC-19.2", "M-A0-CUT", "T34"},
    "D18": {"D18", "SC-19.3", "M-A2-HISTORY", "T35"},
    "D19": {"D19", "SC-19.4", "M-A0-SCOPED-FIRST", "T36"},
    "D20": {"D20", "SC-19.5", "M-INQUIRY-APPEND", "T37"},
    "D21": {"D21", "SC-19.6", "M-SOURCE-FIBER", "T38"},
    "D22": {"D22", "SC-19.7", "M-INQUIRY-APPEND", "T39"},
    "D23": {"D23", "SC-19.8", "M-INQUIRY-APPEND", "T40"},
}
EXPECTED_GROUP_ROUTE_BY_DECISION = {
    **EXPECTED_ROUTE_BY_DECISION,
    "D18": {
        "D18",
        "SC-19.3",
        "M-SOURCE-FIBER",
        "M-A2-HISTORY",
        "T35",
    },
}
EXPECTED_REPOSITORY_CHECKS = {
    "historical_policy",
    "gate5_policy",
    "candidate_input_regression",
    "published_source_and_migration",
    "attack_run_0001_report",
    "attack_run_0002_report",
    "migration_report",
    "attack_run_0003_structure",
    "attack_run_0003_dependencies",
    "leanchecker",
}
EXPECTED_POLICY_FIXTURES = {
    "Audit/fixtures/T05-ascii-omega.fixture",
    "Audit/fixtures/T05-symbol-omega.fixture",
    "Audit/fixtures/AR3-explanatory-shorthand-status.fixture",
    "Audit/fixtures/AR3-first-occurrence-closure.fixture",
}
BENCHMARK_LABELS = (
    ("Build wall time", "build_wall_seconds", "seconds"),
    ("Checked declarations", "checked_declarations", "declarations"),
    ("Empty axiom receipts", "empty_axiom_receipts", "declarations"),
    ("Nonempty axiom receipts", "nonempty_axiom_receipts", "declarations"),
    ("propext-only receipts", "propext_only_receipts", "declarations"),
    (
        "propext + Quot.sound receipts",
        "propext_and_quot_sound_receipts",
        "declarations",
    ),
    ("Formal result rows", "formal_result_count", "results"),
    ("Adversarial/negative controls", "negative_control_count", "controls"),
    ("Policy fixtures", "policy_fixture_count", "fixtures"),
    ("Repository checks", "repository_check_count", "checks"),
)


def load_json(path: pathlib.Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_evidence_file(relative_path: str, expected_sha256: str) -> None:
    path = (ROOT / relative_path).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError(f"benchmark evidence is missing or escapes the repository: {relative_path}")
    text = path.read_text(encoding="utf-8")
    observed = hashlib.sha256(
        text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    ).hexdigest()
    if observed != expected_sha256:
        raise ValueError(f"benchmark evidence hash mismatch: {relative_path}")


def validate(ledger: dict, receipt: dict, benchmarks: dict) -> Counter:
    if ledger.get("run_id") != "attack-0003" or receipt.get("run_id") != "attack-0003":
        raise ValueError("both receipts must identify attack-0003")
    if ledger.get("controlling_release") != "PAL v2.1":
        raise ValueError("Attack Run 0003 must route to PAL v2.1")
    if ledger.get("controlling_doi") != "10.5281/zenodo.21864767":
        raise ValueError("unexpected PAL v2.1 DOI")
    for key in ("controlling_release", "controlling_doi", "authority_ceiling"):
        if ledger.get(key) != receipt.get(key):
            raise ValueError(f"ledger and run receipt disagree on {key}")
    if ledger.get("audit_direction") != "PAL_AUDITS_DECLARED_LEAN_REALIZATIONS":
        raise ValueError("audit direction is not PAL-led")
    if receipt.get("formal_evidence_is_adoption_authority") is not False:
        raise ValueError("formal evidence must not be recorded as adoption authority")
    phrase = receipt.get("occurrence_closed_source_open", {})
    if (
        phrase.get("role") != "EXPLANATORY_SHORTHAND"
        or phrase.get("primitive") is not False
        or phrase.get("status") is not False
    ):
        raise ValueError("occurrence/source shorthand must remain explanatory")

    claims = ledger.get("claims", [])
    if not claims:
        raise ValueError("claim ledger is empty")
    ids = [claim.get("id") for claim in claims]
    if len(ids) != len(set(ids)):
        raise ValueError("claim ids must be unique")
    for claim in claims:
        missing = REQUIRED_CLAIM_FIELDS - set(claim)
        if missing:
            raise ValueError(f"{claim.get('id')} is missing fields: {sorted(missing)}")
        if claim["classification"] not in STATUSES:
            raise ValueError(f"{claim['id']} has an unknown classification")
        if not claim["pal_addresses"]:
            raise ValueError(f"{claim['id']} has no PAL address")
        if claim["classification"] not in {"EXPECTED_REJECTION", "OPEN_MANUAL"}:
            if not claim["lean_declarations"]:
                raise ValueError(f"{claim['id']} has no Lean declaration")
        if claim["classification"] == "ASSUMPTION_BOUND" and not claim["explicit_hypotheses"]:
            raise ValueError(f"{claim['id']} must expose its supplying hypothesis")

    receipt_results = {
        row["id"]: row["classification"] for row in receipt.get("results", [])
    }
    ledger_results = {row["id"]: row["classification"] for row in claims}
    if receipt_results != ledger_results:
        raise ValueError("ledger results do not match the machine run receipt")

    dependency_rows = receipt.get("dependency_receipts", [])
    dependency_by_declaration = {
        row["declaration"]: row.get("axioms", []) for row in dependency_rows
    }
    if len(dependency_by_declaration) != len(dependency_rows):
        raise ValueError("dependency declarations must be unique")
    for claim in claims:
        declared = claim["lean_declarations"]
        missing_declarations = [
            declaration
            for declaration in declared
            if declaration not in dependency_by_declaration
        ]
        if missing_declarations:
            raise ValueError(
                f"{claim['id']} lacks dependency receipts for: {missing_declarations}"
            )
        receipt_axioms = sorted(
            {
                axiom
                for declaration in declared
                for axiom in dependency_by_declaration[declaration]
            }
        )
        if sorted(claim["axioms"]) != receipt_axioms:
            raise ValueError(
                f"{claim['id']} axiom summary disagrees with declaration receipts: "
                f"ledger={sorted(claim['axioms'])}, receipts={receipt_axioms}"
            )

    decisions = {f"D{number}" for number in range(16, 24)}
    covered = {
        address
        for claim in claims
        for address in claim["pal_addresses"]
        if address in decisions
    }
    if covered != decisions:
        raise ValueError(f"decision coverage mismatch: {sorted(covered)}")
    claim_by_id = {claim["id"]: claim for claim in claims}
    for claim in claims:
        claim_addresses = set(claim["pal_addresses"])
        for decision in claim_addresses & decisions:
            if not EXPECTED_ROUTE_BY_DECISION[decision].issubset(claim_addresses):
                raise ValueError(
                    f"{claim['id']} does not carry the exact {decision} source route"
                )

    burdens = receipt.get("open_burdens", [])
    if len(burdens) != 1:
        raise ValueError("the first-occurrence account must remain one debt")
    burden = burdens[0]
    if (
        burden.get("address") != "D-FIRST-OCCURRENCE"
        or burden.get("status") != "OPEN"
        or burden.get("interfaces") != ["O04", "O25"]
        or burden.get("interface_states") != {"O04": "OPEN", "O25": "OPEN"}
    ):
        raise ValueError("O04 and O25 must remain two OPEN interfaces to one debt")

    groups = ledger.get("dependency_groups", [])
    if {group.get("decision") for group in groups} != decisions:
        raise ValueError("dependency diagram must cover D16 through D23")
    if any(not group.get("source_routes") or not group.get("result_ids") for group in groups):
        raise ValueError("each dependency group needs source routes and results")
    for group in groups:
        decision = group["decision"]
        if set(group["source_routes"]) != EXPECTED_GROUP_ROUTE_BY_DECISION[decision]:
            raise ValueError(f"dependency route mismatch for {decision}")
        if any(result_id not in claim_by_id for result_id in group["result_ids"]):
            raise ValueError(f"dependency group {decision} contains a dangling result id")
        for result_id in group["result_ids"]:
            if decision not in claim_by_id[result_id]["pal_addresses"]:
                raise ValueError(
                    f"dependency group {decision} misroutes result {result_id}"
                )
        routed = {
            claim["id"] for claim in claims if decision in claim["pal_addresses"]
        }
        if set(group["result_ids"]) != routed:
            raise ValueError(f"dependency group {decision} omits or adds result ids")

    required_measurements = {
        "build_wall_seconds",
        "checked_declarations",
        "empty_axiom_receipts",
        "nonempty_axiom_receipts",
        "propext_only_receipts",
        "propext_and_quot_sound_receipts",
        "formal_result_count",
        "negative_control_count",
        "policy_fixture_count",
        "repository_check_count",
    }
    measurements = benchmarks.get("measurements", {})
    if benchmarks.get("measured") is not True:
        raise ValueError("benchmark data must be marked as measured")
    if (
        benchmarks.get("baseline_commit")
        != receipt.get("version_control_identity", {}).get("base_sha")
        or benchmarks.get("commit_under_test") is not None
        or not str(benchmarks.get("worktree_state", "")).startswith("UNCOMMITTED_GATE5_WORKTREE")
    ):
        raise ValueError("local benchmark must distinguish its baseline from an unavailable future commit")
    if (
        benchmarks.get("repetitions") != 1
        or benchmarks.get("cache_state") != "WARM_LOCAL_CACHE"
        or not benchmarks.get("measurement_method")
        or not benchmarks.get("missing_data")
        or not benchmarks.get("privacy_redactions")
    ):
        raise ValueError("benchmark method, cache state, repetition, or missing-data receipt is incomplete")
    if set(measurements) != required_measurements:
        raise ValueError("benchmark measurement population mismatch")
    if any(not isinstance(value, (int, float)) or value < 0 for value in measurements.values()):
        raise ValueError("benchmark measurements must be actual nonnegative numbers")
    if measurements["formal_result_count"] != sum(
        claim["classification"]
        not in {"EXPECTED_REJECTION", "OPEN_MANUAL", "TRANSLATION_AMBIGUITY"}
        for claim in claims
    ):
        raise ValueError("formal result count does not match the ledger")
    if measurements["checked_declarations"] != measurements["empty_axiom_receipts"] + measurements["nonempty_axiom_receipts"]:
        raise ValueError("dependency receipt populations do not sum")
    dependencies = dependency_rows
    if measurements["checked_declarations"] != len(dependencies):
        raise ValueError("checked declaration count does not match dependency receipts")
    if measurements["empty_axiom_receipts"] != sum(
        not row.get("axioms") for row in dependencies
    ):
        raise ValueError("empty axiom population does not match dependency receipts")
    if measurements["nonempty_axiom_receipts"] != sum(
        bool(row.get("axioms")) for row in dependencies
    ):
        raise ValueError("nonempty axiom population does not match dependency receipts")
    if measurements["propext_only_receipts"] != sum(
        row.get("axioms") == ["propext"] for row in dependencies
    ):
        raise ValueError("propext-only population does not match dependency receipts")
    if measurements["propext_and_quot_sound_receipts"] != sum(
        row.get("axioms") == ["propext", "Quot.sound"] for row in dependencies
    ):
        raise ValueError("propext/Quot.sound population does not match dependency receipts")
    if measurements["negative_control_count"] != len(receipt.get("negative_controls", [])):
        raise ValueError("negative-control count does not match the run receipt")
    if measurements["policy_fixture_count"] != len(EXPECTED_POLICY_FIXTURES):
        raise ValueError("policy-fixture count does not match the declared fixture set")
    if any(not (ROOT / path).is_file() for path in EXPECTED_POLICY_FIXTURES):
        raise ValueError("one or more policy fixtures are missing")

    build = benchmarks.get("build_measurement", {})
    if (
        build.get("command") != "lake build"
        or build.get("exit_code") != 0
        or build.get("wall_seconds") != measurements["build_wall_seconds"]
    ):
        raise ValueError("build measurement is not backed by the expected successful command")
    validate_evidence_file(
        build.get("output_log", ""), build.get("output_canonical_lf_sha256", "")
    )
    axiom_evidence = benchmarks.get("axiom_evidence", {})
    if axiom_evidence.get("exit_code") != 0 or "Audit/AttackRun0003.lean" not in axiom_evidence.get("command", ""):
        raise ValueError("dependency populations lack a successful axiom-capture command")
    validate_evidence_file(
        axiom_evidence.get("output_log", ""),
        axiom_evidence.get("output_canonical_lf_sha256", ""),
    )
    checks = benchmarks.get("repository_checks", [])
    if (
        len(checks) != measurements["repository_check_count"]
        or {row.get("name") for row in checks} != EXPECTED_REPOSITORY_CHECKS
        or any(row.get("exit_code") != 0 for row in checks)
    ):
        raise ValueError("repository-check count is not backed by the expected passing checks")
    validation_log = benchmarks.get("validation_log", {})
    validate_evidence_file(
        validation_log.get("path", ""),
        validation_log.get("canonical_lf_sha256", ""),
    )

    return Counter(claim["classification"] for claim in claims)


def cell(value: object) -> str:
    if isinstance(value, list):
        value = "; ".join(str(item) for item in value) if value else "None"
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_summary(
    ledger: dict, receipt: dict, benchmarks: dict, counts: Counter
) -> str:
    formal_total = sum(counts[status] for status in FORMAL_STATUSES)
    disposition_total = sum(counts[status] for status in DISPOSITION_STATUSES)
    burdens = receipt["open_burdens"]
    measurements = benchmarks["measurements"]
    lines = [
        "# Attack Run 0003 — PAL-led realization audit",
        "",
        "PAL v2.1 audited the declared Lean realizations in this run. Lean did not redefine, adopt, or prove PAL.",
        "",
        f"- Controlling release: **{ledger['controlling_release']}**",
        f"- DOI: [{ledger['controlling_doi']}](https://doi.org/{ledger['controlling_doi']})",
        f"- Run status: **{receipt['run_status']}**",
        f"- Authority ceiling: {ledger['authority_ceiling']}",
        f"- Exact formal-target source: `{receipt['formal_target_source_identity']['path']}` at canonical-LF SHA-256 `{receipt['formal_target_source_identity']['canonical_lf_sha256']}`.",
        f"- Exact negative-fixture identities: **{len(receipt['fixture_target_identities'])}** path/hash/diagnostic receipts.",
        "- Open burden: **D-FIRST-OCCURRENCE** remains one **OPEN** debt with **O04** and **O25** as two separately preserved **OPEN** interfaces.",
        "- Terminology: “occurrence-closed, source-open” is explanatory shorthand, not a primitive or PAL status.",
        "",
        f"## Formal and control classifications (n={formal_total})",
        "",
        "| Classification | Count |",
        "|---|---:|",
    ]
    lines.extend(f"| `{status}` | {counts[status]} |" for status in FORMAL_STATUSES)
    lines.extend(
        [
            "",
            "_These counts cover formal results and expected policy rejections only._",
            "",
            f"## Required overclaim controls (overlapping evidence; n={len(receipt['negative_controls'])})",
            "",
            "| Control | Attempted overclaim | Disposition | Existing result evidence |",
            "|---|---|---|---|",
        ]
    )
    for control in receipt["negative_controls"]:
        lines.append(
            f"| `{cell(control['id'])}` | {cell(control['attempted_overclaim'])} | "
            f"`{cell(control['disposition'])}` | {cell(control['evidence'])} |"
        )
    lines.extend(
        [
            "",
            "_These ten controls reuse classified result evidence and are not added to the formal/control denominator._",
            "",
            f"## Additional T39 conformance controls (overlapping evidence; n={len(receipt['additional_conformance_controls'])})",
            "",
            "| Control | PAL route | Attempted nonconformance | Disposition | Existing result evidence |",
            "|---|---|---|---|---|",
        ]
    )
    for control in receipt["additional_conformance_controls"]:
        lines.append(
            f"| `{cell(control['id'])}` | {cell(control['pal_route'])} | "
            f"{cell(control['attempted_nonconformance'])} | "
            f"`{cell(control['disposition'])}` | {cell(control['evidence'])} |"
        )
    lines.extend(
        [
            "",
            "_These T39 controls make the separately required missing-event-witness and missing-cost cases explicit; they reuse AR3-13 and AR3-18 and are not added to any classification denominator._",
            "",
            f"## Manual and translation dispositions (separate population; n={disposition_total})",
            "",
            "| Disposition | Count |",
            "|---|---:|",
        ]
    )
    lines.extend(f"| `{status}` | {counts[status]} |" for status in DISPOSITION_STATUSES)
    lines.extend(
        [
            "",
            "_Formal/control classifications, manual/translation dispositions, PAL-source obligations, and benchmarks are not summed. None is a PAL correctness score._",
            "",
            f"## PAL-source obligations (separate population; n={len(burdens)})",
            "",
            "| Obligation | State | Preserved interfaces | Debt count |",
            "|---|---|---|---:|",
        ]
    )
    for burden in burdens:
        interfaces = "; ".join(
            f"{address} {burden['interface_states'][address]}"
            for address in burden["interfaces"]
        )
        lines.append(
            f"| `{cell(burden['address'])}` | `{cell(burden['status'])}` | "
            f"{cell(interfaces)} | 1 |"
        )
    lines.extend(
        [
            "",
            f"## Benchmark measurements (separate population; n={len(measurements)})",
            "",
            "| Measurement | Actual value | Unit |",
            "|---|---:|---|",
        ]
    )
    lines.extend(
        f"| {label} | {measurements[key]} | {unit} |"
        for label, key, unit in BENCHMARK_LABELS
    )
    lines.extend(
        [
            "",
            "The detailed benchmark receipt records command, environment, cache state, repetition method, and missing data. These measurements are not a PAL correctness score.",
            "",
            "## Result table",
            "",
            "| ID | PAL address | Lean declaration | Class | Explicit hypotheses or axioms | Positive claim established | Overclaim not established | Authority ceiling | Retained evidence | Reopening or unresolved burden |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
    )
    for claim in ledger["claims"]:
        dependencies = [f"hypotheses: {cell(claim['explicit_hypotheses'])}", f"axioms: {cell(claim['axioms'])}"]
        lines.append(
            "| " + " | ".join(
                [
                    cell(claim["id"]),
                    cell(claim["pal_addresses"]),
                    cell(claim["lean_declarations"]),
                    f"`{claim['classification']}`",
                    "<br>".join(dependencies),
                    cell(claim["positive_claim_established"]),
                    cell(claim["overclaim_not_established"]),
                    cell(claim["authority_ceiling"]),
                    cell(claim["retained_evidence"]),
                    cell(claim["reopening_or_unresolved_burden"]),
                ]
            ) + " |"
        )
    lines.extend(
        [
            "",
            "## Manual review",
            "",
            "The lexical policy fixtures are bounded guards only. Semantic-surrogate review remains manual, and unresolved possibility remains outside Lean’s object language.",
            "",
            "_Generated from `Audit/attack-run-0003-claim-ledger.json` and `Audit/attack-run-0003-receipt.json`; do not edit by hand._",
            "",
        ]
    )
    return "\n".join(lines)


def render_chart(counts: Counter) -> str:
    width, height = 1120, 580
    left, top, row_height, max_bar = 355, 92, 53, 680
    maximum = max(max(counts.values(), default=0), 1)
    rows: list[str] = []
    for index, status in enumerate(FORMAL_STATUSES):
        y = top + index * row_height
        bar_width = round(max_bar * counts[status] / maximum)
        rows.extend(
            [
                f'<text x="{left - 16}" y="{y + 23}" text-anchor="end" class="label">{escape(status)}</text>',
                f'<rect x="{left}" y="{y}" width="{bar_width}" height="31" rx="5" fill="{COLORS[status]}"/>',
                f'<text x="{left + bar_width + 12}" y="{y + 23}" class="count">{counts[status]}</text>',
            ]
        )
    disposition_rows: list[str] = []
    disposition_top = 406
    for index, status in enumerate(DISPOSITION_STATUSES):
        y = disposition_top + index * row_height
        bar_width = round(max_bar * counts[status] / maximum)
        disposition_rows.extend(
            [
                f'<text x="{left - 16}" y="{y + 23}" text-anchor="end" class="label">{escape(status)}</text>',
                f'<rect x="{left}" y="{y}" width="{bar_width}" height="31" rx="5" fill="{COLORS[status]}"/>',
                f'<text x="{left + bar_width + 12}" y="{y + 23}" class="count">{counts[status]}</text>',
            ]
        )
    formal_total = sum(counts[status] for status in FORMAL_STATUSES)
    disposition_total = sum(counts[status] for status in DISPOSITION_STATUSES)
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" viewBox="0 0 {width} {height}">',
            '<title id="title">Attack Run 0003 result classifications</title>',
            f'<desc id="desc">Actual counts for {formal_total} formal or control classifications and {disposition_total} separate manual or translation dispositions. No correctness score is calculated.</desc>',
            '<rect width="100%" height="100%" fill="#f7fafc"/>',
            '<style>.title{font:700 24px system-ui,sans-serif;fill:#1a202c}.sub{font:14px system-ui,sans-serif;fill:#4a5568}.label{font:600 13px ui-monospace,monospace;fill:#2d3748}.count{font:700 15px system-ui,sans-serif;fill:#1a202c}</style>',
            '<text x="28" y="36" class="title">Attack Run 0003 — classification counts</text>',
            f'<text x="28" y="61" class="sub">Formal/control n={formal_total} · review dispositions n={disposition_total} · zero values are displayed</text>',
            *rows,
            '<line x1="28" y1="362" x2="1092" y2="362" stroke="#cbd5e0" stroke-width="1"/>',
            '<text x="28" y="390" class="sub">Manual and translation dispositions — separate population</text>',
            *disposition_rows,
            '</svg>',
            '',
        ]
    )


def render_dependency_diagram(ledger: dict) -> str:
    groups = ledger["dependency_groups"]
    width, row_height = 1540, 112
    top, height = 100, 100 + row_height * len(groups) + 34
    rows: list[str] = []
    def tspans(value: str, x: int, y: int, width_chars: int) -> str:
        wrapped = textwrap.wrap(
            value,
            width=width_chars,
            break_long_words=False,
            break_on_hyphens=False,
        ) or [""]
        return "".join(
            f'<tspan x="{x}" y="{y + index * 14}">{escape(line)}</tspan>'
            for index, line in enumerate(wrapped)
        )
    for index, group in enumerate(groups):
        y = top + index * row_height
        route = " · ".join(group["source_routes"])
        results = " · ".join(group["result_ids"])
        declarations = " · ".join(group.get("declarations", []))
        rows.extend(
            [
                f'<rect x="24" y="{y}" width="430" height="88" rx="7" class="source"/>',
                f'<text x="40" y="{y + 25}" class="decision">{escape(group["decision"])}</text>',
                f'<text x="40" y="{y + 50}" class="small">{escape(route)}</text>',
                f'<path d="M454 {y + 44} H520" class="arrow" marker-end="url(#arrow)"/>',
                f'<rect x="530" y="{y}" width="610" height="88" rx="7" class="lean"/>',
                f'<text x="546" y="{y + 25}" class="decision">Declared Lean realization</text>',
                f'<text class="small">{tspans(declarations, 546, y + 49, 78)}</text>',
                f'<path d="M1140 {y + 44} H1206" class="arrow" marker-end="url(#arrow)"/>',
                f'<rect x="1216" y="{y}" width="300" height="88" rx="7" class="result"/>',
                f'<text x="1232" y="{y + 25}" class="decision">Result receipt</text>',
                f'<text class="small">{tspans(results, 1232, y + 49, 32)}</text>',
            ]
        )
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" viewBox="0 0 {width} {height}">',
            '<title id="title">Attack Run 0003 dependency diagram</title>',
            '<desc id="desc">Eight PAL v2.1 decision routes control declared Lean realizations, which produce bounded result receipts.</desc>',
            '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#4a5568"/></marker></defs>',
            '<rect width="100%" height="100%" fill="#f7fafc"/>',
            '<style>.title{font:700 24px system-ui,sans-serif;fill:#1a202c}.sub{font:14px system-ui,sans-serif;fill:#4a5568}.decision{font:700 15px system-ui,sans-serif;fill:#1a202c}.small{font:12px ui-monospace,monospace;fill:#2d3748}.source{fill:#ebf8ff;stroke:#3182ce}.lean{fill:#f0fff4;stroke:#38a169}.result{fill:#faf5ff;stroke:#805ad5}.arrow{stroke:#4a5568;stroke-width:2;fill:none}</style>',
            '<text x="24" y="36" class="title">Attack Run 0003 — declared dependency route</text>',
            '<text x="24" y="62" class="sub">PAL v2.1 controls meaning and ceilings; Lean checks only the displayed realizations and dependencies.</text>',
            *rows,
            '</svg>',
            '',
        ]
    )


def render_benchmarks(benchmarks: dict) -> str:
    m = benchmarks["measurements"]
    lines = [
        "# Attack Run 0003 benchmark receipt",
        "",
        f"- Measured at: `{benchmarks['measured_at_utc']}`",
        f"- Environment: {benchmarks['environment']}",
        f"- Baseline commit: `{benchmarks['baseline_commit']}`",
        f"- Tracked commit under test: `{benchmarks['commit_under_test'] or 'UNAVAILABLE_FOR_UNCOMMITTED_WORKTREE'}`",
        f"- Worktree identity: {benchmarks['worktree_state']}",
        f"- Method: {benchmarks['measurement_method']}",
        f"- Repetitions: {benchmarks['repetitions']}",
        f"- Cache state: `{benchmarks['cache_state']}`",
        f"- Missing data: {'; '.join(benchmarks['missing_data'])}",
        f"- Privacy handling: {'; '.join(benchmarks['privacy_redactions'])}",
        "",
        "| Measurement | Actual value | Unit |",
        "|---|---:|---|",
    ]
    lines.extend(
        f"| {label} | {m[key]} | {unit} |"
        for label, key, unit in BENCHMARK_LABELS
    )
    lines.extend(
        [
            "",
            "Build duration is runner- and cache-dependent. Counts describe this declared run; none is a PAL correctness score.",
            "",
            "_Generated from `Audit/attack-run-0003-benchmarks.json`; do not edit by hand._",
            "",
        ]
    )
    return "\n".join(lines)


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
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    ledger = load_json(LEDGER)
    receipt = load_json(RECEIPT)
    benchmarks = load_json(BENCHMARKS)
    counts = validate(ledger, receipt, benchmarks)
    outputs = (
        (SUMMARY, render_summary(ledger, receipt, benchmarks, counts)),
        (CHART, render_chart(counts)),
        (DIAGRAM, render_dependency_diagram(ledger)),
        (BENCHMARK_TABLE, render_benchmarks(benchmarks)),
    )
    ok = True
    for path, content in outputs:
        ok = write_or_check(path, content, args.check) and ok
    if ok:
        action = "Verified" if args.check else "Rendered"
        print(f"{action} {len(outputs)} Attack Run 0003 outputs.")
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Attack Run 0003 report failed: {error}", file=sys.stderr)
        raise SystemExit(1)
