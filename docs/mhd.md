# MHD: constrained transport and divergence cleaning

The [GSPH/GSPMHD notes](gsph.md) describe a separate particle branch.
The [relativistic development review](relativistic-hydrodynamics.md) follows
SRMHD and GRMHD, including CT, primitive recovery, and evolving spacetime.
Neither branch is implemented by the Newtonian planar model below.

## Problem and units

The original Orszag–Tang baseline is planar 2D ideal MHD with `γ=5/3`, `μ0=1`, and `vz=Bz=0` on the
periodic unit square. Arrays are indexed `[x,y,variable]`, with state
`q=(ρ,mx,my,E,Bx,By,ψ)` and
`E=p/(γ-1)+ρ(vx²+vy²)/2+(Bx²+By²)/2`.
The Orszag–Tang initial condition is

\[
\rho=\frac{25}{36\pi},\quad p=\frac5{12\pi},\quad
\mathbf v=(-\sin2\pi y,\sin2\pi x),\quad
\mathbf B=\frac1{\sqrt{4\pi}}(-\sin2\pi y,\sin4\pi x).
\]

This is a widely used compressible-test normalization, rather than a complete
reproduction of the original incompressible MHD study by
[Orszag–Tang (1979)](https://doi.org/10.1017/S002211207900210X).
The [MASCLET paper](https://doi.org/10.1093/mnras/staa877) is one reference for
this compressible normalization.

## CT: share the same edge electric field

Store normal magnetic components on cell faces and update both directions
with a shared corner `Ez`: for example, `Bx <- Bx - Δt D_y Ez` and
`By <- By + Δt D_x Ez`. The corresponding divergence update contains
`-D_xD_y Ez+D_yD_x Ez=0`, preserving the matching discrete divergence.

This edition uses a simple flux-CT construction with arithmetic averages of
electric fields from Rusanov face fluxes. Face Riemann problems use a single
normal magnetic field; interface energy is adjusted to preserve primitive
pressure. After each update, cell-centered fields are averaged from faces.
Total energy is not reset nonconservatively. This implementation does not
reproduce every coordinate-system detail of Evans–Hawley or Athena's upwind CT.
[Evans–Hawley (1988)](https://doi.org/10.1086/166684),
[Tóth (2000)](https://doi.org/10.1006/jcph.2000.6519).

## GLM: transport and damp divergence errors

With cell-centered B and an auxiliary variable ψ, solve

\[
\partial_t\mathbf B+\nabla\cdot(\mathbf v\mathbf B-\mathbf B\mathbf v)+\nabla\psi=0,
\qquad
\partial_t\psi+c_h^2\nabla\cdot\mathbf B=-\alpha\psi.
\]

The induction flux components are `F_i(B_j)=v_i B_j-B_i v_j+δij ψ`.
This edition fixes `ch=3` and uses `α=damping*ch/h`, with `damping=0.18`.
Linear ψ damping is split off and integrated exponentially; the remaining
update uses first-order Rusanov fluxes and forward Euler. The energy variable
is conventional MHD energy without a ψ² contribution. This educational
Dedner-type model covers a subset of GLM/EGLM formulations.
[Dedner et al. (2002)](https://doi.org/10.1006/jcph.2001.6961).

## Measuring ∇·B

CT uses face-field differences; GLM uses centered differences of cell-centered
B. Records include the **operator name**, because values from different discrete
divergences cannot directly rank methods. With the fixed, relatively dissipative
GLM wave speed and symmetric OT data, centered divergence can remain extremely
small. OT alone therefore gives incomplete evidence about cleaning performance.

A separate diagnostic injects `Bx += 0.01sin(2πx)` with
`magnetic_error=0.01`, adjusting energy to preserve initial gas pressure.
This **is not the standard OT problem**. It examines divergence-wave transport
and damping while distinguishing damping from error reduction by numerical
viscosity. CT preserves an initial discrete constraint; it does not
automatically remove an existing magnetic-monopole error.

## Verification scope

Tests check periodic mass and total energy, density and pressure positivity
on selected cases, CT divergence preservation, and GLM injected-error cleaning.
The HLLD section below adds Brio–Wu, Alfvén-wave refinement and field loops.
External reference-code comparisons remain future work. The low-resolution, first-order OT figures
are introductory demonstrations of magnetic-constraint handling.

## Time evolution

The [motion gallery](movies.md) now includes separate 64² Orszag–Tang [CT](https://koyamahr.github.io/numerical-methods-atlas/#/movies?case=orszag-tang-ct) and [GLM](https://koyamahr.github.io/numerical-methods-atlas/#/movies?case=orszag-tang-glm) movies. Their actual adaptive-CFL snapshot times and native divergence diagnostics differ. Playback does not supply an equal-accuracy ranking.


## HLLD and standard wave tests

[Open the HLLD test comparisons](#/mhd-tests). These new full-vector ideal-MHD
runs retain all three velocity and magnetic components, unlike the planar
Orszag–Tang baseline above. With μ0 = 1,
q = (ρ,ρvx,ρvy,ρvz,E,Bx,By,Bz) and
E = p/(γ−1) + ρ|v|²/2 + |B|²/2.
The HLLD fan resolves the contact and two rotational waves between its outer
fast-wave bounds. Intermediate star/double-star states use one shared normal
magnetic field. Invalid intermediate states fall back to HLLE and each face
fallback is counted. [Miyoshi–Kusano (2005)](https://doi.org/10.1016/j.jcp.2005.02.017)
is the original bibliographic source; the accessible
[Athena++ HLLD implementation](https://github.com/PrincetonUniversity/athena-public-version/blob/master/src/hydro/rsolvers/mhd/hlld.cpp)
was used to cross-check the equations. This is an independent educational
implementation, not an Athena++ run or full reproduction of the paper.

All three tests use primitive MC slopes and SSPRK2 with face positivity
scaling. Step retries and HLLE fallbacks are recorded; no conserved mean is clipped.
Selected physical states staying positive is not a general robustness proof.

- **Brio–Wu:** γ = 2 on [0,1], initial discontinuity at x = 0.5,
  (ρ,p,By)L = (1,1,1), (ρ,p,By)R = (0.125,0.1,−1), Bx = 0.75,
  all velocities and Bz zero, open ends, t = 0.1, CFL 0.35.
  Compare HLLE/HLLD at 400 cells and HLLD at 800. Profiles are numerical
  grid comparisons, not exact-solution overlays or a universal uniqueness
  claim. [Brio–Wu (1988)](https://doi.org/10.1016/0021-9991(88)90120-9).
- **Circular Alfvén wave:** γ = 5/3, ρ = 1, p = 0.1, Bx = 1,
  (By,Bz) = 0.1(cos(2πx),sin(2πx)), (vy,vz) = −(By,Bz), vx = 0,
  periodic unit interval, one period t = 1, CFL 0.35. Exact conservative
  cell averages include sinc-averaged transverse fields and constant total
  energy; energy is not reconstructed from squares of averaged fields.
  HLLE and HLLD use 32, 64, 128 and 256 cells. The finest measured orders
  for the mean absolute transverse-field error are both approximately 1.98.
- **Weak magnetic loop:** γ = 5/3, ρ = p = 1, v = (2,1,0),
  Az = 10⁻³ max(0.3−r,0) on a periodic 2 × 1 box, t = 1,
  CFL 0.3, 64 × 32 and 128 × 64 cells. Compare HLLE/HLLD with each
  of CT and GLM. Finite-field translation is a diagnostic, not an exact
  solution: magnetic forces are small, not zero.

![Brio–Wu numerical profiles](figures/mhd-tests/brio-wu.png)
![Circular Alfvén-wave refinement](figures/mhd-tests/alfven.png)
![Weak magnetic-loop comparison](figures/mhd-tests/field-loop.png)

## CT-Contact and GLM scope in the loop test

CT initializes face B from a corner-potential curl. A contact-upwinded corner
EMF uses the face mass-flux sign for transverse electric-field derivatives
(CT-Contact in [Mignone–Del Zanna (2021), equations 20–22](https://arxiv.org/html/2004.10542v1)).
It reduces to the face induction flux in a grid-aligned 1D limit. This is not
the UCT-HLLD construction. The shared curl preserves the native face divergence
at each SSPRK stage; cell B is averaged from faces and total energy is not reset.

GLM initializes cell B from a centered curl of cell Az. At each face, the
longitudinal subsystem is solved first:

\[
 B_n^*=\frac{B_{n,L}+B_{n,R}}2-\frac{\psi_R-\psi_L}{2c_h},\qquad
 \psi^*=\frac{\psi_L+\psi_R}2-\frac{c_h(B_{n,R}-B_{n,L})}2.
\]

HLLD/HLLE then receives common Bn*, preserving interface primitive pressure;
fluxes of Bn and ψ are ψ* and ch²Bn*. Set ch = 4 and use exponential ψ
half-step damping with rate 0.18ch/h before/after SSPRK2. E has no ψ energy.
This is a conservative GLM model inspired by the longitudinal solve in
[Mignone–Tzeferacos (2010)](https://arxiv.org/abs/0911.3410), not their CTU
integrator or EGLM variant. The fixed cleaning speed also changes the step count.

The initial magnetic discretizations and native divergence operators differ.
Energy fractions are normalized by each run's own initial cell-field energy.
Do not infer an equal-accuracy or matched-cost CT/GLM ranking. At 128 × 64,
CT preserves native maximum divergence below 4 × 10⁻¹⁶ in these runs;
GLM's centered maximum is about 3.7 × 10⁻⁴. These operator-dependent numbers
have units of B/length. All published loop runs have zero HLLE fallbacks and
zero retries. External reference-code comparisons, stronger-field loop tests
and UCT-HLLD remain future work.

Reproduce with `python scripts/build_mhd_tests.py`. Download
[definitions, diagnostics and hashes](figures/mhd-tests/mhd-tests.json) and
[computed conservative arrays](figures/mhd-tests/fields.npz).
