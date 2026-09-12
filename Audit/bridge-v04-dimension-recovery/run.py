"""Receipt runner for the bounded BRIDGE finite-dimension and recovery lanes."""
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
from check_policy import OMEGA_LITERAL_IDENTIFIER, strip_lean_comments_and_strings

MODULES = {'dimension': 'BridgeDimension', 'recovery': 'BridgeRecovery'}
PREDECESSOR = '1babbcd19b51bba46dc9a51365dcadbe31bf1763'
OPEN = {'O04': 'OPEN', 'O25': 'OPEN', 'D-FIRST-OCCURRENCE': 'OPEN'}
ALLOWED = {'Classical.choice', 'Quot.sound', 'propext'}

def read(path): return json.loads(path.read_text(encoding='utf-8'))
def write(path, value): path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
def sha(path, canon=False):
    data = path.read_bytes()
    return hashlib.sha256(data.replace(b'\r\n', b'\n') if canon else data).hexdigest()
def rel(path): return path.resolve().relative_to(ROOT).as_posix()

def parse_axioms(path, expected):
    rows = re.findall(r"'([^']+)' (does not depend on any axioms|depends on axioms: \[(.*?)\])", path.read_text(encoding='utf-8'), re.S)
    found = {}
    for name, form, listed in rows:
        assert name not in found
        found[name] = [] if form.startswith('does not') else sorted(x.strip() for x in listed.replace('\n', ' ').split(',') if x.strip())
        assert set(found[name]) <= ALLOWED
    assert set(found) == set(expected)
    return found

def inventory():
    manifest = read(AREA / 'source-manifest.json')
    assert manifest['predecessor_head'] == PREDECESSOR and manifest['reopened_interfaces'] == ['FS-M04']
    excerpts, context = ROOT / manifest['source_excerpts'], ROOT / manifest['source_context']
    assert sha(excerpts) == manifest['source_excerpts_sha256'] and sha(context) == manifest['source_context_sha256']
    source_rows = {p['paragraph']: p for p in read(excerpts)['paragraphs']}
    assert set(source_rows) == {f'P{i:04d}' for i in range(108, 200)}
    assert len(read(context)['paragraphs']) == 3
    for row in list(source_rows.values()) + read(context)['paragraphs']:
        tags = {'{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t', '{http://schemas.openxmlformats.org/officeDocument/2006/math}t'}
        assert ''.join(x.text or '' for x in ET.fromstring(row['ooxml']).iter() if x.tag in tags) == row['text']
    records, names = {}, {}
    for lane, module in MODULES.items():
        record = read(AREA / f'{lane}-claims.json')
        assert record['lane'] == lane and record['claims']
        code = strip_lean_comments_and_strings((ROOT / f'Experiments/{module}.lean').read_text(encoding='utf-8'))
        assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b', code) and not OMEGA_LITERAL_IDENTIFIER.search(code)
        theorems = [f'Experiments.{module}.{x}' for x in re.findall(r'^theorem\s+(\w+)', code, re.M)]
        declarations = [f'Experiments.{module}.{x}' for x in re.findall(r'^(?:noncomputable\s+)?(?:def|theorem|abbrev)\s+(\w+)', code, re.M)]
        found = [claim['declaration'] for claim in record['claims']]
        assert set(theorems) <= set(found) <= set(declarations) and len(found) == len(set(found))
        printed = re.findall(r'^#print axioms (\S+)', strip_lean_comments_and_strings((ROOT / f'Experiments/{module}Axioms.lean').read_text(encoding='utf-8')), re.M)
        assert Counter(printed) == Counter(found)
        for claim in record['claims']:
            required = {'id','title','classification','declaration','statement','source_refs','assumptions','dependencies','countercase','authority_ceiling','residual','reopening'}
            assert required <= claim.keys() and claim['source_refs'] and claim['classification'] in {'PROVED_FROM_DECLARED_RULES','CONSISTENT_REALIZATION','ASSUMPTION_BOUND','COUNTERMODEL_TO_OVERCLAIM'}
            assert all(claim[key] for key in required - {'assumptions', 'dependencies'})
            assert isinstance(claim['assumptions'], list) and isinstance(claim['dependencies'], list)
            for ref in claim['source_refs']:
                assert ref['source_id'] == manifest['source_id']
                match = re.fullmatch(r'P(\d{4})(?:-P(\d{4}))?', ref['paragraphs']); assert match
                lo, hi = int(match[1]), int(match[2] or match[1]); assert 193 <= lo <= hi <= 199
                text = ' '.join(source_rows[f'P{i:04d}']['text'] for i in range(lo, hi + 1))
                assert ref['excerpt'].strip()
                assert ' '.join(ref['excerpt'].split()) in ' '.join(text.split())
        records[lane], names[lane] = record, found
    assert len({c['id'] for r in records.values() for c in r['claims']}) == sum(len(r['claims']) for r in records.values())
    return manifest, records, names

