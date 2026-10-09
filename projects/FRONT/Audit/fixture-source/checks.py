"""Finite conformance suites and failure controls; separate from timed study."""
import collections,copy,itertools,json
import oracle,policy

def need(x,msg):
    if not x:raise RuntimeError(msg)
def valid(s):return s['e']+s['s']+s['holes']<=1 and (s['lock'] is None or s['e']==s['lock'])
def correct(original,e,grant):
    current=copy.deepcopy(original);history=[dict(event='ORIGINAL',state=copy.deepcopy(original))];counts=collections.Counter(detect=1,plan=1)
    history.append(dict(event='PROPOSE',e=e))
    if e==original['e']:counts['revalidate']+=1;status='UNCHANGED_SUPPORTED' if valid(current) else 'NO_VALID_RETURN_FOUND'
    elif not grant:counts['grant']+=1;status='NOT_AUTHORIZED'
    else:
        counts['grant']+=1;counts['apply']+=1;current['e']=e;history.append(dict(event='APPLY_SCRATCH',state=copy.deepcopy(current)))
        counts['revalidate']+=1
        if valid(current):current['version']+=1;status='REVALIDATED_AFTER_CHANGE';history.append(dict(event='COMMIT',state=copy.deepcopy(current)))
        else:
            history.append(dict(event='FAILED_REVALIDATION',state=copy.deepcopy(current)));current=copy.deepcopy(original);history.append(dict(event='ROLLBACK',state=copy.deepcopy(current)));status='NO_VALID_RETURN_FOUND'
    history.append(dict(event='RETURN',status=status));counts['record']=len(history)-1
    return dict(status=status,state=current,history=history,counts=dict(counts))
def row_count(s):
    row=([1,0,1] if s['e'] else [0,1,1])+[1,1]+[0]*s['holes']+[1]+([0,1] if s['s'] else [1])
    selected=[i for i,x in enumerate(row) if x]
    return row[min(selected):max(selected)+1].count(0)
def repairs():
    records=[]
    for e,s,h,lock,g,c in itertools.product((0,1),(0,1),(0,1),(None,0,1),(False,True),(0,1)):
        original=dict(e=e,s=s,holes=h,lock=lock,version=1);trial=dict(original,e=c)
        good=row_count(trial)<=1 and (lock is None or c==lock)
        status=('UNCHANGED_SUPPORTED' if good else 'NO_VALID_RETURN_FOUND') if c==e else ('NOT_AUTHORIZED' if not g else ('REVALIDATED_AFTER_CHANGE' if good else 'NO_VALID_RETURN_FOUND'))
        state=dict(trial,version=2) if status=='REVALIDATED_AFTER_CHANGE' else original
        actual=correct(original,c,g)
        need(actual['state']==state and actual['status']==status,'Repair oracle disagreement')
        need(actual['history'][0]['state']==original,'History erasure')
        records.append(dict(input=original,candidate=c,grant=g,expected=status,**actual))
    return records
class Exhausted(Exception):pass
class Budget(collections.Counter):
    def __init__(self,cap):super().__init__();self.used=0;self.cap=cap
    def __setitem__(self,k,v):
        delta=v-self.get(k,0);priced='bytes' not in k
        if priced and self.used+delta>self.cap:raise Exhausted()
        if priced:self.used+=delta
        super().__setitem__(k,v)
def budget_check(f,cap):
    m=policy.Meter();m.ops=Budget(cap)
    if f['quiet']:return dict(status='STOP',proof=[],used=0)
    try:
        proof=policy.Demand(f,m).check('q')
        return dict(status='SUPPORTED_WITH_BASIS' if proof is not None else 'UNRESOLVED',proof=proof or [],used=m.ops.used)
    except Exhausted:return dict(status='BUDGET_EXHAUSTED_UNRESOLVED',proof=[],used=m.ops.used)
