"""Portable receipts for the selected BRIDGE diagram/readout Lean lanes."""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, os, platform, re, subprocess, sys, time, zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET
if not __debug__:
    raise RuntimeError('Assertions are required; do not use python -O.')
ROOT = Path(__file__).resolve().parents[2]
AREA = Path(__file__).resolve().parent
RESULT = AREA / 'results.json'
sys.path.insert(0, str(ROOT / 'scripts'))
from check_policy import strip_lean_comments_and_strings, OMEGA_LITERAL_IDENTIFIER
MODULES = {'diagram': 'BridgeDiagram', 'readout': 'BridgeReadout', 'four_sector': 'BridgeFourSector'}
OPEN = {'O04': 'OPEN', 'O25': 'OPEN', 'D-FIRST-OCCURRENCE': 'OPEN'}

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def write(p, x):
    p.write_text(json.dumps(x, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

def sha(p, canon=False):
    d = p.read_bytes()
    return hashlib.sha256(d.replace(b'\r\n', b'\n') if canon else d).hexdigest()

def rel(p):
    return p.resolve().relative_to(ROOT).as_posix()

def parse_axioms(path, names):
    rows = re.findall("'([^']+)' (does not depend on any axioms|depends on axioms: \\[(.*?)\\])", path.read_text(encoding='utf-8'), re.S)
    out = {}
    for n, kind, values in rows:
        assert n not in out
        out[n] = [] if kind.startswith('does not') else sorted((x.strip() for x in values.replace('\n', ' ').split(',') if x.strip()))
        assert set(out[n]) <= {'Classical.choice', 'Quot.sound', 'propext'}
    assert set(out) == set(names)
    return out

def inventory():
    manifest = read(AREA / 'source-manifest.json')
    snap = ROOT / manifest['source_excerpts']
    assert sha(snap) == manifest['source_excerpts_sha256']
    context = ROOT / manifest['source_context']
    assert sha(context) == manifest['source_context_sha256']
    for path, expected in [(snap, {f'P{i:04d}' for i in range(108, 200)}), (context, {'P0036', 'P0087', 'P0107'})]:
        data = read(path)
        assert data['source_id'] == manifest['source_id'] and data['source_sha256'] == manifest['sha256']
        assert len(data['paragraphs']) == len(expected) and {p['paragraph'] for p in data['paragraphs']} == expected
        for row in data['paragraphs']:
            tags = {'{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t', '{http://schemas.openxmlformats.org/officeDocument/2006/math}t'}
            assert ''.join(e.text or '' for e in ET.fromstring(row['ooxml']).iter() if e.tag in tags) == row['text']
    paragraphs = {x['paragraph']: x['text'] for x in read(snap)['paragraphs']}
    assert set(paragraphs) == {f'P{i:04d}' for i in range(108, 200)}
    records = {}
    names = {}
    for lane, module in list(MODULES.items())[:2]:
        record = read(AREA / f'{lane}-claims.json')
        assert record['lane'] == lane
        code = strip_lean_comments_and_strings((ROOT / f'Experiments/{module}.lean').read_text(encoding='utf-8'))
        assert not re.search('\\b(sorry|admit|axiom|native_decide)\\b', code) and (not OMEGA_LITERAL_IDENTIFIER.search(code))
        theorem_names = [f'Experiments.{module}.{x}' for x in re.findall('^theorem\\s+(\\w+)', code, re.M)]
        all_names = [f'Experiments.{module}.{x}' for x in re.findall('^(?:noncomputable\\s+)?(?:def|theorem|abbrev)\\s+(\\w+)', code, re.M)]
        claims = record['claims']
        found = [x['declaration'] for x in claims]
        assert set(theorem_names) <= set(found) <= set(all_names) and found and (len(found) == len(set(found))) and (len({c['id'] for c in claims}) == len(claims))
        printed = re.findall('^#print axioms (\\S+)', strip_lean_comments_and_strings((ROOT / f'Experiments/{module}Axioms.lean').read_text(encoding='utf-8')), re.M)
        assert Counter(printed) == Counter(found)
        for c in claims:
            fields = {'id', 'title', 'classification', 'declaration', 'statement', 'source_refs', 'assumptions', 'dependencies', 'countercase', 'authority_ceiling', 'residual', 'reopening'}
            assert fields <= c.keys() and c['classification'] in {'PROVED_FROM_DECLARED_RULES', 'CONSISTENT_REALIZATION', 'ASSUMPTION_BOUND', 'COUNTERMODEL_TO_OVERCLAIM'} and all((c[k] for k in fields - {'assumptions', 'dependencies'}))
            for r in c['source_refs']:
                assert r['source_id'] == manifest['source_id']
                m = re.fullmatch('P(\\d{4})(?:-P(\\d{4}))?', r['paragraphs'])
                assert m
                a, b = (int(m[1]), int(m[2] or m[1]))
                assert 108 <= a <= b <= 192
                text = ' '.join((paragraphs[f'P{i:04d}'] for i in range(a, b + 1)))
                assert ' '.join(r['excerpt'].split()) in ' '.join(text.split()), c['id']
        records[lane] = record
        names[lane] = found
    names['four_sector'] = read(ROOT / 'Audit/bridge-v04-four-sector/results.json')['declarations']
    previous = read(ROOT / 'Audit/bridge-v04-four-sector/claims.json')
    assert names['four_sector'] == [c['declaration'] for c in previous['claims']]
    assert Counter(names['four_sector']) == Counter(re.findall(r'^#print axioms (\S+)', (ROOT / 'Experiments/BridgeFourSectorAxioms.lean').read_text(encoding='utf-8'), re.M))
    return (manifest, records, names)

def inputs():
    base = ['lean-toolchain', 'lake-manifest.json', 'lakefile.lean', 'AGENTS.md', 'docs/REPORTING.md', 'scripts/check_policy.py', 'Audit/BridgeEndpoint.lean', 'Experiments/BridgeFourSector.lean', 'Experiments/BridgeFourSectorAxioms.lean', 'Experiments/BridgeDiagram.lean', 'Experiments/BridgeDiagramAxioms.lean', 'Experiments/BridgeReadout.lean', 'Experiments/BridgeReadoutAxioms.lean', 'Audit/bridge-v04-four-sector/run.py', 'Audit/bridge-v04-four-sector/results.json', 'Audit/recent-work-20260911/results.json', '.github/workflows/bridge-diagram-readout.yml']
    local = ['run.py', 'failure_probes.py', 'RECEIPTS.md', 'README.md', 'SOURCE-CORRESPONDENCE.md', 'input-lock.json', 'source-manifest.json', 'source-context.json', 'diagram-claims.json', 'readout-claims.json', 'DIAGRAM-REVIEW.md', 'READOUT-REVIEW.md', '.gitattributes']
    paths = set(base) | {f'Audit/bridge-v04-diagram-readout/{p}' for p in local}
    for oldarea in ('Audit/bridge-v04-four-sector', 'Audit/recent-work-20260911'):
        paths.update(read(ROOT / oldarea / 'results.json')['input_canonical_lf_sha256'])
        paths.update((rel(p) for p in (ROOT / oldarea).iterdir() if p.is_file()))
    for directory in ('Audit', 'Experiments', 'PALLeanAudit'):
        paths.update((rel(p) for p in (ROOT / directory).rglob('*.lean')))
    paths.update((rel(p) for p in (ROOT / 'scripts').glob('*.py')))
    paths.update((rel(p) for p in (ROOT / '.github/workflows').glob('*.yml')))
    paths.update({'Audit.lean', 'PALLeanAudit.lean', '.gitattributes'})
    return {p: sha(ROOT / p, True) for p in sorted(paths)}

def verify_old():
    lock = read(AREA / 'input-lock.json')
    assert sha(ROOT / 'Audit/bridge-v04-four-sector/results.json') == lock['predecessor_four_sector_results_sha256']
    assert sha(ROOT / 'Audit/recent-work-20260911/results.json') == lock['predecessor_recent_work_results_sha256']
    assert sha(ROOT / 'Audit/bridge-v04-four-sector/run.py') == lock['predecessor_four_sector_runner_sha256']
    assert sha(ROOT / 'Audit/bridge-v04-four-sector/source-manifest.json') == lock['predecessor_source_manifest_sha256']
    for area in ('Audit/bridge-v04-four-sector', 'Audit/recent-work-20260911'):
        old = read(ROOT / area / 'results.json')
        evidence = ROOT / old['evidence_directory']
        for command in old['commands']:
            log = ROOT / command.get('output', evidence / f"{command['label']}.txt")
            assert command['exit_code'] == 0 and log.is_file() and (sha(log) == command['sha256']), f"changed predecessor log: {command['label']}"
        for path, digest in old.get('input_canonical_lf_sha256', {}).items():
            if area == 'Audit/recent-work-20260911' and path == 'Audit.lean':
                data = subprocess.check_output(['git', 'show', 'e00ffc6c506e9801c745856c0090688336e61850:Audit.lean'], cwd=ROOT).replace(b'\r\n', b'\n')
                actual = hashlib.sha256(data).hexdigest()
            else:
                actual = sha(ROOT / path, True)
            assert actual == digest, f'changed predecessor input: {path}'
    spec = importlib.util.spec_from_file_location('previous_publication', ROOT / 'Audit/recent-work-20260911/check_publication.py')
    prior = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prior)
    prior.validate(prior.load(prior.RESULT))
    old = read(ROOT / 'Audit/bridge-v04-four-sector/results.json')
    assert old['status'] == 'PASS_BOUNDED_FOUR_SECTOR' and old['pal_obligations'] == OPEN
    assert read(ROOT / old['evidence_directory'] / 'execution.json') == old
    assert old['axioms'] == parse_axioms(ROOT / old['evidence_directory'] / 'four-sector-axioms.txt', old['declarations'])

def commands(lake, python=None):
    python = python or sys.executable
    out = [('lean-version', [lake, 'env', 'lean', '--version']), ('build-modules', [lake, 'build'] + [f'Experiments.{x}' for x in MODULES.values()])]
    for lane, module in MODULES.items():
        out += [(f'{lane}-axioms', [lake, 'env', 'lean', f'Experiments/{module}Axioms.lean']), (f'{lane}-kernel', [lake, 'env', 'leanchecker', f'Experiments.{module}'])]
    out += [('historical-build', [lake, 'build']), ('policy', [python, 'scripts/check_policy.py']), ('migration', [python, 'scripts/check_release_migration.py']), ('ar3-policy', [python, 'scripts/check_attack_run_0003_policy.py']), ('ar3', [python, 'scripts/check_attack_run_0003.py']), ('report', [python, 'scripts/render_report.py', '--check']), ('migration-report', [python, 'scripts/render_migration_report.py', '--check']), ('ar3-report', [python, 'scripts/render_attack_run_0003.py', '--check']), ('old13-portable', [python, 'Audit/recent-work-20260911/check_publication.py', '--check']), ('diff-check', ['git', 'diff', '--check'])]
    return out

def raw_source(path, manifest):
    assert path.stat().st_size == manifest['bytes'] and sha(path) == manifest['sha256']
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read('word/document.xml'))
    ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    ps = root.findall('.//' + ns + 'p')
    snap = read(ROOT / manifest['source_excerpts'])['paragraphs']
    for row in snap + read(ROOT / manifest['source_context'])['paragraphs']:
        i = int(row['paragraph'][1:])
        actual = ET.tostring(ps[i - 1], encoding='unicode')
        assert actual == row['ooxml']
    return True

