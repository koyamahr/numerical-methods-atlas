# Textbooks: where to look next

A working bookshelf for this atlas. Choose a book by the question you need to answer; this is a reading guide, not a ranking. Bibliographic years below identify the cited editions, not the invention dates of algorithms.

The links lead to publisher records or author-maintained pages. We checked edition metadata and available descriptions or contents, not every derivation in every book. Chapter suggestions describe the atlas connection; they do not claim that all of a textbook has been implemented.

**A short starting path:** Hirsch for the CFD framework; LeVeque for conservation laws and finite-volume reasoning; Toro for Riemann solvers; Patankar for pressure–velocity coupling; Saad for sparse iterative solves. Return to original papers when tracing a particular algorithm.

[Search the full reference library](#/references) · [All cataloged books](#/references?q=type%3Abook) · [Download BibTeX](../references.bib)

## CFD foundations and incompressible flow {#cfd-foundations}

### Hirsch {#hirsch2007}

Hirsch, Charles. **Numerical Computation of Internal and External Flows: The Fundamentals of Computational Fluid Dynamics**. Butterworth-Heinemann, 2007 · edition 2.

Use this for the CFD framework: equations, grid properties, consistency, stability, discretization and solution procedures. The cited 2007 book is the second-edition fundamentals volume.

Atlas connections: [Differences, CFL, von Neumann analysis, and Lax](stability.md) · [Structured, unstructured, and triangular meshes](meshes.md) · [Time integration and leapfrog](time-integration.md).

[Publisher / bibliographic record](https://doi.org/10.1016/B978-0-7506-6594-0.X5037-1) · [Author / source page](https://www.sciencedirect.com/book/monograph/9780750665940/numerical-computation-of-internal-and-external-flows) · `hirsch2007`

### Fletcher / Volume I {#fletcher1991v1}

Fletcher, Clive A. J. **Computational Techniques for Fluid Dynamics 1: Fundamental and General Techniques**. Springer, 1991 · edition 2.

Use Volume I for PDE classification, weighted residual methods, steady and diffusion problems, and linear/nonlinear convection. It supplies the common numerical tools before the flow-specific algorithms of Volume II.

Atlas connections: [Differences, CFL, von Neumann analysis, and Lax](stability.md) · [Continuous finite elements: from weak form to sparse assembly](fem.md) · [Diffusion, elliptic equations, boundary conditions, and iteration](elliptic.md).

[Publisher / bibliographic record](https://doi.org/10.1007/978-3-642-58229-5) · [Author / source page](https://link.springer.com/book/10.1007/978-3-642-58229-5) · `fletcher1991v1`

### Fletcher / Volume II {#fletcher1991v2}

Fletcher, Clive A. J. **Computational Techniques for Fluid Dynamics 2: Specific Techniques for Different Flow Categories**. Springer, 1991 · edition 2.

Use Volume II to connect the general techniques of Volume I to different flow-equation categories and their computational solution procedures. Read assumptions and boundary conditions alongside each algorithm.

Atlas connections: [Incompressible flow: project with compatible discrete operators](incompressible.md) · [Preconditioning, dual time stepping, and residual distribution](advanced.md) · [Polar and cylindrical coordinates: tensors and viscosity](coordinates-viscosity.md).

[Publisher / bibliographic record](https://doi.org/10.1007/978-3-642-58239-4) · [Author / source page](https://link.springer.com/book/10.1007/978-3-642-58239-4) · `fletcher1991v2`

### Ferziger · Perić · Street {#ferziger2020}

Ferziger, Joel H.; Perić, Milovan; Street, Robert L. **Computational Methods for Fluid Dynamics**. Springer, 2020 · edition 4.

Use this when connecting discrete operators to a practical CFD solution procedure, especially incompressible pressure–velocity coupling and boundary conditions.

Atlas connections: [Incompressible flow: project with compatible discrete operators](incompressible.md) · [Polar and cylindrical coordinates: tensors and viscosity](coordinates-viscosity.md).

[Publisher / bibliographic record](https://doi.org/10.1007/978-3-319-99693-6) · [Author / source page](https://link.springer.com/book/10.1007/978-3-319-99693-6) · `ferziger2020`

### Patankar {#patankar1980}

Patankar, Suhas V. **Numerical Heat Transfer and Fluid Flow**. CRC Press (current publisher record), 1980.

Use this for the physical logic of control-volume balances and SIMPLE-type pressure–velocity coupling. Keep the book exposition separate from the original algorithm papers.

Atlas connections: [Incompressible flow: project with compatible discrete operators](incompressible.md) · [Euler reconstruction: PPM, characteristics, WENO-Z and AUSM](reconstruction.md).

[Publisher / bibliographic record](https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow-1st-Edition/Patankar/p/book/9780891165224) · [Author / source page](https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow-1st-Edition/Patankar/p/book/9780891165224) · `patankar1980`

## Conservation laws, Riemann solvers and shocks {#hyperbolic}

### LeVeque / finite volume {#leveque2002}

LeVeque, Randall J. **Finite Volume Methods for Hyperbolic Problems**. Cambridge University Press, 2002.

Use this for weak solutions, finite-volume reasoning, wave propagation, limiters and multidimensional conservation laws. Companion Clawpack material connects the theory to computation.

Atlas connections: [Euler reconstruction: PPM, characteristics, WENO-Z and AUSM](reconstruction.md) · [Slope limiters: minmod, Superbee, MC, van Leer, and van Albada](limiters.md) · [Equation gallery: choose the equation before the algorithm](equation-gallery.md).

[Publisher / bibliographic record](https://doi.org/10.1017/CBO9780511791253) · [Author / source page](https://www.cambridge.org/core/books/finite-volume-methods-for-hyperbolic-problems/97D5D1ACB1926DA1D4D52EAD6909E2B9) · `leveque2002`

### Toro {#toro2009}

Toro, Eleuterio F. **Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction**. Springer, 2009 · edition 3.

Use this when deriving or comparing exact and approximate Euler Riemann solvers, contact waves and high-resolution shock-capturing methods.

Atlas connections: [Preconditioning, dual time stepping, and residual distribution](advanced.md) · [Euler reconstruction: PPM, characteristics, WENO-Z and AUSM](reconstruction.md) · [Benchmark library](benchmarks.md).

[Publisher / bibliographic record](https://doi.org/10.1007/b79761) · [Author / source page](https://doi.org/10.1007/b79761) · `toro2009`

## Finite differences and linear algebra {#common-numerics}

### LeVeque / finite differences {#leveque2007}

LeVeque, Randall J. **Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems**. SIAM, 2007.

Use this for the consistency–stability–convergence chain, ordinary differential equations, boundary-value problems and finite-difference PDE solvers.

Atlas connections: [A-stability, L-stability and error norms](accuracy-stability.md) · [Time integration and leapfrog](time-integration.md) · [Diffusion, elliptic equations, boundary conditions, and iteration](elliptic.md).

[Publisher / bibliographic record](https://doi.org/10.1137/1.9780898717839) · [Author / source page](https://staff.washington.edu/rjl/booksnotes.html) · `leveque2007`

### Golub · Van Loan {#golub2013}

Golub, Gene H.; Van Loan, Charles F. **Matrix Computations**. Johns Hopkins University Press, 2013 · edition 4.

Use this for conditioning, stable matrix factorizations, least squares and eigenproblems before choosing a solver solely by its name.

Atlas connections: [Sparse and nonlinear systems: measure the actual residual](sparse-nonlinear.md) · [Diffusion, elliptic equations, boundary conditions, and iteration](elliptic.md).

[Publisher / bibliographic record](https://doi.org/10.1137/1.9781421407944) · [Author / source page](https://epubs.siam.org/doi/book/10.1137/1.9781421407944) · `golub2013`

### Saad {#saad2003book}

Saad, Yousef. **Iterative Methods for Sparse Linear Systems**. SIAM, 2003 · edition 2.

Use this for Krylov subspaces, GMRES, BiCG-family methods and preconditioners. The author provides the second-edition text and corrections.

Atlas connections: [Sparse and nonlinear systems: measure the actual residual](sparse-nonlinear.md) · [Diffusion, elliptic equations, boundary conditions, and iteration](elliptic.md).

[Publisher / bibliographic record](https://doi.org/10.1137/1.9780898718003) · [Author / source page](https://www-users.cse.umn.edu/~saad/books.html) · `saad2003book`

### Barrett et al. / Templates {#templates1994}

Barrett, Richard; Berry, Michael; Chan, Tony F.; Demmel, James; Donato, June; Dongarra, Jack; Eijkhout, Victor; Pozo, Roldan; Romine, Charles; van der Vorst, Henk. **Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods**. SIAM, 1994.

Use this open reference as a compact algorithm-and-selection companion for iterative linear solvers, with attention to matrix assumptions.

Atlas connections: [Sparse and nonlinear systems: measure the actual residual](sparse-nonlinear.md) · [Diffusion, elliptic equations, boundary conditions, and iteration](elliptic.md).

[Publisher / bibliographic record](https://www.netlib.org/templates/templates.html) · [Author / source page](https://www.netlib.org/templates/templates.html) · `templates1994`

## Spectral bases and discontinuous Galerkin {#high-order}

### Trefethen {#trefethen2000}

Trefethen, Lloyd N. **Spectral Methods in MATLAB**. SIAM, 2000.

Use this for spectral differentiation, Fourier/Chebyshev examples and short reproducible programs. Supplement its limited barycentric-interpolation coverage.

Atlas connections: [Interactive experiment guide](experiments.md) · [Orthogonal polynomials and mesh basis functions](basis-functions.md).

[Publisher / bibliographic record](https://doi.org/10.1137/1.9780898719598) · [Author / source page](https://people.maths.ox.ac.uk/trefethen/spectral.html) · `trefethen2000`

### Hesthaven · Warburton {#hesthaven2008book}

Hesthaven, Jan S.; Warburton, Tim. **Nodal Discontinuous Galerkin Methods: Algorithms, Analysis, and Applications**. Springer, 2008.

Use this to connect nodal polynomial bases, quadrature and reference-element operators to DG interface fluxes and PDE algorithms.

Atlas connections: [Orthogonal polynomials and mesh basis functions](basis-functions.md) · [Interactive experiment guide](experiments.md).

[Publisher / bibliographic record](https://doi.org/10.1007/978-0-387-72067-8) · [Author / source page](https://link.springer.com/book/10.1007/978-0-387-72067-8) · `hesthaven2008book`

## Time integration, geophysics and particles {#time-geophysics-particles}

### Hairer · Lubich · Wanner {#hairer2006book}

Hairer, Ernst; Lubich, Christian; Wanner, Gerhard. **Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations**. Springer, 2006 · edition 2.

Use this for symplectic maps, symmetric compositions, splitting and backward error analysis. Preserving symplectic structure does not mean exactly preserving the original Hamiltonian.

Atlas connections: [Symplectic integration: a canonical map, not an exact energy promise](symplectic.md) · [Time integration and leapfrog](time-integration.md).

[Publisher / bibliographic record](https://doi.org/10.1007/3-540-30666-8) · [Author / source page](https://link.springer.com/book/10.1007/3-540-30666-8) · `hairer2006book`

### Durran {#durran2010}

Durran, Dale R. **Numerical Methods for Fluid Dynamics: With Applications to Geophysics**. Springer, 2010 · edition 2.

Use this for dispersion, advection and time discretization in geophysical flows. Read it alongside the spherical-mesh and variable-staggering notes.

Atlas connections: [Spherical meshes and Arakawa A, B and C grids](geophysical-grids.md) · [Runge–Kutta families: stages, order, stability, and SSP](runge-kutta.md).

[Publisher / bibliographic record](https://doi.org/10.1007/978-1-4419-6412-0) · [Author / source page](https://link.springer.com/book/10.1007/978-1-4419-6412-0) · `durran2010`

### Hockney · Eastwood {#hockney1981book}

Hockney, R. W.; Eastwood, J. W. **Computer Simulation Using Particles**. McGraw-Hill, 1981.

Use this for particle–mesh thinking, force assignment and Fourier-based field calculations. The cited original year is 1981; the linked DOI is a later reissue.

Atlas connections: [Particle gravity: PM, P³M, Tree, multipoles, and multigrid](particle-gravity.md) · [Gravity kernels: isolated FFTs and a periodic slab](gravity-boundaries.md).

[Publisher / bibliographic record](https://doi.org/10.1201/9780367806934) · [Author / source page](https://doi.org/10.1201/9780367806934) · `hockney1981book`
