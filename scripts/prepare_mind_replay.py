"""Keep MIND's frozen whole-repository inventory separate from later additions."""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
BASE='f52f5f09993d63b513105817554df262f570529b'
WORKFLOW='.github/workflows/mind-continuation.yml'
def canonical(data):return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('destination')
    ap.add_argument('--replay',action='store_true',help='Replay an already prepared historical checkout')
    args=ap.parse_args()
    dest=Path(args.destination).resolve()
    if dest.exists() and not args.replay:raise ValueError('Use a fresh destination; historical copies are never replaced')
    current_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    ci={k:os.getenv(k) for k in ['GITHUB_ACTIONS','GITHUB_RUN_ID','GITHUB_SHA','MIND_CONTINUATION_PR_HEAD_SHA']}
    if ci['GITHUB_ACTIONS']=='true':
        if ci['GITHUB_SHA']!=current_commit or not ci['GITHUB_RUN_ID']:raise ValueError('Outer CI identity does not match current checkout')
        if not re.fullmatch(r'[a-f0-9]{40}',ci['MIND_CONTINUATION_PR_HEAD_SHA'] or ''):raise ValueError('Missing pull request head identity')
    receipt_path='Audit/mind-v04-continuation/results.json'
    receipt_bytes=(ROOT/receipt_path).read_bytes()
    original_receipt=subprocess.check_output(['git','show',BASE+':'+receipt_path],cwd=ROOT)
    if canonical(receipt_bytes)!=canonical(original_receipt):raise ValueError('Frozen MIND receipt differs')
    receipt=json.loads(original_receipt)
    current={};historical={}
    for name,digest in receipt['input_hashes_canonical_before'].items():
        p=(ROOT/name).resolve()
        if not p.is_relative_to(ROOT):raise ValueError('Input escapes checkout')
        blob=subprocess.check_output(['git','show',BASE+':'+name],cwd=ROOT)
        if canonical(blob)!=digest:raise ValueError('Historical input differs: '+name)
        historical[name]=digest
        if name!=WORKFLOW:
            if canonical(p.read_bytes())!=digest:raise ValueError('Current proof/input differs: '+name)
            current[name]=digest
    if args.replay:
        if subprocess.check_output(['git','rev-parse','HEAD'],cwd=dest,text=True).strip()!=BASE:raise ValueError('Historical checkout revision differs')
        if subprocess.check_output(['git','status','--porcelain'],cwd=dest,text=True).strip():raise ValueError('Historical checkout is dirty')
    else:subprocess.run(['git','worktree','add','--detach',str(dest),BASE],cwd=ROOT,check=True)
    record={'status':'PASS_CURRENT_INPUT_CORRESPONDENCE',
      'current_commit':current_commit,'outer_ci_environment':ci,
      'replay_commit':BASE,'historical_inputs':historical,'matching_current_inputs':current,
      'separate_workflow':{'path':WORKFLOW,'current_sha256':hashlib.sha256((ROOT/WORKFLOW).read_bytes()).hexdigest(),
        'historical_canonical_sha256':historical[WORKFLOW]},
      'scope':'All frozen MIND proof, runner, ledger and dependency inputs still match the current collection. Only the CI orchestration file differs. Replay occurs in its original whole-repository inventory; later unrelated files are outside that historical population.'}
    record_path=dest/'artifacts/MIND-COLLECTION-CORRESPONDENCE.json'
    record_path.parent.mkdir(exist_ok=True)
    record_path.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS',len(current),'current input identities; preserved historical inventory',len(historical))
    if args.replay:
        # The old runner's merge-SHA fields describe its own checkout. Keep the
        # actual modern CI identity above, and run this historical subprocess
        # without claiming that BASE is the modern pull request's merge SHA.
        env=os.environ.copy()
        for key in ci:env.pop(key,None)
        p=subprocess.run([sys.executable,'Audit/mind-v04-continuation/run.py','--replay','--lake','lake',
            '--output-dir','artifacts/mind-continuation-ci'],cwd=dest,env=env)
        record['historical_replay_exit_code']=p.returncode
        result=dest/'artifacts/mind-continuation-ci/results.json'
        record['historical_receipt_sha256']=hashlib.sha256(result.read_bytes()).hexdigest() if result.exists() else None
        drift=[name for name,digest in current.items() if canonical((ROOT/name).read_bytes())!=digest]
        record['changed_current_inputs_after_replay']=drift
        record['status']='PASS_CURRENT_CORRESPONDENCE_AND_HISTORICAL_REPLAY' if p.returncode==0 and not drift else 'FAILED_OR_INCOMPLETE'
        record['source_pdf_status']='NOT_SUPPLIED_IN_THIS_REPLAY'
        record_path.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        if record['status']!='PASS_CURRENT_CORRESPONDENCE_AND_HISTORICAL_REPLAY':raise SystemExit(p.returncode or 1)
if __name__=='__main__':main()
