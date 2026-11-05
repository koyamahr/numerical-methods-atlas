# Godunov smoothed particle hydrodynamics (GSPH)

**Status: source-based reading notes and an implementation plan.** The existing
[SPH example](particles-sph.md) reconstructs fields; it does not advance a GSPH
fluid. No GSPH benchmark result is claimed here.

## Inutsuka's formulation

[Inutsuka (2002)](https://doi.org/10.1006/jcph.2002.7053) derives particle
evolution from convolutions of the fluid equations. Pairwise Riemann problems
supply pressure and velocity for the interactions, replacing a separately
prescribed shock artificial viscosity. Riemann dissipation still remains.
The [author's preprint, sections 2–3](https://arxiv.org/html/astro-ph/0206401)
is the equation reference. It also cites the earlier *Godunov-type SPH*
contribution (1994); that original report has not been inspected here.

For a common Gaussian smoothing length, a linear approximation to specific
volume V = 1/rho gives the overlap coefficient (equations 48–52)

\[
C_{ij}=\frac{V_i-V_j}{|\mathbf x_i-\mathbf x_j|},\qquad
D_{ij}=\frac{V_i+V_j}{2},\qquad
V_{ij}^{2}(h)=D_{ij}^{2}+\frac{h^2 C_{ij}^{2}}4.
\]

Equation 65 then uses the pair pressure in the momentum update:

\[
\frac{d\mathbf v_i}{dt}
=-2\sum_j m_j P^*_{ij}V_{ij}^{2}(h)
\nabla_i W(\mathbf x_i-\mathbf x_j,\sqrt{2}h).
\]

This is the common-h Gaussian form. The paper's variable-h expressions and
time-centered internal-energy update are needed for its conservation argument.
Changing only the pressure in an existing SPH force is not that derivation.

## Connecting the existing exhibits

The implementation path joins [particle kernels](particles-sph.md),
[Euler Riemann solvers](benchmarks.md), and moving-particle time integration.
The current interpolation uses a compact cubic kernel; the derivation above
uses a Gaussian and its overlap. Their kernel-width conventions must be kept
explicit. The existing fixed-grid flux returns F(U), whereas a GSPH pair update
needs a consistently oriented star pressure and velocity. Reusing a flux
function alone does not provide a complete particle interaction.

## A staged verification plan

1. Check kernel overlaps, specific-volume reconstruction, pair orientation,
   equal and unequal masses, and uniform-pressure consistency.
2. Advance pair forces and internal energy with a matched time update; measure
   momentum and total-energy drift before adding adaptive smoothing lengths.
3. Run a smooth acoustic wave and an advected contact with controlled particle
   spacing and smoothing scale. Separate interpolation and time-step refinement.
4. Compare the paper's first shock tube (equation 89, Figure 2) with its exact
   Euler solution, then add the shared Sod and Shu–Osher tests. Record particle
   masses, spacing, neighbors, boundary reservoirs, and reconstruction choices.

For that first published shock tube, the primitive left/right states are
(rho, v, p) = (1, 0, 1) and (0.5, 0, 0.2), gamma = 1.4, at t = 0.2.
It differs from the standard Sod parameters used elsewhere in this atlas.
These are proposed verification targets, not computed GSPH results.

## The MHD branch

[Iwasaki and Inutsuka (2011)](https://doi.org/10.1111/j.1365-2966.2011.19588.x)
extend the particle approach: compressive interactions use a nonlinear Riemann
problem with magnetic pressure, while Alfvén waves use characteristics.
Their [paper](https://arxiv.org/abs/1106.3389) includes Alfvén, shock-tube,
Orszag–Tang, rotor, and magnetized-blast tests. This is a separate GSPMHD
implementation direction; the atlas's existing grid-based [CT/GLM](mhd.md)
does not implement it. Particle magnetic-divergence and tensile-instability
treatments would require their own verification.

## Special-relativistic continuation

[Kitajima, Inutsuka, and Seno (2026)](https://doi.org/10.1016/j.jcp.2025.114448)
develop SRGSPH with a relativistic Riemann solver, unequal particle baryon
numbers, and variable smoothing lengths. The preprint dates to 2025; the
journal issue is 2026. This is special relativity, not a general-relativistic
fluid solver. Continue with the [SRHD/GRHD development review](relativistic-hydrodynamics.md).
