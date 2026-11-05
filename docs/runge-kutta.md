# Runge–Kutta families: stages, order, stability, and SSP

RK2 and RK4 denote orders, while SSP describes a stability-inheritance
property. These labels answer different questions. The
[Runge–Kutta family notebook](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/runge-kutta)
compares nine explicit methods, their full stage coefficients, nonlinear
predictors, linear stability contours, and measured refinement orders.

## One step, several right-hand-side evaluations

An explicit s-stage Runge–Kutta method for y′=f(t,y) is

\[
Y_i=y_n+h\sum_{j<i}a_{ij}k_j,\qquad
k_i=f(t_n+c_i h,Y_i),\qquad
y_{n+1}=y_n+h\sum_{i=1}^s b_i k_i,
\qquad c_i=\sum_{j<i}a_{ij}.
\]

The Butcher tableau arranges c, A, and b into one coefficient diagram.
The number of stages s counts RHS evaluations in this implementation. Order p
means a global error of O(h^p) under the required smoothness, stability, and
fixed-interval assumptions. Stage predictors Y_i are generally not accurate
solutions at intermediate times. Stage times can go backward: SSPRK(4,3)
evaluates at c=(0,1/2,1,1/2). Time-dependent forcing and boundary data must use
the correct c_i, not just the next chronological fraction of a step.

## RK2 is a family

The two-stage, second-order family can be written

\[
k_1=f(t_n,y_n),\quad
k_2=f(t_n+\alpha h,y_n+\alpha h k_1),\quad
y_{n+1}=y_n+h\left[\left(1-\frac1{2\alpha}\right)k_1+
\frac1{2\alpha}k_2\right].
\]

Heun / explicit trapezoid takes alpha=1; explicit midpoint takes alpha=1/2;
Ralston takes alpha=2/3. Heun is also SSPRK(2,2). For the full nonlinear
methods here, their SSP coefficients are respectively 1, 0, and 1/2, as checked
from the absolute-monotonicity inequalities for the complete tableau.

All three have the same scalar linear stability polynomial

\[
R(z)=1+z+\tfrac12 z^2,\qquad z=h\lambda.
\]

Consequently their trajectories on y′=lambda y coincide in exact arithmetic.
Their nonlinear stages and errors need not coincide. The notebook therefore
also computes y′=−y², y(0)=1, whose exact solution is 1/(1+t). This separates
methods that an oscillator alone cannot distinguish. One benchmark does not
establish a universally best RK2 variant.

## RK3, classical RK4, and SSP stage counts

The implemented third-order group contains Kutta's classical three-stage
method, SSPRK(3,3), and SSPRK(4,3). The first two share
R(z)=1+z+z²/2+z³/6, but their nonlinear SSP coefficients differ: 0 and 1.
SSPRK(4,3) uses a fourth RHS evaluation, has C=2, and adds z⁴/48 to that
polynomial. Four stages do not make it fourth order.

