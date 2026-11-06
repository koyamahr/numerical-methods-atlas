# Site coverage and counting rules

Published web edition, counted 2026-11-06. These are counts of catalog entries and documented examples, not a claim that every entry is a verified end-to-end solver.

**42 equation/model entries · 85 methods and building blocks · 127 journal/conference papers · 148 total sources.**

There are 9 saved-profile equation-gallery cases across 7 equation families, and 43 reading chapters including this inventory.

## Equations and models

Named equation/model entries, not scalar component equations or mathematically disjoint families. Includes frameworks and auxiliary formulations; variants share one entry except the three separately explained SR/GR fluid systems. Biological entries are imported once from their own catalog.

15 entries have scoped local examples; 27 are reading-only, including all 22 biological survey entries. A coupled system is one entry; its individual component equations do not increase the count. Poisson/Laplace and dimensional variants share entries. Named frameworks and specialized kinetic laws can both appear, so this is not a count of mathematically disjoint families.

## Equation/model inventory

### Physics & mathematical models

- [Linear advection](stability.md) — Local example.
- [Heat / diffusion](elliptic.md) — Local example.
- [Poisson / Laplace](elliptic.md) — Local example.
- [Inviscid Burgers](equation-gallery.md) — Local example.
- [LWR traffic flow](equation-gallery.md) — Local example.
- [Compressible Euler](benchmarks.md) — Local example.
- [Shallow water, including the rotating linear model](geophysical-grids.md) — Local example. Wet 1D flow and linear rotating Fourier symbols; no full geophysical dynamical core.
- [Isothermal Euler](benchmarks.md) — Local example.
- [Ideal MHD](mhd.md) — Local example.
- [Incompressible Navier–Stokes](incompressible.md) — Local example.
- [Isothermal lattice BGK](lattice-boltzmann.md) — Local example.
- [Hamiltonian oscillators](symplectic.md) — Local example.
- [Gravitational particle model](particle-gravity.md) — Local example. Static force evaluations and boundary kernels; no coupled self-gravitating fluid evolution.
- [Bratu nonlinear boundary-value problem](sparse-nonlinear.md) — Local example.
- [Auxiliary hyperbolic diffusion system](hyperbolic-diffusion.md) — Local example. Periodic first-order steady-solution baseline, not physical-time heat diffusion.

### Relativistic models

- [Special-relativistic hydrodynamics](relativistic-hydrodynamics.md) — Reading only. Literature review; no local relativistic solver.
- [General-relativistic hydrodynamics](relativistic-hydrodynamics.md) — Reading only. Literature review; no local relativistic solver.
- [General-relativistic MHD](relativistic-hydrodynamics.md) — Reading only. Literature review; no local relativistic solver.
- [Relativistic radiation moments / M1](relativistic-hydrodynamics.md) — Reading only. Literature review; no local relativistic solver.
- [Causal relativistic viscous fluid](relativistic-hydrodynamics.md) — Reading only. Literature review; no local relativistic solver.

### Biological model survey

