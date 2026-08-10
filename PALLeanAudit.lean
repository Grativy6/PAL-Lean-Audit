import PAL
import Audit

/-!
# PAL Lean Audit

Root module for the complete audit environment. External checkers use the Lake
package name as their module entry point, so this module deliberately imports
both the formalization surface and the audit surface.

Attack Run 0001 and the noncanonical Attack Run 0002 candidate audit remain
historical PAL v2.0 evidence. Attack Run 0003 is a PAL v2.1-led audit of
declared Lean realizations. These results have no authority beyond their exact
Lean statements, declared source routing, and recorded ceilings; formal audit
evidence is not PAL adoption authority and closes no PAL obligation.
-/
