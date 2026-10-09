# Fourier savings: the connection in Chris’s corpus

Checked 8 October 2026. This is a source comparison and a small check of the displayed constants. It is not an independent verification of the Fourier theorem or a completed Lean run.

The closest corpus connection is **Finite Abstraction Between the Riemann Hypothesis and P versus NP**, followed by **Abstract Loops**, **Compactification Costs**, and **Golden Phase Prime Ribbons (GPPR)**. They separate information being available, a decoder existing, an allowed procedure constructing the answer, and that procedure meeting a uniform resource bound. This supplies a precise way to examine the Fourier claim. No missing Fourier lemma or counterexample was found in the searched material.

## The concrete distinction

The listed `ExactFourier` formal target says: for every positive fraction c and every starting threshold N, some length n at least N has an exact Fourier circuit costing less than c n log₂ n. Its companion manuscript expresses this as a zero lower limit of the normalized minimum circuit cost. Circuits and their coefficients may depend on the length. This rules out a universal eventual Ω(n log n) lower bound in that circuit model, but does not by itself give one fast algorithm at all sufficiently large lengths.

The headline promises a stronger result: one deterministic algorithm at every positive length, with the fixed asymptotic bound O(n(log n)^(1−10^−13)), under its specified exact-arithmetic and root-supply assumptions.

An elementary illustration of the quantifier distinction: a hypothetical cost equal to n at powers of two and n log n at all other lengths has normalized lower limit zero, yet its normalized cost does not tend to zero. This is only a logical illustration; it is not a model of actual Fourier circuit costs.

Sources: [formal target](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/ComparatorChallenges/ExactFourier.lean), [companion introduction](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/Finite-tensor-savings-and-exact-Fourier-circuits-September-25-2026/build/sections/01-introduction.tex), [solution entry point](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/Computability/FourierCircuit/Main.lean).

## The bridge is present in the manuscript

The explicit DFT paper recognizes the extra obligation and supplies its own construction. It does not simply promote the nonuniform circuit-existence statement into a uniform algorithm. Its main route uses an explicit finite phase network, an exact-width compiler for local Fourier transforms, and synchronized tensor scheduling. The final reduction selects a working length L between 2n and 4n, then uses chirp convolution to handle the requested length. The paper charges the transformed fixed convolution operand, scalar preparation, and array organization.

A focused next proof audit would inspect whether the claimed recurrence survives borrowed workspace and every role, whether local compilation and preparation stay within their bounds, and whether sector traversal avoids an extra per-axis cost at every entry. Those are obligations to check, not defects established by this investigation. I read the introduction and all-length reduction and inspected the appendix’s role; I did not independently verify all underlying constructions.

Sources: [construction and scope](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/introduction.tex), [working lengths and accounting](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/all-lengths.tex).

## What each corpus source contributes

- **Finite Abstraction Between RH and P vs NP v0.1**, §§1–3.1: finite descriptions can legitimately support unbounded conclusions; the question is which theorem earns their coverage. Its four prompts—scope, carrier, bridge, residual—apply directly to the change of quantifiers above.
- **Abstract Loops v1.0**, §4: a static factorization does not show that an allowed machine can realize the decoder. It explicitly distinguishes a uniform constructive strategy from pointwise existence of a successful branch.
- **Compactification Costs v0.2**, §4.5: set-theoretic recoverability alone does not establish an efficient or computable decoder. Its cost profile is typed; it is not itself a Fourier complexity theorem or a claim that every representation change has a positive computational cost.
- **GPPR v0.1**, §§7, 9.5, 10: exact complex encoding and finite-precision usability require different evidence. It also requires upstream preparation, transport, precision refinement, and fallback to be included in performance comparisons. Its geometric construction supplies no demonstrated acceleration for this DFT algorithm.

The preserved source extracts are in `corpus-extracts/`; `corpus-source-records.json` records their locations and hashes. These are September 2026 extractions, reread now, not a claim to have searched every later corpus revision. Some equations were omitted by the old extraction, so this comparison relies on the cited prose rather than reconstructing those equations. Corpus originals were not changed.

## Where the nines come from

The paper sets m=10^6, W=2^71, Δ=6871402692000000 and θ=log_m(m−Δ/W). Its sharper bound includes a (log log n)^(4−θ) factor. The spare exponent margin absorbs that factor eventually, giving the simpler 1−10^−13 corollary. The tiny saving has a stated finite-network origin.

Exact rational arithmetic confirms Δ/(mW)=1717850673/590295810358705651712 and the stated lower estimate 28/10^13. An 85-digit decimal evaluation reproduces θ≈0.99999999999978935615699598. This checks the displayed arithmetic only; it does not validate the claimed network saving. See `displayed-constants-check.json`.

Source: [final estimates](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/preprints/An-explicit-power-saving-for-the-exact-discrete-Fourier-transform-September-25-2026/build/sections/all-lengths.tex).

## Boundaries that matter

The uniform model counts exact complex field operations at unit cost and supplies one specified root of unity; the logarithmic word bound applies to addresses. A bit-level implementation has additional obligations involving representation and numerical behavior. This is an explicit model boundary, not evidence that the arithmetic saving is fictitious. A finite-capacity collision argument from APCI cannot simply be applied to unrestricted exact complex registers without first establishing a finite-capacity interface.

The right practical wording is that no stable floating-point speedup or useful crossover estimate is established here. “Practically useless” is a broader verdict than this source check earns.

The `sorry` in the comparator challenge file is its target placeholder; the designated solution has a separate proof entry point. I did not treat the placeholder as a discovered proof hole, and I did not rerun the comparator or Lean kernel for this family.

## Evidence retained

OpenAI repository revision: fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb. Nineteen selected source files were retrieved from that revision and their SHA-256 values rechecked against `source-manifest.json`. No source file was executed. The prior π and Snaky shelf records were left intact.

Search scope: the preserved Math Stack and Software Stack text extracts, selected adjacent corpus sources above, the two Fourier manuscripts’ stated interfaces, and the listed formal target and solution entry point. No global novelty, complete corpus coverage, or full proof-correctness claim is made.
