# BRIDGE dimension and recovery bounded audit

**PASS_BRIDGE_DIMENSION_RECOVERY**

| Population | Count |
|---|---:|
| New dimension declarations | 7 |
| New recovery declarations | 11 |
| Prior diagram/readout declarations | 19 |
| Prior four-sector declarations | 14 |
| New receipt rejection guards (not theorems) | 18 |

Checked targets: finite-dimensional four-sector accounting; the actual residual readout kernel; linear answer factorization; and full residual identity recovery iff the hidden quotient is zero iff ker(r) is contained in B. The generated-span answer criterion and checked countercases are described in the claim ledgers. Helpers share dependencies and are not independent discoveries.

All 16 controller commands passed, including a pinned historical replay with its own eighteen commands. Axiom inventories and bundled kernel checks are retained. The prior replay checks commit 1babbcd19b51bba46dc9a51365dcadbe31bf1763, separately from the current candidate. Source bytes and 95 original OOXML paragraphs were checked locally; CI verifies committed snapshots without rereading the absent DOCX.

[Dimension claims](dimension-claims.json) · [Recovery claims](recovery-claims.json) · [Source correspondence](SOURCE-CORRESPONDENCE.md) · [Execution and hashes](results.json)

FS-M04 receives new evidence within the declared linear realization; its historical OPEN_MANUAL record remains intact. PAL obligations O04, O25 and D-FIRST-OCCURRENCE remain OPEN. Geometric/Hodge applications, frame morphisms, source adoption and merge remain outside this batch.

Reproduce: python Audit/bridge-v04-dimension-recovery/run.py --run --lake <lake> --source-file <BRIDGE_v0.4.docx>. Check saved evidence with --check; replay into a new directory with --replay --output-dir <directory>.
