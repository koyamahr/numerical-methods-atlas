# Differences, CFL, von Neumann analysis, and Lax

Try the [interactive stability laboratory](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/experiments) and read the [experiment guide](experiments.md) to connect the formulas below with live browser calculations.

## Choose space and time discretizations separately

Forward, backward, and centered spatial differences are

\[
D_+u_j=\frac{u_{j+1}-u_j}{h},\qquad
D_-u_j=\frac{u_j-u_{j-1}}h,\qquad
D_0u_j=\frac{u_{j+1}-u_{j-1}}{2h}.
\]

For smooth functions, the first two are first-order accurate and the centered
stencil is second order. Compare them with `numart.advection.finite_difference`.
For linear advection `u_t+a u_x=0`, upwinding follows information propagation:
use a backward difference for `a>0` and a forward difference for `a<0`.
A forward difference is therefore not synonymous with an upwind difference.

Forward Euler in time gives `u^{n+1}=u^n+Δt L_h u^n`; backward Euler gives
`u^{n+1}=u^n+Δt L_h u^{n+1}` and requires a system solve. A backward spatial
stencil alone does not make a method implicit.

## CFL: can the stencil reach the information it needs?

For constant-coefficient periodic advection with an explicit nearest-neighbor
stencil, domain-of-dependence reasoning requires `|a|Δt/h ≤ 1`. The constant
changes with the stencil, Runge–Kutta method, DG degree, and dimension.
Explicit diffusion introduces a `Δt=O(h²)` restriction. A CFL condition is
generally necessary rather than sufficient for stability.
[Courant–Friedrichs–Lewy (1928)](https://doi.org/10.1007/BF01448839).

Forward-time, centered-space (FTCS) advection is a counterexample. Substituting
a Fourier mode `u_j^n=G^n e^{ijθ}` gives

\[
G=1-i C\sin θ,\quad |G|^2=1+C^2\sin^2 θ,
\qquad C=a\Delta t/h.
\]

Some modes grow even when `|C|<1`. The scheme is unstable under ordinary
fixed-CFL grid refinement.

## Lax–Friedrichs and Lax–Wendroff

The classical Lax–Friedrichs scheme is

\[
u_j^{n+1}=\tfrac12(u_{j+1}^n+u_{j-1}^n)
-\tfrac C2(u_{j+1}^n-u_{j-1}^n),\qquad
G=\cos θ-iC\sin θ.
\]

Since `|G|²=1-(1-C²)sin²θ`, periodic linear advection is stable for `|C|≤1`.
Classical LF uses the numerical-viscosity coefficient `h/Δt`. Rusanov uses a
local maximum wave speed; WENO here uses global LF flux splitting. These are
different discrete constructions.
[Lax (1954)](https://doi.org/10.1002/cpa.3160070112).

Lax–Wendroff is

\[
u_j^{n+1}=u_j^n-\tfrac C2(u_{j+1}^n-u_{j-1}^n)
+\tfrac{C^2}{2}(u_{j+1}^n-2u_j^n+u_{j-1}^n),
\]
\[
G=1-iC\sin θ+C^2(\cos θ-1),\quad
|G|^2=1-4C^2(1-C^2)\sin^4(θ/2).
\]

Its stability condition for this problem is also `|C|≤1`. Second-order accuracy
does not itself suppress oscillations near discontinuities.
[Lax–Wendroff (1960)](https://doi.org/10.1002/cpa.3160130205).

Tests compare the analytical amplification factors from `amplification` with
actual mode evolution from `difference_step`. The gallery seeds a small
Nyquist perturbation and compares `C=0.8` with `C=1.1`.

![Fourier amplification factors and computed advection](figures/stability.png)

## The Lax–Richtmyer equivalence theorem

Consider a **well-posed linear initial-value problem** in an appropriate Banach
space and a **consistent linear difference approximation**. When stability
means uniform boundedness of the discrete evolution operators over a fixed
finite time interval, stability is equivalent to convergence.
[Lax–Richtmyer (1956), original paper](https://math.berkeley.edu/~wilken/228B.S07/LaxRichtmyer.pdf).

Writing the error as `e^{n+1}=S_h e^n+Δt τ^n`, the bound `||S_h^m||≤M_T` gives
`||e^n||≤M_T||e^0||+M_T T max||τ^k||`. Consistency makes the truncation-error
term tend to zero, providing the basic stability-to-convergence argument.
The converse requires a uniform-boundedness argument.

The theorem does not directly certify nonlinear Euler, WENO, shocks, or
arbitrary boundary treatments. The Fourier criterion `|G|≤1` used here applies
to periodic, constant-coefficient scalar problems. Boundaries, variable
coefficients, nonnormal matrices, and multistep schemes need additional analysis.

## Time steps in the first edition

- Euler and barotropic systems: `Δt=C h/max(|u|+c)`, with default `C=0.3`.
- DG: `Δt=C h/((2p+1)|a|)`, with default `C=0.2`.
- 2D MHD: `Δt=C/[max(s_x)/h+max(s_y)/h]`, with default `C=0.3`.

These conservative choices are checked on selected examples. They are not
rigorous nonlinear stability limits for every initial condition.

For definitions and comparisons of **A-stability, L-stability and L1/L2/L∞ error norms**,
see the [shared accuracy and stability guide](accuracy-stability.md).
