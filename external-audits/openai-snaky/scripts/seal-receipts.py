"""Hash the retained Snaky entry, leaving rendering scratch outside the seal."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
summary=json.loads((root/'evidence/verification-results.json').read_text())
assert summary['finite_status']=='PASS'
assert summary['formal_status']=='PARTIAL_RESOURCE'
assert summary['formal_compiled_modules']==83 and summary['formal_required_modules']==94
assert not summary['formal_kernel_replay_passed']
assert 'formal check is unfinished' in (root/'evidence/book-text.txt').read_text(encoding='utf-8').lower()
for name in ['README.md','AUDIT.md']:
    text=(root/name).read_text(encoding='utf-8')
    assert 'PARTIAL_RESOURCE' in text
    assert 'Pending at this draft' not in text
entries=[]
for path in sorted(root.rglob('*')):
    relative=path.relative_to(root)
    if not path.is_file() or path.is_symlink() or relative.parts[0]=='tmp':
        continue
    if '__pycache__' in relative.parts or relative.as_posix()=='SHA256SUMS':
        continue
    entries.append((hashlib.sha256(path.read_bytes()).hexdigest(),relative.as_posix()))
seal=root/'SHA256SUMS'
seal.write_text(''.join(f'{digest}  {name}\n' for digest,name in entries),encoding='utf-8')
for line in seal.read_text(encoding='utf-8').splitlines():
    digest,name=line.split('  ',1)
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,name
print(json.dumps({'status':'SEALED_AND_RECHECKED','files':len(entries),'seal':str(seal),'formal_status':summary['formal_status']},indent=2))