def validate(r, manifest, records, names, mode='local', frozen=None):
    assert r['status'] == 'PASS_BRIDGE_DIAGRAM_READOUT' and r['mode'] == mode
    assert r['inputs'] == inputs() == r['input_after'] and r['obligations'] == OPEN and (r['remaining_interface'] == 'FS-M04')
    assert r['source_sha256'] == manifest['sha256'] and r['source_snapshot_verified'] is True
    source = r['source_check']
    assert source == ({'performed': True, 'docx_sha256': manifest['sha256'], 'original_ooxml_paragraphs': 95} if source['performed'] is True else {'performed': False, 'docx_sha256': None, 'original_ooxml_paragraphs': 0})
    assert re.fullmatch('[a-f0-9]{40}', r['tested_checkout_sha'])
    if mode == 'local':
        assert r['ci_status'] == 'NOT_RUN' and r['pr_head_sha'] is None and (r['tested_merge_sha'] is None) and (r['github_run_id'] is None)
    elif r['github_run_id']:
        assert r['ci_status'] == 'GITHUB_ACTIONS_REPLAY' and re.fullmatch('[a-f0-9]{40}', r['pr_head_sha']) and (r['tested_merge_sha'] == r['tested_checkout_sha']) and (r['clean_worktree'] is True)
    else:
        assert r['ci_status'] == 'LOCAL_REPLAY' and r['tested_merge_sha'] is None and (r['pr_head_sha'] is None)
    assert r['clean_worktree'] == (not bool(r['worktree_status'].strip()))
    assert r['declarations'] == names and r['classifications'] == {k: {c['id']: c['classification'] for c in v['claims']} for k, v in records.items()}
    d = ROOT / r['evidence_directory']
    assert len(r['commands']) == len(commands(r['lake'], r['python_executable']))
    for got, (label, argv) in zip(r['commands'], commands(r['lake'], r['python_executable'])):
        assert got['label'] == label and got['argv'] == argv and (got['exit_code'] == 0) and (sha(d / f'{label}.txt') == got['sha256']) and (got['elapsed_seconds'] >= 0)
        assert got['log'] == rel(d / f'{label}.txt')
    for lane in MODULES:
        assert r['axioms'][lane] == parse_axioms(d / f'{lane}-axioms.txt', r['declarations'].get(lane, []))
    assert r['axioms']['four_sector'] == read(ROOT / 'Audit/bridge-v04-four-sector/results.json')['axioms']
    if frozen is not None:
        assert r['axioms'] == frozen['axioms'] and r['declarations'] == frozen['declarations']

