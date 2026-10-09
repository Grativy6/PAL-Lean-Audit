"""Close the bounded Snaky visit honestly, including unfinished formal coverage."""
import datetime
import hashlib
import json
import pathlib
import re
import subprocess

bench=pathlib.Path("/mnt/h/Hearthline's Path/Math Workbench/openai-math-snaky-2026-10-07")
audit=pathlib.Path('/home/cdpang/math-snaky-audit-20261007')
build=audit/'project'
run=bench/'evidence/comparator-001'
log=(run/'run.log').read_text()
code=int((run/'exit.txt').read_text())
paths=(bench/'evidence/proof-module-paths.txt').read_text().splitlines()
modules=[p.removeprefix('lean/').removesuffix('.lean').replace('/','.') for p in paths]
completed=sorted(set(re.findall(r'Built (OAI\.GameTheory\.SnakyTwentyOne\.[A-Za-z0-9.]+)',log)))
missing=sorted(set(modules)-set(completed))
assert set(completed)<=set(modules)
formal_pass=(code==0 and 'Lean default kernel accepts the solution' in log and 'Your solution is okay!' in log)
if formal_pass:
    formal_status='PASS'
elif 'Finished with result: timeout' in log:
    formal_status='PARTIAL_RESOURCE'
else:
    formal_status='FAILED'
validator=pathlib.Path('/mnt/c/Users/cdpan/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py')
validate=subprocess.run(['python3',str(validator),str(bench/'computations/route21-001/manifest.json'),'--root',str(bench)],text=True,capture_output=True,check=True)
(bench/'evidence/finite-manifest-validation.txt').write_text(validate.stdout+validate.stderr)
report=json.loads((bench/'computations/route21-001/tests/report.json').read_text())
source=json.loads((bench/'evidence/source-manifest.json').read_text())
integrity=json.loads((bench/'evidence/integrity-results.json').read_text())
assert report['status']=='PASS' and integrity['status']=='PASS'
def bytes_under(root):
    return sum(p.stat().st_size for p in root.rglob('*') if p.is_file() and not p.is_symlink())
record={
 'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'source_revision':source['revision'],
 'selected_claim':'C21: a legal Maker win within 21 actual Maker claims on the empty infinite board.',
 'conventional_audit':'PROVED_AS_WRITTEN_FOR_SELECTED_CLAIM',
 'conventional_audit_basis':'The combination lemma, bases, placements, backward-reference induction, exact finite reconstruction, and ordinary-policy move/legality argument were reviewed by one assistant.',
 'finite_status':'PASS','finite_manifest_valid':True,
 'finite_counts':report['counts'],'finite_endpoint':report['endpoint'],
 'negative_raw_reconstruction_tests':report['negative_raw_reconstruction_tests'],
 'negative_cli_tests':report['negative_cli_tests'],
 'negative_finite_board_tests':report['negative_finite_board_tests'],
 'formal_status':formal_status,'formal_exit':code,
 'formal_compiled_modules':len(completed),'formal_required_modules':len(modules),
 'compiled_modules':completed,'remaining_modules':missing,
 'formal_challenge_compiled':'Built ComparatorChallenges.SnakyTwentyOne' in log,
 'formal_target_compiled':'OAI.GameTheory.SnakyTwentyOne.Main' in completed,
 'formal_kernel_replay_passed':'Lean default kernel accepts the solution' in log,
 'formal_comparator_acceptance':'Your solution is okay!' in log,
 'explicit_axiom_audit':'PREPARED_NOT_RUN',
 'formal_resource_ceiling':{'wall_seconds':1800,'cpu_quota_percent':200,'memory_bytes':8*1024**3,'swap_bytes':1024**3,'lean_worker_count':2},
 'formal_start_utc':(run/'start.txt').read_text().strip(),
 'formal_end_utc':(run/'end.txt').read_text().strip(),
 'integrity_status':integrity['status'],
 'dependencies_verified':len(integrity['dependencies']),
 'workspace_logical_bytes_before_seal':bytes_under(bench),
 'linux_build_logical_bytes':bytes_under(audit),
 'reuse_limit':'Existing pinned toolchain and Mathlib cache was reused, not independently bootstrapped.',
 'source_or_solution_modified':False,
 'native_tex_compilation':'UNAVAILABLE: Unable to find standard directories for platform',
 'book_pdf_method':'Separately generated with ReportLab; four rendered pages inspected.',
 'scope_exclusions':['Optimality/lower bound','25- and 35-move appendices','historical novelty','independent referee','Nanoda alternative kernel','formal finite-board theorem'],
}
(bench/'evidence/verification-results.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in ['compiled_modules','remaining_modules','conventional_audit_basis']},indent=2))
