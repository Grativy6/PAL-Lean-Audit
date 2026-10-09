#!/usr/bin/env bash
set -euo pipefail
audit_root=/home/cdpang/math-pi-audit-20261006
bench="/mnt/h/Hearthline's Path/Math Workbench/openai-math-pi-2026-10-06"
main_attempt="${1:?Supply the completed main Comparator attempt label}"
test "$(cat "$audit_root/logs/$main_attempt/comparator-exit.txt")" = 0
run_dir="$audit_root/logs/supplement"
mkdir "$run_dir"
mkdir -p "$audit_root/project/ComparatorChallenges/PiExponent"
cp "$bench/scripts/FlintHillsChallenge.lean" "$audit_root/project/ComparatorChallenges/PiExponent/FlintHills.lean"
cp "$bench/scripts/AxiomAudit.lean" "$audit_root/AxiomAudit.lean"
cat > "$audit_root/project/ComparatorChallenges/PiExponent/FlintHills.json" <<'JSON'
{
  "challenge_module": "ComparatorChallenges.PiExponent.FlintHills",
  "solution_module": "OAI.NumberTheory.PiExponent.Main",
  "theorem_names": ["OAI.PiExponent.flint_hills_summable"],
  "definition_names": [],
  "permitted_axioms": ["propext", "Quot.sound", "Classical.choice"],
  "enable_nanoda": false
}
JSON
export PATH="$audit_root/tools/lean-4.34.1-linux/bin:/usr/bin:/bin"
export LEAN_NUM_THREADS=2
export COMPARATOR_LANDRUN="$audit_root/tools/landrun-with-threads"
export COMPARATOR_LEAN4EXPORT="$audit_root/tools/comparator/.lake/packages/lean4export/.lake/build/bin/lean4export"
cd "$audit_root/project"
date -u +%FT%TZ > "$run_dir/start.txt"
set +e
systemd-run --user --wait --pipe --collect --unit=pi-audit-axioms-20261006 \
  --working-directory="$audit_root/project" \
  --property=RestrictAddressFamilies=~AF_UNIX \
  --property=MemoryMax=11G --property=MemorySwapMax=2G --property=CPUQuota=400% \
  --setenv="PATH=$PATH" --setenv="LEAN_NUM_THREADS=2" \
  "$audit_root/tools/lean-4.34.1-linux/bin/lake" env lean "$audit_root/AxiomAudit.lean" \
  2>&1 | tee "$run_dir/axioms.log"
axioms_result=${PIPESTATUS[0]}
printf '%s\n' "$axioms_result" > "$run_dir/axioms-exit.txt"
if [ "$axioms_result" = 0 ]; then
  systemd-run --user --wait --pipe --collect --unit=pi-audit-flint-hills-20261006 \
    --working-directory="$audit_root/project" \
    --property=RestrictAddressFamilies=~AF_UNIX \
    --property=MemoryMax=11G --property=MemorySwapMax=2G --property=CPUQuota=400% \
    --setenv="PATH=$PATH" --setenv="LEAN_NUM_THREADS=2" \
    --setenv="COMPARATOR_LANDRUN=$COMPARATOR_LANDRUN" --setenv="COMPARATOR_LEAN4EXPORT=$COMPARATOR_LEAN4EXPORT" \
    "$audit_root/tools/lean-4.34.1-linux/bin/lake" env \
    "$audit_root/tools/comparator/.lake/build/bin/comparator" ComparatorChallenges/PiExponent/FlintHills.json \
    2>&1 | tee "$run_dir/comparator.log"
  result=${PIPESTATUS[0]}
else
  result=$axioms_result
fi
printf '%s\n' "$result" > "$run_dir/exit.txt"
date -u +%FT%TZ > "$run_dir/end.txt"
mkdir -p "$bench/evidence/supplement"
cp "$run_dir/"*.txt "$run_dir/"*.log "$bench/evidence/supplement/"
cp "$audit_root/project/ComparatorChallenges/PiExponent/FlintHills.json" "$bench/evidence/supplement/challenge.json"
exit "$result"
