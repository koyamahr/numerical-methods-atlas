# MHD: constrained transport and divergence cleaning

## Problem and units

The model is planar 2D ideal MHD with `γ=5/3`, `μ0=1`, and `vz=Bz=0` on the
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
Reference-code comparisons, grid refinement, Brio–Wu, field-loop advection,
and Alfvén waves remain future work. The low-resolution, first-order OT figures
are introductory demonstrations of magnetic-constraint handling.
