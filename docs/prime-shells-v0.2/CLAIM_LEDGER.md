# Framed Prime Shells v0.2 claim ledger

**Working title:** *Framed Prime Shells: Local Frames, Shell Atlases, and Trace-Bearing Ribbons in the Eisenstein Lattice*  
**Reserved record:** `10.5281/zenodo.22288471`  
**Author / steward / adoption authority:** Christopher D. Pang  
**v0.1 formal branch:** `agent/prime-shells-conjugate-frames`  
**v0.2 successor branch:** `agent/framed-prime-shells-v0.2-atlas-ribbons`  
**Status:** verified formal working successor; not merged into the base branch, adopted, peer reviewed, or published

## Verification boundary

- v0.2 theorem-source freeze: `450e808325743b130c2f6cb3cf7496a7bb3a7556`
- dedicated workflow: `Framed Prime Shells v0.2 Lean`
- workflow run: `33837570265`
- result: `SUCCESS`
- Lean: `4.32.1`
- Mathlib release: `v4.32.1`
- Mathlib revision: `520045ab14e26149ee970e2e617ca04b09bde5d6`
- v0.2 module-chain build: `8660` jobs completed successfully
- v0.2 publication-facing dependency inventory: `26` unique declarations in `2` required receipt files
- allowed logical dependencies: `propext`, `Classical.choice`, `Quot.sound`
- repository proof-hole and lexical policy: passed across `25` Lean files
- receipt artifact ID: `9923832727`
- receipt artifact SHA-256: `6d90e1b47924c2bd1356eb7956ebd81cc36c1983377ad42bc8e2a5ff76672191`
- stacked v0.1 + v0.2 publication-facing inventory: `88` declarations (`62 + 26`)

The formal receipt establishes only the exact declarations under the pinned environment. It does not establish source adequacy, imported classical shell arithmetic, global priority, engineering utility, author adoption, peer review, or publication authority.

## Source roles

- **Framed Prime Shells v0.1:** local conjugate-frame construction, sharp area and condition-number constants, and characterized shell transport.
- **Classical Eisenstein arithmetic:** representability and shell/orbit counts; imported, not reconstructed end to end here.
- **Abstract Loops / Compactification Costs:** exact common-refinement and side-information fiber language; same author-led lineage, not independent corroboration.
- **GPPR / GOLD:** endpoint-versus-route and trace-bearing path precedents; same lineage, not independent corroboration.
- **Smith-chart literature:** external engineering realization of a state sphere, indexed parameter family, and realized sweep; not a premise of the prime-shell theorem.

## Claims

| ID | Claim | Class | Evidence / declaration | Ceiling or residual |
|---|---|---|---|---|
| FPS2-01 | A deterministic added coordinate `h ∘ τ` has exactly the fibers of `τ`. | `LEAN_PROVED` | `derivedAxis_sameFiber` | A representational lift, not an information gain. |
| FPS2-02 | A joint trace `<τ, λ>` has fiber relation `K(τ) ∩ K(λ)`. | `LEAN_PROVED` | `jointAxis_sameFiber` | Standard product equality; no causal or statistical independence claim follows. |
| FPS2-03 | If `λ` separates one pair collapsed by `τ`, the joint trace strictly refines `τ`. | `LEAN_PROVED` | `jointAxis_strictly_refines_of_witness` | Requires a concrete separation witness. |
| FPS2-04 | A coordinate that factors through `τ` is definitionally a derived-axis lift, and the lift and source trace refine one another. | `LEAN_PROVED` | `jointAxis_eq_derived`, `derivedAxis_refinement_equiv` | “Independent” is relative to the declared starting interface. |
| FPS2-05 | The stated stereographic Smith-sphere lift lands on the unit sphere. | `LEAN_PROVED` | `normSq3_smithSphere` | Derived display of the planar state; no RF measurement theorem. |
| FPS2-06 | The lift has an exact left inverse on its image and is injective. | `LEAN_PROVED` | `smithSphereBack_smithSphere`, `smithSphere_injective`, `smithSphere_sameFiber` | Covers the chosen affine chart; the omitted pole is not represented by a finite planar coordinate. |
| FPS2-07 | The exact Smith shell atlas has fibers equal to state equality intersected with condition equality. | `LEAN_PROVED` | `smithAtlasPoint_sameFiber` | Product carrier is authoritative; radial nesting is a rendering. |
| FPS2-08 | Radial rendering puts every indexed state on its declared squared radius. | `LEAN_PROVED` | `radialSmithShell_normSq` | Does not prove the radius function is injective, calibrated, or physically meaningful. |
| FPS2-09 | A represented rational prime shell is supplied as `p` prime with an exact norm representation. | `DEFINITION` | `RepresentedPrimeShell` | The construction does not discover or prove the representation. |
| FPS2-10 | Every supplied represented prime shell admits a certified framed-atlas entry. | `LEAN_PROVED / V0.1-CONDITIONAL` | `representedPrimeShell_has_atlasPoint` | Consumes the v0.1 sharp selector and supplied representation. |
| FPS2-11 | A prime-shell ribbon is a nonempty ordered route through framed atlas entries. | `DEFINITION` | `Ribbon`, `PrimeShellRibbon` | Smooth visual interpolation is not arithmetic evidence. |
| FPS2-12 | Ribbon start, finish, edge count, and order survive map operations as stated. | `LEAN_PROVED` | `Ribbon.start_*`, `finish_*`, `edgeCount_*`, `*_map` | These data do not by themselves prove chronology or provenance. |
| FPS2-13 | Transport composed along any finite ready ribbon equals direct endpoint transport. | `LEAN_PROVED` | `ReadyRibbon.applyTransport_eq_direct`, `primeRibbonTransport_eq_endpoints` | The present connection is flat and endpoint-determined. |
| FPS2-14 | The explicit direct `3→13` and via-`7` `3→7→13` routes share endpoints but differ as routes. | `LEAN_PROVED` | `primeFrameRibbons_same_endpoints`, `primeFrameRibbons_different_routes` | Fixture only; not a distribution theorem about primes. |
| FPS2-15 | Those two different routes induce the same current transport. | `LEAN_PROVED` | `primeFrameRibbons_same_transport` | Route history remains in the ribbon, not in the endpoint map. |
| FPS2-16 | Nontrivial path-sensitive holonomy exists for these transports. | `OPEN / NOT ESTABLISHED` | None | Would require an added connection or path-sensitive structure. |
| FPS2-17 | The Smith sphere, nested parameter shells, and trace-bearing sweep are established engineering precedents. | `IMPORTED / SOURCE-SPECIFIC` | Smith; Caspers; Zelley; Muller et al.; Asavei et al. | Does not make prime shells an RF system or claim invention of 3D Smith charts. |
| FPS2-18 | The exact v0.2 integrated package is globally novel. | `OPEN_PRIORITY_REVIEW` | Targeted search only | Requires systematic database search, citation chaining, and expert review. |
| FPS2-19 | The construction advances RH, prime gaps, or a physical theory. | `EXCLUDED` | No bridge | Must remain outside theorem claims. |

## Reopening handles

- Reopen derived/independent classification when the starting trace changes.
- Reopen atlas occupancy if the represented-prime structure or v0.1 selector changes.
- Reopen flatness if transport is changed, enriched, or supplied path-sensitive data.
- Reopen Smith-chart interpretation when normalization, reference impedance, passivity assumptions, or independent-parameter semantics change.
- Reopen formal status on any Lean/Mathlib version change, failed receipt, unexpected dependency, or source edit.
- Reopen novelty on any equivalent prior theorem or construction found under different vocabulary.
