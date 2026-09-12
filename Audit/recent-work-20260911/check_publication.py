#!/usr/bin/env python3
"""Verify the frozen 13-declaration receipt or create a new portable replay.

The default check validates selected quotations, formal statements, and the
preserved local execution.  It deliberately does not claim that quotations
are a replacement for the supplied DOCX files.  --source-dir performs the
separate, optional raw-DOCX byte check.
"""
from __future__ import annotations

import argparse
import copy
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
AREA = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from check_policy import OMEGA_LITERAL_IDENTIFIER, strip_lean_comments_and_strings

if not __debug__:
    raise RuntimeError('Publication receipt validation requires assertions; do not use python -O.')
RESULT = AREA / 'results.json'
LOCK = AREA / 'publication-inputs.json'
EXCERPTS = AREA / 'source-excerpts.json'
LANES = {'pal': 'Pal23Followup', 'charter': 'CharterFollowup', 'bridge': 'Bridge'}
OPEN = {'O04': 'OPEN', 'O25': 'OPEN', 'D-FIRST-OCCURRENCE': 'OPEN', 'multi_parent_lineage_boundary': 'OPEN'}
ALLOWED_AXIOMS = {'Classical.choice', 'Quot.sound', 'propext'}
ORIGINAL_COMMAND_LABELS = [
    'lean-version', 'lake-build', 'build-supplement', 'pal-axioms', 'pal-kernel',
    'charter-axioms', 'charter-kernel', 'bridge-axioms', 'bridge-kernel',
    'historical-kernel', 'preserved-replay', 'policy', 'candidate-inputs',
    'ar3-policy', 'ar3-structure', 'migration-metadata', 'historical-report',
    'migration-report', 'ar3-report', 'diff-check',
]


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def dump(path: Path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')


def sha_bytes(data: bytes, canonical_lf=False):
    if canonical_lf:
        data = data.replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()


def sha(path: Path, canonical_lf=False):
    return sha_bytes(path.read_bytes(), canonical_lf)


def git_bytes(revision: str, path: str):
    return subprocess.check_output(['git', 'show', f'{revision}:{path}'], cwd=ROOT)


def relative(path: Path):
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def declaration_inventory():
    claims, inventory, refs = {}, {}, []
    for lane, module in LANES.items():
        record = load(AREA / f'{lane}-claims.json')
        assert record['lane'] == lane and isinstance(record['claims'], list)
        source = (ROOT / 'Experiments' / f'{module}.lean').read_text(encoding='utf-8')
        code = strip_lean_comments_and_strings(source)
        assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b', code), f'forbidden proof token: {module}'
        assert not OMEGA_LITERAL_IDENTIFIER.search(code), f'forbidden literal Omega identifier: {module}'
        named = [f'Experiments.{module}.{name}' for name in re.findall(r'^theorem\s+(\w+)', code, re.M)]
        assert named and len(named) == len(set(named)), f'declaration inventory: {module}'
        assert Counter(c['declaration'] for c in record['claims']) == Counter(named), f'claims differ: {lane}'
        axiom_directives = (ROOT / 'Experiments' / f'{module}Axioms.lean').read_text(encoding='utf-8')
        printed = re.findall(r'^#print axioms (\S+)', strip_lean_comments_and_strings(axiom_directives), re.M)
        assert Counter(printed) == Counter(named), f'axiom directive inventory: {module}'
        for claim in record['claims']:
            assert claim['id'] and claim['classification'] and claim['statement'] and claim['authority_ceiling']
            refs.extend((claim['id'], r) for r in claim['source_refs'])
        claims[lane], inventory[lane] = record, named
    all_ids = [c['id'] for r in claims.values() for c in r['claims']]
    assert len(all_ids) == len(set(all_ids)), 'duplicate claim id'
    return claims, inventory, refs


def parse_axioms(path: Path, expected):
    text = path.read_text(encoding='utf-8')
    rows = re.findall(r"'([^']+)' (does not depend on any axioms|depends on axioms: \[(.*?)\])", text, re.S)
    found = {}
    for name, form, listed in rows:
        assert name not in found, f'duplicate axiom row: {name}'
        dependencies = [] if form.startswith('does not') else [x.strip() for x in listed.replace('\n', ' ').split(',') if x.strip()]
        assert set(dependencies) <= ALLOWED_AXIOMS, f'unlisted axiom: {name}'
        found[name] = sorted(dependencies)
    assert set(found) == set(expected), f'axiom rows differ in {path.name}'
    return found


def verify_excerpts(refs, data=None):
    data = load(EXCERPTS) if data is None else data
    rows = {r['id']: r for r in data['excerpts']}
    assert len(rows) == len(data['excerpts']), 'duplicate selected excerpt'
    referenced = set()
    for claim_id, ref in refs:
        key = f"{ref['source_id']}:{ref['paragraphs']}"
        matches = [(row_id, row) for row_id, row in rows.items()
                   if (row_id == key or row_id.startswith(key + ':')) and row['text'] == ref['excerpt']]
        assert len(matches) == 1, f'missing or ambiguous selected excerpt: {claim_id}'
        row_id, row = matches[0]
        referenced.add(row_id)
        assert sha_bytes(row['text'].encode('utf-8')) == row['sha256'], f'changed selected excerpt: {key}'
        assert row['text'] == ref['excerpt'], f'claim quotation differs: {claim_id}'
    assert set(rows) == referenced, 'unreferenced selected excerpt'
    return len(rows)


def original_commands(result):
    commands = result['commands']
    assert commands and len({c['label'] for c in commands}) == len(commands), 'missing or duplicate original command'
    for command in commands:
        assert command['exit_code'] == 0 and command['elapsed_seconds'] >= 0
        log = ROOT / command['output']
        assert log.is_file() and sha(log) == command['sha256'], f'changed original log: {command["label"]}'
    return [c['label'] for c in commands]


def verify_nested_replay(old, folder: Path):
    assert old['status'] == 'PASS_DECLARED_LEAN_REPLAY' and sum(map(len, old['declaration_inventory'].values())) == 27
    assert old['commands'] and len({c['label'] for c in old['commands']}) == len(old['commands'])
    for command in old['commands']:
        assert command['exit_code'] == 0 and command['log'] and command['sha256']
        log = folder / command['log']
        assert log.is_file() and sha(log) == command['sha256'], f'changed nested preserved-replay log: {command["label"]}'


def verify_original_receipt(result, inventory):
    assert result['status'] == 'PASS_LOCAL_BOUNDED_CHECKS'
    assert result['source_obligations'] == OPEN, 'closed source obligation'
    assert sum(map(len, inventory.values())) == 13, 'frozen declaration count'
    assert result['declaration_inventory'] == inventory, 'changed declaration inventory'
    assert result['ci_status'] == 'NOT_RUN' and result['publication_status'] == 'LOCAL_ONLY'
    assert result['classifications'] == {lane: {c['id']: c['classification'] for c in load(AREA / f'{lane}-claims.json')['claims']} for lane in LANES}
    labels = original_commands(result)
    evidence = ROOT / result['evidence_directory']
    assert evidence.is_dir() and load(evidence / 'execution.json') == result, 'original receipt split'
    actual_axioms = {}
    for lane, expected in inventory.items():
        actual_axioms.update(parse_axioms(evidence / f'{lane}-axioms.txt', expected))
    assert actual_axioms == result['declaration_axioms'], 'changed original axiom inventory'
    preserved = evidence / 'preserved-replay' / 'execution.json'
    assert sha(preserved) == result['preserved_replay_sha256'], 'changed preserved replay receipt'
    verify_nested_replay(load(preserved), preserved.parent)
    assert labels == ORIGINAL_COMMAND_LABELS, 'original command inventory or ordering'


def verify_locks(result):
    lock = load(LOCK)
    assert sha(RESULT, True) == lock['historical_results_canonical_lf_sha256'], 'historical receipt changed'
    assert sha(AREA / 'SUMMARY.md', True) == lock['historical_summary_canonical_lf_sha256'], 'historical summary changed'
    assert sha(EXCERPTS, True) == lock['selected_excerpts_canonical_lf_sha256'], 'selected-excerpt file changed'
    original = result['input_canonical_lf_sha256']
    assert sha_bytes(git_bytes(lock['historical_checkout'], 'Audit.lean'), True) == lock['historical_audit_lean_sha256'] == original['Audit.lean']
    for path, digest in original.items():
        if path != 'Audit.lean':
            assert sha(ROOT / path, True) == digest, f'changed historical input: {path}'
    assert sha_bytes(git_bytes(lock['inherited_checkout'], 'Audit.lean'), True) == lock['inherited_audit_lean_sha256']
    assert sha(ROOT / 'Audit.lean', True) == lock['inherited_audit_lean_sha256'], 'current inherited Audit.lean differs'
    endpoint = 'Audit/BridgeEndpoint.lean'
    assert sha_bytes(git_bytes(lock['inherited_checkout'], endpoint), True) == lock['inherited_bridge_endpoint_sha256']
    assert sha(ROOT / endpoint, True) == lock['inherited_bridge_endpoint_sha256'], 'current inherited Bridge endpoint differs'


def replay_input_hashes():
    original = set(load(RESULT)['input_canonical_lf_sha256'])
    additions = {
        'Audit/recent-work-20260911/check_publication.py',
        'Audit/recent-work-20260911/check_publication_guards.py',
        'Audit/recent-work-20260911/publication-inputs.json',
        'Audit/recent-work-20260911/source-excerpts.json',
        'Audit/recent-work-20260911/PUBLICATION.md',
        'Audit/recent-work-20260911/SUMMARY.md',
        '.github/workflows/recent-work.yml', 'Audit.lean', 'Audit/BridgeEndpoint.lean',
    }
    return {path: sha(ROOT / path, True) for path in sorted(original | additions)}


def verify_raw_sources(source_dir: Path):
    manifest = load(AREA / 'source-manifest.json')
    rows = []
    for source in manifest['sources']:
        path = source_dir / source['filename']
        assert path.is_file() and path.stat().st_size == source['bytes'] and sha(path) == source['sha256'], f'raw DOCX mismatch: {source["id"]}'
        rows.append({'id': source['id'], 'status': 'MATCH', 'sha256': source['sha256']})
    return rows


def validate(result, with_raw=None):
    claims, inventory, refs = declaration_inventory()
    excerpt_count = verify_excerpts(refs)
    verify_original_receipt(result, inventory)
    verify_locks(result)
    raw = verify_raw_sources(with_raw) if with_raw else None
    return {'declarations': sum(map(len, inventory.values())), 'selected_excerpts': excerpt_count,
            'original_commands': len(result['commands']), 'raw_docx_check': raw}


def guard_tests():
    result = load(RESULT)
    mutations = {
        'missing-command': lambda x: x['commands'].pop(),
        'duplicate-command': lambda x: x['commands'].append(copy.deepcopy(x['commands'][0])),
        'changed-log': lambda x: x['commands'][0].update(sha256='0' * 64),
        'changed-axiom': lambda x: x['declaration_axioms'].update({next(iter(x['declaration_axioms'])): ['Unexpected.axiom']}),
        'closed-obligation': lambda x: x['source_obligations'].update({'O04': 'PROVED'}),
        'missing-claim': lambda x: x['declaration_inventory']['pal'].pop(),
        'changed-input': lambda x: x['input_canonical_lf_sha256'].update({'lean-toolchain': '0' * 64}),
    }
    for name, mutate in mutations.items():
        changed = copy.deepcopy(result)
        mutate(changed)
        try:
            validate(changed)
        except (AssertionError, KeyError, ValueError):
            continue
        raise AssertionError(f'guard accepted {name}')
    excerpts = load(EXCERPTS)
    changed = copy.deepcopy(excerpts)
    changed['excerpts'][0]['text'] += ' changed'
    try:
        _, _, refs = declaration_inventory()
        verify_excerpts(refs, changed)
    except AssertionError:
        pass
    else:
        raise AssertionError('guard accepted changed selected excerpt')
    with tempfile.TemporaryDirectory() as temporary:
        copied = Path(temporary) / 'preserved-replay'
        source = ROOT / result['evidence_directory'] / 'preserved-replay'
        shutil.copytree(source, copied)
        target = copied / load(copied / 'execution.json')['commands'][0]['log']
        # Mutate a copied nested log only; the historical receipt is never touched.
        target.write_bytes(target.read_bytes() + b'altered')
        try:
            verify_nested_replay(load(copied / 'execution.json'), copied)
        except AssertionError:
            pass
        else:
            raise AssertionError('guard accepted altered nested replay log')
    with tempfile.TemporaryDirectory() as temporary:
        failure = run_command([sys.executable, '-c', 'import sys; sys.exit(7)'], Path(temporary) / 'failure.txt')
        assert failure['exit_code'] == 7 and (Path(temporary) / 'failure.txt').is_file()
    with tempfile.TemporaryDirectory() as temporary:
        output = Path(temporary) / 'failed-replay'
        try:
            replay('definitely-missing-lake-executable', output, None, quiet=True)
        except RuntimeError:
            failed = load(output / 'execution.json')
            assert failed['status'] == 'FAILED_DECLARED_13_REPLAY'
            assert failed['commands'][0]['exit_code'] == 127
            assert (output / 'lean-version.txt').is_file()
        else:
            raise AssertionError('missing lake executable unexpectedly replayed')
    return sorted(list(mutations) + ['altered-nested-replay-log', 'changed-selected-excerpt',
                                      'failed-command-receipt', 'failed-replay-receipt'])


def run_command(argv, output: Path):
    started = time.monotonic()
    try:
        completed = subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, encoding='utf-8', errors='replace', timeout=1200)
        exit_code, text = completed.returncode, completed.stdout
    except OSError as error:
        exit_code, text = 127, f'EXECUTION_ERROR: {error}\n'
    output.write_text(text.replace('\r\n', '\n'), encoding='utf-8', newline='\n')
    return {'argv': argv, 'exit_code': exit_code, 'log': relative(output),
            'sha256': sha(output), 'elapsed_seconds': round(time.monotonic() - started, 6)}


