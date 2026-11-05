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

## Third expansion: Hamiltonian maps and particle gravity

Added fixed-step canonical maps and a notebook for harmonic/quartic oscillators; periodic 3D CIC/FFT PM; an isolated softened octree with monopole/full second moments; isolated doubled-grid convolution; and sampled/continuum slab Green-transform options. Figures have dedicated source manifests. P³M corrections, a coupled TreePM solver, FMM translations, cosmological expansion, shear-periodic remapping, and a gravity-coupled SPH fluid integrator remain future work.

## Fourth expansion: nonsteady movies and smooth KEEP

Added saved-state output that leaves solver time steps unchanged, four numerical movies with frame inspection and MP4 export, and the original second-order Cartesian KEEP flux with smooth-vortex refinement. Steady fields retain still images. The KEEP implementation excludes shock stabilization, later PEP/redefined variants, high-order curvilinear forms, and the 3D TGV/LES examples discussed in the reading guide.

## Fifth expansion: limiters, RK families, and CIP

Added selectable MUSCL slopes, TVB modified-minmod and positive-reconstruction building blocks, nine explicit RK tableaus with nonlinear stage verification, twelve oscillator methods, and original cubic-Hermite CIP with a conservation counterexample. Full Euler-update positivity is still a separate extension.

## Sixth expansion: equations, sparse systems and kinetic transport

Added nine saved-profile cases across seven equation families, including
Burgers and LWR traffic. Exact scalar cell averages, point-sampled Sod references,
and missing shallow-water/isothermal overlays are explicitly distinguished.

The new [continuous P1 FEM](fem.md), [sparse/nonlinear solvers](sparse-nonlinear.md),
[stiff ODE integrators](stiff-integration.md), [periodic MAC projection](incompressible.md),
[D2Q9–BGK](lattice-boltzmann.md), and [first-order hyperbolic diffusion baseline](hyperbolic-diffusion.md)
have dedicated numerical checks, figures and source-hashed manifests.
[Chapman–Enskog expansion](chapman-enskog.md) is a formal derivation linked to
the measured shear viscosity. These local additions are prepared for review;
they have not been deployed by this expansion.

## Authorized next work

- Inutsuka's GSPH: Gaussian convolution and specific-volume reconstruction,
  oriented pair Riemann states, a matched conservative energy update, and
  smooth/contact/shock-tube verification before variable smoothing lengths.
  The Iwasaki–Inutsuka GSPMHD extension is a later, separately verified stage;
  see the [source notes and staged plan](gsph.md).
- Relativistic hydrodynamics is a source-based extension plan: SRHD recovery
  and characteristic tests before SRMHD, fixed-metric GR, and independently
  verified Einstein–matter coupling. Radiation and SRGSPH are separate branches;
  see the [development review checked in November 2026](relativistic-hydrodynamics.md).
- PPM, characteristic reconstruction, and WENO-Z with controlled shock/contact comparisons.
- HLLD, Brio–Wu, Alfvén-wave and field-loop verification, with explicit CT/GLM scope.
- Stiff integration: higher-order IMEX, embedded DIRK, variable-step BDF and operator splitting beyond the implemented BE/BDF2/SDIRK2/IMEX-Euler models.
- Sparse/nonlinear solvers: matrix-free Newton–Krylov, robust reorderings/fill, flexible preconditioning and broader nonlinear benchmarks beyond the implemented fixed-right GMRES/BiCGSTAB and ILU(0).
- Viscous/incompressible flow: wall projection, SIMPLE/PISO, cavity and cylinder-wake validation beyond periodic Taylor–Green.
- FEM: mixed velocity–pressure pairs, inf–sup checks, curved/irregular meshes and natural/mixed boundary assembly.
- LBM: MRT/TRT/cumulant collisions, thermal and multiphase models beyond low-Mach isothermal D2Q9–BGK.
- Hyperbolic diffusion: full second-order RD, anisotropy and unified advection/viscous systems beyond the periodic first-order baseline.

AMR is deferred at the author’s request; it is not part of this expansion.

## Biological and geophysical survey additions

[The biological catalog](biological-models.md) contains 22 survey-only model
families, with equations, source conventions and proposed verification.
A practical implementation sequence is logistic/SIR and enzyme kinetics,
then Fisher fronts, FitzHugh–Nagumo, Schnakenberg and Keller–Segel, with a
birth–death SSA as a separate stochastic branch. No biological solver or
biological validation is added by the survey.

[Arakawa A/B/C](geophysical-grids.md) has variable-location diagrams and
tested semi-discrete f-plane Fourier symbols. D/E, vertical staggering,
nonlinear potential-vorticity schemes, Kelvin/Rossby waves and coastlines
remain additional work. This is not a full geophysical dynamical core.

Quantum chemistry and electronic-structure methods could form an independent
future branch: Schrödinger eigenproblems, Hartree–Fock, Kohn–Sham DFT, basis
sets and self-consistent iteration. This is a scope idea, without a completed
literature survey or an electronic-structure implementation in this edition.

The next editorial priority is to connect shared equations to multiple
verified discretizations, cost/error evidence and explicit failure cases,
while retaining separate labels for surveys, prototypes and verified models.
