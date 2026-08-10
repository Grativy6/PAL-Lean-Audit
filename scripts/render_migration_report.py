#!/usr/bin/env python3
"""Render the deterministic PAL v2.0-to-v2.1 migration summary."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Audit" / "releases" / "pal-v2.1-source-manifest.json"
ADOPTION = ROOT / "Audit" / "releases" / "pal-v2.1-adoption-receipt.json"
MIGRATION = ROOT / "Audit" / "migrations" / "pal-v2.0-to-v2.1-migration-receipt.json"
LOCK = ROOT / "Audit" / "migrations" / "pal-v2.0-to-v2.1-historical-lock.json"
OUTPUT = ROOT / "docs" / "generated" / "pal-v2.0-to-v2.1-migration-summary.md"


def load(path: pathlib.Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def render() -> str:
    source = load(SOURCE)
    adoption = load(ADOPTION)
    migration = load(MIGRATION)
    lock = load(LOCK)
    lines = [
        "# PAL v2.0-to-v2.1 repository migration receipt",
        "",
        f"- Human adoption: **{adoption['receipt_status']}**, by **{adoption['adoption_authority']['name']}**",
        f"- Controlling canon for new runs: **{source['release']['name']}**, DOI [{source['release']['doi']}](https://doi.org/{source['release']['doi']})",
        f"- Repository migration status: **{migration['migration_status']}**",
        f"- Historical baseline: `{lock['baseline']['commit_sha']}` / tree `{lock['baseline']['tree_sha']}`",
        f"- Protected historical blobs: **{len(lock['protected_artifacts'])}**",
        "- Authority ceiling: repository and formal-audit evidence record migration and bounded tests; they do not amend or adopt PAL.",
        "",
        "## Published source identities",
        "",
        "| Authority surface | DOCX SHA-256 | PDF SHA-256 |",
        "|---|---|---|",
    ]
    for surface in source["authority_surfaces"]:
        lines.append(
            f"| {surface['id']} — {surface['title']} | "
            f"`{surface['artifacts']['docx']['sha256']}` | "
            f"`{surface['artifacts']['pdf']['sha256']}` |"
        )
    archive = source["release_archive"]
    lines.extend(
        [
            "",
            f"Published archive: `{archive['filename']}` · {archive['byte_length']} bytes · SHA-256 `{archive['sha256']}` · MD5 `{archive['md5']}`.",
            "",
            "## Adopted decision mapping",
            "",
            "| Historical candidate | Adopted decision | Title | Disposition |",
            "|---|---|---|---|",
        ]
    )
    for row in migration["decision_mappings"]:
        lines.append(
            f"| {row['historical_candidate_id']} | {row['adopted_decision_id']} | "
            f"{row['adopted_title']} | `{row['adoption_disposition']}` |"
        )
    lines.extend(
        [
            "",
            "## Historical and open-burden disposition",
            "",
            "Attack Runs 0001 and 0002 retain their PAL v2.0 source routing and exact protected Git blobs. The candidate workflow, impact map, proposal, issue #4, and PR #5 remain historical noncanonical process evidence.",
            "",
            "`D-FIRST-OCCURRENCE` remains one **OPEN** debt. `O04` and `O25` remain two separate **OPEN** interfaces to that debt. “Occurrence-closed, source-open” remains explanatory shorthand, not a primitive or PAL status.",
            "",
            "_Generated from the versioned source, adoption, migration, and historical-lock receipts; do not edit by hand._",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            print(f"Generated file is stale: {OUTPUT.relative_to(ROOT)}", file=sys.stderr)
            return 1
        print(f"Verified {OUTPUT.relative_to(ROOT)}")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"Rendered {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
