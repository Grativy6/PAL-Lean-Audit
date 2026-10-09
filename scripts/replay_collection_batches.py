"""Replay preserved batches from a clone without following historical absolute paths.

Historical records are immutable. This adapter produces a separate receipt;
source-document bytes are a separately reported local verification scope.
"""
from pathlib import Path
import argparse, copy, datetime, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, time

ROOT=Path(__file__).resolve().parents[1]
AREA=ROOT/'provenance/migrations/2026-10-09'
ALLOWED={'propext','Quot.sound','Classical.choice'}

def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def load(name,rel):
    spec=importlib.util.spec_from_file_location(name,ROOT/rel)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def collection():
    return read(AREA/'batch-inventory.json')

def validate_record(row,receipt):
    if receipt['status']!='PASS_BOUNDED_LEAN_CHECKS':raise ValueError('Incomplete historical batch '+row['batch'])
    if receipt['input_hashes_before']!=receipt['input_hashes_after']:raise ValueError('Historical input drift')
    labels=[c.get('label',c.get('name')) for c in receipt['commands']]
    if labels!=row['command_labels'] or any(c['exit_code']!=0 for c in receipt['commands']):
        raise ValueError('Missing, reordered or failed command')
    if receipt['signatures']!=row['signatures'] or receipt['axioms']!=row['axioms']:
        raise ValueError('Changed signature/axiom record')
    if any(set(a)-ALLOWED for a in receipt['axioms'].values()):raise ValueError('Undeclared axiom')
    if list(receipt['signatures'])!=row['names']:raise ValueError('Changed declaration inventory')
    for item in row['preserved_inputs']:
        if sha(ROOT/item['path'])!=item['sha256']:raise ValueError('Changed input '+item['path'])
    return True

def saved(row):
    receipt=read(ROOT/row['receipt'])
    validate_record(row,receipt)
    if sha(ROOT/row['receipt'])!=row['receipt_sha256']:raise ValueError('Historical receipt changed')
    parser=load('parser_'+row['family'],row['parser'])
    texts=[]
    for c in receipt['commands']:
        if row['family']=='pal24':
            p=ROOT/c['stdout_log']
            if sha(p)!=c['stdout_log_sha256']:raise ValueError('Changed saved log')
            parsed=parser.parse_command_log(p)
            for field in ['argv','cwd','exit_code']:
                if parsed[field]!=c[field]:raise ValueError('Changed log command identity')
            for stream in ['stdout','stderr']:
                if hashlib.sha256(parsed[stream].encode()).hexdigest()!=c[stream+'_sha256']:
                    raise ValueError('Changed saved stream')
            texts.append(parsed['stdout'])
        else:
            for stream in ['stdout','stderr']:
                if sha(ROOT/c[stream])!=c[stream+'_sha256']:raise ValueError('Missing or changed saved log')
            texts.append((ROOT/c['stdout']).read_text(encoding='utf-8'))
    index=1 if row['family']=='pal24' else 2
    inspect=parser.parse_inspection if row['family']=='pal24' else parser.inspections
    sig,ax=inspect(texts[index],row['names'])
    if sig!=row['signatures'] or ax!=row['axioms']:raise ValueError('Saved inspection differs')
    return parser,inspect

def self_test(rows):
    row=rows[0];original=read(ROOT/row['receipt'])
    mutations=[lambda r:r['commands'].pop(),lambda r:r['commands'].reverse(),
      lambda r:r['commands'][0].update(exit_code=1),lambda r:r.update(status='PARTIAL'),
      lambda r:r['signatures'].update({row['names'][0]:'False'}),
      lambda r:r['axioms'].update({row['names'][0]:['sorryAx']}),
      lambda r:r['input_hashes_after'].update({'changed':'0'*64})]
    for mutate in mutations:
        r=copy.deepcopy(original);mutate(r)
        try:validate_record(row,r)
        except (ValueError,KeyError):continue
        raise AssertionError('A malformed receipt was accepted')
    bad=copy.deepcopy(row);bad['preserved_inputs'][0]['path']='__MISSING_MIGRATION_INPUT__'
    try:validate_record(bad,original)
    except FileNotFoundError:pass
    else:raise AssertionError('Missing input accepted')
    print('PASS 8 negative receipt/input controls',flush=True)

