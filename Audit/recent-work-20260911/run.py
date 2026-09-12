"""Replay and verify a finite source-bound local supplement; never publish or adopt.

Source bytes are raw SHA256. Repository input hashes normalize CRLF to LF for
portable replay; evidence logs are LF UTF-8 and hash-checked byte-for-byte.
"""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import argparse
import copy
import hashlib
import json
import platform
import re
import subprocess
import sys
import time

if not __debug__:
    raise RuntimeError('Receipt validation requires Python assertions enabled; do not use -O.')

ROOT = Path(__file__).resolve().parents[2]
AREA = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from check_policy import strip_lean_comments_and_strings, OMEGA_LITERAL_IDENTIFIER
from run_pal23_charter import parse_axioms

LANES = {'pal': 'Pal23Followup', 'charter': 'CharterFollowup', 'bridge': 'Bridge'}
CLASSIFICATIONS = {'PROVED_FROM_DECLARED_RULES', 'ASSUMPTION_BOUND', 'COUNTERMODEL_TO_OVERCLAIM'}
OBLIGATIONS = {'O04': 'OPEN', 'O25': 'OPEN', 'D-FIRST-OCCURRENCE': 'OPEN', 'multi_parent_lineage_boundary': 'OPEN'}
RESULT = AREA / 'results.json'
REPORT = AREA / 'SUMMARY.md'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')


def sha(path, canonical=False):
    raw = path.read_bytes()
    return hashlib.sha256(raw.replace(b'\r\n', b'\n') if canonical else raw).hexdigest()


def relative(path):
    return path.relative_to(ROOT).as_posix()


def verify_sources():
    manifest = read(AREA / 'source-manifest.json')
    assert len(manifest['sources']) == 7, 'Expected seven sources'
    checks = []
    for source in manifest['sources']:
        path = Path(source['path'])
        assert path.stat().st_size == source['bytes'] and sha(path) == source['sha256'], f'Source changed: {source["id"]}'
        assert sha(ROOT / source['extraction']) == source['extraction_sha256'], f'Extraction changed: {source["id"]}'
        checks.append({'id': source['id'], 'sha256': source['sha256'], 'status': 'MATCH'})
    assert len({s['id'] for s in checks}) == 7, 'Duplicate source ids'
    return checks


def inventory():
    sources = {s['id']: s for s in read(AREA / 'source-manifest.json')['sources']}
    records, names = {}, {}
    all_ids = []
    fields = {'id', 'title', 'classification', 'declaration', 'statement', 'source_refs', 'assumptions', 'countercase', 'authority_ceiling', 'residual', 'reopening'}
    for lane, module in LANES.items():
        record = read(AREA / f'{lane}-claims.json')
        assert record['lane'] == lane and isinstance(record['manual_dispositions'], list)
        claims = record['claims']
        minimum, maximum = (4, 6) if lane == 'bridge' else (3, 5)
        assert minimum <= len(claims) <= maximum, f'Frozen count: {lane}'
        raw = (ROOT / f'Experiments/{module}.lean').read_text(encoding='utf-8')
        code = strip_lean_comments_and_strings(raw)
        assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b', code), f'Forbidden token: {module}'
        assert not OMEGA_LITERAL_IDENTIFIER.search(code), f'Literal identifier guard: {module}'
        expected = [f'Experiments.{module}.{name}' for name in re.findall(r'^theorem\s+(\w+)', code, re.M)]
        axiom_code = (ROOT / f'Experiments/{module}Axioms.lean').read_text(encoding='utf-8')
        assert Counter(re.findall(r'^#print axioms (\S+)', axiom_code, re.M)) == Counter(expected), f'Axiom inventory: {module}'
        assert Counter(c['declaration'] for c in claims) == Counter(expected), f'Claim inventory: {module}'
        assert len(set(expected)) == len(expected), f'Duplicate declarations: {module}'
        for c in claims:
            assert fields <= c.keys(), f'Incomplete claim {c.get("id")}'
            assert all(c[k] for k in fields - {'assumptions'}), f'Empty metadata {c["id"]}'
            assert isinstance(c['assumptions'], list) and c['classification'] in CLASSIFICATIONS
            for ref in c['source_refs']:
                source = sources[ref['source_id']]
                match = re.fullmatch(r'P(\d{4})(?:-P(\d{4}))?', ref['paragraphs'])
                assert match, f'Invalid paragraph locator: {ref}'
                start, end = int(match[1]), int(match[2] or match[1])
                assert 1 <= start <= end <= source['paragraphs']
                rows = (ROOT / source['extraction']).read_text(encoding='utf-8').splitlines()
                text = ' '.join(row[6:] for row in rows if start <= int(row[1:5]) <= end)
                assert ' '.join(ref['excerpt'].split()) in ' '.join(text.split()), f'Excerpt mismatch {c["id"]}: {ref}'
            all_ids.append(c['id'])
        records[lane], names[lane] = record, expected
    assert len(all_ids) == len(set(all_ids)), 'Duplicate claim ids'
    return records, names


