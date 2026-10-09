"""Portable replay of the imported APCI core and separately scoped supplement."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,shutil,subprocess,time
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT/'projects/APCI'
SUPPLEMENT=ROOT/'supplements/APCI-manuscript-20261008'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def deps(text):
    rows=re.findall(r"'([^']+)' (?:does not depend on any axioms|depends on axioms:\s*\[(.*?)\])",text,re.S)
    if len({n for n,_ in rows})!=len(rows):raise ValueError('Duplicate axiom record')
    return {n:sorted(a.strip() for a in raw.split(',') if a.strip()) for n,raw in rows}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='.collection-evidence/apci');args=ap.parse_args()
    out=(ROOT/args.output).resolve()
    if not out.is_relative_to(ROOT):raise ValueError('Output must stay inside checkout')
    out.mkdir(parents=True,exist_ok=False)
    lake=shutil.which('lake') or str(Path.home()/'.elan/bin'/('lake.exe' if os.name=='nt' else 'lake'))
    results={'status':'IN_PROGRESS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':[],
      'scope':'15 original declarations and separate four-theorem manuscript supplement; no full paper or source-byte certification'}
    def run(label,cmd,env=None):
        start=time.monotonic();p=subprocess.run(cmd,cwd=PROJECT,env=env,capture_output=True,timeout=600)
        for s in ['stdout','stderr']:(out/(label+'.'+s+'.txt')).write_bytes(getattr(p,s))
        results['commands'].append({'label':label,'argv':cmd,'exit_code':p.returncode,'seconds':time.monotonic()-start,
           **{s+'_sha256':hashlib.sha256(getattr(p,s)).hexdigest() for s in ['stdout','stderr']}})
        print(label,p.returncode,flush=True)
        if p.returncode:raise RuntimeError(label+' failed: '+p.stderr.decode('utf-8',errors='replace'))
        return p.stdout.decode('utf-8').replace('\r\n','\n')
    try:
        if (PROJECT/'lean-toolchain').read_text().strip()!='leanprover/lean4:v4.32.1':raise ValueError('Toolchain drift')
        if json.loads((PROJECT/'lake-manifest.json').read_text())['packages']!=[]:raise ValueError('Third-party dependencies present')
        inventory=json.loads((PROJECT/'THEOREM_INVENTORY.json').read_text())
        names=[x['name'] for x in inventory['declarations']]
        if len(names)!=15 or len(set(names))!=15:raise ValueError('Core inventory changed')
        run('inventory',[os.sys.executable,'scripts/check_inventory.py'])
        run('build',[lake,'build'])
        actual=deps(run('core-dependencies',[lake,'env','lean','Audit.lean']))
        expected=deps((PROJECT/'audit/AXIOM_RECEIPT.txt').read_text())
        if actual!=expected or set(actual)!=set(names):raise ValueError('Core axiom inventory drift')
        run('core-kernel',[lake,'env','leanchecker','APCILeanAudit'])
        source=SUPPLEMENT/'Audits/2026-10-08-manuscript/APCIManuscript.lean'
        if sha(source)!='e996a7b38e71402d6e58a07551015e858c0523ba6e475d15f8bf500a2e2005cf':raise ValueError('Supplement changed')
        code=source.read_text(encoding='utf-8')
        if re.search(r'\b(sorry|admit|axiom|opaque|unsafe|native_decide|run_tac)\b',code):raise ValueError('Supplement escape')
        # Use the actual pinned toolchain binary while explicitly adding the newly
        # compiled supplement directory to Lean's module search path.
        prefix=run('tool-prefix',[lake,'env','lean','--print-prefix']).strip()
        suffix='.exe' if os.name=='nt' else ''
        env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join([str(out),str(PROJECT/'.lake/build/lib/lean')])
        text=run('supplement-compile',[str(Path(prefix)/'bin'/('lean'+suffix)),'-R',str(source.parent),'-j','1','-M','2048','-o',str(out/'APCIManuscript.olean'),str(source)],env)
        wanted={'APCIManuscript.no_exact_on_witness_of_capacity':['Classical.choice','Quot.sound','propext'],
          'APCIManuscript.infinite_world_constant_property':[],
          'APCIManuscript.side_information_changes_interface':[],
          'APCIManuscript.empty_trace_allows_empty_answer':[]}
        if deps(text)!=wanted:raise ValueError('Supplement axiom inventory drift')
        text=run('supplement-kernel',[str(Path(prefix)/'bin'/('leanchecker'+suffix)),'--verbose','APCIManuscript'],env)
        if 'replaying APCIManuscript' not in text:raise ValueError('Target kernel replay not witnessed')
        results.update(status='PASS_FRESH_APCI_AND_SEPARATE_SUPPLEMENT',core_axioms=actual,supplement_axioms=wanted)
    except Exception as e:results.update(status='FAILED_OR_INCOMPLETE',error=str(e));raise
    finally:(out/'receipt.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
