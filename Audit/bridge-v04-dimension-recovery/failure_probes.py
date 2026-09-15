"""Expected tooling failures are retained as receipts, never mathematical results."""
import argparse, importlib.util, sys
from pathlib import Path
from types import SimpleNamespace

AREA = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('bridge_recovery_runner', AREA / 'run.py')
runner = importlib.util.module_from_spec(spec); spec.loader.exec_module(runner)

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output-dir', type=Path, required=True); args = parser.parse_args()
    output = args.output_dir.resolve(); runner.rel(output); assert not output.exists(); output.mkdir(parents=True)
    missing = output / 'missing-executable'
    try: runner.run(SimpleNamespace(lake=str(output / 'no-such-lake'), source_file=None, output_dir=missing), replay=False)
    except RuntimeError: pass
    else: raise AssertionError('missing executable unexpectedly passed')
    receipt = runner.read(missing / 'execution.json'); assert receipt['status'] == 'FAILED_BRIDGE_DIMENSION_RECOVERY' and receipt['commands'][0]['exit_code'] == 127
    assert len(receipt['commands']) == 1 and receipt['commands'][0]['sha256'] == runner.sha(missing / 'lean-version.txt')
    assert receipt['inputs'] == receipt['input_after'] and receipt['error']
    results = [{'case':'missing-executable','exit_code':127,'full_failure_receipt_saved':True}]
    for label, code, expected, timeout in [('nonzero-exit',"print('EXPECTED_NONZERO');raise SystemExit(7)",7,10),('timeout',"import time;print('EXPECTED_TIMEOUT',flush=True);time.sleep(20)",124,1)]:
        directory=output/label; directory.mkdir(); original=runner.commands; runner.commands=lambda lake,python,evidence_directory=None,label=label,code=code:[(label,[python,'-c',code])]
        data={'commands':[],'python_executable':sys.executable}
        try: runner.execute('unused',directory,data,timeout=timeout)
        except RuntimeError: pass
        else: raise AssertionError('probe unexpectedly passed')
        finally: runner.commands=original
        command=data['commands'][0]; assert command['exit_code']==expected and command['sha256']==runner.sha(directory/f'{label}.txt')
        assert len(data['commands']) == 1 and 'EXPECTED_' in (directory / f'{label}.txt').read_text(encoding='utf-8')
        runner.write(directory/'command-receipt.json',data); results.append({'case':label,'exit_code':expected,'failed_command_and_output_retained':True})
    runner.write(output/'failure-probes.json',{'status':'PASS_EXPECTED_TOOLING_FAILURES','population':'TOOLING_TESTS_NOT_THEOREMS','cases':results})
    print('PASS_EXPECTED_TOOLING_FAILURES')
if __name__ == '__main__': main()
