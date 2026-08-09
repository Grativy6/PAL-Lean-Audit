#!/usr/bin/env bash
set -euo pipefail

python_bin="${PYTHON_BIN:-python3}"
run_id="${AUDIT_RUN_ID:-attack-0001}"
environment_output="${AUDIT_ENVIRONMENT_OUTPUT:-artifacts/environment.txt}"
mkdir -p "$(dirname "$environment_output")"
event_name="${GITHUB_EVENT_NAME:-local}"
checked_out_sha="$(git rev-parse HEAD 2>/dev/null || echo unavailable)"
github_event_sha="${GITHUB_SHA:-unavailable}"
pr_number="${AUDIT_PR_NUMBER:-not_applicable}"
pr_head_sha="${AUDIT_PR_HEAD_SHA:-not_applicable}"
pr_base_sha="${AUDIT_PR_BASE_SHA:-not_applicable}"
tested_merge_sha="not_applicable"
if [[ "$event_name" == "pull_request" || "$event_name" == "pull_request_target" ]]; then
  tested_merge_sha="$checked_out_sha"
fi
{
  echo "run_id=$run_id"
  echo "event_name=$event_name"
  echo "github_ref=${GITHUB_REF:-local}"
  echo "head_ref=${GITHUB_HEAD_REF:-not_applicable}"
  echo "base_ref=${GITHUB_BASE_REF:-not_applicable}"
  echo "pr_number=$pr_number"
  echo "pr_head_sha=$pr_head_sha"
  echo "pr_base_sha=$pr_base_sha"
  echo "github_event_sha=$github_event_sha"
  echo "checked_out_sha=$checked_out_sha"
  echo "tested_sha=$checked_out_sha"
  echo "tested_merge_sha=$tested_merge_sha"
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
} > "$environment_output"

cat "$environment_output"
