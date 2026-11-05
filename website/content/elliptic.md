# Diffusion, elliptic equations, boundary conditions, and iteration

## Parabolic problems: evolving diffusion

Solve `u_t=νu_xx` on `[0,1]` with zero Dirichlet boundaries and initial data
`sin(πx)`. The reference solution is `u=exp(-νπ²t)sin(πx)`.
`numart.linear.diffusion_1d` returns interior nodes.

Second-order centered differences and the θ method give

\[
(I-\theta\nu\Delta t D_{xx})u^{n+1}
=(I+(1-\theta)\nu\Delta t D_{xx})u^n.
\]

- θ=0: FTCS, requiring `r=νΔt/h²≤1/2`.
- θ=1: backward Euler, first order in time and unconditionally stable for linear diffusion.
- θ=1/2: Crank–Nicolson, second order in time and A-stable for linear diffusion.

The Fourier amplification factor is
`G=[1-4(1-θ)r sin²(ξ/2)]/[1+4θr sin²(ξ/2)]`.
For large r, Crank–Nicolson can have negative G: high-frequency modes alternate
sign while remaining stable. Stability, positivity, monotonicity, and temporal
resolution need separate checks.
[Crank–Nicolson (1947)](https://doi.org/10.1017/S0305004100023197).

`spectral_diffusion` solves a separate periodic problem by multiplying each
Fourier coefficient by `exp(-νk²t)`. Accuracy comparisons with the Dirichlet
finite-difference problem must account for their different boundaries.

## Thomas elimination: from implicit steps to tridiagonal systems

For subdiagonal a, diagonal b, and superdiagonal c, forward elimination uses
`m_i=a_i/b'_{i-1}`, `b'_i=b_i-m_i c_{i-1}`, and
`d'_i=d_i-m_i d'_{i-1}`. Back substitution uses
`x_i=(d'_i-c_i x_{i+1})/b'_i`. Both work and storage are O(N).

`thomas` preserves its inputs and raises an error for a small pivot. It uses
elimination without pivoting, so it is not safe for every tridiagonal matrix.
The diffusion matrices used here are strictly diagonally dominant. The original
1949 Thomas report has not been inspected; the historical citation and the
verification of this modern implementation are separate claims.

## Elliptic problems: the Poisson equation

The sign convention is `-Δu=f`. In 1D, use a tridiagonal system and Thomas
elimination; in 2D, use a five-point stencil with matrix-free conjugate gradients
or multigrid. Default manufactured solutions are `sin(πx)` in 1D and
`sin(πx)sin(πy)` in 2D. Check the linear-system residual separately from the
discretization error relative to the continuous solution.

## Dirichlet, Neumann, and Robin boundaries

Dirichlet specifies `u=g_D`; Neumann specifies the outward normal derivative
`∂u/∂n=g_N`; Robin specifies `αu+β∂u/∂n=g`. The normal derivative is `-u_x` at
the left end and `+u_x` at the right. Outward conductive heat flux is
`-k∂u/∂n`, so both the specified quantity and its sign matter.

Pass `Boundary.dirichlet(value)`, `Boundary.neumann(value)`, or
`Boundary(alpha,beta,value)` to `poisson_boundary_1d`. Robin and Neumann
conditions eliminate ghost points and use half weights at the endpoints.
The time-dependent `diffusion_1d` currently supports zero Dirichlet boundaries.

A pure-Neumann Poisson solution is determined only up to an additive constant.
The divergence theorem requires

\[
\int_\Omega f\,dV=-\int_{\partial\Omega}g_N\,dS.
\]

The implementation checks the discrete compatibility condition corresponding
to trapezoidal quadrature and fixes the constant with a prescribed mean,
defaulting to zero. Some Robin coefficients also lead to a loss of uniqueness.
Periodic Poisson problems similarly need zero-mode compatibility and a mean
constraint, with the endpoints identified.

## Spectral radius of the iteration matrix

For a stationary iteration `x^{k+1}=T x^k+c` solving `Ax=b`, errors satisfy
`e^{k+1}=T e^k`. In finite dimensions, **convergence for every initial error is
equivalent to `ρ(T)<1`**, where `ρ(T)=max |λ_i(T)|`.
This differs from the radius of convergence of a power series,
`R=1/limsup |a_n|^{1/n}`, and from a Newton iteration's basin of convergence.

With `A=D+L+U`, Jacobi has `T=-D^{-1}(L+U)`, Gauss–Seidel has
`T=-(D+L)^{-1}U`, and SOR has
`T=(D+ωL)^{-1}[(1-ω)D-ωU]`. `iteration_matrix` and `spectral_radius` support
small-matrix demonstrations. Nonnormal matrices can exhibit transient error
growth even when `ρ<1`. The system condition number `κ(A)` and iteration
spectral radius `ρ(T)` measure different properties.
[Netlib Templates](https://www.netlib.org/templates/templates.html).

## Red-black Gauss–Seidel and SOR

Color the five-point grid with `(i+j) mod 2`. Updates of one color depend only
on the other color; update red, then black. Set `ω=1` for Gauss–Seidel and
use `0<ω<2` for SOR relaxation. This interval alone does not guarantee
convergence for arbitrary nonsymmetric systems. The implementation targets
symmetric positive-definite Dirichlet Poisson problems.

## Geometric multigrid V-cycle

1. Apply three red-black Gauss–Seidel sweeps on the fine grid.
2. Compute `r_h=f_h-A_h u_h`.
3. Restrict the residual by full weighting.
4. Solve the coarse-grid error equation recursively.
5. Prolongate the correction bilinearly.
6. Apply three more fine-grid sweeps.

Each side has `N=2^k-1` interior nodes. Coarse grids use rediscretized five-point
operators, and the one-unknown coarsest problem is solved directly. Tests check
interpolation, restriction, grid spacing, and boundary consistency. Variable
coefficients, anisotropy, curved grids, AMG, and FAS are outside this edition.
[Fedorenko (1961)](https://www.mathnet.ru/eng/zvmmf8014),
[Brandt (1977)](https://doi.org/10.1090/S0025-5718-1977-0431719-X).
