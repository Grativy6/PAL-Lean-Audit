# Candidate handoff for PAL v2.3.1

**Proposed wording and evidence handoff only.** This supplement neither creates a PAL release nor amends the source documents. Christopher D. Pang chooses the version, text and adoption. The preceding `Audit/pal-v23-roundtrip/PROPOSED-v2.3.1.md` is preserved; the following incorporates its distinctions with the new coverage.

## Cumulative candidate clarification

Exact work re-entry means that thawing a frozen state recovers that state on the declared work domain: `r(f(w)) = w`. Reconstructing a capsule after thawing it, `f(r(c)) = c`, is a different equation. A clean capsule cycle or a stable repeated cycle can coexist with loss of the original work distinction. Exact work re-entry does not require arbitrary unreachable capsules to reconstruct exactly.

A selected answer `q` can survive even when the whole work state does not. Its source domain, reachable trace domain and decoder class must be named. Reachable answer recovery is governed by constancy on trace fibers. Decoder existence alone does not validate a chosen thaw. For a chosen thaw that preserves reachable capsules, `f(r(f(w))) = f(w)`, answer preservation is equivalent to that fiber condition. Changing the answer or continuation requires checking the relevant preservation claim again.

Deterministic postprocessing of a trace cannot recover an answer distinction already lost by that trace. Repeating the same information under a new label also cannot repair it. A genuinely additional label can separate an obstructing pair; joint information can answer a question that neither component answers alone. Coarsening the requested question may remove an obstruction. For a supplied finite family of answer-distinct states in one trace fiber, a sufficient label must offer enough distinct values to separate that family.

Finite reverse replay requires a correct one-step recovery rule, the declared schedule, and the corresponding retained action records. Matching record count and site order is insufficient: a corrupted action value may pass both checks yet reconstruct a different state. Actual A2 admission still requires the source's complete binding, retention and successful recovery conditions; mathematical reconstruction from a supplied list does not prove those operational facts.

Administrative recurrence and productive recurrence remain distinct. A finite block of administration preserves a projection only under the declared per-step preservation rule. A productive macrostep can be surrounded by administration without losing its rank decrease when that administration also preserves the chosen rank. One way to justify this is to define the rank through a projection that administration preserves. Work preservation alone must not be treated as preservation of an unrelated rank. A strict natural-number rank then bounds the number of productive macrosteps. Activity counts alone supply none of those conditions, and endpoint equality can conceal intervening work changes. Infinite recurrence and liveness require their own stated semantics and evidence.

Differences in separately typed non-work coordinates remain subject to binding, revalidation, residual and reopening requirements. Reconstruction does not restore spent resources or expired grants, recreate evidence, establish storage persistence, or confer token authority. Approximate migration and answer-level adapters need separately declared profiles; they must not be presented as exact recovery of a larger work state.

## Editorial implication

These distinctions fit a clarification of existing scopes and obligations: the supplied v2.3 Atlas already includes the trace-lift, capsule and administrative/productive cadence cards. The new results support clearer statements and examples. They do not establish a missing PAL layer or a contradiction requiring a structural revision.

Admitting loss inside the declared work state while still calling the result exact A12 recovery would change the existing requirement. This handoff makes no such change. It introduces no entropy premise and does not close O04, O25 or D-FIRST-OCCURRENCE.

## Evidence and remaining work

Use `COVERAGE.md`, the claim ledgers and the verified receipt together. Mathematical hypotheses, concrete countercases and implementation evidence are different populations. The wider candidates in `OTHER-CANDIDATES.md` are proposals for later audits; they are not prerequisites invented for publishing this clarification and are not already checked by this batch.
