"""Finite support policies. Pure fixture data; no shell, network or live writes."""
from collections import Counter,defaultdict,deque
import copy,hashlib,json,time

def raw(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
class Meter:
    def __init__(self):self.ops=Counter();self.ns=Counter()
    def call(self,phase,fn,*args):
        start=time.perf_counter_ns()
        try:return fn(*args)
        finally:self.ns[phase]+=time.perf_counter_ns()-start

def root(f,n,m):
    m.ops['root_checks']+=1;r=f['roots'][n];s=f['sources'].get(r['source'])
    if not s or not s['available']:return False
    m.ops['basis_checks']+=3
    if any(s[k]!=r[k] for k in ('version','scope','meaning')):return False
    b=raw(s);m.ops['hash_bytes']+=len(b)
    return hashlib.sha256(b).hexdigest()==r['hash'] and s['trusted'] and s['value'] is True

def rule(f,r,m):
    m.ops['rule_checks']+=1
    return r['version']==f['versions'].get(r['id']) and r['scope']==f['rule_scope'] and r['meaning']==f['rule_meaning']

def affected(f,m):
    rev=defaultdict(list)
    for r in f['rules']:
        for n in r['parents']:rev[n].append(r['head']);m.ops['index_edges']+=1
    S={'p'};todo=deque(S)
    while todo:
        for q in rev[todo.popleft()]:
            m.ops['edge_visits']+=1
            if q not in S:S.add(q);todo.append(q)
    # Historical dependencies matter after the CURRENT graph removed a link.
    for h in f['history']:
        m.ops['history_use_checks']+=1
        if h['event']=='USED' and h['root']=='p':S.add(h['query'])
    return S

def recompute(f,m):
    S={n:[r['id']] for n,r in f['roots'].items() if root(f,n,m)}
    while True:
        m.ops['closure_passes']+=1;changed=False
        for r in reversed(f['rules']):
            ok=rule(f,r,m);m.ops['premise_checks']+=len(r['parents'])
            if ok and r['head'] not in S and all(n in S for n in r['parents']):
                S[r['head']]=sorted(set([r['id']]+[v for n in r['parents'] for v in S[n]]));changed=True;m.ops['derived_nodes']+=1
        if not changed:return S

class Demand:
    def __init__(self,f,m):
        self.f=f;self.m=m;self.byhead=defaultdict(list);self.memo={}
        for r in f['rules']:self.byhead[r['head']].append(r);m.ops['support_index']+=1
    def check(self,q,stack=frozenset()):
        m=self.m;f=self.f;m.ops['node_visits']+=1
        if q in self.memo:return self.memo[q]
        if q in stack:m.ops['cycle_rejections']+=1;return None
        if q in f['roots'] and root(f,q,m):
            self.memo[q]=[f['roots'][q]['id']];return self.memo[q]
        for r in self.byhead[q]:
            if not rule(f,r,m):continue
            proof=[r['id']];good=True
            for n in r['parents']:
                m.ops['premise_checks']+=1;a=self.check(n,stack|{q})
                if a is None:good=False;break
                proof.extend(a)
            if good:self.memo[q]=sorted(set(proof));return self.memo[q]
        # Failed cyclic branches are not cached as globally false.
        return None

def check_grant(f,r,m):
    m.ops['grant_requests']+=1
    for g in f['grants']:
        m.ops['grant_checks']+=1
        if (g['effect'],g['scope'],g['seat'])==(r['effect'],r['scope'],r['seat']) and f['clock']<=g['until']:return True
    return False

def run(f,arm):
    if arm not in ('A','B','C'):raise ValueError(arm)
    start=time.perf_counter_ns();cpu=time.process_time_ns();m=Meter()
    history=m.call('trace',copy.deepcopy,f['history']);m.ops['history_input_bytes']=len(raw(history))
    history.append(dict(event='DETECTED',diagnosis=f['diagnosis']))
    history.append(dict(event='BOUND',root='p',scope=f['roots']['p']['scope'],intent='NOT_ESTABLISHED'))
    ans={};reopened=[];invalidated=[];full=0
    if not f['quiet']:
        impacted=m.call('locate',affected,f,m) if arm!='A' else set()
        reopened=[q for q in f['cache'] if q in impacted]
        if arm=='B':invalidated=list(reopened)
        if reopened:history.append(dict(event='SELECTED_SUPPORT_REOPENED',queries=reopened))
        demand=m.call('alternative_check',Demand,f,m) if arm=='C' else None
        for q in f['queries']:
            if arm=='A' or (arm=='B' and q not in impacted):p=f['cache'][q];route='unchecked_cache' if arm=='A' else 'unchanged_route'
            elif arm=='B':p=m.call('derive',recompute,f,m).get(q);full+=1;route='recomputed'
            else:p=m.call('alternative_check',demand.check,q);route='recorded_witness'
            ans[q]=dict(supported=p is not None,proof=p or [],route=route if p is not None else 'UNRESOLVED')
            history.append(dict(event='QUERY_RESULT',query=q,**ans[q]))
    else:history.append(dict(event='STOP',reason='TASK_COMPLETE'))
    actions=[dict(request=r,allowed=m.call('grant',check_grant,f,r,m),executed=False) for r in f['requests']]
    history.extend(dict(event='GRANT_CHECK',**a) for a in actions)
    unresolved=[q for q,a in ans.items() if not a['supported']]
    if unresolved:history.append(dict(event='CARRIED_UNRESOLVED',queries=unresolved,meaning='NO_RECORDED_ROUTE_NOT_NEGATION'))
    m.ops['history_output_bytes']=len(m.call('record',raw,history));m.ops['witness_bytes']=sum(len(raw(a['proof'])) for a in ans.values())
    out=dict(arm=arm,answers=ans,selected_routes_reopened=reopened,blanket_invalidated=invalidated,full_recomputations=full,history=history,actions=actions,unresolved=unresolved,stop=f['quiet'],intent='NOT_ESTABLISHED',diagnosis=f['diagnosis'],coverage=f['coverage'],operations=dict(m.ops),phase_ns=dict(m.ns),model_calls=None,input_tokens=None,output_tokens=None)
    out['cpu_ns']=time.process_time_ns()-cpu;out['wall_ns']=time.perf_counter_ns()-start;out['phase_ns']['other']=out['wall_ns']-sum(m.ns.values())
    if out['phase_ns']['other']<0:raise RuntimeError('Invalid timing partition')
    return out
