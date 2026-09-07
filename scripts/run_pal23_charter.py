#!/usr/bin/env python3
"""Run and verify the local PAL v2.3 / CHARTER experiment, without publishing.

The report is generated from exact local execution receipts. Historical audit
metadata is checked separately; this does not reverify the old release archive.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

from check_policy import strip_lean_comments_and_strings, OMEGA_LITERAL_IDENTIFIER

ROOT = Path(__file__).resolve().parents[1]
AREA = ROOT / 'Audit/pal-v23-charter'
EVIDENCE = AREA / 'evidence'
RESULT = AREA / 'results.json'
REPORT = ROOT / 'docs/generated/pal-v23-charter-local-checks.md'
LANES = ('Pal23', 'Charter')
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
FIELDS = {'id', 'run_id', 'title', 'classification', 'declaration', 'statement',
          'source_refs', 'assumptions', 'countercase', 'authority_ceiling', 'residual', 'reopening'}
EXPECTED_COMMANDS = ['lean-version', 'lake-build', 'pal23-axioms', 'charter-axioms',
                     'leanchecker-experiments', 'leanchecker-historical',
                     'historical-policy', 'historical-ar3-policy', 'historical-ar3-structure',
                     'historical-migration-metadata', 'historical-report', 'historical-ar2-report',
                     'historical-migration-report', 'historical-ar3-report', 'diff-check']


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path):
    return path.relative_to(ROOT).as_posix()


def claims_and_inventory():
    claims = []
    inventories = {}
    for lane in LANES:
        data = read_json(AREA / ('pal-claims.json' if lane == 'Pal23' else 'charter-claims.json'))
        code = strip_lean_comments_and_strings((ROOT / f'Experiments/{lane}.lean').read_text(encoding='utf-8'))
        bad = re.search(r'\b(sorry|admit|axiom|native_decide)\b', code)
        if bad or OMEGA_LITERAL_IDENTIFIER.search(code):
            raise ValueError(f'Forbidden code token in {lane}')
        names = re.findall(r'^theorem\s+(\w+)', code, re.M)
        expected = [f'Experiments.{lane}.{name}' for name in names]
        prints = re.findall(r'^#print axioms (\S+)', (ROOT / f'Experiments/{lane}Axioms.lean').read_text(encoding='utf-8'), re.M)
        if len(expected) != len(set(expected)) or Counter(expected) != Counter(prints):
            raise ValueError(f'{lane}: theorem / axiom-directive inventory mismatch')
        records = data['claims']
        if Counter(c['declaration'] for c in records) != Counter(expected):
            raise ValueError(f'{lane}: claim / theorem inventory mismatch')
        for claim in records:
            if not FIELDS <= claim.keys() or any(claim[k] is None for k in FIELDS):
                raise ValueError(f'Incomplete claim: {claim.get("id")}')
            if not claim['source_refs'] or not claim['statement']:
                raise ValueError(f'Missing source or exact statement: {claim["id"]}')
            if claim['classification'] not in {'PROVED_FROM_DECLARED_RULES', 'COUNTERMODEL_TO_OVERCLAIM', 'ASSUMPTION_BOUND'}:
                raise ValueError(f'Unsupported experiment classification: {claim["id"]}')
        claims.extend(records)
        inventories[lane] = expected
    if len({c['id'] for c in claims}) != len(claims):
        raise ValueError('Duplicate claim IDs')
    return claims, inventories


def parse_axioms(path, expected):
    text = path.read_text(encoding='utf-8')
    pattern = re.compile(r"^'([^']+)' (?:does not depend on any axioms|depends on axioms:\s*\[([^]]*)\])", re.M)
    matches = pattern.findall(text)
    if Counter(name for name, _ in matches) != Counter(expected):
        raise ValueError(f'Exact executed axiom inventory mismatch: {path}')
    results = {}
    for name, raw in matches:
        axioms = sorted(a.strip() for a in raw.split(',') if a.strip())
        if set(axioms) - ALLOWED_AXIOMS:
            raise ValueError(f'Unapproved dependency: {name}: {axioms}')
        results[name] = axioms
    return results


def input_hashes():
    paths = [ROOT / 'lean-toolchain', ROOT / 'lake-manifest.json', ROOT / 'lakefile.lean',
             ROOT / 'Experiments.lean', Path(__file__), AREA / 'source-manifest.json',
             AREA / 'pal-claims.json', AREA / 'charter-claims.json',
             ROOT / 'scripts/extract_pal23_charter_sources.py', ROOT / '.gitattributes']
    paths += sorted((ROOT / 'Experiments').glob('*.lean'))
    return {rel(p): digest(p) for p in paths}


def execute(label, argv, commands):
    print(f'Running {label}', flush=True)
    p = subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       encoding='utf-8', errors='replace', timeout=1200)
    log = EVIDENCE / f'{label}.txt'
    log.write_text(p.stdout.replace('\r\n', '\n'), encoding='utf-8', newline='\n')
    commands.append({'label': label, 'argv': [str(a) for a in argv], 'exit_code': p.returncode,
                     'output': rel(log), 'sha256': digest(log)})
    print(f'{label}: exit {p.returncode}', flush=True)
    if p.returncode:
        print(p.stdout[-9000:], flush=True)
        raise RuntimeError(f'{label} failed')


def run(lake):
    global EVIDENCE
    claims, inventories = claims_and_inventory()
    EVIDENCE = EVIDENCE / datetime.now(timezone.utc).strftime('attempt-%Y%m%dT%H%M%S%fZ')
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    manifest = read_json(AREA / 'source-manifest.json')
    source_checks = []
    for source in manifest['sources']:
        path = Path(source['path'])
        if path.stat().st_size != source['bytes'] or digest(path) != source['sha256']:
            raise ValueError(f'Source identity changed: {source["id"]}')
        source_checks.append({'id': source['id'], 'sha256': source['sha256'], 'status': 'MATCH'})
    commands = []
    result = {'schema_version': '1.0', 'experiment_id': manifest['experiment_id'],
              'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
              'platform': platform.platform(), 'python': sys.version,
              'base_commit': manifest['base_commit'], 'source_checks': source_checks,
              'commands': commands, 'declaration_axioms': {}, 'input_sha256': input_hashes(),
              'scope': 'Three local bounded run groups, partial source coverage only.',
              'ci_status': 'NOT_RUN', 'publication_status': 'LOCAL_ONLY',
              'source_obligations': {'D-FIRST-OCCURRENCE': 'OPEN', 'O04': 'OPEN', 'O25': 'OPEN',
                                     'multi_parent_lineage_boundary': 'OPEN'},
              'manual_status': 'Source-to-model correspondence remains subject to human review.',
              'historical_source_archive': 'NOT_REVERIFIED; retained metadata and Git history checked only.'}
    try:
        execute('lean-version', [lake, 'env', 'lean', '--version'], commands)
        execute('lake-build', [lake, 'build'], commands)
        for lane in LANES:
            execute(f'{lane.lower()}-axioms', [lake, 'env', 'lean', f'Experiments/{lane}Axioms.lean'], commands)
            result['declaration_axioms'].update(parse_axioms(EVIDENCE / f'{lane.lower()}-axioms.txt', inventories[lane]))
        execute('leanchecker-experiments', [lake, 'env', 'leanchecker', 'Experiments'], commands)
        execute('leanchecker-historical', [lake, 'env', 'leanchecker', 'PALLeanAudit'], commands)
        for label, args in [
            ('historical-policy', ['scripts/check_policy.py']),
            ('historical-ar3-policy', ['scripts/check_attack_run_0003_policy.py']),
            ('historical-ar3-structure', ['scripts/check_attack_run_0003.py']),
            ('historical-migration-metadata', ['scripts/check_release_migration.py']),
            ('historical-report', ['scripts/render_report.py', '--check']),
            ('historical-ar2-report', ['scripts/render_report.py', '--ledger', 'Audit/attack-run-0002-claim-ledger.json', '--summary', 'docs/generated/attack-run-0002-summary.md', '--chart', 'docs/generated/attack-run-0002-outcomes.svg', '--check']),
            ('historical-migration-report', ['scripts/render_migration_report.py', '--check']),
            ('historical-ar3-report', ['scripts/render_attack_run_0003.py', '--check']),
        ]:
            execute(label, [sys.executable] + args, commands)
        execute('diff-check', ['git', 'diff', '--check'], commands)
        if input_hashes() != result['input_sha256']:
            raise ValueError('Experiment inputs changed during execution')
        result['status'] = 'PASS_LOCAL_BOUNDED_CHECKS'
    except Exception as exc:
        result['status'] = 'FAILED_LOCAL_CHECK'
        result['error'] = str(exc)
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        serialized = json.dumps(result, indent=2) + '\n'
        RESULT.write_text(serialized, encoding='utf-8', newline='\n')
        (EVIDENCE / 'attempt-results.json').write_text(serialized, encoding='utf-8', newline='\n')
    return claims, result


def report_text(claims, result):
    counts = Counter(c['classification'] for c in claims)
    lines = ['# PAL v2.3 and CHARTER local Lean checks', '',
             f"Result: **{result['status']}**. {len(claims)} named theorem targets across three local run groups.", '',
             'The selected PAL models preserve the intended limits: a requested answer can be decoded on the reachable image exactly when equal traces cannot disagree on that answer; work-state restoration and heartbeat recurrence need not restore total state, spent resources, grants, or progress.', '',
             'The selected CHARTER arithmetic checks establish the adjacent-bank identities and a fixed-total norm minimum. The indices at m = 1, 2, 3 are prime (7, 19, 37), while m = 5 gives 91 = 7 * 13. A new derived consequence gives an entire composite subfamily:', '',
             '```text', 'n_(7k+5) = 7 * (21k^2 + 33k + 13), for every natural k.', '```', '',
             'The composite family agrees with CHARTER\'s explicit warning that adjacent-bank indices need not be prime. It is a counterexample to universal primality, not a contradiction of CHARTER. No claim about an infinite prime subsequence follows.', '',
             'Lean checks the stated realizations and counterexamples. This is partial source coverage, not a complete PAL conformance suite, proof of PAL, or full CHARTER formalization. It does not adopt or close any source claim.', '',
             'Sources: six user-supplied DOCX files matched their locked SHA-256 values. These checks use the local supplied bytes; public release-package identity was not independently verified.', '',
             '| Classification | Targets |', '|---|---:|']
    lines += [f'| {name} | {count} |' for name, count in sorted(counts.items())]
    lines += ['', '| Run | Target | Result | Lean declaration |', '|---|---|---|---|']
    lines += [f"| {c['run_id']} | {c['title']} | {c['classification']} | `{c['declaration']}` |" for c in claims]
    lines += ['', 'The classifications count theorem targets, not independent corroborations. Several targets share definitions or lemmas. PAL and CHARTER belong to one source lineage.', '',
              '## Evidence and limits', '',
              f"- Exact axiom inventory: {len(result['declaration_axioms'])} declarations, including reports with no axioms.",
              '- Allowed foundational dependencies are propext, Classical.choice, and Quot.sound; each actual dependency list is recorded in results.json. No custom axioms or proof placeholders are admitted.',
              '- The full local Lake build and bundled leanchecker checks cover Experiments and the historical PALLeanAudit module. The bundled checker is a second kernel check, not an independent scientific validation.',
              '- Existing lexical policy, retained historical metadata, and generated-report regressions are recorded separately. The old published source archive was not downloaded or reverified.',
              '- O04 and O25 remain two OPEN interfaces to the single OPEN D-FIRST-OCCURRENCE debt. The multi-parent-lineage boundary remains OPEN. These are not counted as theorem outcomes.',
              '- Broader decoder classes, full-state restoration, liveness, authority, empirical performance, prime-shell occupancy, and remaining CHARTER post-core claims are not established by this run.',
              '- CI and publication were not run. Source-to-model correspondence and adoption remain human review matters.', '',
              '## Reproduce', '',
              'With the pinned Lean toolchain, Mathlib dependencies, and the six source files available at their manifest paths:', '',
              '```text', 'python scripts/run_pal23_charter.py --run --lake <path-to-lake>',
              'python scripts/run_pal23_charter.py --check', '```', '',
              'The check command validates the stored execution evidence, input digests, exact theorem/claim/axiom inventories, and generated report. It does not pretend to rerun Lean.', '',
              'Detailed source routes, exact statements, assumptions, countercases, ceilings, and reopening conditions are in Audit/pal-v23-charter/pal-claims.json and charter-claims.json. Raw execution output and result identities are in that directory\'s evidence folder and results.json.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--run', action='store_true')
    group.add_argument('--check', action='store_true')
    parser.add_argument('--lake', default=shutil.which('lake') or str(Path.home() / '.elan/bin/lake.exe'))
    args = parser.parse_args()
    if args.run:
        claims, result = run(args.lake)
        REPORT.write_text(report_text(claims, result), encoding='utf-8', newline='\n')
    else:
        claims, inventories = claims_and_inventory()
        result = read_json(RESULT)
        if result['status'] != 'PASS_LOCAL_BOUNDED_CHECKS' or result['input_sha256'] != input_hashes():
            raise ValueError('Missing passing result or stale input evidence')
        if [c['label'] for c in result['commands']] != EXPECTED_COMMANDS:
            raise ValueError('Execution command inventory is incomplete or duplicated')
        manifest = read_json(AREA / 'source-manifest.json')
        expected_sources = [{'id': s['id'], 'sha256': s['sha256'], 'status': 'MATCH'}
                            for s in manifest['sources']]
        if len(expected_sources) != 6 or result['source_checks'] != expected_sources:
            raise ValueError('Source identity receipt inventory mismatch')
        if result['source_obligations'] != {'D-FIRST-OCCURRENCE': 'OPEN', 'O04': 'OPEN', 'O25': 'OPEN',
                                             'multi_parent_lineage_boundary': 'OPEN'}:
            raise ValueError('Source obligation boundary changed')
        for command in result['commands']:
            if command['exit_code'] != 0 or digest(ROOT / command['output']) != command['sha256']:
                raise ValueError(f'Invalid command receipt: {command["label"]}')
        observed = {}
        logs = {c['label']: ROOT / c['output'] for c in result['commands']}
        for lane in LANES:
            observed.update(parse_axioms(logs[f'{lane.lower()}-axioms'], inventories[lane]))
        if observed != result['declaration_axioms']:
            raise ValueError('Recorded dependencies differ from executed receipts')
        if REPORT.read_text(encoding='utf-8') != report_text(claims, result):
            raise ValueError('Generated report is stale')
    print(f'Checked {len(claims)} exact theorem/claim/dependency records; local evidence valid.')


if __name__ == '__main__':
    main()