- [Logistic population growth](biological-models.md) — Reading only. The linked original is the later 1847 memoir; the 1838 note itself was not audited. The differential equation is not the discrete logistic map.
- [Michaelis–Menten and full enzyme kinetics](biological-models.md) — Reading only. The 1913 rapid-equilibrium interpretation and the 1925 quasi-steady-state derivation must remain distinct.
- [Lotka–Volterra predator–prey](biological-models.md) — Reading only.
- [McKendrick age-structured population](biological-models.md) — Reading only. This is the classical age-transport form; the later von Foerster lineage is acknowledged without treating its date as the first appearance.
- [SIR and SEIR compartment models](biological-models.md) — Reading only. The original general epidemic framework is broader than this SIR specialization. Population-count and fraction conventions give different β definitions.
- [Fisher–KPP invasion front](biological-models.md) — Reading only. Fisher–KPP is a conventional family name; the independent KPP 1937 original remains an archival follow-up. The exact special speed is not the minimal speed.
- [Monod growth and chemostat](biological-models.md) — Reading only. This writes one constant-yield extension of saturation growth, not a universal metabolic model.
- [Hodgkin–Huxley membrane dynamics](biological-models.md) — Reading only. The original squid-axon model is not a calibrated human cardiac model. No single rate parameter set is selected by this survey.
- [Turing reaction–diffusion framework](biological-models.md) — Reading only. A spot image or unequal diffusion coefficients alone do not establish a Turing mechanism. Boundary conditions determine the available modes.
- [FitzHugh–Nagumo excitation and recovery](biological-models.md) — Reading only. This is a common normalized variant; cubic coefficients, recovery signs and nondimensionalization differ between formulations.
- [Keller–Segel chemotaxis](biological-models.md) — Reading only. This is a common two-field reduction of a more detailed original formulation. Blowup thresholds depend on dimension, domain, boundary and chemical dynamics.
- [Gierer–Meinhardt activator–inhibitor](biological-models.md) — Reading only. Source densities, saturation and baseline production vary across the model family. This simplified formula is not a verbatim transcription of every original variant.
- [Fluid–elastic structure and immersed boundaries](biological-models.md) — Reading only. Immersed boundary is a numerical coupling method, not itself a closed biological constitutive equation. The existing periodic MAC solver does not implement this coupling.
- [Chemical master equation and Gillespie SSA](biological-models.md) — Reading only. The 1977 paper is a foundational SSA reference, not a priority claim for all master equations. SSA is a solver; the reaction network is the model. A seed documents a trajectory, not an ensemble validation.
- [Mackey–Glass delayed physiological feedback](biological-models.md) — Reading only. A scalar initial value alone is insufficient. The delayed ODE is distinct from a spatial reaction–diffusion model.
- [Replicator evolutionary game dynamics](biological-models.md) — Reading only. No universal Lyapunov function or equivalence of fixed point and evolutionarily stable strategy is assumed.
- [Schnakenberg reaction–diffusion](biological-models.md) — Reading only. A mathematical chemical pattern model; matching a visual biological pattern does not calibrate it to a tissue.
- [Shigesada–Kawasaki–Teramoto cross-diffusion](biological-models.md) — Reading only. The displayed homogeneous-environment reduction omits the original environmental-potential terms. It is not equivalent to two independent scalar diffusion equations.
- [Gray–Scott spatial autocatalysis](biological-models.md) — Reading only. 1983 is the well-mixed CSTR source; Pearson 1993 is the spatial pattern reference. Spot division does not by itself demonstrate cell division or a linear Turing instability.
- [Aliev–Panfilov cardiac excitation](biological-models.md) — Reading only. Monodomain/bidomain tissue models add conductivity tensors and, for bidomain, an extracellular elliptic constraint. They are not automatically included by this two-variable model.
- [Repressilator mRNA–protein network](biological-models.md) — Reading only. The six-variable form is distinct from a reduced three-protein oscillator; oscillations are parameter-dependent.
- [Genetic toggle switch](biological-models.md) — Reading only. Bistability is not guaranteed for arbitrary Hill exponents or production rates. Induction, mRNA dynamics and noise are additional model choices.

## Numerical method inventory

Named numerical methods and building blocks with a reading chapter. Aliases count once; RK stages, dimensions, parameter combinations, mesh layouts and theoretical conditions do not add methods. A family and a separately explained algorithm may both appear. Not a count of mutually exclusive end-to-end solvers.

79 entries have scoped local examples; 6 are reading-only. Reconstruction limiters, preconditioners and coupling operators are building blocks, not complete PDE solvers. Mesh layouts, CFL conditions and theorems are not counted as numerical methods.

### Spatial discretization

