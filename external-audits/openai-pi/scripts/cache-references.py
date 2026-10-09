"""Retain the public reference PDFs used in this bounded local audit."""
import json
import pathlib
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

from pypdf import PdfReader

bench = pathlib.Path(__file__).resolve().parents[1]
helper = pathlib.Path(r'C:\Users\cdpan\.codex\plugins\cache\openai-curated-remote\mathbox\3.2.0\skills\literature-check\scripts\literature_cache.py')
temp = bench / 'tmp' / 'pdfs'
temp.mkdir(parents=True, exist_ok=True)
references = [
    ('meiburg-2208.13356v1', 'arxiv:2208.13356v1',
     'Bounds on Irrationality Measures and the Flint-Hills Series', 'v1',
     'https://arxiv.org/pdf/2208.13356v1'),
    ('alekseyev-1104.5100v1', 'arxiv:1104.5100v1',
     'On convergence of the Flint Hills series', 'v1',
     'https://arxiv.org/pdf/1104.5100v1'),
    ('mondal-1806.05346v5', 'arxiv:1806.05346v5',
     'How many zeroes? Counting the number of solutions of systems of polynomials via geometry at infinity (Draft III)', 'v5',
     'https://arxiv.org/pdf/1806.05346v5'),
    ('lazarsfeld-positivity-chapter1', 'url:https://www.math.stonybrook.edu/robert.lazarsfeld/Reprints/Laz.PAG.Chapt1.pdf',
     'Positivity in Algebraic Geometry I - Chapter 1 author reprint', 'author-reprint',
     'https://www.math.stonybrook.edu/robert.lazarsfeld/Reprints/Laz.PAG.Chapt1.pdf'),
]

def cache(*args):
    result = subprocess.run([sys.executable, str(helper), *args],
                            text=True, encoding='utf-8', capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return json.loads(result.stdout)

receipts = []
for slug, identifier, title, version, url in references:
    existing = cache('find', '--root', str(bench), '--id', identifier, '--format', 'json')
    if existing.get('count', 0):
        receipts.append({'id': identifier, 'lookup': existing, 'reused': True})
        print(f'Reused {identifier}', flush=True)
        continue
    pdf = temp / (slug + '.pdf')
    request = urllib.request.Request(url, headers={'User-Agent': 'Local mathematical source audit'})
    with urllib.request.urlopen(request, timeout=90) as response:
        data = response.read()
    if not data.startswith(b'%PDF-'):
        raise ValueError(f'Expected PDF bytes from {url}')
    pdf.write_bytes(data)
    reader = PdfReader(pdf)
    text_path = temp / (slug + '.txt')
    text_path.write_text('\n\n'.join(f'--- PDF page {i + 1} ---\n' + (page.extract_text() or '')
                                     for i, page in enumerate(reader.pages)), encoding='utf-8')
    added = cache('add', '--root', str(bench), '--pdf', str(pdf), '--id', identifier,
                  '--title', title, '--version', version, '--source-url', url,
                  '--date-checked', '2026-10-07', '--retention-basis',
                  'Chris authorized a source-grounded local proof audit and retaining its sources and receipts on this dedicated workbench.',
                  '--text', str(text_path), '--text-tool', 'pypdf extract_text, page-marked',
                  '--format', 'json')
    receipts.append({'id': identifier, 'lookup': existing, 'retained': added, 'pages': len(reader.pages)})
    print(f'Retained {identifier}: {len(reader.pages)} pages', flush=True)

verification = cache('verify', '--root', str(bench), '--format', 'json')
(bench / 'evidence' / 'retained-reference-receipts.json').write_text(
    json.dumps({'checked_at_utc': datetime.now(timezone.utc).isoformat(),
                'references': receipts, 'verification': verification}, indent=2), encoding='utf-8')
print(json.dumps(verification, indent=2))
