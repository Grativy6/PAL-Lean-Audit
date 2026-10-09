# C3 — typed directed paths

Source: PAL v2.3 Mathematical Realization Atlas, SHA-256
c053292376363edd6fc743f0f2e31e3bb3850edc78ade3a289bbb07e7e8452c5,
P0627--P0641. This finite model has three vertex tags, two relation tags, and
receipt versus unverified evidence. `checkedAppend` first requires that the
existing path is valid, then admits an edge only when its source equals the
path endpoint and its evidence is a receipt tag. The general append-validity
theorem derives valid ordered-path preservation from a successful append; list
deletion recovers the predecessor edge list.

Fixtures establish two valid appends, ordered history `[ab, bc]`, endpoint,
evidence-tag, and malformed-prefix rejection, and co-occurring vertices with
no edge. The receipt tag is not source authentication or evidence truth.
Limits: no source authentication, provenance truth, registry, arbitrary graph,
self-edge policy, fixed-roster coverage, PAL A3 definition, or authority
claim. Flat cycle validation is not implemented; acyclicity is not asserted.
