# SCT-C frozen target

SCT v0.1 P0111-P0129 (SCT-05) and P0206-P0211. H1={0,1,2}, H2={3,4}, H3={1,2,4,6}; U1={0}, U2={0,1,2,3,4}, U3={0,1,2,3,4,5}. A valid permutation of 0..6 has actual hull residue <=1 for each H. False requires prefix slack zero, true allows <=1 for each U.

Lean: enumerate all permutations with the standard structural List.permutations' (proved equivalent to List.permutations) and connect membership to List.Perm; kernel-check that existence of a valid order is exactly OR and check the three supplied witnesses. Numerical counts are separately checked by a new Python enumerator (5040 orders, 8 triples, no symmetry filtering). Match the source counts if they agree; record disagreements without tuning the predicate.

Exact natural/integer arithmetic only. This is the local seven-column gadget, not slot forcing, global reduction, gadget minimality, priority, or NP completeness. Python success is bounded computation evidence; only the corresponding compiled Lean theorem with axiom and kernel receipt is a formal proof.
