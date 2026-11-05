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

## 1974 · vanleer1974

van Leer, Bram. **Towards the ultimate conservative difference scheme. II. Monotonicity and conservation combined in a second-order scheme**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(74)90019-9) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/0021999174900199)

Publisher bibliographic record inspected. Historical monotonicity and conservative second-order reconstruction; not a claim to reproduce the original algorithm.

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

Publisher bibliographic record and abstract. This edition uses selectable-limiter MUSCL with SSPRK3, rather than reproducing the original Lagrangian/remap construction.

## 1981 · hockney1981book

Hockney, R. W. and Eastwood, J. W.. **Computer Simulation Using Particles**. McGraw-Hill.

[Original bibliographic record](https://doi.org/10.1201/9780367806934) · [Full text or implementation reference](https://doi.org/10.1201/9780367806934)

Original book date is 1981, as cited by Barnes and Hut (1986); DOI identifies a later Taylor & Francis reissue. Reference for particle-mesh methods and isolated doubled-domain convolution; the self-cell kernel convention is stated separately in our code.

## 1981 · hockney1981p3m

Hockney, R. W.. **The P³M Code**. CCP5 Information Quarterly, June 1981.

[Original bibliographic record](https://www.ccp5.ac.uk/wp-content/uploads/2023/03/CCP5_Newsletter_1981_06_01.pdf) · [Full text or implementation reference](https://www.ccp5.ac.uk/wp-content/uploads/2023/03/CCP5_Newsletter_1981_06_01.pdf)

Original newsletter scan hosted by CCP5. Describes mesh forces plus short-range pair corrections. A full P3M solver is not implemented here.

## 1981 · roe1981

Roe, Philip L.. **Approximate Riemann solvers, parameter vectors, and difference schemes**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(81)90128-5) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/0021999181901285)

Publisher bibliographic record and abstract. This edition implements 1D Euler with quadratic entropy smoothing of acoustic eigenvalues.

## 1983 · hll1983

Harten, Amiram and Lax, Peter D. and van Leer, Bram. **On Upstream Differencing and Godunov-Type Schemes for Hyperbolic Conservation Laws**. SIAM Review.

