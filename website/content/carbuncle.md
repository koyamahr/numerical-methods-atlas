# The carbuncle phenomenon

A strong shock can develop a spurious bulge, streaks, or alternating transverse states when captured by a multidimensional numerical scheme. This **carbuncle instability** is a property of the discretized flow problem; a sharp-looking shock alone does not establish accuracy. Grid-aligned shocks are a particularly revealing setting.

[Quirk (1994)](https://doi.org/10.1002/fld.1650180603) documents failures of Godunov-type solvers and motivates switching between complementary fluxes. [Pandolfi and D’Ambrosio (2001)](https://doi.org/10.1006/jcph.2000.6652) analyze shock-related instabilities and localized remedies. Their analyses motivate the diagnostic questions below; this chapter does not claim a universal mechanism or a new stability proof.

## Why a one-dimensional flux can fail in two dimensions

A face-normal Roe flux has the form

\[
\widehat F_n=\tfrac12(F_n(U_L)+F_n(U_R))
-\tfrac12\sum_k |\widetilde\lambda_k|\,\alpha_k\widetilde r_k.
\]

Its characteristic decomposition gives different dissipation to acoustic, contact, and shear waves. Near a stationary, grid-aligned shock, disturbances in neighboring rows can interact with weakly damped transverse modes and the discrete shock structure. Resolving contacts accurately and stabilizing every strong multidimensional shock are separate design demands. The entire scheme matters: reconstruction, flux, time integration, mesh, and boundaries.

**Odd–even decoupling** describes alternating neighboring-row behavior and is a useful shock-instability diagnostic. It is related to carbuncle studies, but the terms do not identify one identical test in every paper. The familiar blunt-body shock bulge and a perturbed planar-shock experiment have different geometries and boundary conditions.

## Three different questions

- **Entropy correction:** a transonic rarefaction can be represented by an inadmissible expansion shock. Smoothing a small acoustic eigenvalue addresses this sonic-wave issue. It does not by itself certify multidimensional strong-shock stability.
- **Positivity:** density and pressure must remain admissible. Wave-speed bounds, a suitable CFL restriction, and positivity-preserving reconstruction address this question. Positive states can still contain a carbuncle.
- **Transverse shock robustness:** perturbations along the shock must not grow into a grid-dependent artifact. This requires its own multidimensional evidence.

The library’s 1D Roe entropy smoothing belongs to the first category. Passing Sod or the double-rarefaction test does not answer the third.

## Remedies and their tradeoffs

A two-wave HLL/HLLE flux or Rusanov flux usually adds more dissipation to contact and shear information than a contact-resolving solver. A shock sensor can blend a sharper flux with a more dissipative one locally. Rotated or multidimensional flux constructions seek dissipation in directions that a strictly face-normal treatment can miss. See [Nishikawa and Kitamura (2008)](https://doi.org/10.1016/j.jcp.2007.11.003) for a rotated-hybrid approach.

These are design directions, not interchangeable guarantees. A sensor may also damp a physical shear layer; excessive dissipation can conceal an instability while losing the feature of interest. State the actual wave-speed estimate: this atlas’s 2D baseline uses **HLL with Davis-type bounds**, not an implementation of every Einfeldt HLLE variant.

## What an honest comparison must measure

Use a perturbed planar strong shock, then a blunt-body flow on a controlled grid sequence. Fix the shock Mach number, shock location relative to cell faces, perturbation amplitude and wavelength, boundary conditions, reconstruction, CFL, and final time. Compare Roe, HLL/HLLE, and a proposed hybrid under matched settings. Repeat with shifted or rotated meshes.

For periodic transverse rows, one possible alternating-density diagnostic at a selected shock-normal station is

\[
A_\pi(i,t)=\left|\frac{1}{N_y}\sum_{j=0}^{N_y-1}(-1)^j
\bigl(\rho_{i,j}(t)-\overline\rho_i(t)\bigr)\right|.
\]

Record its time history and the maximum over the shock neighborhood, together with shock position, transverse velocity, pressure, and positivity. For a moving shock, track the shock neighborhood rather than a single fixed column. Other wavelengths need their own diagnostics. A small final residual or a visually smooth contour is insufficient evidence.

## Status in this edition

The [Double Mach Reflection exhibit](double-mach.md) is an actual **first-order HLL computation** of an oblique shock interaction. It is not a controlled Roe-versus-HLL carbuncle experiment and supplies no carbuncle-free certification. The planar-shock section below adds a controlled row-perturbation diagnostic; blunt-body comparisons remain future work. The physical cylindrical [viscous stress](coordinates-viscosity.md) and numerical shock dissipation also represent different operators.

Continue with [Roe’s legacy](roe-memorial.md), [the flux benchmarks](benchmarks.md), and [the implementation roadmap](roadmap.md).


## Computed planar odd–even diagnostic

[Open the controlled comparison](#/shock-robustness). This independent test
uses a stationary Mach-6 normal shock in [0,1] × [0,0.25], γ=1.4,
upstream (ρ,u,v,p)=(1.4,6,0,1), and exact normal-shock downstream states.
Both x boundaries are fixed, y is periodic, and cells are square. Compare
64 × 16 and 128 × 32 at t=0.2 using first-order space, SSPRK2 and CFL 0.3.
The shock is either at x=0.5, aligned with a face, or half a cell farther right.
Initial conservative means integrate a row-dependent front displacement of
±10⁻⁴Δx exactly. Each configuration has an unperturbed control.

Compare raw Roe, Roe with acoustic smoothing δ=0.1c̃, Davis HLL,
Einfeldt-type HLLE, a pressure-sensor Roe/HLLE blend, and the common-sound-speed
cubic-pressure [AUSM baseline](reconstruction.md). All runs use the same
spatial/time settings; their step counts and costs need not match.
The blend uses S=max_neighbors |p_neighbor−p|/min(p_neighbor,p),
θ=clip((S−0.05)/0.2,0,1), and the maximum adjacent cell θ at each face.
F=(1−θ)F_Roe_fixed+θF_HLLE. The x-pressure jump can therefore activate
HLLE on nearby transverse faces. This is an explicit educational sensor,
not the published rotated-hybrid construction or a universal cure.

Measure max_i Aπ over |x−xshock|<0.1, pressure/density admissibility, retry
counts, transverse velocity and each row's integrated mass-deficit position.
The latter is not a pointwise detected front location. Density maps subtract
the transverse row mean, using one signed color range per comparison.
The history's logarithmic display floors values at 10⁻¹⁶; raw values remain
in the download. No state clipping or hidden flux replacement is used.

Face-aligned Roe runs amplify the chosen row mode; shifting the shock half a
cell changes the response substantially. The entropy correction does not
remove this position sensitivity. HLL/HLLE and the other fluxes must be judged
from these stated runs, rather than their names. The special Nyquist seed
preserves a symmetry with zero transverse velocity even as density rows
separate, so this experiment does not probe general transverse motion.

![Controlled planar-shock comparison](figures/shock-methods/planar-128-0.png)

Reproduce with `python scripts/build_shock_robustness.py`. Download
[all perturbed/control histories, definitions and source hashes](figures/shock-methods/robustness.json)
and [final conservative fields](figures/shock-methods/planar-fields.npz).
This is not the original Quirk moving-shock/perturbed-grid duct or a blunt-body
carbuncle bulge. Other wavelengths, mesh rotations, blunt-body cases and
broader CFL/strength sweeps remain required work; no carbuncle-free claim is made.
See [Property U](advanced.md#roes-property-u) for the separate single-jump algebra.
