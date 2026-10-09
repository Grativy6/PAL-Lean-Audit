"""Publish only local workshop guides after all retained verification gates pass."""
import re
from datetime import datetime, timezone
import verify

ROOT, AREA = verify.ROOT, verify.AREA
PAPERS = {
    'Single Cut Transport': ('SCT','Three batches complete: finite span, corridor invariance and the full seven-column OR gadget.'),
    'Compactification Costs': ('CC','Three batches complete: boundary topology, typed profiles, and selected geometric fixtures.'),
    'GPPR': ('GPPR','Three batches complete with an explicit external transcendence dependency; exact encoding and routing controls checked.'),
    'Finite Abstraction': ('FA','Selected coverage and quantifier controls complete; no RH or P-versus-NP result claimed.'),
}

def save(path, text):
    path.write_text(text, encoding='utf-8', newline='\n')

def main():
    for b in verify.MODULES:
        verify.check(b)
    integration = verify.read(AREA/'integration-results.json')
    if integration['status'] != 'PASS_INTEGRATION':
        raise ValueError('Integration is not complete')
    rows = []
    for b,m in verify.MODULES.items():
        r = verify.read(AREA/b/'results.json')
        rows.append({'batch':b,'module':m,'execution':r['status'],
                     'explicit_declarations':len(r['declarations']),
                     'theorems_including_helpers_controls_reuse':sum(x['kind']=='theorem' for x in r['declarations']),
                     'receipt_sha256':verify.sha(AREA/b/'results.json'),
                     'review':b+'/REVIEW.md'})
    verify.write(AREA/'summary.json',{
        'status':'COMPLETE_SELECTED_KEY_WITH_EXPLICIT_EXTERNAL_DEPENDENCY',
        'completed_utc':datetime.now(timezone.utc).isoformat(),
        'new_batches':rows,'earlier_batches':['AL-A','AL-B','AL-C'],
        'apci':'Existing local replay retained; not counted as a new audit.',
        'mathematical_open_inputs':['Checked Gelfond-Schneider theorem not supplied; golden formalization conditional.'],
        'optional_unselected_followups':['CC lens integration, Euler triangulations and analytic extension classes',
            'GPPR density/separation development and implementation-specific routing/benchmark protocols',
            'SCT global reduction, minimality and priority'],
        'integration_receipt_sha256':verify.sha(AREA/'integration-results.json'),
        'authority':'Local receipts and commits only. No source amendment, publication, remote CI or adoption.'})
    table = '\n'.join(f"| {r['batch']} | {r['explicit_declarations']} | {r['theorems_including_helpers_controls_reuse']} | [Receipt]({r['batch']}/results.json) · [Review]({r['review']}) |" for r in rows)
    save(AREA/'RECEIPT_BOOK.md',f'''# The remaining workshop key — receipt book

**All ten remaining selected batches completed locally on 8 October 2026.** Each passed its module build, exact declaration/type/axiom inspection and bundled Lean kernel replay. The existing project gates, six receipt-tampering controls and preserved Abstract Loops receipt checks also passed. [Integration evidence](integration-results.json) · [Machine-readable coverage](summary.json).

| Paper | What came back | Book |
| --- | --- | --- |
| Single-Cut Transport | Actual finite-support counting; filled-corridor invariance and puncture controls; all 5040 orders and eight truth triples, with the source's counts reproduced. | [SCT receipts](SCT/RECEIPT_BOOK.md) |
| Compactification Costs | Boundary surjection and continuous recovery derived from topology; compatible profiles; exact cube, common-mode and sector/residual fixtures. | [CC receipts](CC/RECEIPT_BOOK.md) |
| GPPR | Exact valuation and weighted code; positive rational extension; explicit golden theorem dependency; path/root and routing controls. | [GPPR receipts](GPPR/RECEIPT_BOOK.md) |
| Finite Abstraction | Finite-test countermodels, positive unbounded induction, quantifier controls and growing finite records. | [FA receipts](FA/RECEIPT_BOOK.md) |

The earlier [Abstract Loops batches](../abstract-loops-20261008/RECEIPT_BOOK.md) remain complete, and [APCI's existing local replay](../../../Other%20mathematics/APCI/README.md) is retained without counting it as new work. This closes the selected five-paper key, with the explicit dependencies and optional follow-ups below.

## What deserves attention

**GPPR G06 needs a root-representation qualification.** Equal factor multisets can have a shared endpoint and distinct ordered receipts. Distinct finite hashes need a specified representation and a collision condition. The formal controls show the difference; the manuscript was not edited.

**Golden transcendence remains conditional in Lean.** The actual golden arithmetic, irrational algebraic exponent and logarithm branch are checked. The necessary external theorem is supported by the [primary-source record](GPPR-A/LITERATURE.md), but Gelfond-Schneider itself is not in this kernel dependency closure. It is a named hypothesis, not a new axiom. The exact code consumers and their golden specializations expose it.

No additional mathematical correction surfaced in the selected SCT, CC or FA claims. Existing assumptions do real work. See [clarifications for Chris](CLARIFICATIONS.md) for conditions already present, the sector tie convention, the root qualification and the remaining library boundary.

## Coverage without inflated counts

| Batch | Explicit declarations | Theorems within that inventory | Evidence |
| --- | ---: | ---: | --- |
{table}

These inventories include definitions, supporting lemmas, finite controls and reused specializations. They do not count independent paper claims. Policy-definition checks, literature verification, numerical enumeration and new mathematical coverage are distinguished in the reviews. The separate SCT computation checks all 40,320 order/truth pairs; the OR theorem has its own kernel proof.

## Remaining boundaries

Optional CC lens-area, Euler-triangulation and analytic-extension checks need their additional mathematical models. GPPR's full density/separation development, a concrete router and preregistered performance comparisons remain separate work. SCT's global reduction, minimality and priority are unclosed by this local lemma audit. FA supplies no RH, P-versus-NP, lower-bound or independence result. These were not silently included in the completed targets.

Sources remain byte-identified in the [manifest](source-manifest.json), with frozen [program targets](TARGETS.md) and per-batch targets. Original manuscripts, the preparation key, old receipts and unrelated work remain preserved. Failed development and superseded verification attempts remain beside the final receipts. Only standard Lean axioms occur; no proof holes or new axioms were accepted. Review was self-review, and the bundled checker is not an independent kernel implementation.

Replay a batch with the bundled Python runtime and `verify.py --batch BATCH`; use `--check` to validate saved evidence without rerunning Lean. `integration.py` checks the whole selected set and retained project gates. [Navigation and committed input bindings](navigation.json) record the shelf links and exact proof bytes. Local commits do not publish or adopt manuscript claims.
''')
    for name,(slug,coverage) in PAPERS.items():
        path = ROOT.parent/'Other mathematics'/name/'README.md'
        text = path.read_text(encoding='utf-8')
        text, count = re.subn(r'\*\*Current receipt coverage:\*\*[^\n]*', '**Current receipt coverage:** '+coverage,text,count=1)
        if count != 1:
            raise ValueError('Missing coverage entrance: '+str(path))
        start, end = text.index('## Lean proofs and receipts'), text.index('## Working here')
        entrance = f'''## Lean proofs and receipts

[Open the receipt book](<../../Shared Lean project/Audit/workshop-rest-20261008/{slug}/RECEIPT_BOOK.md>) for exact results, assumptions, source comparisons and remaining boundaries. [Cross-paper clarifications](<../../Shared Lean project/Audit/workshop-rest-20261008/CLARIFICATIONS.md>) record what may deserve a manuscript qualification.

The editable proofs remain in the shared project; this folder links to their canonical copy. These are local kernel receipts, with no manuscript adoption, publication or new remote CI implied.

'''
        save(path,text[:start]+entrance+text[end:])
    outer = ROOT.parent/'WORKBENCH.md'
    text = outer.read_text(encoding='utf-8')
    for name,(_,coverage) in PAPERS.items():
        pattern = r'(?m)^- \['+re.escape(name)+r'\].*$'
        label = name
        text,n = re.subn(pattern,f'- [{label}](<Other mathematics/{name}/README.md>) — {coverage}',text,count=1)
        if n != 1:
            raise ValueError('Missing shelf row: '+name)
    old = 'The other ten proposed batches remain unactivated.'
    new = 'Chris then activated the remaining ten batches, which are now complete locally. The [combined receipt book](<Shared Lean project/Audit/workshop-rest-20261008/RECEIPT_BOOK.md>) records all four papers, the explicit golden-transcendence dependency and the G06 root qualification.'
    if old not in text and new not in text:
        raise ValueError('Audit queue changed during work')
    save(outer,text.replace(old,new))
    local = ROOT/'WORKBENCH.md'
    text = local.read_text(encoding='utf-8')
    old = 'The other ten\nproposed batches remain unactivated; the original key is retained as preparation history.'
    new = 'The remaining ten batches were subsequently activated and completed locally: open the\n[combined receipt book](Audit/workshop-rest-20261008/RECEIPT_BOOK.md). GPPR retains an explicit\nexternal transcendence dependency. The original key remains preparation history.'
    if old not in text and new not in text:
        raise ValueError('Local workbench queue changed during work')
    save(local,text.replace(old,new).replace('Preserved experiment modules and the three new Abstract Loops modules, with their axiom-inspection companions.',
        'Preserved experiment modules, three Abstract Loops batches and ten remaining-key batches, with exact axiom-inspection companions.'))
    activation = ROOT/'workbench/keys/20261008-five-paper-audit/REMAINDER_ACTIVATION.md'
    text = activation.read_text(encoding='utf-8')
    marker = '\n## Local completion\n'
    if marker in text:
        text = text.split(marker)[0]
    save(activation,text+marker+'\nAll ten selected batches have passing local receipts. The golden specialization retains its explicitly named external theorem input. [Combined receipt book](../../../Audit/workshop-rest-20261008/RECEIPT_BOOK.md) · [Clarifications](../../../Audit/workshop-rest-20261008/CLARIFICATIONS.md).\n')
    print('WROTE_LOCAL_RECEIPT_BOOKS_AND_SHELF_GUIDES')

if __name__ == '__main__':
    main()
