# KEEP schemes: preserve the smooth-flow balance, test the limits

KEEP stands for **kinetic-energy and entropy preserving**. The work of Yuichi Kuya, Kosuke Totani, and Soshi Kawai at Tohoku University seeks a low-dissipation balance between the conservative equations of compressible flow. [The original 2018 paper](https://doi.org/10.1016/j.jcp.2018.08.058) is the starting point. The authors’ [2022 conference explanation](https://www.iccfd.org/iccfd11/assets/pdf/papers/ICCFD11_Paper-0401.pdf), especially §2.2 and Eq. (9), states the Cartesian flux implemented here.

This exhibit implements **the original second-order arithmetic-mean Cartesian flux**, with periodic boundaries and classical RK4. It does not implement every later scheme named KEEP. [Watch its smooth-vortex evolution](https://koyamahr.github.io/numerical-methods-atlas/#/movies?case=keep-vortex).

![Original KEEP on a smooth isentropic vortex: density, analytic-reference error, refinement, and entropy-proxy history.](figures/keep-vortex.png)

## Which quantities should be preserved?

In a smooth periodic inviscid flow, mass, momentum, and total energy are conservative. The total kinetic energy alone is generally **not** constant in compressible flow: pressure work exchanges kinetic and internal energy. With K = integral rho |u|²/2,

\[
\frac{dK}{dt}=\int p\,\nabla\cdot u\,dV.
\]

A kinetic-energy-consistent convective discretization should not create a spurious kinetic-energy source through an inconsistent mass/momentum product rule. This is different from imposing dK/dt = 0 on a compressible vortex.

We measure the dimensionless entropy proxy

\[
S_* = \int\rho\log\left(\frac{p}{\rho^\gamma}\right)dV.
\]

For a fixed ideal-gas composition this differs from physical entropy only by fixed factors and an additive mass term. Its change per initial mass is useful when initial isentropic data give S_* approximately zero; dividing by initial S_* would be ill-conditioned.

## The implemented two-point flux

Let an overbar denote the arithmetic mean of left and right values, u_n the velocity normal to a Cartesian face, and e = p/[rho(gamma−1)]. The baseline flux is

\[
\begin{aligned}
C&=\overline\rho\,\overline u_n,\\
F_{\rho u_i}&=C\,\overline u_i+\overline p\,\delta_{in},\\
F_E&=C\left[\frac12\boldsymbol u_L\cdot\boldsymbol u_R+\overline e\right]
+\frac12(u_{n,L}p_R+u_{n,R}p_L).
\end{aligned}
\]

The mass flux is C. The cross-velocity kinetic term and cross-pressure work are deliberate; replacing them by a convenient average of the full physical flux changes the discrete energy exchange. The implementation is a central two-point flux-difference method of second spatial order. It has no Riemann-solver dissipation.

Tests verify equal-state consistency, left/right symmetry, periodic conservation of the primary variables, and the semidiscrete kinetic-energy pressure-work identity. RK4 adds temporal truncation error and does not inherit every semidiscrete identity exactly.

## Appropriate first test: smooth isentropic vortex advection

Use gamma = 1.4 on a periodic [−10,10]² square, background velocity (1,0.5), and vortex strength beta = 3. Relative to its translating center, write X, Y and r² = X²+Y². The reference is

\[
\begin{aligned}
u&=1-\frac{\beta Y}{2\pi}e^{(1-r^2)/2},&
v&=0.5+\frac{\beta X}{2\pi}e^{(1-r^2)/2},\\
T&=1-\frac{(\gamma-1)\beta^2}{8\gamma\pi^2}e^{1-r^2},&
\rho&=T^{1/(\gamma-1)},\qquad p=\rho^\gamma.
\end{aligned}
\]

The whole-plane vortex translates analytically. Minimum-image coordinates in a box of length 20 leave its boundary tails below floating-point significance for these parameters, avoiding an appreciable periodic boundary jump. Positivity of the analytic temperature is checked explicitly.

The static study runs 48², 96², and 192² cells to t = 1 at CFL 0.25. It reports pointwise density L1 error, primary-conservation drift, and the change in S_* per mass. A separate 96² run halves the CFL to assess the time-step contribution. The [measurement manifest](figures/keep-vortex.json) states the actual errors; the expected smooth spatial order is two. The movie instead runs 96² to t = 4 and is a qualitative time-history exhibit, not a substitute for refinement.

## Appropriate next tests

A **compressible inviscid 3D Taylor–Green vortex** is a primary KEEP benchmark. Fix the periodic box [0,2 pi]³, reference density, gamma, initial Mach number, velocity amplitude, initial pressure perturbation, and temporal scheme. Track total energy, kinetic energy, pressure dilatation, entropy, density/temperature RMS fluctuations, and resolved spectra under grid and time refinement. Pressure-work exchange must be separated from numerical dissipation. The original paper also examines inviscid isotropic turbulence. These 3D computations are not implemented in this edition; a 2D slice is not a replacement for the three-dimensional vortex-stretching dynamics.

A smooth **constant-pressure density wave** tests preservation of pressure/velocity equilibrium. It is a useful additional diagnostic, but that property depends on the flux variant. Our original arithmetic-mean flux produces a nonzero semidiscrete pressure residual for this data; a test records that limitation instead of claiming it passes. [Shima et al. (2021)](https://doi.org/10.1016/j.jcp.2020.110060) study pressure-equilibrium-preserving split forms.

## Caveats: entropy, shocks, and the scheme version

1. **Preserving is not a roundoff-exact entropy guarantee.** The authors explicitly distinguish improved entropy behavior from exact conservation in their 2022 explanation. [Tamaki, Kuya, and Kawai (2022)](https://doi.org/10.1016/j.jcp.2022.111494) analyze remaining entropy errors and redefine KEEP variants with tunable approximation order. Our code does not implement that redefinition or an exact logarithmic-mean entropy-conservative flux.
2. **A shock requires entropy production.** A bare non-dissipative central flux supplies no general mechanism to select a non-oscillatory admissible shock solution. Sod, Shu–Osher, and Double Mach Reflection are not acceptance tests for the unstabilized baseline demonstrated here. A shock-tube run can still be a deliberate limitation/oscillation diagnostic; it should not be advertised as a validated shock-capturing result. It is inaccurate to turn this into a universal statement that every KEEP-based method is unable to solve any shock tube.
3. **Shock stabilization changes the method.** A sensor, artificial viscosity, upwind blending, filtering, or another entropy-stable construction needs its own definition and tests. Record shock/contact thickness, oscillations, positivity, and added dissipation; keep separate results for the smooth base scheme and stabilized extension. No such extension is implemented here.
4. **No positivity theorem is supplied.** Positive density and pressure in the displayed smooth runs do not establish robustness near vacuum or under arbitrary under-resolution. The code stops on nonphysical states rather than silently clipping them.
5. **Time integration and boundaries matter.** [Asada, Maruyama, and Kawai (2024)](https://doi.org/10.1016/j.compfluid.2023.106143) address temporal preservation. Our RK4, periodic uniform-grid experiment does not implement their method, high-order/curvilinear KEEP, hanging-node treatments, wall models, or a production LES solver.

## Reproduce

```bash
python scripts/build_keep.py
python -m pip install '.[movies]'
python scripts/build_movies.py
```

The first command creates the smooth-error figure and its source manifest. The second build adds the KEEP vortex to the [motion gallery](movies.md). Continue with [shock benchmarks](benchmarks.md), [carbuncle caveats](carbuncle.md), and [the distinction from symplectic Hamiltonian maps](symplectic.md): KEEP’s fluid energy/entropy consistency and symplecticity of a mechanical time map are different properties.
