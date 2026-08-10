#!/usr/bin/env python3
"""Validate the append-only PAL v2.0 to v2.1 repository migration.

The checker distinguishes three authorities:

* published PAL v2.1 source bytes and Christopher D. Pang's adoption receipt;
* immutable historical Git objects for Attack Runs 0001 and 0002; and
* repository/CI evidence, which can validate routing but cannot adopt PAL.

When ``--published-zip`` is supplied, required members are streamed directly
from the archive and hashed without extraction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import zipfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE_MANIFEST_PATH = ROOT / "Audit" / "releases" / "pal-v2.1-source-manifest.json"
ADOPTION_RECEIPT_PATH = ROOT / "Audit" / "releases" / "pal-v2.1-adoption-receipt.json"
MIGRATION_RECEIPT_PATH = (
    ROOT / "Audit" / "migrations" / "pal-v2.0-to-v2.1-migration-receipt.json"
)
HISTORICAL_LOCK_PATH = (
    ROOT / "Audit" / "migrations" / "pal-v2.0-to-v2.1-historical-lock.json"
)

V20_DOI = "10.5281/zenodo.21754097"
V21_DOI = "10.5281/zenodo.21864767"
BASELINE_COMMIT = "144b08973fde16ebeabefc78166691afc861abec"
BASELINE_TREE = "9dffacb765366fe944959cbcff3a8bea1cecfe01"
GATE5_BRANCH = "agent/attack-run-0003-pal-led"
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
MD5_PATTERN = re.compile(r"^[0-9a-f]{32}$")
OID_PATTERN = re.compile(r"^[0-9a-f]{40}$")
PUBLISHED_ARCHIVE_FILENAME = "PAL_v2.1_Zenodo_Release.zip"
PUBLISHED_ARCHIVE_BYTE_LENGTH = 1906990
PUBLISHED_ARCHIVE_SHA256 = "a860ab48a0d754e611bdcd8d79a32db3f88f8465246d234c3df28cc5ec70964c"
PUBLISHED_ARCHIVE_MD5 = "7eed643eb48e8f5adbb8dd0d551abd83"

EXPECTED_SURFACES = {
    "PAL-v2.1-Spine": {
        "docx": (
            "PAL_v2.1_Mechanical_Structural_Spine.docx",
            "e008623ed54dbd3f8adca0fee403f5dc21a5d6d95c54b2d9453093c4dd3148f7",
            69269,
        ),
        "pdf": (
            "PAL_v2.1_Mechanical_Structural_Spine.pdf",
            "f389866e150543c1a15856e49213038d4b77c4bcdf7caaf1fc706d71bc63623f",
            654485,
        ),
    },
    "PAL-v2.1-M": {
        "docx": (
            "PAL_v2.1-M_Mathematical_Realization_Atlas.docx",
            "449a01e5af208c0afaf8cba41bf7de3a3c20a3183889e1f4ee12fdbd48ddddc1",
            77608,
        ),
        "pdf": (
            "PAL_v2.1-M_Mathematical_Realization_Atlas.pdf",
            "8a4621496c5eaad703d32027c394c9d801ce1571d2602b4ecb91d4f0e2f41238",
            854061,
        ),
    },
    "PAL-v2.1-L": {
        "docx": (
            "PAL_v2.1-L_Obligation_and_Decision_Ledger.docx",
            "80a0069aac0d3059c973fc92cabec8c47129c95cef7a0db716fa663a073b486f",
            67889,
        ),
        "pdf": (
            "PAL_v2.1-L_Obligation_and_Decision_Ledger.pdf",
            "c370618fc784d8700ff44fe37e1d0ffd333af0aa7add07db3645b45add5603af",
            733393,
        ),
    },
    "PAL-v2.1-T": {
        "docx": (
            "PAL_v2.1-T_Conformance_Tests.docx",
            "6704bd230970e78cdb20f53f1abaccbf363d40d3be7e7b821c8d406ced4b6d68",
            62596,
        ),
        "pdf": (
            "PAL_v2.1-T_Conformance_Tests.pdf",
            "2585084533c77a09a37c4a6b5ab44046978cd06967409d864a1066f5de384904",
            641052,
        ),
    },
    "PAL-v2.1-C": {
        "docx": (
            "PAL_v2.1-C_1.x_and_v2.0_Compatibility_Note.docx",
            "e4014e5a783ce48390b859cbe46666e90232bffe355a1ff8321fe56c3dbecad9",
            55889,
        ),
        "pdf": (
            "PAL_v2.1-C_1.x_and_v2.0_Compatibility_Note.pdf",
            "6394c9479229c7ed4e3293623c0c042eb43205385d8d2f70c2324f2897c6aa93",
            453602,
        ),
    },
}

EXPECTED_SUPPORTING = {
    "LICENSE.txt": (
        "8c81efe27d32f15106d90dc24ef2e804975ee90336dda52262df9d87435eba48",
        722,
    ),
    "PAL_v2.1_RELEASE_MANIFEST.txt": (
        "79aa4a2cdfdda5dc98aa32b476581da1ccebc9c85a8c692613760ff660c58f71",
        2870,
    ),
}

EXPECTED_DECISIONS = {
    "D16": {
        "title": "Account-relative primacy",
        "candidate": "C21-01",
        "disposition": "REVISED_AND_ADOPTED",
        "statement": "Within a declared PAL account, A0 is the first admitted supplied cut. This account order does not establish temporal, ontic, causal, or global primacy.",
    },
    "D17": {
        "title": "Typed cost-bearing admission",
        "candidate": "C21-02",
        "disposition": "REVISED_AND_ADOPTED",
        "statement": "Every cut admitted into a PAL account records a cut-indexed cost or obligation alongside distinct fields for scope, witness, boundary, carried trace, authority ceiling, residual, and reopening. Cost warrants ledger admission; it is not thereby causal source, truth, physical energy, permission, consent, standing, or authority.",
    },
    "D18": {
        "title": "Occurrence evidence and source ceiling",
        "candidate": "C21-03",
        "disposition": "REVISED_AND_ADOPTED_EXPLANATORY_LABEL_NOT_ADOPTED_AS_STATUS",
        "statement": "After the distinct A1/A2 witness-and-trace route has been earned, a later account may establish that the cut occurred and preserve its recoverable occurrence trace within a declared scope. Any CLOSED_IN_SCOPE claim additionally requires an A15 receipt. Ultimate causal source and global primacy remain OPEN. An A0 cut receipt alone is not an occurrence receipt.",
    },
    "D19": {
        "title": "Account order versus primacy evidence",
        "candidate": "C21-04",
        "disposition": "REVISED_AND_ADOPTED",
        "statement": "Account order and temporal, ontic, causal, or global primacy are distinct. A0 may be called first in its declared PAL account at admission. A stronger primacy claim requires later supplied evidence and a declared comparison scope; the cut or trace alone cannot establish that claim.",
    },
    "D20": {
        "title": "Supplied inquiry-event witness",
        "candidate": "C21-05",
        "disposition": "REVISED_AND_ADOPTED",
        "statement": "When an inquiry event is admitted under a supplied inquiry-event witness, PAL may record a new present inquiry receipt. That receipt does not establish the inquirer’s ontology, consciousness, standing, ultimate source, or global priority, and it does not witness the original cut’s causal source.",
    },
    "D21": {
        "title": "Cut-only source underdetermination",
        "candidate": "C21-06",
        "disposition": "TIGHTENED_AND_ADOPTED",
        "statement": "At an interface whose accessible input is only the cut, equal cut values do not warrant identification of their upstream sources. A unique-source claim requires an explicit injectivity assumption or a supplied discriminating witness.",
    },
    "D22": {
        "title": "Witnessed further inquiry",
        "candidate": "C21-07",
        "disposition": "REVISED_AND_ADOPTED",
        "statement": "When a source inquiry is admitted as a further cut, it requires its own supplied witness, cost, and receipt and preserves the prior receipt. Repeated or reopenable inquiry does not by itself prove an infinite causal ontology.",
    },
    "D23": {
        "title": "Append without backflow",
        "candidate": "C21-08",
        "disposition": "REVISED_AND_ADOPTED",
        "statement": "A later witness may append recovery evidence to an earlier receipt. Within PAL’s account it must not alter the earlier receipt, cost, witness basis, or authority snapshot, and it cannot retroactively supply warrant, consent, standing, or authority that was absent.",
    },
}

EXPECTED_PROTECTED_PATHS = {
    "PAL/AttackRun0001.lean",
    "Audit/AttackRun0001.lean",
    "Audit/attack-run-0001-receipt.json",
    "Audit/claim-ledger.json",
    "Audit/fixtures/T05-ascii-omega.fixture",
    "Audit/fixtures/T05-symbol-omega.fixture",
    "docs/generated/summary.md",
    "docs/generated/outcomes.svg",
    "PAL/AttackRun0002.lean",
    "Audit/AttackRun0002.lean",
    "Audit/attack-run-0002-receipt.json",
    "Audit/attack-run-0002-claim-ledger.json",
    "Audit/pal-2.1-impact.yaml",
    "docs/proposals/PAL-v2.1-first-cut-receipt.md",
    "docs/generated/attack-run-0002-summary.md",
    "docs/generated/attack-run-0002-outcomes.svg",
    "Audit/source-manifest.yaml",
}

REQUIRED_EXCLUDED_SURFACES = {
    "scripts/check_policy.py",
    "scripts/check_candidate_inputs.py",
    "scripts/check_axiom_receipts.py",
    "scripts/render_report.py",
    "scripts/capture_environment.sh",
    "PAL.lean",
    "Audit.lean",
    "PALLeanAudit.lean",
    ".github/workflows/lean.yml",
    "README.md",
    "AGENTS.md",
    "docs/REPORTING.md",
    "lakefile.lean",
}


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: pathlib.Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def canonical_lf_sha256(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    canonical = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def run_git(*args: str, check: bool = True, binary: bool = False) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
        check=False,
    )
    if check and result.returncode != 0:
        stderr = result.stderr if isinstance(result.stderr, str) else result.stderr.decode(errors="replace")
        fail(f"git {' '.join(args)} failed: {stderr.strip()}")
    return result


def tree_entry(ref: str, path: str) -> tuple[str, str, str]:
    result = run_git("ls-tree", ref, "--", path)
    line = result.stdout.strip()
    if not line or "\t" not in line:
        fail(f"{path} is missing from Git tree {ref}")
    metadata, observed_path = line.split("\t", 1)
    if observed_path != path:
        fail(f"Git tree path mismatch: expected {path}, observed {observed_path}")
    fields = metadata.split()
    if len(fields) != 3:
        fail(f"Malformed git ls-tree row for {path}: {line}")
    return fields[0], fields[1], fields[2]


def index_entry(path: str) -> tuple[str, str, str]:
    result = run_git("ls-files", "--stage", "--", path)
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    if len(lines) != 1 or "\t" not in lines[0]:
        fail(f"Expected one index entry for {path}, observed {len(lines)}")
    metadata, observed_path = lines[0].split("\t", 1)
    if observed_path != path:
        fail(f"Git index path mismatch: expected {path}, observed {observed_path}")
    fields = metadata.split()
    if len(fields) != 3:
        fail(f"Malformed git index row for {path}: {lines[0]}")
    return fields[0], fields[1], fields[2]


def validate_source_manifest(manifest: dict) -> dict[str, tuple[str, int]]:
    release = manifest.get("release", {})
    if release.get("name") != "PAL v2.1" or release.get("doi") != V21_DOI:
        fail("source manifest must identify published PAL v2.1 and its exact DOI")
    if release.get("publication_state") != "PUBLISHED":
        fail("PAL v2.1 source manifest must retain publication_state=PUBLISHED")
    if release.get("record_url") != f"https://doi.org/{V21_DOI}":
        fail("source manifest must retain the canonical DOI URL")
    if release.get("zenodo_record_url") != "https://zenodo.org/records/21864767":
        fail("source manifest must retain the exact Zenodo record URL")
    if release.get("author_and_adoption_authority") != "Christopher D. Pang":
        fail("source manifest must identify Christopher D. Pang as adoption authority")
    if release.get("immediate_prior_release", {}).get("doi") != V20_DOI:
        fail("source manifest must retain the exact PAL v2.0 prior DOI")

    rows = manifest.get("authority_surfaces", [])
    by_id = {row.get("id"): row for row in rows}
    if set(by_id) != set(EXPECTED_SURFACES) or len(rows) != len(EXPECTED_SURFACES):
        fail("source manifest must contain the five PAL v2.1 authority surfaces exactly once")

    package_files: dict[str, tuple[str, int]] = {}
    for surface_id, expected_artifacts in EXPECTED_SURFACES.items():
        row = by_id[surface_id]
        if row.get("included_in_repository") is not False:
            fail(f"{surface_id} must remain external to the repository")
        if not row.get("role"):
            fail(f"{surface_id} is missing its declared authority role")
        artifacts = row.get("artifacts", {})
        if set(artifacts) != {"docx", "pdf"}:
            fail(f"{surface_id} must identify exactly one DOCX and one PDF")
        for kind, (filename, digest, byte_length) in expected_artifacts.items():
            observed = artifacts[kind]
            if (
                observed.get("filename") != filename
                or observed.get("sha256") != digest
                or observed.get("byte_length") != byte_length
            ):
                fail(f"{surface_id} {kind} identity does not match the published package")
            if not SHA256_PATTERN.fullmatch(digest):
                fail(f"{surface_id} {kind} has a malformed SHA-256")
            if filename in package_files:
                fail(f"duplicate published filename in manifest: {filename}")
            package_files[filename] = (digest, byte_length)

    supporting = manifest.get("supporting_release_files", [])
    by_filename = {row.get("filename"): row for row in supporting}
    if set(by_filename) != set(EXPECTED_SUPPORTING) or len(supporting) != len(EXPECTED_SUPPORTING):
        fail("source manifest must contain the exact two supporting release files")
    for filename, (digest, byte_length) in EXPECTED_SUPPORTING.items():
        row = by_filename[filename]
        if row.get("sha256") != digest or row.get("byte_length") != byte_length:
            fail(f"supporting release identity mismatch for {filename}")
        package_files[filename] = (digest, byte_length)

    release_archive = manifest.get("release_archive", {})
    if (
        release_archive.get("filename") != PUBLISHED_ARCHIVE_FILENAME
        or release_archive.get("byte_length") != PUBLISHED_ARCHIVE_BYTE_LENGTH
        or release_archive.get("sha256") != PUBLISHED_ARCHIVE_SHA256
        or release_archive.get("md5") != PUBLISHED_ARCHIVE_MD5
        or release_archive.get("included_in_repository") is not False
    ):
        fail("source manifest has the wrong published release-archive identity")
    if not SHA256_PATTERN.fullmatch(release_archive["sha256"]) or not MD5_PATTERN.fullmatch(
        release_archive["md5"]
    ):
        fail("source manifest has a malformed release-archive digest")
    return package_files


def validate_adoption_receipt(adoption: dict, manifest_hash: str) -> None:
    if adoption.get("receipt_status") != "ADOPTED":
        fail("PAL v2.1 adoption must be recorded as ADOPTED, not pending")
    authority = adoption.get("adoption_authority", {})
    if (
        authority.get("name") != "Christopher D. Pang"
        or authority.get("decision_status") != "ADOPTED"
    ):
        fail("adoption receipt must retain Christopher D. Pang's explicit adopted decision")
    decision_kinds = {row.get("kind") for row in authority.get("decision_bases", [])}
    if decision_kinds != {"EXPLICIT_INTERACTIVE_STEWARD_DECISION", "PUBLISHED_CANONICAL_LEDGER"}:
        fail("adoption receipt must retain both the explicit decision and published ledger bases")
    release = adoption.get("adopted_release", {})
    if release.get("doi") != V21_DOI:
        fail("adoption receipt has the wrong PAL v2.1 DOI")
    if release.get("source_manifest_path") != str(SOURCE_MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/"):
        fail("adoption receipt has the wrong source-manifest route")
    if release.get("source_manifest_canonical_lf_sha256") != manifest_hash:
        fail("adoption receipt has a stale source-manifest hash")

    rows = adoption.get("adopted_decisions", [])
    by_id = {row.get("decision_id"): row for row in rows}
    if set(by_id) != set(EXPECTED_DECISIONS) or len(rows) != len(EXPECTED_DECISIONS):
        fail("adoption receipt must contain D16 through D23 exactly once")
    for decision_id, expected in EXPECTED_DECISIONS.items():
        row = by_id[decision_id]
        observed = {
            "title": row.get("title"),
            "candidate": row.get("historical_candidate_id"),
            "disposition": row.get("candidate_disposition"),
            "statement": row.get("statement"),
        }
        if observed != expected:
            fail(f"{decision_id} does not match the exact published decision mapping")
        if row.get("state") != "LOCKED":
            fail(f"{decision_id} must remain LOCKED")
        routes = row.get("source_routes", [])
        required_prefixes = ("PAL-v2.1-Spine", "PAL-v2.1-M", "PAL-v2.1-L", "PAL-v2.1-T", "PAL-v2.1-C")
        if len(routes) != 5 or any(not any(route.startswith(prefix) for route in routes) for prefix in required_prefixes):
            fail(f"{decision_id} must route across all five authority surfaces")

    burdens = {row.get("address"): row for row in adoption.get("open_burden_dispositions", [])}
    if set(burdens) != {"D-FIRST-OCCURRENCE", "O04", "O25"}:
        fail("adoption receipt must retain exactly D-FIRST-OCCURRENCE, O04, and O25")
    if any(row.get("state") != "OPEN" for row in burdens.values()):
        fail("D-FIRST-OCCURRENCE, O04, and O25 must remain OPEN")
    if burdens["D-FIRST-OCCURRENCE"].get("interfaces") != ["O04", "O25"]:
        fail("D-FIRST-OCCURRENCE must retain O04 and O25 as its two interfaces")
    explanatory = adoption.get("explanatory_language", {})
    if explanatory.get("phrase") != "occurrence-closed, source-open" or explanatory.get("status") != "EXPLANATORY_ONLY":
        fail("occurrence-closed, source-open must remain explanatory only")

    provenance = adoption.get("historical_noncanonical_provenance", [])
    expected_ids = {
        "github-issue-4",
        "github-pr-5",
        "PAL-v2.1-Candidate-Workflow",
        "PAL-v2.1-Candidate-Impact-Map",
        "PAL-v2.1-Candidate-Proposal",
    }
    if {row.get("id") for row in provenance} != expected_ids or len(provenance) != len(expected_ids):
        fail("adoption receipt must retain all five historical noncanonical provenance records")
    if any(row.get("authority_role") != "HISTORICAL_NONCANONICAL_ONLY" for row in provenance):
        fail("candidate provenance must remain historical and noncanonical only")
    evidence = adoption.get("formal_audit_evidence", {})
    if evidence.get("adoption_authority") is not False or evidence.get("evidence_role") != "NONAUTHORITATIVE_BOUNDED_FORMAL_AUDIT_EVIDENCE":
        fail("formal audit evidence must remain nonauthoritative for adoption")


def validate_historical_lock(lock: dict) -> None:
    baseline = lock.get("baseline", {})
    if baseline.get("commit_sha") != BASELINE_COMMIT or baseline.get("tree_sha") != BASELINE_TREE:
        fail("historical lock has the wrong baseline commit or tree")
    observed_tree = run_git("rev-parse", f"{BASELINE_COMMIT}^{{tree}}").stdout.strip()
    if observed_tree != BASELINE_TREE:
        fail(f"baseline commit resolves to unexpected tree {observed_tree}")
    if run_git(
        "merge-base", "--is-ancestor", BASELINE_COMMIT, "HEAD", check=False
    ).returncode != 0:
        fail("current HEAD does not extend the recorded historical baseline")

    artifacts = lock.get("protected_artifacts", [])
    by_path = {row.get("path"): row for row in artifacts}
    if set(by_path) != EXPECTED_PROTECTED_PATHS or len(artifacts) != len(EXPECTED_PROTECTED_PATHS):
        fail("historical lock must protect the exact AR1/AR2 artifact path set")

    excluded = set(lock.get("excluded_mutable_repository_surfaces", []))
    if not REQUIRED_EXCLUDED_SURFACES.issubset(excluded):
        fail("historical lock omitted a required mutable Gate 5 repository surface")
    overlap = set(by_path) & excluded
    if overlap:
        fail(f"historical artifacts cannot also be mutable surfaces: {sorted(overlap)}")

    for path, row in sorted(by_path.items()):
        expected_oid = row.get("git_blob_oid")
        expected_digest = row.get("git_blob_sha256")
        expected_length = row.get("git_blob_byte_length")
        if not isinstance(expected_oid, str) or not OID_PATTERN.fullmatch(expected_oid):
            fail(f"{path} has a malformed Git blob OID")
        if not isinstance(expected_digest, str) or not SHA256_PATTERN.fullmatch(expected_digest):
            fail(f"{path} has a malformed Git blob SHA-256")

        baseline_entry = tree_entry(BASELINE_COMMIT, path)
        expected_entry = (row.get("mode"), row.get("git_type"), expected_oid)
        if baseline_entry != expected_entry:
            fail(f"{path} baseline tree entry changed: {baseline_entry} != {expected_entry}")
        if tree_entry("HEAD", path) != expected_entry:
            fail(f"{path} current HEAD blob differs from the historical lock")
        index_mode, index_oid, index_stage = index_entry(path)
        if (index_mode, index_oid, index_stage) != (row.get("mode"), expected_oid, "0"):
            fail(f"{path} index entry differs from the historical lock")

        blob = run_git("cat-file", "blob", expected_oid, binary=True).stdout
        if len(blob) != expected_length:
            fail(f"{path} Git blob length changed: {len(blob)} != {expected_length}")
        if hashlib.sha256(blob).hexdigest() != expected_digest:
            fail(f"{path} Git object bytes do not match the locked SHA-256")

        if run_git("diff", "--quiet", BASELINE_COMMIT, "--", path, check=False).returncode != 0:
            fail(f"{path} filtered working-tree content differs from the baseline")
        if run_git("diff", "--cached", "--quiet", BASELINE_COMMIT, "--", path, check=False).returncode != 0:
            fail(f"{path} staged content differs from the baseline")


def validate_migration_receipt(
    migration: dict,
    manifest_hash: str,
    adoption_hash: str,
    historical_lock_hash: str,
) -> None:
    if migration.get("human_adoption_status") != "ADOPTED":
        fail("migration receipt must not mark PAL v2.1 adoption pending")
    if migration.get("migration_status") != "IMPLEMENTED_LOCAL_VALIDATION_PASSED_CI_PENDING":
        fail("migration receipt has an unexpected migration status")
    from_release = migration.get("from_release", {})
    if from_release.get("doi") != V20_DOI:
        fail("migration receipt has the wrong PAL v2.0 DOI")
    if from_release.get("historical_source_manifest") != "Audit/source-manifest.yaml":
        fail("migration receipt has the wrong historical PAL v2.0 source route")
    target = migration.get("to_release", {})
    if target.get("doi") != V21_DOI:
        fail("migration receipt has the wrong PAL v2.1 DOI")
    expected_paths = {
        "source_manifest_path": "Audit/releases/pal-v2.1-source-manifest.json",
        "adoption_receipt_path": "Audit/releases/pal-v2.1-adoption-receipt.json",
    }
    for field, expected in expected_paths.items():
        if target.get(field) != expected:
            fail(f"migration receipt has the wrong linked path {field}")
    linked_hashes = {
        "source_manifest_canonical_lf_sha256": manifest_hash,
        "adoption_receipt_canonical_lf_sha256": adoption_hash,
    }
    for field, expected in linked_hashes.items():
        if target.get(field) != expected:
            fail(f"migration receipt has stale linked hash {field}")
    baseline = migration.get("repository_baseline", {})
    if (
        baseline.get("repository") != "Grativy6/PAL-Lean-Audit"
        or baseline.get("main_sha") != BASELINE_COMMIT
        or baseline.get("tree_sha") != BASELINE_TREE
    ):
        fail("migration receipt has the wrong repository baseline")
    if baseline.get("historical_lock_canonical_lf_sha256") != historical_lock_hash:
        fail("migration receipt has a stale historical-lock hash")
    if (
        baseline.get("historical_lock_path")
        != "Audit/migrations/pal-v2.0-to-v2.1-historical-lock.json"
    ):
        fail("migration receipt has the wrong historical-lock path")

    identity = migration.get("version_control_identity", {})
    if (
        identity.get("branch") != GATE5_BRANCH
        or identity.get("base_sha") != BASELINE_COMMIT
        or identity.get("base_sha") != baseline.get("main_sha")
    ):
        fail("migration version-control branch/base route is inconsistent")
    nullable = (
        "migration_pr_number",
        "migration_pr_base_sha",
        "migration_pr_head_sha",
        "tested_merge_sha",
        "final_merge_sha",
    )
    if any(identity.get(field) is not None for field in nullable):
        fail("future migration PR/tested/final merge identities must remain null")
    if identity.get("identity_status") != "NOT_YET_AVAILABLE":
        fail("future version-control identities must be explicitly unavailable")

    mappings = migration.get("decision_mappings", [])
    by_decision = {row.get("adopted_decision_id"): row for row in mappings}
    if set(by_decision) != set(EXPECTED_DECISIONS) or len(mappings) != len(EXPECTED_DECISIONS):
        fail("migration receipt must map D16 through D23 exactly once")
    for decision_id, expected in EXPECTED_DECISIONS.items():
        row = by_decision[decision_id]
        if (
            row.get("historical_candidate_id") != expected["candidate"]
            or row.get("adopted_title") != expected["title"]
            or row.get("adoption_disposition") != expected["disposition"]
            or row.get("evidence_authority") != "NONAUTHORITATIVE"
        ):
            fail(f"migration mapping for {decision_id} is inconsistent with adoption")

    burdens = {row.get("address"): row for row in migration.get("open_burden_carry_forward", [])}
    if set(burdens) != {"D-FIRST-OCCURRENCE", "O04", "O25"}:
        fail("migration receipt must carry exactly D-FIRST-OCCURRENCE, O04, and O25")
    if any(row.get("from_state") != "OPEN" or row.get("to_state") != "OPEN" for row in burdens.values()):
        fail("migration must retain D-FIRST-OCCURRENCE, O04, and O25 OPEN")
    if burdens["D-FIRST-OCCURRENCE"].get("interfaces") != ["O04", "O25"]:
        fail("migration must retain O04 and O25 as two interfaces to one debt")
    if migration.get("explanatory_language", {}).get("status") != "EXPLANATORY_ONLY":
        fail("occurrence-closed, source-open must remain explanatory only")
    if any(
        row.get("authority_role") != "HISTORICAL_NONCANONICAL_ONLY"
        for row in migration.get("historical_noncanonical_material", [])
    ):
        fail("candidate workflow/map/proposal and GitHub records must remain noncanonical")


def verify_published_zip(
    zip_path: pathlib.Path,
    expected_files: dict[str, tuple[str, int]],
) -> None:
    if not zip_path.is_file():
        fail(f"published ZIP does not exist: {zip_path}")
    if zip_path.name != PUBLISHED_ARCHIVE_FILENAME:
        fail(
            f"published ZIP filename mismatch: {zip_path.name} != "
            f"{PUBLISHED_ARCHIVE_FILENAME}"
        )
    if zip_path.stat().st_size != PUBLISHED_ARCHIVE_BYTE_LENGTH:
        fail(
            f"published ZIP byte length mismatch: {zip_path.stat().st_size} != "
            f"{PUBLISHED_ARCHIVE_BYTE_LENGTH}"
        )
    archive_sha256 = hashlib.sha256()
    archive_md5 = hashlib.md5(usedforsecurity=False)
    with zip_path.open("rb") as archive_bytes:
        while True:
            chunk = archive_bytes.read(1024 * 1024)
            if not chunk:
                break
            archive_sha256.update(chunk)
            archive_md5.update(chunk)
    if archive_sha256.hexdigest() != PUBLISHED_ARCHIVE_SHA256:
        fail("published ZIP SHA-256 does not match the release manifest")
    if archive_md5.hexdigest() != PUBLISHED_ARCHIVE_MD5:
        fail("published ZIP MD5 does not match the Zenodo archive identity")
    with zipfile.ZipFile(zip_path) as archive:
        members = [info for info in archive.infolist() if not info.is_dir()]
        basenames: dict[str, zipfile.ZipInfo] = {}
        for info in members:
            basename = pathlib.PurePosixPath(info.filename).name
            if basename in basenames:
                fail(f"published ZIP contains duplicate basename {basename}")
            basenames[basename] = info
        if set(basenames) != set(expected_files):
            fail(
                "published ZIP member set mismatch: "
                f"missing={sorted(set(expected_files) - set(basenames))}, "
                f"unexpected={sorted(set(basenames) - set(expected_files))}"
            )
        for filename, (expected_digest, expected_length) in sorted(expected_files.items()):
            info = basenames[filename]
            if info.flag_bits & 0x1:
                fail(f"published ZIP member is encrypted: {info.filename}")
            if info.file_size != expected_length:
                fail(
                    f"published ZIP length mismatch for {filename}: "
                    f"{info.file_size} != {expected_length}"
                )
            digest = hashlib.sha256()
            byte_count = 0
            with archive.open(info, "r") as handle:
                while True:
                    chunk = handle.read(1024 * 1024)
                    if not chunk:
                        break
                    digest.update(chunk)
                    byte_count += len(chunk)
            if byte_count != expected_length or digest.hexdigest() != expected_digest:
                fail(f"published ZIP bytes do not match the manifest for {filename}")
    print(f"Verified {len(expected_files)} published PAL v2.1 ZIP members: {zip_path}")


def run_historical_regressions() -> None:
    commands = (
        [sys.executable, "scripts/check_candidate_inputs.py"],
        [sys.executable, "scripts/render_report.py", "--check"],
        [
            sys.executable,
            "scripts/render_report.py",
            "--ledger",
            "Audit/attack-run-0002-claim-ledger.json",
            "--summary",
            "docs/generated/attack-run-0002-summary.md",
            "--chart",
            "docs/generated/attack-run-0002-outcomes.svg",
            "--check",
        ],
    )
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode != 0:
            fail(f"historical regression command failed: {' '.join(command)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--published-zip",
        type=pathlib.Path,
        help="optionally stream-verify the exact published PAL v2.1 release ZIP",
    )
    args = parser.parse_args()

    manifest = load_json(SOURCE_MANIFEST_PATH)
    adoption = load_json(ADOPTION_RECEIPT_PATH)
    migration = load_json(MIGRATION_RECEIPT_PATH)
    historical_lock = load_json(HISTORICAL_LOCK_PATH)
    manifest_hash = canonical_lf_sha256(SOURCE_MANIFEST_PATH)
    adoption_hash = canonical_lf_sha256(ADOPTION_RECEIPT_PATH)
    historical_lock_hash = canonical_lf_sha256(HISTORICAL_LOCK_PATH)

    package_files = validate_source_manifest(manifest)
    validate_adoption_receipt(adoption, manifest_hash)
    validate_historical_lock(historical_lock)
    validate_migration_receipt(
        migration,
        manifest_hash,
        adoption_hash,
        historical_lock_hash,
    )
    if args.published_zip is not None:
        verify_published_zip(args.published_zip.resolve(), package_files)
    run_historical_regressions()
    print(
        "Release migration check passed: PAL v2.1 published identities and "
        "D16-D23 adoption verified; 17 historical AR1/AR2 Git blobs preserved; "
        "D-FIRST-OCCURRENCE, O04, and O25 remain OPEN."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, zipfile.BadZipFile) as error:
        print(f"Release migration check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
