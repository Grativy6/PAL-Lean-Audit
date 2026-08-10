#!/usr/bin/env python3
"""Fail-closed structural and adversarial checks for Attack Run 0003."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys
from collections import Counter

from check_policy import ROOT, omega_literal_diagnostics
from check_attack_run_0003_policy import diagnostics as gate5_diagnostics


PAL_SOURCE = ROOT / "PAL" / "AttackRun0003.lean"
AUDIT_SOURCE = ROOT / "Audit" / "AttackRun0003.lean"
RECEIPT_PATH = ROOT / "Audit" / "attack-run-0003-receipt.json"
LEDGER_PATH = ROOT / "Audit" / "attack-run-0003-claim-ledger.json"
SOURCE_MANIFEST = ROOT / "Audit" / "releases" / "pal-v2.1-source-manifest.json"
WORKFLOW = ROOT / ".github" / "workflows" / "lean.yml"
SOURCE_MANIFEST_ROUTE = "Audit/releases/pal-v2.1-source-manifest.json"
ADOPTION_RECEIPT_ROUTE = "Audit/releases/pal-v2.1-adoption-receipt.json"
MIGRATION_RECEIPT_ROUTE = "Audit/migrations/pal-v2.0-to-v2.1-migration-receipt.json"
BASELINE_COMMIT = "144b08973fde16ebeabefc78166691afc861abec"
GATE5_BRANCH = "agent/attack-run-0003-pal-led"
STATUSES = {
    "PROVED_FROM_DECLARED_RULES",
    "CONSISTENT_REALIZATION",
    "ASSUMPTION_BOUND",
    "COUNTERMODEL_TO_OVERCLAIM",
    "EXPECTED_REJECTION",
    "OPEN_MANUAL",
    "TRANSLATION_AMBIGUITY",
}
REQUIRED_THEOREMS = {
    "scopedAccountFirstRealization",
    "localFirstGlobalFirstCountermodel",
    "strongerPrimacyAssumptionBound",
    "typedCostBearingAdmission",
    "costCannotSupplyClaimReceipts",
    "occurrenceRecordFromSuppliedA1A2",
    "occurrenceRequiresA1A2Witnesses",
    "a15RequiredSeparatelyForScopedClosure",
    "a0OnlyCountermodel",
    "occurrenceHistoryMonotone",
    "historyOutlastsActivityCountermodel",
    "inquiryReceiptFromSuppliedWitness",
    "questionDoesNotSelfCertify",
    "questionCannotSupplyInquirerClaims",
    "cutOnlyCongruence",
    "noninjectiveSourceFiberCountermodel",
    "injectiveSourceIdentificationAssumptionBound",
    "witnessedInquiryAppendPreservesPrefix",
    "finiteTerminalCountermodel",
    "laterEvidenceAppendPreservesPrior",
    "overwriteIsNotAppendCountermodel",
}
REQUIRED_NEGATIVE_IDS = {f"AR3-N{index:02d}" for index in range(1, 11)}
FORMAL_SOURCE_ROUTE = "PAL/AttackRun0003.lean"
FORMAL_SOURCE_SHA256 = "0225fe8a13702e020ae368697937cfe373761888cbcdc257a19399f5a6e0c34f"
EXPECTED_FIXTURE_TARGETS = {
    "Audit/fixtures/T05-ascii-omega.fixture": {
        "claim_id": "AR3-22",
        "canonical_lf_sha256": "bda584c5ff125536c9dd771bc4b7067923598a35ef2fda674ec85d9fadcfac8a",
        "expected_diagnostic": "literal object-language Omega identifier forbidden by T05 lexical check",
    },
    "Audit/fixtures/T05-symbol-omega.fixture": {
        "claim_id": "AR3-22",
        "canonical_lf_sha256": "ab0931bbfe7ed4d37024ee4c15068dd605c4490452e6a28c2d06ca3372b625ed",
        "expected_diagnostic": "literal object-language Omega identifier forbidden by T05 lexical check",
    },
    "Audit/fixtures/AR3-explanatory-shorthand-status.fixture": {
        "claim_id": "AR3-23",
        "canonical_lf_sha256": "1e3d1d2680f8a920a91784543e030268f7b5eac74b625e75ae688e4bc52b56a9",
        "expected_diagnostic": "selected declaration spelling would promote explanatory shorthand to an object-language primitive or status",
    },
    "Audit/fixtures/AR3-first-occurrence-closure.fixture": {
        "claim_id": "AR3-24",
        "canonical_lf_sha256": "edb1a28dd9418d76c6e9bff80d9dd5668149a90b3cba84e2b486f82fa4c3e6be",
        "expected_diagnostic": "selected declaration spelling would purport to close an OPEN first-occurrence burden",
    },
}
EXPECTED_NEGATIVE_CONTROLS = {
    "AR3-N01": (
        "A0 is globally or causally first.",
        "COUNTERMODEL_TO_OVERCLAIM",
        ["AR3-02"],
    ),
    "AR3-N02": (
        "A recorded cost proves source, truth, energy, permission, consent, standing, or authority.",
        "COUNTERMODEL_TO_OVERCLAIM",
        ["AR3-05"],
    ),
    "AR3-N03": (
        "An A0 receipt alone proves occurrence closure.",
        "COUNTERMODEL_TO_OVERCLAIM",
        ["AR3-09"],
    ),
    "AR3-N04": (
        "A later witness retroactively creates an earlier witness or payment.",
        "PROVED_FROM_DECLARED_RULES",
        ["AR3-20"],
    ),
    "AR3-N05": (
        "A cut-only interface uniquely identifies its source without injectivity or discriminating evidence.",
        "COUNTERMODEL_TO_OVERCLAIM",
        ["AR3-16", "AR3-17"],
    ),
    "AR3-N06": (
        "Asking or producing its receipt proves the inquirer’s ontology, consciousness, standing, ultimate source, or global priority, or witnesses the original cut’s causal source.",
        "COUNTERMODEL_TO_OVERCLAIM",
        ["AR3-13", "AR3-14"],
    ),
    "AR3-N07": (
        "Reopenable inquiry proves an actually infinite causal ontology.",
        "COUNTERMODEL_TO_OVERCLAIM",
        ["AR3-19"],
    ),
    "AR3-N08": (
        "Appending evidence permits alteration of the earlier receipt or authority snapshot.",
        "COUNTERMODEL_TO_OVERCLAIM",
        ["AR3-20", "AR3-21"],
    ),
    "AR3-N09": (
        "Occurrence-closed, source-open functions as a primitive PAL status.",
        "EXPECTED_REJECTION",
        ["AR3-23", "AR3-25"],
    ),
    "AR3-N10": (
        "A formal proof closes O04, O25, or D-FIRST-OCCURRENCE.",
        "EXPECTED_REJECTION",
        ["AR3-24"],
    ),
}
EXPECTED_ADDITIONAL_CONTROLS = {
    "AR3-T39-MISSING-WITNESS": {
        "pal_route": ["D22", "SC-19.7", "M-INQUIRY-APPEND", "T39"],
        "attempted_nonconformance": "A further inquiry receipt is admitted without its own independent event witness.",
        "disposition": "COUNTERMODEL_TO_OVERCLAIM",
        "evidence": ["AR3-13"],
    },
    "AR3-T39-MISSING-COST": {
        "pal_route": ["D22", "SC-19.7", "M-INQUIRY-APPEND", "T39"],
        "attempted_nonconformance": "A further inquiry receipt is admitted without its own independent cost witness.",
        "disposition": "PROVED_FROM_DECLARED_RULES",
        "evidence": ["AR3-18"],
    },
}
EXPECTED_MANUAL_TARGET = {
    "claim_id": "AR3-25",
    "status": "OPEN_MANUAL",
    "target": "Semantic-surrogate and authority review for differently named unresolved-possibility objects, explanatory-status promotion, and formal obligation-closure claims.",
}
EXPECTED_ACTION_REFS = Counter(
    {
        "actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803": 1,
        "leanprover/lean-action@38fbc41a8c28c4cbaec22d7f7de508ec2e7c0dd9": 2,
        "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02": 2,
    }
)


def fail(message: str) -> None:
    raise ValueError(message)


def load(path: pathlib.Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def canonical_lf_sha256(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    return hashlib.sha256(
        text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    ).hexdigest()


def main() -> int:
    receipt = load(RECEIPT_PATH)
    ledger = load(LEDGER_PATH)
    pal_text = PAL_SOURCE.read_text(encoding="utf-8")
    audit_text = AUDIT_SOURCE.read_text(encoding="utf-8")
    if receipt.get("run_id") != "attack-0003" or ledger.get("run_id") != "attack-0003":
        fail("run identity mismatch")
    if receipt.get("audit_direction") != "PAL_AUDITS_DECLARED_LEAN_REALIZATIONS":
        fail("Attack Run 0003 is not recorded as PAL-led")
    if receipt.get("controlling_release") != "PAL v2.1":
        fail("PAL v2.1 must control Attack Run 0003")
    if receipt.get("formal_evidence_is_adoption_authority") is not False:
        fail("formal evidence cannot be adoption authority")
    if (
        receipt.get("source_manifest") != SOURCE_MANIFEST_ROUTE
        or receipt.get("adoption_receipt") != ADOPTION_RECEIPT_ROUTE
        or receipt.get("migration_receipt") != MIGRATION_RECEIPT_ROUTE
    ):
        fail("Attack Run 0003 has an incorrect source/adoption/migration route")
    identity = receipt.get("version_control_identity", {})
    if (
        identity.get("branch") != GATE5_BRANCH
        or identity.get("base_sha") != BASELINE_COMMIT
    ):
        fail("Attack Run 0003 has an incorrect branch or baseline identity")
    future_identity_fields = (
        "pr_number",
        "pr_head_sha",
        "tested_merge_sha",
        "final_merge_sha",
    )
    if any(identity.get(field) is not None for field in future_identity_fields):
        fail("Attack Run 0003 must not guess future PR or merge identities")
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    action_refs = Counter(re.findall(r"^\s*uses:\s+([^\s#]+)", workflow_text, re.MULTILINE))
    if action_refs != EXPECTED_ACTION_REFS:
        fail("GitHub Actions must remain pinned to the reviewed immutable commits")

    theorem_names = set(re.findall(r"^theorem\s+([A-Za-z0-9_']+)", pal_text, re.MULTILINE))
    if theorem_names != REQUIRED_THEOREMS:
        fail(
            f"classified theorem set mismatch: missing={sorted(REQUIRED_THEOREMS - theorem_names)}, "
            f"unexpected={sorted(theorem_names - REQUIRED_THEOREMS)}"
        )
    printed = re.findall(r"^#print axioms\s+(\S+)\s*$", audit_text, re.MULTILINE)
    dependencies = receipt.get("dependency_receipts", [])
    dependency_names = [row.get("declaration") for row in dependencies]
    if len(dependency_names) != len(set(dependency_names)) or set(printed) != set(dependency_names):
        fail("every explicit declaration must have exactly one dependency receipt")
    if len(printed) != 73:
        fail(f"expected 73 explicit declaration receipts, observed {len(printed)}")
    classified_dependencies = {
        row["declaration"].removeprefix("PAL.AttackRun0003.")
        for row in dependencies
        if row.get("role") == "CLASSIFIED_RESULT"
    }
    if classified_dependencies != REQUIRED_THEOREMS:
        fail("classified theorem dependency roles are incomplete")
    custom_axioms = {
        axiom
        for row in dependencies
        for axiom in row.get("axioms", [])
        if axiom not in {"propext", "Quot.sound"}
    }
    if custom_axioms:
        fail(f"undeclared custom axioms found: {sorted(custom_axioms)}")

    results = receipt.get("results", [])
    claims = ledger.get("claims", [])
    result_map = {row.get("id"): row.get("classification") for row in results}
    claim_map = {row.get("id"): row.get("classification") for row in claims}
    if len(result_map) != len(results) or len(claim_map) != len(claims):
        fail("duplicate result or claim id")
    if result_map != claim_map or set(result_map.values()) - STATUSES:
        fail("run receipt and claim ledger classifications differ")
    expected_formal_claim_ids = [f"AR3-{index:02d}" for index in range(1, 22)]
    formal_source = receipt.get("formal_target_source_identity", {})
    if (
        formal_source.get("path") != FORMAL_SOURCE_ROUTE
        or formal_source.get("canonical_lf_sha256") != FORMAL_SOURCE_SHA256
        or formal_source.get("claim_ids") != expected_formal_claim_ids
        or not formal_source.get("identity_rule")
        or canonical_lf_sha256(PAL_SOURCE) != FORMAL_SOURCE_SHA256
    ):
        fail("formal target source bytes or claim route changed")
    formal_claim_ids = [
        claim["id"]
        for claim in claims
        if claim["classification"]
        not in {"EXPECTED_REJECTION", "OPEN_MANUAL", "TRANSLATION_AMBIGUITY"}
    ]
    if formal_claim_ids != expected_formal_claim_ids:
        fail("formal target identity does not cover exactly AR3-01 through AR3-21")

    fixture_rows = receipt.get("fixture_target_identities", [])
    fixture_by_path = {row.get("path"): row for row in fixture_rows}
    if len(fixture_by_path) != len(fixture_rows) or set(fixture_by_path) != set(EXPECTED_FIXTURE_TARGETS):
        fail("fixture target identity set changed")
    for route, expected in EXPECTED_FIXTURE_TARGETS.items():
        row = fixture_by_path[route]
        if row != {"path": route, **expected}:
            fail(f"fixture target receipt changed for {route}")
        path = ROOT / route
        if canonical_lf_sha256(path) != expected["canonical_lf_sha256"]:
            fail(f"fixture target bytes changed for {route}")
        text = path.read_text(encoding="utf-8")
        diagnostics = omega_literal_diagnostics(path, text) + gate5_diagnostics(path, text)
        if len(diagnostics) != 1 or not diagnostics[0].endswith(expected["expected_diagnostic"]):
            fail(f"fixture target diagnostic changed for {route}")
    if receipt.get("manual_target_identity") != EXPECTED_MANUAL_TARGET:
        fail("OPEN_MANUAL target identity changed")

    formal_declarations = {
        declaration.removeprefix("PAL.AttackRun0003.")
        for claim in claims
        for declaration in claim.get("lean_declarations", [])
    }
    if formal_declarations != REQUIRED_THEOREMS:
        fail("claim ledger does not report every classified theorem exactly once")
    dependency_by_declaration = {
        row["declaration"]: row.get("axioms", []) for row in dependencies
    }
    if len(dependency_by_declaration) != len(dependencies):
        fail("dependency declarations must be unique")
    for claim in claims:
        declarations = claim.get("lean_declarations", [])
        missing = [
            declaration
            for declaration in declarations
            if declaration not in dependency_by_declaration
        ]
        if missing:
            fail(f"{claim.get('id')} lacks dependency receipts for {missing}")
        receipt_axioms = sorted(
            {
                axiom
                for declaration in declarations
                for axiom in dependency_by_declaration[declaration]
            }
        )
        if sorted(claim.get("axioms", [])) != receipt_axioms:
            fail(
                f"{claim.get('id')} axiom summary differs from its declaration receipts: "
                f"ledger={sorted(claim.get('axioms', []))}, receipts={receipt_axioms}"
            )

    negative_controls = receipt.get("negative_controls", [])
    control_by_id = {row.get("id"): row for row in negative_controls}
    if set(control_by_id) != REQUIRED_NEGATIVE_IDS or len(negative_controls) != 10:
        fail("required AR3-N01 through AR3-N10 negative controls are incomplete")
    for control_id, (overclaim, disposition, evidence) in EXPECTED_NEGATIVE_CONTROLS.items():
        expected = {
            "id": control_id,
            "attempted_overclaim": overclaim,
            "disposition": disposition,
            "evidence": evidence,
        }
        if control_by_id[control_id] != expected:
            fail(f"negative-control contract changed for {control_id}")
        if any(evidence_id not in result_map for evidence_id in evidence):
            fail(f"{control_id} points to missing evidence")
        if not any(result_map[evidence_id] == disposition for evidence_id in evidence):
            fail(f"{control_id} lacks evidence in its recorded disposition class")

    additional = receipt.get("additional_conformance_controls", [])
    additional_by_id = {row.get("id"): row for row in additional}
    if len(additional_by_id) != len(additional) or set(additional_by_id) != set(EXPECTED_ADDITIONAL_CONTROLS):
        fail("T39 missing-witness/missing-cost control set changed")
    claim_by_id = {claim["id"]: claim for claim in claims}
    for control_id, expected_fields in EXPECTED_ADDITIONAL_CONTROLS.items():
        expected = {"id": control_id, **expected_fields}
        if additional_by_id[control_id] != expected:
            fail(f"additional conformance-control contract changed for {control_id}")
        for evidence_id in expected_fields["evidence"]:
            if evidence_id not in result_map or "D22" not in claim_by_id[evidence_id]["pal_addresses"]:
                fail(f"{control_id} lacks D22-routed evidence")

    burdens = receipt.get("open_burdens", [])
    if len(burdens) != 1:
        fail("first occurrence must remain one debt")
    burden = burdens[0]
    if (
        burden.get("address") != "D-FIRST-OCCURRENCE"
        or burden.get("status") != "OPEN"
        or burden.get("interfaces") != ["O04", "O25"]
        or burden.get("interface_states") != {"O04": "OPEN", "O25": "OPEN"}
    ):
        fail("O04 and O25 must remain two OPEN interfaces to one OPEN debt")
    shorthand = receipt.get("occurrence_closed_source_open", {})
    if shorthand != {
        "phrase": "occurrence-closed, source-open",
        "role": "EXPLANATORY_SHORTHAND",
        "primitive": False,
        "status": False,
    }:
        fail("occurrence/source shorthand was promoted beyond explanation")

    if omega_literal_diagnostics(PAL_SOURCE, pal_text):
        fail("literal unresolved-possibility identifier entered the Lean object language")
    if gate5_diagnostics(PAL_SOURCE, pal_text):
        fail("a forbidden shorthand or debt-closure declaration entered PAL source")
    source_hash = canonical_lf_sha256(SOURCE_MANIFEST)
    if receipt.get("source_manifest_canonical_lf_sha256") != source_hash:
        fail("run receipt has a stale PAL v2.1 source-manifest hash")

    dependency_summary = receipt.get("local_validation", {}).get("dependency_receipts", {})
    expected_dependency_summary = {
        "checked_declarations": len(dependencies),
        "empty": sum(not row.get("axioms") for row in dependencies),
        "propext": sum(row.get("axioms") == ["propext"] for row in dependencies),
        "propext_and_Quot_sound": sum(
            row.get("axioms") == ["propext", "Quot.sound"] for row in dependencies
        ),
        "custom_axioms": len(custom_axioms),
    }
    if dependency_summary != expected_dependency_summary:
        fail("local validation dependency summary differs from declaration receipts")

    print(
        "Attack Run 0003 check passed: 21 classified theorems, 73 dependency "
        "receipts, 10 required overclaim controls, two additional T39 controls, "
        "eight D16-D23 routes, one OPEN debt, "
        "and no literal object-language unresolved-possibility identifier."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"Attack Run 0003 check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
