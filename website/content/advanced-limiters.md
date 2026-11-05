# Advanced limiters: TVB and positivity preservation

The [limiter notebook](https://koyamahr.github.io/numerical-methods-atlas/#/limiters)
includes a TVB scalar experiment and a separate conservative Euler-state
scaling demonstration. These address different failure modes: loss of accuracy
near a smooth extremum and inadmissible thermodynamic states.

## TVB modified minmod

For a candidate increment v and neighboring increments a and b, define

\[
\widetilde m(v,a,b)=
\begin{cases}
v,&|v|\le M\Delta x^2,\\
m(v,a,b),&\text{otherwise},
\end{cases}
\]

where m is the generalized minmod: the smallest magnitude with a shared sign,
and zero when signs disagree. Our scalar demonstration chooses v=(a+b)/2.
At M=0 this reduces to the two-increment minmod used in the TVD experiment.
At M>0 sufficiently small increments survive even when the neighboring slopes
have opposite signs, permitting a smooth peak to remain curved.

The dx-squared threshold reflects the scale of smooth-extremum face
deviations in the RKDG setting. Its coefficient has units of solution divided
by length squared; it is not a universal dimensionless constant. Rescaling the
dependent variable or coordinates requires reconsidering M. Increments and
derivatives require different thresholds.

[Cockburn and Shu (1989)](https://doi.org/10.1090/S0025-5718-1989-0983311-4)
develop the TVB RKDG framework. This edition implements **the modified-minmod
building block in scalar finite volumes**, rather than that full RKDG method
or its theorem. The notebook computes M=0,10,50 on both the sine and square
pulse. Compare errors and measured maximum TV: allowing small extrema means
TV need not decrease at every step, and a large M can also admit small
oscillations beside a discontinuity. Changing M does not prove a uniform TVB
bound for an arbitrary method. No Euler-system TVB extension is implemented.

## Positive density and pressure are different constraints

For ideal-gas conservative variables U=(rho,m,E),

\[
p(U)=(\gamma-1)\left(E-\frac{|m|^2}{2\rho}\right),\qquad
\mathcal G=\{U:\rho>0,\ p(U)>0\}.
\]

Positive density alone does not ensure positive internal energy. TVD, TVB,
an entropy fix, and the absence of visible wiggles do not automatically make
Euler states admissible. A negative pressure can arise from excessive kinetic
energy even when rho and E are positive.

## A mean-preserving scaling building block

Start with an admissible conservative cell average Ubar. Scale every supplied
reconstruction point by the same factor:

\[
\widehat U_\alpha=\bar U+\theta(U_\alpha-\bar U),\qquad 0\le\theta\le1.
\]

If the original points have quadrature mean Ubar, the scaled points retain it.
Using a single theta across components and points is essential to this
particular construction. Clipping rho, pressure, or total energy independently
does not have that conservation property.

First bound theta by the minimum reconstructed density:

\[
\theta_\rho=\min\left(1,
\frac{\bar\rho-\epsilon_\rho}{\bar\rho-\rho_{\min}}\right)
\quad\text{if }\rho_{\min}<\epsilon_\rho;
\qquad\theta_\rho=1\text{ otherwise}.
\]

Then shrink theta in [0,theta_rho] until every supplied point also satisfies
p(Uhat) ≥ epsilon_p. Ideal-gas pressure is concave for positive density, so
the admissible part of this line segment contains the mean and can be found
by bisection. The implementation uses 64 iterations and a small roundoff
retreat. Density and pressure floors are input parameters, not inserted mass
or energy. Inadmissible averages raise an error; scaling around a bad mean
cannot repair conservation and positivity together in this way.

This follows the convex-scaling idea of
[Zhang and Shu (2010)](https://doi.org/10.1016/j.jcp.2010.08.016), with a
deliberately simple common-state scaling and numerical pressure search. It is
not a line-by-line reproduction of their two-stage density-polynomial and
state limiter. The implementation covers the supplied points only; arbitrary
polynomial values between those points are not automatically bounded.

## What the demonstration actually verifies

The three-node cell has xi=-1,0,1, positive Gauss–Lobatto weights
(1/6,2/3,1/6), gamma=1.4, and Ubar=(1,0,2.5). The raw states are
Ubar + xi times delta. Choose delta=(1.2,0,0) for a density violation,
(0,3,0) for a pressure violation, or (1.2,3,1) for a combined violation.
Their weighted mean is exactly Ubar in real arithmetic. The plot samples only
these three nodes and reports theta, minimum limited density, minimum limited
pressure, and the conservative mean defect, with epsilon_rho=epsilon_p=1e-8.
These are constructed reconstruction tests, not blast-wave or rarefaction
time integrations.

```python
import numpy as np
from numart.limiters import positive_reconstruction

mean = np.array([1., 0., 2.5])
raw = mean + np.array([-1., 0., 1.])[:, None] * [0., 3., 0.]
limited, theta = positive_reconstruction(mean, raw)
```

Tests check that an already admissible reconstruction is unchanged, bad means
are rejected, and both floors and conservative quadrature means survive the
three failure cases.

## From reconstruction to a fully discrete guarantee

A complete positivity-preserving Euler method also needs a compatible
positivity-preserving numerical flux, positive quadrature decomposition
including interface states, a corresponding wave-speed/CFL restriction, and
limiting at all required stages. SSP time stepping propagates a forward-Euler
positivity property only when that property and its step restriction already
hold. Source terms and boundary treatment require their own checks.

This helper is **not wired into the existing Euler MUSCL, finite-difference
WENO, CT/GLM, or KEEP time updates**. Those solvers retain their documented
limitations. A future complete implementation should add stage-by-stage
admissibility and conservation checks, near-vacuum double rarefaction, and
strong blast-wave tests before claiming positivity preservation over time.
Multidimensional and non-ideal-EOS extensions need additional analysis.
