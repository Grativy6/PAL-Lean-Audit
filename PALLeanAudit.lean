import PAL
import Audit

/-!
# PAL Lean Audit

Root module for the complete audit environment. External checkers use the Lake
package name as their module entry point, so this module deliberately imports
both the formalization surface and the audit surface.

Attack Run 0001 and the noncanonical Attack Run 0002 candidate audit add
source-accounted bounded realizations, countermodels, and dependency receipts.
These results have no authority beyond their exact Lean statements, declared
source routing, and recorded ceilings; a checked CANDIDATE result is not PAL
canon adoption.
-/
