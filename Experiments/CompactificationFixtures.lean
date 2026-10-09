import Mathlib

namespace Experiments.CompactificationFixtures
open Function Finset

theorem fiber_answer_bound {W T Q S : Type*} [Fintype W] [Fintype S]
    [DecidableEq T] [DecidableEq Q] [DecidableEq S]
    (t : W → T) (q : W → Q) (side : W → S) (d : T × S → Q)
    (recover : ∀ w, d (t w,side w) = q w) (v : T) :
    ((univ.filter (fun w => t w = v)).image q).card ≤ Fintype.card S := by
  calc
    _ ≤ (univ.image (fun s => d (v,s))).card := by
      apply card_le_card
      intro a ha
      obtain ⟨w,hw,rfl⟩ := mem_image.mp ha
      exact mem_image.mpr ⟨side w, mem_univ _, by rw [← (mem_filter.mp hw).2]; exact recover w⟩
    _ ≤ _ := (card_image_le).trans_eq (card_univ)

theorem maximum_answer_bound {W T Q S : Type*} [Fintype W] [Fintype S]
    [DecidableEq T] [DecidableEq Q] [DecidableEq S]
    (t : W → T) (q : W → Q) (side : W → S) (d : T × S → Q)
    (recover : ∀ w, d (t w,side w) = q w) :
    univ.sup (fun w : W => ((univ.filter (fun x => t x = t w)).image q).card) ≤ Fintype.card S := by
  exact Finset.sup_le (fun w _ => fiber_answer_bound t q side d recover (t w))

def cube (v : Bool × Bool × Bool) : ℤ × ℤ :=
  ((if v.1 then 1 else 0) - (if v.2.2 then 1 else 0),
   (if v.2.1 then 1 else 0) - (if v.2.2 then 1 else 0))

def cubeEdges : Finset (Finset (Bool × Bool × Bool)) :=
  (univ.filter (fun p : (Bool × Bool × Bool) × (Bool × Bool × Bool) =>
    (if p.1.1 = p.2.1 then 0 else 1) +
    (if p.1.2.1 = p.2.2.1 then 0 else 1) +
    (if p.1.2.2 = p.2.2.2 then 0 else 1) = (1 : ℕ))).image
      (fun p => {p.1,p.2})

theorem cube_vertex_and_edge_counts :
    (univ.image cube).card = 7 ∧ cubeEdges.card = 12 ∧
    (cubeEdges.image (fun edge => edge.image cube)).card = 12 := by decide +kernel

theorem cube_fibers : ∀ a b : Bool × Bool × Bool,
    cube a = cube b ↔ a = b ∨
      (a = (false,false,false) ∧ b = (true,true,true)) ∨
      (b = (false,false,false) ∧ a = (true,true,true)) := by decide +kernel

theorem cube_side_bit : Injective (fun v : Bool × Bool × Bool => (cube v,v.1)) := by
  intro a b h
  have hc := (cube_fibers a b).mp (congrArg Prod.fst h)
  rcases hc with h | ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩
  · exact h
  · cases congrArg Prod.snd h
  · cases congrArg Prod.snd h

noncomputable def omega : ℂ := Complex.exp (((2 * Real.pi / 3 : ℝ) : ℂ) * Complex.I)

theorem omega_coordinates : omega = (-1/2 : ℂ) + (Real.sqrt 3 / 2 : ℝ) * Complex.I := by
  have hc : Real.cos (2 * Real.pi / 3) = -1/2 := by
    rw [show 2 * Real.pi / 3 = Real.pi - Real.pi / 3 by ring, Real.cos_pi_sub]
    norm_num
  have hs : Real.sin (2 * Real.pi / 3) = Real.sqrt 3 / 2 := by
    rw [show 2 * Real.pi / 3 = Real.pi - Real.pi / 3 by ring, Real.sin_pi_sub]
    exact Real.sin_pi_div_three
  rw [omega,Complex.exp_mul_I, ← Complex.ofReal_cos, ← Complex.ofReal_sin,hc,hs]
  push_cast
  ring

theorem omega_quadratic : 1 + omega + omega ^ 2 = 0 := by
  have h := Real.sq_sqrt (show (0:ℝ) ≤ 3 by norm_num)
  apply Complex.ext <;> simp [omega_coordinates,Complex.mul_re,Complex.mul_im,pow_two] <;> nlinarith

def lattice (w : ℂ) (p : ℤ × ℤ) : ℂ := p.1 + p.2 * w

theorem lattice_injective (w : ℂ) (hw : w.im ≠ 0) : Injective (lattice w) := by
  rintro ⟨a,b⟩ ⟨c,d⟩ h
  have hi := congrArg Complex.im h
  have hr := congrArg Complex.re h
  simp [lattice] at hi hr
  have hb : b = d := hi.resolve_right hw
  subst d
  have ha : (a:ℝ) = c := by linarith
  exact Prod.ext (by exact_mod_cast ha) rfl

theorem omega_nonreal : omega.im ≠ 0 := by
  rw [omega_coordinates]
  norm_num

theorem actual_cube_projection (v : Bool × Bool × Bool) :
    (if v.1 then 1 else 0 : ℂ) + (if v.2.1 then 1 else 0) * omega +
      (if v.2.2 then 1 else 0) * omega^2 = lattice omega (cube v) := by
  have h := omega_quadratic
  rcases v with ⟨a,b,c⟩
  cases a <;> cases b <;> cases c <;> norm_num [cube,lattice] <;> linear_combination h

