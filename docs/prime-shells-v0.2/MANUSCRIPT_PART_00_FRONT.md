---
title: "Framed Prime Shells"
subtitle: "Local Frames, Shell Atlases, and Trace-Bearing Ribbons in the Eisenstein Lattice"
author: "Christopher D. Pang"
date: "Working manuscript v0.2 - 4 September 2026"
---

**Reserved record:** 10.5281/zenodo.22288471  
**Status:** Author working manuscript; v0.1 local core verified; v0.2 successor formal core verified; not adopted, peer reviewed, or published  
**Formal branches:** `agent/prime-shells-conjugate-frames` (v0.1) and `agent/framed-prime-shells-v0.2-atlas-ribbons` (v0.2)  
**Draft pull requests:** `Grativy6/PAL-Lean-Audit#9` and stacked successor `#10`

> **Claim status.** Classical Eisenstein prime-shell arithmetic remains source-side mathematics. Version 0.1 formally proves the minimum-reference, sharp-frame, condition-number, and characterized-transport package. Version 0.2 formally verifies exact derived-axis invariance, independent-axis refinement, an indexed framed-shell atlas, ordered ribbons, and endpoint-determined composite transport. The Smith chart appears only as an established external engineering realization of the three chart roles. Global novelty remains open pending systematic literature and expert review. The reserved DOI is a publication handle, not mathematical evidence.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# Abstract

Let

$$\eta=e^{i\pi/3},\qquad Q(a,b)=N(a+b\eta)=a^2+ab+b^2,$$

and define the Eisenstein norm shell

$$S_n=\{(a,b)\in\mathbb Z^2:Q(a,b)=n\}.$$

Classical arithmetic gives six points for the ramified prime $3$, twelve points arranged in two conjugate six-point unit orbits for every split rational prime $p\equiv1\pmod3$, and an empty norm-$p$ shell for every inert prime $p\equiv2\pmod3$. Version 0.1 asked what additional data turns one occupied arithmetic shell into a stable planar frame. Version 0.2 asks what happens when those framed shells are organized as a family and an ordered route is retained through that family.

The v0.1 result is preserved unchanged: one marked vector cannot span the plane; a suitable vector and its arithmetic conjugate do; among three antipodally distinct unit rotations, one pair has squared normalized area at least $3/4$ and squared Euclidean condition number at most $3$; both constants are sharp at the norm-$3$ shell; and two corresponding references uniquely determine a composable linear transport.

The new result separates three chart roles. A coordinate derived entirely from an existing trace does not refine its fibers. A separately retained coordinate produces the exact joint relation

$$K\!\left(\langle\tau,\lambda\rangle\right)=K(\tau)\cap K(\lambda),$$

and strictly refines the interface whenever it separates one pair collapsed by $\tau$. Applying this distinction to represented rational primes gives a framed prime-shell atlas whose entries retain shell address, selected conjugate frame, readiness, area bound, and condition-number bound. A prime-shell ribbon is then a nonempty ordered sequence of atlas entries. Its route can differ while its endpoints agree. The existing transport is flat: composing transport along any finite ready ribbon equals direct endpoint transport, so path history remains in the ribbon rather than in the endpoint map.

The Smith chart supplies an external realization of the same taxonomy. Stereographic lifting makes a derived spherical state chart; adjoining frequency, time, temperature, bias, or another independent condition makes a shell-indexed family; and one realized sweep makes a trace-bearing ribbon through that family. Existing spherical and 3D Smith-chart work controls that engineering precedent. No new Smith chart, RF theorem, physical prime model, RH route, or prime-gap result is claimed.

The complete v0.1 core and the v0.2 interface, sphere, atlas, ribbon, and transport results are formalized in Lean 4.32.1 with Mathlib 4.32.1. The full arbitrary-prime representation and orbit-count theorem remains cited classical input rather than a newly formalized theorem in this package.

***Keywords:** Eisenstein integers; norm shells; framed shells; indexed atlases; ribbons; kernel relations; stereographic projection; Smith chart; condition number; transport; Lean 4*

# Document map

| **Section** | **Role** |
|---|---|
| 1 | Fixes the object, v0.1-to-v0.2 succession, contribution, and claim ceiling. |
| 2 | Establishes Eisenstein coordinate algebra and reflection coordinates. |
| 3 | Separates classical prime-shell arithmetic from the new construction. |
| 4 | Proves the minimum-reference and unique-reconstruction results. |
| 5 | Proves the three-choice selector from two exact polynomial identities. |
| 6 | Derives sharp normalized-area and condition-number bounds. |
| 7 | Proves sharpness at the norm-$3$ shell. |
| 8 | Defines and characterizes shell-to-shell transport. |
| 9 | Specializes the frame theorem to represented rational primes. |
| 10 | Separates derived-axis redrawings from independent-axis refinements. |
| 11 | Defines the framed prime-shell atlas. |
| 12 | Defines ordered prime-shell ribbons and proves flat composite transport. |
| 13 | Uses three Smith charts as an external engineering realization. |
| 14 | Records the two-stage Lean verification boundary. |
| 15 | Preserves literature limits, nonclaims, and publication burdens. |

