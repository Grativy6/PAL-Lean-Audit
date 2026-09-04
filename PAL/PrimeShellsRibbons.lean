import PAL.PrimeShellsThreeCharts

/-!
# Shell atlases and trace-bearing ribbons

Version 0.2 lifts the local framed shell of version 0.1 into two larger objects:

* an indexed atlas whose points retain a represented rational prime, a selected
  conjugate frame, and its certified quality bounds; and
* an ordered ribbon whose route remains available even when the existing flat
  transport collapses the composite map to its two endpoints.

The exact prime index is discrete. Any smooth visual strip drawn between its
vertices is a rendering layer and not additional arithmetic evidence.
-/

namespace PAL.PrimeShells

noncomputable section

section GenericRibbons

/-- A nonempty ordered route. `extend` appends a new terminal vertex. -/
inductive Ribbon (A : Type*) where
  | singleton (point : A)
  | extend (prior : Ribbon A) (point : A)
  deriving Repr

namespace Ribbon

/-- First vertex of a ribbon. -/
def start {A : Type*} : Ribbon A → A
  | .singleton point => point
  | .extend prior _ => start prior

/-- Last vertex of a ribbon. -/
def finish {A : Type*} : Ribbon A → A
  | .singleton point => point
  | .extend _ point => point

/-- Number of transported edges. -/
def edgeCount {A : Type*} : Ribbon A → ℕ
  | .singleton _ => 0
  | .extend prior _ => edgeCount prior + 1

/-- Ordered vertex list, retained independently of the endpoint. -/
def vertices {A : Type*} : Ribbon A → List A
  | .singleton point => [point]
  | .extend prior point => vertices prior ++ [point]

/-- Apply a map without erasing the order of the route. -/
def map {A B : Type*} (f : A → B) : Ribbon A → Ribbon B
  | .singleton point => .singleton (f point)
  | .extend prior point => .extend (map f prior) (f point)

@[simp] theorem start_singleton {A : Type*} (point : A) :
    start (.singleton point) = point := rfl

@[simp] theorem start_extend {A : Type*} (prior : Ribbon A) (point : A) :
    start (.extend prior point) = start prior := rfl

@[simp] theorem finish_singleton {A : Type*} (point : A) :
    finish (.singleton point) = point := rfl

@[simp] theorem finish_extend {A : Type*} (prior : Ribbon A) (point : A) :
    finish (.extend prior point) = point := rfl

@[simp] theorem edgeCount_singleton {A : Type*} (point : A) :
    edgeCount (.singleton point) = 0 := rfl

@[simp] theorem edgeCount_extend {A : Type*} (prior : Ribbon A) (point : A) :
    edgeCount (.extend prior point) = edgeCount prior + 1 := rfl

@[simp] theorem start_map {A B : Type*} (f : A → B) (route : Ribbon A) :
    start (map f route) = f (start route) := by
  induction route with
  | singleton point => rfl
  | extend prior point ih => exact ih

@[simp] theorem finish_map {A B : Type*} (f : A → B) (route : Ribbon A) :
    finish (map f route) = f (finish route) := by
  cases route <;> rfl

@[simp] theorem edgeCount_map {A B : Type*} (f : A → B) (route : Ribbon A) :
    edgeCount (map f route) = edgeCount route := by
  induction route with
  | singleton point => rfl
  | extend prior point ih => simp [map, edgeCount, ih]

end Ribbon

end GenericRibbons

section PrimeShellAtlas

/-- A rational prime together with one exact supplied Eisenstein norm
representation. This structure does not produce the representation. -/
structure RepresentedPrimeShell where
  p : ℕ
  isPrime : p.Prime
  a : ℤ
  b : ℤ
  norm_eq : a ^ 2 + a * b + b ^ 2 = (p : ℤ)

/-- Real coordinate representative attached to a supplied arithmetic shell. -/
def representedPoint (shell : RepresentedPrimeShell) : Point ℝ :=
  ⟨shell.a, shell.b⟩

/-- One atlas point carries the shell address, selected unit representative,
readiness, normalized-area bound, and condition-number bound. -/
structure FramedPrimeShell where
  shell : RepresentedPrimeShell
  choice : FrameChoice
  ready : FrameReady (choosePoint choice (representedPoint shell))
  strength :
    (3 : ℝ) / 4 ≤ frameStrengthSq (choosePoint choice (representedPoint shell))
  condition :
    frameConditionNumberSq (choosePoint choice (representedPoint shell)) ≤ 3