def supplement(fixtures):
    cnt={''.join(map(str,t)):0 for t in itertools.product((0,1),repeat=3)}
    H=[{0,1,2},{3,4},{1,2,4,6}];U=[{0},set(range(5)),set(range(6))]
    for order in itertools.permutations(range(7)):
        p={v:i for i,v in enumerate(order)}
        if not all(max(p[v] for v in h)-min(p[v] for v in h)+1-len(h)<=1 for h in H):continue
        slack=[max(p[v] for v in u)+1-len(u) for u in U]
        for t in itertools.product((0,1),repeat=3):
            if all(s<=v for s,v in zip(slack,t)):cnt[''.join(map(str,t))]+=1
    need(cnt=={'000':0,'001':8,'010':4,'011':28,'100':2,'101':12,'110':14,'111':50},'SCT OR counts')
    pool=[(h,b) for h in ('a','b') for b in ([],['a'],['b'],['a','b'])];queries=0
    for mask in range(256):
        rules=[dict(id=f'r{i}',head=h,parents=b,version=1,scope='S',meaning='H') for i,(h,b) in enumerate(pool) if mask>>i&1]
        for seed in range(4):
            sources={n:dict(value=bool(seed>>i&1),available=True,trusted=True,version=1,scope='S',meaning='B') for i,n in enumerate(('a','b'))}
            roots={n:dict(id='root_'+n,source=n,version=1,scope='S',meaning='B',hash=__import__('hashlib').sha256(policy.raw(s)).hexdigest()) for n,s in sources.items()}
            f=dict(roots=roots,sources=sources,rules=rules,versions={r['id']:1 for r in rules},rule_scope='S',rule_meaning='H')
            sats=[]
            for val in range(4):
                vs={n for i,n in enumerate(('a','b')) if val>>i&1}
                if {n for n,s in sources.items() if s['value']}<=vs and all(not set(r['parents'])<=vs or r['head'] in vs for r in rules):sats.append(vs)
            truth=set.intersection(*sats);need(oracle.model(f)==truth,'Least-model oracle vs truth table')
            for q in ('a','b'):
                proof=policy.Demand(f,policy.Meter()).check(q);need((proof is not None)==(q in truth),'Demand checker vs truth table')
                if proof is not None:need(oracle.proof(f,q,proof),'Demand returned unsupported witness')
                queries+=1
    budgets=[]
    for f in fixtures:
        snapshot=policy.raw(f)
        for b in (0,1,2,4,16,64,512):
            r=budget_check(f,b);need(r['used']<=b and snapshot==policy.raw(f),'Budget or mutation failure')
            if r['status']=='SUPPORTED_WITH_BASIS':need(oracle.proof(f,'q',r['proof']),'Budget admitted partial proof')
            if r['status']=='UNRESOLVED':need('q' not in oracle.model(f),'False complete negative support result')
            budgets.append(dict(id=f['id'],budget=b,**r))
    return dict(status='PASS',or_orders=5040,or_counts=cnt,horn_systems=1024,horn_queries=queries,budget_cases=len(budgets),budget_outcomes=dict(collections.Counter(r['status'] for r in budgets)),budget_events=budgets)
def controls(f,clean):
    trials=[]
    for name,change,expected in [
      ('history_erasure',lambda x:x['history'][0].update(value=False),'HISTORY_ERASED'),
      ('intent_promotion',lambda x:x.update(intent='KNOWING_LIE'),'INTENT_PROMOTION'),
      ('stale_warrant',lambda x:x['answers']['q'].update(supported=True,proof=f['cache']['q']),'BAD_WARRANT:q'),
      ('hash_as_warrant',lambda x:x['answers']['q'].update(supported=True,proof=['hash-is-enough']),'BAD_WARRANT:q'),
      ('coverage_invention',lambda x:x.update(coverage='ALL_WORLD_EFFECTS'),'COVERAGE_PROMOTION'),
      ('type_collapse',lambda x:x.update(diagnosis='SUCCESS'),'NO_COLLAPSE')]:
        bad=copy.deepcopy(clean);change(bad);found=oracle.inspect(f,bad);need(expected in found,'Control escaped: '+name);trials.append(dict(control=name,expected=expected,faults=found,detected=True))
    return trials
