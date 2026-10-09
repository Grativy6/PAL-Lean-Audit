"""Run only the audited 21-move finite checks, under the external bounded runner."""
import json
import pathlib
import subprocess
import sys
bench = pathlib.Path(__file__).resolve().parents[1]
prefix = bench / 'source/preprints/Snaky-in-21-Maker-moves-September-25-2026/verification'
output = bench / 'computations/route21-001/tests'
subprocess.run([sys.executable, '-B', str(prefix/'verify_certificate.py')], check=True)
subprocess.run([sys.executable, '-B', str(prefix/'supporting/route21/run_tests.py'), '--output-dir', str(output)], check=True)
report = json.loads((output/'report.json').read_text())
assert report['status'] == 'PASS'
print(json.dumps({'reviewed_report':'PASS','cards_compared':report['full_numbered_cards_compared'],'nodes_compared':report['full_postorder_nodes_compared'],'malformed_raw_rejections':report['negative_raw_reconstruction_tests'],'malformed_cli_rejections':report['negative_cli_tests'],'finite_board_boundary_rejections':report['negative_finite_board_tests']},sort_keys=True))

