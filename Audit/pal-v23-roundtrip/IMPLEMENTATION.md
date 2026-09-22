# PAL v2.3 round-trip audit implementation notes

This local supplement formalizes the exact work-state law in PAL v2.3-M A12: thaw after freeze is identity on declared work states. It also separates that premise from the different capsule-cycle equation, freeze after thaw, and from preservation of one chosen answer.

The generic results use arbitrary types `W`, `C`, and `Q`, with no algebraic structure on the answer type. The fiber criterion assumes only reachable-image consistency, `freeze (thaw (freeze w)) = freeze w`; it imposes nothing on unreachable capsules. The separate idempotence and injectivity-equivalence theorems state their stronger, ambient capsule-cycle condition explicitly. The target-specific generic result preserves any fixed suffix when work round-trip holds.

The explicit `Nat × Bool` projection fixture shows the boundary: capsule round-trip and stable repeats hold, but the chosen thaw loses the Boolean field. A total decoder cannot recover both colliding work states. The Nat answer survives and the Bool answer does not. A separate bad-thaw fixture shows fiber constancy alone does not certify the chosen thaw. Finally, the `n ↦ n+1` / predecessor example satisfies exact work round-trip while failing capsule-cycle at unreachable capsule zero, confirming the reachable-vs-ambient boundary.

The standalone axioms module checks all 17 declarations and prints their axiom dependencies. Lean reports no axioms for the declarations except `propext` for the Nat predecessor countercase. No `sorry`, `admit`, or custom axiom is introduced.

These are bounded set-theoretic function results and explicit fixtures. They do not verify serialization code, actual persistence, environment identity, operational suffix execution, a general decoder algorithm, non-work-coordinate recovery, or any PAL adoption or authority claim. The controlling source snapshot is PAL-v2.3-M, SHA-256 `c053292376363edd6fc743f0f2e31e3bb3850edc78ade3a289bbb07e7e8452c5`; source paragraph numbering follows the stored Word paragraph enumeration.
