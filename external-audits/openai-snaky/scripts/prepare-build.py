"""Prepare a separate Lean project; reuse the existing pinned tool/dependency cache."""
import hashlib
import json
import pathlib
import shutil
import subprocess

bench = pathlib.Path("/mnt/h/Hearthline's Path/Math Workbench/openai-math-snaky-2026-10-07")
prior = pathlib.Path('/home/cdpang/math-pi-audit-20261006')
audit = pathlib.Path('/home/cdpang/math-snaky-audit-20261007')
build = audit / 'project'
assert not audit.exists(), 'Preserve previous attempts'
source = bench / 'source/lean'
pin = 'd13f23b723b8a846827a245b89c10fc7d3f11612'
packages = prior / 'project/.lake/packages'
assert subprocess.check_output(['git', '-C', str(packages/'mathlib'), 'rev-parse', 'HEAD'], text=True).strip() == pin
locked = json.loads((prior/'project/lake-manifest.json').read_text())
assert next(p['rev'] for p in locked['packages'] if p['name'] == 'mathlib') == pin
assert shutil.disk_usage(prior).free > 5_000_000_000
build.mkdir(parents=True)
records = []
paths = (bench/'evidence/proof-module-paths.txt').read_text().splitlines()
paths += ['lean/ComparatorChallenges/SnakyTwentyOne.lean', 'lean/ComparatorChallenges/SnakyTwentyOne.json', 'lean/lean-toolchain']
for item in paths:
    relative = pathlib.PurePosixPath(item).relative_to('lean')
    src, dst = source/relative, build/relative
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    data = src.read_bytes()
    assert dst.read_bytes() == data
    records.append({'path':str(relative), 'bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest()})
(build/'lakefile.lean').write_text('''import Lake
open System Lake DSL
package OAI where
  version := v!"0.1.0"
  fixedToolchain := true
  leanOptions := #[⟨`autoImplicit, false⟩]
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"
lean_lib OAI
lean_lib ComparatorChallenges where
  roots := #[`ComparatorChallenges.SnakyTwentyOne]
''')
(build/'.lake').mkdir()
(build/'.lake/packages').symlink_to(packages, target_is_directory=True)
shutil.copyfile(prior/'project/lake-manifest.json', build/'lake-manifest.json')
(audit/'logs').mkdir()
tools = {
 'lean':prior/'tools/lean-4.34.1-linux/bin/lean',
 'lake':prior/'tools/lean-4.34.1-linux/bin/lake',
 'comparator':prior/'tools/comparator/.lake/build/bin/comparator',
 'lean4export':prior/'tools/comparator/.lake/packages/lean4export/.lake/build/bin/lean4export',
 'landrun':prior/'tools/landrun-bin',
 'landrun_wrapper':prior/'tools/landrun-with-threads',
}
versions = {}
for name, path in tools.items():
    data = path.read_bytes()
    versions[name] = {'path':str(path),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
for name in ['lean','lake']:
    versions[name]['version'] = subprocess.check_output([str(tools[name]),'--version'], text=True).strip()
record = {
 'source_revision':'adc7f1241b42e322a6451854ab7e4b4c146bf78a',
 'build_root':str(build), 'mathlib_revision':pin,
 'proof_changes':False,
 'configuration_change':'Narrow Lake configuration to SnakyTwentyOne and the same pinned Mathlib dependency; reuse existing dependency cache via symlink.',
 'trust_limit':'Reused precompiled Mathlib/toolchain cache; this run does not independently bootstrap those dependencies.',
 'files':records, 'tools':versions,
}
(bench/'evidence/build-source-manifest.json').write_text(json.dumps(record,indent=2)+'\n')
shutil.copyfile(build/'lakefile.lean',bench/'evidence/isolated-lakefile.lean')
shutil.copyfile(build/'lake-manifest.json',bench/'evidence/isolated-lake-manifest.json')
print(json.dumps({'status':'PREPARED','files':len(records),'proof_modules':len(paths)-3,'build_root':str(build),'tool_versions':{k:versions[k]['version'] for k in ['lean','lake']}},indent=2))