def input_hashes():
    paths = [ROOT / 'lean-toolchain', ROOT / 'lake-manifest.json', ROOT / 'lakefile.lean', ROOT / 'AGENTS.md', ROOT / 'docs/REPORTING.md', ROOT / '.gitattributes',
        ROOT / 'scripts/check_policy.py', ROOT / 'scripts/run_pal23_charter.py', ROOT / 'Audit/pal-v23-charter/check_publication.py',
        AREA / '.gitattributes', AREA / 'source-manifest.json', AREA / 'extract_sources.py', AREA / 'run.py', AREA / 'REVIEW.md']
    for lane, module in LANES.items():
        paths += [AREA / f'{lane}-claims.json', ROOT / f'Experiments/{module}.lean', ROOT / f'Experiments/{module}Axioms.lean']
    # Lock all imported project modules too. Mathlib identity is in lake-manifest.
    paths += sorted((ROOT / 'PAL').rglob('*.lean')) + sorted((ROOT / 'Audit').glob('*.lean'))
    paths += [ROOT / p for p in ('Experiments.lean', 'Experiments/Pal23.lean', 'Experiments/Charter.lean', 'PAL.lean', 'Audit.lean', 'PALLeanAudit.lean')]
    return {relative(p): sha(p, True) for p in paths}


def commands(lake, evidence):
    result = [('lean-version', [lake, 'env', 'lean', '--version']), ('lake-build', [lake, 'build'])]
    result.append(('build-supplement', [lake, 'build'] + [f'Experiments.{m}' for m in LANES.values()]))
    for lane, module in LANES.items():
        result += [(f'{lane}-axioms', [lake, 'env', 'lean', f'Experiments/{module}Axioms.lean']),
            (f'{lane}-kernel', [lake, 'env', 'leanchecker', f'Experiments.{module}'])]
    result += [('historical-kernel', [lake, 'env', 'leanchecker', 'PALLeanAudit']),
        ('preserved-replay', [sys.executable, 'Audit/pal-v23-charter/check_publication.py', '--replay', '--lake', lake, '--output-dir', str(evidence / 'preserved-replay')])]
    for label, argv in [
        ('policy', ['scripts/check_policy.py']),
        ('candidate-inputs', ['scripts/check_candidate_inputs.py']),
        ('ar3-policy', ['scripts/check_attack_run_0003_policy.py']),
        ('ar3-structure', ['scripts/check_attack_run_0003.py']),
        ('migration-metadata', ['scripts/check_release_migration.py']),
        ('historical-report', ['scripts/render_report.py', '--check']),
        ('migration-report', ['scripts/render_migration_report.py', '--check']),
        ('ar3-report', ['scripts/render_attack_run_0003.py', '--check'])]:
        result.append((label, [sys.executable] + argv))
    result.append(('diff-check', ['git', 'diff', '--check']))
    return result


