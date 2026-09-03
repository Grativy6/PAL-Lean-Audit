# Framed Prime Shells

## Minimal reference data, sharp conditioning, and composable transport in the Eisenstein lattice

**Author and steward:** Christopher D. Pang  
**Version:** working manuscript skeleton, not adopted for publication  
**Reserved record:** `10.5281/zenodo.22288471`  
**Formal branch:** `agent/prime-shells-conjugate-frames`  
**License target:** manuscript and diagrams CC BY 4.0; Lean code Apache-2.0 under the repository license

> **Status.** The classical prime-shell classification is source-side mathematics. The two-reference, sharp-conditioning, and characterized-transport results are manuscript-side deductions checked in Lean. Global novelty remains open pending a systematic literature review. The DOI is a publication handle, not mathematical evidence.

## Abstract draft

Let

\[
\eta=e^{i\pi/3},\qquad
Q(a,b)=N(a+b\eta)=a^2+ab+b^2,
\]

and let

\[
S_n=\{(a,b)\in\mathbb Z^2:Q(a,b)=n\}
\]

be the norm shell of level \(n\) in the Eisenstein lattice. Classical arithmetic gives six points for the ramified prime \(3\), twelve points arranged in two conjugate unit orbits for each split rational prime \(p\equiv1\pmod3\), and an empty norm-\(p\) shell for each inert prime \(p\equiv2\pmod3\).

This paper asks a different question: what additional data turns an arithmetic shell into a stable planar frame? One marked vector cannot span the plane. A noncollinear vector and its arithmetic conjugate do, and every planar vector then has unique coefficients in that pair. More strongly, among the three antipodally distinct unit rotations of every nonzero Eisenstein-lattice vector, one conjugate pair has squared normalized area at least \(3/4\) and symmetric/antisymmetric axis-energy ratio at most \(3\). Both constants are sharp at the norm-\(3\) shell. For any two ready conjugate-pair frames, the unique linear-combination-preserving transport sending the selected and reflected source references to the corresponding target references has a diagonal form in conjugation eigen-coordinates and obeys exact identity, inverse, and composition laws.

The coordinate algebra, mod-three obstruction, minimal-reference theorem, sharp frame-selection theorem, coefficient uniqueness, and transport characterization are formalized in Lean 4.32.1 with Mathlib 4.32.1. The full classical arbitrary-prime representation and orbit-count theorem is cited rather than claimed as newly formalized in the present branch.

---

## 1. Orientation and claim boundary

The phrase **prime shell** refers here to an exact norm level set in the Eisenstein lattice. It does not mean a physical shell, an electron shell, a probability distribution, a zeta-zero packet, or an RH mechanism.

The paper has three separately typed ingredients:

1. **Classical arithmetic.** Eisenstein factorization and the representation theory of \(a^2+ab+b^2\) determine which rational primes occupy a shell and how many lattice points occur.
2. **New manuscript construction.** A selected point, its arithmetic conjugate, a unit-rotation choice, a conditioning functional, and a shell-to-shell transport law turn occupied shells into framed objects.
3. **Geometric exposition.** The visual and intuitive account explains why two references stop a shell from floating, why three unit choices suffice, how a frame approaches collapse, and what transport between shells means.

The third layer is reserved for the author’s intuitive geometry. It may motivate the equations, but it does not replace them.

> **Author geometry insert 1 — What a shell is.**  
> Explain the distinction between a circle as a continuum and the finite lattice points that occupy one exact arithmetic norm level.

## 2. Eisenstein coordinate algebra

Use the sixth root

\[
\eta=e^{i\pi/3},\qquad \eta^2=\eta-1,
\]

and write an Eisenstein integer as

\[
x=a+b\eta,\qquad a,b\in\mathbb Z.
\]

In the \((1,\eta)\) basis:

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

with

\[
N(xy)=N(x)N(y),\qquad N(\bar x)=N(x),\qquad N(Rx)=N(x),
\]

and

\[
x\bar x=N(x).
\]

The Lean formalization proves these identities directly in `PAL/PrimeShells.lean`.

### 2.1 Scaled Cartesian coordinates

Define

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

while conjugation acts by reflection:

