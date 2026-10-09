import hashlib
import json
import pathlib
import re
import shutil
import subprocess
from datetime import datetime, timezone

bench = pathlib.Path("/mnt/h/Hearthline's Path/Math Workbench/openai-math-pi-2026-10-06")
audit = pathlib.Path('/home/cdpang/math-pi-audit-20261006')
out = bench / 'evidence'

def command(*args, cwd=None):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return {'argv': list(args), 'exit_code': result.returncode,
            'stdout': result.stdout, 'stderr': result.stderr}

def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(data)
    return digest.hexdigest()

def check_receipt(folder, log_name, exit_name):
    log_path, exit_path = folder / log_name, folder / exit_name
    if not exit_path.exists():
        return {'status': 'NOT_COMPLETED', 'path': str(folder)}
    code = int(exit_path.read_text().strip())
    log = log_path.read_text(errors='replace') if log_path.exists() else ''
    kernel = 'Lean default kernel accepts the solution' in log
    completed = 'Your solution is okay!' in log
    return {'status': 'PASS' if code == 0 and kernel and completed else 'NOT_PASSED',
            'exit_code': code, 'kernel_acceptance_marker': kernel,
            'comparator_success_marker': completed, 'log_sha256': sha(log_path),
            'path': str(folder)}

tool_logs = out / 'tool-setup'
tool_logs.mkdir(exist_ok=True)
for path in (audit / 'logs').iterdir():
    if path.is_file() and path.suffix in {'.txt', '.log', '.json', '.diff'}:
        shutil.copyfile(path, tool_logs / path.name)

tools = {}
for name in ['comparator', 'landrun']:
    root = audit / 'tools' / name
    tools[name] = {
        'revision': command('git', 'rev-parse', 'HEAD', cwd=root),
        'tracked_changes': command('git', 'status', '--porcelain', '--untracked-files=no', cwd=root),
        'diff': command('git', 'diff', cwd=root),
    }
export_root = audit / 'tools/comparator/.lake/packages/lean4export'
tools['lean4export'] = {
    'revision': command('git', 'rev-parse', 'HEAD', cwd=export_root),
    'tracked_changes': command('git', 'status', '--porcelain', '--untracked-files=no', cwd=export_root),
}
tools['lean_version'] = command(str(audit / 'tools/lean-4.34.1-linux/bin/lean'), '--version')
tools['lake_version'] = command(str(audit / 'tools/lean-4.34.1-linux/bin/lake'), '--version')
tools['kernel'] = command('uname', '-sr')
tools['map_limit'] = pathlib.Path('/proc/sys/vm/max_map_count').read_text().strip()

binaries = {}
for rel in ['tools/lean-4.34.1-linux/bin/lean', 'tools/lean-4.34.1-linux/bin/lake',
            'tools/comparator/.lake/build/bin/comparator',
            'tools/comparator/.lake/packages/lean4export/.lake/build/bin/lean4export',
            'tools/landrun-bin', 'tools/landrun-with-threads']:
    path = audit / rel
    binaries[rel] = {'bytes': path.stat().st_size, 'sha256': sha(path)}

manifest_path = audit / 'project/lake-manifest.json'
shutil.copyfile(manifest_path, out / 'resolved-lake-manifest.json')
package_states = []
for package in json.loads(manifest_path.read_text())['packages']:
    root = audit / 'project/.lake/packages' / package['name']
    package_states.append({
        'name': package['name'], 'expected_revision': package.get('rev'),
        'actual_revision': command('git', 'rev-parse', 'HEAD', cwd=root),
        'tracked_changes': command('git', 'status', '--porcelain', '--untracked-files=no', cwd=root),
    })

attempts = {}
if (audit / 'logs/comparator-exit.txt').exists():
    attempts['initial-root-registration-error'] = check_receipt(
        audit / 'logs', 'comparator-run.log', 'comparator-exit.txt')
    attempts['initial-root-registration-error']['classification'] = 'Audit Lake configuration failure before proof elaboration; retained and repaired.'
for path in sorted((audit / 'logs').glob('attempt-*')):
    attempts[path.name] = check_receipt(path, 'comparator-run.log', 'comparator-exit.txt')
supplement = check_receipt(audit / 'logs/supplement', 'comparator.log', 'exit.txt')
axiom_path = audit / 'logs/supplement/axioms.log'
axiom_exit = audit / 'logs/supplement/axioms-exit.txt'
axioms = {'status': 'NOT_RUN'}
if axiom_path.exists() and axiom_exit.exists():
    axiom_text = axiom_path.read_text()
    declarations = {
        name: [item.strip() for item in names.split(',') if item.strip()]
        for name, names in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", axiom_text)
    }
    expected_declarations = {
        'OAI.PiExponent.main', 'OAI.PiExponent.pi_eventual_lower_bound',
        'OAI.PiExponent.pi_irrationalityExponent_eq_two', 'OAI.PiExponent.flint_hills_summable'
    }
    allowed = {'propext', 'Quot.sound', 'Classical.choice'}
    axiom_ok = (int(axiom_exit.read_text().strip()) == 0
                and expected_declarations.issubset(declarations)
                and all(set(declarations[name]).issubset(allowed) for name in expected_declarations))
    axioms = {'exit_code': int(axiom_exit.read_text().strip()),
              'status': 'PASS' if axiom_ok else 'NEEDS_REVIEW',
              'declarations': declarations,
              'stdout_and_service_log': axiom_text, 'sha256': sha(axiom_path)}

main_success = any(item['status'] == 'PASS' for item in attempts.values())
integrity = json.loads((out / 'source-integrity.json').read_text())
result = {
    'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
    'target': 'OAI.PiExponent.main',
    'source_revision': integrity['source_revision'],
    'main_formal_check': 'PASS' if main_success else 'NOT_VERIFIED',
    'main_attempts': attempts,
    'flint_hills_supplement': supplement,
    'explicit_axiom_inspection': axioms,
    'source_integrity': {'result': integrity['result'],
                         'proof_source_count': integrity['proof_source_count'],
                         'receipt_sha256': sha(out / 'source-integrity.json')},
    'proof_olean_count': len(list((audit / 'project/.lake/build/lib/lean/OAI/NumberTheory/PiExponent').rglob('*.olean'))),
    'permitted_axioms': ['propext', 'Quot.sound', 'Classical.choice'],
    'independent_kernel_implementation_used': False,
    'tool_metadata': tools,
    'tool_binary_hashes': binaries,
    'dependency_sources': package_states,
    'storage': command('du', '-sh', str(audit), str(bench)),
    'limits': [
        'Single-assistant prose review, not an independent second referee.',
        'Trusted public Lean release and pinned Mathlib cache; unrelated Mathlib modules were not all rebuilt.',
        'Isolated Lake dependency slice; original proof sources and official target are unchanged.',
        'Flint-Hills target, when run, is audit-authored and separate from the official PiExponent challenge.',
    ],
}
(out / 'verification-results.json').write_text(json.dumps(result, indent=2))
print(json.dumps({key: result[key] for key in ['main_formal_check', 'flint_hills_supplement', 'proof_olean_count']}, indent=2))
