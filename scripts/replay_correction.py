"""Replay the frozen study unchanged; report unavailable Windows RSS as null."""
from pathlib import Path
import argparse
import importlib.util
import json
import runpy
import sys
import types

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = (ROOT / args.output).resolve()
    if not out.is_relative_to(ROOT / 'Audit' / 'runs'):
        raise ValueError('Output must be in this audit runs directory')
    source = ROOT / 'Audit' / 'fixture-source'
    adaptation = None
    if importlib.util.find_spec('resource') is None:
        # The inspected runner uses resource only for optional final RSS metadata.
        # None explicitly records unavailability; it is never a fabricated zero.
        resource = types.ModuleType('resource')
        resource.RUSAGE_SELF = 0
        resource.getrusage = lambda _: types.SimpleNamespace(ru_maxrss=None)
        sys.modules['resource'] = resource
        adaptation = 'Original resource.getrusage telemetry unavailable; peak_rss_kib is null.'
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(source))
    program = runpy.run_path(str(source / 'run_correct.py'), run_name='frozen_front_runner')
    program['run'](out / 'results')
    (out / 'platform-adapter.json').write_text(json.dumps({
        'adaptation': adaptation,
        'frozen_source_changed': False,
        'python': sys.version,
        'optimized': bool(sys.flags.optimize),
        'scope': 'Only the unavailable resource-reporting field. Policy, oracle, checks, fixtures and timers unchanged.'
    }, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