def summary(records, receipt):
    lines = ['# BRIDGE diagram and readout bounded audit', '', f"Execution: **{receipt['status']}**.", '', '| Lane | Declarations |', '|---|---:|']
    for lane, record in records.items():
        lines.append(f"| {lane} | {len(record['claims'])} |")
    lines.append(f"| Prerequisite four-sector batch (separate prior evidence) | {len(receipt['declarations']['four_sector'])} |")
    lines += ['', 'The new diagram aggregate certifies six short-exact sequences, including endpoints, and all four commuting squares. The readout equivalence sends [t] to [r(t)] and agrees with the induced residual map. Three checked countercases constrain overclaims. Helpers and aggregates share dependencies; counts are not independent discoveries.', '',
              '[Source correspondence and diagram](SOURCE-CORRESPONDENCE.md) · [Diagram claims](diagram-claims.json) · [Readout claims](readout-claims.json) · [Execution, axioms and hashes](results.json)', '',
              'Selected source scope is P0108-P0192 within the retained P0108-P0199 snapshot. Three additional context paragraphs identify the field and linear-instance hypotheses. The local DOCX check verifies its original bytes and all 95 preserved OOXML paragraphs. CI replays the committed excerpts and Lean declarations without claiming absent DOCX bytes were reread.', '',
              'FS-M01 and FS-M03 are addressed by new bounded evidence; their historical OPEN_MANUAL records are preserved. FS-M04, finite-dimensional/recovery claims, frame morphisms, Hodge/Weil and geometric applications remain outside this batch. PAL obligations remain OPEN. No source adoption or merge is performed.', '',
              f"Receipt guards: {len(receipt['receipt_guards'])} expected rejections, separate from theorem and fixture counts.", '',
              'Reproduce with `python Audit/bridge-v04-diagram-readout/run.py --run --lake <lake> --source-file <BRIDGE_v0.4.docx>`. Verify the saved evidence with `--check`; create a fresh replay with `--replay --output-dir <new-directory>`.', '']
    return '\n'.join(lines)

