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


## Roe's Property U {#roes-property-u}

[Roe's 1981 paper, author-uploaded full text, pp. 359–360](https://www.researchgate.net/publication/222453065_Approximate_Riemann_Solvers_Parameter_Vector_and_Difference_Schemes)
uses four conditions: (i) a linear mapping from conserved-state space to
flux space for each fixed state pair; (ii) the coincident-state limit equals
the physical Jacobian; (iii) the matrix maps the state jump exactly onto
the flux jump; (iv) its eigenvectors are linearly independent. The two-state
matrix need not depend linearly on its arguments. For physical ideal-gas Euler
states the construction below also has real acoustic/contact speeds.

Here is the algebra implemented and independently checked in this atlas.
For U=(ρ,ρu,E), H=(E+p)/ρ, set z=√ρ(1,u,H). Then

\[
 U(z)=\begin{pmatrix}z_1^2\\z_1z_2\\
 (z_1z_3+(\gamma-1)z_2^2/2)/\gamma\end{pmatrix},\qquad
 F(z)=\begin{pmatrix}z_1z_2\\
 ((\gamma+1)z_2^2/2+(\gamma-1)z_1z_3)/\gamma\\z_2z_3\end{pmatrix}.
\]

Both maps are quadratic. Their midpoint Jacobians B=∂U/∂z and C=∂F/∂z
therefore satisfy ΔU=B(z̄)Δz and ΔF=C(z̄)Δz exactly. Consequently
Ã=C(z̄)B(z̄)⁻¹ has the jump property. Ratios of z̄ give

\[
 \widetilde u=\frac{\sqrt{\rho_L}u_L+\sqrt{\rho_R}u_R}{\sqrt{\rho_L}+\sqrt{\rho_R}},\quad
 \widetilde H=\frac{\sqrt{\rho_L}H_L+\sqrt{\rho_R}H_R}{\sqrt{\rho_L}+\sqrt{\rho_R}},\quad
 \widetilde c^2=(\gamma-1)(\widetilde H-\widetilde u^2/2).
\]

At equal states, the chain rule gives CB⁻¹=∂F/∂U. The independently constructed
eigenbasis has speeds ũ−c̃,ũ,ũ+c̃. Since c̃>0, its three eigenvectors span
the state space. We check the parameter-vector matrix against this eigenbasis,
the analytic Jacobian, and 2000 deterministic physical state pairs.

If ΔF=sΔU for a single nonzero Rankine–Hugoniot jump, then ÃΔU=sΔU:
the jump lies in the speed-s eigenspace. The unmodified Roe flux consequently
recognizes isolated contact/shock jumps. This does not make every reconstructed,
time-discretized shock calculation exact. Smoothing |λ| changes the flux
without changing the matrix identity, and can smear a stationary shock.

An expansion discontinuity can also satisfy the jump relation. Our reversed
stationary normal-shock pair passes Property U but the raw Roe flux differs
from the entropy Riemann reference. This is a numerical counterexample to
confusing the jump property with entropy selection. The entropy fix is an
additional design choice; neither gives a multidimensional carbuncle guarantee.

![Roe flux-jump residuals](figures/shock-methods/roe-property-u.png)

`python scripts/build_shock_robustness.py` saves the matrix checks, moving and
stationary shocks, a contact and the expansion counterexample in the
[diagnostic manifest](figures/shock-methods/robustness.json).
