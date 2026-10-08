"""Bind the approved manuscript claims to named declarations and explicit limits."""
from pathlib import Path
import hashlib, json, re

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT.parent/'Sources/v1.0/FRONT_v1.0_WORKING_DRAFT.md'

# Key, batch, module, declarations, exact scope, remaining correspondence obligation.
ROWS=[
('1','B','Propagation',['premise_substitution'],
 'Fixed finitary inference rules, arbitrary proposition labels, every retained premise has a valid present derivation; substitution is proved by structural induction.',
 'Explicit finitary calculus realization. No encoding of all sound monotone calculi or natural deduction with discharged assumptions.'),
('2','B','Propagation',['negative_core_transfer'],
 'Arbitrary clauses and valuations with a fixed satisfaction relation; an unsatisfiable core is a subset of the new clause set.', ''),
('3','A','Answers',['answer_sufficiency'],
 'Arbitrary types and total input/answer maps. Decoder lives on the reachable subtype, including empty domains. Reuses APCI exactOnReachable_iff_fiberConstant.', ''),
('3A','A','Answers',['joint_equality','joint_sufficiency'],
 'Dependent labeled family of readouts, with a decoder on its actual reachable tuples; classical choice is explicit in the dependency inventory.', ''),
('3B','E','Linear',['linear_factorization'],
 'Linear maps on one full vector space over a field; the decoder domain is the image of J and existence is equivalent to ker J <= ker q.', ''),
('4','A','Answers',['common_action_iff'],
 'One adequate action common to each reachable fiber, with adequacy supplied as a relation. The proof permits arbitrary sets; the finite manuscript case is an instance.', ''),
('5','D','Continuation',['future_output_preservation','online_update_iff','future_eq_is_right_congruence'],
 'All finite words over the declared deterministic update alphabet; output preservation and a same-encoding transition function have separate iff statements.', ''),
('6','A','Answers',['coordinate_bit_bound'],
 'Exact recovery of every coordinate of d Boolean bits from a fixed-length b-bit representation. No noise, probabilistic guarantee, variable length, or external rereading.', ''),
('5A','DE','Continuation',['admitted_outputs_sufficiency'],
 'The actual admitted index set, not its rectangular completion. Dependent indexed outputs. Linear joint-kernel and refinement statements in Linear.lean.', ''),
('5B','E','Horizon',['invariant_kernel_iff','horizon_antitone','finite_horizon_closure','infinite_invariant','all_outputs_equal_iff'],
 'Full vector-space difference domain; one linear endomorphism and readout. Stabilization at dim T holds for any finite-dimensional field vector space (including zero dimension). The Lean proof uses strict dimension drop, not Cayley-Hamilton.', ''),
('5C','E','Horizon',['finite_readout_subfamily','finite_subfamily_inside'],
 'Arbitrary indexed family; finite-dimensional input. At most dim T readouts preserve the common kernel. The proof works even without finite-dimensional codomains; no effective selection or acquisition claim.', ''),
('5D','E','Linear',['joint_residual_short_exact','joint_visible_equiv','joint_sector_dimensions','visibleRefinement','refinement_commutes'],
 'One common B and actual J; typed hidden injection, residual quotient map, exactness, injectivity, surjectivity and visible equivalence. Finite dimension only for the dimension identity. Refinement uses the same B. Verbatim inherited BRIDGE proofs keep their identity.', ''),
('5E','E','Linear',['side_trace_decodable','side_trace_rank_lower_bound','minimum_side_trace','side_trace_capacity','side_trace_capacity_injection','residual_query_criterion','residual_debt_image','residual_side_trace_capacity'],
 'Finite-dimensional input, state query q, actual J and linear side trace. Lower bound plus attaining noncanonical extension. Finite-side-space dimension iff; arbitrary side spaces use an equivalent injective-copy capacity statement. Residual target uses T/B and the range of its named hidden injection. Rank is not acquisition cost.', ''),
('5F','DE','Linear',['quotient_update_iff','transported_return'],
 'Arbitrary subspace B and linear L: a commuting quotient update exists iff B is invariant. B may be ker J. Equation 20m uses powers of the same endomorphism and transports the second return.', ''),
('7','F','Costs',['reuse_cheaper_iff','no_saving_when_reuse_is_costlier'],
 'Equal-unit real costs in the stated model; algebraic break-even identity. No-cost-saving corollary assumes m>=1, B>=0 and R>=D.', ''),
('7A','B','Propagation',['finite_stabilization','horn_least_closure','stable_round_persists'],
 'Finite atom type, finite rule set, inflationary monotone Horn step. At most card atoms minus card seeds strict growth rounds; fixed point contains seeds and is least among closed supersets. Final no-change scan is additional work.', ''),
('7B','B','Propagation',['horn_rounds_sound','derivation_sound','empty_seed_stays_empty'],
 'Declared true roots and truth-preserving rules; every conjunctive parent is checked. No unsupported cycle generates support. Empty-body rules require their own declared rule soundness.', ''),
('7C','B','Propagation',['wake_decomposition','redundant_seed'],
 'Finite set partition with E subset B subset S and old/new least-closure properties supplied for the redundancy corollary. No generic speedup is asserted.', ''),
('7D','B','Propagation',['increasing_depth_no_cycle','valid_under_unchanged_basis','derivation_sound'],
 'Any strictly increasing discovery ranking rules out cycles. A finite rooted derivation remains valid when every actually used root and rule retains validity; that returned derivation implies its head under sound interpretations.',
 'Sharing is represented by the finite tree obtained after unfolding a DAG. No verified parser, DAG-to-tree compiler, exact byte matcher or Python implementation refinement theorem.'),
('7E','C','Correction',['recorded_support_sound','unchanged_alternative_survives','scratch_commit_iff','failed_scratch_keeps_original','scratch_preserves_history','finite_history_preservation'],
 'Finite recorded witnesses with all children grounded; conditional root/rule truth. An explicit pure scratch transition commits changed state iff its grant and postcondition hold, otherwise retains the original state. Every transition appends history; prefix preservation composes.',
 'A checked realization of the conditional correction claims, not a proof for arbitrary repair implementations. The grant/postcondition are fixed supplied predicates; the Python fixture increments a version on commit and is not compiled from this Lean transition. External authority, concurrent revocation and crash recovery remain outside.'),
('8','F','Costs',['descending_rank_bounds_steps','total_cost_bound','polynomial_accounting'],
 'Natural-valued strictly decreasing rank, bounded initial rank, bounded per-stage cost, polynomial init cost. Proves the p0+(p1+1)*p2 numerical bound and polynomial expression.',
 'No encoding of a uniform SAT decider or machine-level complexity classes. The source consequence about P=NP remains conditional on its stated algorithm, correctness, totality and cost hypotheses; none is constructed here.')]

