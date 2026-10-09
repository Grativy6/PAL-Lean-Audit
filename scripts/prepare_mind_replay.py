"""Keep MIND's frozen whole-repository inventory separate from later additions."""
from pathlib import Path
import argparse,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
BASE='f52f5f09993d63b513105817554df262f570529b'
WORKFLOW='.github/workflows/mind-continuation.yml'
def canonical(data):return hashlib.sha256(data.replace(b'\r\n',b'\n')).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('destination');args=ap.parse_args()
    dest=Path(args.destination).resolve()
    if dest.exists():raise ValueError('Use a fresh destination; historical copies are never replaced')
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
    subprocess.run(['git','worktree','add','--detach',str(dest),BASE],cwd=ROOT,check=True)
    record={'status':'PASS_CURRENT_INPUT_CORRESPONDENCE',
      'current_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
      'replay_commit':BASE,'historical_inputs':historical,'matching_current_inputs':current,
      'separate_workflow':{'path':WORKFLOW,'current_sha256':hashlib.sha256((ROOT/WORKFLOW).read_bytes()).hexdigest(),
        'historical_canonical_sha256':historical[WORKFLOW]},
      'scope':'All frozen MIND proof, runner, ledger and dependency inputs still match the current collection. Only the CI orchestration file differs. Replay occurs in its original whole-repository inventory; later unrelated files are outside that historical population.'}
    (dest/'MIND-COLLECTION-CORRESPONDENCE.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('PASS',len(current),'current input identities; preserved historical inventory',len(historical))
if __name__=='__main__':main()
