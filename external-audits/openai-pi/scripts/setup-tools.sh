#!/usr/bin/env bash
set -euo pipefail
audit_root=/home/cdpang/math-pi-audit-20261006
mkdir -p "$audit_root/downloads" "$audit_root/tools" "$audit_root/logs"
cd "$audit_root"
curl --fail --location --silent --show-error --retry 2 \
  https://github.com/leanprover/lean4/releases/download/v4.34.1/lean-4.34.1-linux.tar.zst \
  --output downloads/lean-4.34.1-linux.tar.zst
printf '%s\n' '47bf4bbd78f70c2e9670598ab7124d92b6efb7330ff33e5fbb4030f6fd72e4e4  downloads/lean-4.34.1-linux.tar.zst' | sha256sum --check
python3 - <<'PY'
import pathlib, tarfile
root=pathlib.Path('/home/cdpang/math-pi-audit-20261006')
with tarfile.open(root/'downloads/lean-4.34.1-linux.tar.zst', 'r:zst') as archive:
    archive.extractall(root/'tools', filter='data')
PY
tools/lean-4.34.1-linux/bin/lean --version
curl --fail --location --silent --show-error --retry 2 \
  https://go.dev/dl/go1.27.1.linux-amd64.tar.gz \
  --output downloads/go1.27.1.linux-amd64.tar.gz
printf '%s\n' '63d339f0da5ab53635a56f2490a7984dfe12dfcff22ad749f63edaf590168445  downloads/go1.27.1.linux-amd64.tar.gz' | sha256sum --check
tar -xzf downloads/go1.27.1.linux-amd64.tar.gz -C tools
tools/go/bin/go version
git clone https://github.com/leanprover/comparator.git tools/comparator
git -C tools/comparator checkout --detach ca04cfc72b550331658ec314bf47685281bfd4bf
git clone https://github.com/Zouuup/landrun.git tools/landrun
git -C tools/landrun checkout --detach 811cfff51ceaf3d9843708aa6d22e9b84ccac8b4
printf '%s\n' 'Public tool acquisition complete; comparator compatibility still to inspect.'
