# 3. Classical prime-shell arithmetic

Let

$$S_{n} = \{(a,b) \in \mathbb{Z}^{2}:a^{2} + ab + b^{2} = n\}$$

and let

$$U = \{\eta^{j}:0 \leq j < 6\}$$

be the six-element unit group.

The classical prime classification is

$$\left| S_{p} \right| = \left\{ \begin{matrix}
6, & p = 3, \\
12, & p \equiv 1\ (mod\ 3), \\
0, & p \equiv 2\ (mod\ 3).
\end{matrix} \right.\ $$

For a split prime $p \equiv 1\ (mod\ 3)$, choose $\pi_{p}$ satisfying

$$p = \pi_{p}\overline{\pi_{p}}.$$

Then

$$S_{p} = U\pi_{p}\mspace{6mu} \sqcup \mspace{6mu} U\overline{\pi_{p}}.$$

After quotienting by the six unit rotations, exactly two conjugate arithmetic classes remain.

## Proposition 3.1 — Modulo-three obstruction

For all integers $a,b$,

$$a^{2} + ab + b^{2} ≢ 2\ (mod\ 3).$$

Consequently,

$$n \equiv 2\ (mod\ 3) \Rightarrow S_{n} = \varnothing.$$

### Proof

The finite ring $\mathbb{Z}/3\mathbb{Z}$ has nine pairs $(a,b)$. Direct reduction shows the quadratic form assumes only $0$ and $1$. The publication-facing Lean declaration discharges the finite case by ordinary kernel-reduced decision, then transports the contradiction back to the integer equation. In particular, the norm-$17$ shell is empty. ∎

The formal branch also checks occupied fixtures at norms $3,7,13,$ and $19$. It does **not** yet reconstruct the arbitrary split-prime representation theorem or the full six/twelve-point orbit count. Those remain cited classical inputs.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 4. Minimal reference data

The norm already identifies an unmarked shell as a set. A **framed shell** asks for enough internal relation to express arbitrary planar comparison without importing an undeclared second direction.

## Theorem 4.1 — One reference is insufficient

For every $u \in \mathbb{R}^{2}$, there exists $v \in \mathbb{R}^{2}$ that is not a scalar multiple of $u$.

### Proof

Write $u = \left( u_{1},u_{2} \right)$. If $u_{1} = 0$, take $v = (1,0)$. No scalar multiple of $u$ has first coordinate $1$. If $u_{1} \neq 0$, take $v = (0,1)$. An equation $cu = v$ forces $cu_{1} = 0$, hence $c = 0$, contradicting the second coordinate. ∎

One marked shell vector therefore cannot span a two-dimensional real carrier.

## Theorem 4.2 — Two conjugate references reconstruct uniquely

Let $x$ be frame-ready. For $v = (r,s)$, define

$$c_{x}(v) = \frac{r}{2X(x)} + \frac{s}{2Y(x)},$$

$$d_{x}(v) = \frac{r}{2X(x)} - \frac{s}{2Y(x)}.$$

Then

$$v = c_{x}(v)u_{x} + d_{x}(v)w_{x}.$$

These coefficients are unique.

### Proof

Expanding the right side gives

$$\left( \left( c_{x} + d_{x} \right)X,\left( c_{x} - d_{x} \right)Y \right) = (r,s).$$

Because $X$ and $Y$ are nonzero, the two scalar equations have the displayed unique solution. Equivalently, the determinant $- 2XY$ is nonzero, so the two references are linearly independent and form a basis of $\mathbb{R}^{2}$. ∎

This is the exact seam behind the informal statement that two references are required for a shell to carry its own two-dimensional frame.

> **AUTHOR GEOMETRY INSERT 3 — WHAT “STABLE” MEANS**  
> Separate three meanings: (i) the norm identifies the unmarked shell; (ii) one marked point can orient it relative to an already supplied outside axis; (iii) two nonparallel internal references furnish a complete local planar frame. Suggested figure: the same shell shown unmarked, externally oriented, and internally framed.

# 5. Three unit choices and the robust selector

The six unit rotations contain three antipodal pairs. It is therefore enough to inspect

$$x,\quad\quad Rx,\quad\quad R^{2}x.$$

For $x = (a,b)$, define the determinant coordinates

$$A_{0} = b(2a + b),$$

$$A_{1} = a^{2} - b^{2},$$

$$A_{2} = - a(a + 2b).$$

Each $A_{k}$ is $X\left( R^{k}x \right)Y\left( R^{k}x \right)$, up to the displayed sign convention.

## Lemma 5.1 — Three-area identity

$$A_{0}^{2} + A_{1}^{2} + A_{2}^{2} = 2N(x)^{2}.$$

### Proof

Substitute the three coordinate polynomials and expand. The difference between the two sides normalizes to the zero polynomial. ∎

## Lemma 5.2 — Shortfall-product identity

$$\prod_{k = 0}^{2}\left( N(x)^{2} - A_{k}^{2} \right) = - a^{2}b^{2}(a - b)^{2}(a + b)^{2}(a + 2b)^{2}(2a + b)^{2}.$$

### Proof

Again substitute and normalize as a polynomial identity. The right side is the negative of a product of six squares and is therefore nonpositive over $\mathbb{R}$. ∎

## Theorem 5.3 — Robust conjugate-pair selection

For every Eisenstein-lattice vector $x$, at least one of the three antipodally distinct unit choices satisfies

$$N(x)^{2} \leq A_{k}^{2}.$$

If $N(x) \neq 0$, the selected pair is frame-ready.

### Proof

Assume all three strict inequalities $A_{k}^{2} < N(x)^{2}$. Every factor on the left side of Lemma 5.2 is then positive, so their product is positive. Lemma 5.2 says the same product is nonpositive, a contradiction. Thus one $A_{k}^{2}$ is at least $N(x)^{2}$.

If $N(x) \neq 0$, then $N(x)^{2} > 0$, so the selected $A_{k} = XY$ is nonzero. Hence both $X$ and $Y$ are nonzero and the conjugate pair is frame-ready. ∎

# 6. Sharp area and conditioning

## 6.1 Normalized area

Because

$$\parallel E(x) \parallel^{2} = \parallel E\left( \bar{x} \right) \parallel^{2} = N(x),$$

and

$$\det\left( E(x),E\left( \bar{x} \right) \right) = - \frac{\sqrt{3}}{2}X(x)Y(x),$$

the squared normalized area is

$$\mathcal{A}(x)^{2} = \frac{\left| \det\left( E(x),E\left( \bar{x} \right) \right) \right|^{2}}{\parallel E(x) \parallel^{2} \parallel E\left( \bar{x} \right) \parallel^{2}} = \frac{3X(x)^{2}Y(x)^{2}}{4N(x)^{2}}.$$

This is also the squared sine of the angle between the references.

## Theorem 6.1 — Sharp normalized-area lower bound

For the robust choice from Theorem 5.3,

$$\frac{3}{4} \leq \mathcal{A}\left( R^{k}x \right)^{2} \leq 1.$$

### Proof

The robust inequality $N^{2} \leq X^{2}Y^{2}$ gives the lower bound immediately:

$$\mathcal{A}^{2} = \frac{3X^{2}Y^{2}}{4N^{2}} \geq \frac{3}{4}.$$

For the upper bound, use

$$\left( X^{2} - 3Y^{2} \right)^{2} \geq 0.$$

Expanding and substituting $X^{2} + 3Y^{2} = 4N$ yields

$$3X^{2}Y^{2} \leq 4N^{2},$$

so $\mathcal{A}^{2} \leq 1$. ∎

The selected references therefore meet at an angle between $60^{\circ}$ and $120^{\circ}$.

## 6.2 Axis balance

Set

$$H(x) = X(x)^{2},\quad\quad V(x) = 3Y(x)^{2}.$$

The robust inequality also gives

$$\left( X^{2} - Y^{2} \right)\left( X^{2} - 9Y^{2} \right) = \left( X^{2} + 3Y^{2} \right)^{2} - 16X^{2}Y^{2} = 16\left( N^{2} - X^{2}Y^{2} \right) \leq 0.$$

Hence

$$Y^{2} \leq X^{2} \leq 9Y^{2},$$

and therefore

$$H \leq 3V,\quad\quad V \leq 3H.$$

## 6.3 Euclidean frame condition number

The Euclidean frame matrix is

$$F_{x} = \frac{1}{2}\begin{pmatrix}
X & X \\
\sqrt{3}Y & - \sqrt{3}Y
\end{pmatrix}.$$

Its two rows are orthogonal and

$$F_{x}F_{x}^{\mathsf{T}} = \frac{1}{2}\begin{pmatrix}
X^{2} & 0 \\
0 & 3Y^{2}
\end{pmatrix}.$$

Thus the squared spectral condition number is

$$\kappa_{2}\left( F_{x} \right)^{2} = \frac{\max\{ H,V\}}{\min\{ H,V\}}.$$

## Theorem 6.2 — Uniform condition-number bound

For one of the three antipodally distinct unit choices,

$$\kappa_{2}\left( F_{R^{k}x} \right)^{2} \leq 3,$$

or equivalently

$$\kappa_{2}\left( F_{R^{k}x} \right) \leq \sqrt{3}.$$

### Proof

The selected choice is frame-ready and satisfies $H \leq 3V$ and $V \leq 3H$. If $H \leq V$, then $\kappa_{2}^{2} = V/H \leq 3$. If $V \leq H$, then $\kappa_{2}^{2} = H/V \leq 3$. ∎

> **AUTHOR GEOMETRY INSERT 4 — THREE CHANCES AROUND THE SHELL**  
> Show the six unit rotations as three antipodal candidate pairs. A candidate may approach the reflection axis and collapse, but the hexagonal symmetry supplies two more distinct choices. The algebra proves that all three cannot be too narrow at once: one opens by at least $60^{\circ}$ and has condition number at most $\sqrt{3}$. Use the norm-$3$ shell as the equality case.

# 7. Sharpness at the norm-three shell

Take the ramified point

$$x = 1 + \eta,$$

so $(a,b) = (1,1)$. Then

$$N(x) = 3,\quad\quad X(x) = 3,\quad\quad Y(x) = 1.$$

Consequently,

$$\mathcal{A}(x)^{2} = \frac{3 \cdot 9 \cdot 1}{4 \cdot 9} = \frac{3}{4},$$

and

$$H(x) = 9,\quad\quad V(x) = 3,$$

so

$$\kappa_{2}\left( F_{x} \right)^{2} = 3.$$

## Theorem 7.1 — Sharpness

No universal normalized-area lower bound larger than $3/4$, and no universal squared condition-number bound smaller than $3$, works for the stated selector among the three antipodally distinct unit choices while requiring a frame-ready output.

### Proof

At the norm-$3$ point, the ready choices attain squared normalized area $3/4$ and squared condition number $3$; the remaining candidate is singular. Therefore any stronger universal constant fails on this shell. ∎

The exceptional ramified shell is not only a boundary case in the classical arithmetic classification. It also certifies the exact constants of the framing theorem.

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# 8. Shell-to-shell transport

Let $x$ and $y$ be frame-ready. In conjugation eigen-coordinates, define

$$T_{x \rightarrow y}(r,s) = \left( \frac{X(y)}{X(x)}r,\frac{Y(y)}{Y(x)}s \right).$$

Then

$$T_{x \rightarrow y}\left( u_{x} \right) = u_{y},\quad\quad T_{x \rightarrow y}\left( w_{x} \right) = w_{y}.$$

## Theorem 8.1 — Characterized transport

Suppose $f:\mathbb{R}^{2} \rightarrow \mathbb{R}^{2}$ preserves every real linear combination and satisfies

$$f\left( u_{x} \right) = u_{y},\quad\quad f\left( w_{x} \right) = w_{y}.$$

Then

$$f = T_{x \rightarrow y}.$$

### Proof

By Theorem 4.2, every $v$ has a unique decomposition

$$v = c_{x}(v)u_{x} + d_{x}(v)w_{x}.$$

Linearity and the two prescribed reference images force

$$f(v) = c_{x}(v)u_{y} + d_{x}(v)w_{y}.$$

Direct expansion gives exactly the displayed diagonal formula for $T_{x \rightarrow y}$. Therefore no other combination-preserving map can satisfy the same two reference correspondences. ∎

## Theorem 8.2 — Exact composition laws

For frame-ready $x,y,z$,

$$T_{x \rightarrow x} = id,$$

$$T_{y \rightarrow z} \circ T_{x \rightarrow y} = T_{x \rightarrow z},$$

$$T_{y \rightarrow x} = T_{x \rightarrow y}^{- 1}.$$

### Proof

Each statement is coordinatewise cancellation of the nonzero scale ratios. For example,

$$\frac{X(z)}{X(y)}\frac{X(y)}{X(x)} = \frac{X(z)}{X(x)},$$

with the same identity in the $Y$ coordinate. ∎

The transport is a coordinate comparison between framed shells. It does not by itself describe physical motion, elapsed time, causal transfer, or a historical path.

> **AUTHOR GEOMETRY INSERT 5 — TRANSPORT WITHOUT TELEPORTATION**  
> Draw a source and target shell with two paired reference correspondences. Decompose one arbitrary source vector in the source pair and rebuild it in the target pair with the same coefficients. Add a three-shell strip for exact composition. Keep the map distinct from an object physically moving between radii.

# 9. Prime-shell specialization

Every exact supplied representation

$$p = a^{2} + ab + b^{2}$$

of a rational prime gives a nonzero shell vector. The sharp selector therefore applies.

## Corollary 9.1 — Represented prime shells admit sharp frames

Let $p$ be prime and suppose

$$p = a^{2} + ab + b^{2}.$$

Then one of the three antipodally distinct unit choices produces a frame-ready conjugate pair satisfying

$$\mathcal{A}^{2} \geq \frac{3}{4},$$

and

$$\kappa_{2}^{2} \leq 3.$$

The corollary consumes a certified representation; it does not discover, factor, or prove the representation. For split primes, the classical two-orbit theorem supplies the conjugate arithmetic classes. The ramified prime $3$ remains exceptional in orbit structure and is the sharp equality case.


```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```