def replay(lake: str, output_dir: Path, raw_docx_check, quiet=False):
    validate(load(RESULT))
    assert not output_dir.exists(), f'replay output already exists: {output_dir}'
    output_dir.mkdir(parents=True)
    _, inventory, _ = declaration_inventory()
    commands, dependencies = [], {}
    execution = {
        'schema_version': '1.0', 'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(),
        'tested_checkout_sha': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'pr_head_sha': os.getenv('RECENT_WORK_PR_HEAD_SHA'), 'github_run_id': os.getenv('GITHUB_RUN_ID'),
        'platform': sys.platform, 'python': sys.version, 'lean_version': None,
        'input_canonical_lf_sha256_before': replay_input_hashes(), 'declaration_inventory': inventory,
        'declaration_axioms': dependencies, 'commands': commands, 'original_results_sha256': sha(RESULT),
        'source_document_check': {'performed': bool(raw_docx_check),
                                  'results': raw_docx_check,
                                  'basis': 'raw DOCX SHA-256' if raw_docx_check else 'selected excerpts only; raw DOCX not supplied'},
    }
    try:
        if not quiet:
            print('Replaying 13 declarations', flush=True)
        steps = [('lean-version', [lake, 'env', 'lean', '--version']),
                 ('build-named-modules', [lake, 'build'] + [f'Experiments.{module}' for module in LANES.values()])]
        for label, argv in steps:
            record = run_command(argv, output_dir / f'{label}.txt')
            commands.append({'label': label, **record})
            if record['exit_code']:
                raise RuntimeError(f'{label} failed ({record["exit_code"]})')
            if label == 'lean-version':
                execution['lean_version'] = (output_dir / 'lean-version.txt').read_text(encoding='utf-8')
        for lane, module in LANES.items():
            for label, argv in [(f'{lane}-axioms', [lake, 'env', 'lean', f'Experiments/{module}Axioms.lean']),
                                (f'{lane}-kernel', [lake, 'env', 'leanchecker', f'Experiments.{module}'])]:
                record = run_command(argv, output_dir / f'{label}.txt')
                commands.append({'label': label, **record})
                if record['exit_code']:
                    raise RuntimeError(f'{label} failed ({record["exit_code"]})')
            dependencies.update(parse_axioms(output_dir / f'{lane}-axioms.txt', inventory[lane]))
        assert dependencies == load(RESULT)['declaration_axioms'], 'replay axiom inventory differs from original receipt'
        assert replay_input_hashes() == execution['input_canonical_lf_sha256_before'], 'replay input changed during execution'
        execution['status'] = 'PASS_DECLARED_13_REPLAY'
        if not quiet:
            print('PASS_DECLARED_13_REPLAY', flush=True)
    except Exception as error:
        execution['status'] = 'FAILED_DECLARED_13_REPLAY'
        execution['error'] = str(error)
        raise
    finally:
        status = subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True)
        execution['finished_utc'] = datetime.now(timezone.utc).isoformat()
        execution['worktree_status'] = status
        execution['clean_worktree'] = not bool(status.strip())
        execution['input_canonical_lf_sha256_after'] = replay_input_hashes()
        dump(output_dir / 'execution.json', execution)


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--replay', action='store_true')
    parser.add_argument('--source-dir', type=Path)
    parser.add_argument('--lake', default='lake')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'artifacts' / 'recent-work-20260911-replay')
    args = parser.parse_args()
    result = load(RESULT)
    verified = validate(result, args.source_dir)
    if args.check:
        guards = guard_tests()
        print(f"PASS_PUBLICATION_CHECK: {verified['declarations']} declarations, {verified['selected_excerpts']} selected excerpts, {verified['original_commands']} preserved commands, {len(guards)} rejection guards.")
    else:
        replay(args.lake, args.output_dir, verified['raw_docx_check'])


if __name__ == '__main__':
    main()
