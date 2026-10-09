"""Check and retain the local entrances changed by this workshop."""
import re
import hashlib
import subprocess
from urllib.parse import unquote
import verify

ROOT, AREA = verify.ROOT, verify.AREA
FILES = [ROOT / "WORKBENCH.md", ROOT.parent / "WORKBENCH.md",
         ROOT.parent / "Other mathematics/Abstract Loops/README.md",
         AREA / "RECEIPT_BOOK.md", AREA / "REVIEW.md", AREA / "CLARIFICATIONS.md",
         ROOT / "workbench/keys/20261008-five-paper-audit/ABSTRACT_LOOPS_ACTIVATION.md"]

def main():
    links, snapshots = [], []
    for path in FILES:
        text = path.read_text(encoding="utf-8")
        snapshots.append({"path": str(path), "sha256": verify.sha(path),
                          "content": text if not path.is_relative_to(ROOT) else None})
        for match in re.finditer(r"\[[^\]]*\]\((?:<([^>]+)>|([^\)]+))\)", text):
            raw = match.group(1) or match.group(2)
            if raw.startswith(("https://", "http://", "#")):
                continue
            target = (path.parent / unquote(raw.split("#")[0])).resolve()
            if not target.is_relative_to(ROOT.parent):
                raise ValueError("Navigation leaves the personal math home: " + raw)
            if not target.exists():
                raise ValueError("Broken local link in " + str(path) + ": " + raw)
            links.append({"from": str(path), "link": raw, "target": str(target)})
    bindings = {}
    for batch in verify.MODULES:
        receipt = verify.read(AREA / batch / "results.json")
        for name, expected in receipt["input_hashes_after"].items():
            path = verify.Path(name)
            if not path.is_relative_to(ROOT):
                continue
            rel = path.relative_to(ROOT).as_posix()
            if not (rel.startswith("Experiments/AbstractLoops") or path.is_relative_to(AREA)):
                continue
            blob = subprocess.check_output(["git", "show", "HEAD:" + rel], cwd=ROOT)
            digest = hashlib.sha256(blob).hexdigest()
            if digest != expected:
                raise ValueError("Committed bytes differ from checked input: " + rel)
            bindings[rel] = digest
    verify.write(AREA / "navigation.json", {"status": "PASS_LOCAL_LINKS_AND_GIT_INPUT_BYTES",
        "checked_links": len(links), "files": snapshots, "links": links,
        "checked_git_head": verify.git("rev-parse", "HEAD"), "committed_input_hashes": bindings,
        "snapshot_note": "Outer shelf guides are outside Git; content is retained here as a dated evidence snapshot, not another editable guide."})
    print("PASS_LOCAL_LINKS", len(links), "PASS_COMMITTED_INPUT_BYTES", len(bindings))

if __name__ == "__main__":
    main()
