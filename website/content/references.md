# References by original publication year

Original papers and books are distinguished from sources used to check the implementations. A DOI does not imply that the full text has been inspected or its figures reproduced.
Each note identifies publicly available originals, later expositions, and original sources that still need verification. NASA case resources appear in the [2D case catalog](nasa-2d.md).

This file and `references.bib` are generated from `catalog/references.json` by `python scripts/build_references.py`.

## 1928 · cfl1928

Courant, Richard and Friedrichs, Kurt and Lewy, Hans. **Über die partiellen Differenzengleichungen der mathematischen Physik**. Mathematische Annalen.

[Original bibliographic record](https://doi.org/10.1007/BF01448839) · [Full text or implementation reference](https://www.stat.uchicago.edu/~lekheng/courses/302/classics/courant-friedrichs-lewy.pdf)

Originally published in 1928; the linked source is a later English translation. Background on domains of dependence and the CFL condition.

## 1947 · crank1947

Crank, John and Nicolson, Phyllis. **A practical method for numerical evaluation of solutions of partial differential equations of the heat-conduction type**. Proceedings of the Cambridge Philosophical Society.

[Original bibliographic record](https://doi.org/10.1017/S0305004100023197) · [Full text or implementation reference](https://doi.org/10.1007/BF02127704)

Originally published in 1947; the linked source is a 1996 reprint. This edition implements the theta method for linear diffusion, rather than reproducing the original nonlinear problem.

## 1949 · thomas1949

Thomas, Llewellyn Hilleth. **Elliptic problems in linear difference equations over a network**. Watson Scientific Computing Laboratory, Columbia University.

[Original bibliographic record](https://www.netlib.org/na-digest-html/96/v96n09.html) · [Full text or implementation reference](https://www.netlib.org/na-digest-html/96/v96n09.html)

The original report and a holding URL have not been verified. This provisional record follows the historical citation in Netlib and does not imply direct inspection of the original.

## 1950 · charney1950

Charney, Jule G. and Fjørtoft, Ragnar and von Neumann, John. **Numerical Integration of the Barotropic Vorticity Equation**. Tellus.

[Original bibliographic record](https://doi.org/10.1111/j.2153-3490.1950.tb00336.x) · [Full text or implementation reference](https://maths.ucd.ie/~plynch/eniac/CFvN-1950.pdf)

Publicly accessible original paper. Historical context for stability analysis; the numerical weather forecast is not implemented here.

## 1954 · lax1954

Lax, Peter D.. **Weak solutions of nonlinear hyperbolic equations and their numerical computation**. Communications on Pure and Applied Mathematics.

[Original bibliographic record](https://doi.org/10.1002/cpa.3160070112) · [Full text or implementation reference](https://onlinelibrary.wiley.com/doi/10.1002/cpa.3160070112)

Publisher bibliographic record and abstract. Background on weak solutions and Lax-type differences. The Lax shock-tube parameters have not been matched directly to the original table.

## 1956 · lax1956

Lax, Peter D. and Richtmyer, Robert D.. **Survey of the stability of linear finite difference equations**. Communications on Pure and Applied Mathematics.

[Original bibliographic record](https://doi.org/10.1002/cpa.3160090206) · [Full text or implementation reference](https://math.berkeley.edu/~wilken/228B.S07/LaxRichtmyer.pdf)

Publicly accessible original paper. The equivalence theorem assumes a well-posed linear initial-value problem and a consistent linear approximation.

## 1959 · godunov1959

Godunov, Sergei K.. **A difference method for numerical calculation of discontinuous solutions of the equations of hydrodynamics**. Matematicheskii Sbornik.

[Original bibliographic record](https://www.mathnet.ru/eng/sm4873) · [Full text or implementation reference](https://www.mathnet.ru/eng/sm4873)

Original publication in 1959, accepted in 1956. The godunov option in this edition is a Godunov-type finite-volume method with approximate fluxes.

## 1960 · lax1960

Lax, Peter D. and Wendroff, Burton. **Systems of conservation laws**. Communications on Pure and Applied Mathematics.

[Original bibliographic record](https://doi.org/10.1002/cpa.3160130205) · [Full text or implementation reference](https://onlinelibrary.wiley.com/doi/10.1002/cpa.3160130205)

Publisher bibliographic record. Background for linear-advection Lax–Wendroff and systems of conservation laws.

## 1961 · fedorenko1961

Fedorenko, Radii P.. **A relaxation method for solving elliptic difference equations**. Zhurnal Vychislitelnoi Matematiki i Matematicheskoi Fiziki.

[Original bibliographic record](https://www.mathnet.ru/eng/zvmmf8014) · [Full text or implementation reference](https://www.mathnet.ru/eng/zvmmf8014)

Original publication in 1961; English translation in 1962. A historical entry point to multigrid.

## 1961 · rusanov1961

Rusanov, Vladimir V.. **The calculation of the interaction of non-stationary shock waves with barriers**. Zhurnal Vychislitelnoi Matematiki i Matematicheskoi Fiziki.

[Original bibliographic record](https://www.mathnet.ru/eng/zvmmf7987) · [Full text or implementation reference](https://www.mathnet.ru/eng/zvmmf7987)

Russian original in 1961; English translation in 1962. This edition uses a modern local Lax–Friedrichs/Rusanov flux.

## 1973 · reed1973

Reed, W. H. and Hill, T. R.. **Triangular mesh methods for the neutron transport equation**. Los Alamos Scientific Laboratory.

[Original bibliographic record](https://digital.library.unt.edu/ark:/67531/metadc1036080/) · [Full text or implementation reference](https://digital.library.unt.edu/ark:/67531/metadc1036080/)

Public government-report record. This edition implements modal DG for 1D linear advection, rather than triangular-mesh neutron transport.

## 1974 · hirt1974

Hirt, C. W. and Amsden, A. A. and Cook, J. L.. **An arbitrary Lagrangian-Eulerian computing method for all flow speeds**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(74)90051-5) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/0021999174900515)

Publisher record and abstract. Historical ALE reference; the implemented example is only a 1D moving-volume uniform-state check.

## 1977 · brandt1977

Brandt, Achi. **Multi-level adaptive solutions to boundary-value problems**. Mathematics of Computation.

[Original bibliographic record](https://doi.org/10.1090/S0025-5718-1977-0431719-X) · [Full text or implementation reference](https://www.ams.org/mcom/1977-31-138/S0025-5718-1977-0431719-X/S0025-5718-1977-0431719-X.pdf)

AMS-hosted original paper. This edition implements a fixed-grid geometric V-cycle, rather than the full adaptive framework.

## 1977 · gingold1977

Gingold, R. A. and Monaghan, J. J.. **Smoothed particle hydrodynamics: theory and application to non-spherical stars**. Monthly Notices of the Royal Astronomical Society.

[Original bibliographic record](https://doi.org/10.1093/mnras/181.3.375) · [Full text or implementation reference](https://academic.oup.com/mnras/article/181/3/375/988212)

Original publisher record. Early SPH paper; this edition implements static 1D kernel reconstruction, not the stellar calculation.

## 1977 · lucy1977

Lucy, L. B.. **A numerical approach to the testing of the fission hypothesis**. The Astronomical Journal.

[Original bibliographic record](https://doi.org/10.1086/112164) · [Full text or implementation reference](https://articles.adsabs.harvard.edu/pdf/1977AJ.....82.1013L)

ADS-hosted original article. Independent early particle-method reference; the cubic-spline reconstruction here is not a reproduction of Lucy’s original kernel or dynamics.

## 1977 · spectral1977

Gottlieb, David and Orszag, Steven A.. **Numerical Analysis of Spectral Methods: Theory and Applications**. SIAM.

[Original bibliographic record](https://doi.org/10.1137/1.9781611970425) · [Full text or implementation reference](https://epubs.siam.org/doi/abs/10.1137/1.9781611970425.ch2)

Publisher chapter information for a representative spectral-methods monograph. This edition is limited to periodic linear Fourier problems.

## 1978 · sod1978

Sod, Gary A.. **A survey of several finite difference methods for systems of nonlinear hyperbolic conservation laws**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(78)90023-2) · [Full text or implementation reference](https://faculty.washington.edu/rjl/riemann_book/Euler_equations.html)

The DOI identifies the original paper; the source is an implementation reference for the standard Sod problem and exact solution. The original methods and figures are not reproduced in full.

## 1979 · orszag1979

Orszag, Steven A. and Tang, Cha-Mei. **Small-scale structure of two-dimensional magnetohydrodynamic turbulence**. Journal of Fluid Mechanics.

[Original bibliographic record](https://doi.org/10.1017/S002211207900210X) · [Full text or implementation reference](https://doi.org/10.1017/S002211207900210X)

The original study concerns incompressible MHD. Distinguish it from the normalization of the modern compressible Orszag–Tang test used here.

## 1979 · vanleer1979

van Leer, Bram. **Towards the ultimate conservative difference scheme. V. A second-order sequel to Godunov's method**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(79)90145-1) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/0021999179901451)

Publisher bibliographic record and abstract. This edition uses minmod MUSCL with SSPRK3, rather than reproducing the original Lagrangian/remap construction.

## 1981 · roe1981

Roe, Philip L.. **Approximate Riemann solvers, parameter vectors, and difference schemes**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(81)90128-5) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/0021999181901285)

Publisher bibliographic record and abstract. This edition implements 1D Euler with quadratic entropy smoothing of acoustic eigenvalues.

## 1983 · hll1983

Harten, Amiram and Lax, Peter D. and van Leer, Bram. **On Upstream Differencing and Godunov-Type Schemes for Hyperbolic Conservation Laws**. SIAM Review.

[Original bibliographic record](https://doi.org/10.1137/1025002) · [Full text or implementation reference](https://www.ece.uvic.ca/~bctill/papers/numacoust/Harten_etal_1983.pdf)

Publicly accessible original paper. Background on HLL; the hll implementation here uses Davis-type minimum/maximum acoustic wave speeds.

## 1984 · woodward1984

Woodward, Paul and Colella, Phillip. **The numerical simulation of two-dimensional fluid flow with strong shocks**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(84)90142-6) · [Full text or implementation reference](https://www.nas.nasa.gov/LAVA/unst_docs/tutorials/double_mach/double_mach/)

DOI identifies the original 1984 paper; linked NASA tutorial is a later setup reference. This edition computes a first-order 2D HLL Double Mach Reflection baseline, not the original PPM figure. Forward-facing step remains future work.

## 1987 · eno1987

Harten, Amiram and Engquist, Bjorn and Osher, Stanley and Chakravarthy, Sukumar R.. **Uniformly high order accurate essentially non-oscillatory schemes, III**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(87)90031-3) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/0021999187900313)

Original publication in 1987, distinct from the 1997 reprint. A standalone ENO implementation is planned; this edition implements WENO5-JS.

## 1987 · turkel1987

Turkel, Eli. **Preconditioned methods for solving the incompressible and low speed compressible equations**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(87)90084-2) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/0021999187900842)

Publisher bibliographic record and abstract. Low-speed PDE preconditioning is discussed as future work and is distinct from the Jacobi matrix-scaling example.

## 1988 · einfeldt1988

Einfeldt, Bernd. **On Godunov-Type Methods for Gas Dynamics**. SIAM Journal on Numerical Analysis.

[Original bibliographic record](https://doi.org/10.1137/0725021) · [Full text or implementation reference](https://epubs.siam.org/doi/abs/10.1137/0725021)

Publisher bibliographic record and abstract. Background for Einfeldt-type wave-speed estimates in Euler HLLE.

## 1988 · evans1988

Evans, Charles R. and Hawley, John F.. **Simulation of magnetohydrodynamic flows: A constrained transport method**. The Astrophysical Journal.

[Original bibliographic record](https://doi.org/10.1086/166684) · [Full text or implementation reference](https://adsabs.harvard.edu/pdf/1988ApJ...332..659E)

Publicly accessible original paper. This edition uses a Cartesian flux-CT-type construction and does not reproduce every part of the original method.

## 1988 · shu1988

Shu, Chi-Wang and Osher, Stanley. **Efficient implementation of essentially non-oscillatory shock-capturing schemes**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(88)90177-5) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/0021999188901775)

Publisher bibliographic record and abstract. Background on TVD Runge–Kutta and flux-based constructions.

## 1989 · cockburn1989

Cockburn, Bernardo and Shu, Chi-Wang. **TVB Runge-Kutta local projection discontinuous Galerkin finite element method for conservation laws. II. General framework**. Mathematics of Computation.

[Original bibliographic record](https://doi.org/10.1090/S0025-5718-1989-0983311-4) · [Full text or implementation reference](https://www-users.cse.umn.edu/~cockburn/lecture_notes/DG-4.pdf)

The DOI identifies the original paper; the linked source is a later set of author lecture notes. This edition implements DG for smooth advection without a TVB limiter.

## 1989 · shu1989

Shu, Chi-Wang and Osher, Stanley. **Efficient implementation of essentially non-oscillatory shock-capturing schemes, II**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(89)90222-2) · [Full text or implementation reference](https://academic.oup.com/mnras/article/512/1/1430/6530656)

The DOI identifies the original paper. Initial-condition parameters follow the later Quokka paper. Digitized comparisons with original figures have not been performed.

## 1991 · einfeldt1991

Einfeldt, Bernd and Munz, Claus-Dieter and Roe, Philip L. and Sjögreen, Björn. **On Godunov-type methods near low densities**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(91)90211-3) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/0021999191902113)

Publisher bibliographic record and abstract. Background on low-density positivity; this edition uses the standard Toro formulation of the 1–2–3 problem.

## 1991 · jameson1991

Jameson, Antony. **Time dependent calculations using multigrid, with applications to unsteady flows past airfoils and wings**. 10th AIAA Computational Fluid Dynamics Conference.

[Original bibliographic record](https://doi.org/10.2514/6.1991-1596) · [Full text or implementation reference](https://cfd.ku.edu/JRV/Martinelli.pdf)

The DOI identifies the original paper; the linked source is a later exposition by a coauthor. Dual time stepping here is a minimal linear-advection model.

## 1994 · hllc1994

Toro, E. F. and Spruce, M. and Speares, W.. **Restoration of the contact surface in the HLL-Riemann solver**. Shock Waves.

[Original bibliographic record](https://doi.org/10.1007/BF01414629) · [Full text or implementation reference](https://doi.org/10.1007/BF01414629)

Publisher bibliographic record and abstract. This edition uses HLLC with Davis-type wave speeds and does not implement every original wave-speed estimate or WAF construction.

## 1994 · quirk1994

Quirk, James J.. **A contribution to the great Riemann solver debate**. International Journal for Numerical Methods in Fluids.

[Original bibliographic record](https://doi.org/10.1002/fld.1650180603) · [Full text or implementation reference](https://onlinelibrary.wiley.com/doi/10.1002/fld.1650180603)

Publisher record and abstract. Background for shock instability and complementary fluxes. Controlled odd-even and blunt-body carbuncle experiments remain future work.

## 1994 · templates1994

Barrett, Richard and Berry, Michael and Chan, Tony F. and Demmel, James and Donato, June and Dongarra, Jack and Eijkhout, Victor and Pozo, Roldan and Romine, Charles and van der Vorst, Henk. **Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods**. SIAM.

[Original bibliographic record](https://www.netlib.org/templates/templates.html) · [Full text or implementation reference](https://www.netlib.org/templates/templates.html)

Publicly available author-side reference material for Jacobi, Gauss–Seidel, preconditioning, and multigrid.

## 1994 · weno1994

Liu, Xu-Dong and Osher, Stanley and Chan, Tony. **Weighted Essentially Non-oscillatory Schemes**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1006/jcph.1994.1187) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/S0021999184711879)

Publisher bibliographic record and abstract. Historical introduction to WENO; the weights implemented here are Jiang–Shu (1996).

## 1996 · jiang1996

Jiang, Guang-Shan and Shu, Chi-Wang. **Efficient Implementation of Weighted ENO Schemes**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1006/jcph.1996.0130) · [Full text or implementation reference](https://www.ece.uvic.ca/~bctill/papers/numacoust/Jiang_Shu_1996.pdf)

Publicly accessible original paper. Reference for WENO5-JS flux reconstruction, smoothness indicators, and nonlinear weights.

## 1996 · shewchuk1996

Shewchuk, Jonathan Richard. **Triangle: Engineering a 2D Quality Mesh Generator and Delaunay Triangulator**. Springer.

[Original bibliographic record](https://www.cs.cmu.edu/~quake/tripaper/triangle0.html) · [Full text or implementation reference](https://www.cs.cmu.edu/~quake/tripaper/triangle0.html)

Author-hosted paper. Mesh-generation reading reference; the example meshes use Matplotlib triangulation and do not invoke Triangle.

## 2000 · toth2000

Tóth, Gábor. **The ∇·B = 0 Constraint in Shock-Capturing Magnetohydrodynamics Codes**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1006/jcph.2000.6519) · [Full text or implementation reference](https://public.websites.umich.edu/~gtoth/Papers/Toth2000_divb.pdf)

Author-hosted original paper. Reference for CT variants and differences between discrete divergence operators.

## 2001 · pandolfi2001

Pandolfi, Maurizio and D’Ambrosio, Domenic. **Numerical Instabilities in Upwind Methods: Analysis and Cures for the “Carbuncle” Phenomenon**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1006/jcph.2000.6652) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/S002199910096652X)

Publisher record and abstract. Linearized shock-instability analysis and localized cures; the proposed methods are not implemented in this edition.

## 2002 · dedner2002

Dedner, Andreas and Kemm, Friedemann and Kröner, Dietmar and Munz, Claus-Dieter and Schnitzer, Thomas and Wesenberg, Matthias. **Hyperbolic Divergence Cleaning for the MHD Equations**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1006/jcph.2001.6961) · [Full text or implementation reference](https://www.tp4.ruhr-uni-bochum.de/~sw/papers/JCP2002.6961.pdf)

Publicly accessible original paper, published in 2002 despite 2001 appearing in the DOI. This edition uses a simplified GLM model with fixed cleaning speed.

## 2002 · leveque2002

LeVeque, Randall J.. **Finite Volume Methods for Hyperbolic Problems**. Cambridge University Press.

[Original bibliographic record](https://doi.org/10.1017/CBO9780511791253) · [Full text or implementation reference](https://www.cambridge.org/core/books/finite-volume-methods-for-hyperbolic-problems/97D5D1ACB1926DA1D4D52EAD6909E2B9)

Publisher bibliographic record and abstract. Background for conservation laws and shallow-water implementations.

## 2006 · abgrall2006

Abgrall, Rémi. **Residual distribution schemes: Current status and future trends**. Computers & Fluids.

[Original bibliographic record](https://doi.org/10.1016/j.compfluid.2005.01.007) · [Full text or implementation reference](https://www.math.u-bordeaux.fr/~rabgrall/mes_papiers/caf_2006_35.pdf)

Author-hosted review. The 2006 date identifies the review, rather than the origin of residual distribution. This edition implements only 1D scalar RD.

## 2008 · nishikawa2008

Nishikawa, Hiroaki and Kitamura, Keiichi. **Very simple, carbuncle-free, boundary-layer-resolving, rotated-hybrid Riemann solvers**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/j.jcp.2007.11.003) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/abs/pii/S0021999107004822)

Publisher bibliographic record and abstract. The 2D rotated solver and carbuncle tests are future work.

## 2009 · toro2009

Toro, Eleuterio F.. **Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction**. Springer.

[Original bibliographic record](https://doi.org/10.1007/b79761) · [Full text or implementation reference](https://doi.org/10.1007/b79761)

Publisher bibliographic record. Background for exact Riemann solutions and the standard double-rarefaction setup.

## 2009 · williams2009

Williams, Paul D.. **A Proposed Modification to the Robert–Asselin Time Filter**. Monthly Weather Review.

[Original bibliographic record](https://doi.org/10.1175/2009MWR2724.1) · [Full text or implementation reference](https://journals.ametsoc.org/abstract/journals/mwre/137/8/2009mwr2724.1.xml)

Publisher record identifies the time-filter paper. The ODE laboratory uses unfiltered leapfrog with RK4 startup and does not implement this filter.

## 2016 · fitzpatrick2016

Fitzpatrick, Richard. **Fluid Equations in Cylindrical Coordinates**. University of Texas at Austin.

[Original bibliographic record](https://farside.ph.utexas.edu/teaching/336L/Fluid/node20.html) · [Full text or implementation reference](https://farside.ph.utexas.edu/teaching/336L/Fluid/node20.html)

Author lecture notes, dated January 22, 2016. Reference for cylindrical fluid operators; the atlas declares its bulk-viscosity and orthonormal-component conventions separately.

## 2022 · quokka2022

Wibking, Benjamin D. and Krumholz, Mark R.. **quokka: a code for two-moment AMR radiation hydrodynamics on GPUs**. Monthly Notices of the Royal Astronomical Society.

[Original bibliographic record](https://doi.org/10.1093/mnras/stac439) · [Full text or implementation reference](https://academic.oup.com/mnras/article/512/1/1430/6530656)

Section 3.1.5 of the public paper is the reference for the adopted Shu–Osher parameters. The Quokka code itself is not reproduced.

## 2026 · powell2026

Powell, Ken. **Philip Lawrence Roe, Professor Emeritus of Aerospace Engineering at the University of Michigan, passed away April 26, 2026, at the age of 87**. University of Michigan Aerospace Engineering.

[Original bibliographic record](https://aero.engin.umich.edu/2026/04/29/philip-lawrence-roe-professor-emeritus-of-aerospace-engineering-at-the-university-of-michigan-passed-away-april-26-2026-at-the-age-of-87/) · [Full text or implementation reference](https://aero.engin.umich.edu/2026/04/29/philip-lawrence-roe-professor-emeritus-of-aerospace-engineering-at-the-university-of-michigan-passed-away-april-26-2026-at-the-age-of-87/)

Official university memorial published April 29, 2026. A biographical source, not a numerical-method research paper.
