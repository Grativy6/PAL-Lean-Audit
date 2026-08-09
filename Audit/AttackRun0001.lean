import PAL.AttackRun0001

/-!
# Attack Run 0001 dependency receipts

Each command below asks Lean to report the axioms used by an adopted bounded
result. T05 is intentionally outside this list: its literal-identifier check
is enforced by the repository policy scan and deterministic rejected fixtures,
not by making unresolved possibility an object-language proposition. This
lexical check cannot detect differently named semantic surrogates.
-/

#print axioms PAL.AttackRun0001.noCutWithoutWitness
#print axioms PAL.AttackRun0001.noReflectionWithoutWitness
#print axioms PAL.AttackRun0001.noTurnWithoutWitness
#print axioms PAL.AttackRun0001.noReadableWithoutWitness
#print axioms PAL.AttackRun0001.noTraceWithoutWitness
#print axioms PAL.AttackRun0001.reflectionForgetsToIndexedCut
#print axioms PAL.AttackRun0001.cutAddressNeReflectionAddress
#print axioms PAL.AttackRun0001.turnForgetsToIndexedReflection
#print axioms PAL.AttackRun0001.turnCountermodelIsInhabited
#print axioms PAL.AttackRun0001.thetaDoesNotProvideReadable
#print axioms PAL.AttackRun0001.primitivePlacement
#print axioms PAL.AttackRun0001.floorChainReturnsCut
#print axioms PAL.AttackRun0001.readableForgetsToIndexedTurn
#print axioms PAL.AttackRun0001.traceForgetsToIndexedReadable
#print axioms PAL.AttackRun0001.readableDoesNotProvideTrace
#print axioms PAL.AttackRun0001.allLayersHaveStrictPredecessor
#print axioms PAL.AttackRun0001.noLayerExtensionWithoutWitness
#print axioms PAL.AttackRun0001.missingWitnessYieldsNoOutput
#print axioms PAL.AttackRun0001.noRelationStageWithoutWitness
#print axioms PAL.AttackRun0001.routePreservesProtectedTrace
#print axioms PAL.AttackRun0001.authorizedCompressionRestores
#print axioms PAL.AttackRun0001.noAuthorityBackflow