Classical four-stage RK4 uses weights (1/6,1/3,1/3,1/6). Its stability
polynomial adds z⁴/24 instead, and it is fourth order. Its general nonlinear
SSP coefficient is zero. This does not say that every RK4 computation
oscillates; it says the generic forward-Euler SSP inheritance guarantee is
unavailable. The [Numipedia RK4 record](https://ketch.github.io/numipedia/methods/RK44.html)
lists its tableau and scalar stability properties.

For comparison, the notebook implements the five-stage fourth-order
Spiteri–Ruuth SSP method, labeled SSPRK(5,4). Its full coefficients are given
in section 3.1 of the
[Gottlieb–Ketcheson–Shu review](https://www.davidketcheson.info/assets/papers/sspreview.pdf).
The implementation converts that decimal Shu–Osher form to a Butcher tableau;
representing increments relative to y_n avoids drift from rounded affine
weights. It uses the conservative rounded bound C=1.508, rather than claiming
an exact rational coefficient. Order conditions and nonlinear refinement are
checked at the supplied coefficient precision.

For standard explicit RK methods with a positive general nonlinear SSP
coefficient, the order is at most four. A four-stage fourth-order explicit
method cannot have C>0; fourth-order SSP therefore needs additional stages.
SSPRK(5,4) is one example, not a claim that every five-stage fourth-order
method is SSP. See [Spiteri–Ruuth (2002)](https://doi.org/10.1137/S0036142901389025)
and [Gottlieb–Ketcheson–Shu (2009)](https://doi.org/10.1007/s10915-008-9239-z).

## What SSP preserves

Suppose a particular semidiscrete spatial operator L satisfies a convex
stability property under forward Euler for h ≤ h_FE. An SSP method with
coefficient C inherits that property under

\[
h\le C h_{\rm FE}.
\]

The premise might concern total variation, a norm, or an admissible convex
set, provided the actual operator and its stage treatment satisfy the premise.
SSP does not create a TVD spatial discretization, cure an inappropriate
boundary condition, or supply missing positive Euler states. The
[SSP review by Gottlieb–Shu–Tadmor (2001)](https://www.math.umd.edu/~tadmor/pub/linear-stability/Gottlieb-Shu-Tadmor.SIREV-01.pdf)
develops this viewpoint. Compare it with the separate
[slope-limiter](limiters.md) and [positive-reconstruction](advanced-limiters.md)
requirements.

The family labels are **SSPRK(s,p)**: stages first, order second. In this
edition, Heun / SSPRK(2,2) has C=1, SSPRK(3,3) has C=1, SSPRK(4,3) has C=2,
and SSPRK(5,4) has C=1.508 as a rounded bound. The SSP step bound per RHS
evaluation, C/s, is useful context but is not a wall-clock performance ranking.
Memory traffic, storage, spatial accuracy, and other stability constraints
can decide the actual cost.

## Linear stability is a separate picture

For y′=lambda y, one step multiplies y by

\[
R(z)=1+z\,b^T(I-zA)^{-1}{\bf1}.
\]

The region |R(z)|≤1 is the scalar absolute-stability region. Its boundary is
sampled on a 401×401 grid over Re(z)∈[−6,2], Im(z)∈[−4,4]. The curves in the
notebook are approximate contours, not rigorous boundary locations. An
eigenvalue of a normal linear spatial operator suggests where to evaluate R;
eigenvalues alone may miss transient growth for a nonnormal operator.

For the undamped oscillator, RK2 has no nonzero imaginary-axis stability
interval, while SSPRK(3,3) and classical RK4 do. This concerns the scalar
linear problem; it does not contradict Heun's SSP property, because forward
Euler itself has no nonzero stable step on that oscillator.

## Other branches of the time-integration family

Embedded RK pairs, such as Dormand–Prince 5(4), use two orders to estimate
error and select a step. Here those parentheses describe the embedded orders,
unlike the stage/order pair in SSPRK(s,p). No embedded error estimator,
adaptive controller, dense output, or FSAL optimization runs in this edition.

Low-storage RK methods reorganize stage calculations to reduce stored arrays;
they are not automatically SSP. Implicit RK families include midpoint and
Gauss/Radau/SDIRK methods, with nonlinear solves and their own stability
properties. IMEX pairs split explicit and implicit operators. These are
reading context, except for the existing **scalar linear** backward-Euler and
implicit-midpoint demonstrations. The generic `rk_step` below supports the
nine explicit tableaus only. Leapfrog is a multistep recurrence; mechanical
Verlet and the [symplectic maps](symplectic.md) form another distinct branch.

## Reproduction and verification

```python
from numart.runge_kutta import rk_step, nonlinear_trajectory

value, stages = rk_step(lambda t, y: -y*y, 0., 1., 0.5,
                        method="ssprk43", return_stages=True)
t, y = nonlinear_trajectory("ssprk54", steps=40)
```

```bash
python scripts/build_runge_kutta.py
python scripts/sync_web_content.py
```

The JSON records all tableaus, contours, 27 one-step stage cases (h=0.25,0.5,1),
and nine refinement studies (N=10,20,40,80, T=1), plus source hashes. Errors
use the exact nonlinear solution; stages are actual RHS evaluations. Tests
check all order conditions through order four, a nonlinear manufactured
time-dependent equation, complex linear stability factors, full-tableau SSP
inequalities at the stated C, and scalar MUSCL conservation/TVD under the
inherited step restriction. These do not turn the existing Euler/WENO solvers
into selectable-RK or fully positivity-preserving implementations.

![Computed RK family comparison](figures/runge-kutta.png)
