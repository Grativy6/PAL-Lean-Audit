"""Real failed commands test receipt retention; these are not theorem results."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

AREA = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('bridge_receipts', AREA / 'run.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    runner.rel(output)
    assert not output.exists()
    output.mkdir(parents=True)
    missing = output / 'missing-executable'
    assert not (output / 'no-such-lake-executable').exists()
    try:
        runner.run(SimpleNamespace(lake=str(output / 'no-such-lake-executable'), source_file=None,
                                   output_dir=missing), replay=False)
    except RuntimeError:
        pass
    else:
        raise AssertionError('Missing executable did not fail')
    receipt = runner.read(missing / 'execution.json')
    assert receipt['status'] == 'FAILED_BRIDGE_DIAGRAM_READOUT'
    assert len(receipt['commands']) == 1 and receipt['commands'][0]['exit_code'] == 127
    assert receipt['commands'][0]['sha256'] == runner.sha(missing / 'lean-version.txt')
    assert receipt['inputs'] == receipt['input_after'] and 'error' in receipt
    results = [{'case': 'missing-executable', 'exit_code': 127, 'full_failure_receipt_saved': True}]
    probes = [('nonzero-exit', "print('EXPECTED_NONZERO'); raise SystemExit(7)", 7, 10),
              ('timeout', "import time; print('EXPECTED_TIMEOUT',flush=True); time.sleep(20)", 124, 1)]
    for label, code, expected, timeout in probes:
        directory = output / label
        directory.mkdir()
        runner.commands = lambda lake, python, label=label, code=code: [(label, [python, '-c', code])]
        recorded = {'commands': [], 'python_executable': sys.executable}
        try:
            runner.execute('unused', directory, recorded, timeout=timeout)
        except RuntimeError:
            pass
        else:
            raise AssertionError('Probe did not fail: ' + label)
        assert len(recorded['commands']) == 1
        command = recorded['commands'][0]
        assert command['exit_code'] == expected and command['sha256'] == runner.sha(directory / (label + '.txt'))
        assert 'EXPECTED_' in (directory / (label + '.txt')).read_text(encoding='utf-8')
        runner.write(directory / 'command-receipt.json', recorded)
        results.append({'case': label, 'exit_code': expected, 'failed_command_and_output_retained': True})
    runner.write(output / 'failure-probes.json', {'status': 'PASS_EXPECTED_TOOLING_FAILURES',
                 'population': 'TOOLING_TESTS_NOT_THEOREMS', 'cases': results})
    print('PASS_EXPECTED_TOOLING_FAILURES: missing executable, nonzero exit, timeout')


if __name__ == '__main__':
    main()
