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

The [Double Mach Reflection exhibit](double-mach.md) is an actual **first-order HLL computation** of an oblique shock interaction. It is not a controlled Roe-versus-HLL carbuncle experiment and supplies no carbuncle-free certification. The planar-shock perturbation and blunt-body comparison described above remain future work. The physical cylindrical [viscous stress](coordinates-viscosity.md) and numerical shock dissipation also represent different operators.

Continue with [Roe’s legacy](roe-memorial.md), [the flux benchmarks](benchmarks.md), and [the implementation roadmap](roadmap.md).