/-- The type of all supplied, certified framed prime-shell states. -/
abbrev FramedPrimeShellAtlas := FramedPrimeShell

/-- Selected frame point carried by an atlas entry. -/
def atlasFrame (entry : FramedPrimeShellAtlas) : Point ℝ :=
  choosePoint entry.choice (representedPoint entry.shell)

/-- Shell label retained by the atlas. -/
def atlasPrime (entry : FramedPrimeShellAtlas) : ℕ := entry.shell.p

/-- Every supplied represented prime shell admits at least one certified atlas
entry by the sharp selector from version 0.1. -/
theorem representedPrimeShell_has_atlasPoint (shell : RepresentedPrimeShell) :
    ∃ entry : FramedPrimeShellAtlas, entry.shell = shell := by
  obtain ⟨choice, hChoice⟩ :=
    prime_shell_has_sharply_conditioned_frame shell.isPrime shell.norm_eq
  dsimp at hChoice
  rcases hChoice with ⟨hReady, hStrength, hBound⟩
  have hCondition :
      frameConditionNumberSq
          (choosePoint choice (representedPoint shell)) ≤ 3 := by
    apply frameConditionNumberSq_le_of_conditionBound
    · simpa [representedPoint] using hReady
    · simpa [representedPoint] using hBound
  refine ⟨{
    shell := shell
    choice := choice
    ready := ?_
    strength := ?_
    condition := hCondition
  }, rfl⟩
  · simpa [representedPoint] using hReady
  · simpa [representedPoint] using hStrength

/-- An exact prime-shell ribbon is an ordered route through certified atlas
entries. -/
abbrev PrimeShellRibbon := Ribbon FramedPrimeShellAtlas

end PrimeShellAtlas

section ReadyFrameRibbons

/-- A ribbon whose every vertex is a frame-ready point. -/
inductive ReadyRibbon where
  | singleton (point : Point ℝ) (ready : FrameReady point)
  | extend (prior : ReadyRibbon) (point : Point ℝ) (ready : FrameReady point)

namespace ReadyRibbon

/-- First frame of a ready ribbon. -/
def start : ReadyRibbon → Point ℝ
  | .singleton point _ => point
  | .extend prior _ _ => start prior

/-- Last frame of a ready ribbon. -/
def finish : ReadyRibbon → Point ℝ
  | .singleton point _ => point
  | .extend _ point _ => point

/-- Number of transport edges retained by the route. -/
def edgeCount : ReadyRibbon → ℕ
  | .singleton _ _ => 0
  | .extend prior _ _ => edgeCount prior + 1

/-- Readiness of the first frame. -/
theorem start_ready : ∀ route : ReadyRibbon, FrameReady (start route)
  | .singleton _ ready => ready
  | .extend prior _ _ => start_ready prior

/-- Readiness of the last frame. -/
theorem finish_ready : ∀ route : ReadyRibbon, FrameReady (finish route)
  | .singleton _ ready => ready
  | .extend _ _ ready => ready

/-- Compose the version-0.1 frame transport along every edge of a ribbon. -/
def applyTransport : ReadyRibbon → Point ℝ → Point ℝ
  | .singleton _ _ => fun vector => vector
  | .extend prior point _ => fun vector =>
      transport (finish prior) point (applyTransport prior vector)

/-- The present transport is flat: every finite ribbon composite is determined
by its first and last frames. The route remains separate data. -/
theorem applyTransport_eq_direct (route : ReadyRibbon) (vector : Point ℝ) :
    applyTransport route vector = transport (start route) (finish route) vector := by
  induction route with
  | singleton point ready =>
      simpa [applyTransport, start, finish] using
        (transport_self point vector ready).symm
  | extend prior point ready ih =>
      change
        transport (finish prior) point (applyTransport prior vector) =
          transport (start prior) point vector
      rw [ih]
      exact transport_compose
        (start prior) (finish prior) point vector
        (start_ready prior) (finish_ready prior)

end ReadyRibbon

/-- Convert an atlas ribbon into the corresponding ready-frame ribbon. -/
def primeRibbonFrames : PrimeShellRibbon → ReadyRibbon
  | .singleton entry => .singleton (atlasFrame entry) entry.ready
  | .extend prior entry =>
      .extend (primeRibbonFrames prior) (atlasFrame entry) entry.ready

@[simp] theorem primeRibbonFrames_start (route : PrimeShellRibbon) :
    ReadyRibbon.start (primeRibbonFrames route) = atlasFrame (Ribbon.start route) := by
  induction route with
  | singleton entry => rfl
  | extend prior entry ih => exact ih