\[
E(\bar x)=\frac12\bigl(X(x),-\sqrt3\,Y(x)\bigr).
\]

Thus the symmetric coordinate is radial along the reflection axis and the antisymmetric coordinate measures displacement across it.

> **Author geometry insert 2 — The two references.**  
> Describe the selected shell point and its reflected partner as two separately readable directions from a supplied center. Mark clearly that the center is supplied; without it the corresponding affine statement would require three noncollinear points.

## 3. Classical prime-shell classification

Let

\[
U=\{\eta^j:0\le j<6\}
\]

be the unit group. The classical classification is:

\[
|S_p|=
\begin{cases}
6,&p=3,\\
12,&p\equiv1\pmod3,\\
0,&p\equiv2\pmod3.
\end{cases}
\]

For a split prime \(p\equiv1\pmod3\), choose one factor \(\pi_p\) with

\[
p=\pi_p\overline{\pi_p}.
\]

Then

\[
S_p=U\pi_p\;\sqcup\;U\overline{\pi_p}.
\]

After quotienting by the six unit rotations, precisely two conjugate arithmetic classes remain.

The present Lean branch proves the elementary obstruction

\[
Q(a,b)\not\equiv2\pmod3,
\]

hence every level \(n\equiv2\pmod3\) has an empty integer shell. It also checks concrete occupied fixtures. The arbitrary split-prime existence theorem and the general twelve-point/two-orbit count remain imported classical results and must be cited as such.

## 4. Minimal reference data

A shell as an unmarked set is already determined by its norm. A framed shell asks for more: an internally carried basis capable of expressing planar comparison without borrowing an undeclared outside direction.

### Theorem 4.1 — One reference is insufficient

For every \(u\in\mathbb R^2\), there exists \(v\in\mathbb R^2\) that is not a scalar multiple of \(u\). Therefore one marked shell vector cannot span the plane.

Lean declaration:

```text
PAL.PrimeShells.one_reference_is_insufficient
```

### Theorem 4.2 — Two conjugate references reconstruct

Let \(x\) satisfy

\[
X(x)\ne0,\qquad Y(x)\ne0.
\]

Then the vectors

\[
B_x^+=\bigl(X(x),Y(x)\bigr),\qquad
B_x^-=\bigl(X(x),-Y(x)\bigr)
\]

form a basis of \(\mathbb R^2\). For \(v=(r,s)\), the unique coefficients are

\[
c_x(v)=\frac{r}{2X(x)}+\frac{s}{2Y(x)},
\]

\[
d_x(v)=\frac{r}{2X(x)}-\frac{s}{2Y(x)},
\]

and

\[
v=c_x(v)B_x^++d_x(v)B_x^-.
\]

Lean declarations:

```text
PAL.PrimeShells.two_references_reconstruct
PAL.PrimeShells.conjugate_references_independent
PAL.PrimeShells.conjugate_reference_coefficients_unique
```

This is the exact seam behind the informal statement that a shell needs two references to become stable as its own two-dimensional frame.

> **Author geometry insert 3 — What “stable” means.**  
> Separate set identity, orientation relative to an imported ambient axis, and the stronger claim that the shell carries its own local rank-two frame.

## 5. Three unit choices and a sharp frame theorem

The six unit rotations contain three antipodal pairs. It is therefore enough to examine

\[
x,\qquad Rx,\qquad R^2x.
\]

Define the three determinant coordinates

\[
A_0=b(2a+b),
\]

\[
A_1=a^2-b^2,
\]

\[
A_2=-a(a+2b).
\]

Each \(A_k\) is the product \(X(R^kx)Y(R^kx)\), up to the displayed sign convention. Direct algebra gives two exact identities:

\[
A_0^2+A_1^2+A_2^2=2N(x)^2,
\]

and

\[
\prod_{k=0}^{2}\bigl(N(x)^2-A_k^2\bigr)
=-a^2b^2(a-b)^2(a+b)^2(a+2b)^2(2a+b)^2.
\]

The right side is nonpositive. If every \(A_k^2\) were strictly below \(N(x)^2\), all three factors on the left would be positive, a contradiction. Therefore:

### Theorem 5.1 — Robust conjugate-pair selection