def guards(r, manifest, records, names, frozen=None):
    validate(r, manifest, records, names, r['mode'], frozen)
    tests = {'missing-command': lambda x: x['commands'].pop(), 'duplicate-command': lambda x: x['commands'].append(copy.deepcopy(x['commands'][0])), 'failed-kernel': lambda x: x['commands'][3].update(exit_code=1), 'altered-log': lambda x: x['commands'][0].update(sha256='0' * 64), 'altered-argv': lambda x: x['commands'][0].update(argv=['bad']), 'altered-input': lambda x: x['inputs'].update({'lean-toolchain': '0' * 64}), 'altered-after-input': lambda x: x['input_after'].update({'lean-toolchain': '0' * 64}), 'altered-axiom': lambda x: x['axioms']['four_sector'].clear(), 'altered-source': lambda x: x.update(source_sha256='0' * 64), 'closed-obligation': lambda x: x['obligations'].update({'O04': 'CLOSED'}), 'closed-out-of-scope-interface': lambda x: x.update(remaining_interface='CLOSED'), 'missing-diagram': lambda x: x['declarations'].pop('diagram'), 'missing-readout': lambda x: x['declarations'].pop('readout'), 'duplicate-declaration': lambda x: x['declarations']['readout'].append(x['declarations']['readout'][0]), 'invented-ci': lambda x: x.update(ci_status='PASS'), 'falsified-docx': lambda x: x['source_check'].update(performed=not x['source_check']['performed'])}
    for label, f in tests.items():
        x = copy.deepcopy(r)
        f(x)
        try:
            validate(x, manifest, records, names, r['mode'], frozen)
        except (AssertionError, KeyError, ValueError):
            continue
        raise AssertionError('guard accepted ' + label)
    return sorted(tests)

