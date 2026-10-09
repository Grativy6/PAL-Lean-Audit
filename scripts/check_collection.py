"""Verify imported bytes, navigation, and the retained external-audit ceilings."""
from pathlib import Path
import hashlib,json,re,subprocess,urllib.parse
ROOT=Path(__file__).resolve().parents[1]
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

for p in sorted((ROOT/'provenance/imports').glob('*.json')):
    entry=read(p)
    for row in entry['files']:
        target=ROOT/entry['prefix']/row['path']
        if sha(target)!=row['sha256']:raise ValueError('Imported blob changed: '+str(target))
    subprocess.run(['git','merge-base','--is-ancestor',entry['original_commit'],'HEAD'],cwd=ROOT,check=True)
    print('PASS imported bytes and ancestry:',entry['prefix'])

for p in sorted((ROOT/'external-audits').glob('*/MIGRATION.json')):
    record=read(p)
    for row in record['files']:
        target=p.parent/row['path']
        if target.stat().st_size!=row['bytes'] or sha(target)!=row['sha256']:raise ValueError('External receipt/source changed: '+str(target))
    if p.parent.name=='openai-snaky':
        r=read(p.parent/'evidence/verification-results.json')
        if r['formal_status']!='PARTIAL_RESOURCE' or r['formal_kernel_replay_passed'] or r['formal_comparator_acceptance']:
            raise ValueError('Partial Snaky record was promoted')
    if p.parent.name=='openai-pi':
        r=read(p.parent/'evidence/verification-results.json')
        if r['main_formal_check']!='PASS' or r['source_integrity']['proof_source_count']!=869:
            raise ValueError('Retained pi receipt differs')
    if p.parent.name=='openai-fourier' and record['status']!='READING_AND_CONSTANTS_ONLY':raise ValueError('Fourier status promoted')
    print('PASS selected external bytes; retained status:',record['status'])

navigation=[ROOT/'papers/INDEX.md',ROOT/'REPRODUCE.md',ROOT/'LICENSE_SCOPE.md',
            *sorted((ROOT/'papers').glob('*/README.md'))]
errors=[];count=0
for p in navigation:
    for raw in re.findall(r'\]\((?:<([^>]+)>|([^\s)]+))(?:\s+"[^"]*")?\)',p.read_text(encoding='utf-8')):
        link=raw[0] or raw[1]
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',link) or link.startswith('#'):continue
        target=(p.parent/urllib.parse.unquote(link.split('#',1)[0])).resolve()
        if not target.is_relative_to(ROOT) or not target.exists():errors.append((str(p.relative_to(ROOT)),link))
        count+=1
if errors:raise ValueError('Broken current navigation: '+repr(errors))
print('PASS current navigation:',count,'relative links')
print('Source-document replay and historical local-only links are separately scoped; this is not mathematical certification.')