def inputs():
    prior = set(read(ROOT / 'Audit/bridge-v04-diagram-readout/results.json')['inputs'])
    fixed = {'Experiments/BridgeDimension.lean','Experiments/BridgeDimensionAxioms.lean','Experiments/BridgeRecovery.lean','Experiments/BridgeRecoveryAxioms.lean','Audit/bridge-v04-dimension-recovery/run.py','Audit/bridge-v04-dimension-recovery/failure_probes.py','Audit/bridge-v04-dimension-recovery/replay_bridge_predecessor.py','Audit/bridge-v04-dimension-recovery/input-lock.json','Audit/bridge-v04-dimension-recovery/RECEIPTS.md','Audit/bridge-v04-dimension-recovery/README.md','Audit/bridge-v04-dimension-recovery/SOURCE-CORRESPONDENCE.md','Audit/bridge-v04-dimension-recovery/source-manifest.json','Audit/bridge-v04-dimension-recovery/dimension-claims.json','Audit/bridge-v04-dimension-recovery/recovery-claims.json','Audit/bridge-v04-dimension-recovery/.gitattributes','.github/workflows/bridge-dimension-recovery.yml','.github/workflows/bridge-diagram-readout.yml'}
    fixed.update(read(AREA / 'input-lock.json')['frozen_current_paths'])
    fixed.update(f'Audit/bridge-v04-dimension-recovery/{p}' for p in ('DIMENSION-REVIEW.md', 'RECOVERY-REVIEW.md'))
    return {p: sha(ROOT / p, True) for p in sorted(prior | fixed)}

def predecessor_lock():
    lock = read(AREA / 'input-lock.json')
    assert lock['predecessor_head'] == PREDECESSOR
    for path, digest in lock['frozen_current_paths'].items(): assert sha(ROOT / path, True) == digest
    previous = read(ROOT / 'Audit/bridge-v04-diagram-readout/results.json')
    for path, digest in previous['inputs'].items():
        if path != '.github/workflows/bridge-diagram-readout.yml':
            assert sha(ROOT / path, True) == digest, path
    for prior_area in ('bridge-v04-diagram-readout', 'bridge-v04-four-sector'):
        old = read(ROOT / f'Audit/{prior_area}/results.json')
        assert read(ROOT / old['evidence_directory'] / 'execution.json') == old
        for command in old['commands']:
            log = ROOT / old['evidence_directory'] / (command['label'] + '.txt')
            assert command['exit_code'] == 0 and sha(log) == command['sha256']
    # The historical workflow is immutable as a Git object; later workflow changes are not prior coverage.
    data = subprocess.check_output(['git','show',f'{PREDECESSOR}:.github/workflows/bridge-diagram-readout.yml'], cwd=ROOT)
    assert hashlib.sha256(data.replace(b'\r\n', b'\n')).hexdigest() == lock['historical_workflow_canonical_lf_sha256']
    return lock


