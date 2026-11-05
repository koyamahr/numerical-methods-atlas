# A-stability, L-stability and error norms

A-stability and L-stability describe the response of a time integrator to
linear decay modes. L1, L2 and L∞ instead describe the size and distribution
of an error. They answer different questions. A method can be stable with a
large error, and a small algebraic residual need not imply a small PDE error.

## A-stability concerns the whole left half-plane

Apply a one-step method to y′=λy, with z=λΔt. Its stability function satisfies

\[
y_{n+1}=R(z)y_n,\qquad
\mathcal S=\{z\in\mathbb C:|R(z)|\leq1\}.
\]

The method is **A-stable** if its absolute-stability region contains the entire
closed left half-plane. In particular, R must have no pole there. Thus a
scalar mode with Re λ≤0 does not grow for any positive step size in this test.
[Dahlquist (1963)](https://doi.org/10.1007/BF01963532) is a foundational
A-stability reference in the linear-multistep setting. The one-step notation
here is used to make the comparison transparent.

Forward Euler, R(z)=1+z, is stable on the negative real axis only for
−2≤z≤0. No consistent explicit RK method is A-stable: its nonconstant
stability polynomial is unbounded along the negative real axis.
Being implicit alone does not guarantee A-stability.

## L-stability also damps infinitely stiff modes

An **L-stable** one-step method is A-stable and satisfies

\[
\lim_{|z|\to\infty,\;\operatorname{Re}z<0}R(z)=0.
\]

This extra property damps modes that are much faster than the chosen step.
Backward Euler has R(z)=1/(1−z), so it is both A-stable and L-stable.
Crank–Nicolson / the trapezoidal rule has

\[
R_{CN}(z)=\frac{1+z/2}{1-z/2},\qquad
\lim_{z\to-\infty}R_{CN}(z)=-1.
\]

It is A-stable but not L-stable: very stiff negative-real modes alternate
sign and decay only slowly. Implicit midpoint has the same scalar linear
R(z), although its nonlinear update is different from the trapezoidal rule.
For z=−1000, backward Euler gives about 0.001 in one step, while CN gives
about −0.996; the exact factor is exp(−1000).

For the [implemented SDIRK2](stiff-integration.md),

\[
\gamma=1-1/\sqrt2,\qquad
R(z)=\frac{1+(1-2\gamma)z}{(1-\gamma z)^2}.
\]

Its poles are in the right half-plane, it is A-stable and its large-z limit
is zero. This is the L-stable two-stage family associated with
[Alexander (1977)](https://doi.org/10.1137/0714068).
BDF2 is a two-step method: analyze its characteristic roots and parasitic
mode, rather than assigning it an arbitrary single-valued R(z).

These are linear absolute-stability statements. Accuracy, nonlinear
contractivity, SSP/TVD inheritance, positivity and boundary stability require
their own checks. Eigenvalues alone can also miss transient growth of
nonnormal operators. An A-stable time step cannot repair an inconsistent
spatial discretization, and L-stability cannot make an underresolved transient
accurate.

## Continuous L1, L2 and L∞ errors

For scalar error e(x)=u_h(x)−u_ref(x) on a domain Ω,

\[
\|e\|_{L^1}=\int_\Omega |e|\,dV,\qquad
\|e\|_{L^2}=\left(\int_\Omega |e|^2\,dV\right)^{1/2},\qquad
\|e\|_{L^\infty}=\operatorname*{ess\,sup}_{x\in\Omega}|e(x)|.
\]

L1 measures integrated absolute error. L2 emphasizes larger deviations more
strongly. L∞ measures the worst error apart from measure-zero sets. For a
continuous error on a compact domain, the essential supremum equals the maximum.
For discontinuous solutions, the value assigned exactly at a jump does not
change the continuous norm.

For a domain with volume V, mean absolute error is L1/V and RMS error is
L2/√V. These normalized quantities have the same physical units as u;
unnormalized integral norms also contain powers of length. State the convention
before comparing domains of different size.

## Discrete weights and the reference representation

For finite-volume error e_i between a numerical cell mean and a reference cell
mean, with positive cell volumes V_i,

\[
E_1=\sum_iV_i|e_i|,\qquad
E_2=\left(\sum_iV_i|e_i|^2\right)^{1/2},\qquad
E_\infty=\max_i|e_i|.
\]

On a uniform grid, V_i=h^d. On the unit interval, these become mean absolute
error, RMS error and maximum cell-mean error. On a nonuniform mesh, an unweighted
arithmetic mean generally gives the wrong spatial weighting. For e=(1,3) and
cell volumes (0.75,0.25), E1=1.5, E2=√3 and E∞=3; unweighted means disagree.

The Euclidean vector norm `np.linalg.norm(e)` omits the h^(d/2) factor of a
physical discrete L2 norm. Comparing that raw norm across meshes can therefore
change an apparent convergence exponent. Relative error E_p/||u_ref||_p needs
a stated reference norm; when the denominator is zero, it is undefined. Any
regularization must be explicitly reported.

A reference at cell centers is not an exact cell-average reference. DG and FEM
need reconstruction and quadrature **inside elements**; a coefficient-vector
norm is not automatically a function L2 norm. Likewise, a maximum over sample
points is a sampled L∞ diagnostic, not necessarily the exact supremum of a
high-order reconstructed field. Vector components with different units should
be reported separately or nondimensionalized with stated scales.

## Convergence, shocks and algebraic residuals

For matched runs at the same physical time and error convention, the observed
order is

\[
p_{obs}=\frac{\log(E_{coarse}/E_{fine})}{\log(h_{coarse}/h_{fine})}.
\]

Temporal error, reference error, quadrature error, roundoff and incomplete
iterative convergence can mask spatial order. Refine time separately, or state
how Δt scales with h. Adaptive ODE tolerance is a local, component-scaled error
control; it is not a global spatial L2 error bound.

Different norms can behave differently near shocks. For example, an O(1)
error supported on width O(h) has L1=O(h), L2=O(√h) and L∞=O(1). This simple
scaling is not a universal convergence-rate claim for a shock solver. A useful
L1 refinement result need not imply maximum-norm convergence of a shifted jump.

For Ax=b, the residual is r=b−Ax. The solution error satisfies
x_num−x_exact=−A^(−1)r, so conditioning matters. An algebraic residual compares
against the discrete equation; discretization error compares that equation's
solution against the continuous problem. See [sparse/nonlinear solvers](sparse-nonlinear.md)
and the [Lax–Richtmyer discussion](stability.md).

## Where the atlas reports each quantity

- [The equation gallery](equation-gallery.md) reports L1/MAE, L2/RMS and
  L∞ over its stored unit-interval profiles. Its labels retain the distinction
  between exact cell means, point-sampled Euler references and absent references.
- [The browser stability laboratory](experiments.md) has a point-sampled
  L1/MAE diagnostic and amplification factors; it does not thereby measure
  a reconstructed finite-volume function norm.
- [P1 FEM](fem.md) integrates L2 and H1 seminorm errors inside triangles.
- [Periodic MAC flow](incompressible.md) reports a combined velocity RMS error
  and maximum absolute discrete divergence. These are different diagnostics.
- [Stiff integration](stiff-integration.md) reports maximum error over accepted
  time nodes, separate from nonlinear stage residuals and local step estimates.

Original exhibits keep their documented conventions; this chapter does not
retroactively relabel point samples as cell averages or certify a missing
maximum-norm calculation.
