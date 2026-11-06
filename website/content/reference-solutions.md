# Exact and reference solutions

A verification library should say what its answer means. The [reference explorer](https://koyamahr.github.io/numerical-methods-atlas/#/exact-solutions) contains **18 cases** with formulas, assumptions, source links, point values and, for one-dimensional cases, cell means. It evaluates references; it does not advance a numerical PDE solution.

## Four different reference categories

- **Analytic:** explicit formulas, including scalar entropy waves, sine translation/decay, dry-bed and vacuum fans, channel profiles and Taylor–Green flow. Floating-point evaluation still has rounding error.
- **Semi-analytic:** Euler, wet shallow-water and isothermal Riemann solutions. The wave curves are analytic, but matching the middle state requires a numerical scalar root solve.
- **Manufactured:** prescribe a smooth field and derive the forcing and boundary conditions. The Poisson sine case tests a forced problem chosen for that field.
- **Numerical reference:** a refined numerical computation. It retains discretization, boundary and time-integration errors. Existing high-resolution atlas comparisons belong here when explicitly identified; they are not additional analytic cases in this library.

Agreement with a reference verifies a particular setup. It does not validate a physical model against experiments or certify every boundary treatment.

## Included fields and assumptions

The scalar cases are periodic sine advection and heat decay, Burgers shock/fan and quadratic traffic shock/fan. Euler includes Sod, Lax, a double rarefaction and a generated vacuum, all for an ideal gas with gamma 1.4. Shallow water includes a wet dam break, expansion into a dry bed and a dry middle state, with a flat bottom and gravity 1. Isothermal Euler uses constant sound speed 1 and strictly positive initial density; it has no energy equation and no finite vacuum state.

The viscous cases are planar steady Couette and Poiseuille profiles in a unit channel and a periodic two-dimensional Taylor–Green vortex. Channel profiles are velocity fields, not compressible conserved states. Taylor–Green returns velocity and pressure with a fixed zero-mean pressure gauge. The Poisson manufactured sine returns both the field and its forcing.

These are canonical, nondimensional setups. Dry-bed/vacuum support in the reference evaluator does **not** add that capability to the existing positive-state finite-volume solver. Topography, viscosity in Riemann problems, arbitrary equations of state and multidimensional shock interactions are outside this first library.

![Point references and conserved/scalar cell means in six cases](figures/reference-solutions.png)

## Point values and finite-volume means

For a conserved state, a finite-volume comparison uses

\[
\overline{\boldsymbol U}_i(t)=\frac{1}{x_{i+1/2}-x_{i-1/2}}
\int_{x_{i-1/2}}^{x_{i+1/2}}\boldsymbol U(x,t)\,dx.
\]

The library integrates density, momentum and total energy for Euler, and depth/density and momentum for shallow-water/isothermal flow. Converting a mean conserved state to primitive variables is generally different from averaging primitive variables. A shock cutting a cell makes a center sample particularly misleading.

Known shocks, contacts and both edges of rarefaction fans split each integral into smooth pieces. Gauss–Legendre quadrature uses 24 and 48 points **per piece**; saved means use the 48-point result. The maximum difference between the two orders is a convergence estimate, **not a rigorous error bound**. This convention also applies to analytic cases: their saved cell means use finite-order quadrature rather than symbolic integration.

For a nonuniform mesh, the reported error norms are normalized by total domain length:

\[
L_1=\frac{\sum_i\Delta x_i|e_i|}{\sum_i\Delta x_i},\qquad
L_2=\left(\frac{\sum_i\Delta x_i e_i^2}{\sum_i\Delta x_i}\right)^{1/2},\qquad
L_\infty=\max_i|e_i|.
\]

Each component is reported separately. The Euler/SWE/isothermal [equation gallery](equation-gallery.md) now uses these conserved cell means. Its saved physical times still come from independent final-time numerical solves.

## Riemann construction and tolerances

The self-similar solution uses xi=(x−x0)/t. For Euler the matched unknown is pressure; for shallow water it is depth; for isothermal flow it is density. The implementation brackets a monotone wave-matching residual in the logarithm of that positive unknown, then bisects. The target logarithmic bracket width is 2e−13, with at most 160 bisections and a final residual check of 2e−10 times a characteristic velocity scale. An exact zero residual can terminate earlier. Iterations, final bracket width and residual are saved alongside each case.

Separating Euler or shallow-water fans can create a middle vacuum/dry region. Those cases bypass the positive-state root solve. Conserved variables vanish there. Velocity is physically undefined in vacuum; the low-level conversion displays zero by convention. Isothermal expansion approaches arbitrarily small positive density instead of a finite vacuum. States outside the supported float64 range raise an error rather than silently clipping the reference.

[The Clawpack Euler chapter](https://www.clawpack.org/riemann_book/html/Euler.html) and [shallow-water chapter](https://www.clawpack.org/riemann_book/html/Shallow_water.html) describe the wave construction and dry/vacuum cases. [Bhat and Fetecau's author manuscript](https://www.sfu.ca/~van/papers/Riemann-inv.pdf) gives the isothermal wave curves for the original Euler system in its Riemann-problem discussion; this library uses that original system, not the paper's regularized model.

## Viscous and manufactured formulas

For a unit-height channel, unit density and viscosity nu, the steady profiles are

\[
u_{\rm Couette}(y)=y,\qquad
u_{\rm Poiseuille}(y)=\frac{G}{2\nu}y(1-y),\qquad G=1,\quad\nu=0.1.
\]

Couette has wall speeds 0 and 1 with zero pressure gradient. Poiseuille has stationary no-slip walls; G is either the negative pressure gradient per unit density or an equivalent body acceleration. These are fully developed planar flows, not pipe flow.

For Taylor–Green on the periodic square [0,2pi]², with nu=0.1 and unit density,

\[
u=\sin x\cos y\,e^{-2\nu t},\qquad
v=-\cos x\sin y\,e^{-2\nu t},\qquad
p=\frac{\cos(2x)+\cos(2y)}4e^{-4\nu t}.
\]

The Web explorer displays an x-slice at y=pi/4, **not two-dimensional area means**. The Python evaluator accepts full 2D coordinates and smooth rectangular box averages. Related methods are in the [viscous-flow chapter](incompressible.md).

The manufactured case prescribes u=sin(pi x), giving −u_xx=f=pi² sin(pi x) with homogeneous Dirichlet endpoints. Its source is available through the same object; it is not an arbitrary-source Poisson solver.

## Reuse and reproduce

```python
import numpy as np
from numart.reference_solutions import get_reference, riemann_reference

ref = get_reference('euler-sod')
edges = np.array([0., .15, .42, .51, .7, 1.])
points = ref.point((edges[:-1] + edges[1:]) / 2, t=.2)
report = ref.cell_average_report(edges, t=.2)
means = report['values']  # columns: rho, rho*u, E
# With actual numerical conserved means q of the same shape:
# errors = ref.compare_means(q, edges, t=.2)
custom = riemann_reference('shallow-water', (2., 0.), (1., 0.),
                           parameter=9.81)
tg = get_reference('taylor-green')
box_mean = tg.box_average([0., 0.], [.2, .3], t=.5)
```

Rebuild the saved profiles and figure with `MPLCONFIGDIR=.mplconfig python scripts/build_reference_solutions.py`. [Download the data and numerical source hashes](figures/reference-solutions.json). Python tests compare Euler with an existing independent implementation, check Rankine–Hugoniot jumps and Lax inequalities, rarefaction PDE residuals and invariants, global balances, known integrals, manufactured forcing and Taylor–Green momentum/divergence residuals. The Web build checks the saved schema, wave locations, source hashes and averaging conventions.

Blasius, Sedov, Noh and additional multidimensional references remain future extensions. [LANL ExactPack](https://github.com/lanl/ExactPack) is an independent source collection to consult for those additions; it is not a dependency or a claim of cross-validation for the cases above.
