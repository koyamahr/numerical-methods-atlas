# Interactive experiment guide

The web edition now includes a [stability laboratory](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/experiments)
and a [convergence notebook](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/convergence).
The laboratory computes in the browser; the convergence notebook displays
measurements from the original gallery manifest. These are distinct sources
of evidence.

## Periodic advection in the browser

The model is

\[
u_t+a u_x=0,\qquad x\in[0,1],\qquad u(x+1,t)=u(x,t).
\]

Use 64 cell-centered sample points, `h=1/64`, velocity `a=+1` or `a=-1`,
and `Δt=|C|h`. The signed Courant number is `C=aΔt/h`. The controls expose
`0.05≤|C|≤1.5` and 0–100 time steps. The exact comparison samples the
continuous translated profile `u(x-at,0)` at the same grid points.

Initial data can be a sine wave, a square pulse equal to one on `[0.25,0.65)`
and zero elsewhere, or a sine wave with small high-frequency perturbations:

\[
u(x,0)=\sin(2\pi x)+10^{-3}
\left[\sin(2\pi(N/2)x)+\cos(2\pi(N/4)x)\right].
\]

The ripple seeds both Nyquist and shorter resolved grid-scale modes. It makes
unstable growth visible without relying on machine roundoff. The square
pulse illustrates smearing and dispersive oscillations; it is not a smooth
convergence test.

## Four discrete updates

`numart.advection.difference_step` and the browser implement FTCS, upwind,
classical Lax–Friedrichs, and Lax–Wendroff. Upwind switches stencil with the
velocity sign. The [stability chapter](stability.md) develops their context.
For FTCS,

\[
u_j^{n+1}=u_j^n-\frac C2(u_{j+1}^n-u_{j-1}^n),\qquad
G(\theta)=1-iC\sin\theta.
\]

Its squared amplification is `1+C²sin²θ`. Consequently, nonzero C produces
growing modes even when the necessary domain-of-dependence bound `|C|≤1`
is met. Upwind, LF, and LW satisfy the Fourier stability criterion for this
periodic constant-coefficient problem when `|C|≤1`.

The solution plot updates alongside `|G(θ)|`. The reported maximum samples
all distinct real-data Fourier wavenumbers of the 64-point grid. The dashed
threshold marks `|G|=1`. When the solution grows, its vertical scale expands
rather than clipping the computed values. Pointwise L1 error, maximum
amplitude, and arithmetic mean drift are reported separately.

These properties concern this linear periodic model. They do not transfer
automatically to nonlinear systems, other boundaries, or a different time
integrator. With unstable growth, cancellation and floating-point rounding
can also corrupt the measured mean.

## Reproducibility and export

The browser kernels are compared with 24 reference cases generated from the
Python implementation: four methods, six signed Courant numbers, and twelve
updates per case. Tests compare complete sample arrays and complex Fourier
amplification factors. Separate tests check exact one-cell translation at
unit CFL, direction reversal, periodic wrapping, and observed-order arithmetic.
The fixture records the SHA-256 of `numart/advection.py`; a source mismatch
fails the browser numerical tests until the reference export is refreshed.

The experiment download contains settings, grid coordinates, initial,
computed, and exact samples, diagnostics, and the Python reference hash.
It records a calculation performed in JavaScript, rather than claiming that
Python runs in the browser.

To apply the same stencil from Python:

```python
import numpy as np
from numart.advection import difference_step

n, courant, steps = 64, 0.8, 40
x = (np.arange(n) + 0.5) / n
q = np.sin(2 * np.pi * x)
for _ in range(steps):
    q = difference_step(q, courant, "lax-wendroff")
exact = np.sin(2 * np.pi * (x - courant * steps / n))
print("pointwise L1 error:", np.mean(abs(q - exact)))
```

## Reading a refinement study

The notebook uses the first-edition `docs/figures/validation.json` measurements.
The original manifest, including source hashes and runtime versions, is
available for download. These data predate the browser laboratory and are not
new wall-clock measurements.

For successive meshes, the displayed observed order is

\[
p_{\mathrm{obs}}=
\frac{\log(E_{\mathrm{coarse}}/E_{\mathrm{fine}})}
{\log(N_{\mathrm{fine}}/N_{\mathrm{coarse}})}.
\]

**DG advection:** periodic scalar transport, final time 0.2, CFL 0.2,
`N=8,16,32,64`, modal Legendre P0/P1/P2, and SSPRK3. The error is RMS sampled
at the implementation's quadrature points. It is not a separately integrated
L2 norm. Pp stores `N(p+1)` scalar unknowns. Toggle the horizontal axis between
elements and unknowns; the data remain unchanged. Spatial orders 1, 2, and 3
and SSPRK3's time order three explain the expected smooth behavior.

**Euler entropy wave:** final time 1, CFL 0.3, `N=40,80,160`, primitive minmod
MUSCL or componentwise FD WENO5-JS with SSPRK3. The error is pointwise density
L1. WENO's fifth-order spatial reconstruction does not remove the third-order
time error, so slopes from this finite sequence do not guarantee asymptotic
fifth-order fully discrete convergence. Euler stores three scalar state
components per point or cell; equal counts do not imply equal computational
cost or identical approximation spaces.

A decreasing error, an observed slope, a positivity test, a small divergence,
and a performance comparison answer different questions. The notebook keeps
those distinctions explicit. See the [benchmark definitions](benchmarks.md)
and the [implementation roadmap](roadmap.md) for the remaining checks.

## Temporal trajectories and mesh connectivity

The [time integration notebook](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/time-integration) selects Python-computed y′ = i y trajectories for seven temporal methods, with fixed final time 20. It exposes step size, leapfrog startup perturbation, two characteristic roots, sampled error, and amplitude. These are precomputed ODE results, unlike the browser-computed spatial stability laboratory. Read the [time integration definitions](time-integration.md).

The [mesh explorer](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/meshes) displays three explicit vertex/cell datasets. Selection highlights face-sharing neighbors; the cell dropdown and keyboard-accessible polygons provide equivalent controls. Geometry is fixed, and no flow is integrated. Read [mesh definitions](meshes.md), [ALE](ale.md), and [SPH](particles-sph.md).

Both notebooks expose `foundations.json`, generated by `scripts/sync_web_content.py`, with source SHA-256 hashes for the temporal and geometry modules. Their Python tests check refinement orders, leapfrog modes, midpoint amplitude, kernel normalization, mesh topology, and moving-volume uniform-state preservation.
