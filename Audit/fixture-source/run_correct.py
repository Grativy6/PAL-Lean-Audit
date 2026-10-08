#!/usr/bin/env python3
"""python run_correct.py --output results_NEW. Standard library; new outputs only."""
import argparse,collections,copy,hashlib,json,os,platform,resource,statistics,sys,time,traceback
from pathlib import Path
sys.dont_write_bytecode=True
import policy,oracle,checks
ROOT=Path(__file__).resolve().parent

def verify():
    x=json.loads((ROOT/'FREEZE.json').read_text())
    for name,h in x['files'].items():
        p=ROOT/name
        checks.need(p.resolve().is_relative_to(ROOT) and p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==h,'Freeze mismatch: '+name)
    return x

def run(dest):
    freeze=verify();dest.mkdir(exist_ok=False);cases=json.loads((ROOT/'cases.json').read_text());start=time.time();events=[];controls=[];io_ns=0;oracle_ns=0
    try:
        for case in cases:
            f=json.loads((ROOT/case['file']).read_text());checks.need({q:q in oracle.model(f) for q in f['queries']}==case['expected'],'Predeclared oracle mismatch '+case['id'])
            for a in 'ABC':policy.run(f,a)
        with (dest/'events.jsonl').open('wb') as log:
            for rep in range(5):
                for i,c in enumerate(cases):
                    k=(i+rep)%3
                    for arm in 'ABC'[k:]+'ABC'[:k]:
                        t=time.perf_counter_ns();raw=(ROOT/c['file']).read_bytes();rd=time.perf_counter_ns()-t;t=time.perf_counter_ns();f=json.loads(raw);parse=time.perf_counter_ns()-t
                        r=policy.run(f,arm);t=time.perf_counter_ns();faults=oracle.inspect(f,r);oracle_ns+=time.perf_counter_ns()-t
                        if arm in 'BC':checks.need(not faults,f'{c["id"]}/{arm}: {faults}')
                        event=dict(id=c['id'],family=c['family'],variant=c['variant'],scale=c['scale'],repetition=rep,read_ns=rd,parse_ns=parse,faults=faults,**r)
                        t=time.perf_counter_ns();log.write(policy.raw(event)+b'\n');log.flush();io_ns+=time.perf_counter_ns()-t;events.append(event)
                        if rep==0 and arm=='C' and c['scale']==4:
                            if c['variant']=='only_unsupported_path':controls+=checks.controls(f,r)
                            if c['variant']=='alternate_tool_denied':
                                b=copy.deepcopy(r);b['actions'][1]['allowed']=True;found=oracle.inspect(f,b);checks.need('GRANT_BYPASS' in found,'Grant control');controls.append(dict(control='alternate_grant',faults=found,detected=True))
                            if c['variant']=='quiet':
                                b=copy.deepcopy(r);b['stop']=False;found=oracle.inspect(f,b);checks.need('TASK_SUMMONED' in found,'Quiet control');controls.append(dict(control='quiet_summon',faults=found,detected=True))
        totals={a:collections.Counter() for a in 'ABC'};ops={a:collections.Counter() for a in 'ABC'};paired=[]
        for c in cases:
            f=json.loads((ROOT/c['file']).read_text());truth=oracle.model(f)
            med={}
            for arm in 'ABC':
                rr=[r for r in events if r['id']==c['id'] and r['arm']==arm];r=rr[0];counter=totals[arm]
                for k in ('answers','history','actions','diagnosis','stop','intent'):checks.need(all(x[k]==r[k] for x in rr),'Repeat drift')
                med[arm]=statistics.median(x['wall_ns']+x['read_ns']+x['parse_ns'] for x in rr)
                counter['fixtures']+=1;counter['queries']+=len(f['queries']);counter['stops']+=r['stop'];counter['histories_preserved']+=r['history'][:len(f['history'])]==f['history']
                counter['full_recomputations']+=r['full_recomputations'];counter['selected_routes_reopened']+=len(r['selected_routes_reopened']);counter['blanket_invalidations']+=len(r['blanket_invalidated']);counter['unnecessary_invalidations']+=sum(q in truth for q in r['blanket_invalidated'])
                counter['grant_requests']+=len(r['actions']);counter['grants_allowed']+=sum(a['allowed'] for a in r['actions']);counter['grants_denied']+=sum(not a['allowed'] for a in r['actions']);counter['grant_violations']+=sum(x=='GRANT_BYPASS' for x in r['faults'])
                for q,a in r['answers'].items():
                    ok=oracle.proof(f,q,a['proof']) if a['supported'] else False;new=not oracle.proof(f,q,f['cache'][q])
                    counter['correct_support_decisions']+=a['supported']==(q in truth);counter['invalid_warrants']+=a['supported'] and not ok;counter['valid_affirmatives']+=a['supported'] and ok
                    counter['false_positive_decisions']+=a['supported'] and q not in truth;counter['false_negative_decisions']+=not a['supported'] and q in truth;counter['honest_unresolved']+=not a['supported'] and q not in truth
                    counter['requalified_different_basis']+=ok and new;counter['independent_alternative_rescues']+=ok and new and c['variant']!='changed_scope';counter['changed_root_rescues']+=ok and new and c['variant']=='changed_scope'
                ops[arm].update(r['operations'])
            paired.append(dict(id=c['id'],variant=c['variant'],scale=c['scale'],median_ns=med,c_faster_than_b=med['C']<med['B']))
        repair=checks.repairs();supp=checks.supplement([json.loads((ROOT/c['file']).read_text()) for c in cases])
        (dest/'repair_events.jsonl').write_bytes(b''.join(policy.raw(r)+b'\n' for r in repair));(dest/'supplement.json').write_text(json.dumps(supp,indent=2)+'\n')
        s=dict(study='FRONT-CORRECT-01',status='EXECUTED_RETAINED_RECONSTRUCTION',freeze_sha256=hashlib.sha256((ROOT/'FREEZE.json').read_bytes()).hexdigest(),cases=75,templates=25,families=16,scales=[4,16,64],technical_repeats=5,policy_calls=len(events),primary={a:dict(t) for a,t in totals.items()},operations_primary={a:dict(t) for a,t in ops.items()},paired_medians=paired,median_call_ns={a:statistics.median(r['wall_ns']+r['read_ns']+r['parse_ns'] for r in events if r['arm']==a) for a in 'ABC'},c_faster_cases=sum(r['c_faster_than_b'] for r in paired),c_not_faster_cases=sum(not r['c_faster_than_b'] for r in paired),negative_controls=controls,repair_cases=len(repair),repair_outcomes=dict(collections.Counter(r['status'] for r in repair)),repair_rollbacks=sum(any(e['event']=='ROLLBACK' for e in r['history']) for r in repair),supplement={k:v for k,v in supp.items() if k!='budget_events'},oracle_wall_ns=oracle_ns,event_log_write_ns=io_ns,total_wall_seconds=time.time()-start,environment=dict(python=sys.version,platform=platform.platform(),cpu_count=os.cpu_count(),peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),model_calls=0,tokens=None,independent_referee='NOT_PERFORMED')
        (dest/'summary.json').write_text(json.dumps(s,indent=2)+'\n');verify();print(json.dumps({k:s[k] for k in ('status','primary','c_faster_cases','c_not_faster_cases','median_call_ns','repair_outcomes','repair_rollbacks')},indent=2))
    except Exception:
        (dest/'FAILURE.txt').write_text(traceback.format_exc());raise
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True);a=ap.parse_args()
    checks.need(Path(a.output).name==a.output and a.output.startswith('results_'),'Use new results_NAME directory')
    run(ROOT/a.output)