EXTRA={'5A':['FrontLean.joint_kernel','FrontLean.kernel_refinement'],
       '5D':['Experiments.BridgeRecovery.ker_residualReadout'],
       '5E':['Experiments.BridgeRecovery.answer_decodable_iff']}

def main():
    data=json.loads((ROOT/'Audit/claims.json').read_text(encoding='utf-8'))
    old={r['id']:r for r in data['claims']}
    rows=[]
    for cid,batch,module,names,scope,gap in ROWS:
        row=old[cid]
        row.update(batch=batch,module='FrontLean.'+module,
                   status='BOUNDED_REALIZATION' if gap else 'GENERAL_STATEMENT_CHECKED',
                   verification='Authoritative local verification status: receipts/formal/receipt.json',
                   formal_declarations=['FrontLean.'+n for n in names]+EXTRA.get(cid,[]),
                   assumptions_and_scope=scope,remaining_obligation=gap or
                   'No open gap in the stated formal target. External application, illustrative examples and all surrounding prose are not thereby certified.')
        row['source_heading_sha256']=hashlib.sha256(row['source_heading'].encode()).hexdigest()
        rows.append(row)
    data.update(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),claims=rows,
                review_status='SAME_SESSION_SELF_REVIEW',
                source_correspondence='Human-readable map assessed separately from Lean acceptance.',
                definitions_and_schemas=[
                  {'id':'C1','kind':'definition','declaration':'FrontLean.RecordedSupport',
                   'scope':'Existence among a fixed finite recorded list. Exhaustion is not negation of the query.'},
                  {'id':'C2','kind':'accounting schema','evidence':'receipts/experiment-reconciliation.json',
                   'scope':'All logged phase times sum to measured wall time; operation counters reaggregate. No universal cost theorem or memory sandbox follows.'}])
    (ROOT/'Audit/claims.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    md=['# Source-to-proof coverage','',
        'Source: supplied FRONT v1.0 working draft. General means the named formal statement covers the mathematical claim at the scope below. Bounded means an explicit realization or numerical core with the remaining bridge named. Neither label certifies all prose or the Python implementation. Final checking lives in `receipts/formal/receipt.json`.','',
        '| Claim | Batch | Disposition | Main declaration |','|---|---|---|---|']
    for row in rows:
        md.append(f"| {row['id']} | {row['batch']} | {row['status']} | `{row['formal_declarations'][0]}` |")
    for row in rows:
        md+=['',f"## Proposition {row['id']}",'',row['source_heading']+f" — manuscript line {row['source_markdown_line']}.",'',
             row['assumptions_and_scope'],'', '**Remaining limit:** '+row['remaining_obligation'],'',
             'Declarations: '+', '.join('`'+d+'`' for d in row['formal_declarations'])+'.']
    (ROOT/'Audit/COVERAGE.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    declarations=[]
    modules=['APCILeanAudit.Interface','Experiments.BridgeFourSector','Experiments.BridgeReadout',
             'Experiments.BridgeRecovery','Experiments.BridgeDimension']
    modules += ['FrontLean.'+m for m in ('Answers','Continuation','Costs','Propagation','Correction','Linear','Horizon','Controls')]
    for module in modules:
        path=ROOT/(module.replace('.','/')+'.lean')
        text=path.read_text(encoding='utf-8')
        namespace=re.search(r'^namespace (\S+)',text,re.M).group(1)
        for match in re.finditer(r'^(?:noncomputable )?(theorem|def|abbrev) (\w+)',text,re.M):
            declarations.append({'name':namespace+'.'+match[2],'kind':match[1],
                                 'file':path.relative_to(ROOT).as_posix(),
                                 'line':text[:match.start()].count('\n')+1,
                                 'inherited':not module.startswith('FrontLean.')})
    known={d['name'] for d in declarations}
    for row in rows:
        if not set(row['formal_declarations'])<=known: raise ValueError(row['id'])
    inventory={'modules':modules,'declarations':declarations,
               'excluded_from_public_inventory':'Private helpers, generated recursors and instances are checked inside their modules but not counted as public declarations.'}
    (ROOT/'Audit/declarations.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8')
    axioms=['import FrontLean','', '-- Signatures and transitive axioms for every public authored/inherited declaration.']
    for d in declarations: axioms.extend(['#check @'+d['name'],'#print axioms '+d['name']])
    (ROOT/'Audit/Axioms.lean').write_text('\n'.join(axioms)+'\n',encoding='utf-8')
    print(json.dumps({'claims':len(rows),'general':sum(not r[5] for r in ROWS),
                      'bounded':sum(bool(r[5]) for r in ROWS),'public_declarations':len(declarations),
                      'new_theorems':sum(d['kind']=='theorem' and not d['inherited'] for d in declarations),
                      'inherited_theorems':sum(d['kind']=='theorem' and d['inherited'] for d in declarations)}))

if __name__=='__main__':main()