- [Forward spatial difference](stability.md) — Local example.
- [Backward spatial difference](stability.md) — Local example.
- [Centered spatial difference](stability.md) — Local example.
- [Upwind finite differences](stability.md) — Local example.
- [Lax–Friedrichs](stability.md) — Local example.
- [Lax–Wendroff](stability.md) — Local example.
- [Godunov-type finite volumes](benchmarks.md) — Local example.
- [MUSCL reconstruction](benchmarks.md) — Local example.
- [WENO5-JS](benchmarks.md) — Local example.
- [Discontinuous Galerkin / Legendre](benchmarks.md) — Local example.
- [Fourier differentiation and evolution](benchmarks.md) — Local example.
- [Cubic-Hermite CIP](cip.md) — Local example.
- [Continuous P1 Galerkin FEM](fem.md) — Local example.

### Riemann fluxes & corrections

- [Rusanov / local Lax–Friedrichs flux](benchmarks.md) — Local example.
- [HLL](benchmarks.md) — Local example.
- [HLLC](benchmarks.md) — Local example.
- [Roe](benchmarks.md) — Local example.
- [HLLE / Einfeldt wave speeds](benchmarks.md) — Local example.
- [Acoustic Roe entropy correction](advanced.md) — Local example.
- [Rotated-hybrid Riemann solver](advanced.md) — Reading only.

### Limiters & admissibility

- [Minmod](limiters.md) — Local example.
- [Superbee](limiters.md) — Local example.
- [Monotonized central / MC](limiters.md) — Local example.
- [Van Leer limiter](limiters.md) — Local example.
- [Clipped Van Albada limiter](limiters.md) — Local example.
- [TVB modified minmod](advanced-limiters.md) — Local example.
- [Mean-preserving positive-state scaling](advanced-limiters.md) — Local example. Reconstruction building block; no full Euler-update positivity guarantee.

### Time integration

- [Forward Euler](time-integration.md) — Local example.
- [Backward Euler](time-integration.md) — Local example.
- [Heun / SSPRK(2,2)](time-integration.md) — Local example.
- [Explicit midpoint RK2](time-integration.md) — Local example.
- [Ralston RK2](time-integration.md) — Local example.
- [Kutta RK3](time-integration.md) — Local example.
- [SSPRK(3,3)](time-integration.md) — Local example.
- [SSPRK(4,3)](time-integration.md) — Local example.
- [Classical RK4](time-integration.md) — Local example.
- [SSPRK(5,4)](time-integration.md) — Local example.
- [Implicit midpoint](time-integration.md) — Local example.
- [Two-step leapfrog](time-integration.md) — Local example.
- [Crank–Nicolson](elliptic.md) — Local example.
- [BDF2](stiff-integration.md) — Local example.
- [L-stable SDIRK2](stiff-integration.md) — Local example.
- [IMEX Euler](stiff-integration.md) — Local example.
- [Adaptive SDIRK2 / step doubling](stiff-integration.md) — Local example.
- [Symplectic Euler](symplectic.md) — Local example.
- [Velocity Verlet / particle leapfrog](symplectic.md) — Local example.
- [Yoshida fourth-order composition](symplectic.md) — Local example.

### Linear & nonlinear solvers

- [Thomas tridiagonal elimination](elliptic.md) — Local example.
- [Jacobi iteration](elliptic.md) — Local example.
- [Gauss–Seidel iteration](elliptic.md) — Local example.
- [Successive over-relaxation / SOR](elliptic.md) — Local example.
- [Conjugate gradients](elliptic.md) — Local example.
- [Red-black Gauss–Seidel](elliptic.md) — Local example.
- [Geometric multigrid V-cycle](elliptic.md) — Local example.
- [Restarted GMRES](sparse-nonlinear.md) — Local example.
- [BiCGSTAB](sparse-nonlinear.md) — Local example.
- [Jacobi / diagonal preconditioning](sparse-nonlinear.md) — Local example.
- [Unpivoted ILU(0)](sparse-nonlinear.md) — Local example.
- [Armijo-damped Newton](sparse-nonlinear.md) — Local example.
- [Newton–Krylov with assembled Jacobian](sparse-nonlinear.md) — Local example.

