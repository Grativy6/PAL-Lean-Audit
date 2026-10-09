"""Exact seven-column local gadget enumeration; no symmetry filtering."""
from itertools import permutations, product
from pathlib import Path
import json, sys

H = ({0,1,2}, {3,4}, {1,2,4,6})
U = ({0}, set(range(5)), set(range(6)))
expected = {'000':0,'001':8,'010':4,'011':28,'100':2,'101':12,'110':14,'111':50}
triples = list(product((0,1), repeat=3))
counts = {''.join(map(str,t)):0 for t in triples}
all_orders = list(permutations(range(7)))
assert len(all_orders) == len(set(all_orders)) == 5040
assert all(set(p) == set(range(7)) for p in all_orders)
witnesses = {}
for p in all_orders:
    rank = {v:i for i,v in enumerate(p)}
    charges = []
    for row in H:
        selected = {rank[v] for v in row}
        holes = set(range(min(selected),max(selected)+1)) - selected
        counted = len(holes)
        span = max(selected)-min(selected)+1-len(row)
        assert counted == span
        charges.append(counted)
    slacks = []
    for row in U:
        selected = {rank[v] for v in row}
        counted = len(set(range(max(selected)+1))-selected)
        assert counted == max(selected)+1-len(row)
        slacks.append(counted)
    for t in triples:
        ok = all(k <= 1 for k in charges) and all(s <= b for s,b in zip(slacks,t))
        label = ''.join(map(str,t))
        counts[label] += int(ok)
        if ok: witnesses.setdefault(label,p)
assert counts == expected, {'actual':counts,'expected':expected}
assert {k for k,v in counts.items() if v} == set(expected)-{'000'}
result = {'status':'IMPLEMENTATION_AND_FINITE_ASSERTION_VERIFIED','orders':len(all_orders),
          'truth_triples':len(triples),'order_truth_pairs':len(all_orders)*len(triples),
          'arithmetic':'exact Python integers and sets','filtering':'none',
          'counts':counts,'example_witnesses':witnesses,
          'checks':['hull set counting agrees with span subtraction','prefix set counting agrees with slack subtraction','all orders unique','exact OR projection','source count comparison'],
          'review':'self-review; Python and Lean implementations share the inspected source specification',
          'scope':'local gadget only; no global reduction or minimality claim'}
path = Path(sys.argv[1]); path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,indent=2))
