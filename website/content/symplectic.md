# Symplectic integration: a canonical map, not an exact energy promise

A symplectic integrator advances a Hamiltonian system while preserving its canonical two-form. This is the map property behind the good long-time behavior of many orbital and particle integrators. It does **not** generally preserve the original Hamiltonian exactly. The [Hamiltonian map notebook](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/hamiltonian) separates those two questions with computed examples.

![Fixed-step energy and phase-space comparisons for harmonic and quartic oscillators.](figures/hamiltonian.png)

## What the map preserves

For state z = (q,p), Hamilton’s equations and the symplectic condition are

\[
\dot z=J\nabla H(z),\qquad J=\begin{pmatrix}0&I\\-I&0\end{pmatrix},
\qquad D\Phi_h(z)^T J D\Phi_h(z)=J.
\]

The last identity says that each numerical step is a canonical transformation. For one degree of freedom it is equivalent to det(D Phi) = 1, preserving oriented phase-plane area. In higher dimensions, preservation of total volume alone is weaker than symplecticity.

Three separate properties should be tested: preservation of the two-form, preservation of H, and time symmetry Phi_(−h) = Phi_h^(−1). Symplectic Euler already illustrates the distinction: it is symplectic but is neither exactly energy preserving nor time symmetric in general.

## Split the Hamiltonian, compose exact subflows

For a unit-mass separable system H(q,p) = p²/2 + V(q), the two subflows are a drift and a kick:

\[
D_h(q,p)=(q+hp,p),\qquad K_h(q,p)=(q,p-h\nabla V(q)).
\]

Each is symplectic; compositions remain symplectic. The notebook includes kick–drift symplectic Euler, and the symmetric second-order Störmer–Verlet update

\[
p_{n+1/2}=p_n-\frac h2\nabla V(q_n),\quad
q_{n+1}=q_n+h p_{n+1/2},\quad
p_{n+1}=p_{n+1/2}-\frac h2\nabla V(q_{n+1}).
\]

This is the mechanical Leapfrog/velocity-Verlet formulation. It differs from the two-step scalar recurrence in the [earlier time-integration notebook](time-integration.md).

## Fourth order by composition

Writing S2(h) for a Verlet step, one fourth-order composition is

\[
S_4(h)=S_2(a h)\,S_2(b h)\,S_2(a h),\qquad
a=\frac1{2-2^{1/3}},\quad b=-\frac{2^{1/3}}{2-2^{1/3}}.
\]

[Yoshida (1990)](https://doi.org/10.1016/0375-9601(90)90092-3) develops higher-order symplectic compositions. Here b is negative: an internal substep goes backward in time. The construction is suitable for the smooth conservative examples used here; simply applying it to irreversible diffusion, shocks, or collision handling is not justified. Higher order also does not establish unconditional stability or an equal-cost advantage.

## Energy and a modified Hamiltonian

Backward error analysis describes a nearby, generally formal modified Hamiltonian. Under smoothness, bounded-trajectory, small-step, and related hypotheses, this explains small long-time energy errors. It does not assert an exact invariant of the original H for every orbit or step size. [Hairer, Lubich, and Wanner (2003)](https://doi.org/10.1017/S0962492902000144) develop this geometric viewpoint and its assumptions.

For the special oscillator H = (p²+q²)/2, kick–drift–kick Verlet preserves the quadratic invariant

\[
I_h=\frac12p^2+\frac12\left(1-\frac{h^2}{4}\right)q^2
\]

up to roundoff. H itself oscillates. This invariant is not a claim that its unscaled Hamiltonian flow is exactly the numerical time-h map. The oscillator map is bounded for |h| < 2; above that limit it can be symplectic **and unstable**.

## Implicit midpoint and RK4 as comparisons

Implicit midpoint is symplectic and time symmetric when its endpoint equation is solved accurately. It preserves the quadratic oscillator H to roundoff here. It need not exactly conserve a nonquadratic H. Classical RK4 is fourth order but is generally neither symplectic nor time symmetric. Good short-time accuracy alone does not certify the map’s geometry.

The second test problem is H = p²/2 + q²/2 + q⁴/4, a smooth nonlinear oscillator. It makes midpoint’s special quadratic-energy conservation visibly distinguishable from a general claim.

## Reproducible notebook and checks

```python
from numart.hamiltonian import trajectory, energy, canonical_step, J
t, z = trajectory(h=0.2, steps=1000, method='yoshida4', system='quartic')
print(max(abs((energy(z, 'quartic')-energy(z[0], 'quartic'))/energy(z[0], 'quartic'))))
_, M = canonical_step([0.7, 0.4], 0.2, 'yoshida4', 'quartic', True)
print(M.T @ J @ M - J)
```

The [computed dataset and source manifest](figures/hamiltonian.json) supplies 30 Python trajectories: five methods, two Hamiltonians, and h = 0.1, 0.2, or 0.4, all to T = 200 from (q,p) = (1,0.2). Plotted trajectories contain at most 1001 samples; maximum energy errors use **every integration step**. The phase-patch view applies one step to a square centered at (0.7,0.4). Its sampled polygon boundary is an illustration; the displayed local defect uses an analytic map Jacobian at the patch center.

Tests check refinement orders against the exact oscillator, analytic Jacobians against independent finite differences, the canonical identity on both potentials, time reversal for symmetric methods, the Verlet quadratic invariant, and the difference between quadratic and nonquadratic midpoint energy. The gallery and notebook are educational fixed-step examples, not orbit-accuracy or timing rankings.

## Connecting to particle gravity

A fixed step and a force that is the gradient of a consistent position-dependent potential support the splitting argument. A generic approximate Tree force, changing opening decisions, ad hoc mesh interpolation, or state-dependent step selection does not automatically retain that proof. Force approximation and time integration need joint tests. Continue with [particle gravity and Poisson solvers](particle-gravity.md) and [gravity boundary kernels](gravity-boundaries.md).
