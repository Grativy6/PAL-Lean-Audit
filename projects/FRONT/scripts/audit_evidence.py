"""Data-only reaggregation. Does not import/execute any supplied study program.

This is a same-session audit, not an independent referee or a Python/Lean equivalence proof.
"""
from pathlib import Path
from collections import Counter, defaultdict, deque
from statistics import median
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / 'Sources/v1.0/extracted/FRONT_v1.0_Working_Draft'
OUT = ROOT / 'Audit/receipts'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def need(condition, label):
    if not condition:
        raise RuntimeError(label)


def lines(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]


def basis(f):
    """Finite fixture meaning; the truth/authority fields remain supplied assumptions."""
    roots = {}
    for atom, receipt in f['roots'].items():
        source = f['sources'].get(receipt['source'])
        raw = json.dumps(source, sort_keys=True, separators=(',', ':')).encode()
        if (source and all(source.get(k) is True for k in ('trusted', 'value', 'available'))
                and all(source.get(k) == receipt[k] for k in ('version', 'scope', 'meaning'))
                and hashlib.sha256(raw).hexdigest() == receipt['hash']):
            roots[receipt['id']] = atom
    rules = {r['id']: r for r in f['rules'] if
             r['version'] == f['versions'].get(r['id']) and
             (r['scope'], r['meaning']) == (f['rule_scope'], f['rule_meaning'])}
    return roots, rules


def closure(roots, rules):
    """Agenda implementation distinct from the supplied rescanning oracle/DFS checker."""
    known = set(roots.values())
    waiting = {rid: set(rule['parents']) - known for rid, rule in rules.items()}
    agenda = deque(rid for rid, parents in waiting.items() if not parents)
    reverse = defaultdict(list)
    for rid, parents in waiting.items():
        for parent in parents:
            reverse[parent].append(rid)
    while agenda:
        rid = agenda.popleft()
        head = rules[rid]['head']
        if head in known:
            continue
        known.add(head)
        for child in reverse[head]:
            waiting[child].discard(head)
            if not waiting[child]:
                agenda.append(child)
    return known


def warrant(roots, rules, query, ids):
    chosen = set(ids)
    return bool(ids) and chosen <= roots.keys() | rules.keys() and query in closure(
        {rid: atom for rid, atom in roots.items() if rid in chosen},
        {rid: rule for rid, rule in rules.items() if rid in chosen})


