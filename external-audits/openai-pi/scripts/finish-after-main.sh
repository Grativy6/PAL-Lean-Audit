#!/usr/bin/env bash
set -euo pipefail
audit_root=/home/cdpang/math-pi-audit-20261006
bench="/mnt/h/Hearthline's Path/Math Workbench/openai-math-pi-2026-10-06"
attempt="${1:?Supply the running main attempt label}"
exit_file="$audit_root/logs/$attempt/comparator-exit.txt"
while [ ! -f "$exit_file" ]; do
  sleep 15
done
main_result="$(cat "$exit_file")"
if [ "$main_result" = 0 ]; then
  set +e
  bash "$bench/scripts/run-supplement.sh" "$attempt"
  supplement_result=$?
  set -e
else
  supplement_result=1
  printf 'Main check exited %s; supplementary proof checks were not started.\n' "$main_result"
fi
python3 "$bench/scripts/verify-integrity.py"
python3 "$bench/scripts/collect-receipts.py"
if [ "$main_result" != 0 ]; then
  exit "$main_result"
fi
exit "$supplement_result"