theorem complex_projection_counts :
    (univ.image (lattice omega ∘ cube)).card = 7 ∧
    (cubeEdges.image (fun edge => edge.image (lattice omega ∘ cube))).card = 12 := by
  classical
  have hi := lattice_injective omega omega_nonreal
  constructor
  · rw [← Finset.image_image,Finset.card_image_of_injective _ hi]
    exact cube_vertex_and_edge_counts.1
  · have h : (fun edge : Finset (Bool × Bool × Bool) => edge.image (lattice omega ∘ cube)) =
        (fun edge : Finset (ℤ × ℤ) => edge.image (lattice omega)) ∘ (fun edge => edge.image cube) := by
      funext edge
      simp [Function.comp_def,Finset.image_image]
    rw [h,← Finset.image_image,Finset.card_image_of_injective _ (Finset.image_injective hi)]
    exact cube_vertex_and_edge_counts.2.2

theorem discrete_hub_size : (univ.filter (fun v => cube v = (0,0))).card = 2 := by decide +kernel

noncomputable def mean : (Fin 6 → ℝ) →ₗ[ℝ] ℝ where
  toFun x := (∑ j, x j) / 6
  map_add' x y := by simp [sum_add_distrib,add_div]
  map_smul' a x := by
    change (∑ j, a*x j)/6 = a*((∑ j,x j)/6)
    rw [← Finset.mul_sum]
    ring

noncomputable def common (x : Fin 6 → ℝ) : Fin 6 → ℝ := fun _ => mean x
noncomputable def residual (x : Fin 6 → ℝ) : Fin 6 → ℝ := x - common x

theorem mean_constant (a : ℝ) : mean (fun _ => a) = a := by simp [mean]

theorem mean_surjective : Surjective mean := fun a => ⟨fun _ => a,mean_constant a⟩

theorem comparison_dimension : Module.finrank ℝ mean.ker = 5 := by
  have h := mean.finrank_range_add_finrank_ker
  rw [LinearMap.range_eq_top.mpr mean_surjective] at h
  simp at h
  omega

theorem common_comparison_reconstruction (x : Fin 6 → ℝ) :
    common x + residual x = x ∧ mean (residual x) = 0 := by
  constructor
  · simp [residual]
  · change mean (x - common x) = 0
    rw [map_sub,show mean (common x) = mean x from mean_constant (mean x),sub_self]

theorem mean_fiber (x y : Fin 6 → ℝ) : mean x = mean y ↔ x-y ∈ mean.ker := by
  simp [LinearMap.mem_ker,map_sub,sub_eq_zero]

theorem mean_loses_comparisons : ∃ x : Fin 6 → ℝ, mean x = mean 0 ∧ residual x ≠ residual 0 := by
  let x : Fin 6 → ℝ := fun j => if j.val = 0 then 1 else if j.val = 1 then -1 else 0
  have hm : mean x = 0 := by norm_num [mean,x,Fin.sum_univ_succ] <;> decide
  refine ⟨x,by simpa using hm,?_⟩
  intro h
  have h0 := congrFun h 0
  change x 0 - mean x = 0 - mean 0 at h0
  rw [hm,map_zero] at h0
  norm_num [x] at h0

noncomputable def sectorInteger (x : ℝ) : ℤ := ⌊6*x+1/2⌋
noncomputable def sector (x : ℝ) : ℤ := sectorInteger x % 6
noncomputable def angularResidual (x : ℝ) : ℝ := x - (sectorInteger x : ℝ)/6

theorem residual_bounds (x : ℝ) : -1/12 ≤ angularResidual x ∧ angularResidual x < 1/12 := by
  have hl := Int.floor_le (6*x+1/2)
  have hu := Int.lt_floor_add_one (6*x+1/2)
  dsimp [angularResidual,sectorInteger]
  constructor <;> linarith

theorem sector_range (x : ℝ) : 0 ≤ sector x ∧ sector x < 6 := by
  exact ⟨Int.emod_nonneg _ (by norm_num),Int.emod_lt_of_pos _ (by norm_num)⟩

theorem phase_reconstruction (x : ℝ) :
    x = (sector x : ℝ)/6 + angularResidual x + (sectorInteger x / 6 : ℤ) := by
  have h : ((sectorInteger x % 6 : ℤ) : ℝ) + 6 * ((sectorInteger x / 6 : ℤ) : ℝ) = sectorInteger x := by
    exact_mod_cast Int.emod_add_mul_ediv (sectorInteger x) 6
  dsimp [sector,angularResidual]
  linarith

theorem radians_reconstruction (theta : ℝ) :
    ∃ n : ℤ, theta = (sector (theta/(2*Real.pi)) : ℝ)*Real.pi/3 +
      (2*Real.pi)*angularResidual (theta/(2*Real.pi)) + (2*Real.pi)*n := by
  refine ⟨sectorInteger (theta/(2*Real.pi)) / 6, ?_⟩
  have h := phase_reconstruction (theta/(2*Real.pi))
  have hp := Real.pi_pos
  field_simp at h
  nlinarith

theorem sector_collision_and_tie :
    sector 0 = sector (1/24) ∧ (0:ℝ) ≠ 1/24 ∧
    sector (1/12) = 1 ∧ angularResidual (1/12) = -1/12 := by
  norm_num [sector,sectorInteger,angularResidual,Int.floor_eq_iff]

end Experiments.CompactificationFixtures
