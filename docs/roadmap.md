# Implementation roadmap

## Current priority: shock methods

Shock-method expansion takes priority over relativity and new subject areas.
The first published stage adds [limited parabolic FV, characteristics, WENO-Z and an AUSM baseline](reconstruction.md), [Roe's Property U with numerical counterexamples](advanced.md#roes-property-u), and [controlled planar odd–even diagnostics](carbuncle.md). Original PPM wave tracing/contact steepening/shock flattening, AUSM+/AUSM+-up, blunt-body carbuncle tests and rotated-hybrid schemes remain the next steps in this priority group. They are not silently marked complete by the scoped experiments.

## First edition: executable foundations

Version 0.1.0 brings together an educational Python library, a historical atlas,
English method notes, a bibliographic catalog, comparison figures, and automated
numerical checks. The repository is the first-edition distribution; the reading
guide in the [README](../README.md) connects the material.

The NASA case catalog includes computed 15-degree wedge baselines and remaining
implementation candidates. Rotated-solver notes still describe future work;
catalog inclusion alone does not indicate an implemented simulation.

## Next verification work

- Strengthen links between run manifests and saved arrays; report grid and time refinement together with wall-clock costs.
- Add finite-volume cell-average initialization and integrated references, characteristic WENO, positivity limiters, and stronger shock tests.
- Add exact shallow-water and isothermal references; treat topography, well balancing, and dry beds as separate implementation steps.
- Extend the new HLLD standard tests with UCT-HLLD, stronger-field cases and external reference-code comparisons.
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

## Shock gallery: NASA wedges and a forward-facing step

Computed the NASA 15-degree wedges at Mach 2.0 and 2.5 with independent
body-fitted first-order HLL / SSPRK2 finite volumes, two grids and oblique-shock
references. Added the classical Mach-3 forward step on a 240 × 80 blocked-cell
mesh, 81 saved states to t = 4 and an MP4, bringing the movie catalog to five.
The step uses plain reflecting corners, not the entropy/enthalpy reset of the
original PPM comparison. These are educational inviscid baselines, not Wind-US
outputs or viscous experimental validations. [Setup and limits](nasa-2d.md).
Mach-5 shock/boundary-layer interaction, Mach-7 viscous ramps and the existing
transonic diffuser/airfoil cases remain implementation candidates.

## Web edition

[The public web edition](https://koyamahr.github.io/numerical-methods-atlas/)
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

[The 2D Double Mach Reflection baseline](double-mach.md) now computes an actual Mach-10 interaction with first-order HLL and SSPRK2. Higher-order reconstruction, full grid refinement, and resolution of the fine wall jet remain future work. The NASA wedge baselines were added later; the cataloged viscous and turbulence cases remain unimplemented. [Blunt-body carbuncle comparisons beyond the new planar diagnostic](carbuncle.md), a complete SPH fluid solver, unstructured flow fluxes, and a complete ALE Euler solver also remain future work. [The Roe memorial](roe-memorial.md) is sourced from official university records.

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
the measured shear viscosity. These educational additions are included in the
published atlas at https://koyamahr.github.io/numerical-methods-atlas/ . Their
implementation limits and remaining verification work are stated in each chapter.

## Authorized next work

- **Added — Roe's Property U:** original four conditions, parameter-vector derivation, jump/consistency/eigenbasis checks and an expansion-discontinuity counterexample; see [the explanation](advanced.md#roes-property-u).
- Inutsuka's GSPH: Gaussian convolution and specific-volume reconstruction,
  oriented pair Riemann states, a matched conservative energy update, and
  smooth/contact/shock-tube verification before variable smoothing lengths.
  The Iwasaki–Inutsuka GSPMHD extension is a later, separately verified stage;
  see the [source notes and staged plan](gsph.md).
- Relativistic hydrodynamics is a source-based extension plan: SRHD recovery
  and characteristic tests before SRMHD, fixed-metric GR, and independently
  verified Einstein–matter coupling. Radiation and SRGSPH are separate branches;
  see the [development review checked in November 2026](relativistic-hydrodynamics.md).
- **First stage added:** limited parabolic FV, conservative characteristics and FD WENO-Z with Sod/contact/Shu–Osher comparisons. Complete original PPM features remain pending; see [the scope](reconstruction.md).
- AUSM common-sound-speed/cubic-pressure baseline added; AUSM+ and AUSM+-up are planned separately.
- **Completed web stage:** HLLD with Brio–Wu, Alfvén-wave refinement and weak field-loop CT-Contact/GLM comparisons; see the [MHD tests](#/mhd-tests).
- **Planned — electromagnetic FDTD (finite-difference time-domain):** Yee-grid
  placement, leapfrog Maxwell updates, CFL limits and numerical dispersion;
  start with vacuum-wave and conducting-cavity tests, then absorbing boundaries
  and PML reflection checks. Implementation and dedicated verification are pending.
- **Planned — plasma PIC (Particle-in-Cell):** start with electrostatic
  particle–Poisson coupling, then electromagnetic particle–Maxwell coupling.
  Cover particle shapes, deposition/gather, Boris pushing, charge-conserving
  current deposition and Gauss-law diagnostics. Plan plasma-oscillation,
  two-stream and Landau-damping tests, with energy, noise and grid/time/particle
  refinement checks. Existing gravitational PM is a separate scoped example.
  The [WarpX PIC theory notes](https://warpx.readthedocs.io/en/25.11/theory/pic.html)
  are a starting reference; no plasma PIC solver is implemented here yet.
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

## Planned machine-learning numerics

**Status: revision candidates; the dedicated explanations, implementations and
verification below have not been added.** Start with stable function evaluation,
automatic differentiation and optimization as shared foundations for Volume 1.
Scientific machine-learning applications are later candidates. These plans do
not add to implemented-method counts, and no release date is assigned.

Mixed-precision arithmetic and the design of low-precision GPU computations are
outside the current scope. Ordinary floating-point roundoff and stable function
evaluation remain part of the shared foundations.

- [ ] **Softmax and log-sum-exp:** maximum shifting, log-softmax, exponential
  overflow and underflow. Plan checks for large inputs, invariance under constant
  shifts, probability sums and derivative consistency. See the
  [SciPy softmax notes](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.softmax.html).
- [ ] **Cross-entropy and stable loss evaluation:** compute directly from logits,
  connect to log-sum-exp, and cover sigmoid and binary cross-entropy. Check finite
  values and analytic gradients for extreme inputs. Start from the
  [PyTorch cross-entropy documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html).
- [ ] **Automatic differentiation and backpropagation:** forward/reverse modes,
  the chain rule, Jacobian–vector products (JVPs), vector–Jacobian products (VJPs)
  and Hessian–vector products. Distinguish symbolic and finite-difference
  derivatives; cover roundoff, nondifferentiable points and intermediate-storage
  costs. Use the [JAX autodiff guide](https://docs.jax.dev/en/latest/301/index.html)
  and plan analytic/directional derivative comparisons.
- [ ] **Implicit differentiation, adjoints and differentiable solvers:**
  sensitivities through linear solves, converged nonlinear systems and time
  evolution. Distinguish unrolling iterations from differentiating the defining
  equations; state Jacobian invertibility, solve tolerances and gradient checks.
  The [implicit-differentiation paper](https://papers.neurips.cc/paper_files/paper/2022/file/228b9279ecf9bbafe582406850c57115-Paper-Conference.pdf)
  is a starting reference.
- [ ] **Machine-learning optimization:** gradient
  descent/SGD, momentum, Adam, L-BFGS and Gauss–Newton/Levenberg–Marquardt.
  Distinguish objective minimization from the existing Newton root solves;
  compare scaling, conditioning, learning rates and gradient norms.
  Do not claim universal convergence or a universal ranking.
- [ ] **Application candidate — PINNs and inverse problems:** separate PDE,
  initial/boundary and observation losses; compare with conventional finite
  differences/FEM using shared error measures. A lower training loss alone is
  not a PDE-error guarantee. See the [authors' PINN notes](https://maziarraissi.github.io/PINNs/)
  and [failure-mode study](https://papers.nips.cc/paper_files/paper/2021/hash/df438e5206f31600e6ae4af72f2725f1-Abstract.html).
- [ ] **Application candidate — neural operators/Fourier neural operators:**
  connect learned function-to-solution maps with the existing Fourier bases and
  spectral methods. Plan separate checks of out-of-distribution behavior, grid
  changes, discretization and aliasing errors; changing grid resolution alone
  does not guarantee accuracy. See the
  [neural-operator paper](https://www.jmlr.org/papers/volume24/21-1524/21-1524.pdf).
- [ ] **Application candidate — symbolic regression and equation discovery:**
  search for explicit expressions from data or learned models, separately from
  automatic derivative evaluation. Assess noise, dimensions/symmetries,
  expression complexity and independent-data checks. Consider the study on
  [extracting symbolic models from deep learning](https://proceedings.neurips.cc/paper_files/paper/2020/hash/c9f2f917078bd2db12f23c3b413d9cba-Abstract.html).

## Planned quantum chemistry and DFT

**Status: planned; implementation and the dedicated literature review have not
started. No release date is assigned.** This is a separate electronic-structure
branch, with the following development checklist. None of these planned items
adds to the current implemented-method or equation counts.

- [ ] **Schrödinger eigenproblems:** begin with one-electron models, including
  the harmonic oscillator and hydrogenic radial problem. Compare finite
  differences, finite elements and spectral discretization, recording boundary,
  domain-truncation and resolution errors separately.
- [ ] **Electronic-structure bases:** introduce atomic orbitals, Gaussian and
  Slater functions, plane waves and real-space grids. Include overlap matrices
  and generalized eigenproblems. Connect to the existing
  [element-basis notebook](basis-functions.md), while distinguishing its
  mesh-local polynomial examples from molecular orbital basis sets.
- [ ] **Coulomb and Hartree potentials:** connect electronic charge density to
  Poisson solvers. State electrostatic units, charge signs, isolated/periodic
  boundaries, zero modes and self-interaction conventions explicitly; do not
  silently reuse gravitational signs or normalizations.
- [ ] **Hartree–Fock:** develop a small closed-shell molecular example with
  matrix assembly, a generalized eigenvalue solve and a self-consistent field
  loop. Verify the required integral machinery before presenting energies.
- [ ] **Kohn–Sham density functional theory:** explain the density, effective
  potential and exchange–correlation approximation. Start with an explicitly
  identified LDA model; GGA and later functionals require their own verification.
- [ ] **SCF iteration and mixing:** compare damping, density/potential mixing
  and Pulay/DIIS acceleration. Report electron-number checks, eigenproblem and
  SCF residuals, energy changes and explicit nonconvergence.
- [ ] **Verification examples:** use one-electron references and small atoms or
  molecules, with basis/grid refinement and independent reference-code checks.
  Separate discretization error, SCF tolerance and physical-model differences.

The intended first milestones are a verified one-electron eigensolver, followed
by a minimal-basis Hartree–Fock example, then a clearly scoped Kohn–Sham DFT
example. Periodic materials, pseudopotentials, spin-dependent extensions and
post-Hartree–Fock correlation are later branches, rather than promises of the
first implementation. This plan does not change the current priority of the
fluid-method work above, and AMR remains deferred.

The next editorial priority is to connect shared equations to multiple
verified discretizations, cost/error evidence and explicit failure cases,
while retaining separate labels for surveys, prototypes and verified models.

Reference-element basis functions now have an executable [Legendre/nodal notebook](basis-functions.md), including exact and quadrature mass, affine metric scaling and triangular P2 shapes. Curved-element metrics, orthogonal simplex modes and higher-order FEM/DG fluid assembly remain separate extensions.


## Verified Euler and MHD comparisons

Added 2D primitive MUSCL with minmod/MC, exact-cell-average smooth refinement, NASA wedge first/second-order comparisons on two grids, and three forward-step reconstruction clips. The [comparison page](#/flow-comparison) fixes HLL/SSPRK2 and exposes diagnostics. Added full-vector HLLD, Brio–Wu, four-grid circular Alfvén waves and weak magnetic loops on two grids with HLLE/HLLD × CT-Contact/GLM. Source/artifact hashes, conservative arrays, positivity/retry/fallback diagnostics and bilingual scope notes accompany the [MHD page](#/mhd-tests). These complete the agreed three web stages; books remain deferred.