@[simp] theorem primeRibbonFrames_finish (route : PrimeShellRibbon) :
    ReadyRibbon.finish (primeRibbonFrames route) = atlasFrame (Ribbon.finish route) := by
  cases route <;> rfl

/-- Composite transport associated with a prime-shell ribbon. -/
def primeRibbonTransport (route : PrimeShellRibbon) (vector : Point ℝ) : Point ℝ :=
  ReadyRibbon.applyTransport (primeRibbonFrames route) vector

/-- Prime-shell ribbon transport is endpoint-determined even though the ordered
atlas route remains available independently. -/
theorem primeRibbonTransport_eq_endpoints
    (route : PrimeShellRibbon) (vector : Point ℝ) :
    primeRibbonTransport route vector =
      transport (atlasFrame (Ribbon.start route))
        (atlasFrame (Ribbon.finish route)) vector := by
  rw [primeRibbonTransport, ReadyRibbon.applyTransport_eq_direct]
  simp

end ReadyFrameRibbons

section RouteSeparationFixture

/-- Selected ready frame on the norm-3 shell. -/
def selectedFrame3 : Point ℝ := choosePoint .base ⟨1, 1⟩

/-- Selected ready frame on the norm-7 shell. -/
def selectedFrame7 : Point ℝ := choosePoint .turnTwice ⟨2, 1⟩

/-- Selected ready frame on the norm-13 shell. -/
def selectedFrame13 : Point ℝ := choosePoint .turnTwice ⟨3, 1⟩

@[simp] theorem selectedFrame3_ready : FrameReady selectedFrame3 := by
  norm_num [selectedFrame3, FrameReady, choosePoint, rotate, xCoord, yCoord]

@[simp] theorem selectedFrame7_ready : FrameReady selectedFrame7 := by
  norm_num [selectedFrame7, FrameReady, choosePoint, rotate, xCoord, yCoord]

@[simp] theorem selectedFrame13_ready : FrameReady selectedFrame13 := by
  norm_num [selectedFrame13, FrameReady, choosePoint, rotate, xCoord, yCoord]

@[simp] theorem selectedFrame3_norm : eNorm selectedFrame3 = 3 := by
  norm_num [selectedFrame3, choosePoint, rotate, eNorm]

@[simp] theorem selectedFrame7_norm : eNorm selectedFrame7 = 7 := by
  norm_num [selectedFrame7, choosePoint, rotate, eNorm]

@[simp] theorem selectedFrame13_norm : eNorm selectedFrame13 = 13 := by
  norm_num [selectedFrame13, choosePoint, rotate, eNorm]

/-- Direct route from the norm-3 frame to the norm-13 frame. -/
def directPrimeFrameRibbon : ReadyRibbon :=
  .extend (.singleton selectedFrame3 selectedFrame3_ready)
    selectedFrame13 selectedFrame13_ready

/-- A different route with the norm-7 frame retained between the same
endpoints. -/
def viaPrimeFrameRibbon : ReadyRibbon :=
  .extend
    (.extend (.singleton selectedFrame3 selectedFrame3_ready)
      selectedFrame7 selectedFrame7_ready)
    selectedFrame13 selectedFrame13_ready

/-- The direct and via routes have the same endpoints. -/
theorem primeFrameRibbons_same_endpoints :
    ReadyRibbon.start directPrimeFrameRibbon =
        ReadyRibbon.start viaPrimeFrameRibbon ∧
      ReadyRibbon.finish directPrimeFrameRibbon =
        ReadyRibbon.finish viaPrimeFrameRibbon := by
  constructor <;> rfl

/-- The routes remain different because one retains an intermediate prime-shell
frame and the other does not. -/
theorem primeFrameRibbons_different_routes :
    directPrimeFrameRibbon ≠ viaPrimeFrameRibbon := by
  intro h
  have hEdges := congrArg ReadyRibbon.edgeCount h
  norm_num [directPrimeFrameRibbon, viaPrimeFrameRibbon,
    ReadyRibbon.edgeCount] at hEdges

/-- Despite their different ordered histories, the current flat transport gives
the same endpoint map. -/
theorem primeFrameRibbons_same_transport (vector : Point ℝ) :
    ReadyRibbon.applyTransport directPrimeFrameRibbon vector =
      ReadyRibbon.applyTransport viaPrimeFrameRibbon vector := by
  rw [ReadyRibbon.applyTransport_eq_direct,
    ReadyRibbon.applyTransport_eq_direct]
  rfl

end RouteSeparationFixture

end

end PAL.PrimeShells
