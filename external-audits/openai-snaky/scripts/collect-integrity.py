"""Read-only checks of source, build copies, reused dependency pins and tool identity."""
import hashlib
import json
import pathlib
import re
import subprocess

bench = pathlib.Path("/mnt/h/Hearthline's Path/Math Workbench/openai-math-snaky-2026-10-07")
build = pathlib.Path('/home/cdpang/math-snaky-audit-20261007/project')
source = json.loads((bench/'evidence/source-manifest.json').read_text())
build_record = json.loads((bench/'evidence/build-source-manifest.json').read_text())
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
for row in source['files']:
    data=(bench/'source'/row['path']).read_bytes()
    assert len(data)==row['bytes']
    assert hashlib.sha256(data).hexdigest()==row['sha256'], row['path']
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob']
for row in build_record['files']:
    assert sha(build/row['path'])==row['sha256'], row['path']
for name,row in build_record['tools'].items():
    assert sha(pathlib.Path(row['path']))==row['sha256'], name
deps=[]
for row in json.loads((build/'lake-manifest.json').read_text())['packages']:
    name=row['name']
    directory=build/'.lake/packages'/name
    actual=subprocess.check_output(['git','-C',str(directory),'rev-parse','HEAD'],text=True).strip()
    diff=subprocess.run(['git','-C',str(directory),'diff','--quiet','HEAD','--'])
    assert actual==row['rev'] and diff.returncode==0, name
    deps.append({'name':name,'revision':actual,'tracked_changes':False})
paths=(bench/'evidence/proof-module-paths.txt').read_text().splitlines()
pattern=re.compile(r'\b(?:sorry|admit|native_decide|run_elab|run_cmd|implemented_by)\b|(?m:^\s*(?:axiom|unsafe|#eval|#exec)\b)|\bIO\.Process\b')
hits=[]
for relative in paths:
    text=(bench/'source'/relative).read_text()
    for number,line in enumerate(text.splitlines(),1):
        if pattern.search(line):
            hits.append({'file':relative,'line':number,'text':line})
record={'status':'PASS','source_files_checked':len(source['files']),
        'build_files_checked':len(build_record['files']),
        'tool_files_checked':len(build_record['tools']),'dependencies':deps,
        'solution_modules_scanned':len(paths),'textual_scan_hits':hits,
        'scan_limit':'A textual screening pass, not a proof-term or kernel check.',
        'no_tracked_proof_changes':True}
assert not hits,hits
(bench/'evidence/integrity-results.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='dependencies'},indent=2))
