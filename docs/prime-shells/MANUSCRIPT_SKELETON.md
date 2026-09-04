# Framed Prime Shells

## Minimal reference data, sharp conditioning, and composable transport in the Eisenstein lattice

**Author and steward:** Christopher D. Pang  
**Version:** working manuscript core, not adopted for publication  
**Reserved record:** `10.5281/zenodo.22288471`  
**Formal branch:** `agent/prime-shells-conjugate-frames`  
**License target:** manuscript and diagrams CC BY 4.0; Lean code Apache-2.0 under the repository license

> **Claim status.** The classical arithmetic of Eisenstein norm shells is source-side mathematics. The two-reference reconstruction, three-choice sharp frame selector, exact condition bound, and characterized shell transport are manuscript-side deductions checked in Lean 4.32.1 with Mathlib 4.32.1. Global novelty remains open pending systematic literature and expert review. The reserved DOI is a publication handle, not mathematical evidence.

## Abstract draft

Let

\[
\eta=e^{i\pi/3},\qquad Q(a,b)=N(a+b\eta)=a^2+ab+b^2,
\]

and define the Eisenstein norm shell

\[
S_n=\{(a,b)\in\mathbb Z^2:Q(a,b)=n\}.
\]

Classical arithmetic gives six points for the ramified prime \(3\), twelve points arranged in two conjugate six-point unit orbits for every split rational prime \(p\equiv1\pmod3\), and an empty norm-\(p\) shell for every inert prime \(p\equiv2\pmod3\). This paper asks a different question: what additional data turns an occupied arithmetic shell into a stable planar frame?

One marked vector cannot span the plane. A suitable vector and its arithmetic conjugate do, and every planar vector then has unique coordinates in that pair. More strongly, among the three antipodally distinct unit rotations of every nonzero Eisenstein-lattice vector, one conjugate pair has squared normalized area at least \(3/4\). In conjugation eigen-coordinates, the same choice has symmetric and antisymmetric axis energies within a factor of \(3\), so its squared Euclidean frame condition number is at most \(3\). Both constants are sharp at the norm-\(3\) shell. For any two ready shell frames, the unique map preserving real linear combinations and sending the selected and reflected source references to their target counterparts has a diagonal form and obeys exact identity, inverse, and composition laws.

The coordinate algebra, kernel-reduced modulo-three obstruction, minimal-reference theorem, sharp selector, coefficient uniqueness, condition-number result, and transport characterization are formalized in Lean. The full arbitrary-prime representation and orbit-count theorem is cited as classical input rather than claimed as newly formalized here.

---

## 1. Orientation and claim boundary

A **prime shell** in this paper is an exact norm level set in the Eisenstein lattice. It is not a physical shell, an electron shell, a probability distribution, a zeta-zero packet, or an RH mechanism.

The paper keeps three roles separate:

1. **Classical arithmetic.** Eisenstein factorization and representation theory determine shell occupancy, point counts, and unit-orbit structure.
2. **Framed-shell construction.** A selected point, its arithmetic conjugate, a unit-rotation choice, a conditioning functional, and a shell-to-shell comparison law turn an occupied shell into a framed object.
3. **Geometric exposition.** The author supplies the intuitive account of why two references stop a shell from floating, why three unit choices suffice, how a frame approaches collapse, and what shell transport means.

The geometric account may orient the mathematics; it does not replace a theorem or strengthen its scope.

> **Author geometry insert 1 - What a shell is.**  
> Explain the difference between the continuum circle \(Q(x)=n\) and the finite lattice points \(S_n\) occupying that level. The norm fixes the unmarked shell; framing asks for additional carried relation.

## 2. Eisenstein coordinate algebra

Use the sixth root

\[
\eta=e^{i\pi/3},\qquad \eta^2=\eta-1,
\]

and write

\[
x=a+b\eta,\qquad a,b\in\mathbb Z.
\]

In the \((1,\eta)\) basis,

