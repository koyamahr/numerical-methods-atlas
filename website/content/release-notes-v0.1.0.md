# v0.1.0 — First edition

The first edition of **The Art of Numerical Algorithms** connects historical
papers with equations, executable educational implementations, benchmark
figures, and numerical verification.

## Included

- An English historical atlas and method notes covering conservation laws, stability, diffusion, boundary conditions, iterative solvers, DG, spectral methods, and MHD.
- A Python library and CLI for Euler, shallow-water, isothermal, linear-advection, diffusion, Poisson, and planar ideal-MHD examples.
- Godunov-type and MUSCL finite volumes, Rusanov/HLL/HLLE/HLLC/Roe fluxes, FD WENO5-JS, modal DG, and Fourier propagation.
- Thomas elimination, matrix-free conjugate gradients, red-black relaxation, and geometric multigrid.
- Minimal dual-time, matrix-scaling, and scalar residual-distribution examples.
- CT and GLM magnetic-constraint demonstrations with distinct divergence diagnostics.
- A 39-entry bibliography with English source notes, generated Markdown and BibTeX, plus a NASA 2D case catalog for future work.
- Automated numerical checks and a gallery-generation workflow for Python 3.9 and 3.12.

## Install and run

Requires Python 3.9 or later. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install '.[test]'
python -m pytest -q
python -m numart.cli gallery --output outputs/gallery
```

Start with the [reading guide](../README.md#reading-guide) and
[benchmark definitions](benchmarks.md).

## Scope of this edition

The examples are independently implemented educational models. Their figures
do not claim to reproduce the original papers' figures. Verification covers
selected configurations and does not prove general nonlinear stability or
positivity. Finite-volume and finite-difference errors are identified as
pointwise comparisons, and CT/GLM divergence measurements name their operators.

NASA flow cases, multidimensional Euler rotated-hybrid fluxes, low-Mach PDE
preconditioning, Euler/MHD DG, and multidimensional residual distribution remain
future work. See the [roadmap](roadmap.md) for next steps and the
[reference notes](references.md) for unverified original-source details.