def execute(lake, d, receipt, timeout=1200):
    for label, argv in commands(lake, receipt['python_executable']):
        print('Running ' + label, flush=True)
        start = time.monotonic()
        try:
            p = subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', timeout=timeout)
            code, text = (p.returncode, p.stdout)
        except subprocess.TimeoutExpired as e:
            captured = e.stdout or ''
            captured = captured.decode('utf-8', errors='replace') if isinstance(captured, bytes) else captured
            code, text = (124, captured + '\nEXECUTION_TIMEOUT\n')
        except OSError as e:
            code, text = (127, f'EXECUTION_ERROR: {e}\n')
        log = d / f'{label}.txt'
        log.write_text(text.replace('\r\n', '\n'), encoding='utf-8', newline='\n')
        receipt['commands'].append({'label': label, 'argv': argv, 'exit_code': code, 'log': rel(log), 'sha256': sha(log), 'elapsed_seconds': round(time.monotonic() - start, 6)})
        if code:
            raise RuntimeError(f'{label} failed ({code})')

def run(args, replay=False):
    manifest, records, names = inventory()
    verify_old()
    raw = raw_source(args.source_file, manifest) if args.source_file else False
    frozen = check_saved(manifest, records, names) if replay else None
    d = (args.output_dir or AREA / 'evidence' / datetime.now(timezone.utc).strftime('attempt-%Y%m%dT%H%M%S%fZ')).resolve()
    rel(d)
    assert not d.exists()
    d.mkdir(parents=True)
    checkout = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    is_ci = bool(replay and os.getenv('GITHUB_RUN_ID'))
    r = {'schema_version': '1.0', 'status': 'RUNNING', 'mode': 'replay' if replay else 'local', 'lake': args.lake, 'python_executable': sys.executable, 'started_utc': datetime.now(timezone.utc).isoformat(), 'tested_checkout_sha': checkout, 'tested_merge_sha': checkout if is_ci else None, 'pr_head_sha': os.getenv('BRIDGE_DIAGRAM_PR_HEAD_SHA') if is_ci else None, 'github_run_id': os.getenv('GITHUB_RUN_ID') if is_ci else None, 'platform': platform.platform(), 'python': sys.version, 'inputs': inputs(), 'declarations': names, 'classifications': {k: {c['id']: c['classification'] for c in v['claims']} for k, v in records.items()}, 'obligations': OPEN.copy(), 'remaining_interface': 'FS-M04', 'source_sha256': manifest['sha256'], 'source_check': {'performed': raw, 'docx_sha256': manifest['sha256'] if raw else None, 'original_ooxml_paragraphs': 95 if raw else 0}, 'source_snapshot_verified': True, 'evidence_directory': rel(d), 'commands': [], 'axioms': {}, 'ci_status': 'GITHUB_ACTIONS_REPLAY' if is_ci else 'LOCAL_REPLAY' if replay else 'NOT_RUN'}
    try:
        execute(args.lake, d, r)
        for lane in MODULES:
            r['axioms'][lane] = parse_axioms(d / f'{lane}-axioms.txt', names.get(lane, []))
        r['input_after'] = inputs()
        r['worktree_status'] = subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True)
        r['clean_worktree'] = not bool(r['worktree_status'].strip())
        r['status'] = 'PASS_BRIDGE_DIAGRAM_READOUT'
        validate(r, manifest, records, names, r['mode'], frozen)
        r['receipt_guards'] = guards(r, manifest, records, names, frozen)
    except Exception as e:
        r['status'] = 'FAILED_BRIDGE_DIAGRAM_READOUT'
        r['error'] = str(e)
        raise
    finally:
        r['finished_utc'] = datetime.now(timezone.utc).isoformat()
        r.setdefault('input_after', inputs())
        r.setdefault('worktree_status', subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True))
        r.setdefault('clean_worktree', not bool(r['worktree_status'].strip()))
        write(d / 'execution.json', r)
    if not replay:
        write(RESULT, r)
        (AREA / 'SUMMARY.md').write_text(summary(records, r), encoding='utf-8', newline='\n')
    print(r['status'])

