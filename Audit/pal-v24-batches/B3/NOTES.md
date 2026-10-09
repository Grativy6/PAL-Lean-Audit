# B3 bounded realization notes

This batch realizes only a finite binary nested account for candidate SC-22,
D42, O65, T75, M-NESTED-ACCOUNT, and the cited PAL v2.3 A13/A14 resource and
epoch boundaries.  Candidate document byte hashes and paragraph bindings are
pending the controller's source freeze; the ledger therefore deliberately has
no fabricated source-input hash.

The model uses natural-number charges, exact unit tags, supplied event IDs,
and an inductive binary tree.  Unknown is `none`, never numeric zero.  Equal
unit tags compose; a mismatch rejects.  The recursive/flattened aggregate
identity is unconditional over the supplied tree.  A separate accepted-account
theorem combines that identity with `Nodup` of the supplied flattened event
IDs; count-once therefore depends on treating those IDs as identity keys and
does not establish external event identity or completeness.

Appending a known root event is an unconditional arithmetic identity for any
account, ID, and natural-number amount.  It does not check scope, ID freshness,
unit compatibility, or acceptedness; callers must revalidate.  A linked epoch
adds supplied prior spend when the caller supplies the link flag; unlinked
reset is unresolved.

Positive fixtures cover compatible two- and three-level accounts.  Negative
fixtures cover a promised missing child, same-node and parent-child duplicate
IDs, mismatched unit, unknown required charge, and unrecorded reset.  The
T75-routed administrative exhaustion fixture returns denial and preserves the
nested-account projection bundled in `AccountWork`.  It does not represent the
full protected work state, a scheduler, real resource contention, or other
protected fields; the unchanged projection follows from the declared model
transition, not from an external enforcement mechanism.

Limits: no flat cycle validator, arbitrary branching, unit conversion,
measurement/calibration, real-world inventory completeness, external source
authentication, spending permission, resume authority, or PAL adoption.
