# NASA 2D verification and validation case catalog

Start with the official [NPARC Verification and Validation Archive](https://www.grc.nasa.gov/WWW/wind/valid/archive.html),
[CFL3D test cases](https://nasa.github.io/CFL3D/Cfl3dv6/cfl3dv6_testcases.html),
and [Turbulence Modeling Resource](https://tmbwg.github.io/turbmodels/).
NASA's [TMR information page](https://www.nasa.gov/nasa-turbulence-modeling-resource/)
describes the resource's move to GitHub in February 2026.
The entries below are **cataloged candidates**. This repository does not yet
contain implementations or reproduction results for the NASA cases listed below.
A separate classical [Double Mach Reflection baseline](double-mach.md) is now computed.

## Starting with Euler and analytical references

- **15° wedge, Mach 2.0:** oblique shock, wall pressure, grid dependence, and Roe/HLLE comparisons. [NASA case](https://www.grc.nasa.gov/WWW/wind/valid/wedgeM2/wedgeM2.html).
- **15° wedge, Mach 2.5:** compare shock angle and downstream states with theory. Pair this compression case with the expansion corner below. Find its entry through the [official archive](https://www.grc.nasa.gov/WWW/wind/valid/archive.html).
- **Prandtl–Meyer 15° expansion, Mach 2.5:** expansion-fan structure and analytical Mach/pressure relations. [Official archive](https://www.grc.nasa.gov/WWW/wind/valid/archive.html).

## Laminar flow, unsteadiness, and pressure Poisson problems

- **Driven cavity:** centerline velocities, primary vortex, and corner vortices in a square. NASA uses low-Mach calculations to approximate incompressible flow and compares with Ghia and colleagues. [NASA case](https://www.grc.nasa.gov/WWW/wind/valid/cavity/cavity.html).
- **Blasius laminar flat plate:** boundary-layer profiles, skin friction, and wall-normal mesh resolution. [NASA case](https://www.grc.nasa.gov/www/wind/valid/fplam/fplam.html).
- **Unsteady laminar circular cylinder:** vortex shedding, drag/lift histories, and temporal accuracy; a candidate after dual time stepping. [NASA case](https://www.grc.nasa.gov/WWW/wind/valid/lamcyl/lam_cyl.html).

## Turbulence models, separation, and airfoils

- **Zero-pressure-gradient turbulent flat plate:** skin friction, turbulence-model implementation verification, and grid convergence. [TMR verification](https://tmbwg.github.io/turbmodels/flatplate.html).
- **2D bump-in-channel:** curved-wall pressure and friction, with comparisons between codes using the same turbulence model. [TMR verification](https://tmbwg.github.io/turbmodels/bump.html).
- **Driver–Seegmiller backward-facing step:** separation, reattachment, Cp/Cf, and velocity profiles. Fix the dataset version, including Reynolds-number definitions and corrections. [TMR validation](https://tmbwg.github.io/turbmodels/backstep_val.html), [NPARC](https://www.grc.nasa.gov/WWW/wind/valid/backstep/backstep.html).
- **Sajben transonic diffuser:** internal shocks, back pressure, and shock/boundary-layer interaction. [NASA case](https://www.grc.nasa.gov/WWW/wind/valid/transdif/transdif.html).
- **RAE 2822 transonic airfoil:** surface Cp, shocks, and boundary layers. State the case number and corrected Mach number and angle of attack. [NASA case](https://www.grc.nasa.gov/WWW/wind/valid/raetaf/raetaf.html).
- **NACA 0012:** surface pressure, lift/drag, and sensitivity to grids, far-field boundaries, and turbulence models. [TMR validation](https://tmbwg.github.io/turbmodels/naca0012_val.html).
- **NACA 4412 trailing-edge separation:** adverse pressure gradients and trailing-edge separation. [TMR validation](https://tmbwg.github.io/turbmodels/naca4412sep_val.html).
- **NASA wall-mounted hump:** wall-induced separation and reattachment. Record the applicability of 2D calculations to experiments containing three-dimensional effects. [TMR validation](https://tmbwg.github.io/turbmodels/nasahump_val.html).
- **2D mixing layer:** free-shear-layer growth, velocity, and turbulence quantities. [TMR validation](https://tmbwg.github.io/turbmodels/delvilleshear_val.html).
- **2D airfoil near-wake:** wake velocity deficit and recovery. [TMR validation](https://tmbwg.github.io/turbmodels/airfoilwake_val.html).

## Other classical 2D benchmarks

Double Mach Reflection, the Mach 3 forward-facing step, 2D Riemann
configurations, the isentropic vortex, and odd-even shock/carbuncle tests are
also useful flux demonstrations. The first two have a representative source
in [Woodward–Colella (1984)](https://doi.org/10.1016/0021-9991(84)90142-6).
[Our Double Mach Reflection exhibit](double-mach.md) is an implemented first-order
HLL baseline; the step and other tests in this paragraph remain future work.
See the separate [carbuncle notes](carbuncle.md) for the required stability comparisons.
Do not label all of these as NASA-originated problems. ONERA M6 is a 3D wing;
axisymmetric bump and jet cases are also different from planar 2D cases and
are excluded from the main list.

## Information to fix for each implementation

Record the original source, case number, geometry, nondimensionalization,
Mach/Reynolds numbers, angle of attack, wall/far-field/inlet/outlet boundaries,
grid sequence, exact turbulence-model variant, convergence residuals, time
steps, and definitions of Cp/Cf/Cl/Cd. A decreasing residual alone establishes
neither grid convergence nor agreement with experiments. Add the original
measurement papers at implementation time rather than citing only NASA's
resource pages.
