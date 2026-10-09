"""Check local entrances and bind every tracked input to committed Git bytes."""
import hashlib
import re
import subprocess
from urllib.parse import unquote
import verify

ROOT, AREA = verify.ROOT, verify.AREA
FILES = [ROOT/'WORKBENCH.md',ROOT.parent/'WORKBENCH.md',AREA/'RECEIPT_BOOK.md',
         AREA/'CLARIFICATIONS.md',AREA/'WORKING.md',
         ROOT/'workbench/keys/20261008-five-paper-audit/REMAINDER_ACTIVATION.md']
FILES += [AREA/p/'RECEIPT_BOOK.md' for p in ('SCT','CC','GPPR','FA')]
FILES += [ROOT.parent/'Other mathematics'/p/'README.md' for p in
          ('Single Cut Transport','Compactification Costs','GPPR','Finite Abstraction')]
FILES += [AREA/b/'REVIEW.md' for b in verify.MODULES]

def main():
    links, snapshots, bindings = [], [], {}
    for path in FILES:
        content = path.read_text(encoding='utf-8')
        snapshots.append({'path':str(path),'sha256':verify.sha(path),
                          'content':content if not path.is_relative_to(ROOT) else None})
        for match in re.finditer(r'\[[^\]]*\]\((?:<([^>]+)>|([^\)]+))\)',content):
            raw = match.group(1) or match.group(2)
            if raw.startswith(('https://','http://','#')):
                continue
            target = (path.parent/unquote(raw.split('#')[0])).resolve()
            if not target.is_relative_to(ROOT.parent) or (not target.exists() and target != (AREA/'navigation.json').resolve()):
                raise ValueError('Invalid local link: '+str(path)+' -> '+raw)
            links.append({'from':str(path),'link':raw,'target':str(target)})
    for batch in verify.MODULES:
        receipt = verify.read(AREA/batch/'results.json')
        for name, expected in receipt['input_hashes_after'].items():
            path = verify.Path(name)
            if not path.is_relative_to(ROOT):
                continue
            rel = path.relative_to(ROOT).as_posix()
            if not (rel.startswith('Experiments/') or path.is_relative_to(AREA)):
                continue
            if rel in bindings:
                continue
            blob = subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT)
            digest = hashlib.sha256(blob).hexdigest()
            if digest != expected:
                raise ValueError('Committed bytes differ from checked input: '+rel)
            bindings[rel] = digest
    verify.write(AREA/'navigation.json',{
        'status':'PASS_LOCAL_LINKS_AND_GIT_INPUT_BYTES','checked_links':len(links),
        'files':snapshots,'links':links,'checked_git_head':verify.git('rev-parse','HEAD'),
        'committed_input_hashes':bindings,
        'snapshot_note':'Outer guides are outside Git; these dated snapshots preserve the changed navigation, not a second editable copy.'})
    if not all(verify.Path(link['target']).exists() for link in links):
        raise ValueError('A navigation target is missing after writing the self-linked manifest')
    print('PASS_LOCAL_LINKS',len(links),'PASS_COMMITTED_INPUT_BYTES',len(bindings))

if __name__ == '__main__':
    main()
