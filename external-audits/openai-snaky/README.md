# Snaky: a win with a ceiling

A second math-shelf visit for Chris, begun October 7 and written October 8, 2026.
Source: OpenAI's *Snaky in 21 Maker moves*, pinned to
adc7f1241b42e322a6451854ab7e4b4c146bf78a.

Start with **Snaky-a-win-with-a-ceiling.pdf**, a four-page illustrated companion.
It explains the game, a two-way finishing fork, and how a finite certificate
gives a guarantee against every legal opponent. Twenty-one is an upper bound,
not a proved minimum.

**AUDIT.md** has the exact claim, dependencies, checks, and limits.
The selected source and its license are under source/. The evidence/ folder
records source/build identity. The computations/route21-001/ folder holds
the successfully reproduced finite checks and validated manifest.

Current state: the selected written argument and finite certificate checked out.
The separate Lean rerun is **PARTIAL_RESOURCE**: 83 of 94 proof modules compiled
before its 30-minute limit, with no completed theorem comparison or kernel
replay. Its cached progress and exact remaining modules are preserved.

The final machine-readable record is evidence/verification-results.json.
Source/build/dependency integrity passed. SHA256SUMS records the retained
documents, source, computation results, scripts, and evidence.

The standalone TeX remains editable. Its native compiler hit a setup error,
so its compilation is unverified. The readable PDF was generated separately,
and its pages were visually checked.

The prior pi visit and PAL-lean workbench are separate. This work did not
modify Branchline, publish anything, or start another agent.