def source_check(mapping,source_root):
    result=[]
    for row in mapping:
        item={k:v for k,v in row.items() if k!='local_path'}
        if source_root:
            base=Path(source_root).resolve();p=(base/row['local_path']).resolve()
            if not p.is_relative_to(base):raise ValueError('Source mapping escapes supplied home')
            if sha(p)!=row['sha256']:raise ValueError('Missing or changed source bytes: '+row['local_path'])
            item['status']='PASS_EXACT_LOCAL_SOURCE_BYTES'
        else:item['status']='NOT_REPLAYED_SOURCE_BYTES_LOCAL_ONLY'
        result.append(item)
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--replay',action='store_true');ap.add_argument('--family',choices=['pal24','loops','workshop'])
    ap.add_argument('--output',default='.collection-evidence/batches')
    ap.add_argument('--source-root');args=ap.parse_args()
    inventory=collection();rows=[r for r in inventory['batches'] if not args.family or r['family']==args.family]
    for row in rows:saved(row)
    self_test(rows)
    sources=source_check(inventory['local_sources'],args.source_root)
    print('PASS saved receipts, exact proof bytes and dependency inventories; '+str(len(rows))+' batches',flush=True)
    if not args.replay:return
    out=(ROOT/args.output).resolve()
    if not out.is_relative_to(ROOT):raise ValueError('Output must stay inside checkout')
    out.mkdir(parents=True,exist_ok=False)
    lake=shutil.which('lake') or str(Path.home()/'.elan/bin'/('lake.exe' if os.name=='nt' else 'lake'))
    commands=[];result={'status':'IN_PROGRESS','batches':[],'sources':sources,
      'scope':'Exact formal statements, signatures, axiom inventories and bundled Lean kernel; source bytes separate; no publication-source rebind',
      'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':commands}
    def run(label,args):
        start=time.monotonic();print('START '+label,flush=True)
        p=subprocess.run([lake]+args,cwd=ROOT,capture_output=True,timeout=1200)
        for stream in ['stdout','stderr']:(out/(label+'.'+stream+'.txt')).write_bytes(getattr(p,stream))
        commands.append({'label':label,'args':args,'exit_code':p.returncode,'seconds':time.monotonic()-start,
          **{s+'_sha256':hashlib.sha256(getattr(p,s)).hexdigest() for s in ['stdout','stderr']}})
        write(out/'receipt.json',result)
        if p.returncode:raise RuntimeError(label+' failed: '+p.stderr.decode('utf-8',errors='replace')[-3000:])
        return p.stdout.decode('utf-8').replace('\r\n','\n')
    try:
        version=run('lean-version',['env','lean','--version'])
        if '4.32.1' not in version:raise ValueError('Toolchain differs')
        for row in rows:
            _,inspect=saved(row);label=row['batch']
            run(label+'-build',['build',row['module']])
            text=run(label+'-inspect',['env','lean',row['axioms_file']])
            sig,ax=inspect(text,row['names'])
            if sig!=row['signatures'] or ax!=row['axioms']:raise ValueError('Fresh signature/axiom difference: '+label)
            run(label+'-kernel',['env','leanchecker',row['module']])
            result['batches'].append({'batch':label,'status':'PASS_FRESH_FORMAL_REPLAY',
              'historical_receipt_sha256':row['receipt_sha256'],'declarations':len(row['names'])})
            print('PASS '+label,flush=True)
        for row in rows:saved(row)
        result['status']='PASS_FRESH_FORMAL_REPLAY'
    except Exception as e:
        result['status']='FAILED_OR_INCOMPLETE';result['error']=str(e);raise
    finally:write(out/'receipt.json',result)

if __name__=='__main__':main()