def validate_historical(directory):
    wrapper = read(directory / 'execution.json')
    assert wrapper['status'] == 'PASS_HISTORICAL_PR14_REPLAY'
    assert wrapper['mode'] == 'HISTORICAL_REPLAY' and wrapper['historical_checkout'] == PREDECESSOR
    assert [c['label'] for c in wrapper['commands']] == ['historical-check', 'historical-replay']
    for command in wrapper['commands']:
        assert command['exit_code'] == 0 and sha(directory / command['log']) == command['sha256']
    nested_dir = directory / 'historical-replay'
    nested = read(nested_dir / 'execution.json')
    assert sha(nested_dir / 'execution.json') == wrapper['historical_replay_execution_sha256']
    assert nested['status'] == 'PASS_BRIDGE_DIAGRAM_READOUT' and nested['mode'] == 'replay'
    assert nested['tested_checkout_sha'] == PREDECESSOR and nested['ci_status'] == 'LOCAL_REPLAY'
    assert nested['github_run_id'] is None and nested['pr_head_sha'] is None and nested['tested_merge_sha'] is None
    assert nested['clean_worktree'] and not nested['worktree_status'].strip()
    old = read(ROOT / 'Audit/bridge-v04-diagram-readout/results.json')
    assert nested['inputs'] == nested['input_after'] == old['inputs']
    assert nested['axioms'] == old['axioms'] and nested['declarations'] == old['declarations']
    assert nested['receipt_guards'] == old['receipt_guards'] and nested['obligations'] == OPEN
    assert nested['source_check'] == {'performed': False, 'docx_sha256': None, 'original_ooxml_paragraphs': 0}
    spec = importlib.util.spec_from_file_location('historical_bridge_runner', ROOT / 'Audit/bridge-v04-diagram-readout/run.py')
    prior_runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prior_runner)
    expected = prior_runner.commands(nested['lake'], nested['python_executable'])
    assert len(expected) == len(nested['commands']) == 18
    for command, (label, argv) in zip(nested['commands'], expected):
        assert command['label'] == label and command['argv'] == argv and command['exit_code'] == 0
        assert sha(nested_dir / (label + '.txt')) == command['sha256']
    for lane, names in nested['declarations'].items():
        assert parse_axioms(nested_dir / f'{lane}-axioms.txt', names) == nested['axioms'][lane]
    return sha(directory / 'execution.json')

def commands(lake, python, evidence_directory=None):
    out = [('lean-version',[lake,'env','lean','--version']), ('build-modules',[lake,'build'] + [f'Experiments.{x}' for x in MODULES.values()])]
    for lane, module in MODULES.items():
        out += [(f'{lane}-axioms', [lake, 'env', 'lean', f'Experiments/{module}Axioms.lean']),
                (f'{lane}-kernel', [lake, 'env', 'leanchecker', f'Experiments.{module}'])]
    predecessor_output = (Path(evidence_directory) / 'predecessor-replay').as_posix() if evidence_directory else '<evidence>/predecessor-replay'
    out += [('historical-build',[lake,'build']),('policy',[python,'scripts/check_policy.py']),('migration',[python,'scripts/check_release_migration.py']),('ar3-policy',[python,'scripts/check_attack_run_0003_policy.py']),('ar3',[python,'scripts/check_attack_run_0003.py']),('report',[python,'scripts/render_report.py','--check']),('migration-report',[python,'scripts/render_migration_report.py','--check']),('ar3-report',[python,'scripts/render_attack_run_0003.py','--check']),('prior-replay',[python,'Audit/bridge-v04-dimension-recovery/replay_bridge_predecessor.py','--lake',lake,'--output-dir',str(predecessor_output)]),('diff-check',['git','diff','--check'])]
    return out

def raw_source(path, manifest):
    assert path.stat().st_size == manifest['bytes'] and sha(path) == manifest['sha256']
    root = ET.fromstring(zipfile.ZipFile(path).read('word/document.xml')); ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    paragraphs = root.findall('.//' + ns + 'p')
    rows = read(ROOT / manifest['source_excerpts'])['paragraphs'] + read(ROOT / manifest['source_context'])['paragraphs']
    for row in rows: assert ET.tostring(paragraphs[int(row['paragraph'][1:]) - 1], encoding='unicode') == row['ooxml']
    return True

