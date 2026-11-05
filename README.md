# The Art of Numerical Algorithms

**Read the paper. Understand the method. Run the benchmark.**

A historical, executable guide to numerical algorithms: the equations they solve,
the ideas behind their discretizations, and the evidence used to check them.
This is the **first edition, v0.1.0**, and a companion to
[The Art of Thermal Instability](https://koyamahr.github.io/the-art-of-thermal-instability/#home).

Explore the [historical atlas](docs/history.md), run the Python examples, and
compare the results with analytical solutions and conservation checks. The
library covers selected educational models; the [roadmap](docs/roadmap.md)
identifies the extensions still to be implemented.

**[Read the web edition](https://koyamahr.github.io/the-art-of-numerical-algorithms/)** — browse the atlas, methods, gallery, and searchable references.

## Getting started

Requires Python 3.9 or later.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install '.[test]'
python -m pytest -q
python -m numart.cli gallery --output outputs/gallery
```

For an existing environment, start with `source .venv/bin/activate`.
Figures, numerical data, settings, and source SHA-256 hashes are saved together.
Runs made before the first Git commit record a `null` Git revision and use the
source hashes to identify the implementation.

## Reading guide

1. [Historical atlas](docs/history.md): CFL, implicit diffusion, Lax, Godunov, multigrid, DG, spectral methods, Roe, ENO/WENO, MHD, and dual time stepping.
2. [Differences, CFL, and stability](docs/stability.md): spatial stencils, explicit and implicit time integration, von Neumann analysis, and the Lax equivalence theorem.
3. [Diffusion, elliptic problems, and iteration](docs/elliptic.md): Thomas elimination, boundary conditions, spectral radii, and a multigrid V-cycle.
4. [Benchmark library](docs/benchmarks.md): initial conditions, reference solutions, boundaries, and the limits of each comparison.
5. [MHD: CT and GLM](docs/mhd.md): discrete magnetic divergence, Orszag–Tang, and injected-error diagnostics.
6. [Preconditioning and advanced methods](docs/advanced.md): dual time stepping, residual distribution, and the path to multidimensional solvers.
7. [NASA 2D case catalog](docs/nasa-2d.md): official verification and validation resources for future implementations.
8. [References](docs/references.md), [BibTeX](references.bib), [roadmap](docs/roadmap.md), and [first-edition release notes](docs/release-notes-v0.1.0.md).

Additional reading: [time integration and leapfrog](docs/time-integration.md), [meshes](docs/meshes.md), [SPH](docs/particles-sph.md), [ALE](docs/ale.md), [cylindrical tensors and viscosity](docs/coordinates-viscosity.md), [Double Mach Reflection](docs/double-mach.md), [carbuncle](docs/carbuncle.md), and [Remembering Philip L. Roe](docs/roe-memorial.md).

Further reading: [symplectic Hamiltonian maps](docs/symplectic.md), [PM / P³M / Tree / multipoles](docs/particle-gravity.md), and [Hockney–Eastwood / Koyama–Ostriker gravity kernels](docs/gravity-boundaries.md).

New exhibits: [CIP value/gradient transport](docs/cip.md), [Runge–Kutta families](docs/runge-kutta.md), [slope limiters](docs/limiters.md), [advanced TVB and positive-state scaling](docs/advanced-limiters.md), [nonsteady movies](docs/movies.md), and [original KEEP with smooth tests and caveats](docs/keep.md). Steady fields remain still figures.

## Interactive notebooks

- [Stability laboratory](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/experiments): compute periodic FTCS, upwind, LF, and LW advection in the browser. Change the signed Courant number, initial profile, and step count; inspect amplification and export the experiment.
- [Convergence notebook](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/convergence): inspect the original DG and Euler entropy-wave refinement data, switch between elements and unknowns, and read measured convergence orders.
- [CIP profiles](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/cip): cubic-Hermite value/gradient transport, scalar advection, refinement, oscillations, and a conservation counterexample.
- [Runge–Kutta families](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/runge-kutta): nine explicit RK methods, actual nonlinear stages, Butcher tableaus, stability contours, measured orders, and conditional SSP bounds.
- [Time integration](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/time-integration): twelve Python-computed oscillator methods, including unfiltered leapfrog and its startup mode.
- [Mesh explorer](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/meshes): select cells and inspect face-sharing neighbors in structured and irregular meshes.
- [Hamiltonian maps](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/hamiltonian): symplectic Euler, Verlet, Yoshida fourth order, implicit midpoint, and RK4 on two Hamiltonians.
- [Limiter notebook](https://koyamahr.github.io/the-art-of-numerical-algorithms/#/limiters): minmod, Superbee, MC, van Leer, and clipped van Albada; scalar advection, Sod, Sweby bounds, refinement, TVB parameters, and a separate mean-preserving positive Euler reconstruction.
- [Experiment guide](docs/experiments.md): equations, provenance, reproducibility, and the limits of each comparison.

## Run a benchmark

```bash
python -m numart.cli run sod --method muscl --riemann roe --n 200
python -m numart.cli run double-mach --n 64 --cfl 0.4 --output outputs/double-mach
python -m numart.cli run lax --method muscl --riemann hllc --n 200
python -m numart.cli run shu-osher --method weno5 --n 400
python -m numart.cli run entropy-wave --method weno5 --n 160
python -m numart.cli run double-rarefaction --method godunov --riemann hlle --n 200
python -m numart.cli run dam-break --riemann hll --n 200
python -m numart.cli run isothermal --riemann hll --n 200
python -m numart.cli run orszag-tang --method ct --n 64 --output outputs/ct
python -m numart.cli run orszag-tang --method glm --n 64 --output outputs/glm
```

`run` writes numerical arrays and a `run.json` manifest. `gallery` generates
comparison figures. Reusing an output directory overwrites its files; use a
separate `--output` for each result you want to retain.
WENO uses global Lax–Friedrichs flux splitting and ignores `--riemann`.

The same methods are available from Python:

```python
from numart import get_problem, solve
from numart.advection import dg_advection, dual_time_advection
from numart.linear import diffusion_1d, poisson_1d, poisson_2d, Boundary, poisson_boundary_1d
from numart.multigrid import solve_poisson_multigrid
import numpy as np

r = solve(get_problem("sod"), n=200, method="muscl", riemann="hllc")
x, u, modes = dg_advection(n=32, degree=2)
x, u, settings = diffusion_1d(method="crank-nicolson", dt=0.001)
x, u = poisson_boundary_1d(63, -2., Boundary.dirichlet(1.), Boundary.neumann(2.))
u, residual = solve_poisson_multigrid(np.ones((63, 63)))
```

## First-edition gallery

![Sod shock tube compared with the exact Riemann solution](docs/figures/sod.png)

![Discontinuous Galerkin and Fourier advection examples](docs/figures/dg-spectral.png)

![Orszag–Tang vortex: CT and GLM educational implementations](docs/figures/orszag-tang.png)

These figures come from independent educational implementations. They do not
claim to reproduce the original papers' figures. CT and GLM use different
discrete operators and dissipation; magnetic-divergence values alone do not
establish which method is more accurate.

## Implemented in the current first edition

- **Finite differences:** forward, backward, centered, and upwind stencils; Lax–Friedrichs, Lax–Wendroff, and componentwise FD WENO5-JS.
- **Finite volumes:** piecewise-constant Godunov-type updates and primitive-variable slope-limited MUSCL; Rusanov, HLL, HLLE, HLLC, and Roe fluxes.
- **Discontinuous Galerkin:** periodic linear advection with modal Legendre P0/P1/P2, upwind fluxes, and SSPRK3.
- **Spectral methods:** periodic Fourier advection and diffusion, exact integration of linear modes, and Fourier differentiation.
- **Smooth KEEP:** original second-order arithmetic-mean Cartesian Euler flux with RK4, periodic isentropic-vortex refinement and explicit entropy/shock/PEP caveats.
- **2D Euler:** first-order HLL + SSPRK2 Double Mach Reflection with time-dependent shock and reflecting-wall boundaries.
- **Temporal and geometric models:** twelve scalar ODE integrators, explicit mesh connectivity, 1D SPH reconstruction, and a moving-volume ALE identity check.
- **Cylindrical tensors:** orthonormal velocity gradient, Newtonian stress with bulk viscosity, and symmetric stress divergence at r > 0.
- **Particle gravity:** periodic 3D CIC/FFT PM; isolated softened octree with monopole or second moments; isolated doubled-grid and periodic-horizontal/vacuum-vertical slab convolution. Full P³M, TreePM, and FMM remain reading directions.
- **Hamiltonian maps:** fixed-step symplectic Euler, Verlet, Yoshida fourth order, implicit midpoint, and RK4 comparisons for harmonic/quartic oscillators.
- **MHD:** planar 2D ideal MHD with first-order Rusanov fluxes, staggered constrained transport, and cell-centered GLM cleaning.
- **Diffusion and elliptic equations:** FTCS, backward Euler, Crank–Nicolson, 1D Thomas elimination, and 2D matrix-free conjugate gradients.
- **Iterative methods:** Jacobi, Gauss–Seidel, and SOR iteration matrices; red-black relaxation; and geometric multigrid V-cycles.
- **Minimal advanced models:** BDF1/BDF2 dual time stepping, symmetric Jacobi scaling, and 1D scalar residual distribution.

Multidimensional Euler rotated-hybrid fluxes, low-Mach PDE preconditioning,
2D residual distribution, and Euler/MHD DG remain future work. The NASA airfoil,
boundary-layer, and separated-flow catalog requires additional Navier–Stokes or
RANS solvers, meshes, and wall treatments.

## Verification and reproducibility

The test suite checks flux consistency, exact solutions, selected convergence
orders, periodic conservation, selected positivity cases, CT divergence
preservation, GLM error cleaning, linear-system residuals, boundary conditions,
and multigrid. These checks establish behavior for the tested cases; they do
not prove general positivity or nonlinear stability.

[GitHub Actions](https://github.com/koyamahr/the-art-of-numerical-algorithms/actions)
runs the numerical checks and gallery generation on Python 3.9 and 3.12.
Bibliographic notes record whether a source is an original paper, a later
exposition, or a reference that still needs direct inspection. Regenerate the
reference list and BibTeX together with:

```bash
python scripts/build_references.py
```

## Build the web edition

The static website lives in [`website/`](website/README.md). It renders twenty-eight
reading chapters and their equations, includes nineteen gallery figures and four computed movies, and uses
precomputed library results for the interactive Sod comparison. See the web
README for local preview and content-refresh commands.

Regenerate the new geometric and gravity exhibits before syncing the web content:

```bash
python scripts/build_hamiltonian.py
python scripts/build_particle_gravity.py
python scripts/build_gravity_boundaries.py
python scripts/build_limiters.py
python scripts/build_runge_kutta.py
python scripts/build_cip.py
python scripts/sync_web_content.py
```

Build and verify the nonsteady movies (optional MP4 encoder):

```bash
python -m pip install '.[movies]'
python scripts/build_keep.py
python scripts/build_movies.py
python scripts/check_movies.py
python scripts/sync_web_content.py
```
