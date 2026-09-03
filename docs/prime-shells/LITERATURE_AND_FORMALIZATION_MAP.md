# Prime Shells literature and formalization map

**Search checkpoint:** 3 September 2026  
**Status:** targeted initial review, not an exhaustive priority search

## 1. Classical shell arithmetic

### U. P. Nair — representability

**Source:** Umesh P. Nair, “Elementary results on the binary quadratic form `a²+ab+b²`,” arXiv:math/0408107 (2004).

Source role:

- gives an elementary representability route;
- states that a rational prime is represented exactly for primes of the form `6k+1`, with `3` as the exceptional represented prime;
- states the composite representability criterion through even exponents of the other prime classes.

Boundary:

- Nair’s abstract describes the general representation-count formula as conjectural;
- do not use Nair alone as authority for the exact arbitrary-`n` shell count.

### O. Marmon — shell count, factor packets, and angles

**Source:** Oscar Marmon, “Hexagonal Lattice Points on Circles,” arXiv:math/0508201 (2005).

Source role:

- identifies the lattice with `ℤ[η]`, `η=e^{iπ/3}`;
- defines `r_Q(n)=#{(a,b)∈ℤ² : a²+ab+b²=n}`;
- states the split/ramified/inert classification:
  - `p≡1 (mod 3)` split,
  - `p≡2 (mod 3)` inert,
  - `p=3` ramified;
- derives

  `r_Q(n)=6 ∏_{p_i≡1 (mod 3)} (α_i+1)`

  when every inert-prime exponent is even;
- identifies a unique chosen split-prime generator angle in a fundamental sector;
- studies angular equidistribution of shell points and Eisenstein primes.

Boundary:

- these are classical source-side results, not manuscript novelty;
- the present Lean branch does not yet reconstruct Marmon’s arbitrary-prime splitting and count argument end to end.

## 2. Nearby geometric and lattice literature

The initial search covered the following query families:

- Eisenstein or hexagonal lattice points on circles;
- prime norm shells and shelling functions;
- angular distributions of Eisenstein primes;
- conjugate vectors in hexagonal lattices;
- well-conditioned lattice bases;
- condition numbers attached to Eisenstein conjugate pairs;
- transport between marked norm shells.

Nearby work located:

- angular distribution and discrepancy for Eisenstein shell points and primes;
- general lattice-shell and circle-point distribution literature;
- well-rounded and reduced lattice-basis literature;
- standard finite-frame and condition-number theory;
- standard groupoid/cocycle language for composable coordinate changes.

No reviewed source in this targeted pass was found to package the following exact sequence as one theorem family:

1. select a point and its arithmetic conjugate as the two references of a norm shell;
2. quotient six unit rotations to three antipodal candidate pairs;
3. prove the exact three-area sum and negative shortfall-product identities;
4. obtain the sharp universal normalized-area lower bound `3/4`;
5. obtain the sharp squared condition-number bound `3`;
6. characterize the unique linear transport by its two reference images;
7. compose those transports across shells.

This negative search result is not a proof of novelty. A full review should include MathSciNet, zbMATH, Google Scholar or equivalent citation chaining, books on binary quadratic forms and lattice reduction, and expert review.

## 3. Manuscript-side candidate contribution

The candidate new contribution should be stated narrowly:

> A conjugate-pair framing of occupied Eisenstein norm shells, together with a three-choice algebraic selector having sharp normalized-area and condition-number bounds, plus the uniquely characterized composable transport between ready shell frames.

Avoid claiming:

- invention of Eisenstein prime shells;
- invention of the split-prime two-orbit classification;
- invention of basis conditioning;
- invention of coordinate-change composition;
- a new prime-distribution theorem;
- an RH bridge.

The paper’s possible novelty lies in the exact integration and the sharp selector theorem, not in any component vocabulary alone.

## 4. Current Lean coverage

Formalized now:

- coordinate ring operations and norm algebra;
- conjugation and sixfold unit rotation;
- modulo-three shell obstruction;
- three candidate determinant coordinates;
- exact sum-of-squares and product identities;
- robust frame selection;
- sharp area and axis-energy conditioning;
- unique two-reference coefficients;
- characterized transport and groupoid laws;
- exact squared condition-number definition and sharp bound.

Not yet formalized end to end:

- arbitrary split-prime existence in the form `p=a²+ab+b²`;
- the full `12`-point/two-orbit theorem for every split prime;
- the arbitrary-`n` count formula;
- a systematic literature-priority result.

## 5. Viable Mathlib route for the classical input

Mathlib 4.32.1 contains substantial infrastructure for a future end-to-end formalization:

- the third cyclotomic field and its ring of integers;
- the PID theorem for cyclotomic fields of class number one, including the third cyclotomic case;
- prime-ideal splitting data through ramification index and inertia degree;
- the theorem that, for primes not dividing the conductor, the inertia degree is the multiplicative order modulo the conductor;
- ideal norms and principal-ideal machinery.

A plausible formal route is:

1. instantiate the third cyclotomic field `ℚ(ζ₃)`;
2. prove that `p≡1 (mod 3)` has inertia degree one and ramification index one;
3. use the degree-two fundamental identity to obtain two prime ideals above `p`;
4. use the PID instance to choose a generator of one prime ideal;
5. show its algebraic norm is associated to `p`;
6. extract integer coordinates in the basis `1,η`;
7. classify associates and conjugates to obtain the two six-point orbits;
8. handle `p=3` through the ramified-prime theorem and `p≡2 (mod 3)` through inertia degree two;
9. extend by unique factorization to the arbitrary-`n` count formula.

That route is real but materially larger than the new frame theorem. Until completed, the classical shell classification remains an imported theorem with an explicit source rather than an unproved local assertion.

## 6. Reopening conditions

Reopen the literature account if:

- a source is found with the same conjugate-pair selector and sharp constants;
- the chosen norm convention changes from `a²+ab+b²`;
- the unit-rotation quotient or conditioning definition changes;
- the paper expands from local shell framing to prime distribution;
- the classical classification is fully formalized and the dependency boundary changes;
- expert review finds an equivalent standard theorem under different vocabulary.
