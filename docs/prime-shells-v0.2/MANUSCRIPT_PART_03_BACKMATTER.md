# 14. Formal verification account

Version 0.2 preserves the five v0.1 theorem modules and adds two successor modules:

    PAL/PrimeShells.lean
    PAL/PrimeShellsModThreeKernel.lean
    PAL/PrimeShellsConditioning.lean
    PAL/PrimeShellsBasisTransport.lean
    PAL/PrimeShellsConditionNumber.lean
    PAL/PrimeShellsThreeCharts.lean
    PAL/PrimeShellsRibbons.lean

The corresponding dependency receipts are generated from seven audit modules. The v0.1 and v0.2 workflows are separate so the successor does not rewrite the earlier formal receipt.

The v0.2 modules formalize:

1. derived-axis fiber invariance;
2. joint-fiber intersection and a strict-refinement witness;
3. the stereographic sphere equation, exact image inverse, and injectivity;
4. the exact product shell atlas and radial shell-radius identity;
5. represented-prime atlas occupancy inherited from the sharp selector;
6. generic and prime-shell ribbon structures;
7. finite ready-ribbon transport reduction to endpoints; and
8. an explicit same-endpoint/different-route prime-shell fixture.

The formal environment remains pinned to Lean 4.32.1 and Mathlib 4.32.1. The dedicated successor workflow compiles the new module chain, captures dependency receipts, requires both v0.2 receipt files, rejects dependencies outside `propext`, `Classical.choice`, and `Quot.sound`, runs the repository proof-hole policy, and uploads the exact build record.

**Verification receipt.** The v0.2 theorem-source freeze is commit `450e808325743b130c2f6cb3cf7496a7bb3a7556`. Dedicated workflow run `33837570265` completed successfully in Lean 4.32.1 with Mathlib 4.32.1 at revision `520045ab14e26149ee970e2e617ca04b09bde5d6`. The complete module chain built in 8,660 jobs. Two required v0.2 dependency files exposed 26 unique publication-facing declarations; the fail-closed gate admitted only `propext`, `Classical.choice`, and `Quot.sound`; and the repository policy passed across 25 Lean files. Receipt artifact `9923832727` has SHA-256 `6d90e1b47924c2bd1356eb7956ebd81cc36c1983377ad42bc8e2a5ff76672191`. Together with the preserved 62-declaration v0.1 receipt, the stacked formal package exposes 88 publication-facing declarations.

This formal receipt establishes only the exact Lean statements under the pinned environment. It does not establish the imported classical prime classification, global novelty, engineering validity of a Smith-chart measurement, author adoption, peer review, or publication authority.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 15. Literature boundary and open burdens

U. P. Nair supplies elementary representability background for $a^2+ab+b^2$. Oscar Marmon supplies the Eisenstein/hexagonal shell count, split/ramified/inert classification, and angular structure. Standard linear algebra supplies basis, determinant, singular-value, and condition-number concepts. PAL v2.3-M / RAINBOW supplies the author's prior research address for shell and local-frame language. Abstract Loops and Compactification Costs supply same-lineage fixed-interface fiber language. GPPR and GOLD supply same-lineage endpoint-versus-route precedents.

Phillip H. Smith's transmission-line calculator supplies the classical engineering chart. Later spherical and 3D Smith-chart work maps the extended reflection-coefficient plane to a Riemann sphere and uses additional scalar or frequency-dependent structure for multi-parameter visualization. Those sources govern the Smith-chart precedent; this manuscript does not backdate its atlas/ribbon terminology into them.

The v0.2 candidate contribution is narrower: the exact three-role taxonomy as applied to framed prime shells, the dependent atlas of certified represented-prime frames, and the explicit theorem that the current shell transport is endpoint-determined while an ordered ribbon retains route history. Initial targeted searching has not established that this complete package is globally novel.

## 15.1 Explicit nonclaims

This manuscript does not claim:

- a proof or new route to the Riemann Hypothesis, twin primes, or a prime-gap bound;
- a new classification of Eisenstein primes or a new proof of the classical shell counts;
- invention of the ordinary, spherical, generalized, or 3D Smith chart;
- that a third visual coordinate necessarily adds information;
- that the prime label is independent when the starting trace already contains exact Eisenstein coordinates;
- that a smooth drawn ribbon is the exact arithmetic object;
- nontrivial holonomy or path-dependent transport under the present flat transport law;
- a physical shell, particle model, wavefunction, force law, RF-prime coupling, or cosmology;
- that the selected unit choice is canonical without a tie-break rule;
- that exact real-number conditioning guarantees every finite-precision implementation; or
- that Lean compilation establishes source truth, global novelty, peer review, author adoption, or publication authority.

## 15.2 Work remaining before publication

