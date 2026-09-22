# Candidate clarification for PAL v2.3.1

**PROPOSED — not an adopted release, source amendment, or new admission rule.** The version label records Christopher's current direction for discussing these clarifications. The Lean audit cannot select the release number or authorize adoption.

## Suggested clarification text

For freeze `f : S_work → C_work` and thaw `r`, exact work re-entry means `r(f(w)) = w` for every declared work state in scope. Capsule reconstruction `f(r(c)) = c` is a different equation on a different domain. Even a clean capsule roundtrip, or a stable repeated freeze/thaw cycle, does not establish exact recovery of the original work state. Conversely, exact work re-entry makes no claim about decoding unreachable capsules.

A claim to preserve a requested answer must name the answer `q`, its work domain and its reachable decoder domain. An answer decoder on the reachable capsules exists exactly when the answer is constant on the capsule's fibers. This existence claim does not validate an arbitrary thaw implementation. For a chosen thaw that preserves the reachable capsule, `f(r(f(w))) = f(w)`, the same fiber condition is equivalent to that thaw preserving `q`. Changing the requested answer, thaw or continuation requires checking the relevant condition again. Selected-answer preservation must not be reported as exact work-state recovery.

Any distinction lost inside the declared work state defeats the exact capsule profile. Differences in separately typed non-work coordinates remain subject to their existing binding, revalidation, residual and reopening requirements. Approximate migration continues to require a separately declared adapter. Mathematical reconstruction does not establish storage persistence, restore spent resources or expired grants, recreate missing evidence, or confer token authority.

Administrative recurrence and productive recurrence remain separate as already specified by M-A13-STUTTER. Repeated checkpoint activity alone establishes neither progress nor liveness.

## Adoption boundary

These paragraphs make existing scopes and invalid inferences explicit. They leave the A12 exact work-roundtrip requirement and A13 cadence obligations intact. That is a plausible patch-level clarification, subject to the author's release policy.

Admitting a lossy representation as **exact** A12 recovery would change the existing requirement. A new answer-level or approximate adapter would need its own specification and review, even if published in the same document package. This proposal does not add one. No entropy assumption or new PAL layer is proposed.
