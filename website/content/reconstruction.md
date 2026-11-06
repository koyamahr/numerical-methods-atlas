# Euler reconstruction: PPM, characteristics, WENO-Z and AUSM

[Open the computed comparison](#/reconstruction). This 1D experiment separates
reconstruction choices from numerical-flux choices. It extends the original
[componentwise MUSCL/WENO baseline](benchmarks.md); previous exhibits are retained.

## What is compared

The reconstruction view compares conservative-component and characteristic
MUSCL/MC, limited parabolic finite volumes, and finite-difference WENO5-JS/Z.
FV uses HLLC; FD uses global Lax–Friedrichs flux splitting. Both use SSPRK3,
nominal CFL 0.3 and the same number of grid locations. Their representations,
fluxes and error norms differ: this is not an isolated reconstruction or
matched-cost ranking. Within each method, changing only the basis is a
controlled component/characteristic comparison.

The separate flux view fixes conservative characteristic MUSCL/MC and SSPRK3,
then switches HLLC, acoustic-smoothed Roe, Einfeldt-type HLLE and the explicitly
defined AUSM baseline below. It does not change the spatial reconstruction.

## Limited parabolic finite volumes

Following the reconstruction idea of [Colella–Woodward (1984)](https://doi.org/10.1016/0021-9991(84)90143-8),
form a parabola in each cell from its mean and two edges. The inspected public
[1982 author preprint](https://escholarship.org/uc/item/5sr307f1) is an earlier
version, not the final journal layout. This implementation includes limited
edge interpolation and monotonicity constraints, coupled by method of lines
to SSPRK3. It excludes original PPM wave tracing, contact steepening, shock
flattening, Lagrangian evolution and remap. Those remain explicit future work.

For a cell mean Q and edges L,R, use the local coordinate ξ in [0,1]:

\[
 q(\xi)=L+\xi[R-L+q_6(1-\xi)],\qquad q_6=6Q-3(L+R).
\]

The integral is exactly Q. Limit initial edge interpolation between adjacent
means; flatten a parabolic extremum and apply the usual curvature bounds.
Characteristic projection freezes a local conservative eigenbasis in each
cell, limits projected deviations, then transforms back. Components are
conservative variables, not primitive variables. Reconstructed left/mid/right
states share one affine positivity scaling about Q if needed. Their Simpson
mean remains Q; no conserved mean is clipped. Inadmissible RK stages retry
with a halved time step. These safeguards do not prove fully discrete positivity.

## Characteristic finite-difference WENO-Z

For each face freeze a Roe-averaged conservative eigenbasis. Project the
positive and negative global-LF split flux stencils, reconstruct each
characteristic component, and transform the resulting face flux back.
FD evolves point values; it is not FV state reconstruction. Shared flux
differences conserve the discrete sum on a periodic grid.

The Z variant uses the JS smoothness indicators with

\[
 \tau_5=|\beta_0-\beta_2|,\quad
 \alpha_k^Z=d_k\left[1+\left(\frac{\tau_5}{\beta_k+\epsilon}\right)^2\right],
 \quad\omega_k^Z=\frac{\alpha_k^Z}{\sum_l\alpha_l^Z},
 \quad(d_0,d_1,d_2)=(0.1,0.6,0.3).
\]

Here ε = 10⁻⁶ is fixed and the Z exponent is 2. These choices must accompany
comparisons; the regularization and normalization of the characteristics affect
the weights. [Borges, Carmona, Costa and Don (2008)](https://doi.org/10.1016/j.jcp.2007.11.038)
is the original bibliographic reference. Publisher metadata and the public
[earlier three-author manuscript](https://citeseerx.ist.psu.edu/document?doi=84e17864257f4a33bd045df500e93cbad44e8f49&repid=rep1&type=pdf)
were inspected; that manuscript has different weight conventions. The formula
above, its exponent and the executable checks define this edition's variant;
no final-paper figure is reproduced.

## AUSM: keep the variant explicit

[Liou–Steffen (1993)](https://doi.org/10.1006/jcph.1993.1122) introduced AUSM.
The local baseline uses a common interface sound speed a = (aL+aR)/2,
Mach polynomials M± = ±(M±1)²/4 in the subsonic interval, and the cubic
pressure fractions P± = (M±1)²(2∓M)/4. Supersonic branches use signed upwind
Mach and pressure fractions. These formulas were cross-checked against the
[official FEST-3D AUSM source](https://fest3d.github.io/sourcefile/ausm.f90.html).
This is an independently implemented, specified AUSM-family variant, not
FEST-3D output or a reproduction of every 1993 sound-speed/pressure option.

Let Mf = M+(uL/a)+M−(uR/a). Upwind the advected vector (ρ,ρu,ρv,ρH)
using a max(Mf,0) on the left and a min(Mf,0) on the right, and add
pL P+(uL/a)+pR P−(uR/a) to normal momentum only. Energy transports total
enthalpy. Tests include uniform states, both supersonic directions, Mach ±1
branch limits, stationary/moving contacts and the computed Euler problems.

[AUSM+ (1996)](https://doi.org/10.1006/jcph.1996.0256) and
[AUSM+-up (2006)](https://doi.org/10.1016/j.jcp.2005.09.020) are distinct planned
extensions. The current baseline has no all-speed correction or low-Mach
verification. None of these names implies universal shock stability; inspect
the separate [odd–even comparison](#/shock-robustness).

## Problems, references and accuracy

- **Sod:** N=200, x∈[0,1], t=0.2, standard states, extrapolated ends.
- **Moving contact:** N=200, periodic [0,1], u=p=1, density 1 on the first
  half and 2 on the second; one crossing t=1.
- **Shu–Osher:** N=240, x∈[−5,5], t=1.8, fixed end states, shock at −4,
  left (ρ,u,p)=(3.857143,2.629369,10.33333), right density 1+0.2sin(5x), u=0,p=1.
  The dashed curve is our internal characteristic FD WENO-Z N=960 run, not
  an exact solution or an external-code validation.

FV initialization integrates conserved quantities. Sod final density errors
use 128-node Gauss quadrature of the analytic Riemann solution; the saved
64/128-node discrepancy estimates quadrature sensitivity across discontinuities.
FD errors are pointwise. Derived FV primitive curves are primitive variables
of conserved means, not exact primitive means. No exact Shu–Osher error is reported.

A separate smooth periodic entropy wave uses N=32,64,128 at t=0.2 and
CFL = 0.25(32/N)^(2/3). This reduces dt proportional to dx^(5/3), making the
SSPRK3 time error O(dx⁵). Measured WENO orders are about five on this smooth
case; limited PPM is about two on this sequence because of extremum limiting.
This is not a global fifth-order guarantee at shocks or arbitrary critical points.

![Computed reconstruction comparison](figures/reconstruction/reconstruction.png)

Reproduce with `python scripts/build_reconstruction.py`. Download
[profiles, diagnostics and source hashes](figures/reconstruction/reconstruction.json)
and [conserved arrays](figures/reconstruction/fields.npz). The final arrays,
positive-state checks and retry counts apply only to the stated tests.