def report(records, result):
    lines = ['# PAL CHARTER and BRIDGE bounded Lean audit', '',
        f'Local execution: **{result["status"]}**. Source identity: all seven supplied DOCX files verified by SHA256.', '',
        'This is a finite supplement to the 2026-09-07 experiments. Historical Attack Runs 0001-0003 keep their original release scope. The user-selected PAL v2.3, CHARTER v1.0 and BRIDGE v0.4 documents control this supplement only.', '',
        '| Work | New checked declarations | Classifications |', '|---|---:|---|']
    for lane, record in records.items():
        counts = Counter(c['classification'] for c in record['claims'])
        lines.append(f'| {lane.upper()} | {len(record["claims"])} | ' + '; '.join(f'{k}: {v}' for k,v in sorted(counts.items())) + ' |')
    lines += ['', 'Counts are theorem declarations, not independent scientific findings or full source conformance. The preserved 27-declaration PAL/CHARTER replay is a separate population. Each named module passed the bundled Lean kernel checker; exact dependencies appear in results.json.', '']
    for lane, record in records.items():
        lines += [f'## {lane.upper()}', '']
        for c in record['claims']:
            lines += [f'- **{c["id"]}: {c["title"]}** ({c["classification"]}). {c["residual"]}']
        lines += ['', 'Manual dispositions (not Lean results):', '']
        for item in record['manual_dispositions']:
            lines.append('- ' + (item if isinstance(item, str) else json.dumps(item, ensure_ascii=False)))
        lines += ['']
    lines += ['## Evidence and limits', '',
        '- [Exact statements and PAL source mapping](pal-claims.json), [CHARTER mapping](charter-claims.json), [BRIDGE mapping](bridge-claims.json).',
        '- [Execution receipt](results.json), [source lock](source-manifest.json), and [source correspondence review](REVIEW.md).',
        '- Reproduce with `python Audit/recent-work-20260911/run.py --run`; verify with `--check`. Pass `--lake` if the pinned Lake executable is not on PATH.',
        '- Repository input digests normalize CRLF to LF; original DOCX and log digests are byte exact. Missing source files stop local verification.',
        '- PAL: Omega remains metalinguistic. O04 and O25 remain separate OPEN interfaces to D-FIRST-OCCURRENCE; multi-parent lineage remains OPEN. Finite administrative or algebraic models confer no actual authority.',
        '- BRIDGE: this batch does not verify the Hodge conjecture reduction, cycle construction, Markman coverage, monodromy, or the branch-aware boundary-lifting protocol.',
        '- Source correspondence is a review judgment; matching quotations and successful Lean checks do not prove that an encoding fully captures its prose source.',
        '- Local Windows execution only. CI was not run; no publication, source adoption, or canon amendment occurred. Historical release archive bytes were not reread.',
        '- No benchmark comparison or numerical correctness score is claimed.', '']
    return '\n'.join(lines)


def validate(result, records, names):
    assert result['status'] == 'PASS_LOCAL_BOUNDED_CHECKS'
    assert result['source_checks'] == verify_sources()
    assert result['input_canonical_lf_sha256'] == input_hashes(), 'Changed inputs'
    assert result['source_obligations'] == OBLIGATIONS, 'Changed obligation boundary'
    assert result['declaration_inventory'] == names
    assert result['ci_status'] == 'NOT_RUN' and result['publication_status'] == 'LOCAL_ONLY'
    assert result['classifications'] == {lane: {c['id']:c['classification'] for c in r['claims']} for lane,r in records.items()}
    evidence = ROOT / result['evidence_directory']
    expected = commands(result['lake'], evidence)
    assert len(result['commands']) == len(expected), 'Missing/extra command'
    deps = {}
    for command, (label, argv) in zip(result['commands'], expected):
        assert command['label'] == label and command['argv'] == argv and command['exit_code'] == 0, f'Command mismatch: {label}'
        log = ROOT / command['output']
        assert log == evidence / f'{label}.txt', 'Unexpected log path'
        assert sha(log) == command['sha256'], f'Log changed: {label}'
        assert command['elapsed_seconds'] >= 0
    for lane in LANES:
        deps.update(parse_axioms(evidence / f'{lane}-axioms.txt', names[lane]))
    assert deps == result['declaration_axioms'], 'Axiom evidence changed'
    old = read(evidence / 'preserved-replay/execution.json')
    assert old['status'] == 'PASS_DECLARED_LEAN_REPLAY' and sum(map(len, old['declaration_inventory'].values())) == 27
    assert result['preserved_replay_sha256'] == sha(evidence / 'preserved-replay/execution.json')
    for command in old['commands']:
        assert command['exit_code'] == 0 and sha(evidence / 'preserved-replay' / command['log']) == command['sha256']


