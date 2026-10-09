"""Freeze exact inventories and generate explicit type/axiom inspections."""
import sys
import verify

for batch in sys.argv[1:]:
    module = verify.MODULES[batch]
    target = verify.AREA / batch / 'TARGET.md'
    if not target.exists():
        raise ValueError('Write the source-mapped target before accepting a proof')
    rows = verify.inventory(module)
    source = (verify.ROOT / 'Experiments' / (module + '.lean')).read_text(encoding='utf-8')
    code = verify.policy.strip_lean_comments_and_strings(source)
    for row, match in zip(rows, verify.DECL.finditer(code)):
        row.update(source_line=source[:match.start()].count('\n')+1,
                   source_target=verify.relative(target),
                   allowed_axioms=sorted(verify.ALLOWED))
    verify.write(verify.AREA / batch / 'claims.json', {'batch':batch,'module':'Experiments.'+module,
        'declarations':rows,'scope':'TARGET.md; exact quantified statements and axiom dependencies are recorded by the final receipt. Counts include definitions, helpers and controls, not independent source claims.'})
    lines=['import Experiments.'+module, '', 'set_option pp.fullNames true', '']
    for row in rows:
        lines += ['#check @'+row['name'], '#print axioms '+row['name']]
    (verify.ROOT/'Experiments'/(module+'Axioms.lean')).write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print(batch,len(rows),'explicit declarations',sum(row['kind']=='theorem' for row in rows),'theorems including helpers/controls')