\[
(a,b)(c,d)=(ac-bd,\ ad+bc+bd),
\]

\[
\overline{(a,b)}=(a+b,-b),
\]

and multiplication by \(\eta\) is the sixty-degree unit rotation

\[
R(a,b)=(-b,a+b).
\]

The norm is

\[
N(a,b)=a^2+ab+b^2,
\]

and the formal core proves

\[
N(xy)=N(x)N(y),\qquad N(\bar x)=N(x),\qquad N(Rx)=N(x),
\]

\[
x\bar x=N(x),\qquad R^6x=x.
\]

The only fixed point of \(R\) is the origin, so no positive shell contains a point fixed by a full sixty-degree rotation.

### 2.1 Conjugation eigen-coordinates

Define the scaled coordinates

\[
X(x)=2a+b,\qquad Y(x)=b.
\]

Then

\[
X(x)^2+3Y(x)^2=4N(x).
\]

The ordinary Euclidean embedding is

\[
E(x)=\frac12\bigl(X(x),\sqrt3\,Y(x)\bigr),
\]

and conjugation becomes reflection:

\[
E(\bar x)=\frac12\bigl(X(x),-\sqrt3\,Y(x)\bigr).
\]

The symmetric coordinate \(X\) is fixed by conjugation; the antisymmetric coordinate \(Y\) changes sign. In the integer-scaled carrier

\[
B_x^+=(X,Y),\qquad B_x^-=(X,-Y),
\]

one has

\[
\det(B_x^+,B_x^-)=-2XY.
\]

Thus the selected and reflected references are nonparallel exactly when

\[
X\ne0\quad\text{and}\quad Y\ne0.
\]

The formalization calls this predicate `FrameReady`.

> **Author geometry insert 2 - The reflected pair.**  
> Describe \(x\) and \(\bar x\) as two distinct rays from a supplied center. Their common component fixes the reflection-axis direction; their opposed component fixes the across-axis orientation. The center is supplied. Without a supplied center, the analogous affine frame needs three noncollinear points.

## 3. Classical prime-shell arithmetic

Let

\[
U=\{\eta^j:0\le j<6\}
\]

be the unit group. The classical prime classification is

\[
|S_p|=
\begin{cases}
6,&p=3,\\
12,&p\equiv1\pmod3,\\
0,&p\equiv2\pmod3.
\end{cases}
\]

For a split prime \(p\equiv1\pmod3\), choose \(\pi_p\) with

\[
p=\pi_p\overline{\pi_p}.
\]

Then

\[
S_p=U\pi_p\;\sqcup\;U\overline{\pi_p}.
\]

After quotienting by the six unit rotations, exactly two conjugate arithmetic classes remain.

The current Lean branch proves the elementary modular obstruction

\[
Q(a,b)\not\equiv2\pmod3,
\]

and therefore

\[
n\equiv2\pmod3\Longrightarrow S_n=\varnothing.
\]

The publication-facing proof uses ordinary kernel-reduced finite decision rather than the earlier native-decision certificate. Concrete occupied fixtures at norms \(3,7,13,19\) are also checked. The arbitrary split-prime existence theorem and the general six/twelve-point orbit count remain cited classical inputs.

Formal declarations:

```text
PAL.PrimeShells.norm_mod_three_kernel
PAL.PrimeShells.no_integer_shell_of_mod_three_two_kernel
PAL.PrimeShells.shell_seventeen_empty_kernel
```

## 4. Minimal reference data

The norm already identifies an unmarked shell as a set. A **framed shell** asks for enough internal relation to express arbitrary planar comparison without importing an undeclared second direction.

### Theorem 4.1 - One reference is insufficient

For every \(u\in\mathbb R^2\), there exists \(v\in\mathbb R^2\) that is not a scalar multiple of \(u\). Therefore one marked vector cannot span a two-dimensional real carrier.

```text
PAL.PrimeShells.one_reference_is_insufficient
```

### Theorem 4.2 - Two conjugate references reconstruct uniquely

