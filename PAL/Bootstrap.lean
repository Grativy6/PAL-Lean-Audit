import Mathlib.Data.List.Basic

/-!
# Bootstrap smoke target

This file proves no PAL claim. It exists only to verify that the pinned Lean and
Mathlib environment can compile the project before Attack Run 0001 begins.
-/

namespace PAL

/-- Infrastructure-only smoke theorem. It is not evidence for a PAL claim. -/
theorem bootstrapCompiles : True := by
  trivial

end PAL
