# CIP: carry the value and the gradient

The original cubic-interpolated pseudo-particle (CIP) idea stores a field and
its spatial derivative, then reconstructs an upwind cubic profile. The broader
family is also called constrained interpolation profile. The
[CIP notebook](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/cip)
implements the original polynomial construction for constant-speed periodic
scalar advection. It compares value-only linear interpolation with CIP and
checks diffusion, gradient transport, oscillations, refinement, and conservation.

Historical references are [Takewaki–Nishiguchi–Yabe (1985)](https://doi.org/10.1016/0021-9991(85)90085-3)
and [Yabe–Aoki (1991)](https://doi.org/10.1016/0010-4655(91)90071-R).
The accessible [Saito–Obase–Abe-Ouchi (2020) paper](https://doi.org/10.5194/gmd-13-5875-2020)
describes CIP-family value/gradient evolution and a rational variant; its
ice-sheet application and RCIP algorithm are separate from this polynomial example.

## Characteristics and an additional unknown

For constant velocity a,

\[
f_t+a f_x=0,\qquad g=f_x,\qquad g_t+a g_x=0.
\]

At a receiving point x_i, trace backward to x_d=x_i−a dt. Interpolate both
f and g from the old upwind interval at that departure point. The evolved g
is an independent state variable; it is not replaced after each step by a
finite difference of the updated f. For N nodes, CIP therefore stores 2N
scalar unknowns, while the linear comparison stores N.

For variable velocity the gradient equation instead includes stretching:

\[
g_t+a g_x=-a_xg.
\]

Source terms, velocity variation, and compressibility require additional
updates and characteristic treatment. A transported tracer f_t+a f_x=0 and
a conserved density f_t+(af)_x=0 also differ when a_x is nonzero. This edition
uses constant a only, where the two PDE forms coincide.

## Four endpoint constraints determine a cubic

On an interval of width h, with normalized coordinate s∈[0,1], the cubic is

\[
P(s)=H_{00}(s)f_L+hH_{10}(s)g_L+H_{01}(s)f_R+hH_{11}(s)g_R,
\]

\[
\begin{aligned}
H_{00}&=2s^3-3s^2+1,&H_{10}&=s^3-2s^2+s,\\
H_{01}&=-2s^3+3s^2,&H_{11}&=s^3-s^2.
\end{aligned}
\]

The endpoint values and physical derivatives are reproduced, and the new
states are f_i=P(s_d) and g_i=P′(s_d)/h. Here P′ differentiates with respect
to s. For positive a, the interval is [x_{i−1},x_i] and s_d=1−a dt/h; for
negative a it is [x_i,x_{i+1}] and s_d=−a dt/h. The implementation restricts
|a|dt/h≤1 to keep the departure point in this adjacent interval. The case
|a|dt/h=1 shifts both arrays by one node exactly.

This is a complete characteristic/remapping update for this constant-speed
problem, rather than a spatial RHS subsequently advanced by an arbitrary RK
method. It belongs beside the [RK family](runge-kutta.md), not inside its list
of time-integration tableaus. More general semi-Lagrangian schemes can cross
multiple cells; that capability is outside this adjacent-cell example.

## Reproducible scalar tests

The domain is periodic [0,1], with N=128 point nodes x_i=i/N. Notebook choices
are a=±1, Courant magnitudes 0.25, 0.6, or 1, and final times 0.25 or 1.
The last step is shortened. Every configuration is solved independently to
its selected final time, without interpolation between saved solutions.

The smooth profile is 1+0.2 sin(2πx). Initial g is either its analytic
derivative or the centered periodic difference. The square pulse is one on
[0.2,0.4) and zero elsewhere. Its initial slopes are either zero or centered
differences. Zero is an explicit convention at a sampled discontinuity, not
an analytic derivative there. Consequently there is no square-pulse exact
gradient error displayed.

The reference f is exact translated **point samples**. These are not the
cell-average references used in the finite-volume [limiter notebook](limiters.md).
Reported L1 means the average absolute point error. Initial-gradient choice
can materially affect sharp features. The basic cubic has no TVD, monotonicity,
or positivity limiter, and the square test shows overshoot and undershoot.
The linear interpolation comparison is the same signed-characteristic
point-value update, algebraically first-order upwind for |C|≤1.

Smooth refinement uses N=32,64,128,256, a=1, Courant=0.6, and T=0.37. The
computed value errors approach order three for both gradient initializations;
the gradient errors are recorded separately. A cubic interpolant alone is
not a fourth-order global-accuracy claim after repeated remapping. Integer
Courant shifts are a special exact-translation case, so they are not used
to infer a generic refinement order. No equal-cost ranking is made between
the N-state linear method and the 2N-state CIP method.

## Why a sine wave is not a conservation proof

The exact integral of the periodic piecewise-Hermite reconstruction is

\[
M=\sum_i\left[\frac h2(f_i+f_{i+1})+
\frac{h^2}{12}(g_i-g_{i+1})\right]=h\sum_i f_i.
\]

For uniform constant-speed remapping with fraction s, its one-step change is

\[
\Delta M=h^2\,[H_{10}(s)+H_{11}(s)]\sum_i g_i.
\]

The initial analytic sine slopes and centered differences sum to zero, so
the displayed scalar runs can conserve this integral to roundoff even though
the method has no universal conservative remapping property.

The separate counterexample uses N=32 and a valid periodic C1 Hermite field
with f_i=1 and g_i=1 at every node. This is **not a constant function**:
each interval contains a small cubic ripple, and its derivative varies
between the nodes. Its exact integral is 1. Exact translation preserves that
integral, while one CIP remapping step at C=0.35 gives

\[
s=0.65,\qquad \Delta M=h\,s(1-s)(1-2s)=-0.0021328125.
\]

The plot shows the exact shifted original reconstruction and the reconstructed
CIP field over the first four intervals. This is an intentionally constructed
grid-scale test of a claimed property, not a prediction of the mass error for
every smooth flow. Integrals are evaluated analytically, not by coarse
quadrature. Small errors in an easy test cannot establish a stronger guarantee.

## Conservative and shape-preserving branches

[CIP–CSL (Yabe et al., 2001)](https://doi.org/10.1175/1520-0493(2001)129%3C0332:AECSLS%3E2.0.CO;2)
introduces an integral constraint and conservative semi-Lagrangian transport.
Rational CIP / RCIP changes the reconstruction, and variants apply additional
shape constraints. Conservation and boundedness require their own definitions
and tests; neither follows solely from the CIP name.

This edition implements the original 1D cubic only. CIP–CSL2/CSL4, RCIP,
fluid advection/non-advection splitting, multidimensional mixed derivatives,
and complete compressible or multiphase solvers are reading context. The
existing Euler shock-tube solvers retain their documented reconstruction and
flux choices.

## Reproduce

```python
from numart.cip import solve_advection, mass_counterexample

wave = solve_advection(profile="sine", speed=-1., cfl=0.6)
pulse = solve_advection(profile="square", gradient="centered")
print(mass_counterexample()["mass_after"])
```

```bash
python scripts/build_cip.py
python scripts/sync_web_content.py
```

`docs/figures/cip.json` records 48 paired CIP/linear configurations, derivative
arrays, diagnostics, three refinement series, the conservation counterexample,
and source hashes. The browser selects these Python-computed results. Tests
check exact cubic reconstruction and derivatives, both directions, one-cell
shifts, constant preservation, smooth refinement, oscillations, and the
analytic mass-change identity.

![Computed CIP comparisons](figures/cip.png)
