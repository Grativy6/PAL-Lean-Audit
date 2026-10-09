# APCI manuscript audit — 8 October 2026

Chris narrowed the active grant to APCI alone. This pass reads the copied APCI
v1.0.0 manuscript, maps it to the recovered formal core, and checks the remaining
written finite-interface corollary. It does not turn the five-paper workshop key.

## Finish criteria

1. Bind the DOCX/PDF bytes and manuscript-cited repository commit/tree.
2. Map Theorems 1–5, their boundaries, and Appendix A to the existing 15
   declarations and today's preserved replay.
3. Check §4.1's answer-class corollary with a new, separate Lean module. The
   alternative and ambient trace types remain arbitrary. Finite capacity is an
   injective labeling of the actual reachable trace subtype into `Fin n`.
4. Check three controls: a constant property on an infinite domain; recovery
   after supplying new side information; and total decoding when both trace
   and answer types are empty. These are scope tests, not new independent
   corroborating theorems.
5. Save exact commands, dependency output, source map, and a readable receipt
   book. Preserve the manuscript, original repository, and historical receipts.

## Claim and proof boundary

For arbitrary types W, T, Q, a trace τ : W → T, answer q : W → Q, natural n,
and witnesses w : Fin (n+1) → W, assume an injective labeling of Reachable τ
into Fin n and injectivity of q ∘ w. Then no decoder on the reachable traces
of τ ∘ w recovers q ∘ w exactly. This is the manuscript's §4.1 corollary,
expressed with explicit functions instead of an unstated cardinality library.

The proof reduces to the existing `fin_succ_has_collision` and
`exactOnReachable_implies_fiberConstant`. The source-to-formal translation
is a human/self-review obligation; kernel checking does not verify that mapping.

## Resources and outcomes

- Reuse installed native Lean 4.32.1, core plus bundled Std, no downloads.
- One supplementary module, one primary corollary and three controls.
- Sequential formal commands; at most three proof-repair attempts.
- Each compiler/checker invocation: 120-second timeout. Compiler: one thread,
  2,048 MB requested memory limit. One outer run: 360 seconds and 2 MiB logs.
- A kernel pass plus expected declaration/dependency checks is formal evidence
  for those exact statements. Compilation failure is not a counterexample.
- Preserve failed logs. A resource failure remains incomplete; do not silently
  grow the ceiling or extend to another paper.

Entropy's finite Shannon inequality receives a written algebra check only.
The thermodynamic citations, empirical capacity premises, stochastic/quantum
extensions, novelty, and unavailable predecessor ZIP bytes are outside this
bounded formal pass. No independent reviewer or external Rust checker pass is
claimed. No publication or remote writes are authorized by this work.