[Original bibliographic record](https://doi.org/10.1137/1025002) · [Full text or implementation reference](https://www.ece.uvic.ca/~bctill/papers/numacoust/Harten_etal_1983.pdf)

Publicly accessible original paper. Background on HLL; the hll implementation here uses Davis-type minimum/maximum acoustic wave speeds.

## 1984 · sweby1984

Sweby, P. K.. **High Resolution Schemes Using Flux Limiters for Hyperbolic Conservation Laws**. SIAM Journal on Numerical Analysis.

[Original bibliographic record](https://doi.org/10.1137/0721062) · [Full text or implementation reference](https://epubs.siam.org/doi/10.1137/0721062)

Publisher record and abstract inspected. Historical scalar TVD flux-limiter framework, including the compressive limiter due to Roe. The notebook uses explicitly documented slope conventions and a separate MUSCL/SSPRK3 operator.

## 1984 · woodward1984

Woodward, Paul and Colella, Phillip. **The numerical simulation of two-dimensional fluid flow with strong shocks**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(84)90142-6) · [Full text or implementation reference](https://www.nas.nasa.gov/LAVA/unst_docs/tutorials/double_mach/double_mach/)

DOI identifies the original 1984 paper; linked NASA tutorial is a later setup reference. This edition computes a first-order 2D HLL Double Mach Reflection baseline, not the original PPM figure. Forward-facing step remains future work.

## 1986 · barnes1986

Barnes, Josh and Hut, Piet. **A hierarchical O(N log N) force-calculation algorithm**. Nature.

[Original bibliographic record](https://doi.org/10.1038/324446a0) · [Full text or implementation reference](https://www.nature.com/articles/324446a0)

Original publisher record. The educational octree uses a geometric opening criterion and compares monopole/full second-moment forces with an identical softened direct sum.

## 1987 · eno1987

Harten, Amiram and Engquist, Bjorn and Osher, Stanley and Chakravarthy, Sukumar R.. **Uniformly high order accurate essentially non-oscillatory schemes, III**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(87)90031-3) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/0021999187900313)

Original publication in 1987, distinct from the 1997 reprint. A standalone ENO implementation is planned; this edition implements WENO5-JS.

## 1987 · greengard1987

Greengard, L. and Rokhlin, V.. **A fast algorithm for particle simulations**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(87)90140-9) · [Full text or implementation reference](https://web.stanford.edu/class/cme324/classics/greengard-rokhlin.pdf)

Original paper hosted by a university course. FMM reading reference; multipole-to-local translations and an FMM solver are not implemented here.

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

## 1989 · cockburn1989tvb

Cockburn, Bernardo and Shu, Chi-Wang. **TVB Runge-Kutta local projection discontinuous Galerkin finite element method for conservation laws. II. General framework**. Mathematics of Computation.

[Original bibliographic record](https://doi.org/10.1090/S0025-5718-1989-0983311-4) · [Full text or implementation reference](https://www.ams.org/mcom/1989-52-186/S0025-5718-1989-0983311-4/)

Historical RKDG/TVB reference. Publisher full-text retrieval was unavailable in this session. This edition demonstrates the modified-minmod operation in scalar finite volumes, not the complete RKDG framework or its theorem.

## 1989 · shu1989

Shu, Chi-Wang and Osher, Stanley. **Efficient implementation of essentially non-oscillatory shock-capturing schemes, II**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/0021-9991(89)90222-2) · [Full text or implementation reference](https://academic.oup.com/mnras/article/512/1/1430/6530656)

The DOI identifies the original paper. Initial-condition parameters follow the later Quokka paper. Digitized comparisons with original figures have not been performed.

## 1990 · yoshida1990

Yoshida, Haruo. **Construction of higher order symplectic integrators**. Physics Letters A.

[Original bibliographic record](https://doi.org/10.1016/0375-9601(90)90092-3) · [Full text or implementation reference](https://tlakoba.w3.uvm.edu/math6737/for_final_topics/SSM_1990_Yoshida.pdf)

Original paper hosted by a university course. This edition implements the fourth-order triple composition of symmetric Verlet steps on two smooth 1-DOF Hamiltonians.

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

## 2001 · gottlieb2001ssp

Gottlieb, Sigal and Shu, Chi-Wang and Tadmor, Eitan. **Strong Stability-Preserving High-Order Time Discretization Methods**. SIAM Review.

[Original bibliographic record](https://doi.org/10.1137/S003614450036757X) · [Full text or implementation reference](https://www.math.umd.edu/~tadmor/pub/linear-stability/Gottlieb-Shu-Tadmor.SIREV-01.pdf)

Author-hosted original manuscript inspected. Conditional inheritance of forward-Euler convex stability, and the distinction between linear and nonlinear SSP. The atlas verifies full-tableau inequalities for its explicit RK methods.

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

## 2002 · spiteri2002ssp

Spiteri, Raymond J. and Ruuth, Steven J.. **A New Class of Optimal High-Order Strong-Stability-Preserving Time Discretization Methods**. SIAM Journal on Numerical Analysis.

[Original bibliographic record](https://doi.org/10.1137/S0036142901389025) · [Full text or implementation reference](https://epubs.siam.org/doi/abs/10.1137/S0036142901389025)

Publisher record and abstract inspected. SSP methods with more stages than their order. The implemented five-stage fourth-order coefficients are taken from the later author-hosted Gottlieb–Ketcheson–Shu review, rather than asserting direct full-text reproduction of this paper.

## 2003 · hairer2003

Hairer, Ernst and Lubich, Christian and Wanner, Gerhard. **Geometric numerical integration illustrated by the Störmer–Verlet method**. Acta Numerica.

[Original bibliographic record](https://doi.org/10.1017/S0962492902000144) · [Full text or implementation reference](https://jduarte.physics.ucsd.edu/phys141/_downloads/0b06fe9fe40aeb83699c2bc17b71a93d/stoermer-verlet.pdf)

Original article hosted by a university course. Reference for symplecticity, reversibility, modified equations, and conditional long-time energy estimates; no general exact-energy claim is made.

## 2005 · springel2005

Springel, Volker. **The cosmological simulation code GADGET-2**. Monthly Notices of the Royal Astronomical Society.

[Original bibliographic record](https://doi.org/10.1111/j.1365-2966.2005.09655.x) · [Full text or implementation reference](https://arxiv.org/abs/astro-ph/0505010)

Author preprint and publisher record. Reference for TreePM force splitting; the separate PM and Tree laboratories do not implement the GADGET code or a complete TreePM pipeline.

## 2006 · abgrall2006

Abgrall, Rémi. **Residual distribution schemes: Current status and future trends**. Computers & Fluids.

[Original bibliographic record](https://doi.org/10.1016/j.compfluid.2005.01.007) · [Full text or implementation reference](https://www.math.u-bordeaux.fr/~rabgrall/mes_papiers/caf_2006_35.pdf)

Author-hosted review. The 2006 date identifies the review, rather than the origin of residual distribution. This edition implements only 1D scalar RD.

## 2008 · nishikawa2008

Nishikawa, Hiroaki and Kitamura, Keiichi. **Very simple, carbuncle-free, boundary-layer-resolving, rotated-hybrid Riemann solvers**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/j.jcp.2007.11.003) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/abs/pii/S0021999107004822)

Publisher bibliographic record and abstract. The 2D rotated solver and carbuncle tests are future work.

## 2009 · gottlieb2009ssp

Gottlieb, Sigal and Ketcheson, David I. and Shu, Chi-Wang. **High Order Strong Stability Preserving Time Discretizations**. Journal of Scientific Computing.

[Original bibliographic record](https://doi.org/10.1007/s10915-008-9239-z) · [Full text or implementation reference](https://www.davidketcheson.info/assets/papers/sspreview.pdf)

Author-hosted 2008 draft of the 2009 review inspected. Section 3.1 supplies the SSPRK(5,4) decimal coefficients; the atlas converts its state combinations to increments and uses the conservative rounded bound C=1.508. SSP order barriers, low-storage, and alternative families are reading context.

## 2009 · koyama2009

Koyama, Hiroshi and Ostriker, Eve C.. **Gas Properties and Implications for Galactic Star Formation in Numerical Models of the Turbulent, Multiphase Interstellar Medium**. The Astrophysical Journal.

[Original bibliographic record](https://doi.org/10.1088/0004-637X/693/2/1316) · [Full text or implementation reference](https://arxiv.org/abs/0812.1846)

Published in 2009, with a December 2008 preprint. Section 2.3 and Appendix A give the Cartesian disk-potential FFT method. Our independent kernel laboratory distinguishes the sampled DFT from a continuous Fourier coefficient and does not reproduce the ISM simulations.

## 2009 · toro2009

Toro, Eleuterio F.. **Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction**. Springer.

[Original bibliographic record](https://doi.org/10.1007/b79761) · [Full text or implementation reference](https://doi.org/10.1007/b79761)

Publisher bibliographic record. Background for exact Riemann solutions and the standard double-rarefaction setup.

## 2009 · williams2009

Williams, Paul D.. **A Proposed Modification to the Robert–Asselin Time Filter**. Monthly Weather Review.

[Original bibliographic record](https://doi.org/10.1175/2009MWR2724.1) · [Full text or implementation reference](https://journals.ametsoc.org/abstract/journals/mwre/137/8/2009mwr2724.1.xml)

Publisher record identifies the time-filter paper. The ODE laboratory uses unfiltered leapfrog with RK4 startup and does not implement this filter.

## 2010 · zhangshu2010euler

Zhang, Xiangxiong and Shu, Chi-Wang. **On positivity-preserving high order discontinuous Galerkin schemes for compressible Euler equations on rectangular meshes**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/j.jcp.2010.08.016) · [Full text or implementation reference](https://www.math.purdue.edu/~zhan1966/research/paper/euler.pdf)

Author-hosted manuscript inspected. Convex admissible Euler states, mean-preserving limiting, and additional flux, quadrature, CFL, and SSP requirements. The atlas implements only a common-state reconstruction scaling building block, not the full time-update scheme.

## 2016 · fitzpatrick2016

Fitzpatrick, Richard. **Fluid Equations in Cylindrical Coordinates**. University of Texas at Austin.

[Original bibliographic record](https://farside.ph.utexas.edu/teaching/336L/Fluid/node20.html) · [Full text or implementation reference](https://farside.ph.utexas.edu/teaching/336L/Fluid/node20.html)

Author lecture notes, dated January 22, 2016. Reference for cylindrical fluid operators; the atlas declares its bulk-viscosity and orthonormal-component conventions separately.

## 2018 · kuya2018

Kuya, Yuichi and Totani, Kosuke and Kawai, Soshi. **Kinetic energy and entropy preserving schemes for compressible flows by split convective forms**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/j.jcp.2018.08.058) · [Full text or implementation reference](https://www.iccfd.org/iccfd11/assets/pdf/papers/ICCFD11_Paper-0401.pdf)

DOI identifies the original 2018 paper. The authors’ 2022 conference explanation, Eq. (9), is the accessible implementation source for our second-order arithmetic-mean Cartesian baseline. Entropy is not claimed exact to roundoff; no shock stabilization is implemented.

## 2021 · shima2021

Shima, Nao and Kuya, Yuichi and Tamaki, Yoshiharu and Kawai, Soshi. **Preventing spurious pressure oscillations in split convective form discretization for compressible flows**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/j.jcp.2020.110060) · [Full text or implementation reference](https://kyushu-u.elsevierpure.com/en/publications/preventing-spurious-pressure-oscillations-in-split-convective-for/)

Author-university publication record; published in 2021 despite 2020 in the DOI. Pressure-equilibrium-preserving variants are discussed but are not the original arithmetic-mean flux used here.

## 2022 · kuya2022keep

Kuya, Yuichi and Kawai, Soshi. **Stable and non-dissipative kinetic-energy and entropy preserving (KEEP) schemes for compressible flows**. Eleventh International Conference on Computational Fluid Dynamics.

[Original bibliographic record](https://www.iccfd.org/iccfd11/assets/pdf/papers/ICCFD11_Paper-0401.pdf) · [Full text or implementation reference](https://www.iccfd.org/iccfd11/assets/pdf/papers/ICCFD11_Paper-0401.pdf)

Official conference paper, inspected in full. Section 2.2 Eq. (9) specifies the implemented original Cartesian flux; Section 2.1 explicitly limits exact entropy-conservation claims. Other extensions in the paper are not implemented here.

## 2022 · quokka2022

Wibking, Benjamin D. and Krumholz, Mark R.. **quokka: a code for two-moment AMR radiation hydrodynamics on GPUs**. Monthly Notices of the Royal Astronomical Society.

[Original bibliographic record](https://doi.org/10.1093/mnras/stac439) · [Full text or implementation reference](https://academic.oup.com/mnras/article/512/1/1430/6530656)

Section 3.1.5 of the public paper is the reference for the adopted Shu–Osher parameters. The Quokka code itself is not reproduced.

## 2022 · tamaki2022

Tamaki, Yoshiharu and Kuya, Yuichi and Kawai, Soshi. **Comprehensive analysis of entropy conservation property of non-dissipative schemes for compressible flows: KEEP scheme redefined**. Journal of Computational Physics.

[Original bibliographic record](https://doi.org/10.1016/j.jcp.2022.111494) · [Full text or implementation reference](https://kyushu-u.elsevierpure.com/en/publications/comprehensive-analysis-of-entropy-conservation-property-of-non-di/)

Author-university record and abstract. Analyzes entropy-error terms and redefined KEEP variants with adjustable expansion order; these variants are not implemented in the original-flux exhibit.

## 2024 · asada2024

Asada, Hiroyuki and Maruyama, Kanako and Kawai, Soshi. **Temporal discretization for improving kinetic-energy and entropy preservation properties in KEEP schemes**. Computers & Fluids.

[Original bibliographic record](https://doi.org/10.1016/j.compfluid.2023.106143) · [Full text or implementation reference](https://www.sciencedirect.com/science/article/pii/S0045793023003687)

Publisher record and abstract. Published in 2024 despite 2023 in the DOI. The auxiliary-variable temporal method is not implemented; the exhibit uses classical RK4 with a time-refinement diagnostic.

## 2026 · amrvaclimiters

MPI-AMRVAC Team. **Slope Limiters**. .

[Original bibliographic record](https://amrvac.org/md_doc_2limiter.html) · [Full text or implementation reference](https://amrvac.org/md_doc_2limiter.html)

Official code documentation inspected in November 2026; access year only. Implementation notes on minmod, Superbee, MC, van Leer, van Albada variants, and regularization. The atlas uses an explicitly clipped van Albada form without epsilon smoothing.

## 2026 · clawpacklimiters

Clawpack Development Team. **Pyclaw Limiters**. .

[Original bibliographic record](https://www.clawpack.org/pyclaw/evolve/limiters.html) · [Full text or implementation reference](https://www.clawpack.org/pyclaw/evolve/limiters.html)

Official implementation documentation inspected in November 2026; this is an access-year record, not an invention date. Used to distinguish common limiter functions and wave-limiting conventions from the atlas slope reconstruction.

## 2026 · numipediark

Ketcheson, David I.. **Numipedia: Runge–Kutta method records**. .

[Original bibliographic record](https://ketch.github.io/numipedia/methods/RK44.html) · [Full text or implementation reference](https://ketch.github.io/numipedia/methods/RK44.html)

Author-maintained coefficient and stability records inspected in November 2026; access year, not an invention date. RK44, SSPRK22, and SSPRK43 records cross-check tableaus, scalar polynomials, and absolute-monotonicity radii.

## 2026 · powell2026

Powell, Ken. **Philip Lawrence Roe, Professor Emeritus of Aerospace Engineering at the University of Michigan, passed away April 26, 2026, at the age of 87**. University of Michigan Aerospace Engineering.

[Original bibliographic record](https://aero.engin.umich.edu/2026/04/29/philip-lawrence-roe-professor-emeritus-of-aerospace-engineering-at-the-university-of-michigan-passed-away-april-26-2026-at-the-age-of-87/) · [Full text or implementation reference](https://aero.engin.umich.edu/2026/04/29/philip-lawrence-roe-professor-emeritus-of-aerospace-engineering-at-the-university-of-michigan-passed-away-april-26-2026-at-the-age-of-87/)

Official university memorial published April 29, 2026. A biographical source, not a numerical-method research paper.
