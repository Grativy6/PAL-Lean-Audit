"""Sequential source-bound build, declaration inspection, and bundled kernel replay."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, subprocess, time

ROOT=Path(__file__).resolve().parents[1]
AREA=ROOT/'Audit/receipts/formal'
LAKE=Path.home()/'.elan/bin/lake.exe'
ALLOWED={'propext','Classical.choice','Quot.sound'}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def inputs():
    paths=[ROOT/p for p in ('lakefile.lean','lake-manifest.json','lean-toolchain','FrontLean.lean',
        'Audit/claims.json','Audit/declarations.json','Audit/Axioms.lean',
        'Audit/bridge-dependencies.json','Audit/dependencies.json',
        'scripts/verify_formal.py','scripts/map_claims.py')]
    for sub in ('FrontLean','APCILeanAudit','Experiments'):
        paths+=list((ROOT/sub).glob('*.lean'))
    return {p.relative_to(ROOT).as_posix():sha(p) for p in sorted(paths)}

def inspect(text,names):
    pattern='|'.join(map(re.escape,names))
    headers=list(re.finditer(r'^@?('+pattern+r')(?:\.\{[^}]+\})?\s*:',text,re.M))
    if [m[1] for m in headers]!=names: raise ValueError('Signature inventory mismatch')
    axrows=re.findall(r"'([^']+)' (does not depend on any axioms|depends on axioms: \[(.*?)\])",text,re.S)
    if [r[0] for r in axrows]!=names: raise ValueError('Axiom inventory mismatch')
    axioms={name:[] if form.startswith('does not') else sorted(a.strip() for a in raw.replace('\n',' ').split(',') if a.strip())
            for name,form,raw in axrows}
    if any(set(a)-ALLOWED for a in axioms.values()): raise ValueError('Unapproved axiom or proof placeholder')
    signatures={}
    for i,match in enumerate(headers):
        end=headers[i+1].start() if i+1<len(headers) else len(text)
        signatures[names[i]]=text[match.start():end].split("'"+names[i]+"'")[0].strip()
    return signatures,axioms

def run(label,argv):
    print('START '+label,flush=True)
    start=time.monotonic()
    completed=subprocess.run([str(x) for x in argv],cwd=ROOT,capture_output=True,timeout=300)
    out=AREA/(label+'.stdout.txt'); err=AREA/(label+'.stderr.txt')
    out.write_bytes(completed.stdout);err.write_bytes(completed.stderr)
    rec=dict(label=label,argv=list(map(str,argv)),cwd=str(ROOT),exit_code=completed.returncode,
             seconds=time.monotonic()-start,stdout=out.relative_to(ROOT).as_posix(),
             stderr=err.relative_to(ROOT).as_posix(),stdout_sha256=sha(out),stderr_sha256=sha(err))
    write(AREA/(label+'.command.json'),rec)
    print('END '+label+' exit='+str(completed.returncode),flush=True)
    if completed.returncode: raise RuntimeError(label+' failed; retained output is in '+str(AREA))
    return rec

def check():
    receipt=read(AREA/'receipt.json')
    if receipt['status']!='PASS_SOURCE_BOUND_KERNEL_CHECKS':raise ValueError('No passing final receipt')
    if inputs()!=receipt['inputs_after']:raise ValueError('Current source differs from checked source')
    for cmd in receipt['commands']:
        if cmd['exit_code']!=0:raise ValueError('Command did not pass')
        for stream in ('stdout','stderr'):
            if sha(ROOT/cmd[stream])!=cmd[stream+'_sha256']:raise ValueError('Command output changed')
    for path,digest in receipt['compiled_artifacts'].items():
        if sha(ROOT/path)!=digest:raise ValueError('Compiled artifact changed')
    names=[d['name'] for d in read(ROOT/'Audit/declarations.json')['declarations']]
    signatures,axioms=inspect((AREA/'axioms.stdout.txt').read_text(encoding='utf-8'),names)
    if signatures!=receipt['signatures'] or axioms!=receipt['axioms']:raise ValueError('Inspection differs')
    print('PASS_SAVED_RECEIPT_INTEGRITY: '+str(len(names))+' declarations; no Lean rerun')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.check:check();return
    AREA.mkdir(parents=True,exist_ok=False)
    before=inputs();inventory=read(ROOT/'Audit/declarations.json');commands=[]
    # The module checker is bundled with this pinned Lean. It is not an independent prover.
    try:
        commands.append(run('lean-version',[LAKE,'env','lean','--version']))
        commands.append(run('build',[LAKE,'build','FrontLean']))
        commands.append(run('axioms',[LAKE,'env','lean','Audit/Axioms.lean']))
        signatures,axioms=inspect((AREA/'axioms.stdout.txt').read_text(encoding='utf-8'),
                                 [d['name'] for d in inventory['declarations']])
        for module in inventory['modules']:
            commands.append(run('kernel-'+module.replace('.','-'),[LAKE,'env','leanchecker',module]))
        after=inputs()
        if after!=before:raise ValueError('Proof inputs changed during sequential final run')
        compiled={}
        for module in inventory['modules']+['FrontLean']:
            path=ROOT/'.lake/build/lib/lean'/(module.replace('.','/')+'.olean')
            compiled[path.relative_to(ROOT).as_posix()]=sha(path)
        receipt=dict(status='PASS_SOURCE_BOUND_KERNEL_CHECKS',
                     utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                     review='SAME_SESSION_SELF_REVIEW',inputs_before=before,inputs_after=after,
                     commands=commands,compiled_artifacts=compiled,signatures=signatures,axioms=axioms,
                     dependency_axioms_allowed=sorted(ALLOWED),
                     limits=['Bundled checker, not independent scientific validation',
                             'Source correspondence and mathematical hypotheses remain part of each claim',
                             'No Python/Lean refinement theorem, external authority validation or complexity separation'])
        write(AREA/'receipt.json',receipt)
        check()
    except Exception as exc:
        write(AREA/'FAILURE.json',{'error':repr(exc),'commands_completed':commands,'inputs_before':before})
        raise

if __name__=='__main__':main()