def validate(receipt, manifest, records, names, frozen=None):
    assert receipt['status'] == 'PASS_BRIDGE_DIMENSION_RECOVERY' and receipt['inputs'] == inputs() == receipt['input_after']
    assert receipt['obligations'] == OPEN and receipt['predecessor_head'] == PREDECESSOR and receipt['source_sha256'] == manifest['sha256']
    assert receipt['predecessor_populations'] == {'diagram_readout_new': 19, 'four_sector_prerequisite': 14}
    assert receipt['scope_status'] == 'BOUNDED_LINEAR_REALIZATION_ONLY'
    assert receipt['declarations'] == names and receipt['classifications'] == {k:{c['id']:c['classification'] for c in r['claims']} for k,r in records.items()}
    source = receipt['source_check']; assert source == ({'performed':True,'docx_sha256':manifest['sha256'],'original_ooxml_paragraphs':95} if source['performed'] else {'performed':False,'docx_sha256':None,'original_ooxml_paragraphs':0})
    evidence = ROOT / receipt['evidence_directory']; expected = commands(receipt['lake'], receipt['python_executable'], receipt['evidence_directory'])
    assert len(receipt['commands']) == len(expected)
    for got, (label, argv) in zip(receipt['commands'], expected):
        assert got['label'] == label and got['argv'] == argv and got['exit_code'] == 0 and got['sha256'] == sha(evidence / f'{label}.txt')
        assert got['log'] == receipt['evidence_directory'] + '/' + label + '.txt' and got['elapsed_seconds'] >= 0
    assert receipt['historical_receipt_sha256'] == validate_historical(evidence / 'predecessor-replay')
    for lane in MODULES: assert receipt['axioms'][lane] == parse_axioms(evidence / f'{lane}-axioms.txt', names[lane])
    assert receipt['clean_worktree'] == (not bool(receipt['worktree_status'].strip()))
    assert receipt['mode'] in ('local', 'replay') and re.fullmatch(r'[a-f0-9]{40}', receipt['tested_checkout_sha'])
    if receipt['mode'] == 'local': assert receipt['ci_status'] == 'NOT_RUN' and receipt['pr_head_sha'] is None and receipt['tested_merge_sha'] is None and receipt['github_run_id'] is None
    elif receipt['github_run_id']: assert receipt['ci_status'] == 'GITHUB_ACTIONS_REPLAY' and re.fullmatch(r'[a-f0-9]{40}', receipt['pr_head_sha']) and receipt['tested_merge_sha'] == receipt['tested_checkout_sha'] and receipt['clean_worktree']
    else: assert receipt['ci_status'] == 'LOCAL_REPLAY' and receipt['pr_head_sha'] is None and receipt['tested_merge_sha'] is None
    if frozen is not None: assert receipt['axioms'] == frozen['axioms'] and receipt['declarations'] == frozen['declarations']

def guards(receipt, manifest, records, names, frozen=None):
    validate(receipt, manifest, records, names, frozen)
    tests = {'missing-command':lambda r:r['commands'].pop(),'duplicate-command':lambda r:r['commands'].append(copy.deepcopy(r['commands'][0])),'bad-log':lambda r:r['commands'][0].update(sha256='0'*64),'bad-input':lambda r:r['inputs'].update({'lean-toolchain':'0'*64}),'bad-axiom':lambda r:r['axioms']['dimension'].clear(),'closed-obligation':lambda r:r['obligations'].update({'O04':'CLOSED'}),'wrong-predecessor':lambda r:r.update(predecessor_head='0'*40),'bad-source':lambda r:r.update(source_sha256='0'*64),'invented-ci':lambda r:r.update(ci_status='PASS'),'falsified-docx':lambda r:r['source_check'].update(performed=not r['source_check']['performed'])}
    tests.update({'bad-argv': lambda r: r['commands'][0].update(argv=['wrong']),
                  'failed-kernel': lambda r: r['commands'][3].update(exit_code=1),
                  'bad-after-input': lambda r: r['input_after'].update({'lean-toolchain':'0'*64}),
                  'missing-declaration': lambda r: r['declarations']['recovery'].pop(),
                  'bad-history': lambda r: r.update(historical_receipt_sha256='0'*64),
                  'merged-populations': lambda r: r['predecessor_populations'].update(diagram_readout_new=33),
                  'promoted-scope': lambda r: r.update(scope_status='BRIDGE_PROVED'),
                  'bad-mode': lambda r: r.update(mode='invented')})
    for label, mutate in tests.items():
        bad = copy.deepcopy(receipt); mutate(bad)
        try: validate(bad, manifest, records, names, frozen)
        except (AssertionError, KeyError): continue
        raise AssertionError('guard accepted ' + label)
    return sorted(tests)

