#!/usr/bin/env bash
set -uo pipefail
audit=/home/cdpang/math-snaky-audit-20261007
prior=/home/cdpang/math-pi-audit-20261006
bench="/mnt/h/Hearthline's Path/Math Workbench/openai-math-snaky-2026-10-07"
run="$audit/logs/comparator-001"
mkdir "$run" || exit 1
export PATH="$prior/tools/lean-4.34.1-linux/bin:$PATH"
export COMPARATOR_LANDRUN="$prior/tools/landrun-with-threads"
export COMPARATOR_LEAN4EXPORT="$prior/tools/comparator/.lake/packages/lean4export/.lake/build/bin/lean4export"
export LEAN_NUM_THREADS=2
cd "$audit/project" || exit 1
date -u +%FT%TZ > "$run/start.txt"
systemd-run --user --wait --pipe --collect --unit=snaky-audit-comparator-20261007 \
 --working-directory="$audit/project" \
 --property=RestrictAddressFamilies=~AF_UNIX \
 --property=MemoryMax=8G --property=MemorySwapMax=1G --property=CPUQuota=200% \
 --property=RuntimeMaxSec=1800 --property=TimeoutStopSec=20 \
 --setenv="PATH=$PATH" --setenv="LEAN_NUM_THREADS=2" \
 --setenv="COMPARATOR_LANDRUN=$COMPARATOR_LANDRUN" \
 --setenv="COMPARATOR_LEAN4EXPORT=$COMPARATOR_LEAN4EXPORT" \
 "$prior/tools/lean-4.34.1-linux/bin/lake" env \
 "$prior/tools/comparator/.lake/build/bin/comparator" ComparatorChallenges/SnakyTwentyOne.json \
 2>&1 | tee "$run/run.log"
result=${PIPESTATUS[0]}
printf '%s\n' "$result" > "$run/exit.txt"
date -u +%FT%TZ > "$run/end.txt"
mkdir -p "$bench/evidence/comparator-001"
cp "$run/"*.txt "$run/"*.log "$bench/evidence/comparator-001/"
exit "$result"
