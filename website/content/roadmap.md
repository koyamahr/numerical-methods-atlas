# Implementation roadmap

## First edition: executable foundations

Version 0.1.0 brings together an educational Python library, a historical atlas,
English method notes, a bibliographic catalog, comparison figures, and automated
numerical checks. The repository is the first-edition distribution; the reading
guide in the [README](../README.md) connects the material.

The NASA case catalog and rotated-solver reading notes describe future work.
Their inclusion does not indicate that those flow simulations are implemented.

## Next verification work

- Strengthen links between run manifests and saved arrays; report grid and time refinement together with wall-clock costs.
- Add finite-volume cell-average initialization and integrated references, characteristic WENO, positivity limiters, and stronger shock tests.
- Add exact shallow-water and isothermal references; treat topography, well balancing, and dry beds as separate implementation steps.
- Extend MHD verification with Alfvén waves, Brio–Wu, field loops, less dissipative upwind CT, and external reference-code comparisons.
- Explore nonlinear Fourier methods and dealiasing, Euler DG with limiting, and multidimensional residual distribution.
- Implement low-Mach PDE preconditioning and 2D Euler rotated-hybrid solvers; test entropy correction, positivity, and carbuncle resistance separately.
- Extend elliptic solvers to variable coefficients, anisotropy, line smoothing, FAS, AMG, and 2D mixed boundaries.

## Suggested order for NASA cases

Start with wedge and expansion flows to verify 2D Euler fluxes and wall
boundaries. Use the cavity and Blasius cases to establish viscous, pressure,
and boundary treatments, then the cylinder to examine unsteady accuracy.
For RANS, verify model implementations on flat-plate and bump cases before
moving to airfoils, steps, diffusers, and humps. This order follows dependencies
and difficulty and complements the atlas's publication chronology.

## Web edition

[The public web edition](https://koyamahr.github.io/the-art-of-numerical-algorithms/)
organizes the first-edition library as a historical atlas, method reading room,
computed gallery, and searchable reference library. Each exhibit connects
literature, equations, execution, figures, and verification scope.

The interactive Sod comparison switches between four precomputed MUSCL density
curves from the Python library. Figures and the original gallery validation
manifest remain available alongside the complete source edition. Future
exhibits should continue to distinguish tested educational examples,
original-figure reproductions, prototypes, literature-only entries, and
planned work.

## First expansion: interactive numerical notebooks

The stability laboratory runs periodic FTCS, upwind, classical LF, and LW
updates in the browser, with both velocity signs, Fourier amplification,
pointwise error, and downloadable experiment snapshots. Its numerical kernels
are checked against the Python implementation across 24 reference cases.

The convergence notebook makes the existing DG and Euler entropy-wave gallery
measurements inspectable, including observed slopes and scalar-unknown counts.
It introduces no new wall-clock ranking or general nonlinear stability claim.
The [experiment guide](experiments.md) records definitions and provenance.

## Second expansion: geometry, time, and multidimensional shocks

Added seven scalar ODE integrators with a temporal notebook; three mesh-connectivity examples with an explorer; 1D SPH kernel reconstruction; a 1D ALE geometric-conservation check; and cylindrical gradient, Newtonian stress, and stress-divergence operators verified against analytic fields. The [coordinate and viscosity chapter](coordinates-viscosity.md) distinguishes physical components from coordinate-basis tensors.

[The 2D Double Mach Reflection baseline](double-mach.md) now computes an actual Mach-10 interaction with first-order HLL and SSPRK2. Higher-order reconstruction, full grid refinement, and resolution of the fine wall jet remain future work. This does not implement the other cataloged NASA cases. [Carbuncle comparisons](carbuncle.md), a complete SPH fluid solver, unstructured flow fluxes, and a complete ALE Euler solver also remain future work. [The Roe memorial](roe-memorial.md) is sourced from official university records.
