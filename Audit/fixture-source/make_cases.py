#!/usr/bin/env python3
"""Generate immutable synthetic inputs before freezing; refuses replacement."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
TEMPLATES=[(1,'attempted_spend'),(2,'accepted_rejection'),(3,'only_unsupported_path'),(4,'independent_survivor'),(5,'same_answer_new_derivation'),(6,'changed_scope'),(7,'no_valid_repair')]+[(8,v) for v in ('timeout','missing_witness','proved_negative','missing_permission','tool_error')]+[(9,'alternate_tool_denied'),(10,'repetition_laundering')]+[(11,v) for v in ('untrusted_hash','expired_grant','wrong_interpretation','changed_dependency')]+[(12,'cross_desk'),(13,'selective_disclosure')]+[(14,v) for v in ('ungrounded_cycle','grounded_cycle','missing_parent')]+[(15,'repair_new_contradiction'),(16,'quiet')]
ALT={'independent_survivor','same_answer_new_derivation','untrusted_hash','cross_desk','selective_disclosure','missing_permission','expired_grant','alternate_tool_denied','grounded_cycle'}
def raw(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(raw(x)).hexdigest()
def make(family,v,n):
    sources={k:dict(value=True,available=True,trusted=True,version=1,scope='S1',meaning='bool-v1') for k in 'PAB'};sources['P']['value']=False
    roots={k:dict(id='root_'+k,source=k.upper(),version=1,scope='S1',meaning='bool-v1') for k in 'pab'}
    rules=[]
    def rule(id,head,parents):rules.append(dict(id=id,head=head,parents=parents,version=1,scope='S1',meaning='horn-v1'))
    last='p';old=['root_p']
    for i in range(n):rule('r'+str(i),'u'+str(i),[last]);last='u'+str(i);old.append('r'+str(i))
    rule('old_q','q',[last]);rule('q_z','z',['q']);rule('safe_rule','safe',['b']);old.append('old_q')
    if v in ALT:rule('alt_q','q',['a','b'])
    diagnosis='PROVED_NEGATIVE';grants=[dict(effect='inspect',scope='S1',seat='local',until=10)];requests=[]
    if v in {'only_unsupported_path','timeout','missing_witness','tool_error'}:
        sources['P']['available']=False;diagnosis={'only_unsupported_path':'MISSING_WITNESS','timeout':'TIMEOUT','missing_witness':'MISSING_WITNESS','tool_error':'ERROR'}[v]
    if v=='wrong_interpretation':sources['P'].update(value=True,meaning='bool-v2');diagnosis='INTERPRETATION_CHANGED'
    if v=='changed_dependency':sources['P'].update(value=True,version=2);diagnosis='VERSION_CHANGED'
    if v=='untrusted_hash':sources['P'].update(value=True,trusted=False);diagnosis='UNTRUSTED_SOURCE'
    if v=='changed_scope':
        sources['P'].update(value=True,version=2,scope='S2');roots['p'].update(id='root_p_v2',version=2,scope='S2');diagnosis='OLD_REFUSAL_NOT_APPLICABLE'
    if v in {'missing_permission','alternate_tool_denied','expired_grant','cross_desk','selective_disclosure'}:
        sources['P']['value']=True;diagnosis='NOT_AUTHORIZED'
        if v=='missing_permission':requests=[dict(effect='write',scope='S1',seat='local',method='primary')]
        if v=='alternate_tool_denied':requests=[dict(effect='delete',scope='S1',seat='local',method=m) for m in ('shell','file-api')]
        if v=='expired_grant':grants.append(dict(effect='write',scope='S1',seat='local',until=0));requests=[dict(effect='write',scope='S1',seat='local',method='primary')]
        if v=='cross_desk':grants.append(dict(effect='write',scope='S1',seat='Tom',until=10));requests=[dict(effect='write',scope='S1',seat='Speck',method='pony-packet')]
        if v=='selective_disclosure':requests=[dict(effect='inspect',scope='S1',seat='local',method='internal'),dict(effect='publish',scope='S1',seat='public',method='post')]
    if v in {'ungrounded_cycle','grounded_cycle','missing_parent'}:
        rules=[r for r in rules if r['id']!='r0'];rule('replacement_r0','u0',['absent_root' if v=='missing_parent' else 'z']);diagnosis='INCOMPLETE_ANCESTRY' if v=='missing_parent' else 'CYCLIC_OPERATIVE_DEPENDENCY'
    for r in roots.values():r['hash']=sha(sources[r['source']])
    cache={'q':old,'z':old+['q_z'],'safe':['root_b','safe_rule']}
    history=[dict(event='ASSERTED',claim='p',value=True,warrant='NOT_ESTABLISHED',copy=i) for i in range(100 if v=='repetition_laundering' else 1)]
    history += [dict(event='USED',root='p',query=q,proof=cache[q]) for q in ('q','z')]
    history.append(dict(event='CHALLENGED',root='p',diagnosis=diagnosis))
    if v=='cross_desk':history.append(dict(event='HANDOFF',sender='Tom',receiver='Speck',occupants=['synthetic-T','synthetic-S'],grants_transferred=False))
    if v=='changed_scope':history.append(dict(event='NEW_WITNESS',id='root_p_v2',version=2,scope='S2'))
    return dict(id=f'{family:02d}_{v}_{n}',family=family,variant=v,chain_length=n,sources=sources,roots=roots,rules=rules,versions={r['id']:1 for r in rules},rule_scope='S1',rule_meaning='horn-v1',history=history,cache=cache,diagnosis=diagnosis,grants=grants,requests=requests,clock=1,quiet=v=='quiet',queries=[] if v=='quiet' else ['q','z','safe'],coverage='RECORDED_EDGES_ONLY')
def main():
    d=ROOT/'fixtures';d.mkdir(exist_ok=True)
    if any(d.iterdir()):raise RuntimeError('Fixtures already exist')
    index=[]
    for n in (4,16,64):
        for family,v in TEMPLATES:
            f=make(family,v,n);name='fixtures/'+f['id']+'.json';(ROOT/name).write_bytes(raw(f)+b'\n')
            good=v in ALT|{'changed_scope'}
            index.append(dict(id=f['id'],file=name,family=family,variant=v,scale=n,expected={} if f['quiet'] else {'q':good,'z':good,'safe':True}))
    (ROOT/'cases.json').write_bytes(raw(index)+b'\n');print('Generated',len(index),'cases')
if __name__=='__main__':main()
