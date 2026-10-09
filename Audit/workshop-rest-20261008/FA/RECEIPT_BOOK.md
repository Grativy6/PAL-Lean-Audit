# Finite Abstraction v0.1 — workshop receipt book

The selected coverage and quantifier suite passed its local build, exact type/axiom inspection and bundled Lean kernel replay on 8 October 2026. [Execution receipt](../FA-A/results.json) · [Review](../FA-A/REVIEW.md) · [Frozen target](../FA-A/TARGET.md) · [Editable Lean](../../../Experiments/FiniteAbstractionControls.lean).

The checked controls preserve both sides of the paper's distinction:

- A finite prefix or arbitrary finite tested set leaves an untested countercase for a suitably chosen predicate.
- A short induction proves an identity for every natural number.
- Per-size bounds do not supply a single constant bound, although the same witnesses may have a simple uniform construction.
- A deliberately truncated trace fails to recover identity because of a demonstrated collision.
- Finite records whose lengths grow with input can preserve every natural number exactly.

The existing reachable-fiber criterion is reused from AbstractLoopsJoint, with the same mathematical dictionary as APCI. Existing capacity evidence remains in AbstractLoopsFiniteImage. Neither reused theorem is counted as independent corroboration here.

These are accurately labeled models for a bounded synthesis. They do not prove a result about RH, P versus NP, runtime lower bounds, independence or all finite abstractions. No source correction was found in the selected distinctions. The inventory contains eleven explicit declarations, including ten theorems and controls. Only standard Lean axioms occur. [Source identity](../source-manifest.json) and [clarifications](../CLARIFICATIONS.md) remain separate from source adoption.
