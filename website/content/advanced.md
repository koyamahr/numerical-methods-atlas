# Preconditioning, dual time stepping, and residual distribution

## Condition numbers and PDE preconditioning

For `Ax=b`, the 2-norm condition number is `κ₂(A)=σmax/σmin`. It measures
sensitivity to perturbations rather than the convergence rate of a particular
iteration. Left preconditioning gives `P^{-1}Ax=P^{-1}b`; right preconditioning
gives `AP^{-1}y=b, x=P^{-1}y`. For symmetric positive-definite systems,
`P^{-1/2}AP^{-1/2}` supports symmetry-preserving comparisons.

`conditioning_example` constructs `A=S B S`, where B is a 1D Poisson matrix
and S is diagonal scaling. It demonstrates the change in condition number
under symmetric Jacobi scaling. It does not implement Turkel's low-Mach flow
preconditioning matrix.

Compressible PDEs pose a separate preconditioning problem when low-Mach
convective and acoustic characteristic speeds differ greatly. A pseudo-time
system such as `Γ(U) ∂U/∂τ + R(U)=0` modifies characteristic speeds,
convergence, and numerical dissipation. Deriving Γ, transforming variables,
choosing Mach-dependent coefficients, and maintaining boundary consistency
require additional verification. Replacing the physical time derivative
indiscriminately changes the time-dependent solution.
[Turkel (1987)](https://doi.org/10.1016/0021-9991(87)90084-2).

## Dual time stepping

Applying BDF2 in physical time to `dU/dt+R(U)=0` gives

\[
\frac{3U^{n+1}-4U^n+U^{n-1}}{2\Delta t}+R(U^{n+1})=0.
\]

At each physical step, evolve the pseudo-time equation for Q,

\[
\frac{dQ}{d\tau}+\frac{3Q-4U^n+U^{n-1}}{2\Delta t}+R(Q)=0,
\]

to a steady state. Backward Euler starts the first step. Physical-time accuracy
depends on Δt, spatial error, and incomplete inner convergence. A large physical
CFL alone does not establish accurate time evolution.
[Jameson (1991)](https://doi.org/10.2514/6.1991-1596).

`dual_time_advection` is a minimal periodic 1D example: implicit upwind
advection with BDF1/BDF2, solved by a Jacobi pseudo-time iteration. The inner
residual threshold is `tol*max(1,||b||∞)`, with default `tol=1e-10`. Failure to
converge within the iteration limit raises an error. Tests compare against an
independent dense solve of the BDF2 discrete equations. This is a reduced model
rather than Jameson's complete compressible-flow multigrid algorithm.

## Residual distribution schemes

Distribute an element residual `Φ_K=∫K ∇·F(U) dV` to its nodes while preserving
`Σ_{i∈K} Φ_i^K=Φ_K`. This conservation condition connects continuous finite
elements with upwind ideas.
[Abgrall (2006), author-hosted review](https://www.math.u-bordeaux.fr/~rabgrall/mes_papiers/caf_2006_35.pdf).

`rd_residual` is a minimal 1D P1 scalar-advection example. It assigns all of
`Φ_K=a(u_{i+1}-u_i)` to the downstream node and divides by lumped mass h.
Tests establish equivalence to first-order upwind differences in this case.
2D triangular N/LDA schemes, nonlinear blending, time-consistent mass matrices,
and Euler systems remain unimplemented.

## Roe, entropy fixes, Einfeldt, and rotated solvers

Roe uses a linearization satisfying `F_R-F_L=Ã(U_R-U_L)` and its eigensystem.
This edition forms sqrt(ρ)-weighted u and H, with
`ã²=(γ-1)(H̃-ũ²/2)`, and adds dissipation through wave strengths and
eigenvectors.
[Roe (1981)](https://doi.org/10.1016/0021-9991(81)90128-5).

The entropy fix replaces the absolute acoustic eigenvalue below δ with
`(λ²+δ²)/(2δ)`. HLLE is a separate flux using Einfeldt-type left/right wave
speeds for strong low-density expansions. Roe entropy correction, HLLE
positivity properties, and carbuncle treatments address different problems.
[Einfeldt (1988)](https://doi.org/10.1137/0725021),
[Einfeldt et al. (1991)](https://doi.org/10.1016/0021-9991(91)90211-3).

Rotated-hybrid Riemann solvers combine fluxes using directions beyond the face
normal to balance shock robustness and shear-layer resolution. A coordinate
rotation alone does not reproduce this construction. This edition supplies
the literature context; 2D Euler geometry, direction selection, and carbuncle
tests are next implementation steps.
[Nishikawa–Kitamura (2008)](https://doi.org/10.1016/j.jcp.2007.11.003).
