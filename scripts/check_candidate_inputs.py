#!/usr/bin/env python3
"""Validate the source-locked PAL v2.1 candidate inputs and receipt locks."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
IMPACT_PATH = ROOT / "Audit" / "pal-2.1-impact.yaml"
RECEIPT_PATHS = (
    ROOT / "Audit" / "attack-run-0002-receipt.json",
    ROOT / "Audit" / "attack-run-0002-claim-ledger.json",
)
SOURCE_MANIFEST = ROOT / "Audit" / "source-manifest.yaml"
EXPECTED_CANDIDATES = {f"C21-{index:02d}" for index in range(1, 9)}
EXPECTED_NEGATIVE_FIXTURES = {f"AR2-N{index:02d}" for index in range(1, 12)}
EXPECTED_SOURCE_IDS = {
    "PAL-v2.0-Spine",
    "PAL-v2.0-M",
    "PAL-v2.0-L",
    "PAL-v2.0-T",
    "PAL-v2.0-C",
}


def canonical_text_sha256(path: pathlib.Path) -> str:
    """Hash tracked UTF-8 text with all line endings normalized to LF."""
    text = path.read_text(encoding="utf-8")
    canonical = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def fail(message: str) -> None:
    raise ValueError(message)


def locked_repo_file_hash(relative_path: str) -> str:
    path = (ROOT / relative_path).resolve()
    if not path.is_relative_to(ROOT):
        fail(f"locked input path escapes the repository: {relative_path}")
    if not path.is_file():
        fail(f"locked input path is missing: {relative_path}")
    return canonical_text_sha256(path)


def manifest_source_hashes() -> dict[str, str]:
    """Read only the five flat id/hash pairs from the locked source manifest."""
    hashes: dict[str, str] = {}
    current_id: str | None = None
    id_pattern = re.compile(r"^\s+- id:\s+(PAL-v2\.0-\S+)\s*$")
    hash_pattern = re.compile(r"^\s+sha256:\s+([0-9a-f]{64})\s*$")
    for line in SOURCE_MANIFEST.read_text(encoding="utf-8").splitlines():
        id_match = id_pattern.match(line)
        if id_match:
            current_id = id_match.group(1)
            continue
        hash_match = hash_pattern.match(line)
        if current_id and hash_match:
            hashes[current_id] = hash_match.group(1)
            current_id = None
    return hashes


def main() -> int:
    # The repository copy deliberately uses JSON syntax, which is valid YAML 1.2,
    # so CI can perform a strict parse without adding a YAML package dependency.
    impact = json.loads(IMPACT_PATH.read_text(encoding="utf-8"))
    if impact.get("status") != "CANDIDATE_NONCANONICAL":
        fail("impact map must remain CANDIDATE_NONCANONICAL")
    candidates = impact.get("candidate_statements", [])
    candidate_ids = {candidate.get("id") for candidate in candidates}
    if candidate_ids != EXPECTED_CANDIDATES or len(candidates) != 8:
        fail("impact map must contain C21-01 through C21-08 exactly once")
    if any(candidate.get("adoption_status") != "CANDIDATE" for candidate in candidates):
        fail("every impact-map candidate must remain CANDIDATE")
    debt = impact.get("first_occurrence_debt", {})
    if debt.get("current_state") != "OPEN":
        fail("D-FIRST-OCCURRENCE must remain OPEN")
    if debt.get("o04", {}).get("current_state") != "OPEN":
        fail("O04 must remain OPEN")
    if debt.get("o25", {}).get("current_state") != "OPEN":
        fail("O25 must remain OPEN")

    pal_source_rows = [
        item
        for item in impact["source_lock"]["files"]
        if item.get("id") in EXPECTED_SOURCE_IDS
    ]
    impact_sources = {item["id"]: item["sha256"] for item in pal_source_rows}
    if set(impact_sources) != EXPECTED_SOURCE_IDS or len(pal_source_rows) != 5:
        fail("impact source lock must contain the five PAL v2.0 authority surfaces")
    manifest_sources = manifest_source_hashes()
    if impact_sources != manifest_sources:
        fail("impact source hashes do not match Audit/source-manifest.yaml")

    impact_hash = canonical_text_sha256(IMPACT_PATH)
    supplied_hash = impact["input_provenance"]["supplied_map_sha256"]
    workflow_hash = impact["authority"]["candidate_workflow_sha256"]
    baseline_sha = impact["input_provenance"]["accepted_baseline_sha"]
    for path in RECEIPT_PATHS:
        receipt = json.loads(path.read_text(encoding="utf-8"))
        lock = receipt["input_lock"]
        if lock.get("repository_normalized_impact_sha256") != impact_hash:
            fail(f"{path.name} does not lock the current repository impact map")
        if lock.get("supplied_impact_input_sha256") != supplied_hash:
            fail(f"{path.name} does not preserve the supplied impact-map hash")
        if lock.get("candidate_workflow_sha256") != workflow_hash:
            fail(f"{path.name} does not preserve the candidate-workflow hash")
        if lock.get("baseline_sha") != baseline_sha:
            fail(f"{path.name} does not preserve the accepted baseline SHA")
        if receipt.get("source_hashes_verified") != impact_sources:
            fail(f"{path.name} source hashes do not match the impact map")
        statuses = receipt.get("candidate_adoption_statuses", [])
        if (
            {row.get("id") for row in statuses} != EXPECTED_CANDIDATES
            or len(statuses) != 8
        ):
            fail(f"{path.name} must list all eight candidate adoption statuses")
        if any(row.get("adoption_status") != "CANDIDATE" for row in statuses):
            fail(f"{path.name} must retain every C21 status as CANDIDATE")
        implementation_hashes = receipt.get("implementation_input_hashes", {})
        expected_implementation_paths = {
            "PAL/AttackRun0002.lean",
            "Audit/AttackRun0002.lean",
        }
        if set(implementation_hashes) != expected_implementation_paths:
            fail(f"{path.name} must lock both Attack Run 0002 Lean inputs")
        for relative_path, locked_hash in implementation_hashes.items():
            if locked_repo_file_hash(relative_path) != locked_hash:
                fail(f"{path.name} has a stale implementation hash for {relative_path}")
        formal_hash = implementation_hashes["PAL/AttackRun0002.lean"]
        axiom_hash = implementation_hashes["Audit/AttackRun0002.lean"]
        negative_fixtures = receipt.get("negative_fixtures", [])
        if (
            {fixture.get("id") for fixture in negative_fixtures}
            != EXPECTED_NEGATIVE_FIXTURES
            or len(negative_fixtures) != 11
        ):
            fail(f"{path.name} must contain AR2-N01 through AR2-N11 exactly once")
        for fixture in negative_fixtures:
            fixture_id = fixture["id"]
            fixture_inputs = fixture.get("input_hashes", {})
            if fixture_inputs.get("candidate_workflow_sha256") != workflow_hash:
                fail(f"{path.name} {fixture_id} has a stale workflow hash")
            if fixture_inputs.get("supplied_impact_input_sha256") != supplied_hash:
                fail(f"{path.name} {fixture_id} has a stale supplied-impact hash")
            if fixture.get("formal_input_sha256") != formal_hash:
                fail(f"{path.name} {fixture_id} has a stale formal-input hash")
            if fixture.get("axiom_input_sha256") != axiom_hash:
                fail(f"{path.name} {fixture_id} has a stale axiom-input hash")
            for relative_path, locked_hash in fixture.get(
                "lexical_policy_input_hashes", {}
            ).items():
                if locked_repo_file_hash(relative_path) != locked_hash:
                    fail(
                        f"{path.name} {fixture_id} has a stale lexical-policy "
                        f"hash for {relative_path}"
                    )
        manual_controls = receipt.get("manual_source_review_controls", [])
        if len(manual_controls) != 1:
            fail(f"{path.name} must retain one manual semantic-surrogate control")
        manual_control = manual_controls[0]
        if (
            manual_control.get("id") != "AR2-MANUAL-SEMANTIC-SURROGATE"
            or manual_control.get("status") != "OPEN"
            or manual_control.get("formal_result") is not False
        ):
            fail(f"{path.name} manual semantic-surrogate control must remain OPEN")

    print(
        "Candidate input check passed: strict JSON-compatible YAML, five source "
        "locks, eight CANDIDATE statements, and OPEN O04/O25."
    )
    print(f"Repository impact canonical-LF SHA-256: {impact_hash}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Candidate input check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