def correction(directory):
    events = lines(directory / 'events.jsonl')
    repairs = lines(directory / 'repair_events.jsonl')
    saved = load(directory / 'summary.json')
    cases = load(ROOT / 'Audit/fixture-source/cases.json')
    by_case = {c['id']: c for c in cases}
    groups = defaultdict(list)
    for event in events:
        groups[event['id'], event['arm']].append(event)
    need(len(events) == 1125 and len(groups) == 225, 'Correction event dimensions')
    totals = {arm: Counter() for arm in 'ABC'}
    ops = {arm: Counter() for arm in 'ABC'}
    paired = []
    substantive = {}
    for cid, case in by_case.items():
        f = load(ROOT / 'Audit/fixture-source' / case['file'])
        roots, rules = basis(f)
        truth = closure(roots, rules)
        need({q: q in truth for q in f['queries']} == case['expected'], 'Predeclared truth '+cid)
        med = {}
        for arm in 'ABC':
            group = sorted(groups[cid, arm], key=lambda e: e['repetition'])
            need([e['repetition'] for e in group] == list(range(5)), 'Missing/duplicate repeats')
            event = group[0]
            stable = ('answers','history','actions','diagnosis','stop','intent','coverage',
                      'selected_routes_reopened','blanket_invalidated','full_recomputations','operations')
            need(all(all(e[k] == event[k] for k in stable) for e in group), 'Outcome drift')
            substantive[cid+'/'+arm] = {k:event[k] for k in stable}
            med[arm] = median(e['wall_ns']+e['read_ns']+e['parse_ns'] for e in group)
            need(all(sum(e['phase_ns'].values()) == e['wall_ns'] for e in group), 'Timing partition')
            counter = totals[arm]
            counter.update(fixtures=1, queries=len(f['queries']), stops=int(event['stop']),
                           histories_preserved=int(event['history'][:len(f['history'])] == f['history']),
                           full_recomputations=event['full_recomputations'],
                           selected_routes_reopened=len(event['selected_routes_reopened']),
                           blanket_invalidations=len(event['blanket_invalidated']),
                           unnecessary_invalidations=sum(q in truth for q in event['blanket_invalidated']))
            counter['grant_requests'] += len(event['actions'])
            for action in event['actions']:
                request = action['request']
                allowed = any(all(g[k] == request[k] for k in ('effect','scope','seat')) and
                              f['clock'] <= g['until'] for g in f['grants'])
                counter['grants_allowed'] += bool(action['allowed'])
                counter['grants_denied'] += not action['allowed']
                counter['grant_violations'] += action['allowed'] != allowed or action['executed']
            for query, answer in event['answers'].items():
                current = warrant(roots, rules, query, answer['proof']) if answer['supported'] else False
                old_invalid = not warrant(roots, rules, query, f['cache'][query])
                counter['correct_support_decisions'] += answer['supported'] == (query in truth)
                counter['invalid_warrants'] += answer['supported'] and not current
                counter['valid_affirmatives'] += answer['supported'] and current
                counter['false_positive_decisions'] += answer['supported'] and query not in truth
                counter['false_negative_decisions'] += not answer['supported'] and query in truth
                counter['honest_unresolved'] += not answer['supported'] and query not in truth
                counter['requalified_different_basis'] += current and old_invalid
                counter['independent_alternative_rescues'] += current and old_invalid and case['variant'] != 'changed_scope'
                counter['changed_root_rescues'] += current and old_invalid and case['variant'] == 'changed_scope'
            ops[arm].update(event['operations'])
        paired.append({'id':cid,'variant':case['variant'],'scale':case['scale'],'median_ns':med,
                       'c_faster_than_b':med['C'] < med['B']})
    for arm in 'ABC':
        need(dict(totals[arm]) == saved['primary'][arm], 'Summary primary mismatch '+arm)
        need(dict(ops[arm]) == saved['operations_primary'][arm], 'Summary operations mismatch '+arm)
    need(paired == saved['paired_medians'], 'Timing medians mismatch')
    outcomes = dict(Counter(event['status'] for event in repairs))
    rollbacks = sum(any(e['event']=='ROLLBACK' for e in event['history']) for event in repairs)
    need(len(repairs)==96 and outcomes==saved['repair_outcomes'] and rollbacks==saved['repair_rollbacks'], 'Repair aggregation')
    need(all(event['history'][0]['state']==event['input'] for event in repairs), 'Original state lost')
    for event in repairs:
        if event['status']=='REVALIDATED_AFTER_CHANGE':
            need(event['grant'] and sum(event['state'][k] for k in ('e','s','holes'))<=1
                 and (event['state']['lock'] is None or event['state']['e']==event['state']['lock']), 'Bad commit')
        else:
            need(event['state']==event['input'], 'Noncommit changed state')
    return {'study':'FRONT-CORRECT-01','result_directory':str(directory),
            'hashes':{p.name:digest(p) for p in directory.glob('*') if p.is_file()},
            'recomputed':True,'primary':{a:dict(t) for a,t in totals.items()},
            'faster':sum(p['c_faster_than_b'] for p in paired),
            'not_faster':sum(not p['c_faster_than_b'] for p in paired),
            'repair_outcomes':outcomes,'rollbacks':rollbacks,
            'supplement':saved['supplement'],'negative_controls':saved['negative_controls']}, substantive