1. Christopher D. Pang's intuitive geometry and final figures for the seven marked inserts.
2. Systematic literature and priority review of both the v0.1 selector and the v0.2 atlas/ribbon integration.
3. Independent mathematical review of the sharp constants, atlas typing, and flat-ribbon theorem.
4. Freeze the publication release manifest around the successful v0.2 Lean receipt and final reviewed manuscript bytes.
5. Optional end-to-end Lean reconstruction of the classical arbitrary-prime representation and orbit-count theorem.
6. Optional empirical work testing whether any particular atlas or ribbon visualization improves a declared engineering or computational task.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Conclusion

A shell knows its arithmetic level. A frame knows how that shell is locally oriented. An atlas knows which framed states are available under their retained indices. A ribbon remembers the route actually taken through them.

Version 0.1 established the local frame and proved that sixfold unit symmetry always supplies one of three conjugate-pair choices with sharp protection against collapse. Version 0.2 establishes the next scale. A derived axis can redraw the same state without adding a distinction. An independent axis can refine the interface. The resulting atlas is a family of framed shell states, while a ribbon is an ordered history inside that family.

The existing transport then reveals its own limit cleanly: every finite composite closes to the endpoint map. The route has not vanished; it was never stored in that map. It remains in the ribbon. That separation is the central v0.2 result.

# References

1. Marmon, Oscar. "Hexagonal Lattice Points on Circles." arXiv:math/0508201, 2005.
2. Nair, Umesh P. "Elementary Results on the Binary Quadratic Form $a^2+ab+b^2$." arXiv:math/0408107, 2004.
3. Pang, Christopher D. *PAL v2.3: Primitive Axiom Layers*. Mathematical Realization Atlas, RAINBOW section. Zenodo, 2026. DOI 10.5281/zenodo.22240134.
4. Pang, Christopher D. *Abstract Loops: Joint Certification, Generative Coupling, and the Cut Inside the Composite*. v1.0. Zenodo, 2026. DOI 10.5281/zenodo.21950771.
5. Pang, Christopher D. *Compactification Costs: A Typed Framework for Extension, Boundary, Identification, and Ambiguity*. v0.2. Zenodo, 2026. DOI 10.5281/zenodo.22238012.
6. Pang, Christopher D. *Golden Phase Prime Ribbons*. GPPR v0.1. Zenodo, 2026. DOI 10.5281/zenodo.22225414.
7. Pang, Christopher D. *GOLD: Golden-Oriented Lens Diagram*. v0.1. Zenodo, 2026. DOI 10.5281/zenodo.22236848.
8. Smith, Phillip H. "Transmission Line Calculator." *Electronics* 12, no. 1 (January 1939): 29-31.
9. Caspers, F. "RF Engineering Basic Concepts: The Smith Chart." arXiv:1201.4068, 2012.
10. Zelley, Chris. "A Spherical Representation of the Smith Chart." *IEEE Microwave Magazine* 8, no. 3 (2007): 60-66. DOI 10.1109/MMW.2007.365060.
11. Muller, Andrei A., P. Soto, D. Dascalu, D. Neculoiu, and V. E. Boria. "A 3-D Smith Chart Based on the Riemann Sphere for Active and Passive Microwave Circuits." *IEEE Microwave and Wireless Components Letters* 21, no. 6 (2011): 286-288. DOI 10.1109/LMWC.2011.2132697.
12. Muller, Andrei A., et al. "3D Smith Charts Scattering Parameters Frequency-Dependent Orientation Analysis and Complex-Scalar Multi-Parameter Characterization Applied to Peano Reconfigurable Vanadium Dioxide Inductors." *Scientific Reports* 9 (2019). DOI 10.1038/s41598-019-54600-5; arXiv:1905.09701.
13. Asavei, Victor, Andrei A. Muller, Esther Sanabria-Codesal, Alin Moldoveanu, and Adrian M. Ionescu. "3D Smith Chart Constant Quality Factor Semi-Circles Contours for Positive and Negative Resistance Circuits." arXiv:2006.13315, 2020.
14. Lean Prover Community. *Mathlib 4*, release v4.32.1, 2026.
15. Pang, Christopher D. *Framed Prime Shells Formal Package*. v0.1 draft branch `agent/prime-shells-conjugate-frames`, pull request 9; v0.2 successor branch `agent/framed-prime-shells-v0.2-atlas-ribbons`, pull request 10. `Grativy6/PAL-Lean-Audit`, 2026.

# Authorship and AI-assistance disclosure

Christopher D. Pang is the sole author, steward, and adoption/publication authority. He supplied the originating shell-frame intuition, recognized the sphere/atlas/ribbon distinction, selected the v0.2 direction, and remains responsible for the final geometry, claims, citations, and release. OpenAI ChatGPT and connected coding tools assisted with retrieval, mathematical exploration, Lean formalization, proof repair, figures, and document production. They are tools, not authors, co-authors, witnesses, stewards, or mathematical authorities.
