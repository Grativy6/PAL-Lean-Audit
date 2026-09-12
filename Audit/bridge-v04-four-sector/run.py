"""Bounded BRIDGE v0.4 four-sector execution and receipt verification."""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import argparse
import copy
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time

if not __debug__:
    raise RuntimeError('Validation requires assertions enabled.')
ROOT = Path(__file__).resolve().parents[2]
AREA = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from check_policy import strip_lean_comments_and_strings, OMEGA_LITERAL_IDENTIFIER
from run_pal23_charter import parse_axioms
MODULE = 'Experiments.BridgeFourSector'
RESULT = AREA / 'results.json'
REPORT = AREA / 'SUMMARY.md'
OBLIGATIONS = {'O04': 'OPEN', 'O25': 'OPEN', 'D-FIRST-OCCURRENCE': 'OPEN'}


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def write(p, value):
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')


def sha(p, canonical=False):
    data = p.read_bytes()
    return hashlib.sha256(data.replace(b'\r\n', b'\n') if canonical else data).hexdigest()


def rel(p):
    return p.relative_to(ROOT).as_posix()


def inventory():
    manifest = read(AREA / 'source-manifest.json')
    excerpt = ROOT / manifest['source_excerpts']
    assert sha(excerpt) == manifest['source_excerpts_sha256'], 'Changed source excerpt'
    snapshot = read(excerpt)
    assert snapshot['source_sha256'] == manifest['sha256'] and snapshot['source_id'] == manifest['source_id']
    assert len(snapshot['paragraphs']) == 92
    paragraphs = {p['paragraph']: p['text'] for p in snapshot['paragraphs']}
    assert set(paragraphs) == {f'P{i:04d}' for i in range(108, 200)}
    record = read(AREA / 'claims.json')
    assert record['lane'] == 'bridge-four-sector'
    claims = record['claims']
    assert 8 <= len(claims) <= 15, 'Frozen audited-declaration count'
    names = [c['declaration'] for c in claims]
    assert len(names) == len(set(names)) and len({c['id'] for c in claims}) == len(claims)
    lean = strip_lean_comments_and_strings((ROOT / 'Experiments/BridgeFourSector.lean').read_text(encoding='utf-8'))
    assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b', lean)
    assert not OMEGA_LITERAL_IDENTIFIER.search(lean)
    theorem_names = {MODULE + '.' + n for n in re.findall(r'^theorem\s+(\w+)', lean, re.M)}
    all_declarations = {MODULE + '.' + n for n in re.findall(r'^(?:noncomputable\s+)?(?:def|theorem|abbrev)\s+(\w+)', lean, re.M)}
    assert theorem_names <= set(names) <= all_declarations, 'Theorem inventory mismatch'
    prints = re.findall(r'^#print axioms (\S+)', (ROOT / 'Experiments/BridgeFourSectorAxioms.lean').read_text(encoding='utf-8'), re.M)
    assert Counter(prints) == Counter(names), 'Axiom directive mismatch'
    fields = {'id','title','classification','declaration','statement','source_refs','assumptions','dependencies','countercase','authority_ceiling','residual','reopening'}
    for c in claims:
        assert fields <= c.keys()
        assert c['classification'] in {'PROVED_FROM_DECLARED_RULES','CONSISTENT_REALIZATION','ASSUMPTION_BOUND','COUNTERMODEL_TO_OVERCLAIM'}
        assert all(c[f] for f in fields - {'assumptions','dependencies'})
        for reference in c['source_refs']:
            assert reference['source_id'] == manifest['source_id']
            match = re.fullmatch(r'P(\d{4})(?:-P(\d{4}))?', reference['paragraphs'])
            assert match
            first, last = int(match[1]), int(match[2] or match[1])
            assert 108 <= first <= last <= 199
            text = ' '.join(paragraphs[f'P{i:04d}'] for i in range(first,last+1))
            assert ' '.join(reference['excerpt'].split()) in ' '.join(text.split()), c['id']
    assert isinstance(record['manual_dispositions'], list)
    return record, names


def inputs():
    paths = [ROOT / p for p in ('lean-toolchain','lake-manifest.json','lakefile.lean','AGENTS.md','docs/REPORTING.md','Audit/BridgeEndpoint.lean','Experiments/BridgeFourSector.lean','Experiments/BridgeFourSectorAxioms.lean','scripts/check_policy.py','scripts/run_pal23_charter.py')]
    paths += [AREA / n for n in ('run.py','claims.json','SOURCE-REVIEW.md','source-manifest.json','source-excerpts.json','.gitattributes')]
    return {rel(p):sha(p, True) for p in paths}