def execute(lake, directory, receipt, timeout=1200):
    for label, argv in commands(lake, receipt['python_executable'], rel(directory)):
        print('Running ' + label, flush=True)
        started = time.monotonic()
        try:
            result = subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', timeout=timeout); code, text = result.returncode, result.stdout
        except subprocess.TimeoutExpired as exc:
            text = exc.stdout or ''; text = text.decode('utf-8', errors='replace') if isinstance(text,bytes) else text; code, text = 124, text + '\nEXECUTION_TIMEOUT\n'
        except OSError as exc: code, text = 127, f'EXECUTION_ERROR: {exc}\n'
        log = directory / f'{label}.txt'; log.write_text(text.replace('\r\n','\n'), encoding='utf-8', newline='\n')
        receipt['commands'].append({'label':label,'argv':argv,'exit_code':code,'log':rel(log),'sha256':sha(log),'elapsed_seconds':round(time.monotonic()-started,6)})
        if code: raise RuntimeError(f'{label} failed ({code})')

def run(args, replay=False):
    manifest, records, names = inventory(); predecessor_lock(); raw = raw_source(args.source_file, manifest) if args.source_file else False
    frozen = check_saved() if replay else None
    directory = (args.output_dir or AREA/'evidence'/datetime.now(timezone.utc).strftime('attempt-%Y%m%dT%H%M%S%fZ')).resolve(); assert not directory.exists(); directory.mkdir(parents=True)
    checkout = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(); ci = bool(replay and os.getenv('GITHUB_RUN_ID'))
    receipt = {'schema_version':'1.0','status':'RUNNING','mode':'replay' if replay else 'local','lake':args.lake,'python_executable':sys.executable,'started_utc':datetime.now(timezone.utc).isoformat(),'tested_checkout_sha':checkout,'tested_merge_sha':checkout if ci else None,'pr_head_sha':os.getenv('BRIDGE_RECOVERY_PR_HEAD_SHA') if ci else None,'github_run_id':os.getenv('GITHUB_RUN_ID') if ci else None,'platform':platform.platform(),'python':sys.version,'inputs':inputs(),'declarations':names,'classifications':{k:{c['id']:c['classification'] for c in r['claims']} for k,r in records.items()},'obligations':OPEN.copy(),'predecessor_head':PREDECESSOR,'predecessor_populations':{'diagram_readout_new':19,'four_sector_prerequisite':14},'source_sha256':manifest['sha256'],'source_check':{'performed':raw,'docx_sha256':manifest['sha256'] if raw else None,'original_ooxml_paragraphs':95 if raw else 0},'evidence_directory':rel(directory),'commands':[],'axioms':{},'ci_status':'GITHUB_ACTIONS_REPLAY' if ci else 'LOCAL_REPLAY' if replay else 'NOT_RUN'}
    receipt['scope_status'] = 'BOUNDED_LINEAR_REALIZATION_ONLY'
    try:
        execute(args.lake,directory,receipt)
        receipt['historical_receipt_sha256'] = validate_historical(directory / 'predecessor-replay')
        for lane in MODULES: receipt['axioms'][lane] = parse_axioms(directory/f'{lane}-axioms.txt',names[lane])
        receipt['input_after']=inputs(); receipt['worktree_status']=subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True); receipt['clean_worktree']=not bool(receipt['worktree_status'].strip()); receipt['status']='PASS_BRIDGE_DIMENSION_RECOVERY'; validate(receipt,manifest,records,names,frozen); receipt['receipt_guards']=guards(receipt,manifest,records,names,frozen)
    except Exception as exc: receipt['status']='FAILED_BRIDGE_DIMENSION_RECOVERY'; receipt['error']=str(exc); raise
    finally:
        receipt['finished_utc']=datetime.now(timezone.utc).isoformat(); receipt.setdefault('input_after',inputs()); receipt.setdefault('worktree_status',subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True)); receipt.setdefault('clean_worktree',not bool(receipt['worktree_status'].strip())); write(directory/'execution.json',receipt)
    if not replay:
        write(RESULT,receipt)
        (AREA / 'SUMMARY.md').write_text(summary(receipt), encoding='utf-8', newline='\n')
    print(receipt['status'])

