#!/usr/bin/env bash
set -euo pipefail
audit_root=/home/cdpang/math-pi-audit-20261006
export PATH="$audit_root/tools/lean-4.34.1-linux/bin:$PATH"
export MATHLIB_NO_CACHE_ON_UPDATE=1
export LEAN_NUM_THREADS=4
python3 "/mnt/h/Hearthline's Path/Math Workbench/openai-math-pi-2026-10-06/scripts/prepare-build.py"
cd "$audit_root/project"
lake update 2>&1 | tee "$audit_root/logs/mathlib-update.log"
lake exe cache get 2>&1 | tee "$audit_root/logs/mathlib-cache.log"
