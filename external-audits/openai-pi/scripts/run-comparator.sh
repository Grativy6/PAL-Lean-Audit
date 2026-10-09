#!/usr/bin/env bash
set -uo pipefail
audit_root=/home/cdpang/math-pi-audit-20261006
bench="/mnt/h/Hearthline's Path/Math Workbench/openai-math-pi-2026-10-06"
attempt="${1:?Supply a new attempt label}"
run_dir="$audit_root/logs/$attempt"
mkdir "$run_dir" || exit 1
cp "$bench/scripts/landrun-with-threads.sh" "$audit_root/tools/landrun-with-threads"
chmod u+x "$audit_root/tools/landrun-with-threads"
export PATH="$audit_root/tools/lean-4.34.1-linux/bin:$PATH"
export COMPARATOR_LANDRUN="$audit_root/tools/landrun-with-threads"
export COMPARATOR_LEAN4EXPORT="$audit_root/tools/comparator/.lake/packages/lean4export/.lake/build/bin/lean4export"
export LEAN_NUM_THREADS=2
cd "$audit_root/project"
date -u +%FT%TZ > "$run_dir/comparator-start.txt"
systemd-run --user --wait --pipe --collect --unit=pi-audit-comparator-20261006 \
  --working-directory="$audit_root/project" \
  --property=RestrictAddressFamilies=~AF_UNIX \
  --property=MemoryMax=11G --property=MemorySwapMax=2G --property=CPUQuota=400% \
  --setenv="PATH=$PATH" --setenv="LEAN_NUM_THREADS=2" \
  --setenv="COMPARATOR_LANDRUN=$COMPARATOR_LANDRUN" \
  --setenv="COMPARATOR_LEAN4EXPORT=$COMPARATOR_LEAN4EXPORT" \
  "$audit_root/tools/lean-4.34.1-linux/bin/lake" env \
  "$audit_root/tools/comparator/.lake/build/bin/comparator" ComparatorChallenges/PiExponent.json \
  2>&1 | tee "$run_dir/comparator-run.log"
result=${PIPESTATUS[0]}
printf '%s\n' "$result" > "$run_dir/comparator-exit.txt"
date -u +%FT%TZ > "$run_dir/comparator-end.txt"
mkdir -p "$bench/evidence/$attempt"
cp "$run_dir/"*.txt "$run_dir/"*.log "$bench/evidence/$attempt/"
exit "$result"
