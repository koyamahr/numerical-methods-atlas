# Slope limiters: minmod, Superbee, MC, van Leer, and van Albada

Limiters trade linear high-order reconstruction for a nonlinear choice of
local slope. Open the [limiter notebook](https://koyamahr.github.io/numerical-methods-atlas/#/limiters)
to compare five choices on identical grids and time integrators, together with
first-order and unlimited scalar baselines.

## Reconstruction and the ratio convention

For uniform cells, let the backward and forward increments be

\[
a_i=\bar u_i-\bar u_{i-1},\qquad b_i=\bar u_{i+1}-\bar u_i,
\qquad r_i=a_i/b_i,\qquad s_i=\phi(r_i)b_i.
\]

The two states reconstructed from cell i are

\[
u_{i+1/2}^{L}=\bar u_i+\tfrac12s_i,\qquad
u_{i-1/2}^{R}=\bar u_i-\tfrac12s_i.
\]

The implementation works directly with a and b, so a zero denominator at a
plateau requires neither a numerical epsilon nor an arbitrary ratio. Opposite
signs or either zero increment give zero limited slope. These are increments;
divide by cell width only if a derivative is required.

## Five limiter functions

Each function below is zero for r ≤ 0. For r > 0:

\[
\begin{aligned}
\phi_{\rm minmod}(r)&=\min(1,r),\\
\phi_{\rm Superbee}(r)&=\max\{\min(2r,1),\min(r,2)\},\\
\phi_{\rm MC}(r)&=\min\{2r,(1+r)/2,2\},\\
\phi_{\rm van\ Leer}(r)&=2r/(1+r),\\
\phi_{\rm van\ Albada}(r)&=(r^2+r)/(r^2+1).
\end{aligned}
\]

This is the **clipped, symmetric van Albada form**, without an epsilon
regularization; other variants differ near extrema. MC means monotonized
central. All five satisfy phi(1)=1 and the plotted scalar bounds
0 ≤ phi(r) ≤ min(2r,2). See [Sweby (1984)](https://doi.org/10.1137/0721062)
for the scalar flux-limiter framework and Roe's compressive construction, and
the [Clawpack limiter documentation](https://www.clawpack.org/pyclaw/evolve/limiters.html)
and [MPI-AMRVAC slope-limiter notes](https://amrvac.org/md_doc_2limiter.html)
for implementation conventions. Names shared by different codes do not settle
which variables, time integrator, or epsilon are used.

Minmod chooses the smaller same-sign increment. Superbee takes a more
compressive slope and can sharpen a smooth feature into a plateau. MC and van
Leer retain more slope than minmod in many monotone regions. The notebook
lets the error, variation, and overshoot measurements qualify those tendencies;
no limiter wins every problem.

## Computed comparisons

The scalar equation is u_t + a u_x = 0 on [0,1], with periodic boundaries.
All runs use conservative finite volumes, upwind interface fluxes, SSPRK(3,3),
N=200, |a| dt/dx ≤ 0.3, and final time 1. The last step is shortened. Both
directions a=±1 are computed. The two profiles are a unit square pulse on
[0.2,0.4] and sin(2πx). Initial and reference values are **exact cell averages**,
including partially covered square-pulse cells and the sine's sinc factor.
Displayed L1 errors use those cell averages. Periodic total variation includes
the last-to-first cell jump; mass is dx times the sum. Maximum TV uses every
saved full-step diagnostic, including the initial state.

The first-order comparison has zero slope. The unlimited comparison uses the
centered slope (a+b)/2 with the same flux and SSPRK3; it can produce oscillations.
It is not the Lax–Wendroff fully discrete method.

The separate Sod comparison uses the existing ideal-gas setup, gamma=1.4,
N=200, t=0.2, HLLC, primitive-variable reconstruction, and SSPRK3 at CFL=0.3.
Only the slope choice changes. Its density error is **pointwise**, following
the existing Sod convention; it is not an exact cell-average error. Outflow
boundaries mean that the periodic scalar mass/TV diagnostics are not applied
to this panel.

Smooth sine refinement at N=40,80,160 and t=0.2 reports measured L1 errors and
orders. A second-order label describes smooth-region consistency, not uniform
pointwise accuracy at extrema or a second-order error on discontinuities.

## TVD is a property of the complete scalar update

For this scalar MUSCL operator, the stated slope bounds together with
|a| dt/dx ≤ 1/2 give a TVD forward-Euler building block; SSPRK3 preserves its
convex stability property under that bound. The executable solver restricts
CFL to this range. Tests check both signs, periodic conservation, full-step
variation, bounds, and a forward-Euler random-data case at CFL=1/2.

The same function applied componentwise to Euler primitive variables is not a
general system TVD theorem, entropy condition, or guarantee of positive cell
averages. Characteristic reconstruction and a fully discrete positivity
construction are separate extensions. See [advanced limiters](advanced-limiters.md)
for TVB extrema relaxation and conservative positive-state scaling.

## Reproduce and inspect

```bash
python -m numart.cli run sod --method muscl --riemann hllc --limiter superbee --n 200
python scripts/build_limiters.py
python scripts/sync_web_content.py
```

```python
from numart import get_problem, solve
from numart.tvd import solve_advection

sod = solve(get_problem("sod"), limiter="mc")
pulse = solve_advection(profile="square", limiter="van-leer", speed=-1.)
```

`docs/figures/limiters.json` records all plotted arrays, refinement results,
diagnostics, and source hashes. The browser selects these Python-computed
curves; it does not run another implementation of the PDE solver. Default
MUSCL remains minmod. The limiter option does not apply to WENO5 or the 2D
Euler/MHD baselines.

![Computed slope-limiter comparison](figures/limiters.png)
