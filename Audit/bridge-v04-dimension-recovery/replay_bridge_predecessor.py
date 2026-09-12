"""Replay PR14 from its own pinned checkout, never from a later batch tree."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PINNED_HEAD = '1babbcd19b51bba46dc9a51365dcadbe31bf1763'
RUNNER = 'Audit/bridge-v04-diagram-readout/run.py'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def command(argv, cwd: Path, log: Path, env: dict) -> dict:
    try:
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, encoding='utf-8', errors='replace', timeout=1200)
        code, text = result.returncode, result.stdout
    except subprocess.TimeoutExpired as exc:
        text = exc.stdout or ''
        text = text.decode('utf-8', errors='replace') if isinstance(text, bytes) else text
        code, text = 124, text + '\nEXECUTION_TIMEOUT\n'
    except OSError as exc:
        code, text = 127, f'EXECUTION_ERROR: {exc}\n'
    log.write_text(text.replace('\r\n', '\n'), encoding='utf-8', newline='\n')
    return {'argv': argv, 'exit_code': code, 'log': log.name, 'sha256': sha(log)}


def replay(lake: str, output: Path) -> dict:
    output = output.resolve()
    if output.exists():
        raise AssertionError(f'output already exists: {output}')
    output.mkdir(parents=True)
    record = {'schema_version': '1.0', 'status': 'RUNNING', 'mode': 'HISTORICAL_REPLAY', 'historical_checkout': PINNED_HEAD,
              'historical_runner': RUNNER, 'started_utc': datetime.now(timezone.utc).isoformat(), 'commands': []}
    record['parent_github_run_id'] = os.getenv('GITHUB_RUN_ID')
    record['parent_pr_head_sha'] = os.getenv('BRIDGE_RECOVERY_PR_HEAD_SHA')
    record['parent_checkout_sha'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    record['coverage'] = 'PINNED_HISTORICAL_TREE_ONLY_NOT_CURRENT_CANDIDATE'
    with tempfile.TemporaryDirectory(prefix='bridge-pr14-') as temporary:
        worktree = Path(temporary) / 'checkout'
        linked_lake = worktree / '.lake'
        cache_links = []
        assert worktree.resolve().parent == Path(temporary).resolve()
        try:
            subprocess.run(['git', 'worktree', 'add', '--detach', str(worktree), PINNED_HEAD], cwd=ROOT, check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
            actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=worktree, text=True).strip()
            assert actual == PINNED_HEAD
            # .gitignore contains .lake/: it ignores a directory, not a Unix symlink.
            # Keep that directory real and expose prepared cache entries inside it.
            linked_lake.mkdir()
            for cache_entry in (ROOT / '.lake').iterdir():
                target = linked_lake / cache_entry.name
                if cache_entry.is_dir():
                    try:
                        os.symlink(cache_entry, target, target_is_directory=True)
                    except OSError:
                        if os.name != 'nt': raise
                        subprocess.run(['cmd', '/c', 'mklink', '/J', str(target), str(cache_entry)], check=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')
                    cache_links.append(target)
                else:
                    shutil.copy2(cache_entry, target)
            assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=worktree, text=True).strip()
            child_env = os.environ.copy()
            child_env.pop('GITHUB_RUN_ID', None)
            child_env.pop('BRIDGE_DIAGRAM_PR_HEAD_SHA', None)
            child_env.pop('BRIDGE_RECOVERY_PR_HEAD_SHA', None)
            receipt_dir = worktree / 'artifacts' / 'bridge-pr14-historical-replay'
            steps = [
                ('historical-check', [sys.executable, RUNNER, '--check']),
                ('historical-replay', [sys.executable, RUNNER, '--replay', '--lake', lake, '--output-dir', str(receipt_dir)]),
            ]
            for label, argv in steps:
                result = command(argv, worktree, output / f'{label}.txt', child_env)
                result['label'] = label
                record['commands'].append(result)
                if result['exit_code']:
                    raise RuntimeError(f'{label} failed ({result["exit_code"]})')
            shutil.copytree(receipt_dir, output / 'historical-replay')
            replay_receipt = json.loads((receipt_dir / 'execution.json').read_text(encoding='utf-8'))
            assert replay_receipt['status'] == 'PASS_BRIDGE_DIAGRAM_READOUT'
            assert replay_receipt['tested_checkout_sha'] == PINNED_HEAD
            record['historical_replay_execution_sha256'] = sha(output / 'historical-replay' / 'execution.json')
            record['status'] = 'PASS_HISTORICAL_PR14_REPLAY'
        except Exception as exc:
            if (worktree / 'artifacts' / 'bridge-pr14-historical-replay').is_dir():
                shutil.copytree(worktree / 'artifacts' / 'bridge-pr14-historical-replay', output / 'historical-replay', dirs_exist_ok=True)
            record['status'] = 'FAILED_HISTORICAL_PR14_REPLAY'
            record['error'] = str(exc)
            raise
        finally:
            record['finished_utc'] = datetime.now(timezone.utc).isoformat()
            write(output / 'execution.json', record)
            for cache_link in cache_links:
                assert cache_link.parent == linked_lake and linked_lake.parent == worktree
                if cache_link.is_symlink(): cache_link.unlink()
                else:
                    assert os.name == 'nt' and cache_link.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
                    os.rmdir(cache_link)
            assert worktree.resolve().parent == Path(temporary).resolve()
            subprocess.run(['git', 'worktree', 'remove', '--force', str(worktree)], cwd=ROOT, check=False,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--lake', default='lake')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    record = replay(args.lake, args.output_dir)
    print(record['status'])


if __name__ == '__main__':
    main()
