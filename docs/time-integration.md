# Time integration and leapfrog

Spatial reconstruction and time integration are independent choices. After spatial discretization, a PDE becomes an ODE system dU/dt = L(U). Accuracy, stability, monotonicity, dissipation, and cost then depend on both parts. The [time integration notebook](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/time-integration) isolates the temporal choice using y′ = i y, y(0) = 1.

## Seven methods on one oscillator

The exact solution exp(i t) follows the unit circle. Forward Euler and backward Euler are first order: the former grows on this undamped oscillator, while the latter damps it. Heun is second order; SSPRK3 and classical RK4 have orders three and four. Implicit midpoint is second order and preserves the amplitude of this linear oscillator. Its phase still has error.

For y′ = lambda y, define z = lambda delta t. One-step amplification factors include

\[
R_{\rm FE}=1+z,\quad R_{\rm BE}=\frac1{1-z},\quad
R_{\rm midpoint}=\frac{1+z/2}{1-z/2}.
\]

The RK factors are the exponential Taylor polynomial through degree two, three, or four for Heun, SSPRK3, or RK4 on this scalar linear equation. This coincidence does not make the nonlinear RK stages identical. SSPRK3’s strong-stability property also depends on a forward-Euler bound for the spatial operator; it is not unconditional stability.

## Leapfrog needs two roots

The centered, two-step first-order-system recurrence is

\[
y^{n+1}=y^{n-1}+2z y^n,\qquad
\xi_\pm=z\pm\sqrt{1+z^2}.
\]

The root tending to +1 as z tends to zero carries the physical mode; the root tending to −1 carries a computational mode alternating between steps. Both roots and their multiplicities matter. For z = i sigma, distinct roots have unit modulus when |sigma| < 1. At |sigma| = 1 the repeated root can give linearly growing solutions; do not include that endpoint in a general boundedness claim. Above it, one root grows geometrically.

A starting value is required in addition to y(0). This implementation takes one RK4 step, optionally adding a real perturbation epsilon to y(1). At lambda = 0 that perturbation gives even samples equal to 1 and odd samples equal to 1+epsilon: a direct computational-mode demonstration. For the notebook’s oscillator it also perturbs the physical mode.

Time filters such as the Robert–Asselin family modify this behavior, with their own damping and accuracy tradeoffs; see [Williams (2009)](https://doi.org/10.1175/2009MWR2724.1). No filter is applied in this edition.

## Particle leapfrog is a different formulation

A staggered kick–drift scheme for position and velocity, or velocity Verlet for a second-order mechanical system, is often also called leapfrog. Its variables live at different temporal locations and its symplectic interpretation uses that structure. The scalar recurrence above is not a demonstration of a complete SPH particle integrator or a proof of long-time energy conservation for general mechanics.

## Reproduce and read the notebook

```python
from numart.time_integration import linear_trajectory, leapfrog_roots
t, y = linear_trajectory(rate=1j, dt=0.1, steps=200, method='leapfrog')
print(leapfrog_roots(0.1j))
```

The browser selects from Python-computed trajectories with fixed final time 20, seven methods, seven step sizes, and three leapfrog starting perturbations. Axes expand for unstable samples. A matching time interval is not an equal-cost comparison: implicit solves and RK stages differ. Tests measure temporal refinement orders and check the leapfrog roots, alternating mode, and midpoint amplitude.

Continue with [the spatial stability laboratory](experiments.md), [SPH](particles-sph.md), and [ALE](ale.md).
