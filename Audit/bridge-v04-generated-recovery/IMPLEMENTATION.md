# BRIDGE v0.4 generated-span recovery

This lane directly audits the first clause of P0195.  For a supplied
submodule `B` and linear readout `r`, `generatedRangeReadout` is the actual
restriction `r.comp B.subtype` with codomain restricted to its reachable
range.

The unrestricted theorem uses arbitrary functions: an answer factors through
the reachable readout exactly when it is constant on every readout fiber.
The linear theorem records the corresponding kernel criterion using the
named `BridgeFourSector.generatedCollision` submodule.  Identity recovery is
then equivalent to injectivity and to vanishing generated collision.

The checked countercase uses `B = top` in `Q × Q`, first-coordinate readout,
and first-coordinate answer.  The answer decodes while the readout is not
injective, so answer recovery must not be reported as full identity recovery.
The construction is mathematical factorization; it does not claim an
executable decoder, chosen representative, or source adoption.

The reachable decoder is unique because every point in the restricted range
has a preimage.  An ambient decoder can still be nonunique when the ambient
codomain is larger than the reachable image.  A nonlinear countercase also
checks that agreement on the collision subspace alone is insufficient: the
answer must be constant on every readout fiber.  These are wording and
boundary improvements for future source text and ledgers, not amendments to
BRIDGE v0.4.

Source identity is the preserved local BRIDGE v0.4 DOCX SHA-256
`a13d91a728ab6da2a5654b3263a595242397d7fb8edb17cffafdcf32036a2470`.
The direct target is P0195, interpreted with the P0107 fiber/linear-lane
boundary in the preserved source context.
