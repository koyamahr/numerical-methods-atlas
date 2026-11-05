# Double Mach Reflection

This exhibit computes a Mach-10 shock reflecting from a wall using the two-dimensional ideal-gas Euler equations. The benchmark is associated with [Woodward and Colella (1984)](https://doi.org/10.1016/0021-9991(84)90142-6). NASA’s [LAVA tutorial](https://www.nas.nasa.gov/LAVA/unst_docs/tutorials/double_mach/double_mach/) is a modern implementation reference.

![Computed Double Mach Reflection: density and density contours on a 256 by 64 grid, first-order HLL with SSPRK2.](figures/double-mach.png)

## Equations and initial states

Use gamma = 1.4 on [0,4] × [0,1], with conserved state U = (rho, rho u, rho v, E) and E = p/(gamma−1) + rho(u²+v²)/2. The initial shock intersects the bottom wall at x = 1/6 and makes a 60-degree angle with it:

\[
x_s(y,0)=\frac16+\frac{y}{\sqrt3}.
\]

The post-shock state to its left is (rho,u,v,p) = (8, 8.25 sqrt(3)/2, −4.125, 116.5). The ambient state to its right is (1.4,0,0,1). The upstream sound speed is one, so the shock-normal propagation speed of ten corresponds to Mach 10.

Initial cell states are assigned by the cell-center side of the shock; cut-cell averages are not integrated exactly.

The moving incident-shock line is

\[
x_s(y,t)=\frac16+\frac{y+20t}{\sqrt3}.
\]

These states satisfy the moving Rankine–Hugoniot relation in the shock-normal direction; the automated check uses normal (sqrt(3)/2,−1/2) and speed 10.

## Boundary conditions and discretization

The left boundary supplies the post-shock state. The right boundary uses zero-gradient outflow. At the bottom, x < 1/6 supplies post-shock data; the remaining wall reflects normal momentum. The top boundary assigns the two states using x_s(1,t). SSPRK2 stages evaluate this boundary at their corresponding stage times.

The calculation uses piecewise-constant finite volumes, a two-wave HLL flux with Davis-type minimum/maximum acoustic speeds, and an unsplit flux divergence. The step is bounded by

\[
\Delta t=C\left[\frac{\max(|u|+c)}{\Delta x}
+\frac{\max(|v|+c)}{\Delta y}\right]^{-1}.
\]

The displayed run has Nx = 256, Ny = 64, delta x = delta y = 1/64, C = 0.4, final time 0.2, and 811 steps. Its minimum final density is 1.4 and minimum final pressure is 1.0. These are measured diagnostics for this run, not a general positivity theorem.

## Reproduce and inspect

```bash
python -m numart.cli run double-mach --n 64 --cfl 0.4 --output outputs/double-mach
```

Here `--n` sets Ny and Nx = 4 Ny. The command saves `solution.npz`, `run.json`, and `double-mach.png`. The gallery snapshot includes its [run manifest](figures/double-mach-run.json) and [conserved-state arrays](figures/double-mach.npz). Array q has shape (Nx,Ny,4); x and y are cell-center coordinates. The manifest records source hashes and the working-tree state at generation time.

## What the figure establishes

The image shows a computed incident/reflected shock pattern, with density and thirty density contours. **First-order spatial reconstruction is deliberately diffusive.** This grid does not resolve the fine wall jet and roll-up of high-resolution PPM or adaptive calculations. There is no exact final-time solution, grid-convergence study, or digitized original-paper comparison in this exhibit.

Tests check equal-state flux consistency, a periodic uniform state, the incident-shock jump relation, moving-top and reflecting-wall data, and admissible states in a small-grid run. They do not establish convergence of the full reflection pattern. Further work should add higher-order reconstruction, refinement, and independent reference-code comparisons.

For strong-shock instability diagnostics, continue to [the carbuncle phenomenon](carbuncle.md). This HLL image is not a demonstration that a Roe implementation is stable or unstable.

## Watch the reflection evolve

[The saved-state movie](https://koyamahr.github.io/numerical-methods-atlas/#/movies?case=double-mach) shows density and pressure from the same 256 × 64 calculation. It includes actual physical times, solver steps, fixed scales, frame inspection, and MP4 export. Read [the sampling definitions](movies.md).
