"""Continuous P1 Galerkin Poisson models: weak forms, assembly and error norms.

1D intervals and affine triangles on a square. Sparse assembly is explicit;
there is no general mesh generator, mixed element or adaptive refinement.
"""
from dataclasses import dataclass
import numpy as np
from numpy.polynomial.legendre import leggauss
from .krylov import CSR, gmres, ilu0_preconditioner


def eliminate_dirichlet(a, rhs, nodes, values):
    """Symmetric row/column elimination, including nonzero boundary data."""
    fixed = dict(zip(np.asarray(nodes, dtype=int), np.asarray(values, dtype=float)))
    b = np.array(rhs, dtype=float, copy=True)
    rows, cols, entries = [], [], []
    for i in range(a.shape[0]):
        if i in fixed:
            rows.append(i); cols.append(i); entries.append(1.)
            b[i] = fixed[i]
            continue
        lo, hi = a.indptr[i:i+2]
        for j, value in zip(a.indices[lo:hi], a.data[lo:hi]):
            if j in fixed:
                b[i] -= value*fixed[j]
            else:
                rows.append(i); cols.append(j); entries.append(value)
    return CSR.from_coo(rows, cols, entries, a.shape), b


@dataclass
class FEMResult:
    points: np.ndarray
    cells: np.ndarray
    u: np.ndarray
    stiffness: CSR
    mass: CSR
    rhs: np.ndarray
    residual: float


def poisson_1d(elements=32, forcing=None, boundary=lambda x: np.zeros_like(x)):
    """-u''=f on [0,1], continuous linear elements; default exact sin(pi*x)."""
    if elements < 2:
        raise ValueError("At least two elements required")
    forcing = forcing or (lambda x: np.pi**2*np.sin(np.pi*x))
    x = np.linspace(0, 1, elements+1)
    cells = np.column_stack((np.arange(elements), np.arange(1, elements+1)))
    rows, cols, kvals, mvals = [], [], [], []
    rhs = np.zeros_like(x)
    z, w = leggauss(4)
    shapes = np.column_stack(((1-z)/2, (1+z)/2))
    for cell in cells:
        h = x[cell[1]]-x[cell[0]]
        k = np.array([[1., -1.], [-1., 1.]])/h
        mass = h*np.array([[2., 1.], [1., 2.]])/6
        positions = x[cell[0]]+(z+1)*h/2
        rhs[cell] += h/2*(shapes.T @ (w*np.broadcast_to(forcing(positions), z.shape)))
        for i in range(2):
            for j in range(2):
                rows.append(cell[i]); cols.append(cell[j]); kvals.append(k[i, j]); mvals.append(mass[i, j])
    k = CSR.from_coo(rows, cols, kvals, (len(x), len(x)))
    mass = CSR.from_coo(rows, cols, mvals, k.shape)
    a, b = eliminate_dirichlet(k, rhs, [0, elements], np.broadcast_to(boundary(x[[0, -1]]), (2,)))
    solve = gmres(a, b, preconditioner=ilu0_preconditioner(a))
    if not solve.converged:
        raise RuntimeError(solve.reason)
    return FEMResult(x[:, None], cells, solve.x, k, mass, b, float(solve.residuals[-1]))


def square_mesh(n=16):
    if n < 2:
        raise ValueError("n>=2 required")
    x, y = np.meshgrid(np.linspace(0, 1, n+1), np.linspace(0, 1, n+1), indexing="ij")
    points = np.column_stack((x.ravel(), y.ravel()))
    cells = []
    for i in range(n):
        for j in range(n):
            a = i*(n+1)+j
            b, c, d = a+n+1, a+n+2, a+1
            cells.extend(((a, b, c), (a, c, d)))
    return points, np.array(cells)


def triangle_quadrature(vertices, order=4):
    """Tensor Gauss rule under a Duffy transform; physical weights sum to area."""
    z, w = leggauss(order)
    z, w = (z+1)/2, w/2
    r, s = np.meshgrid(z, z, indexing="ij")
    weights = np.outer(w, w)*r
    basis = np.stack((1-r, r*(1-s), r*s), axis=-1).reshape(-1, 3)
    determinant = np.linalg.det(np.column_stack((vertices[1]-vertices[0], vertices[2]-vertices[0])))
    if abs(determinant) < 1e-15:
        raise ValueError("Degenerate triangle")
    inverse = np.linalg.inv(np.column_stack((np.ones(3), vertices)))
    gradients = inverse[1:, :].T
    return basis@vertices, (abs(determinant)*weights).ravel(), basis, gradients


def poisson_2d(n=16, forcing=None, boundary=None):
    """P1 triangle -Laplacian; default exact sin(pi*x)sin(pi*y), zero boundary."""
    forcing = forcing or (lambda p: 2*np.pi**2*np.sin(np.pi*p[:, 0])*np.sin(np.pi*p[:, 1]))
    boundary = boundary or (lambda p: np.zeros(len(p)))
    points, cells = square_mesh(n)
    rows, cols, kvals, mvals = [], [], [], []
    rhs = np.zeros(len(points))
    for cell in cells:
        q, weights, basis, gradients = triangle_quadrature(points[cell])
        area = weights.sum()
        k = area*(gradients@gradients.T)
        mass = area*(np.ones((3, 3))+np.eye(3))/12
        rhs[cell] += basis.T@(weights*np.broadcast_to(forcing(q), weights.shape))
        for i in range(3):
            for j in range(3):
                rows.append(cell[i]); cols.append(cell[j]); kvals.append(k[i, j]); mvals.append(mass[i, j])
    k = CSR.from_coo(rows, cols, kvals, (len(points), len(points)))
    mass = CSR.from_coo(rows, cols, mvals, k.shape)
    fixed = np.flatnonzero(np.any((points == 0) | (points == 1), axis=1))
    a, b = eliminate_dirichlet(k, rhs, fixed, boundary(points[fixed]))
    result = gmres(a, b, preconditioner=ilu0_preconditioner(a), restart=35, maxiter=350, rtol=1e-11)
    if not result.converged:
        raise RuntimeError(result.reason)
    return FEMResult(points, cells, result.x, k, mass, b, float(result.residuals[-1]))


def error_norms(result, exact, gradient):
    """Continuous L2 error and H1 seminorm, evaluated inside each triangle."""
    l2, h1 = 0., 0.
    for cell in result.cells:
        q, weights, basis, gradients = triangle_quadrature(result.points[cell], order=5)
        error = basis@result.u[cell]-exact(q)
        derivative = result.u[cell]@gradients-gradient(q)
        l2 += weights @ error**2
        h1 += weights @ np.sum(derivative**2, axis=1)
    return float(np.sqrt(l2)), float(np.sqrt(h1))
