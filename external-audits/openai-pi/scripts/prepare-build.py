import hashlib
import json
import pathlib
import shutil

bench = pathlib.Path("/mnt/h/Hearthline's Path/Math Workbench/openai-math-pi-2026-10-06")
source = bench / "source"
audit = pathlib.Path('/home/cdpang/math-pi-audit-20261006')
build = audit / 'project'
build.mkdir(parents=True, exist_ok=True)
original = source / 'lean/OAI/NumberTheory/PiExponent'
destination = build / 'OAI/NumberTheory/PiExponent'
shutil.copytree(original, destination, dirs_exist_ok=True)
(build / 'ComparatorChallenges').mkdir(exist_ok=True)
for name in ['PiExponent.lean', 'PiExponent.json']:
    shutil.copyfile(source / 'lean/ComparatorChallenges' / name, build / 'ComparatorChallenges' / name)
shutil.copyfile(source / 'lean/lean-toolchain', build / 'lean-toolchain')
(build / 'lakefile.lean').write_text('''import Lake
open System Lake DSL
package OAI where
  version := v!"0.1.0"
  fixedToolchain := true
  leanOptions := #[⟨`autoImplicit, false⟩]
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "d13f23b723b8a846827a245b89c10fc7d3f11612"
lean_lib OAI
lean_lib ComparatorChallenges where
  roots := #[`ComparatorChallenges.PiExponent]
''', encoding='utf-8')
manifest = []
for src in sorted(original.rglob('*.lean')):
    rel = src.relative_to(source / 'lean')
    a, b = src.read_bytes(), (build / rel).read_bytes()
    assert a == b, rel
    manifest.append({'path': rel.as_posix(), 'bytes': len(a), 'sha256': hashlib.sha256(a).hexdigest()})
(bench / 'evidence').mkdir(exist_ok=True)
(bench / 'evidence/build-source-manifest.json').write_text(json.dumps({
    'source_revision': 'adc7f1241b42e322a6451854ab7e4b4c146bf78a',
    'toolchain': 'leanprover/lean4:v4.34.1',
    'mathlib_revision': 'd13f23b723b8a846827a245b89c10fc7d3f11612',
    'build_root': str(build),
    'change': 'Only the Lake configuration is narrowed to the exact import closure and pinned Mathlib. No proof source changed.',
    'files': manifest,
}, indent=2), encoding='utf-8')
shutil.copyfile(build / 'lakefile.lean', bench / 'evidence/isolated-lakefile.lean')
print(f'Copied and verified {len(manifest)} unmodified proof source files.')
