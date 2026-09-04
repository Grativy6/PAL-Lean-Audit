# Framed Prime Shells - geometry handoff

**For:** Christopher D. Pang  
**Role:** author-supplied intuitive geometry and figure direction  
**Formal boundary:** the equations and theorem statuses in `MANUSCRIPT_SKELETON.md` and `CLAIM_LEDGER.md` control the mathematical claims. This handoff leaves the explanatory layer open without asking the geometry to carry proof authority.

## Keeper

An unmarked shell knows its norm. A framed shell additionally carries two nonparallel references, a readable measure of how far they are from collapse, and a unique comparison rule to another framed shell.

## Insert 1 - The shell before the frame

### Formal anchor

\[
S_n=\{(a,b)\in\mathbb Z^2:a^2+ab+b^2=n\}.
\]

### Intuitive job

Explain that the continuum ellipse/circle-like level set is not the arithmetic shell itself. The shell is the finite set of lattice points landing exactly on that level. The value \(n\) fixes the unmarked shell as a set; no marked orientation is yet chosen.

### Figure brief

- Draw the triangular/Eisenstein lattice faintly.
- Draw one norm level through its occupied lattice points.
- Show one occupied split-prime shell and one empty inert-prime level.
- Label continuum level set and arithmetic occupancy separately.

### Do not imply

- that every norm level is occupied;
- that the drawn circle radius alone contains the arithmetic factorization;
- that a shell is a physical surface or PAL boundary without a separate adapter.

## Insert 2 - Two reflected references

### Formal anchor

For \(x=a+b\eta\),

\[
X=2a+b,\qquad Y=b,
\]

\[
B_x^+=(X,Y),\qquad B_x^-=(X,-Y),
\]

\[
\det(B_x^+,B_x^-)=-2XY.
\]

### Intuitive job

Show how arithmetic conjugation keeps the common direction while reversing the across-axis component. One point gives a ray. The point together with its conjugate gives two rays. When neither common nor opposed component vanishes, the pair stops the local coordinate frame from floating.

### Figure brief

- Center supplied and visibly marked.
- Draw \(B_x^+\) and \(B_x^-\) as reflected rays.
- Decompose them into one shared horizontal component and opposite vertical components.
- Mark the parallelogram area as the noncollapse witness.

### Do not imply

- that conjugation creates the center;
- that one point is always insufficient relative to a fully supplied outside coordinate system;
- that nonzero determinant alone is a physical stability theorem.

## Insert 3 - Set stability, imported orientation, and self-carried frame

### Formal anchor

One vector does not span \(\mathbb R^2\). A ready conjugate pair does, with unique coefficients.

### Intuitive job

Separate three meanings that ordinary language can bundle as “stable”:

1. **Set-stable:** the norm identifies the shell.
2. **Externally oriented:** one marked point can be compared with an ambient axis that was already supplied.
3. **Internally framed:** two nonparallel references carried by the shell reconstruct every local planar vector without importing a second direction afterward.

### Figure brief

Use three small panels with the same shell:

- unmarked shell;
- one marked ray plus an external compass/grid;
- selected/conjugate pair with its own local axes.

### Do not imply

- that the paper proves a universal philosophical minimum independent of the declared carrier;
- that an affine frame without a supplied center also needs only two points.

## Insert 4 - Three chances and the sharp opening

### Formal anchor

The three antipodal unit choices have determinant coordinates

\[
A_0=b(2a+b),\quad A_1=a^2-b^2,\quad A_2=-a(a+2b),
\]

and one satisfies

\[
N(x)^2\le A_k^2.
\]

Consequently,

\[
\sin^2\theta_k\ge\frac34,
\qquad
\kappa_2(F_k)^2\le3.
\]

Both bounds are sharp at the norm-\(3\) shell.

### Intuitive job

Describe the six unit rotations as three antipodal candidate pairs. A candidate may approach collapse against the reflection axis, but the hexagonal geometry gives two more distinct choices. The algebra proves that all three cannot be too narrow at once. One pair opens by at least sixty degrees, and the corresponding coordinate frame is never worse than condition number \(\sqrt3\).

### Figure brief

- Show the three candidate conjugate pairs overlaid or in three panels.
- Mark the angle for each pair.
- Highlight the selected pair whose opening is at least \(60^\circ\).
- Include the norm-3 shell as the equality case, not merely a decorative example.

### Do not imply

- that the selected pair is unique;
- that the choice is canonical without a tie-break rule;
- that the sharp constant is a new fact about all lattice-basis reduction methods.

## Insert 5 - Transport fixed by two correspondences

### Formal anchor

For ready frames \(x,y\),

\[
T_{x\to y}(r,s)=
\left(\frac{X_y}{X_x}r,\frac{Y_y}{Y_x}s\right),
\]

with

\[
T_{x\to y}(B_x^+)=B_y^+,
\qquad
T_{x\to y}(B_x^-)=B_y^-.
\]

It is the unique real-linear map with those two reference images, and

\[
T_{y\to z}T_{x\to y}=T_{x\to z}.
\]

### Intuitive job

Explain that two corresponding references determine how every other local vector must compare. Transport here is not an object crossing the gap between shells. It is the unique coordinate-change rule that preserves the declared linear relations.

### Figure brief

- Draw a source shell and target shell with their two selected references.
- Use paired labels to show the two required correspondences.
- Show one arbitrary vector decomposed in the source pair and rebuilt in the target pair with the same coefficients.
- Add a three-shell strip illustrating exact composition.

### Do not imply

- physical motion, elapsed time, causal transfer, or a particle trajectory;
- one canonical global atlas across all shells;
- that endpoint correspondence records a historical path.

## Optional opening paragraph seed

A prime shell is already exact before it is framed. Its norm determines which lattice points belong to it. But exact membership does not yet say how the shell should compare directions, how securely those directions remain distinguishable, or how one shell's coordinates should pass to another. Those questions require reference data. In the Eisenstein lattice, arithmetic conjugation supplies a natural pair; the sixfold unit symmetry supplies three genuinely different chances to choose it well.

## Optional closing paragraph seed

The construction does not make primes less irregular or turn their shells into a prediction engine. It does something smaller and cleaner. Once an occupied shell is supplied, it identifies the least local relational data needed for a complete planar readout, proves that the hexagonal symmetry always offers a uniformly well-conditioned choice, and fixes the comparison between any two such choices without leaving an arbitrary degree of freedom behind.