def check_saved():
    manifest, records, names = inventory(); predecessor_lock(); receipt=read(RESULT); validate(receipt,manifest,records,names); assert receipt['receipt_guards']==guards(receipt,manifest,records,names); assert read(ROOT/receipt['evidence_directory']/'execution.json')==receipt
    assert (AREA / 'SUMMARY.md').read_text(encoding='utf-8') == summary(receipt)
    return receipt


def summary(receipt):
    lines = ['# BRIDGE dimension and recovery bounded audit', '', '**' + receipt['status'] + '**', '',
             '| Population | Count |', '|---|---:|']
    for lane, declarations in receipt['declarations'].items():
        lines.append(f'| New {lane} declarations | {len(declarations)} |')
    lines += ['| Prior diagram/readout declarations | 19 |', '| Prior four-sector declarations | 14 |',
              f"| New receipt rejection guards (not theorems) | {len(receipt['receipt_guards'])} |", '',
              'Checked targets: finite-dimensional four-sector accounting; the actual residual readout kernel; linear answer factorization; and full residual identity recovery iff the hidden quotient is zero iff ker(r) is contained in B. The generated-span answer criterion and checked countercases are described in the claim ledgers. Helpers share dependencies and are not independent discoveries.', '',
              f"All {len(receipt['commands'])} controller commands passed, including a pinned historical replay with its own eighteen commands. Axiom inventories and bundled kernel checks are retained. The prior replay checks commit {PREDECESSOR}, separately from the current candidate. Source bytes and 95 original OOXML paragraphs were checked locally; CI verifies committed snapshots without rereading the absent DOCX.", '',
              '[Dimension claims](dimension-claims.json) · [Recovery claims](recovery-claims.json) · [Source correspondence](SOURCE-CORRESPONDENCE.md) · [Execution and hashes](results.json)', '',
              'FS-M04 receives new evidence within the declared linear realization; its historical OPEN_MANUAL record remains intact. PAL obligations O04, O25 and D-FIRST-OCCURRENCE remain OPEN. Geometric/Hodge applications, frame morphisms, source adoption and merge remain outside this batch.', '',
              'Reproduce: python Audit/bridge-v04-dimension-recovery/run.py --run --lake <lake> --source-file <BRIDGE_v0.4.docx>. Check saved evidence with --check; replay into a new directory with --replay --output-dir <directory>.', '']
    return '\n'.join(lines)

def main():
    parser=argparse.ArgumentParser(); mode=parser.add_mutually_exclusive_group(required=True); mode.add_argument('--run',action='store_true'); mode.add_argument('--check',action='store_true'); mode.add_argument('--replay',action='store_true'); mode.add_argument('--check-inputs',action='store_true'); parser.add_argument('--lake',default='lake'); parser.add_argument('--output-dir',type=Path); parser.add_argument('--source-file',type=Path); args=parser.parse_args()
    if args.check or args.check_inputs:
        inventory(); predecessor_lock(); inputs()
        if args.source_file: raw_source(args.source_file,read(AREA/'source-manifest.json'))
        if args.check: check_saved()
        print('PASS_BRIDGE_RECOVERY_RECEIPTS' if args.check else 'PASS_BRIDGE_RECOVERY_INPUTS')
    else: run(args,args.replay)
if __name__ == '__main__': main()
