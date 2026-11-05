# Arakawa A, B and C grids in geophysical fluid dynamics

A/B/C names specify **where different variables live on a mesh**. They are
not an accuracy order, a mesh shape, or a time-stepping family. A structured
rectangular mesh may use any of these staggerings. The conventional comparison
is described by [Arakawa–Lamb (1977)](https://doi.org/10.1016/B978-0-12-460817-7.50009-4),
with a useful agency exposition in the
[ECMWF numerical-methods notes](https://www.ecmwf.int/sites/default/files/elibrary/2002/16948-numerical-methods.pdf).

**Implemented here:** placement diagrams and tested Fourier symbols for a
linear periodic f-plane shallow-water system. This is not an A/B/C nonlinear
weather or ocean model, and it introduces no new full flow simulation.

## A, B and C specify relative placement

Take free-surface perturbation η at scalar cell centers (i+1/2,j+1/2), with
square cell size Δ. Define u as the x velocity and v as the y velocity.

- **A grid:** η, u and v are all at the same center.
- **B grid:** η is at the center; both u and v are at vertices (i,j).
- **C grid:** η is at the center; u is at x-normal faces (i,j+1/2), and v is
  at y-normal faces (i+1/2,j).

Choosing vertices rather than centers as the origin reverses some diagram
conventions without changing the relative placement. Plot the locations and
component directions before comparing array indices between models.

![A/B/C placement and four linear dispersion cuts](figures/geophysical-grids.png)

On a C grid, normal face velocities naturally supply cell divergence, and
center-to-center scalar differences give face pressure gradients. That is the
placement already used by the atlas's [periodic MAC projection](incompressible.md).
The relationship concerns spatial location; MAC and an ocean C-grid dynamical
core need not share their Coriolis, advection, boundary or time algorithms.
The official [MITgcm staggering description](https://mitgcm.readthedocs.io/en/latest/algorithm/c-grid.html)
shows this face-normal arrangement in three dimensions.

## Rotation and gravity waves make the difference visible

For constant mean depth H and constant Coriolis parameter f,

\[
u_t-fv=-g\eta_x,\qquad v_t+fu=-g\eta_y,
\qquad\eta_t+H(u_x+v_y)=0.
\]

The continuum has a zero-frequency geostrophic branch and gravity branches

\[
\omega^2=f^2+c^2(k^2+\ell^2),\qquad c=\sqrt{gH},\qquad L_D=c/|f|.
\]

A discrete dispersion relation depends on the operators **and** the locations.
Here each grid uses centered second-order pressure/divergence; C-grid Coriolis
uses the symmetric four-point interpolation between u and v locations.
With the physical staggering phases removed, the effective wavenumbers are

\[
\begin{aligned}
A:\quad &\widetilde k=\sin(k\Delta)/\Delta,
&\widetilde\ell=\sin(\ell\Delta)/\Delta,&\quad f_h=f,\\
B:\quad &\widetilde k=2\sin(k\Delta/2)\cos(\ell\Delta/2)/\Delta,
&\widetilde\ell=2\cos(k\Delta/2)\sin(\ell\Delta/2)/\Delta,&\quad f_h=f,\\
C:\quad &\widetilde k=2\sin(k\Delta/2)/\Delta,
&\widetilde\ell=2\sin(\ell\Delta/2)/\Delta,&\quad f_h=f\cos(k\Delta/2)\cos(\ell\Delta/2).
\end{aligned}
\]

The computed baseline has ω_h²=f_h²+c²(k̃²+ℓ̃²). For the energy-scaled state
(u,v,cη/H), the full 3×3 Fourier generator is skew-Hermitian: its eigenvalues
are 0 and ±iω_h. This is a **semi-discrete** result. A time integrator can add
phase error, damping or instability even when the spatial generator conserves
this linear energy.

## Checkerboards and an unresolved deformation radius

A centered A-grid pressure gradient cannot see the shortest alternating
height mode in a coordinate direction. The B-grid baseline removes that
axis-only null mode but retains a diagonal height checkerboard. The C-grid
pressure-gradient/divergence pair couples that mode; however, its simple
Coriolis average vanishes at certain shortest waves. These are distinct
operator effects, not one universal checkerboard diagnosis.

The figure compares both axial and diagonal waves at L_D/Δ=0.25 and 2.
A and B overlap on the diagonal for these square-grid operators, while their
axial curves differ. When the deformation radius is unresolved, Coriolis
averaging can strongly distort the C-grid near-inertial branches. Thus
“C is always best” is not a valid conclusion. Resolved gravity waves,
coarse-grid geostrophic adjustment and directional errors are different tests.
Different Coriolis discretizations can change the comparison without changing
the C placement itself.

## D and E, vertical staggering and magnetic grids

The **D grid** interchanges the face locations of u and v relative to C:
u lies at the y-normal face location and v at the x-normal face location.
The arrows still denote physical x and y components, so a D diagram is not
obtained by merely renaming the C velocity arrays. The **E grid** is commonly
viewed as a B arrangement rotated by 45 degrees; its indexing and resolvable
wavevector set must be treated consistently. They are described here but
have no implemented symbols in this addition.

Horizontal Arakawa staggering is separate from **Lorenz versus
Charney–Phillips vertical staggering**. Likewise, [MHD constrained transport](mhd.md)
uses face/edge placement to enforce a magnetic-divergence identity; it is not
synonymous with an Arakawa C-grid shallow-water algorithm. Each needs its own
compatible discrete operators.

## Evidence and the next geophysical benchmarks

`numart.geophysical_grids` supplies the A/B/C symbols. Tests compare them with
independently applied physical-grid finite-difference stencils on Fourier
waves, check skew-Hermitian energy structure and the geostrophic zero branch,
verify long-wave second-order convergence, and expose the distinct short-wave
null modes. Reproduce the figure with `python scripts/build_geophysical_grids.py`;
the [manifest](figures/geophysical-grids.json) records assumptions, sampled
frequencies and source hashes.

A sensible next flow sequence is geostrophic adjustment, inertia–gravity
waves, a coastal Kelvin wave, and a beta-plane Rossby wave, followed by
potential-vorticity and nonlinear energy/enstrophy budgets. The present
constant-f symbols do not verify beta-plane Rossby propagation, coastlines,
spherical metrics, topography or wetting/drying. A nonlinear Arakawa Jacobian
or energy/enstrophy-conserving shallow-water flux is another algorithmic
choice; selecting A, B or C placement alone does not provide those invariants.
