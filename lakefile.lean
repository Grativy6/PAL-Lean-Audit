import Lake
open Lake DSL
package FrontLean where
  version := v!"0.1.0"
require "leanprover-community" / "mathlib" @ git "v4.32.1"
lean_lib APCILeanAudit
lean_lib Experiments
@[default_target]
lean_lib FrontLean
