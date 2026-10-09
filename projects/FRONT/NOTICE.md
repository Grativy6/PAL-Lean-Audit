# Source inheritance

This local companion was prepared by Hearthline with Chris under the activated FRONT v1.0 work key. Attribution is preserved separately from proof checking. A named theorem below is not a novelty claim.

`APCILeanAudit/Interface.lean` is a verbatim copy from `Grativy6/APCI-Lean-Audit`, commit `0f85cc7fac47c3b34ecfd11160f3efae454b900c`. It supplies the reachable-image decoder/fiber criterion. Its hash and original local path are in `Audit/dependencies.json`.

`Experiments/BridgeFourSector.lean`, `BridgeReadout.lean`, `BridgeRecovery.lean`, and `BridgeDimension.lean` are verbatim copies from `Grativy6/PAL-Lean-Audit`, commit `30fd51f8d1927d92f32fb42f68db37fec796098b`. They retain the existing BRIDGE namespaces and receipt identities. Their hashes and original paths are in `Audit/bridge-dependencies.json`.

The original correction program and fixtures retain their supplied bytes under `Audit/fixture-source`; the audit does not claim their authorship. The local `resource` shim is an explicit adaptation in `scripts/replay_correction.py`.

Lean and Mathlib retain their own authorship and license terms. The bundled checker is a second kernel check within the pinned Lean toolchain, not an independently implemented scientific referee. The original audit selected no new project license. Christopher D. Pang subsequently approved repository publication; publication remains separate from mathematical checking and does not assign new licensing terms.