For every nonzero Eisenstein-lattice vector \(x\), one of the three antipodally distinct unit choices satisfies

\[
N(x)^2\le A_k^2.
\]

Lean declaration:

```text
PAL.PrimeShells.exists_robust_frame_choice
```

### 5.1 Normalized area

The squared normalized Euclidean area of the conjugate pair is

\[
\mathcal A(x)^2
=\frac{|\det(E(x),E(\bar x))|^2}{\|E(x)\|^2\|E(\bar x)\|^2}
=\frac{3X(x)^2Y(x)^2}{4N(x)^2}.
\]

This equals the squared sine of the angle between the references. The robust choice therefore obeys

\[
\mathcal A(R^kx)^2\ge\frac34.
\]

Equivalently, its two references meet at an angle between \(60^\circ\) and \(120^\circ\).

Lean declarations:

```text
PAL.PrimeShells.robust_strength_lower_bound
PAL.PrimeShells.frameStrengthSq_le_one
PAL.PrimeShells.strength_three_quarters_is_sharp
```

### 5.2 Axis balance and conditioning

Set

\[
H(x)=X(x)^2,
\qquad
V(x)=3Y(x)^2.
\]

For the robust choice, the determinant inequality is equivalent to

\[
Y(x)^2\le X(x)^2\le9Y(x)^2,
\]

which in turn gives

\[
H(x)\le3V(x),\qquad V(x)\le3H(x).
\]

For the associated Euclidean frame matrix

\[
F_x=rac12
\begin{pmatrix}
X(x)&X(x)\\
\sqrt3Y(x)&-\sqrt3Y(x)
\end{pmatrix},
\]

one has

\[
F_xF_x^{\mathsf T}
=\frac12
\begin{pmatrix}
X(x)^2&0\\
0&3Y(x)^2
\end{pmatrix}.
\]

Thus the squared spectral condition number is the larger of \(H,V\) divided by the smaller, and the robust choice satisfies

\[
\kappa_2(F_x)^2\le3,
\qquad
\kappa_2(F_x)\le\sqrt3.
\]

The Lean core formalizes the division-free energy inequalities. The displayed matrix interpretation is an exact rewriting of those inequalities and is scheduled for its own matrix-level declaration before release.

Lean declarations:

```text
PAL.PrimeShells.robust_axis_balance
PAL.PrimeShells.robust_condition_bound_three
PAL.PrimeShells.exists_sharply_conditioned_frame_choice
```

### Theorem 5.2 — Sharpness

At the ramified norm-\(3\) point

\[
x=1+\eta,
\]

one has \(X=3\), \(Y=1\), so

\[
\mathcal A(x)^2=\frac34,
\qquad
\kappa_2(F_x)^2=3.
\]

No choice among the three unit-rotation classes admits a universal squared conditioning constant smaller than \(3\). Hence both \(3/4\) and \(3\) are sharp for the stated selector problem.

Lean declarations:

```text
PAL.PrimeShells.ramified_strength_upper
PAL.PrimeShells.ramified_strength_attained
PAL.PrimeShells.ramified_no_condition_bound_below_three
PAL.PrimeShells.universal_condition_constant_three_is_sharp
```

> **Author geometry insert 4 — Three chances around the shell.**  
> Give the visual argument: the three conjugate-pair angles are the same reflected opening viewed after sixty-degree unit rotations; one choice must stay at least sixty degrees open. Use the algebraic identity as the certificate, not as a replacement for the picture.

## 6. Shell-to-shell transport

Let \(x\) and \(y\) be ready frames. In the scaled conjugation eigen-coordinates, define

\[
T_{x\to y}(r,s)
=
\left(
\frac{X(y)}{X(x)}r,
\frac{Y(y)}{Y(x)}s
\right).
\]

Then

\[
T_{x\to y}(B_x^+)=B_y^+,
\qquad
T_{x\to y}(B_x^-)=B_y^-.
\]

It is the unique map preserving arbitrary real linear combinations with those two endpoint conditions.

### Theorem 6.1 — Characterized transport

If \(f:\mathbb R^2\to\mathbb R^2\) preserves linear combinations and

