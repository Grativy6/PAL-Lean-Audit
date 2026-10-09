#!/usr/bin/env bash
set -euo pipefail
audit_root=/home/cdpang/math-pi-audit-20261006
export PATH="$audit_root/tools/lean-4.34.1-linux/bin:$audit_root/tools/go/bin:$PATH"
export GOPATH="$audit_root/go-work"
export GOCACHE="$audit_root/go-cache"
export LEAN_NUM_THREADS=4
cd "$audit_root/tools/landrun"
go build -trimpath -o "$audit_root/tools/landrun-bin" ./cmd/landrun 2>&1 | tee "$audit_root/logs/landrun-build.log"
"$audit_root/tools/landrun-bin" --version
cd "$audit_root/tools/comparator"
git checkout --detach d03acab154d269c06e60e4de7e4cc85deebff94b
# This is the comparator revision for the Lean 4.34 series. Compile it with
# the manuscript's exact 4.34.1 toolchain; retain this harness-only change.
printf '%s\n' leanprover/lean4:v4.34.1 > lean-toolchain
lake build comparator lean4export 2>&1 | tee "$audit_root/logs/comparator-build.log"
git diff -- lean-toolchain > "$audit_root/logs/comparator-toolchain.diff"
git rev-parse HEAD > "$audit_root/logs/comparator-revision.txt"
cat lake-manifest.json > "$audit_root/logs/comparator-manifest.json"
