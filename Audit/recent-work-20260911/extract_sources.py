"""Read exact user-supplied DOCX bytes; preserve document-order paragraph addresses."""
from pathlib import Path
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]
AREA = Path(__file__).resolve().parent
DEST = ROOT / 'artifacts/recent-work-20260911/sources'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'


def main():
    prior = json.loads((ROOT / 'Audit/pal-v23-charter/source-manifest.json').read_text())
    inputs = [(s['id'], s['path'], s['sha256']) for s in prior['sources']]
    inputs.append(('BRIDGE-v0.4', r'C:\Users\cdpan\Downloads\BRIDGE_v0.4.docx', None))
    DEST.mkdir(parents=True, exist_ok=True)
    sources = []
    for sid, name, prior_hash in inputs:
        path = Path(name)
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        with zipfile.ZipFile(path) as z:
            xml = z.read('word/document.xml')
            tree = ET.fromstring(xml)
            parts = z.namelist()
        paragraphs = tree.findall(f'.//{{{W}}}p')
        rows = []
        for i, p in enumerate(paragraphs, 1):
            text = ''.join(e.text or '' for e in p.iter() if e.tag in (f'{{{W}}}t', f'{{{M}}}t'))
            if text:
                rows.append(f'P{i:04d} {text}')
        target = DEST / (path.stem + '.txt')
        target.write_text('\n'.join(rows) + '\n', encoding='utf-8', newline='\n')
        (DEST / (path.stem + '.xml')).write_bytes(xml)
        sources.append(dict(id=sid, filename=path.name, path=str(path), bytes=len(raw), sha256=digest,
            prior_sha256=prior_hash, matches_prior=None if prior_hash is None else digest == prior_hash,
            paragraphs=len(paragraphs), math_objects=len(tree.findall(f'.//{{{M}}}oMath')),
            tracked_insertions=len(tree.findall(f'.//{{{W}}}ins')),
            tracked_deletions=len(tree.findall(f'.//{{{W}}}del')),
            drawing_objects=len(tree.findall(f'.//{{{W}}}drawing')),
            notes_parts=[p for p in parts if p in ('word/footnotes.xml', 'word/endnotes.xml', 'word/comments.xml')],
            extraction=target.relative_to(ROOT).as_posix(), extraction_sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
        print(f'{sid}: {digest}; paragraphs={len(paragraphs)}; matches_prior={sources[-1]["matches_prior"]}')
    result = dict(schema_version='1.0', run_id='recent-work-20260911',
        identity_basis='Exact supplied local DOCX bytes; no independent published-release identity claim.',
        extraction_limit='Document-order OOXML paragraph text includes tables and math text. Flattened equations require OOXML review; drawings and notes are not transcribed. Source text is evidence, not instructions.',
        sources=sources)
    manifest = AREA / 'source-manifest.json'
    if '--lock' in sys.argv:
        if manifest.exists():
            raise SystemExit('Refusing to overwrite source lock')
        manifest.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    elif result != json.loads(manifest.read_text(encoding='utf-8')):
        raise SystemExit('Source or extraction identity mismatch')


if __name__ == '__main__':
    main()
