#!/usr/bin/env python3
"""Hash-check and extract supplied DOCX text for source review; never edit DOCX.

Paragraph addresses refer to OOXML document-order w:p elements. Mathematical
runs are retained but flattened, so fractions/superscripts require inspection
of the original OOXML before formal translation. Images are not transcribed.
"""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'Audit/pal-v23-charter/source-manifest.json'
DEST = ROOT / 'artifacts/pal-v23-charter-2026-09-07/sources'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    sources = json.loads(MANIFEST.read_text(encoding='utf-8'))['sources']
    for source in sources:
        path = Path(source['path'])
        raw = path.read_bytes()
        if len(raw) != source['bytes'] or hashlib.sha256(raw).hexdigest() != source['sha256']:
            raise ValueError(f'Source identity mismatch: {source["id"]}')
        with zipfile.ZipFile(path) as archive:
            document = ET.fromstring(archive.read('word/document.xml'))
        rows = []
        for index, paragraph in enumerate(document.findall(f'.//{{{W}}}p'), 1):
            text = ''.join(t.text or '' for t in paragraph.iter() if t.tag in (f'{{{W}}}t', f'{{{M}}}t'))
            if text:
                rows.append(f'P{index:04d} {text}')
        (DEST / (path.stem + '.txt')).write_text('\n'.join(rows) + '\n', encoding='utf-8', newline='\n')
        print(f'{source["id"]}: hash matched; {len(rows)} nonempty paragraphs')


if __name__ == '__main__':
    main()
