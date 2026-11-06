# Textbooks: where to look next

A working bookshelf for this atlas. Choose a book by the question you need to answer; this is a reading guide, not a ranking. Bibliographic years below identify the cited editions, not the invention dates of algorithms.

The links lead to publisher records or author-maintained pages. We checked edition metadata and available descriptions or contents, not every derivation in every book. Chapter suggestions describe the atlas connection; they do not claim that all of a textbook has been implemented.

**A short starting path:** Hirsch for the CFD framework; LeVeque for conservation laws and finite-volume reasoning; Toro for Riemann solvers; Patankar for pressure–velocity coupling; Saad for sparse iterative solves. Return to original papers when tracing a particular algorithm.

[Search the full reference library](#/references) · [All cataloged books](#/references?q=type%3Abook) · [Download BibTeX](../references.bib)

Covers are supplied by [Open Library](https://openlibrary.org/dev/docs/api/covers) for the listed ISBN. Each card links to Amazon Japan and the publisher or bibliographic record. The title stays visible when a cover is unavailable.

## CFD foundations and incompressible flow {#cfd-foundations}

<section class="textbook-card" aria-labelledby="hirsch2007">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="missing">
<a href="https://openlibrary.org/isbn/9780750665940" target="_blank" rel="noopener" aria-label="Open Library: Numerical Computation of Internal and External Flows: The Fundamentals of Computational Fluid Dynamics">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Numerical Computation of Internal and External Flows: The Fundamentals of Computational Fluid Dynamics</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780750665940" target="_blank" rel="noopener">Open Library record</a>
<span class="book-isbn">ISBN 9780750665940</span>
</div>
<div class="textbook-details">

### Hirsch {#hirsch2007}

Hirsch, Charles. **Numerical Computation of Internal and External Flows: The Fundamentals of Computational Fluid Dynamics**. Butterworth-Heinemann, 2007 · edition 2.

Use this for the CFD framework: equations, grid properties, consistency, stability, discretization and solution procedures. The cited 2007 book is the second-edition fundamentals volume.

Atlas connections: [Differences, CFL, von Neumann analysis, and Lax](stability.md) · [Structured, unstructured, and triangular meshes](meshes.md) · [Time integration and leapfrog](time-integration.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0750665947" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1016/B978-0-7506-6594-0.X5037-1" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://www.sciencedirect.com/book/monograph/9780750665940/numerical-computation-of-internal-and-external-flows" target="_blank" rel="noopener">Author / source ↗</a>
<code>hirsch2007</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="fletcher1991v1">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9783540530589" target="_blank" rel="noopener" aria-label="Open Library: Computational Techniques for Fluid Dynamics 1: Fundamental and General Techniques">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Computational Techniques for Fluid Dynamics 1: Fundamental and General Techniques</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/2225072-M.jpg?default=false" alt="Cover of Computational Techniques for Fluid Dynamics 1: Fundamental and General Techniques" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9783540530589" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9783540530589</span>
</div>
<div class="textbook-details">

### Fletcher / Volume I {#fletcher1991v1}

Fletcher, Clive A. J. **Computational Techniques for Fluid Dynamics 1: Fundamental and General Techniques**. Springer, 1991 · edition 2.

Use Volume I for PDE classification, weighted residual methods, steady and diffusion problems, and linear/nonlinear convection. It supplies the common numerical tools before the flow-specific algorithms of Volume II.

Atlas connections: [Differences, CFL, von Neumann analysis, and Lax](stability.md) · [Continuous finite elements: from weak form to sparse assembly](fem.md) · [Diffusion, elliptic equations, boundary conditions, and iteration](elliptic.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/3540530584" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/978-3-642-58229-5" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://link.springer.com/book/10.1007/978-3-642-58229-5" target="_blank" rel="noopener">Author / source ↗</a>
<code>fletcher1991v1</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="fletcher1991v2">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="missing">
<a href="https://openlibrary.org/isbn/9783540536017" target="_blank" rel="noopener" aria-label="Open Library: Computational Techniques for Fluid Dynamics 2: Specific Techniques for Different Flow Categories">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Computational Techniques for Fluid Dynamics 2: Specific Techniques for Different Flow Categories</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9783540536017" target="_blank" rel="noopener">Open Library record</a>
<span class="book-isbn">ISBN 9783540536017</span>
</div>
<div class="textbook-details">

### Fletcher / Volume II {#fletcher1991v2}

Fletcher, Clive A. J. **Computational Techniques for Fluid Dynamics 2: Specific Techniques for Different Flow Categories**. Springer, 1991 · edition 2.

Use Volume II to connect the general techniques of Volume I to different flow-equation categories and their computational solution procedures. Read assumptions and boundary conditions alongside each algorithm.

Atlas connections: [Incompressible flow: project with compatible discrete operators](incompressible.md) · [Preconditioning, dual time stepping, and residual distribution](advanced.md) · [Polar and cylindrical coordinates: tensors and viscosity](coordinates-viscosity.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/3540536019" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/978-3-642-58239-4" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://link.springer.com/book/10.1007/978-3-642-58239-4" target="_blank" rel="noopener">Author / source ↗</a>
<code>fletcher1991v2</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="ferziger2020">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9783319996912" target="_blank" rel="noopener" aria-label="Open Library: Computational Methods for Fluid Dynamics">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Computational Methods for Fluid Dynamics</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/10130550-M.jpg?default=false" alt="Cover of Computational Methods for Fluid Dynamics" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9783319996912" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9783319996912</span>
</div>
<div class="textbook-details">

### Ferziger · Perić · Street {#ferziger2020}

Ferziger, Joel H.; Perić, Milovan; Street, Robert L. **Computational Methods for Fluid Dynamics**. Springer, 2020 · edition 4.

Use this when connecting discrete operators to a practical CFD solution procedure, especially incompressible pressure–velocity coupling and boundary conditions.

Atlas connections: [Incompressible flow: project with compatible discrete operators](incompressible.md) · [Polar and cylindrical coordinates: tensors and viscosity](coordinates-viscosity.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/3319996916" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/978-3-319-99693-6" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://link.springer.com/book/10.1007/978-3-319-99693-6" target="_blank" rel="noopener">Author / source ↗</a>
<code>ferziger2020</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="patankar1980">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780891165224" target="_blank" rel="noopener" aria-label="Open Library: Numerical Heat Transfer and Fluid Flow">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Numerical Heat Transfer and Fluid Flow</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/12927123-M.jpg?default=false" alt="Cover of Numerical Heat Transfer and Fluid Flow" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780891165224" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9780891165224</span>
</div>
<div class="textbook-details">

### Patankar {#patankar1980}

Patankar, Suhas V. **Numerical Heat Transfer and Fluid Flow**. CRC Press (current publisher record), 1980.

Use this for the physical logic of control-volume balances and SIMPLE-type pressure–velocity coupling. Keep the book exposition separate from the original algorithm papers.

Atlas connections: [Incompressible flow: project with compatible discrete operators](incompressible.md) · [Euler reconstruction: PPM, characteristics, WENO-Z and AUSM](reconstruction.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0891165223" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://www.routledge.com/Numerical-Heat-Transfer-and-Fluid-Flow-1st-Edition/Patankar/p/book/9780891165224" target="_blank" rel="noopener">Publisher / record ↗</a>
<code>patankar1980</code></p>

</div>
</section>

## Conservation laws, Riemann solvers and shocks {#hyperbolic}

<section class="textbook-card" aria-labelledby="leveque2002">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780521009249" target="_blank" rel="noopener" aria-label="Open Library: Finite Volume Methods for Hyperbolic Problems">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Finite Volume Methods for Hyperbolic Problems</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/328569-M.jpg?default=false" alt="Cover of Finite Volume Methods for Hyperbolic Problems" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780521009249" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9780521009249</span>
</div>
<div class="textbook-details">

### LeVeque / finite volume {#leveque2002}

LeVeque, Randall J. **Finite Volume Methods for Hyperbolic Problems**. Cambridge University Press, 2002.

Use this for weak solutions, finite-volume reasoning, wave propagation, limiters and multidimensional conservation laws. Companion Clawpack material connects the theory to computation.

Atlas connections: [Euler reconstruction: PPM, characteristics, WENO-Z and AUSM](reconstruction.md) · [Slope limiters: minmod, Superbee, MC, van Leer, and van Albada](limiters.md) · [Equation gallery: choose the equation before the algorithm](equation-gallery.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0521009243" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1017/CBO9780511791253" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://www.cambridge.org/core/books/finite-volume-methods-for-hyperbolic-problems/97D5D1ACB1926DA1D4D52EAD6909E2B9" target="_blank" rel="noopener">Author / source ↗</a>
<code>leveque2002</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="toro2009">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9783540252023" target="_blank" rel="noopener" aria-label="Open Library: Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/7368028-M.jpg?default=false" alt="Cover of Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9783540252023" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9783540252023</span>
</div>
<div class="textbook-details">

### Toro {#toro2009}

Toro, Eleuterio F. **Riemann Solvers and Numerical Methods for Fluid Dynamics: A Practical Introduction**. Springer, 2009 · edition 3.

Use this when deriving or comparing exact and approximate Euler Riemann solvers, contact waves and high-resolution shock-capturing methods.

Atlas connections: [Preconditioning, dual time stepping, and residual distribution](advanced.md) · [Euler reconstruction: PPM, characteristics, WENO-Z and AUSM](reconstruction.md) · [Benchmark library](benchmarks.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/3540252029" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/b79761" target="_blank" rel="noopener">Publisher / record ↗</a>
<code>toro2009</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="godlewski1996book">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780387945293" target="_blank" rel="noopener" aria-label="Open Library: Numerical Approximation of Hyperbolic Systems of Conservation Laws">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Numerical Approximation of Hyperbolic Systems of Conservation Laws</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/245411-M.jpg?default=false" alt="Cover of Numerical Approximation of Hyperbolic Systems of Conservation Laws" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780387945293" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9780387945293</span>
</div>
<div class="textbook-details">

### Godlewski · Raviart {#godlewski1996book}

Godlewski, Edwige; Raviart, Pierre-Arnaud. **Numerical Approximation of Hyperbolic Systems of Conservation Laws**. Springer, 1996 · edition 1.

Use this for a mathematical treatment of nonlinear hyperbolic systems and their numerical approximation, including Riemann problems and gas dynamics. Read it alongside LeVeque for finite-volume reasoning and Toro for solver construction. This entry cites the 1996 first edition; a [revised second edition appeared in 2021](https://link.springer.com/book/10.1007/978-1-0716-1344-3).

Atlas connections: [Preconditioning, dual time stepping, and residual distribution](advanced.md) · [Euler reconstruction: PPM, characteristics, WENO-Z and AUSM](reconstruction.md) · [A-stability, L-stability and error norms](accuracy-stability.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0387945296" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/978-1-4612-0713-9" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://link.springer.com/book/10.1007/978-1-4612-0713-9" target="_blank" rel="noopener">Author / source ↗</a>
<code>godlewski1996book</code></p>

</div>
</section>

## Finite differences and linear algebra {#common-numerics}

<section class="textbook-card" aria-labelledby="leveque2007">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="missing">
<a href="https://openlibrary.org/isbn/9780898716290" target="_blank" rel="noopener" aria-label="Open Library: Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780898716290" target="_blank" rel="noopener">Open Library record</a>
<span class="book-isbn">ISBN 9780898716290</span>
</div>
<div class="textbook-details">

### LeVeque / finite differences {#leveque2007}

LeVeque, Randall J. **Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems**. SIAM, 2007.

Use this for the consistency–stability–convergence chain, ordinary differential equations, boundary-value problems and finite-difference PDE solvers.

Atlas connections: [A-stability, L-stability and error norms](accuracy-stability.md) · [Time integration and leapfrog](time-integration.md) · [Diffusion, elliptic equations, boundary conditions, and iteration](elliptic.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0898716292" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1137/1.9780898717839" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://staff.washington.edu/rjl/booksnotes.html" target="_blank" rel="noopener">Author / source ↗</a>
<code>leveque2007</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="golub2013">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9781421407944" target="_blank" rel="noopener" aria-label="Open Library: Matrix Computations">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Matrix Computations</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/8779096-M.jpg?default=false" alt="Cover of Matrix Computations" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9781421407944" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9781421407944</span>
</div>
<div class="textbook-details">

### Golub · Van Loan {#golub2013}

Golub, Gene H.; Van Loan, Charles F. **Matrix Computations**. Johns Hopkins University Press, 2013 · edition 4.

Use this for conditioning, stable matrix factorizations, least squares and eigenproblems before choosing a solver solely by its name.

Atlas connections: [Sparse and nonlinear systems: measure the actual residual](sparse-nonlinear.md) · [Diffusion, elliptic equations, boundary conditions, and iteration](elliptic.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/1421407949" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1137/1.9781421407944" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://epubs.siam.org/doi/book/10.1137/1.9781421407944" target="_blank" rel="noopener">Author / source ↗</a>
<code>golub2013</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="saad2003book">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780898715347" target="_blank" rel="noopener" aria-label="Open Library: Iterative Methods for Sparse Linear Systems">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Iterative Methods for Sparse Linear Systems</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/698819-M.jpg?default=false" alt="Cover of Iterative Methods for Sparse Linear Systems" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780898715347" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9780898715347</span>
</div>
<div class="textbook-details">

### Saad {#saad2003book}

Saad, Yousef. **Iterative Methods for Sparse Linear Systems**. SIAM, 2003 · edition 2.

Use this for Krylov subspaces, GMRES, BiCG-family methods and preconditioners. The author provides the second-edition text and corrections.

Atlas connections: [Sparse and nonlinear systems: measure the actual residual](sparse-nonlinear.md) · [Diffusion, elliptic equations, boundary conditions, and iteration](elliptic.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0898715342" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1137/1.9780898718003" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://www-users.cse.umn.edu/~saad/books.html" target="_blank" rel="noopener">Author / source ↗</a>
<code>saad2003book</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="templates1994">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780898713282" target="_blank" rel="noopener" aria-label="Open Library: Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/698646-M.jpg?default=false" alt="Cover of Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780898713282" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9780898713282</span>
</div>
<div class="textbook-details">

### Barrett et al. / Templates {#templates1994}

Barrett, Richard; Berry, Michael; Chan, Tony F.; Demmel, James; Donato, June; Dongarra, Jack; Eijkhout, Victor; Pozo, Roldan; Romine, Charles; van der Vorst, Henk. **Templates for the Solution of Linear Systems: Building Blocks for Iterative Methods**. SIAM, 1994.

Use this open reference as a compact algorithm-and-selection companion for iterative linear solvers, with attention to matrix assumptions.

Atlas connections: [Sparse and nonlinear systems: measure the actual residual](sparse-nonlinear.md) · [Diffusion, elliptic equations, boundary conditions, and iteration](elliptic.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0898713285" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://www.netlib.org/templates/templates.html" target="_blank" rel="noopener">Publisher / record ↗</a>
<code>templates1994</code></p>

</div>
</section>

## Multigrid: intuition, analysis and implementation {#multigrid}

<section class="textbook-card" aria-labelledby="briggs2000book">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780898714623" target="_blank" rel="noopener" aria-label="Open Library: A Multigrid Tutorial">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>A Multigrid Tutorial</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/698765-M.jpg?default=false" alt="Cover of A Multigrid Tutorial" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780898714623" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9780898714623</span>
</div>
<div class="textbook-details">

### Briggs · Henson · McCormick / A Multigrid Tutorial {#briggs2000book}

Briggs, William L.; Henson, Van Emden; McCormick, Steve F. **A Multigrid Tutorial**. SIAM, 2000 · edition 2.

Start here for why relaxation damps oscillatory error while coarse grids address the remaining smooth error. Follow the model problems into residual correction, restriction, prolongation and a working multigrid cycle. The second edition also introduces nonlinear problems and AMG.

Atlas connections: [Diffusion, elliptic equations, boundary conditions, and iteration](elliptic.md) · [Sparse and nonlinear systems: measure the actual residual](sparse-nonlinear.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0898714621" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1137/1.9780898719505" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://epubs.siam.org/doi/book/10.1137/1.9780898719505" target="_blank" rel="noopener">Author / source ↗</a>
<code>briggs2000book</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="trottenberg2001">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780127010700" target="_blank" rel="noopener" aria-label="Open Library: Multigrid">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Multigrid</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/1100584-M.jpg?default=false" alt="Cover of Multigrid" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780127010700" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9780127010700</span>
</div>
<div class="textbook-details">

### Trottenberg · Oosterlee · Schüller / Multigrid {#trottenberg2001}

Trottenberg, Ulrich; Oosterlee, Cornelius W.; Schüller, Anton. **Multigrid**. Academic Press, 2001 · edition 1.

Use this as the detailed reference after the tutorial: elementary multigrid theory, local Fourier analysis, smoother and coarse-grid choices, parallel implementation, systems and an AMG appendix. For the atlas Poisson comparison, use it to ask why a cycle converges and how its work changes; AMG, anisotropy and parallel performance need separate implementations and tests.

Atlas connections: [Diffusion, elliptic equations, boundary conditions, and iteration](elliptic.md) · [Sparse and nonlinear systems: measure the actual residual](sparse-nonlinear.md) · [Particle gravity: PM, P³M, Tree, multipoles, and multigrid](particle-gravity.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/012701070X" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://shop.elsevier.com/books/multigrid/trottenberg/978-0-08-047956-9" target="_blank" rel="noopener">Publisher / record ↗</a>
<code>trottenberg2001</code></p>

</div>
</section>

## Spectral bases and discontinuous Galerkin {#high-order}

<section class="textbook-card" aria-labelledby="trefethen2000">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780898714654" target="_blank" rel="noopener" aria-label="Open Library: Spectral Methods in MATLAB">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Spectral Methods in MATLAB</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/698768-M.jpg?default=false" alt="Cover of Spectral Methods in MATLAB" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780898714654" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9780898714654</span>
</div>
<div class="textbook-details">

### Trefethen {#trefethen2000}

Trefethen, Lloyd N. **Spectral Methods in MATLAB**. SIAM, 2000.

Use this for spectral differentiation, Fourier/Chebyshev examples and short reproducible programs. Supplement its limited barycentric-interpolation coverage.

Atlas connections: [Interactive experiment guide](experiments.md) · [Orthogonal polynomials and mesh basis functions](basis-functions.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0898714656" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1137/1.9780898719598" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://people.maths.ox.ac.uk/trefethen/spectral.html" target="_blank" rel="noopener">Author / source ↗</a>
<code>trefethen2000</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="hesthaven2008book">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9780387720654" target="_blank" rel="noopener" aria-label="Open Library: Nodal Discontinuous Galerkin Methods: Algorithms, Analysis, and Applications">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Nodal Discontinuous Galerkin Methods: Algorithms, Analysis, and Applications</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/2412519-M.jpg?default=false" alt="Cover of Nodal Discontinuous Galerkin Methods: Algorithms, Analysis, and Applications" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780387720654" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9780387720654</span>
</div>
<div class="textbook-details">

### Hesthaven · Warburton {#hesthaven2008book}

Hesthaven, Jan S.; Warburton, Tim. **Nodal Discontinuous Galerkin Methods: Algorithms, Analysis, and Applications**. Springer, 2008.

Use this to connect nodal polynomial bases, quadrature and reference-element operators to DG interface fluxes and PDE algorithms.

Atlas connections: [Orthogonal polynomials and mesh basis functions](basis-functions.md) · [Interactive experiment guide](experiments.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/0387720650" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/978-0-387-72067-8" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://link.springer.com/book/10.1007/978-0-387-72067-8" target="_blank" rel="noopener">Author / source ↗</a>
<code>hesthaven2008book</code></p>

</div>
</section>

## Time integration, geophysics and particles {#time-geophysics-particles}

<section class="textbook-card" aria-labelledby="hairer2006book">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9783540306634" target="_blank" rel="noopener" aria-label="Open Library: Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/2221190-M.jpg?default=false" alt="Cover of Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9783540306634" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9783540306634</span>
</div>
<div class="textbook-details">

### Hairer · Lubich · Wanner {#hairer2006book}

Hairer, Ernst; Lubich, Christian; Wanner, Gerhard. **Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations**. Springer, 2006 · edition 2.

Use this for symplectic maps, symmetric compositions, splitting and backward error analysis. Preserving symplectic structure does not mean exactly preserving the original Hamiltonian.

Atlas connections: [Symplectic integration: a canonical map, not an exact energy promise](symplectic.md) · [Time integration and leapfrog](time-integration.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/3540306633" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/3-540-30666-8" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://link.springer.com/book/10.1007/3-540-30666-8" target="_blank" rel="noopener">Author / source ↗</a>
<code>hairer2006book</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="durran2010">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="loading">
<a href="https://openlibrary.org/isbn/9781441964113" target="_blank" rel="noopener" aria-label="Open Library: Numerical Methods for Fluid Dynamics: With Applications to Geophysics">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Numerical Methods for Fluid Dynamics: With Applications to Geophysics</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
<img class="book-cover-image" src="https://covers.openlibrary.org/b/id/8701007-M.jpg?default=false" alt="Cover of Numerical Methods for Fluid Dynamics: With Applications to Geophysics" width="160" height="240" loading="lazy" decoding="async" referrerpolicy="no-referrer">
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9781441964113" target="_blank" rel="noopener">Cover: Open Library</a>
<span class="book-isbn">ISBN 9781441964113</span>
</div>
<div class="textbook-details">

### Durran {#durran2010}

Durran, Dale R. **Numerical Methods for Fluid Dynamics: With Applications to Geophysics**. Springer, 2010 · edition 2.

Use this for dispersion, advection and time discretization in geophysical flows. Read it alongside the spherical-mesh and variable-staggering notes.

Atlas connections: [Spherical meshes and Arakawa A, B and C grids](geophysical-grids.md) · [Runge–Kutta families: stages, order, stability, and SSP](runge-kutta.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/1441964118" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1007/978-1-4419-6412-0" target="_blank" rel="noopener">Publisher / record ↗</a>
<a href="https://link.springer.com/book/10.1007/978-1-4419-6412-0" target="_blank" rel="noopener">Author / source ↗</a>
<code>durran2010</code></p>

</div>
</section>

<section class="textbook-card" aria-labelledby="hockney1981book">
<div class="textbook-art">
<div class="textbook-cover" data-cover-state="missing">
<a href="https://openlibrary.org/isbn/9780070291089" target="_blank" rel="noopener" aria-label="Open Library: Computer Simulation Using Particles">
<span class="book-cover-placeholder" aria-hidden="true"><span class="book-placeholder-title" lang="en" data-original>Computer Simulation Using Particles</span><span class="book-cover-loading">Loading cover</span><span class="book-cover-unavailable">Cover unavailable</span></span>
</a>
</div>
<a class="book-cover-credit" href="https://openlibrary.org/isbn/9780070291089" target="_blank" rel="noopener">Open Library record</a>
<span class="book-isbn">ISBN 9780070291089</span>
</div>
<div class="textbook-details">

### Hockney · Eastwood {#hockney1981book}

Hockney, R. W.; Eastwood, J. W. **Computer Simulation Using Particles**. McGraw-Hill, 1981.

Use this for particle–mesh thinking, force assignment and Fourier-based field calculations. The cited original year is 1981; the linked DOI is a later reissue.

Atlas connections: [Particle gravity: PM, P³M, Tree, multipoles, and multigrid](particle-gravity.md) · [Gravity kernels: isolated FFTs and a periodic slab](gravity-boundaries.md).

<p class="book-links"><a class="book-purchase" href="https://www.amazon.co.jp/dp/007029108X" target="_blank" rel="noopener">Amazon Japan ↗</a>
<a href="https://doi.org/10.1201/9780367806934" target="_blank" rel="noopener">Publisher / record ↗</a>
<code>hockney1981book</code></p>

</div>
</section>