### Coupling, constraints & particles

- [Dual time stepping](advanced.md) — Local example.
- [Scalar residual distribution](advanced.md) — Local example. 1D P1 upwind equivalent, not multidimensional Euler RD.
- [Low-Mach PDE preconditioning](advanced.md) — Reading only.
- [Constrained transport / CT](mhd.md) — Local example.
- [GLM divergence cleaning](mhd.md) — Local example.
- [MAC pressure projection](incompressible.md) — Local example.
- [D2Q9–BGK collision and streaming](lattice-boltzmann.md) — Local example.
- [Guo forcing](lattice-boltzmann.md) — Local example.
- [Half-way bounce-back](lattice-boltzmann.md) — Local example.
- [First-order hyperbolic diffusion baseline](hyperbolic-diffusion.md) — Local example.
- [SPH kernel reconstruction](particles-sph.md) — Local example.
- [ALE uniform-state / geometric-conservation model](ale.md) — Local example. Moving-volume scalar check; no complete ALE Euler solver.
- [Godunov SPH / GSPH](gsph.md) — Reading only.

### Particle fields & gravity

- [Cloud-in-cell assignment and interpolation](particle-gravity.md) — Local example.
- [FFT particle–mesh forces](particle-gravity.md) — Local example.
- [Barnes–Hut octree](particle-gravity.md) — Local example.
- [Monopole and second-moment expansion](particle-gravity.md) — Local example.
- [Isolated doubled-grid FFT convolution](gravity-boundaries.md) — Local example.
- [Horizontal-periodic slab Green-function FFT](gravity-boundaries.md) — Local example.
- [P³M short-range correction](particle-gravity.md) — Reading only.
- [TreePM force splitting](particle-gravity.md) — Reading only.
- [Fast multipole translations](particle-gravity.md) — Reading only.

### Additional formulations

- [Original Cartesian KEEP split flux](keep.md) — Local example.

### Element bases & approximation

- [Legendre modal basis / orthonormal scaling](basis-functions.md) — Local example. Reference-element tabulation, derivatives, projection and affine mass/stiffness matrices.
- [Lagrange nodal basis / GLL collocation](basis-functions.md) — Local example. Interval cardinal functions, modal transforms, exact versus quadrature mass, and P1/P2 triangle shapes.

## Papers versus all sources

Unique bibliographic publications classified as journal articles or conference papers, deduplicated by DOI or author/title/year. Includes reviews, translations and explicitly labeled accepted papers; not a claim that every full text was inspected. Books, chapters, reports, preprints and documentation are separate.

Unique cataloged works across all publication types. An original publication and a later translation are separate works; duplicate DOI records are not. NASA case links in prose are not catalog records.

- 124 journal-article records, including reviews, translations and explicitly labeled accepted papers.
- 3 conference papers.
- 7 books.
- 2 book chapters.
- 3 technical/teaching reports.
- 9 other records, including documentation and a separately identified preprint.

A duplicate Cockburn–Shu 1989 record was merged. Burgers 1948 is classified as a book chapter. The former 146-record total included that duplicate; subsequent source additions are reflected in the current unique-work totals above. An original paper and a separately published translation remain separate works. The bibliography does not claim that every full text has been inspected; source notes preserve the inspection status.

## Reproduction

The named registry is `catalog/coverage.json`; biological entries and publication types come from their respective catalogs. `python scripts/build_coverage.py` checks unique publication identities and local reading links, then generates the counts and this inventory. The website build runs that audit before rendering. Parameter choices, time frames, repeated equations in prose and test function counts do not increase these totals.

[Download the counted inventory and source hashes](figures/site-coverage.json). Browse the [reference catalog](references.md), [equation gallery](equation-gallery.md), [biological survey](biological-models.md) or [implementation roadmap](roadmap.md).
