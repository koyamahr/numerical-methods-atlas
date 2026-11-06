"""Reference-element polynomial bases and mass matrices (NumPy only).

Small educational degrees, not a high-degree production tabulation library.
All interval mass matrices below use the unweighted measure dxi.
"""
import numpy as np
from numpy.polynomial.legendre import legvander, Legendre, leggauss
from numpy.polynomial.chebyshev import chebvander, Chebyshev


def _degree(p, minimum=0):
    if isinstance(p, (bool, np.bool_)) or not isinstance(p, (int, np.integer)) or p < minimum:
        raise ValueError('Require an integer polynomial degree >= %d' % minimum)
    return int(p)


def legendre(x, degree, orthonormal=False, derivative=False):
    """Columns P_0..P_p, optionally d/dxi and/or unit L2 normalization."""
    p = _degree(degree)
    x = np.asarray(x, dtype=float)
    if derivative:
        values = np.stack([Legendre.basis(k).deriv()(x) for k in range(p+1)], axis=-1)
    else:
        values = legvander(x, p).reshape(x.shape+(p+1,))
    return values*np.sqrt((2*np.arange(p+1)+1)/2) if orthonormal else values


def lobatto(degree):
    """p+1 GLL points, endpoints included; exact quadrature through degree 2p-1."""
    p = _degree(degree, 1)
    poly = Legendre.basis(p)
    nodes = np.r_[-1., poly.deriv().roots(), 1.]
    # Preserve exact symmetry, in particular the zero node for even p.
    # A spurious 1e-16 center would change sign(x) interpolation at its jump.
    nodes = .5*(nodes-nodes[::-1])
    weights = 2/(p*(p+1)*poly(nodes)**2)
    return nodes, weights


def lagrange(x, nodes, derivative=False):
    """Nodal cardinal polynomials from a Legendre Vandermonde solve.

    Supports arbitrary distinct real interval nodes at modest degree.
    """
    nodes = np.asarray(nodes, dtype=float)
    if nodes.ndim != 1 or len(nodes) < 1 or not np.isfinite(nodes).all() or len(np.unique(nodes)) != len(nodes):
        raise ValueError('Require a nonempty vector of distinct finite nodes')
    p = len(nodes)-1
    v = legendre(nodes, p)
    values = legendre(x, p, derivative=derivative)
    return np.linalg.solve(v.T, values.reshape(-1, p+1).T).T.reshape(values.shape)


def interval_basis(x, degree, kind='legendre', derivative=False):
    p = _degree(degree)
    if kind in ('legendre', 'orthonormal'):
        return legendre(x, p, kind == 'orthonormal', derivative)
    if kind == 'chebyshev':
        x = np.asarray(x, dtype=float)
        if derivative:
            return np.stack([Chebyshev.basis(k).deriv()(x) for k in range(p+1)], axis=-1)
        return chebvander(x, p).reshape(x.shape+(p+1,))
    if kind == 'gll':
        nodes, _ = lobatto(p)
    elif kind == 'equispaced':
        nodes = np.linspace(-1, 1, p+1) if p else np.array([0.])
    else:
        raise ValueError('Unknown interval basis')
    return lagrange(x, nodes, derivative)


def element_matrices(degree, kind='legendre', length=2., quadrature='exact'):
    """Physical affine interval M=J int(phi phi), K=1/J int(phi' phi').

    'exact' uses p+1 Gauss points; 'gll' deliberately uses p+1 GLL points.
    Constant metric/coefficient only. K has the expected constant nullspace.
    """
    p = _degree(degree)
    if not np.isfinite(length) or length <= 0:
        raise ValueError('Require positive finite element length')
    if quadrature == 'exact':
        x, w = leggauss(p+1)
    elif quadrature == 'gll':
        x, w = lobatto(p)
    else:
        raise ValueError('Unknown quadrature')
    b = interval_basis(x, p, kind)
    d = interval_basis(x, p, kind, derivative=True)
    jac = length/2
    return jac*np.einsum('qi,q,qj->ij', b, w, b), np.einsum('qi,q,qj->ij', d, w, d)/jac


def project_legendre(function, degree, quadrature_order=None):
    """Unweighted L2 modal projection, evaluated with Gauss quadrature."""
    p = _degree(degree)
    n = max(p+1, 32) if quadrature_order is None else _degree(quadrature_order, 1)
    x, w = leggauss(n)
    values = np.broadcast_to(np.asarray(function(x), dtype=float), x.shape)
    return np.einsum('qk,q,q->k', legendre(x, p), w, values)*(2*np.arange(p+1)+1)/2


def triangle_lagrange(points, degree=1):
    """P1/P2 on (0,0),(1,0),(0,1); vertices then edges 01,12,20.

    These are nodal shape functions, not an orthogonal triangle family.
    """
    p = _degree(degree, 1)
    xy = np.asarray(points, dtype=float)
    if xy.shape[-1:] != (2,):
        raise ValueError('Require points with last dimension 2')
    b = np.stack((1-xy[..., 0]-xy[..., 1], xy[..., 0], xy[..., 1]), axis=-1)
    if p == 1:
        return b
    if p == 2:
        return np.concatenate((b*(2*b-1), np.stack((4*b[..., 0]*b[..., 1],
                               4*b[..., 1]*b[..., 2], 4*b[..., 2]*b[..., 0]), axis=-1)), axis=-1)
    raise ValueError('Triangle example supports P1 or P2')


def tensor_basis(points, degree, kind='gll'):
    """Quadrilateral Q_p tensor product; i varies slowly, j quickly."""
    xy = np.asarray(points, dtype=float)
    if xy.shape[-1:] != (2,):
        raise ValueError('Require points with last dimension 2')
    x = interval_basis(xy[..., 0], degree, kind)
    y = interval_basis(xy[..., 1], degree, kind)
    return (x[..., :, None]*y[..., None, :]).reshape(x.shape[:-1]+(-1,))
