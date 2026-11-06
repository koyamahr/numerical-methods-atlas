# NASA 2D verification and validation case catalog

Start with the official [NPARC Verification and Validation Archive](https://www.grc.nasa.gov/WWW/wind/valid/archive.html),
[CFL3D test cases](https://nasa.github.io/CFL3D/Cfl3dv6/cfl3dv6_testcases.html),
and [Turbulence Modeling Resource](https://tmbwg.github.io/turbmodels/).
NASA's [TMR information page](https://www.nasa.gov/nasa-turbulence-modeling-resource/)
describes the resource's move to GitHub in February 2026.
The two **15-degree wedge flows are now computed educational Euler baselines**.
The remaining NASA entries below are cataloged candidates. These independent
calculations are not Wind-US output, experimental validations or reproductions
of NASA's complete solver/grid comparison. A classical Mach-3 forward-facing
step and [Double Mach Reflection](double-mach.md) complement the NASA cases.

## Computed shock tests

[Open the shock-containing fields in the gallery](https://koyamahr.github.io/numerical-methods-atlas/#/gallery).
Both wedges start from uniform freestream with gamma 1.4, density 1 and sound
speed 1. The independent body-fitted mesh spans x = −0.5 to 1, the lower wall
y = max(x,0) tan(15°), and the upper boundary y = 1.2. The higher farfield keeps
the Mach-2 weak shock below that boundary at the outlet; it differs from the
height 1 of NASA's Mach-2.5 domain. Inlet and upper-boundary
states are fixed at freestream, the outlet is extrapolated and the lower wall
reflects normal momentum. Shared oriented face fluxes conserve the cell totals;
cell areas and face normals come from the actual quadrilaterals.

- **NASA wedge, Mach 2.0:** Mach and pressure maps on 240 × 80 cells at t = 3,
  with the theoretical weak-shock line. A 120 × 40 run supplies a second grid.
  [NASA setup](https://www.grc.nasa.gov/WWW/wind/valid/wedgeM2/wedgeM2.html).
- **NASA wedge, Mach 2.5:** the same independent meshes and terminal time.
  The reference shock angle is approximately 36.94490°, pressure ratio 2.467500,
  and downstream Mach number 1.873526. The theta–beta–Mach root and normal-shock
  relations supply the reference, with a numerical Rankine–Hugoniot check.
  [NASA analytical comparison](https://www.grc.nasa.gov/WWW/wind/valid/wedge/wedge.html).
- **Classical Mach-3 forward-facing step:** a 3 × 1 tunnel with the step at
  x = 0.6 and height 0.2, uniform inflow (density 1.4, pressure 1, velocity 3),
  reflecting walls and an extrapolated exit. A 240 × 80 grid reaches t = 4,
  with 81 saved states and an MP4. [Watch the shock reflections](https://koyamahr.github.io/numerical-methods-atlas/#/movies?case=forward-step).
  This is the classical Emery/Woodward–Colella benchmark, not a NASA-originated
  experiment. The corner treatment differs from the corrected PPM comparison
  in [Woodward–Colella §VI.b](https://www.researchgate.net/publication/222459521_The_numerical_simulation_of_two-dimensional_fluid_flow_with_strong_shocks):
  this baseline applies plain reflection and does not reset entropy or enthalpy
  near the step corner. Corner artifacts and smeared slip lines may remain.

These use **first-order HLL finite volumes and SSPRK2**, with CFL 0.4. Wedges
have no imposed analytical shock in their initial state. Their normalized L1
density errors compare conservative cell averages with an exactly clipped
piecewise-constant oblique-shock reference. Wall-pressure medians use the first
fluid row over 0.5 < x < 0.9; a density-gradient fit over 0.35 < x < 0.85 estimates
the shock angle. Mach-2 MC still has local time variation at t = 3 (maximum conserved update
rate approximately 6.08 in the published run); it is not a converged steady
solution. This residual is exposed alongside the sharper density error.
Two grids at one finite terminal time do not establish general
asymptotic order or complete steady convergence. The step has no exact overlay
and only one published grid; t = 4 is an unsteady snapshot.

![NASA Mach-2 wedge](figures/nasa-wedge-m20.png)
![NASA Mach-2.5 wedge](figures/nasa-wedge-m25.png)
![Mach-3 forward-facing step](figures/forward-step.png)

Reproduce with `python scripts/build_shock_gallery.py`; `--reuse` renders cached,
source-checked trajectories. Download [run definitions, diagnostics and hashes](figures/shock-gallery.json),
[final numerical fields](figures/shock-gallery.npz), and the
[step movie manifest](https://koyamahr.github.io/numerical-methods-atlas/assets/movies/shock-catalog.json).

## Shock-containing NASA cases still to implement

The [Mach-5 shock/boundary-layer interaction](https://www.grc.nasa.gov/WWW/wind/valid/m5swbli/m5swbli.html),
[Mach-7 laminar ramp](https://www.grc.nasa.gov/WWW/wind/valid/hypramp/hypramp.html),
Sajben diffuser and RAE 2822 are later candidates. Their viscous, turbulence or
gas-model requirements are part of each case; an inviscid wedge image is not
a substitute for those validations. These cases have no computed exhibit here.

## Starting with Euler and analytical references

- **15° wedge, Mach 2.0 — computed baseline:** oblique shock and wall pressure with two grids. Roe/HLLE method comparisons remain future work. [NASA case](https://www.grc.nasa.gov/WWW/wind/valid/wedgeM2/wedgeM2.html).
- **15° wedge, Mach 2.5 — computed baseline:** shock angle and downstream-state reference. Pair this compression case with the planned expansion corner below. [NASA case](https://www.grc.nasa.gov/WWW/wind/valid/wedge/wedge.html).
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
[Our Double Mach Reflection exhibit](double-mach.md) and the forward step above
are implemented first-order HLL baselines. Riemann configurations and controlled
odd-even/carbuncle comparisons remain future work; the smooth KEEP vortex is computed.
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


## MUSCL reconstruction comparisons

[Compare first order, minmod and MC](#/flow-comparison?case=wedge-m2.5&method=mc).
The new runs keep acoustic HLL, SSPRK2 and nominal CFL 0.4 fixed. Primitive
variables are reconstructed from physical gradients at quadrilateral area
centroids to face midpoints. On the body-fitted grid, x secants account for
the accompanying physical y displacement. A shared face flux updates both
neighbors. The limiter choices are minmod(a,b) and
MC(a,b) = minmod(2a,(a+b)/2,2b); see the [limiter definitions](limiters.md).
Boundary reconstruction excludes solid neighbors and reflects fluid-side
states. One cellwise factor scales reconstructed deviations when a face
would have nonpositive density or pressure. Failed SSPRK2 steps halve the
step size and retry; these events are recorded. Conserved means are not clipped.
This is a tested safeguard, not a general positivity theorem for this solver.

Both NASA wedges have all three reconstructions on 120 × 40 and 240 × 80
meshes at t = 3. Wall pressure, fitted shock angle and integrated density
errors use the definitions above. A separate periodic entropy wave uses
velocity (0.7,0.3), pressure 1 and density
1 + 0.2 sin(2πx) sin(2πy), initialized and compared as exact cell averages.
Grids 16², 32², 64² and 128² reach t = 0.5. Observed orders are printed in the
comparison page; MC approaches second order on this smooth test. Limiter
activation at extrema affects the measured minmod order. Shock errors have
a different convergence regime and do not establish smooth second order.

![Smooth two-dimensional refinement](figures/comparisons/smooth-refinement.png)

The [forward-step comparison](#/flow-comparison?case=forward-step&method=mc)
adds minmod and MC stills and 81-state clips on the same 240 × 80 mesh. All
three clips share density/pressure scales and requested output times, but
actual intermediate timestamps can differ by one adaptive solver step.
Nominal CFL and grids do not imply equal computational cost. These are three
reconstructions of one physical case; the original first-order movie remains
available. The corner treatment is unchanged and the t = 4 flow is unsteady.

Reproduce with `python scripts/build_euler_comparison.py`. Download the
[comparison definitions, diagnostics and hashes](figures/comparisons/euler-comparison.json)
and [final conservative arrays](figures/comparisons/final-fields.npz).
Full trajectories are cached locally under `outputs/euler-comparison`.
