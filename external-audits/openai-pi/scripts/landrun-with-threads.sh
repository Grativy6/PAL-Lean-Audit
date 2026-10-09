#!/usr/bin/env bash
# Retain Comparator's sandbox; set a bounded Lean worker count inside it.
exec /home/cdpang/math-pi-audit-20261006/tools/landrun-bin --env LEAN_NUM_THREADS=2 "$@"