Assume \(x\) is ready, so \(X(x)Y(x)\ne0\). For \(v=(r,s)\), define

\[
c_x(v)=\frac{r}{2X(x)}+\frac{s}{2Y(x)},
\]

\[
d_x(v)=\frac{r}{2X(x)}-\frac{s}{2Y(x)}.
\]

Then

\[
v=c_x(v)B_x^++d_x(v)B_x^-.
\]

Moreover, if

\[
v=cB_x^++dB_x^-,
\]

then

\[
c=c_x(v),\qquad d=d_x(v).
\]

Thus a ready selected/conjugate pair is a basis and its coordinates are unique.

```text
PAL.PrimeShells.two_references_reconstruct
PAL.PrimeShells.conjugate_references_independent
PAL.PrimeShells.conjugate_reference_coefficients_unique
```

This is the exact version of the intuition that two references are required for a shell to carry its own two-dimensional frame.

> **Author geometry insert 3 - What “stable” means.**  
> Separate three claims: the shell is stable as an unmarked norm level; one point may orient it relative to a supplied outside axis; two nonparallel internal references let it carry a complete local planar frame.

## 5. Three unit choices and the sharp selector

The six unit rotations contain three antipodal pairs. It is therefore enough to inspect

\[
x,\qquad Rx,\qquad R^2x.
\]

For \(x=(a,b)\), define their determinant coordinates

\[
A_0=b(2a+b),
\]

\[
A_1=a^2-b^2,
\]

\[
A_2=-a(a+2b).
\]

Each \(A_k\) is \(X(R^kx)Y(R^kx)\), with the displayed sign convention. Direct algebra gives

\[
A_0^2+A_1^2+A_2^2=2N(x)^2,
\]

and

\[
\prod_{k=0}^{2}\bigl(N(x)^2-A_k^2\bigr)
=-a^2b^2(a-b)^2(a+b)^2(a+2b)^2(2a+b)^2.
\]

The right side is nonpositive. If every \(A_k^2\) were strictly below \(N(x)^2\), the left side would be positive. Hence:

### Theorem 5.1 - Robust conjugate-pair selection

For every Eisenstein-lattice vector \(x\), one of the three antipodally distinct unit choices satisfies

\[
N(x)^2\le A_k^2.
\]

For nonzero \(x\), the selected pair is ready.

```text
PAL.PrimeShells.three_area_square_sum
PAL.PrimeShells.frame_gap_product
PAL.PrimeShells.exists_robust_frame_choice
PAL.PrimeShells.frameReady_of_robust
```

### 5.1 Sharp normalized-area bound

The squared normalized Euclidean area of the conjugate pair is

\[
\mathcal A(x)^2
=\frac{|\det(E(x),E(\bar x))|^2}
{\|E(x)\|^2\|E(\bar x)\|^2}
=\frac{3X(x)^2Y(x)^2}{4N(x)^2}.
\]

Equivalently, \(\mathcal A^2\) is the squared sine of the angle between the two references. The robust choice obeys

\[
\frac34\le\mathcal A(R^kx)^2\le1.
\]

So the chosen pair meets at an angle between \(60^\circ\) and \(120^\circ\).

```text
PAL.PrimeShells.robust_strength_lower_bound
PAL.PrimeShells.frameStrengthSq_le_one
PAL.PrimeShells.strength_three_quarters_is_sharp
```

### 5.2 Sharp condition-number bound

Define the conjugation-eigenmode energies

\[
H(x)=X(x)^2,
\qquad
V(x)=3Y(x)^2.
\]

The robust determinant inequality implies

\[
Y(x)^2\le X(x)^2\le9Y(x)^2,
\]

hence

\[
H(x)\le3V(x),\qquad V(x)\le3H(x).
\]

For the Euclidean frame matrix

\[
F_x=\frac12
\begin{pmatrix}
X(x)&X(x)\\
\sqrt3Y(x)&-\sqrt3Y(x)
\end{pmatrix},
\]

