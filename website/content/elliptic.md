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

For a teaching path, start with [Briggs–Henson–McCormick, *A Multigrid Tutorial*, second edition (2000)](https://doi.org/10.1137/1.9780898719505), then use [Trottenberg–Oosterlee–Schüller, *Multigrid*](https://shop.elsevier.com/books/multigrid/trottenberg/978-0-08-047956-9) for local Fourier analysis, algorithm design and advanced applications. The [textbook guide](#/read/textbooks?section=multigrid) explains where each book fits. Their broader scope includes methods beyond the geometric V-cycle implemented here.

## Particle and disk gravity

The new [particle-gravity chapter](particle-gravity.md) connects PM, P³M, Tree, multipoles, and multigrid. [Gravity boundary kernels](gravity-boundaries.md) adds Hockney–Eastwood isolated convolution and Koyama–Ostriker slab Fourier kernels. The existing multigrid example retains its 2D zero-Dirichlet operator; it is not a 3D open-boundary gravity solver.

## Further routes to diffusion and elliptic problems

See [continuous P1 FEM](fem.md) for weak-form assembly,
[GMRES/ILU and nonlinear solves](sparse-nonlinear.md) for nonsymmetric systems,
and [Nishikawa hyperbolic diffusion](hyperbolic-diffusion.md) for auxiliary-gradient
pseudo-time iteration. The [equation gallery](equation-gallery.md) separately
shows physical-time heat diffusion.

For definitions and comparisons of **A-stability, L-stability and L1/L2/L∞ error norms**,
see the [shared accuracy and stability guide](accuracy-stability.md).


## Same-system Poisson comparison

[Open the Poisson solver notebook](#/poisson-comparison). All 2D methods solve
one constant-coefficient five-point SPD system on the unit square with zero
Dirichlet boundaries. N=31,63,127 counts **interior nodes per side**, hence
N² unknowns. Every iterative method starts from zero. The common stopping
criterion uses the explicitly recomputed true residual, including for CG:

\[
 (A_hu)_{ij}=\frac{4u_{ij}-u_{i-1,j}-u_{i+1,j}-u_{i,j-1}-u_{i,j+1}}{h^2},\quad
 h=\frac1{N+1},\qquad
 \frac{\|f-A_hu\|_2}{\|f\|_2}\le 10^{-8}.
\]

Forcing choices are a broad smooth manufactured field and two localized
opposite-sign sources. The manufactured solution is
u=x(1−x)e^(2x)y(1−y)e^(−1.5y), with f=−Δu differentiated analytically.
The localized forcing is
100exp(−[(x−0.28)²+(y−0.35)²]/0.006)
−60exp(−[(x−0.70)²+(y−0.65)²]/0.012), with no continuous exact solution supplied.
Algebraic error is nodal RMS against the FFT/DST discrete solution;
continuous nodal RMS for the manufactured field measures discretization error.
Neither is a continuous integral L2 norm. Tight residuals do not remove
second-order discretization error.

The separate N=31 single-sine diagnostic uses u=sin(πx)sin(πy) and f=2π²u.
It is one eigenvector of this discrete matrix: exact-arithmetic CG requires
one iteration from zero. It is therefore unsuitable as the sole general
solver benchmark. Broad forcing avoids this shortcut.

The compared configurations are Jacobi, weighted Jacobi (ω=2/3), red-black
Gauss–Seidel, red-black SOR, unpreconditioned CG, the existing geometric
multigrid V-cycle, DST+Thomas and FFT/DST direct elimination. SOR uses
ω=2/[1+sin(π/(N+1))] for this model and ordering. This is not a generally
optimal setting for arbitrary meshes/operators. A sweep, CG iteration and
V-cycle are different work units. Multigrid has three pre/post RBGS sweeps
at every level and additional coarse-grid work. Its cycle count is not a
fine-grid sweep count. [Netlib's SOR discussion](https://www.netlib.org/linalg/html_templates/node15.html)
provides the method context.

The FFT route uses an orthonormal DST-I computed with an odd extension and
NumPy FFT, following the [DST-I definition](https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.dst.html).
The 1D eigenvalues of the difference operator are
λk=4h⁻²sin²[kπ/(2(N+1))]; in 2D divide by λk+λl.
This solves the **same discrete operator**, rather than substituting continuum
wave numbers k². Zero Dirichlet boundaries are not periodic boundaries.
No SciPy dependency is required by the implementation.

Plain Thomas solves 1D tridiagonal systems. The 2D separable direct route
transforms y, solves N shifted tridiagonal x systems with Thomas, then applies
the inverse transform. It is labeled DST+Thomas, not a generic 2D Thomas
solver. Both FFT/DST routes rely on constant coefficients, a rectangular
uniform mesh and separable boundary conditions. A separate 1D table compares
plain Thomas with FFT/DST at N=63,255,1023 for u=x(1−x)e^(2x).

### Timing protocol and downloadable evidence

Each configuration is run three times after a small N=7 code-path warmup.
The reported median trial supplies its own convergence history. Wall time
includes solver setup, allocations, per-unit true-residual checks and logging;
it excludes imports, problem/reference generation, file I/O and plotting.
No cached factorization/eigenvalues are reused between trials. The 1D timings
also include their final residual check. Hardware/software metadata and all
three times are saved. Python loops and compiled NumPy kernels have different
costs; these measurements rank these diagnostic implementations on one host,
not algorithms independently of implementation or hardware.

Direct solvers have only a completed-solve endpoint marker. The chart samples
long histories and floors displayed residuals at 10⁻¹⁴; full values are in the
table and download. The NPZ retains every selected-trial residual/timestamp
and final fields. CG's recursive residual chooses directions, but its true
residual decides convergence. Residual histories need not be monotone.

![Poisson convergence and cost overview](figures/poisson-comparison/overview.png)

Reproduce with `python scripts/build_poisson_comparison.py`. Download
[settings, sampled histories, timings and source hashes](figures/poisson-comparison/comparison.json)
and [fields and full selected histories](figures/poisson-comparison/fields-and-histories.npz).
Tests independently check DST against a dense sine matrix, direct solves
against dense linear systems, common true residuals, all method solutions,
zero forcing and manufactured second-order refinement. Variable coefficients,
anisotropy, irregular meshes, periodic/pure-Neumann nullspaces and parallel
scaling require separate comparisons.
