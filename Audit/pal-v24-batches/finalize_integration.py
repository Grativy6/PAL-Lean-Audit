"""Resolve only the obsolete whole-directory receipt check, preserving its failure.

The final receipt combines unchanged successful command evidence with a newly run
scoped validator already used by this repository's PAL23/CHARTER CI workflow.
It does not replay or relabel any failed Lean command.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AREA = ROOT / 'Audit/pal-v24-batches/integration'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    result_path = AREA / 'results.json'
    old = json.loads(result_path.read_text(encoding='utf-8'))
    failures = [r for r in old['commands'] if r['exit_code'] != 0]
    assert old['status'] == 'FAILED_LOCAL_INTEGRATION'
    assert len(failures) == 1 and failures[0]['name'] == 'pal23-charter-preserved-receipt'
    assert old['inputs_unchanged'] and old['input_hashes_before'] == old['input_hashes_after']
    for name, digest in old['input_hashes_after'].items():
        assert sha(ROOT / name) == digest, name
    diagnosis_path = AREA / 'legacy-hash-diagnosis.json'
    diagnosis = json.loads(diagnosis_path.read_text(encoding='utf-8'))
    assert diagnosis['summary']['added_paths'] > 0
    assert diagnosis['summary']['changed_original_paths'] == 0
    assert all(r['historical_raw'] is None for r in diagnosis['mismatches'])
    parent = Path(old['commands'][0]['logs']['stdout']['path']).parent / 'results.json'
    assert (ROOT / parent).read_bytes() == result_path.read_bytes()
    stamp = datetime.now(timezone.utc)
    evidence = AREA / stamp.strftime('scoped-validator-%Y%m%dT%H%M%S%fZ')
    evidence.mkdir(exist_ok=False)
    source_dir = (ROOT / old['verified_source_copies'][0]['copy']).parent
    argv = [sys.executable, '-X', 'utf8', 'Audit/pal-v23-charter/check_publication.py', '--check', '--source-dir', str(source_dir)]
    t0 = time.monotonic()
    p = subprocess.run(argv, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
    row = {'name': 'pal23-charter-preserved-receipt', 'argv': argv, 'cwd': str(ROOT),
           'exit_code': p.returncode, 'runtime_seconds': round(time.monotonic() - t0, 6), 'logs': {},
           'started_utc': stamp.isoformat(), 'finished_utc': datetime.now(timezone.utc).isoformat()}
    for stream, data in [('stdout', p.stdout), ('stderr', p.stderr)]:
        log = evidence / f'publication-validator.{stream}.log'
        log.write_bytes(data)
        row['logs'][stream] = {'path': log.relative_to(ROOT).as_posix(), 'sha256': sha(log), 'bytes': len(data)}
    (evidence / 'command.json').write_text(json.dumps(row, indent=2) + '\n', encoding='utf-8')
    if p.returncode != 0:
        print('FAILED_SCOPED_HISTORICAL_VALIDATOR')
        return 1
    for name, digest in old['input_hashes_after'].items():
        assert sha(ROOT / name) == digest, name
    result = dict(old)
    result['status'] = 'PASS_LOCAL_INTEGRATION'
    result['assembly_method'] = '13 successful commands retained with unchanged inputs; one scoped historical validator executed now. Command list is logical inventory order, not a new sequential replay.'
    result['parent_attempt'] = {'path': parent.as_posix(), 'sha256': sha(ROOT / parent), 'status': old['status']}
    result['assembly_tool'] = {'path': Path(__file__).relative_to(ROOT).as_posix(), 'sha256': sha(Path(__file__))}
    result['diagnosis'] = {'path': diagnosis_path.relative_to(ROOT).as_posix(), 'sha256': sha(diagnosis_path)}
    result['retained_failed_diagnostics'] = [{'command': failures[0], 'disposition': f"Obsolete whole-directory inventory guard: {diagnosis['summary']['added_paths']} later experiment files are additions; no historical raw input changed. The committed scoped publication validator is the applicable preserved-evidence check."}]
    result['commands'] = [row if r['name'] == row['name'] else r for r in old['commands']]
    result['finished_utc'] = row['finished_utc']
    serialized = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
    (evidence / 'results.json').write_text(serialized, encoding='utf-8')
    result_path.write_text(serialized, encoding='utf-8')
    print('PASS_LOCAL_INTEGRATION: 14 scoped checks; obsolete diagnostic failure retained; no repeated Lean execution.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
