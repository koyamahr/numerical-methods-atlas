# Historical atlas

Dates refer to original publication years, with translations, reprints, and
online publication dates distinguished where relevant. This atlas offers a
reading path through representative sources. It does not settle every claim
of invention or priority. The [reference catalog](references.md) records the
relationship between each source and the implementation, including open questions.

## Classical foundations: equations, differences, and iteration

Begin with forward, backward, and centered differences, Euler time integration,
Fourier expansions, heat conduction, and the Laplace and Poisson equations.
Distinguish boundary values from boundary fluxes before introducing Dirichlet,
Neumann, and Robin conditions. The mathematical origins of these ideas precede
their later use in computational fluid dynamics.

## 1928: CFL and domains of dependence

Courant–Friedrichs–Lewy compares the continuous domain of dependence with the
reach of a discrete stencil. Vary `C=a Δt/Δx` in linear advection to distinguish
necessary conditions from sufficient ones.
[Original CFL paper](https://doi.org/10.1007/BF01448839),
[derivations and experiments](stability.md).

## 1939–1943: kinetic asymptotics and variational assembly

Chapman–Cowling's kinetic-theory book appeared in 1939; this is a book date,
not the invention date of the [Chapman–Enskog expansion](chapman-enskog.md).
[Courant (1943)](https://doi.org/10.1090/S0002-9904-1943-07818-4) connects
variational problems to piecewise representations. The [P1 FEM exhibit](fem.md)
implements independent sparse Poisson examples.

## 1947–1950: diffusion, implicit methods, and linear stability

Crank–Nicolson (1947); Thomas tridiagonal elimination, commonly cited to a 1949
report whose original text has not been inspected here; and stability analysis
in Charney–Fjørtoft–von Neumann's numerical forecasting work (1950).
The 1950 paper is historical context, rather than a claim that von Neumann
analysis originated in that paper alone. Connect the diffusion number
`r=ν Δt/Δx²` with A-stability, monotonicity, and implicit linear systems.
[Diffusion and linear solvers](elliptic.md).

[Burgers (1948)](https://doi.org/10.1016/S0065-2156(08)70100-5) supplies a
parallel nonlinear model branch. The [equation gallery](equation-gallery.md)
uses the inviscid shock/fan problem, rather than reproducing its turbulence analysis.

## 1954–1961: Lax, Godunov, and conservation form

Lax (1954), Lax–Richtmyer (1956), Godunov (1959), Lax–Wendroff (1960), and
Rusanov (1961) lead into weak solutions, numerical fluxes, shock speeds,
numerical viscosity, and dispersion. The Lax–Richtmyer linear convergence
theorem and Lax–Wendroff-type results about weak limits of nonlinear
conservative approximations have different hypotheses.
Here, `method="godunov"` denotes a Godunov-type finite-volume method with
approximate Riemann fluxes, rather than a complete reproduction of the
original exact-flux algorithm.

[BGK (1954)](https://doi.org/10.1103/PhysRev.94.511) provides a kinetic
relaxation model. [Lighthill–Whitham (1955)](https://doi.org/10.1098/rspa.1955.0089)
and [Richards (1956)](https://doi.org/10.1287/opre.4.1.42) connect conservation
laws to traffic waves. These separate branches meet in the gallery through
explicit equations and references, not a single invention chronology.

## 1961–1977: relaxation, multigrid, and local and global bases

Fedorenko (1961), Reed–Hill (1973), Gottlieb–Orszag (1977), and Brandt (1977).
Split Poisson iteration into smoothing of high-frequency errors and coarse-grid
correction of smooth errors. DG uses elementwise polynomials joined by boundary
fluxes; spectral methods use global bases. Earlier Galerkin and Fourier ideas
provide the mathematical background to these developments.
[Poisson and multigrid](elliptic.md), `numart.advection.dg_advection`.

[Chorin (1968)](https://doi.org/10.1090/S0025-5718-1968-0242392-2)
leads to [incompressible projection](incompressible.md).
[Alexander (1977)](https://doi.org/10.1137/0714068) supplies the
[SDIRK branch](stiff-integration.md); source treatment and adaptive error control
remain distinct from a method's linear stability function.

## 1978–1983: shared benchmarks and high-resolution fluxes

Sod (1978), van Leer's MUSCL (1979), Orszag–Tang (1979), Roe (1981), and
Harten–Lax–van Leer (1983). Compare contact and acoustic-wave resolution on the
same Sod problem. The first-edition MUSCL implementation uses minmod and the
method of lines; van Leer's original Lagrangian/remap construction is different.
The original incompressible Orszag–Tang study and the normalization of today's
compressible test are also distinguished.
[Benchmark definitions](benchmarks.md), [MHD](mhd.md).

## 1984–1989: TVD slopes and TVB extrema relaxation

[Sweby (1984)](https://doi.org/10.1137/0721062) organizes scalar flux-limiter bounds. [Cockburn–Shu (1989)](https://doi.org/10.1090/S0025-5718-1989-0983311-4) develops the TVB RKDG framework. Compare five [slope limiters](limiters.md), then inspect the separate [TVB and positive-state scaling](advanced-limiters.md) building blocks. The latter also links the positivity framework of Zhang–Shu (2010), with its required flux, quadrature, CFL, and SSP conditions.

## 1985–1991: cubic profiles and transported gradients

[Takewaki–Nishiguchi–Yabe (1985)](https://doi.org/10.1016/0021-9991(85)90085-3) and [Yabe–Aoki (1991)](https://doi.org/10.1016/0010-4655(91)90071-R) develop the CIP line of cubic value/gradient transport. The [CIP chapter](cip.md) computes a constant-speed scalar example and distinguishes later conservative and rational branches. Its constructed Hermite-field test separates low diffusion from a mass-conservation guarantee.

## 1987–1989: higher order, preconditioning, and magnetic constraints

ENO by Harten and colleagues (1987), Turkel's low-speed preconditioning (1987),
Einfeldt (1988), Evans–Hawley CT (1988), Shu–Osher (1988, 1989), and
Cockburn–Shu RKDG (1989). High-order interpolation alone does not ensure robust
shock capture. Entropy fixes and positivity require separate attention.
The Shu–Osher test combines a shock with a smooth density wave.

## 1991–1996: unsteady iteration, low densities, HLLC, and WENO

Einfeldt and colleagues (1991), Jameson (1991), Toro–Spruce–Speares (1994),
Liu–Osher–Chan (1994), and Jiang–Shu (1996). Study physical and pseudo-time,
low-density failure, contact restoration, and nonlinear WENO weights.
The origin of WENO in 1994 is distinguished from WENO5-JS (1996), which is the
variant implemented in this edition.
[Preconditioning and dual time stepping](advanced.md).

## 2000–2008: multidimensional robustness and constraints

Tóth (2000), Dedner and colleagues (2002), Abgrall's residual-distribution
review (2006), and Nishikawa–Kitamura (2008). Follow discrete CT/GLM operators,
conservative residual distribution, rotated-hybrid fluxes, and the carbuncle
instability. The 2006 date identifies the RD review, rather than the invention
of residual distribution.

[Inutsuka (2002)](https://doi.org/10.1006/jcph.2002.7053) adds a parallel
particle branch: convolution-based SPH evolution with pairwise Riemann
problems. The [GSPH chapter](gsph.md) distinguishes its 1994 precursor from
the detailed 2002 formulation and the later MHD extension by
[Iwasaki–Inutsuka (2011)](https://doi.org/10.1111/j.1365-2966.2011.19588.x).
These are source notes and planned fluid solvers, rather than the existing
static SPH reconstruction.

## 2001–2009: SSP inheritance and additional Runge–Kutta stages

[Gottlieb–Shu–Tadmor (2001)](https://doi.org/10.1137/S003614450036757X), [Spiteri–Ruuth (2002)](https://doi.org/10.1137/S0036142901389025), and [Gottlieb–Ketcheson–Shu (2009)](https://doi.org/10.1007/s10915-008-9239-z) distinguish scalar linear stability from conditional nonlinear stability inheritance. These are developments in the SSP branch, not the origin of Runge–Kutta methods. The [RK family chapter](runge-kutta.md) compares RK2 variants, RK4, and SSPRK(s,p), with actual nonlinear stages and refinement.

## Relativistic branch: 1972–2026

The [SRHD/GRHD/GRMHD review](relativistic-hydrodynamics.md) connects Wilson's
Kerr-background calculation (1972), exact SR Riemann solutions (1994), Valencia
(1997), local-frame solvers (1998), relativistic magnetic constraints, HARM
(2003), dynamical spacetime, and nonlinear primitive recovery. Later branches
include radiation, DG–FD hybrids, physical-state constraints, and GPU-oriented
merger codes. [SRGSPH (2026)](https://doi.org/10.1016/j.jcp.2025.114448) connects
back to Inutsuka's particle formulation. The review records source and
publication status as checked on 6 November 2026; it adds no relativistic solver.

## Toward modern verification and validation

The [NASA 2D case catalog](nasa-2d.md) introduces the distinction between
numerical verification and physical validation against experiments. Each
future exhibit should connect its original source, current data access point,
implementation status, and verification evidence.

## Moving meshes, particles, and temporal modes

The fixed-grid history has parallel branches. [Hirt, Amsden, and Cook (1974)](https://doi.org/10.1016/0021-9991(74)90051-5) provide a classical ALE framework; [Gingold and Monaghan (1977)](https://doi.org/10.1093/mnras/181.3.375) and [Lucy (1977)](https://doi.org/10.1086/112164) are independent early SPH sources. The new [ALE](ale.md), [particle](particles-sph.md), and [mesh](meshes.md) chapters connect their different representations of geometry and motion. The code implements small reconstruction and geometric-conservation examples, rather than those original flow calculations.

The [time integration chapter](time-integration.md) gives the two-step leapfrog recurrence and its computational root. Its discussion of time filtering points to a later modification by [Williams (2009)](https://doi.org/10.1175/2009MWR2724.1), without assigning the invention of leapfrog to that paper.

The [Double Mach Reflection exhibit](double-mach.md) adds a computed two-dimensional shock interaction. [Quirk (1994)](https://doi.org/10.1002/fld.1650180603) and [Pandolfi and D’Ambrosio (2001)](https://doi.org/10.1006/jcph.2000.6652) lead into the separate [carbuncle reading notes](carbuncle.md). Finally, [Remembering Philip L. Roe](roe-memorial.md) records the university’s 2026 memorial and returns to his 1981 contribution.

## Particle fields and canonical time maps

[Hockney’s P³M account (1981)](https://www.ccp5.ac.uk/wp-content/uploads/2023/03/CCP5_Newsletter_1981_06_01.pdf), [Barnes–Hut (1986)](https://doi.org/10.1038/324446a0), and [Greengard–Rokhlin (1987)](https://doi.org/10.1016/0021-9991(87)90140-9) connect mesh, tree, and expansion-based field calculations. [Yoshida (1990)](https://doi.org/10.1016/0375-9601(90)90092-3) provides a route to high-order symplectic compositions. The new [gravity](particle-gravity.md) and [Hamiltonian-map](symplectic.md) chapters make their different roles explicit. [Koyama–Ostriker (2009)](https://doi.org/10.1088/0004-637X/693/2/1316) supplies the disk-potential FFT reference in the [boundary-kernel chapter](gravity-boundaries.md).

## Smooth-flow structure and honest test selection

[Kuya, Totani, and Kawai (2018)](https://doi.org/10.1016/j.jcp.2018.08.058) introduce the KEEP line of compressible-flow discretizations. The [KEEP chapter](keep.md) implements the original second-order Cartesian form and distinguishes later entropy, pressure-equilibrium, and temporal extensions. Its smooth-vortex refinement and [saved-state movie](movies.md) are separate from shock-capturing benchmarks; neither kinetic-energy consistency nor a visually smooth movie is a universal stability guarantee.

## Parallel solver branches: 1986–2010

[GMRES (1986)](https://doi.org/10.1137/0907058) and
[BiCGSTAB (1992)](https://doi.org/10.1137/0913035) provide nonsymmetric
[sparse-system solvers](sparse-nonlinear.md).
[Qian et al. (1992)](https://doi.org/10.1209/0295-5075/17/6/001) and
[Guo et al. (2002)](https://doi.org/10.1103/PhysRevE.65.046308) lead to the
[lattice-BGK and forcing exhibits](lattice-boltzmann.md).
[Nishikawa (2007)](https://doi.org/10.1016/j.jcp.2007.07.029) develops the
[first-order hyperbolic diffusion system](hyperbolic-diffusion.md), with an
advection–diffusion extension published in 2010. The reading room distinguishes
that system's original second-order RD scheme from our first-order FV baseline.

## Biological and geophysical branches

The [biological equation survey](biological-models.md) follows population
growth through Lotka/Volterra, age structure and SIR, then Fisher fronts,
Turing morphogenesis, excitable membranes, chemotaxis, stochastic reaction
networks and synthetic gene circuits. Original, translated and reduced model
forms have separate source notes. All 22 biological entries are survey-only.

[Arakawa–Lamb (1977)](https://doi.org/10.1016/B978-0-12-460817-7.50009-4)
connects variable placement to geophysical waves. The [A/B/C chapter](geophysical-grids.md)
adds independent centered f-plane symbol comparisons; the horizontal grid
classification is separate from vertical staggering and nonlinear invariant
conservation.