its two rows are orthogonal, with squared row lengths proportional to \(H\) and \(V\). Therefore

\[
\kappa_2(F_x)^2
=\frac{\max\{H(x),V(x)\}}{\min\{H(x),V(x)\}}
\le3,
\]

or

\[
\kappa_2(F_x)\le\sqrt3.
\]

The Lean formalization proves the row orthogonality, row-energy identities, exact max/min ratio, and bound.

```text
PAL.PrimeShells.conjugate_frame_rows_orthogonal
PAL.PrimeShells.symmetric_row_energy
PAL.PrimeShells.antisymmetric_row_energy
PAL.PrimeShells.robust_axis_balance
PAL.PrimeShells.robust_condition_bound_three
PAL.PrimeShells.frameConditionNumberSq_le_of_conditionBound
PAL.PrimeShells.exists_frameConditionNumberSq_le_three
```

### Theorem 5.2 - Sharpness at the ramified shell

At

\[
x=1+\eta,
\]

one has

\[
N(x)=3,\qquad X(x)=3,\qquad Y(x)=1,
\]

and therefore

\[
\mathcal A(x)^2=\frac34,
\qquad
\kappa_2(F_x)^2=3.
\]

No universal area lower bound larger than \(3/4\) and no universal squared conditioning constant smaller than \(3\) works for the stated three-choice ready-frame selector. Both constants are exact.

```text
PAL.PrimeShells.ramified_strength_upper
PAL.PrimeShells.ramified_strength_attained
PAL.PrimeShells.ramified_no_condition_bound_below_three
PAL.PrimeShells.universal_condition_constant_three_is_sharp
PAL.PrimeShells.ramified_frameConditionNumberSq
PAL.PrimeShells.frameConditionNumberSq_three_is_sharp
```

> **Author geometry insert 4 - Three chances around the shell.**  
> Show the three antipodal candidate pairs as the same reflected opening after successive sixty-degree unit turns. One of the three openings must remain at least sixty degrees wide. Let the product identity carry the proof burden.

## 6. Shell-to-shell transport

Let \(x\) and \(y\) be ready frames. In conjugation eigen-coordinates, define

\[
T_{x\to y}(r,s)
=
\left(
\frac{X(y)}{X(x)}r,
\frac{Y(y)}{Y(x)}s
\right).
\]

It sends the source references to their target counterparts:

\[
T_{x\to y}(B_x^+)=B_y^+,
\qquad
T_{x\to y}(B_x^-)=B_y^-.
\]

### Theorem 6.1 - Characterized transport

Suppose \(f:\mathbb R^2\to\mathbb R^2\) preserves all real linear combinations and

\[
f(B_x^+)=B_y^+,
\qquad
f(B_x^-)=B_y^-.
\]

Then

\[
f=T_{x\to y}.
\]

Two corresponding references therefore determine the transport uniquely.

```text
PAL.PrimeShells.transport_combine
PAL.PrimeShells.transport_preservesCombinations
PAL.PrimeShells.transport_unique
```

### Theorem 6.2 - Exact composition laws

For ready source and intermediate frames,

\[
T_{x\to x}=\operatorname{id},
\]

\[
T_{y\to z}\circ T_{x\to y}=T_{x\to z},
\]

\[
T_{y\to x}=T_{x\to y}^{-1}.
\]

```text
PAL.PrimeShells.transport_selected
PAL.PrimeShells.transport_reflected
PAL.PrimeShells.transport_self
PAL.PrimeShells.transport_compose
PAL.PrimeShells.transport_inverse
```

The map is a coordinate comparison between framed shells. It does not by itself describe a physical trajectory, time evolution, causal process, or canonical global atlas.

> **Author geometry insert 5 - Transport without teleportation.**  
> Explain transport as the unique comparison rule fixed by the two reference correspondences. Distinguish a map between frames from an object physically moving between radii.

## 7. Prime-shell specialization

Every exact supplied representation

\[
p=a^2+ab+b^2
\]

