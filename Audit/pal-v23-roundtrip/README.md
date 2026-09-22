# PAL v2.3 directional roundtrip audit

This supplement to **PAL Lean Audit — Primitive Axiom Layers** tests the difference between recovering a capsule, recovering declared work, and preserving a requested answer. It is separate from historical Attack Runs 0001–0003 and leaves their source versions and receipts unchanged.

For freeze `f : W → C` and thaw `r : C → W`:

| Equation | What it preserves |
|---|---|
| `r (f w) = w` | Original declared work, after freeze then thaw |
| `f (r c) = c` | Capsule, after thaw then freeze |
| `q (r (f w)) = q w` | The particular requested answer `q` |

PAL v2.3's exact A12 capsule profile requires the first law, on declared work. It does not infer it from the second. The lossy projection fixture deliberately fails that exact profile. A stable repeat cycle can retain a requested answer and still lose another original distinction.

The new Lean module and its full declaration ledger are in `Experiments/Pal23Roundtrip.lean` and `claims.json`. `SUMMARY.md` is generated from the passing receipt; declaration counts include definitions and related formulations, not independent discoveries. `REVIEW.md` records source and proof review. `SOURCE-CORRESPONDENCE.md` maps the assumptions and limits to exact source paragraphs.

`PROPOSED-v2.3.1.md` contains candidate clarification wording only. It does not publish a PAL release or adopt a new admission rule. Christopher D. Pang remains PAL's author and adoption authority; AI systems are tools and assistants.

Reproduce with `python Audit/pal-v23-roundtrip/run.py --run --lake <lake> --source-dir <PAL DOCX directory>`. Check the saved receipt with `--check`. The CI workflow replays the bounded declarations and checks committed source snapshots; it does not claim access to the original local DOCX files.

O04, O25 and D-FIRST-OCCURRENCE remain OPEN. Storage reliability, complete bindings, environment identity, actual serialization, external effects, live-token authority and A13 fairness/liveness are outside this mathematical batch. No physical entropy premise is used.
