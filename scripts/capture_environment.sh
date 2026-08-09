#!/usr/bin/env bash
set -euo pipefail

mkdir -p artifacts
python_bin="${PYTHON_BIN:-python3}"
{
  echo "run_id=attack-0001"
  echo "git_commit=$(printenv GITHUB_SHA 2>/dev/null || git rev-parse HEAD 2>/dev/null || echo unavailable)"
  echo "runner_os=$(printenv RUNNER_OS 2>/dev/null || echo unknown)"
  echo "runner_arch=$(printenv RUNNER_ARCH 2>/dev/null || echo unknown)"
  echo "kernel=$(uname -a)"
  echo "lean=$(lean --version 2>/dev/null || echo unavailable)"
  echo "lake=$(lake --version 2>/dev/null || echo unavailable)"
  echo "python=$($python_bin --version 2>&1)"
  echo "toolchain=$(tr -d '\r\n' < lean-toolchain)"
  echo "mathlib_rev=v4.32.1"
  if [[ -f lake-manifest.json ]]; then
    echo "lake_manifest_sha256=$(sha256sum lake-manifest.json | cut -d' ' -f1)"
  else
    echo "lake_manifest_sha256=unavailable"
  fi
} > artifacts/environment.txt

cat artifacts/environment.txt
