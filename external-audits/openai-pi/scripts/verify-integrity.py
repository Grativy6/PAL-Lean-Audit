import hashlib
import json
import pathlib
import subprocess
from datetime import datetime, timezone

bench = pathlib.Path("/mnt/h/Hearthline's Path/Math Workbench/openai-math-pi-2026-10-06")
source = bench / 'source'
build = pathlib.Path('/home/cdpang/math-pi-audit-20261006/project')
expected = 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'

def git(*args):
    return subprocess.check_output(
        ['git', '-c', f'safe.directory={source}', '-C', str(source), *args])

revision = git('rev-parse', 'HEAD').decode().strip()
assert revision == expected, revision
tracked = {}
for entry in git('ls-files', '-s', '-z').split(b'\0'):
    if not entry:
        continue
    header, filename = entry.split(b'\t', 1)
    mode, oid, stage = header.decode().split()
    assert stage == '0', filename
    tracked[filename.decode()] = oid

manifest = json.loads((bench / 'evidence/build-source-manifest.json').read_text())
entries = []
for item in manifest['files']:
    relative = item['path']
    data = (source / 'lean' / relative).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    blob = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
    assert digest == item['sha256'], relative
    assert blob == tracked['lean/' + relative], relative
    assert data == (build / relative).read_bytes(), relative
    entries.append({'path': 'lean/' + relative, 'sha256': digest, 'git_blob': blob})

additional = []
for path in sorted(source.rglob('*')):
    if not path.is_file() or '.git' in path.relative_to(source).parts:
        continue
    rel = path.relative_to(source).as_posix()
    if rel.startswith('lean/OAI/') or rel not in tracked:
        continue
    data = path.read_bytes()
    blob = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
    assert blob == tracked[rel], rel
    additional.append({'path': rel, 'sha256': hashlib.sha256(data).hexdigest(), 'git_blob': blob})

for filename in ['PiExponent.lean', 'PiExponent.json']:
    rel = pathlib.Path('ComparatorChallenges') / filename
    assert (source / 'lean' / rel).read_bytes() == (build / rel).read_bytes(), filename
assert (source / 'lean/lean-toolchain').read_bytes() == (build / 'lean-toolchain').read_bytes()

status = git('status', '--porcelain=v1').decode()
assert not status.strip(), status
result = {
    'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'source_revision': revision,
    'git_status': status,
    'result': 'PASS',
    'proof_source_count': len(entries),
    'proof_sources': entries,
    'additional_preserved_sources': additional,
    'challenge_and_toolchain_copies_match': True,
    'scope': 'Git object bytes, preserved working files, and isolated proof-source copies agree. No claim about mathematical truth is inferred from hashing.'
}
(bench / 'evidence/source-integrity.json').write_text(json.dumps(result, indent=2))
print(f'PASS: {len(entries)} proof files and {len(additional)} additional source artifacts match Git; build proof copies and challenge match; source tree clean.')
