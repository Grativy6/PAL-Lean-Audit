"""Final local gates; preserve historical reports and old proof receipts."""
import json
import sys
from datetime import datetime, timezone
import verify

def main():
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    directory = verify.AREA / 'integration' / stamp
    directory.mkdir(parents=True)
    for batch in verify.MODULES:
        verify.check(batch)
    verify.self_test()
    commands = [
        ('default-build', [verify.LAKE, 'build']),
        ('root-kernel', [verify.LAKE, 'env', 'leanchecker', 'PALLeanAudit']),
        ('historical-policy', [sys.executable, 'scripts/check_policy.py']),
        ('report-check', [sys.executable, 'scripts/render_report.py', '--check']),
        ('migration-report-check', [sys.executable, 'scripts/render_migration_report.py', '--check']),
        ('attack-run-0003-report-check', [sys.executable, 'scripts/render_attack_run_0003.py', '--check']),
        ('preserved-AL-A', [sys.executable, 'Audit/abstract-loops-20261008/verify.py', '--batch', 'AL-A', '--check']),
        ('preserved-AL-B', [sys.executable, 'Audit/abstract-loops-20261008/verify.py', '--batch', 'AL-B', '--check']),
        ('preserved-AL-C', [sys.executable, 'Audit/abstract-loops-20261008/verify.py', '--batch', 'AL-C', '--check']),
        ('diff-check', ['git', 'diff', '--check']),
    ]
    rows = []
    for label, argv in commands:
        row = verify.run(argv, directory, label)
        rows.append(row)
        verify.write(directory/'progress.json', rows)
        print(label, 'exit', row['exit_code'], flush=True)
    for batch in verify.MODULES:
        verify.check(batch)
    result = {
        'schema': 'remaining-workshop-integration-v1',
        'status': 'PASS_INTEGRATION' if all(r['exit_code'] == 0 for r in rows) else 'FAILED_INTEGRATION_GATE',
        'started_utc': stamp, 'git_head': verify.git('rev-parse','HEAD'),
        'commands': rows, 'receipt_mutation_controls': 6,
        'receipts': {b: verify.sha(verify.AREA/b/'results.json') for b in verify.MODULES},
        'literature_record_sha256': verify.sha(verify.AREA/'GPPR-A/LITERATURE.md'),
        'runner_sha256': verify.sha(verify.Path(__file__)),
        'scope': 'Local integration only. Historical policy/reports retain their original scope. New source/axiom/signature policy is enforced by verify.py. No CI, publication or manuscript adoption.',
    }
    verify.write(directory/'results.json',result)
    verify.write(verify.AREA/'integration-results.json',result)
    if result['status'] != 'PASS_INTEGRATION':
        raise SystemExit(1)

if __name__ == '__main__':
    main()
