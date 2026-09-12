#!/usr/bin/env python3
"""Run the negative receipt guards without changing the frozen local receipt."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

AREA = Path(__file__).resolve().parent
sys.path.insert(0, str(AREA))
import check_publication


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=AREA / 'publication-guard-results.json')
    args = parser.parse_args()
    rejected = check_publication.guard_tests()
    value = {'population': 'PUBLICATION_RECEIPT_MUTATION_GUARDS_NOT_THEOREM_RESULTS',
             'status': 'PASS_EXPECTED_REJECTIONS', 'rejected_mutations': rejected}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('PASS_PUBLICATION_GUARDS: ' + ', '.join(rejected))


if __name__ == '__main__':
    main()
