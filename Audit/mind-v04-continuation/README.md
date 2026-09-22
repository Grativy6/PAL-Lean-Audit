# MIND v0.4: protected work and continuation

This is a **reduced, branch-local Lean experiment** in PAL Lean Audit — Primitive Axiom Layers. It uses selected pieces of Christopher D. Pang's supplied MIND v0.4 draft to investigate checkpoint preservation and bounded continuation. It is not a full MIND implementation, a PAL revision, a versioned PAL conformance fixture, or a new historical Attack Run.

## Question and chosen realization

When an account is preserved, what else must survive for its continuation to agree? Can an operation make task progress without changing that account? Can administration preserve protected work while exhausting the resources needed to finish it?

The chosen task processes a finite, already-admitted queue of evidence records. Each record has a natural-number identifier and a Boolean value. A fixed Boolean rule determines which values increment a natural-number account. Each processed item produces a minimal receipt naming the before-account, evidence, rule, and after-account. The identifier is a supplied label, not an authenticated source or a claim of independent corroboration.

The model deliberately reduces MIND's richer relational account, retrieval mechanisms, and wake records. The count is an accumulator, not confidence, truth, intelligence, or a general representation of MIND's matrix. It counts matching queue entries, including repeats; identifier uniqueness and independent corroboration are not assumed or established. Boolean matching is a supplied task rule. It does not implement warranted inference. The queue is already admitted: search, retrieval, cue generation, selection, and admission are outside this experiment.

| Role | Chosen state | Preservation claim |
|---|---|---|
| Substantive account | Natural-number accumulator | May stay unchanged when a nonmatching item is processed |
| Protected work | Account, pending evidence, fixed rule, retained processing receipts | Preserved exactly by the modeled capsule roundtrip under its stated guard |
| Progress | Length of the remaining queue | Decreases per successful processing step; measures this finite task only |
| Operating state | Fuel, supplied current context/version, administrative counter | Governed separately; restoring work does not restore the old operating history |
| Capsule | Protected work and saved context/version | A mathematical record; no byte serialization or durable storage claim |

The partition is fixed for this task. Mechanics such as the rule and queue position belong to protected work because they determine future behavior. The administrative counter and fuel are outside that equality, but remain consequential to execution. Calling something outside the work projection does not make it disposable or irrelevant.

## Transitions and assumptions

A successful processing step consumes one fuel unit, removes one evidence item, applies the fixed rule, and retains a receipt even if the account does not change. A consistency predicate checks whether a receipt's recorded after-account follows from its recorded before-account, evidence, and rule. This checks internal arithmetic attribution only; it cannot authenticate the evidence, its origin, or arbitrary history supplied initially.

An administrative step consumes a fuel unit when one is available, updates its counter, and preserves protected work. A checkpoint stores the protected work with the current version. Restoration compares that saved version with a separately supplied current version and accepts only a match. It takes a newly supplied fuel budget and administrative counter. Version equality checks exactly one declared dependency. It does not certify observation freshness, grants, resource availability, target identity, or general contextual applicability. Checkpoint and restore are pure mathematical record functions here; their own time, resource cost, storage faults, and interruption behavior are not modeled.

The completion theorem concerns deterministic processing with enough fuel for the remaining queue and no intervening administrative steps, new arrivals, changed rule, or environmental changes. Administrative starvation is tested separately. Natural-number arithmetic and finite Lean lists are exact; the proofs cover arbitrary finite list lengths where quantified, rather than a numerical sample of lengths.

## Evidence targets and countercases

- Preserve exact protected work on accepted restoration; reject a changed supplied version.
- Under sufficient fuel, finish the queue and preserve final protected work across restoration.
- Compose an actual processed prefix with checkpoint restoration: the resumed remainder agrees with uninterrupted execution from the original start for the prefix plus the remaining queue length.
- Retain a consistent receipt on an update that leaves the substantive account unchanged.
- Exhibit differing continuations after discarding the rule or pending evidence while retaining the same account.
- Exhibit resource failure after an administrative step that preserves work but consumes the last available fuel.
- Reject a receipt claiming a delta unsupported by its own evidence and rule.

`claims.json` inventories the explicit Lean declarations and their source routes, assumptions, countercases, limits, and reopening conditions. Compiler-generated constructors, projections, recursors, and helper declarations are covered by module checking but are not counted as independent reported claims. Definitions and theorems are counted separately; declaration counts are not discoveries or a coverage percentage.

`SOURCE-CORRESPONDENCE.md` explains the reductions. `source-manifest.json` identifies the exact supplied PDF. `source-excerpts.json` retains selected short anchors. The PDF itself is not copied into the repository, and its intended DOI is not treated as evidence of publication. `REVIEW.md` records review findings and dispositions.

## Running and checking

Use the repository's pinned Lean toolchain. The runner compiles the new module, checks its exact signatures and axiom dependencies, runs the bundled kernel checker, and runs the repository's relevant baseline checks. Final evidence is produced sequentially.

```text
python Audit/mind-v04-continuation/run.py --check-inputs
python Audit/mind-v04-continuation/run.py --replay --lake lake --source-pdf /path/to/MIND_v0.4_Draft.pdf --output-dir artifacts/mind-continuation-local --record
python Audit/mind-v04-continuation/run.py --check --require-artifacts
```

Only a run supplied with the PDF can independently bind the excerpts to the source bytes. A replay without it checks the recorded source identity and excerpts as inputs, not the unavailable PDF. Raw logs and execution manifests remain in the selected local artifact directory. The compact `results.json`, when present, records the actual completed checks and their hashes. `--check --require-artifacts` also requires every raw log and manifest. On a different checkout without that local artifact directory, plain `--check` validates the recorded receipt against current inputs and explicitly reports that raw evidence requires replay. If the artifact directory exists, missing or changed files fail either mode. The CI workflow follows its portable recorded-receipt check with a fresh replay. A workflow definition is preparation, not evidence that CI has executed.

Each declaration's exact printed signature and imported-axiom list are frozen in the claim ledger and compared during replay, so adding even an otherwise permitted axiom or weakening a theorem type requires an explicit ledger change. Source inputs carry both exact checkout hashes and separately labeled CRLF-to-LF hashes for cross-platform comparison. The PDF digest always identifies exact bytes.

## Scope, grant, and reopening

This local proposal starts from `93d9c7811e833b57367d1939c862b08fd8d187bb`, the head of still-open PR #18 when work began. It does not modify that PR or treat it as merged. Christopher requested the next Lean experiment using MIND's pieces. The working grant is local source analysis, bounded implementation, verification, and review. No publication, release amendment, external action, or deployment follows from this experiment.

Finish means checked model/proofs, source correspondence, reviewed countercases, and reproducible local receipts. Remaining implementation needs include a chosen byte format, actual storage/recovery, source authentication, external dependency checks, interruption/crash behavior, and a scheduler contract. MIND's wider account, empirical benefits, and CHARTER adapter remain outside the checked model. PAL's O04, O25, and D-FIRST-OCCURRENCE remain OPEN; unresolved possibility is not encoded as an object.

Reopen this experiment if the account, evidence, rule, retained history, progress measure, resource accounting, capsule fields, version guard, or continuation policy changes. Christopher D. Pang retains authorship and adoption authority; AI systems are tools and assistants.
