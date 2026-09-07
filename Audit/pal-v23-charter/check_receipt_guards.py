"""Mutation checks for the new experiment's exact axiom-receipt parser."""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from run_pal23_charter import claims_and_inventory, parse_axioms


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).parent / 'receipt-guard-results.json')
    args = parser.parse_args()
    _, inventories = claims_and_inventory()
    source = sorted((ROOT / 'Audit/pal-v23-charter/evidence').glob('attempt-*/pal23-axioms.txt'))[-1]
    baseline = source.read_text(encoding='utf-8')
    parse_axioms(source, inventories['Pal23'])
    lines = baseline.splitlines(keepends=True)
    empty_row = next(line for line in lines if 'does not depend on any axioms' in line)
    probes = {
        'missing_axiom_free_row': baseline.replace(empty_row, '', 1),
        'duplicated_row': baseline + empty_row,
        'unlisted_dependency': baseline.replace('Classical.choice', 'Unexpected.customAxiom', 1),
    }
    folder = ROOT / 'artifacts/pal-v23-charter-2026-09-07/receipt-parser-probes'
    folder.mkdir(parents=True, exist_ok=True)
    results = []
    for name, text in probes.items():
        path = folder / f'{name}.txt'
        path.write_text(text, encoding='utf-8', newline='\n')
        try:
            parse_axioms(path, inventories['Pal23'])
        except ValueError as exc:
            results.append({'probe': name, 'status': 'EXPECTED_REJECTION', 'diagnostic': str(exc)})
        else:
            raise RuntimeError(f'Malformed receipt was accepted: {name}')
    output = {'population': 'TOOLING_MUTATION_CHECKS_NOT_THEOREM_RESULTS',
              'baseline': source.relative_to(ROOT).as_posix(), 'valid_baseline': 'ACCEPTED', 'probes': results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Valid receipt accepted; missing axiom-free row, duplicate row, and unlisted axiom rejected.')


if __name__ == '__main__':
    main()
