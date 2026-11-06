# Orthogonal polynomials and mesh basis functions

A mesh supplies cells, geometry and connectivity. A **basis** supplies the functions used to represent a field on those cells. The choice of basis is separate from cell shape and variable staggering. The [basis notebook](https://koyamahr.github.io/numerical-methods-atlas/#/basis) makes modes, nodes and their mass matrices visible. The existing [DG advection example](benchmarks.md) already uses Legendre modes internally; this chapter exposes the algebra behind it.

## Start on a reference element

Map a physical interval of length h and center x_c to a reference interval:

\[
x=x_c+J\xi,\qquad J=h/2,\qquad -1\leq\xi\leq1,
\qquad u_h(x)=\sum_{j=0}^{p}a_j\phi_j(\xi).
\]

The p+1 coefficients are element degrees of freedom. In a continuous finite-element method, neighboring elements share selected boundary degrees of freedom. DG keeps independent element coefficients and couples traces through numerical fluxes. A local polynomial basis can serve either formulation.

For constant material coefficients and an affine map, the element mass and diffusion matrices are

\[
M_{ij}=J\int_{-1}^{1}\phi_i\phi_j\,d\xi,
\qquad K_{ij}=J^{-1}\int_{-1}^{1}\phi_i'\phi_j'\,d\xi.
\]

Curved maps introduce a variable Jacobian; variable density or coefficients also change these integrals. Reference-element orthogonality alone then does not make the physical matrix diagonal.

## Legendre modes and orthonormal modes

With unit weight on [-1,1], the Legendre family satisfies

\[
P_0=1,\quad P_1=\xi,\quad P_2=(3\xi^2-1)/2,
\qquad (n+1)P_{n+1}=(2n+1)\xi P_n-nP_{n-1},
\]

\[
\int_{-1}^{1}P_iP_j\,d\xi=\frac{2}{2i+1}\delta_{ij},
\qquad \widehat P_i=\sqrt{\frac{2i+1}{2}}P_i.
\]

The ordinary Legendre mass is diagonal, with unequal diagonal entries. The orthonormal reference mass is the identity. Their coefficient values differ, although both span exactly the same degree-p polynomial space. The constant mode encodes the element mean; the higher Legendre modes have zero mean. See [NIST DLMF §18.3](https://dlmf.nist.gov/18.3) for normalization and [§18.9](https://dlmf.nist.gov/18.9) for recurrence relations.

## Nodal Lagrange functions represent the same space

Choose distinct nodes and define cardinal polynomials:

\[
\ell_j(\xi)=\prod_{k\ne j}\frac{\xi-\xi_k}{\xi_j-\xi_k},
\qquad \ell_j(\xi_i)=\delta_{ij},\qquad
u_h=\sum_j u_j\ell_j.
\]

Here the coefficients u_j are **nodal values**. In a modal expansion, the coefficients are polynomial amplitudes. For the same polynomial, the change of representation is

\[
u_i=\sum_j V_{ij}a_j,\qquad V_{ij}=P_j(\xi_i),\qquad a=V^{-1}u.
\]

The notebook compares equispaced nodes and Gauss–Lobatto–Legendre (GLL) nodes. It reports the condition number of this Legendre Vandermonde; that number depends on normalization and is not the condition number of a complete PDE solve. Endpoint clustering can help interpolation, but does not remove Gibbs oscillations at a jump.

## Quadrature and the diagonal-mass caveat

With p+1 points, Gauss–Legendre quadrature integrates polynomials through degree 2p+1. GLL includes the endpoints and integrates through degree 2p−1. Its interior points are the zeros of P'_p, and its weights are

\[
w_i=\frac{2}{p(p+1)P_p(\xi_i)^2},\qquad p\geq1.
\]

Products of degree-p basis functions can have degree 2p. Consequently, GLL collocation gives a **quadrature mass** diag(w), while the exactly integrated GLL nodal mass generally has off-diagonal entries. On an affine interval with unit weight, their difference is rank one. The highest Legendre squared norm is 2/p under GLL quadrature, instead of 2/(2p+1). The notebook lets you switch between both matrices. These facts, and an efficient correction, are derived in [Teukolsky's mass-matrix note](https://arxiv.org/html/1412.2276v1).

For constant-coefficient stiffness, the polynomial degree is at most 2p−2, so the same GLL rule is sufficient. Nonlinear fluxes and variable metrics can require additional quadrature or a suitable split formulation; a diagonal mass alone is not a nonlinear stability guarantee. [DLMF §3.5](https://dlmf.nist.gov/3.5) explains Gaussian quadrature more generally.

## Projection is different from interpolation

An unweighted L2 Legendre projection uses integral moments:

\[
a_k=\frac{2k+1}{2}\int_{-1}^{1}f(\xi)P_k(\xi)\,d\xi.
\]

Nodal interpolation instead matches f at the chosen nodes. They agree for every polynomial of degree at most p, but need not agree for other functions. For exp(ξ), the notebook shows rapidly decreasing errors as p increases. For sign(ξ), the displayed overshoot and slow convergence expose the loss of smoothness; neither approximation supplies a shock limiter. The jump is integrated on two separate half-intervals, and interpolation explicitly uses sign(0)=0. L2 errors are integrated with 80-point Gauss rules on each half.

## Quadrilaterals and triangles have different polynomial spaces

On a quadrilateral, a tensor basis takes products of one-dimensional functions:

\[
\phi_{ij}(\xi,\eta)=\ell_i(\xi)\ell_j(\eta),\qquad
0\leq i,j\leq p.
\]

This Q_p space has (p+1)^2 functions. A triangle's total-degree P_p space has (p+1)(p+2)/2. Thus Q2 has nine degrees of freedom, while triangular P2 has six. The cell topology determines which reference map and trace connectivity are needed. [DefElement's Lagrange definition](https://defelement.org/elements/lagrange.html) distinguishes these spaces and nodal variants.

On the reference triangle (0,0), (1,0), (0,1), barycentric coordinates are λ0=1−ξ−η, λ1=ξ, λ2=η. The P1 vertex functions are λ_i. P2 has vertex functions λ_i(2λ_i−1) and edge functions 4λ_iλ_j. They form a partition of unity and reproduce quadratic fields; they are **not an orthogonal basis**. The notebook colors each of these six shape functions on the actual triangle.

Orthogonal modal triangle bases can instead be built from suitably weighted Jacobi polynomials in collapsed coordinates, including the Dubiner construction. A rectangular Legendre tensor product restricted to a triangle does not automatically retain orthogonality. This edition implements P1/P2 nodal triangles and quadrilateral tensor evaluation; a Dubiner implementation remains additional work.

## Other orthogonal families and their measures

Orthogonality always includes a domain and a weight. Changing either changes the inner product. The notebook also tabulates Chebyshev T modes and demonstrates their nonorthogonality under unit weight. The remaining families below are mathematical reading connections. Conventions follow [DLMF §18.2](https://dlmf.nist.gov/18.2) and [§18.3](https://dlmf.nist.gov/18.3).

- **Chebyshev T_n:** T_n(cos θ)=cos(nθ), on [-1,1], weight (1−ξ²)^−1/2. Useful for endpoint-clustered spectral interpolation. They are not mutually orthogonal under the unweighted finite-element mass integral.
- **Jacobi:** P_n^(α,β), weight (1−ξ)^α(1+ξ)^β on [-1,1], α,β>−1. This family includes Legendre and, after normalization, Chebyshev; weighted coordinate transforms connect it to simplex bases.
- **Hermite:** physicists' H_n has weight exp(−ξ²) on the real line; probabilists' He_n uses exp(−ξ²/2). These are different conventions. Orthogonal Hermite polynomials are distinct from the endpoint value/derivative Hermite interpolation used by [CIP](cip.md).
- **Generalized Laguerre:** L_n^(α) uses ξ^α exp(−ξ) on [0,∞), α>−1. It addresses a semi-infinite domain rather than an ordinary bounded mesh cell.
- **Fourier modes:** exp(ikx) are orthogonal on a periodic interval with matching integer wave numbers. They form a global periodic basis rather than a mesh-local polynomial family; the [spectral advection example](benchmarks.md) uses these modes.

## Verification and scope

`numart.basis` supplies Legendre/Chebyshev and nodal tabulation, derivatives, affine interval matrices, GLL quadrature, projection, P1/P2 triangles and tensor products. Tests check continuous Legendre orthogonality, GLL exactness limits, cardinal interpolation, polynomial reproduction, partition of unity, derivative reproduction, the GLL summation-by-parts identity, rank-one mass difference and physical Jacobian scaling. The existing DG solver remains restricted to scalar periodic P0/P1/P2 advection.

Reproduce the exhibit with `python scripts/build_basis.py`. [Saved arrays and source hashes](https://koyamahr.github.io/numerical-methods-atlas/basis.json) accompany the figure. This adds reference-element building blocks, not a general curved-mesh assembly or a higher-order fluid solver.

![Reference-element bases and approximations](figures/basis.png)

Continue with [mesh connectivity](meshes.md), [continuous triangular FEM](fem.md), [DG advection](benchmarks.md), [limiters](limiters.md) and [variable staggering](geophysical-grids.md).
