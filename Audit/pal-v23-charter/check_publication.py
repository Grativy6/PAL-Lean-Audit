#!/usr/bin/env python3
"""Verify preserved local evidence or replay the declared Lean targets in CI.

CI replay checks formal statements, not the correspondence of those statements
to unavailable source DOCX files. --source-dir separately verifies source bytes.
"""
from collections import Counter
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
AREA = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
import run_pal23_charter as original


def canonical_digest(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def verify_publication(source_dir=None):
    lock = original.read_json(AREA / 'publication-inputs.json')
    result_path = AREA / 'results.json'
    result = original.read_json(result_path)
    if original.digest(result_path) != lock['local_results_sha256']:
        raise ValueError('Original local execution receipt changed')
    if result['status'] != 'PASS_LOCAL_BOUNDED_CHECKS':
        raise ValueError('Original local execution did not pass')
    expected_paths = set(result['input_sha256'])
    if set(lock['input_canonical_lf_sha256']) != expected_paths:
        raise ValueError('Publication input inventory differs from original run')
    for name, expected in lock['input_canonical_lf_sha256'].items():
        if canonical_digest(ROOT / name) != expected:
            raise ValueError(f'Published input changed: {name}')
    claims, inventories = original.claims_and_inventory()
    if inventories != lock['declaration_inventory'] or sum(map(len, inventories.values())) != 27:
        raise ValueError('Frozen 27-name declaration inventory changed')
    if {c['id']: c['classification'] for c in claims} != lock['claim_classifications']:
        raise ValueError('Published classifications changed')
    if Counter(c['classification'] for c in claims) != Counter({
        'PROVED_FROM_DECLARED_RULES': 18, 'ASSUMPTION_BOUND': 4, 'COUNTERMODEL_TO_OVERCLAIM': 5
    }):
        raise ValueError('Publication classification populations changed')
    if [c['label'] for c in result['commands']] != original.EXPECTED_COMMANDS:
        raise ValueError('Original execution command inventory changed')
    logs = {}
    for command in result['commands']:
        log = ROOT / command['output']
        if command['exit_code'] != 0 or original.digest(log) != command['sha256']:
            raise ValueError(f'Original execution output changed: {command["label"]}')
        logs[command['label']] = log
    dependencies = {}
    for lane, names in inventories.items():
        dependencies.update(original.parse_axioms(logs[f'{lane.lower()}-axioms'], names))
    if dependencies != result['declaration_axioms']:
        raise ValueError('Original dependency receipts changed')
    manifest = original.read_json(AREA / 'source-manifest.json')
    source_checks = [{'id': s['id'], 'sha256': s['sha256'], 'status': 'MATCH'}
                     for s in manifest['sources']]
    if len(source_checks) != 6 or result['source_checks'] != source_checks:
        raise ValueError('Original six-source receipt changed')
    if result['source_obligations'] != {'D-FIRST-OCCURRENCE': 'OPEN', 'O04': 'OPEN',
        'O25': 'OPEN', 'multi_parent_lineage_boundary': 'OPEN'}:
        raise ValueError('Open-source-obligation boundary changed')
    if original.REPORT.read_text(encoding='utf-8') != original.report_text(claims, result):
        raise ValueError('Original local report differs from its generator')
    if source_dir is not None:
        for source in manifest['sources']:
            path = source_dir / source['filename']
            if path.stat().st_size != source['bytes'] or original.digest(path) != source['sha256']:
                raise ValueError(f'Supplied source bytes differ: {source["id"]}')
    print('Preserved local evidence, canonical-LF inputs, and all 27 declarations verified.')
    print('Source DOCX bytes: ' + ('VERIFIED (6)' if source_dir else 'NOT_RECHECKED'))
    return claims, inventories, dependencies


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def replay(args):
    claims, inventories, expected_dependencies = verify_publication(args.source_dir)
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    receipt = {
        'schema_version': '1.0', 'status': 'RUNNING',
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Replay of the 27 declared Lean targets; not full PAL/CHARTER conformance.',
        'source_docx_bytes_verified_this_execution': args.source_dir is not None,
        'git_checkout_sha': git('rev-parse', 'HEAD'),
        'git_tree_sha': git('rev-parse', 'HEAD^{tree}'),
        'tracked_worktree_dirty': bool(git('status', '--porcelain', '--untracked-files=no')),
        'pr_head_sha': os.environ.get('PAL23_PR_HEAD_SHA') or None,
        'pr_number': os.environ.get('PAL23_PR_NUMBER') or None,
        'github_run_id': os.environ.get('GITHUB_RUN_ID') or None,
        'platform': platform.platform(), 'python': sys.version,
        'publication_lock_sha256': original.digest(AREA / 'publication-inputs.json'),
        'declaration_inventory': inventories, 'declaration_axioms': {}, 'commands': [],
    }
    try:
        for label, argv in [
            ('lean-version', [args.lake, 'env', 'lean', '--version']),
            ('lake-build-experiments', [args.lake, 'build', 'Experiments']),
            ('pal23-axioms', [args.lake, 'env', 'lean', 'Experiments/Pal23Axioms.lean']),
            ('charter-axioms', [args.lake, 'env', 'lean', 'Experiments/CharterAxioms.lean']),
            ('leanchecker-experiments', [args.lake, 'env', 'leanchecker', 'Experiments']),
        ]:
            print(f'Running {label}', flush=True)
            proc = subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  encoding='utf-8', errors='replace', timeout=1200)
            log = output / f'{label}.txt'
            log.write_text(proc.stdout.replace('\r\n', '\n'), encoding='utf-8', newline='\n')
            receipt['commands'].append({'label': label, 'argv': argv, 'exit_code': proc.returncode,
                                        'log': log.name, 'sha256': original.digest(log)})
            if proc.returncode:
                raise RuntimeError(f'{label}: exit {proc.returncode}: {proc.stdout[-4000:]}')
        for lane, names in inventories.items():
            receipt['declaration_axioms'].update(original.parse_axioms(output / f'{lane.lower()}-axioms.txt', names))
        if receipt['declaration_axioms'] != expected_dependencies:
            raise ValueError('Live dependencies differ from the source-bound local receipt')
        verify_publication(args.source_dir)
        receipt['status'] = 'PASS_DECLARED_LEAN_REPLAY'
    except Exception as exc:
        receipt['status'] = 'FAILED_DECLARED_LEAN_REPLAY'
        receipt['error'] = str(exc)
        raise
    finally:
        receipt['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (output / 'execution.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('PASS_DECLARED_LEAN_REPLAY: 27 exact declarations and dependencies; bundled kernel passed.')


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--replay', action='store_true')
    parser.add_argument('--source-dir', type=Path, help='Optional flat directory containing the six hash-locked DOCX files.')
    parser.add_argument('--lake', default=shutil.which('lake') or str(Path.home() / '.elan/bin/lake.exe'))
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'artifacts/pal23-charter-replay')
    args = parser.parse_args()
    if args.replay:
        replay(args)
    else:
        verify_publication(args.source_dir)


if __name__ == '__main__':
    main()