def legacy():
    directory = SOURCE / 'experiment_reuse_v0.4/results_run_01'
    events = lines(directory / 'events.jsonl')
    summary = load(directory / 'summary.json')
    ledger = {e['id']:e for e in load(SOURCE / 'experiment_reuse_v0.4/validity_ledger.json')}
    result = {}
    for arm in 'ABC':
        selected = [e for e in events if e['arm']==arm and e['rep']==0 and e['turn']=='repeat']
        counts = dict(first_pass_repeat_queries=len(selected),
                      correct_repeat=sum(e['answer']==ledger[e['id']]['current_answer'] for e in selected),
                      cache_reuses=sum(e['cache_reused'] for e in selected),
                      false_reuses=sum(e['cache_reused'] and not ledger[e['id']]['old_answer_valid_for_current_query'] for e in selected),
                      support_available_repeat=sum(e['support_available'] for e in selected))
        for k,v in counts.items(): need(summary['arms'][arm][k]==v, 'Legacy count mismatch '+arm+'/'+k)
        result[arm]=counts
    return {'study':'FRONT-REUSE-01','status':'SAVED_EVENT_REAGGREGATION_NOT_FRESH_REPLAY',
            'event_count':len(events),'arms':result,
            'truth_reference':'Predeclared validity ledger; no fresh legacy solver run.',
            'policy_identity':'A fresh recomputation; B blind cache; C checked reuse. These letters do not name the correction policies.',
            'hashes':{p.name:digest(p) for p in directory.glob('*') if p.is_file()}}


def native_equations():
    docx=SOURCE / 'FRONT_v1.0_WORKING_DRAFT.docx'
    ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'm':'http://schemas.openxmlformats.org/officeDocument/2006/math'}
    with zipfile.ZipFile(docx) as archive:
        xml=archive.read('word/document.xml')
    root=ET.fromstring(xml)
    texts=[]
    for idx,p in enumerate(root.findall('.//w:p',ns)):
        text=''.join(n.text or '' for n in p.iter() if n.tag in (f"{{{ns['w']}}}t",f"{{{ns['m']}}}t"))
        # Native conversion omits equation tags. Retain the entire pertinent sections,
        # including actual equation paragraphs, rather than searching tags alone.
        if (260 <= idx <= 385 or 1040 <= idx <= 1090) and p.findall('.//m:oMath',ns):
            texts.append({'paragraph_index':idx,'linearized_text':text,
                          'math_xml':[ET.tostring(m,encoding='unicode') for m in p.findall('.//m:oMath',ns)]})
    return {'docx_sha256':digest(docx),'document_xml_sha256':hashlib.sha256(xml).hexdigest(),
            'native_math_count':len(root.findall('.//m:oMath',ns)),
            'note':'Selected native equations retain structural OMML; linear text alone does not represent subscripts or fractions.',
            'selected_paragraphs':texts}


def main():
    OUT.mkdir(exist_ok=True)
    runs={}; substantive={}
    locations={
        'supplied_primary':SOURCE / 'experiment_correct/results_retained_01',
        'supplied_optimized':SOURCE / 'experiment_correct/results_retained_optimized',
        'fresh_windows_normal':ROOT / 'Audit/runs/correction-normal/results',
        'fresh_windows_optimized':ROOT / 'Audit/runs/correction-optimized/results'}
    for key,path in locations.items():
        runs[key],substantive[key]=correction(path)
    first=substantive['supplied_primary']
    need(all(s==first for s in substantive.values()), 'Substantive cross-run disagreement')
    report={'status':'PASS','review_status':'SAME_SESSION_SELF_REVIEW',
            'all_four_runs_same_substantive_results':True,'correction':runs,'legacy':legacy(),
            'completion_message_55_20':'No matching source run located; do not substitute for supplied 67/8 or 63/12.',
            'limits':['No general Python-to-Lean refinement theorem','No external trust or authority authentication',
                      'Shared-machine timing observations are descriptive, not a superiority benchmark']}
    (OUT/'experiment-reconciliation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    native=native_equations()
    (OUT/'native-equations.json').write_text(json.dumps(native,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'timings':{k:[v['faster'],v['not_faster']] for k,v in runs.items()},
                      'legacy':report['legacy']['arms'],'native_equations':len(native['selected_paragraphs'])},indent=2))


if __name__=='__main__': main()