\[
f(B_x^+)=B_y^+,
\qquad
f(B_x^-)=B_y^-,
\]

then

\[
f=T_{x\to y}.
\]

Lean declarations:

```text
PAL.PrimeShells.transport_combine
PAL.PrimeShells.transport_preservesCombinations
PAL.PrimeShells.transport_unique
```

### Theorem 6.2 — Groupoid laws

For ready source and intermediate frames:

\[
T_{x\to x}=\operatorname{id},
\]

\[
T_{y\to z}\circ T_{x\to y}=T_{x\to z},
\]

\[
T_{y\to x}=T_{x\to y}^{-1}.
\]

Lean declarations:

```text
PAL.PrimeShells.transport_self
PAL.PrimeShells.transport_compose
PAL.PrimeShells.transport_inverse
```

The shell labels select the endpoints of transport; they do not create a physical motion, causal history, or privileged global coordinate system.

> **Author geometry insert 5 — Transport without teleportation.**  
> Explain transport as the unique comparison rule fixed by two corresponding references. Distinguish the mathematical map from a path traversed through physical space or time.

## 7. Prime-shell specialization

Every supplied exact representation

\[
p=a^2+ab+b^2
\]

of a rational prime gives a nonzero shell vector. The sharp frame selector therefore applies immediately:

### Corollary 7.1 — Prime shell with a sharp local frame

For every represented rational prime \(p\), there is a unit-rotation choice whose conjugate pair is ready, has squared normalized area at least \(3/4\), and satisfies the squared conditioning bound \(3\).

Lean declaration:

```text
PAL.PrimeShells.prime_shell_has_sharply_conditioned_frame
```

For split primes, the classical two-orbit theorem supplies the two conjugate arithmetic classes from which the references are selected. For the ramified prime \(3\), the same finite selector remains valid while the orbit structure is exceptional.

## 8. Formal verification account

The current Lean modules are:

```text
PAL/PrimeShells.lean
PAL/PrimeShellsConditioning.lean
PAL/PrimeShellsBasisTransport.lean
Audit/PrimeShells.lean
Audit/PrimeShellsConditioning.lean
Audit/PrimeShellsBasisTransport.lean
```

The dedicated workflow pins Lean 4.32.1 and Mathlib 4.32.1, compiles the modules, records `#print axioms` output, enforces the repository proof-hole policy, and uploads its build and dependency receipts.

No `sorry`, `admit`, or manuscript-specific axiom is permitted. Standard Lean logical dependencies remain visible in the receipts. Any finite native-decision certificate, if retained, must remain separately identified rather than described as a handwritten kernel proof.

## 9. Literature and priority boundary

The following source roles must remain separate:

- U. P. Nair, *Elementary results on the binary quadratic form* \(a^2+ab+b^2\): classical representability background.
- O. Marmon, *Hexagonal Lattice Points on Circles*: Eisenstein/hexagonal representation counts and angular distribution.
- Standard linear algebra: basis, determinant, singular values, condition number, and uniqueness of a linear map from basis images.
- This manuscript: the selected conjugate-pair frame package, the three-choice product certificate, the sharp \(3/4\) area and \(3\) squared-conditioning constants, and the characterized shell-transport organization—subject to systematic priority review.
- PAL v2.3-M / RAINBOW: the author’s prior research address and provenance for shell/frame language, not independent corroboration.

Initial searching has not yet located the complete theorem package in this exact form. That is not an exhaustive novelty result.

## 10. Nonclaims

This paper does not claim:

- a proof or new route to the Riemann Hypothesis;
- a new classification of Eisenstein primes;
- that every use of the phrase “prime shell” is new;
- a physical shell, particle model, wavefunction, force law, or cosmology;
- that one marked point is insufficient when an ambient orientation operator has already been supplied;
- that the selected frame is canonical without a declared tie-break rule;
- that exact real-number conditioning automatically yields stable floating-point decoding at every scale;
- that a formal proof establishes global novelty, publication quality, or author adoption.

## 11. Proposed closing sentence

An arithmetic shell knows its level. A framed prime shell additionally carries enough internal relation to say how it is oriented, how securely that orientation is held, and how its coordinates pass to another shell without erasing the references that made the passage determinate.