of a rational prime gives a nonzero shell vector. The sharp selector therefore yields a ready conjugate pair with

\[
\mathcal A^2\ge\frac34,
\qquad
\kappa_2^2\le3.
\]

```text
PAL.PrimeShells.prime_shell_has_robust_conjugate_frame
PAL.PrimeShells.prime_shell_has_sharply_conditioned_frame
PAL.PrimeShells.prime_shell_has_conditionNumberSq_le_three
```

This corollary consumes a certified representation; it does not discover or factor the prime. For split primes, the classical two-orbit theorem supplies the two conjugate arithmetic classes. The ramified prime \(3\) is exceptional in orbit structure and simultaneously certifies sharpness of the frame constants.

## 8. Formal verification account

The theorem surface is divided into five Lean modules:

```text
PAL/PrimeShells.lean
PAL/PrimeShellsModThreeKernel.lean
PAL/PrimeShellsConditioning.lean
PAL/PrimeShellsBasisTransport.lean
PAL/PrimeShellsConditionNumber.lean
```

Dependency receipts are generated from:

```text
Audit/PrimeShells.lean
Audit/PrimeShellsModThreeKernel.lean
Audit/PrimeShellsConditioning.lean
Audit/PrimeShellsBasisTransport.lean
Audit/PrimeShellsConditionNumber.lean
```

The dedicated workflow pins Lean 4.32.1 and Mathlib 4.32.1, compiles the complete module chain, records each `#print axioms` result, requires all five receipt files, rejects any dependency outside `propext`, `Classical.choice`, and `Quot.sound`, runs the repository proof-hole policy, and uploads the build record.

The current theorem inventory contains 62 publication-facing declarations. No `sorry`, `admit`, manuscript-specific postulate, or native-decision dependency is admitted by the publication receipt gate.

A green formal receipt proves only the exact Lean statements under the pinned environment. It does not prove that the cited classical sources are complete, that the paper is novel, that the geometric interpretation is canonical, or that the author has adopted the manuscript for publication.

## 9. Literature and priority boundary

Source roles must remain separate:

- U. P. Nair supplies elementary representability background for \(a^2+ab+b^2\).
- O. Marmon supplies the Eisenstein/hexagonal shell count, split/ramified/inert classification, and angular structure.
- Standard linear algebra supplies familiar basis, determinant, orthogonality, and condition-number concepts.
- PAL v2.3-M / RAINBOW supplies the author’s prior research address for shell and local-frame language; it is provenance, not independent corroboration.
- This manuscript contributes the selected conjugate-pair construction, the exact three-choice product certificate, the sharp \(3/4\) area and \(3\) squared-conditioning constants, and the characterized composable transport - subject to systematic priority review.

The initial targeted search found nearby literature on lattice shells, angular distribution, reduced bases, and frame conditioning, but not the exact theorem package above. That is not an exhaustive novelty result.

## 10. Nonclaims and open burdens

This manuscript does not claim:

- a proof or new route to the Riemann Hypothesis;
- a new classification of Eisenstein primes;
- that every phrase “prime shell” is new;
- a physical shell, particle model, wavefunction, force law, or cosmology;
- that one marked point is insufficient when a complete ambient orientation has already been supplied;
- that the selected unit choice is canonical without a tie-break rule;
- that exact real-number conditioning automatically guarantees every finite-precision implementation;
- that Lean compilation establishes global novelty, peer review, author adoption, or publication authority.

Open work before publication:

1. Christopher’s intuitive geometry and figures.
2. Systematic literature and priority review.
3. Independent mathematical review of the new sharp selector and transport package.
4. Final citation metadata and exact release manifest.
5. Optional future end-to-end Lean reconstruction of the classical arbitrary-prime representation and orbit-count theorem.

## 11. Proposed closing sentence

An arithmetic shell knows its level. A framed prime shell additionally carries enough internal relation to say how it is oriented, how securely that orientation is held, and how its coordinates pass to another shell without erasing the references that made the passage determinate.