def check_saved(manifest, records, names):
    verify_old()
    r = read(RESULT)
    validate(r, manifest, records, names)
    assert r['receipt_guards'] == guards(r, manifest, records, names)
    assert (AREA / 'SUMMARY.md').read_text(encoding='utf-8') == summary(records, r)
    assert read(ROOT / r['evidence_directory'] / 'execution.json') == r
    return r

def main():
    p = argparse.ArgumentParser()
    m = p.add_mutually_exclusive_group(required=True)
    m.add_argument('--run', action='store_true')
    m.add_argument('--check', action='store_true')
    m.add_argument('--replay', action='store_true')
    m.add_argument('--check-inputs', action='store_true')
    p.add_argument('--lake', default='lake')
    p.add_argument('--output-dir', type=Path)
    p.add_argument('--source-file', type=Path)
    a = p.parse_args()
    if a.check or a.check_inputs:
        manifest, records, names = inventory()
        verify_old()
        inputs()
        if a.source_file:
            raw_source(a.source_file, manifest)
        if a.check:
            check_saved(manifest, records, names)
        print('PASS_BRIDGE_RECEIPTS' if a.check else 'PASS_BRIDGE_INPUTS', {k: len(v) for k, v in names.items()})
    else:
        run(a, a.replay)
if __name__ == '__main__':
    main()