def commands(lake):
    return [
        ('lean-version', [lake,'env','lean','--version']),
        ('build-four-sector', [lake,'build',MODULE]),
        ('four-sector-axioms', [lake,'env','lean','Experiments/BridgeFourSectorAxioms.lean']),
        ('four-sector-kernel', [lake,'env','leanchecker',MODULE]),
        ('historical-build', [lake,'build']),
        ('historical-policy', [sys.executable,'scripts/check_policy.py']),
        ('historical-report', [sys.executable,'scripts/render_report.py','--check']),
        ('historical-migration', [sys.executable,'scripts/check_release_migration.py']),
        ('historical-ar3', [sys.executable,'scripts/check_attack_run_0003.py']),
        ('historical-ar3-report', [sys.executable,'scripts/render_attack_run_0003.py','--check']),
        ('diff-check', ['git','diff','--check'])]


def validate(result, record, names):
    assert result['status'] == 'PASS_BOUNDED_FOUR_SECTOR'
    assert result['input_canonical_lf_sha256'] == inputs()
    assert result['declarations'] == names
    assert result['classifications'] == {c['id']: c['classification'] for c in record['claims']}
    assert result['source_sha256'] == read(AREA / 'source-manifest.json')['sha256']
    assert result['pal_obligations'] == OBLIGATIONS
    assert result['authority_ceiling'] == 'Bounded formal evidence only; no source adoption or Hodge result.'
    assert result['ci_status'] == 'NOT_RUN' and result['publication_status'] == 'LOCAL_ONLY'
    expected = commands(result['lake'])
    assert len(expected) == len(result['commands'])
    directory = ROOT / result['evidence_directory']
    for command,(label,argv) in zip(result['commands'],expected):
        assert command['label'] == label and command['argv'] == argv and command['exit_code'] == 0
        log = directory / f'{label}.txt'
        assert command['output'] == rel(log) and command['sha256'] == sha(log)
        assert command['elapsed_seconds'] >= 0
    assert result['axioms'] == parse_axioms(directory / 'four-sector-axioms.txt', names)


def guards(result, record, names):
    mutations = {
        'missing-command':lambda r:r['commands'].pop(),
        'failed-kernel':lambda r:r['commands'][3].update(exit_code=1),
        'changed-log':lambda r:r['commands'][0].update(sha256='0'*64),
        'changed-source':lambda r:r.update(source_sha256='0'*64),
        'missing-axiom-inventory':lambda r:r['axioms'].pop(next(iter(r['axioms']))),
        'closed-obligation':lambda r:r['pal_obligations'].update(O04='CLOSED'),
        'invented-ci':lambda r:r.update(ci_status='PASS'),
        'missing-declaration':lambda r:r['declarations'].pop()}
    for label, change in mutations.items():
        altered = copy.deepcopy(result)
        change(altered)
        try:
            validate(altered,record,names)
        except (AssertionError,KeyError,ValueError):
            continue
        raise AssertionError('Failed rejection guard: '+label)
    return list(mutations)


def report(record,result):
    lines = ['# BRIDGE v0.4 four-sector audit','',f'Execution: **{result["status"]}**. Audited declarations: {len(record["claims"])}.','',
        'Source: the supplied BRIDGE v0.4 manuscript, Four Sector Endpoint Theorem, OOXML paragraphs P0108-P0199. The preserved source excerpt contains the original mathematical XML as well as readable paragraph text.','',
        'The earlier v0.2 four-sector dimension identity remains prior evidence. This batch checks the declarations listed below; broader diagram coverage is described in SOURCE-REVIEW.md.','',
        '| ID | Checked content | Classification |','|---|---|---|']
    for c in record['claims']:
        lines.append(f'| {c["id"]} | {c["title"]} | {c["classification"]} |')
    lines += ['','## Boundaries and evidence','',
        '- [Exact claims, hypotheses and source mappings](claims.json).',
        '- [Source correspondence and diagram coverage](SOURCE-REVIEW.md).',
        '- [Execution, dependencies and log hashes](results.json).',
        '- [Source identity](source-manifest.json).',
        '- Formal statements have only their recorded scope. No Hodge or Weil result, geometric application, canon adoption, or PAL obligation closure is claimed.',
        '- Local Windows execution; CI and publication for this new batch are not claimed.',
        '- Counts are declarations and may share dependencies. The v0.2 dimension result is not an independent new discovery.','',
        'Manual dispositions:', '']
    for item in record['manual_dispositions']:
        lines.append('- '+(item if isinstance(item,str) else ' '.join(f'{k}: {v}' for k,v in item.items())))
    lines += ['', 'Reproduce with `python Audit/bridge-v04-four-sector/run.py --run --lake <lake>`. Add `--source-file <BRIDGE_v0.4.docx>` to reread original source bytes. Verify the saved bundle with `--check`.','']
    return '\n'.join(lines)


