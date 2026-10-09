"""Run the declared local integration checks; never publish or rewrite history."""
from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AREA = ROOT / 'Audit/pal-v24-batches/integration'
LAKE = str(Path.home() / '.elan/bin/lake.exe')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def main():
    started = datetime.now(timezone.utc)
    attempt = AREA / started.strftime('attempt-%Y%m%dT%H%M%S%fZ')
    attempt.mkdir(parents=True, exist_ok=False)
    sources = attempt / 'source-copies'
    sources.mkdir()
    original = json.loads((ROOT / 'Audit/pal-v23-charter/source-manifest.json').read_text(encoding='utf-8'))
    verified_sources = []
    for row in original['sources']:
        source = Path(row['path'])
        if sha(source) != row['sha256']:
            raise ValueError(f'Original source changed: {source}')
        copy = sources / row['filename']
        shutil.copyfile(source, copy)
        assert sha(copy) == row['sha256']
        verified_sources.append({'path': str(source), 'sha256': row['sha256'], 'copy': copy.relative_to(ROOT).as_posix()})

    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode('utf-8').split('\0')
    paths = {ROOT / name for name in tracked if name and (ROOT / name).is_file()}
    paths.update(ROOT.glob('Experiments/*.lean'))
    paths.update((ROOT / 'Audit/pal-v24-batches').glob('*/claims.json'))
    paths.update({Path(__file__), ROOT / 'Audit/pal-v24-batches/run.py', ROOT / 'Audit/pal-v24-candidate/source-manifest.json'})
    before = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(paths)}
    receipt = {
        'schema': 'pal-v24-local-integration-v1', 'status': 'RUNNING',
        'started_utc': started.isoformat(), 'platform': platform.platform(),
        'python': sys.version, 'cwd': str(ROOT),
        'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
        'scope': 'Local integration and preserved historical evidence only; not GitHub CI or full PAL conformance.',
        'published_v21_archive_retrieved': False,
        'nanoda': 'NOT_RUN: optional experimental checker; no new claim of success',
        'verified_source_copies': verified_sources, 'input_hashes_before': before, 'commands': [],
    }
    py = [sys.executable, '-X', 'utf8']
    jobs = [
        ('full-build', [LAKE, 'build']),
        ('historical-kernel-check', [LAKE, 'env', 'leanchecker', 'PALLeanAudit']),
        ('historical-policy', py + ['scripts/check_policy.py']),
        ('ar3-policy', py + ['scripts/check_attack_run_0003_policy.py']),
        ('ar3-structure', py + ['scripts/check_attack_run_0003.py']),
        ('candidate-input-locks', py + ['scripts/check_candidate_inputs.py']),
        ('migration-metadata', py + ['scripts/check_release_migration.py']),
        ('ar1-report', py + ['scripts/render_report.py', '--check']),
        ('ar2-report', py + ['scripts/render_report.py', '--ledger', 'Audit/attack-run-0002-claim-ledger.json', '--summary', 'docs/generated/attack-run-0002-summary.md', '--chart', 'docs/generated/attack-run-0002-outcomes.svg', '--check']),
        ('migration-report', py + ['scripts/render_migration_report.py', '--check']),
        ('ar3-report', py + ['scripts/render_attack_run_0003.py', '--check']),
        ('pal23-charter-preserved-receipt', py + ['scripts/run_pal23_charter.py', '--check']),
        ('pal23-charter-replay', py + ['Audit/pal-v23-charter/check_publication.py', '--replay', '--lake', LAKE, '--source-dir', str(sources), '--output-dir', str(attempt / 'pal23-charter-replay')]),
        ('tracked-diff-whitespace', ['git', 'diff', '--check']),
    ]
    write(AREA / 'results.json', receipt)
    for name, argv in jobs:
        print(f'Running {name}', flush=True)
        t0 = time.monotonic()
        try:
            proc = subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1800)
            code, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as exc:
            code, stdout, stderr = -1, exc.stdout or b'', (exc.stderr or b'') + b'\nTIMEOUT\n'
        logs = {}
        for stream, data in [('stdout', stdout), ('stderr', stderr)]:
            p = attempt / f'{name}.{stream}.log'
            p.write_bytes(data)
            logs[stream] = {'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'bytes': len(data)}
        receipt['commands'].append({'name': name, 'argv': argv, 'cwd': str(ROOT), 'exit_code': code,
            'runtime_seconds': round(time.monotonic() - t0, 6), 'logs': logs})
        write(AREA / 'results.json', receipt)
        print(f'{name}: {code}', flush=True)

    after = {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(paths)}
    receipt['input_hashes_after'] = after
    receipt['inputs_unchanged'] = before == after
    receipt['finished_utc'] = datetime.now(timezone.utc).isoformat()
    receipt['status'] = 'PASS_LOCAL_INTEGRATION' if before == after and all(r['exit_code'] == 0 for r in receipt['commands']) else 'FAILED_LOCAL_INTEGRATION'
    write(attempt / 'results.json', receipt)
    write(AREA / 'results.json', receipt)
    print(receipt['status'], flush=True)
    return 0 if receipt['status'] == 'PASS_LOCAL_INTEGRATION' else 1


if __name__ == '__main__':
    raise SystemExit(main())
