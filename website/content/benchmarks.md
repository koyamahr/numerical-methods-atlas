# Benchmark library

Each 1D `Problem` stores the equation, domain, final time, boundaries, initial
condition, reference solution, and citation keys. `get_problem(name)` exposes
the same definition to every method. The last array axis contains variables:
Euler uses `(ρ,ρu,E)`, shallow water uses `(h,hu)`, and isothermal flow uses `(ρ,ρu)`.

## Smooth problems

Linear advection uses periodic `[0,1]`, speed a, and initial data `sin(2πx)`.
The exact translated solution compares finite differences, DG, and Fourier
methods. DG uses modal Legendre P0/P1/P2, upwind boundary fluxes, and SSPRK3.
Distinguish the spatial order of Pp from the third-order time integrator.
DG has elements × (p+1) unknowns. Fourier integrates the linear modes exactly
in time; the gallery does not establish an equal-cost or equal-degree-of-freedom
ranking. Nonlinear products, dealiasing, and Gibbs treatments are future work.

`entropy-wave` uses Euler data `ρ=1+0.2sin(2πx)`, `u=1,p=1,γ=1.4`, periodic
`[0,1]`, and `t=1`. Only density translates, giving an exact reference for smooth
accuracy and periodic conservation. Isothermal Euler has no independent energy
or entropy variable and does not support this same Euler entropy-wave problem.

## Shock tubes

**Sod:** `[0,1]`, `x0=0.5`, left `(ρ,u,p)=(1,0,1)`, right `(0.125,0,0.1)`,
`γ=1.4`, and `t=0.2`. Boundaries use zero-gradient extrapolation; the main waves
do not reach them before the final time. The exact Riemann solver finds the
matching pressure by bisection and samples shocks, contacts, and rarefaction
fans. Exact solutions containing a vacuum are unsupported.
[Sod (1978)](https://doi.org/10.1016/0021-9991(78)90023-2),
[exact-solution implementation reference](https://faculty.washington.edu/rjl/riemann_book/Euler_equations.html).

**Lax:** `[-5,5]`, `x0=0`, left `(0.445,0.698,3.528)`, right `(0.5,0,0.571)`,
`γ=1.4`, `t=1.3`, and extrapolation boundaries. The Lax test and the
Lax–Friedrichs algorithm are different namesakes. These are standard parameters
from later literature; the original 1954 paper's table has not been directly
matched here.

**Shu–Osher:** `[-5,5]`, `x0=-4`, `t=1.8`, `γ=1.4`, left
`(3.857143,2.629369,10.33333)`, and right `(1+0.2sin(5x),0,1)`.
Ghost states are fixed to the initial conditions evaluated at the domain ends.
There is no exact final-time reference; the first-edition figure compares
MUSCL and WENO numerical results.
[Shu–Osher (1989)](https://doi.org/10.1016/0021-9991(89)90222-2),
[adopted parameters in Quokka, §3.1.5](https://academic.oup.com/mnras/article/512/1/1430/6530656).

## Low densities and Einfeldt-type tests

`double-rarefaction` uses `[0,1]`, `x0=0.5`, left `(1,-2,0.4)`, right
`(1,2,0.4)`, `γ=1.4`, and `t=0.15`. This strong expansion is commonly called
the 1–2–3 problem. The selected positivity test uses piecewise-constant
reconstruction with HLLE. It does not transfer a positivity guarantee to
high-order MUSCL or WENO.
[Einfeldt et al. (1991)](https://doi.org/10.1016/0021-9991(91)90211-3).

## Shallow-water and isothermal flow

`dam-break` solves flat-bottom shallow water with `g=1`, left `h=2`, right
`h=1`, `u=0`, `[0,1]`, and `t=0.1`. Dry beds, topographic sources,
well-balanced discretization, and wetting/drying are unsupported.
`isothermal` uses `p=cs²ρ`, `cs=1`, left `ρ=1`, right `ρ=0.125`, and `u=0`
on the same domain and time interval. Both use extrapolation boundaries.
First-edition checks compare solvers, admissible states, and conservative
form; exact Riemann references remain to be added.
[LeVeque (2002)](https://doi.org/10.1017/CBO9780511791253).

## Riemann fluxes and reconstruction

Rusanov and HLL support Euler, shallow water, and isothermal flow. HLLC, Roe,
and HLLE currently support ideal-gas Euler only. HLL uses minimum/maximum
local acoustic speeds; HLLE uses Einfeldt-type estimates including Roe averages.
Roe applies quadratic entropy smoothing to acoustic eigenvalues with
`δ=0.1ã`, leaving the contact eigenvalue unchanged. This is neither a
low-density positivity fix nor a general entropy-stable flux construction.

MUSCL uses minmod reconstruction in primitive variables. WENO5-JS is a
componentwise **finite-difference** implementation with pointwise fluxes and
global LF splitting. Characteristic reconstruction, WENO-Z, and positivity
limiters are future work. Errors are labeled `pointwise`: finite-volume cell
averages and finite-difference point values are not strictly interchangeable.

See [MHD](mhd.md) for Orszag–Tang definitions and limits, and
[elliptic problems](elliptic.md) for diffusion and Poisson cases.

## Matching the benchmark to the scheme

The [original KEEP exhibit](keep.md) uses a smooth isentropic vortex and conservation diagnostics. Its bare central flux has no shock stabilization and is not presented as a Sod/DMR solver. The [movie guide](movies.md) separates those smooth computations from shock-capturing and MHD movies, and keeps steady fields as still images.
