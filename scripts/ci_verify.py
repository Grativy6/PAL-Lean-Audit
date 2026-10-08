"""Portable replay of the frozen FRONT inventory without replacing historical receipts."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, platform, re, shutil, subprocess, sys, time
import verify_formal as historical

ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def saved():
    receipt=read(ROOT/'Audit/receipts/formal/receipt.json')
    if receipt['status']!='PASS_SOURCE_BOUND_KERNEL_CHECKS': raise ValueError('Historical receipt is not passing')
    if historical.inputs()!=receipt['inputs_after']: raise ValueError('Frozen proof inputs changed')
    for command in receipt['commands']:
        if command['exit_code']!=0:raise ValueError('Historical command failed')
        for stream in ('stdout','stderr'):
            if sha(ROOT/command[stream])!=command[stream+'_sha256']:raise ValueError('Historical log changed')
    inventory=read(ROOT/'Audit/declarations.json')
    names=[d['name'] for d in inventory['declarations']]
    signatures,axioms=historical.inspect((ROOT/'Audit/receipts/formal/axioms.stdout.txt').read_text(encoding='utf-8'),names)
    if signatures!=receipt['signatures'] or axioms!=receipt['axioms']:raise ValueError('Historical inventory mismatch')
    publication=ROOT/'Publication/source-concordance.json'
    if publication.exists():
        concordance=read(publication)
        for rel,digest in concordance['repository_files'].items():
            p=(ROOT/rel).resolve()
            if not p.is_relative_to(ROOT) or sha(p)!=digest:raise ValueError('Publication byte mismatch: '+rel)
        source=(ROOT/'Publication/audited-source/FRONT_v1.0_WORKING_DRAFT.md').read_text(encoding='utf-8-sig')
        release=(ROOT/'Publication/FRONT_v1.0.md').read_text(encoding='utf-8-sig')
        for pattern in (r'\\\[(.*?)\\\]',r'\\\((.*?)\\\)'):
            if re.findall(pattern,source,re.S)!=re.findall(pattern,release,re.S):raise ValueError('Publication math differs')
        for block in concordance['proposition_blocks']:
            if block['release_sha256']!=hashlib.sha256(block['release_text'].encode()).hexdigest():raise ValueError('Bad proposition digest')
            if block['release_text'] not in release:raise ValueError('Publication proposition differs')
    return receipt,inventory

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    parser.add_argument('--output',default='.ci-evidence')
    args=parser.parse_args()
    receipt,inventory=saved()
    print('PASS frozen inputs, retained logs, exact signatures and axiom inventory',flush=True)
    if not args.replay:return
    lake=shutil.which('lake') or str(Path.home()/'.elan/bin'/('lake.exe' if os.name=='nt' else 'lake'))
    out=(ROOT/args.output).resolve()
    if not out.is_relative_to(ROOT):raise ValueError('Replay output must stay within the checkout')
    out.mkdir(parents=True,exist_ok=False)
    before=historical.inputs();commands=[]
    def run(label,arguments):
        start=time.monotonic()
        print('START '+label,flush=True)
        result=subprocess.run([lake]+arguments,cwd=ROOT,capture_output=True,timeout=900)
        for stream,data in [('stdout',result.stdout),('stderr',result.stderr)]:
            (out/(label+'.'+stream+'.txt')).write_bytes(data)
        entry={'label':label,'arguments':arguments,'exit_code':result.returncode,
               'seconds':time.monotonic()-start,'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),
               'stderr_sha256':hashlib.sha256(result.stderr).hexdigest()}
        commands.append(entry)
        if result.returncode:
            print(result.stderr.decode('utf-8',errors='replace'))
            raise RuntimeError(label+' failed')
        print('PASS '+label,flush=True)
        return result.stdout.decode('utf-8')
    status='FAIL'
    try:
        run('lean-version',['env','lean','--version'])
        run('build',['build','FrontLean'])
        text=run('axioms',['env','lean','Audit/Axioms.lean'])
        signatures,axioms=historical.inspect(text,[d['name'] for d in inventory['declarations']])
        if signatures!=receipt['signatures'] or axioms!=receipt['axioms']:
            raise ValueError('Fresh signatures or axiom dependencies differ from the retained inventory')
        for module in inventory['modules']:
            run('kernel-'+module.replace('.','-'),['env','leanchecker',module])
        if before!=historical.inputs():raise ValueError('Proof inputs changed during replay')
        saved()
        status='PASS_FRESH_PORTABLE_KERNEL_REPLAY'
    finally:
        result={'status':status,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'platform':platform.platform(),'python':sys.version,'inputs':before,'commands':commands,
                'inventory_declarations':len(inventory['declarations']),'kernel_modules':len(inventory['modules']),
                'historical_receipt_sha256':sha(ROOT/'Audit/receipts/formal/receipt.json'),
                'limit':'Same pinned Lean kernel family; no independent scientific review or Python refinement proof'}
        (out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(status,flush=True)

if __name__=='__main__':main()
