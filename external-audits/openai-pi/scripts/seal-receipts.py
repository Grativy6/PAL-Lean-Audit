"""Write and immediately verify checksums for this audit's final documents and receipts."""
import hashlib
import json
from pathlib import Path

bench = Path(__file__).resolve().parents[1]
results = json.loads((bench / 'evidence/verification-results.json').read_text(encoding='utf-8'))
files = [bench / 'README.md', bench / 'AUDIT.md']
for name in ('scripts', 'evidence'):
    files.extend(path for path in (bench / name).rglob('*')
                 if path.is_file() and '__pycache__' not in path.parts)

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

lines = [f'{digest(path)}  {path.relative_to(bench).as_posix()}'
         for path in sorted(files)]
manifest = bench / 'SHA256SUMS'
manifest.write_text('\n'.join(lines) + '\n', encoding='utf-8')
for line in manifest.read_text(encoding='utf-8').splitlines():
    expected, relative = line.split('  ', 1)
    path = (bench / relative).resolve()
    assert path.is_relative_to(bench.resolve()), relative
    assert digest(path) == expected, relative
print(f'PASS: {len(lines)} document, script, and receipt checksums verified.')
print(f"Recorded main proof status: {results['main_formal_check']}")