def run(args):
    record,names = inventory()
    manifest = read(AREA/'source-manifest.json')
    source_checked = False
    if args.source_file:
        assert args.source_file.stat().st_size == manifest['bytes'] and sha(args.source_file) == manifest['sha256']
        source_checked = True
    directory = AREA/'evidence'/datetime.now(timezone.utc).strftime('attempt-%Y%m%dT%H%M%S%fZ')
    directory.mkdir(parents=True)
    git = lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
    result = dict(schema_version='1.0',status='RUNNING',started_utc=datetime.now(timezone.utc).isoformat(),
        platform=platform.platform(),python=sys.version,lake=args.lake,git_checkout_sha=git('rev-parse','HEAD'),git_branch=git('branch','--show-current'),
        worktree_status=git('status','--short'),pr_head_sha=None,tested_merge_sha=None,
        ci_status='NOT_RUN',publication_status='LOCAL_ONLY',source_sha256=manifest['sha256'],source_docx_bytes_verified=source_checked,
        source_excerpt_verified=True,pal_obligations=OBLIGATIONS.copy(),authority_ceiling='Bounded formal evidence only; no source adoption or Hodge result.',
        input_canonical_lf_sha256=inputs(),declarations=names,classifications={c['id']:c['classification'] for c in record['claims']},
        commands=[],axioms={},evidence_directory=rel(directory))
    try:
        for label,argv in commands(args.lake):
            print('Running '+label,flush=True)
            start=time.monotonic()
            process=subprocess.run(argv,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf-8',errors='replace',timeout=1200)
            log=directory/f'{label}.txt'
            log.write_text(process.stdout.replace('\r\n','\n'),encoding='utf-8',newline='\n')
            result['commands'].append(dict(label=label,argv=argv,exit_code=process.returncode,output=rel(log),sha256=sha(log),elapsed_seconds=round(time.monotonic()-start,6)))
            if process.returncode:
                raise RuntimeError(label+' failed: '+process.stdout[-5000:])
            print(label+': PASS',flush=True)
        result['axioms']=parse_axioms(directory/'four-sector-axioms.txt',names)
        result['status']='PASS_BOUNDED_FOUR_SECTOR'
        validate(result,record,names)
        result['receipt_guards']=guards(result,record,names)
    except Exception as error:
        result['status']='FAILED_LOCAL_CHECK'
        result['error']=str(error)
        raise
    finally:
        result['finished_utc']=datetime.now(timezone.utc).isoformat()
        write(directory/'execution.json',result)
        write(RESULT,result)
    REPORT.write_text(report(record,result),encoding='utf-8',newline='\n')
    print('PASS_BOUNDED_FOUR_SECTOR')


def main():
    p=argparse.ArgumentParser()
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument('--run',action='store_true')
    mode.add_argument('--check',action='store_true')
    p.add_argument('--lake',default=shutil.which('lake') or str(Path.home()/'.elan/bin/lake.exe'))
    p.add_argument('--source-file',type=Path)
    args=p.parse_args()
    if args.run:
        run(args)
    else:
        record,names=inventory()
        result=read(RESULT)
        validate(result,record,names)
        assert result['receipt_guards']==guards(result,record,names)
        assert REPORT.read_text(encoding='utf-8')==report(record,result)
        assert read(ROOT/result['evidence_directory']/'execution.json')==result
        if args.source_file:
            assert sha(args.source_file)==result['source_sha256']
        print('PASS_FOUR_SECTOR_RECEIPTS')


if __name__=='__main__':
    main()