def guard_tests(result, records, names):
    mutations = {
        'missing-command': lambda r: r['commands'].pop(),
        'failed-command': lambda r: r['commands'][0].update(exit_code=1),
        'changed-source': lambda r: r['source_checks'][0].update(sha256='0' * 64),
        'closed-obligation': lambda r: r['source_obligations'].update(O04='PROVED'),
        'missing-dependency': lambda r: r['declaration_axioms'].pop(next(iter(r['declaration_axioms']))),
        'changed-input': lambda r: r['input_canonical_lf_sha256'].update({'lean-toolchain': '0' * 64}),
        'changed-log-hash': lambda r: r['commands'][0].update(sha256='0' * 64),
        'invented-ci': lambda r: r.update(ci_status='PASS'),
        'duplicate-command': lambda r: r['commands'].append(r['commands'][0]),
    }
    for name, mutate in mutations.items():
        changed = copy.deepcopy(result)
        mutate(changed)
        try:
            validate(changed, records, names)
        except (AssertionError, ValueError, KeyError):
            continue
        raise AssertionError(f'Guard accepted mutation: {name}')
    return list(mutations)


def run(lake):
    records, names = inventory()
    source_checks = verify_sources()
    evidence = AREA / 'evidence' / datetime.now(timezone.utc).strftime('attempt-%Y%m%dT%H%M%S%fZ')
    evidence.mkdir(parents=True)
    result = dict(schema_version='1.0', run_id='recent-work-20260911', status='RUNNING',
        started_utc=datetime.now(timezone.utc).isoformat(), platform=platform.platform(), python=sys.version, lake=lake,
        git_base_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        git_branch=subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip(),
        worktree_status=subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True),
        source_checks=source_checks, input_canonical_lf_sha256=input_hashes(), source_obligations=OBLIGATIONS.copy(),
        ci_status='NOT_RUN', publication_status='LOCAL_ONLY', declaration_inventory=names, declaration_axioms={},
        classifications={lane:{c['id']:c['classification'] for c in r['claims']} for lane,r in records.items()},
        evidence_directory=relative(evidence), commands=[])
    try:
        for label, argv in commands(lake, evidence):
            print(f'Running {label}', flush=True)
            start = time.monotonic()
            proc = subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8', errors='replace', timeout=1200)
            log = evidence / f'{label}.txt'
            log.write_text(proc.stdout.replace('\r\n', '\n'), encoding='utf-8', newline='\n')
            result['commands'].append(dict(label=label, argv=argv, exit_code=proc.returncode, output=relative(log), sha256=sha(log), elapsed_seconds=round(time.monotonic()-start, 6)))
            if proc.returncode:
                raise RuntimeError(f'{label} failed ({proc.returncode}): {proc.stdout[-5000:]}')
            print(f'{label}: PASS', flush=True)
        for lane in LANES:
            result['declaration_axioms'].update(parse_axioms(evidence / f'{lane}-axioms.txt', names[lane]))
        result['preserved_replay_sha256'] = sha(evidence / 'preserved-replay/execution.json')
        result['status'] = 'PASS_LOCAL_BOUNDED_CHECKS'
        validate(result, records, names)
        result['receipt_guards'] = guard_tests(result, records, names)
    except Exception as error:
        result['status'] = 'FAILED_LOCAL_CHECK'
        result['error'] = str(error)
        raise
    finally:
        result['finished_utc'] = datetime.now(timezone.utc).isoformat()
        write(evidence / 'execution.json', result)
        write(RESULT, result)
    REPORT.write_text(report(records, result), encoding='utf-8', newline='\n')
    print('PASS_LOCAL_BOUNDED_CHECKS: ' + ', '.join(f'{lane}={len(r["claims"])}' for lane,r in records.items()))


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--run', action='store_true')
    mode.add_argument('--check', action='store_true')
    parser.add_argument('--lake', default=str(Path.home() / '.elan/bin/lake.exe'))
    args = parser.parse_args()
    if args.run:
        run(args.lake)
    else:
        records, names = inventory()
        result = read(RESULT)
        validate(result, records, names)
        assert result['receipt_guards'] == guard_tests(result, records, names)
        assert REPORT.read_text(encoding='utf-8') == report(records, result), 'Stale report'
        assert read(ROOT / result['evidence_directory'] / 'execution.json') == result, 'Attempt/result mismatch'
        print('PASS_RECEIPT_CHECK: source bytes, inputs, declarations, dependencies, commands, logs, report and nine rejection guards.')


if __name__ == '__main__':
    main()
