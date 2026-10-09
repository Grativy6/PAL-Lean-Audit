# SCT-A frozen target

Source SCT v0.1 P0057-P0092: Lemma 2.1 and Theorem 3.1 (SCT-01/02). Columns are identified with their natural-number positions through a supplied bijection with Fin n; arbitrary supports become finite sets of ranks. Zero-based indexing is a change of origin only.

For nonempty finite ranks S, hull = [min S,max S], residue = hull minus S, charge = cardinality of residue. Prove charge = max-min+1-card S. Empty/singleton charge is zero; at-most-one-hole criterion is about this actual hull.

Serial realization: chosen literal at rank 0, e missing mate slots (source specializes e=0 or 1), c+1 fully selected corridor/guard positions starting at e+1, then nonempty clause subset U at offset e+c+2. Clause ranks start at zero. Prove actual hull charge = e + (max U+1-card U) from this support. General e is an explicit arithmetic extension; the Boolean source conclusion restricts e to 0/1.

Assumptions: finite support, exact supplied rank order, nonempty clause subset; all intermediate corridor positions selected. No global reduction, hidden derivation of orientation, or physical transport. A normalized rank model must be related to arbitrary finite column names by a bijective-order image theorem.
