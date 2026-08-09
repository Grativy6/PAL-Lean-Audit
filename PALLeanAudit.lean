/-!
# PAL Lean Audit

Root module for the complete audit environment. External checkers use the Lake
package name as their module entry point, so this module deliberately imports
both the formalization surface and the audit surface.

The bootstrap still makes no substantive PAL claim.
-/

import PAL
import Audit