# 1. Orientation and claim boundary

A **prime shell** in this paper is an exact norm level set in the Eisenstein lattice. It is not a physical shell, an electron shell, a probability distribution, a zeta-zero packet, or a mechanism for the Riemann Hypothesis.

The paper keeps three roles separate.

1.  **Classical arithmetic.** Eisenstein factorization and representation theory determine shell occupancy, point counts, and unit-orbit structure.
2.  **Framed-shell construction.** A selected point, its arithmetic conjugate, a unit-rotation choice, a conditioning functional, and a shell-to-shell comparison law turn an occupied shell into a framed object.
3.  **Geometric exposition.** The author supplies the intuitive account of why two references stop a shell from floating, why three unit choices suffice, how a frame approaches collapse, and what shell transport means.

The geometric account may orient the mathematics; it does not replace a theorem or strengthen its scope.

> **AUTHOR GEOMETRY INSERT 1 — THE SHELL BEFORE THE FRAME**  
> Explain the difference between the continuum level $Q(x) = n$ and the finite lattice points $S_{n}$ occupying it. The norm fixes the unmarked shell; framing asks for additional carried relation. Suggested figure: one occupied split-prime level beside one empty inert-prime level, with continuum and lattice occupancy labeled separately.

## 1.1 Candidate contribution

The classical shell classification is not new. The candidate contribution is the following integrated theorem package:

- a selected point and its arithmetic conjugate furnish the minimum internal reference pair for a planar shell frame;
- among three antipodally distinct unit choices, one pair is uniformly far from collapse;
- its squared normalized area is at least $3/4$ and its squared Euclidean condition number is at most $3$;
- both constants are sharp at the norm-$3$ shell; and
- two corresponding references uniquely determine a composable linear transport between ready shell frames.

This package is formally checked. Its global priority remains unresolved until a dedicated literature and expert review is complete.

# 2. Eisenstein coordinate algebra

Use the sixth root

$$\eta = e^{i\pi/3},\quad\quad\eta^{2} = \eta - 1,$$

and write an Eisenstein integer as

$$x = a + b\eta,\quad\quad a,b \in \mathbb{Z}.$$

In the $(1,\eta)$ basis, multiplication is

$$(a,b)(c,d) = (ac - bd,\ ad + bc + bd).$$

Arithmetic conjugation and multiplication by the unit $\eta$ are

$$\overline{(a,b)} = (a + b, - b),$$

$$R(a,b) = ( - b,a + b).$$

The norm is

$$N(a,b) = a^{2} + ab + b^{2}.$$

## Proposition 2.1 — Coordinate identities

For all coordinate points $x,y$,

$$\overline{\bar{x}} = x,\quad\quad R^{6}x = x,$$

$$N\left( \bar{x} \right) = N(x),\quad\quad N(Rx) = N(x),$$

$$N(xy) = N(x)N(y),\quad\quad x\bar{x} = N(x).$$

### Proof

Each statement follows by substitution in the displayed coordinate operations and polynomial normalization. The Lean proofs use only the declared commutative-ring structure for the algebraic identities. The fixed-point equation $Rx = x$ gives $- b = a$ and $a + b = b$, hence $a = b = 0$. Therefore no positive shell contains a point fixed by the full sixty-degree unit rotation. ∎

## 2.1 Conjugation eigen-coordinates

Define

$$X(x) = 2a + b,\quad\quad Y(x) = b.$$

Then

$$X(x)^{2} + 3Y(x)^{2} = 4N(x).$$

The ordinary Euclidean embedding is

$$E(x) = \frac{1}{2}\left( X(x),\sqrt{3}\, Y(x) \right),$$

and conjugation becomes reflection:

$$E\left( \bar{x} \right) = \frac{1}{2}\left( X(x), - \sqrt{3}\, Y(x) \right).$$

In the integer-scaled carrier, set

$$u_{x} = (X,Y),\quad\quad w_{x} = (X, - Y).$$

Their determinant is

$$\det\left( u_{x},w_{x} \right) = - 2XY.$$

Thus the pair is nonparallel exactly when

$$X \neq 0\quad\text{and}\quad Y \neq 0.$$

We call such a point **frame-ready**.

> **AUTHOR GEOMETRY INSERT 2 — THE REFLECTED PAIR**  
> Show $x$ and $\bar{x}$ as two rays from a supplied center. Their common component fixes the reflection-axis direction; their opposed component fixes the across-axis orientation. Mark the parallelogram area as the noncollapse witness. The center is supplied; an affine frame without a supplied center needs three noncollinear points.
