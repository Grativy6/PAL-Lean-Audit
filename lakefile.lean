import Lake

open Lake DSL

package PALLeanAudit where
  version := v!"0.1.0"

require "leanprover-community" / "mathlib" @ git "v4.32.1"

lean_lib PAL

lean_lib Audit

@[default_target]
lean_lib PALLeanAudit
