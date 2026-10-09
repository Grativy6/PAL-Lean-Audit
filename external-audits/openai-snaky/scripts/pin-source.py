"""Pin one public Snaky manuscript and its exact OAI Lean import closure."""
import hashlib, json, os, pathlib, re, subprocess, time
BENCH = pathlib.Path(__file__).resolve().parents[1]
REPO = BENCH.parent / "openai-math-pi-2026-10-06" / "source"
PIN = "adc7f1241b42e322a6451854ab7e4b4c146bf78a"
PAPER = "preprints/Snaky-in-21-Maker-moves-September-25-2026/"
START = time.monotonic()
GIT = r"C:\Program Files\Git\mingw64\bin\git.exe"
def git(*args):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    return subprocess.run([GIT, "-C", str(REPO), *args], check=True, capture_output=True, timeout=120, env=env).stdout
assert git("rev-parse", "HEAD").decode().strip() == PIN
assert not git("status", "--porcelain", "--untracked-files=no").strip()
tree = {}
print("Reading tree names without fetching unrelated blob sizes", flush=True)
for line in git("ls-tree", "-r", PIN).decode().splitlines():
    meta, path = line.split("\t",1)
    mode, kind, oid = meta.split()
    if kind == "blob": tree[path] = {"mode":mode,"git_blob":oid}
blobs = {}
def read(path):
    assert path in tree, path
    if path not in blobs:
        data = git("show", f"{PIN}:{path}")
        tree[path]["bytes"] = len(data)
        actual = hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        assert actual == tree[path]["git_blob"], path
        blobs[path] = data
        assert sum(map(len, blobs.values())) < 50_000_000
    return blobs[path]
proofs, pending, external = set(), ["OAI.GameTheory.SnakyTwentyOne.Main"], set()
while pending:
    module = pending.pop()
    path = "lean/"+module.replace(".","/")+".lean"
    if path in proofs: continue
    proofs.add(path)
    if len(proofs) % 25 == 0: print(f"Reading proof module {len(proofs)}: {module}", flush=True)
    text = read(path).decode("utf-8")
    for line in re.findall(r"(?m)^import\s+([^\n]+)",text):
        for dep in line.split("--",1)[0].split():
            if dep.startswith("OAI."): pending.append(dep)
            else: external.add(dep)
selected = set(proofs)
selected.update(p for p in tree if p.startswith(PAPER))
selected.update(["README.md","LICENSE","lean/README.md","lean/lean-toolchain","lean/lakefile.lean","lean/lake-manifest.json","lean/docs/187.md","lean/ComparatorChallenges/README.md","lean/ComparatorChallenges/SnakyTwentyOne.lean","lean/ComparatorChallenges/SnakyTwentyOne.json"])
assert not any(p.endswith("AGENTS.md") for p in tree), "Check repository instructions before export"
print(f"Selected {len(selected)} files; reading only those blobs", flush=True)
planned = sum(len(read(p)) for p in selected)
assert planned < 50_000_000, planned
total = count = 0
print("Counting shelf storage, including long Windows paths", flush=True)
for directory, dirs, files in os.walk("\\\\?\\" + str(BENCH.parent.parent), followlinks=False):
    dirs[:] = [d for d in dirs if not pathlib.Path(directory,d).is_symlink()]
    for name in files:
        path = pathlib.Path(directory,name)
        if not path.is_symlink():
            total += path.stat().st_size
            count += 1
assert total + planned < 500_000_000_000
dest = BENCH/"source"
assert not dest.exists(), "Preserve existing export"
entries=[]
for p in sorted(selected):
    data=read(p)
    output=dest/pathlib.PurePosixPath(p)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    assert output.read_bytes()==data
    entries.append({"path":p,**tree[p],"sha256":hashlib.sha256(data).hexdigest()})
(BENCH/"evidence").mkdir(exist_ok=True)
record={
 "status":"PINNED_SOURCE_EXPORTED","repository":"https://github.com/openai/math","revision":PIN,
 "selected_files":len(entries),"source_bytes":planned,"proof_modules":len(proofs),
 "proof_lines":sum(read(p).count(b"\n") for p in proofs),"external_imports":sorted(external),
 "paper_prefix":PAPER,"target":"OAI.SnakyPrototype.snaky_winning_strategy_21_with_legal_states",
 "source_checkout_tracked_changes":False,"git_blobs_verified":True,
 "storage_before":{"root":str(BENCH.parent.parent),"logical_bytes":total,"files":count,"ceiling_bytes":500_000_000_000},
 "elapsed_seconds":time.monotonic()-START,"files":entries
}
(BENCH/"evidence/source-manifest.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
(BENCH/"evidence/proof-module-paths.txt").write_text("\n".join(sorted(proofs))+"\n",encoding="utf-8")
print(json.dumps({k:v for k,v in record.items() if k not in ["files","external_imports"]},indent=2))
