import numpy as np
import pytest
from numpy.polynomial.legendre import leggauss
from numart.basis import (legendre, lobatto, lagrange, interval_basis,
                          element_matrices, project_legendre, triangle_lagrange, tensor_basis)


@pytest.mark.parametrize('p', [1, 2, 4, 8, 12])
def test_orthogonality_normalization_and_lobatto_exactness(p):
    x, w = leggauss(p+1)
    v = legendre(x, p)
    np.testing.assert_allclose(np.einsum('qi,q,qj->ij', v, w, v), np.diag(2/(2*np.arange(p+1)+1)), atol=2e-14)
    v = legendre(x, p, orthonormal=True)
    np.testing.assert_allclose(np.einsum('qi,q,qj->ij', v, w, v), np.eye(p+1), atol=3e-14)
    z, q = lobatto(p)
    assert z[0] == -1 and z[-1] == 1 and np.all(q > 0)
    np.testing.assert_array_equal(z, -z[::-1])
    if p % 2 == 0: assert z[p//2] == 0
    for k in range(2*p):
        assert abs(q@z**k-(0 if k % 2 else 2/(k+1))) < 2e-14
    # The next degree is outside the rule's exactness, even though mass looks diagonal.
    assert abs(q@z**(2*p)-2/(2*p+1)) > 1e-9


@pytest.mark.parametrize('p', [1, 2, 4, 8])
def test_nodal_transform_derivative_and_sbp(p):
    z, w = lobatto(p)
    np.testing.assert_allclose(lagrange(z, z), np.eye(p+1), atol=2e-14)
    x = np.linspace(-1, 1, 31)
    b, d = lagrange(x, z), lagrange(x, z, derivative=True)
    np.testing.assert_allclose(b.sum(axis=1), 1, atol=2e-14)
    np.testing.assert_allclose(d.sum(axis=1), 0, atol=8e-14)
    q = np.arange(p+1, dtype=float)/max(p, 1)
    # A random degree-p polynomial is identical in modal and nodal representation.
    np.testing.assert_allclose(b@(legendre(z, p)@q), legendre(x, p)@q, atol=1e-13)
    np.testing.assert_allclose(d@(legendre(z, p)@q), legendre(x, p, derivative=True)@q, atol=3e-13)
    deriv = lagrange(z, z, derivative=True)
    boundary = np.zeros((p+1, p+1)); boundary[0, 0] = -1; boundary[-1, -1] = 1
    np.testing.assert_allclose(w[:, None]*deriv+deriv.T*w[None, :], boundary, atol=2e-13)


def test_exact_vs_lumped_mass_and_affine_mapping():
    p = 5
    m, k = element_matrices(p, 'gll')
    lump, kl = element_matrices(p, 'gll', quadrature='gll')
    _, w = lobatto(p)
    np.testing.assert_allclose(lump, np.diag(w), atol=1e-14)
    assert np.linalg.matrix_rank(m-lump, tol=1e-12) == 1
    np.testing.assert_allclose(k, kl, atol=1e-13)  # degree 2p-2 is integrated exactly
    np.testing.assert_allclose(m@np.ones(p+1), w, atol=1e-14)
    mp, kp = element_matrices(p, 'gll', length=.3)
    np.testing.assert_allclose(mp, .15*m, atol=1e-14)
    np.testing.assert_allclose(kp, k/.15, atol=1e-12)
    assert np.linalg.eigvalsh(m).min() > 0


def test_projection_polynomial_and_discontinuous_split_integral():
    coefficients = project_legendre(lambda x: 1+2*x+3*x*x, 4)
    np.testing.assert_allclose(coefficients, [2, 2, 2, 0, 0], atol=3e-14)
    # Integrate sign(x) separately on each smooth half; avoid quadrature across its jump.
    x, w = leggauss(10)
    c = ((legendre((x+1)/2, 5)-legendre((x-1)/2, 5)).T@w)/2
    c *= (2*np.arange(6)+1)/2
    np.testing.assert_allclose(c[:4], [0, 1.5, 0, -.875], atol=2e-14)


@pytest.mark.parametrize('p', [1, 2])
def test_triangle_nodal_completeness_and_partition(p):
    nodes = np.array([[0, 0], [1, 0], [0, 1], [.5, 0], [.5, .5], [0, .5]])[:3 if p == 1 else 6]
    np.testing.assert_allclose(triangle_lagrange(nodes, p), np.eye(len(nodes)), atol=1e-14)
    points = np.random.default_rng(30).dirichlet(np.ones(3), 30)[:, 1:]
    b = triangle_lagrange(points, p)
    np.testing.assert_allclose(b.sum(axis=1), 1, atol=1e-14)
    np.testing.assert_allclose(b@nodes, points, atol=1e-14)
    if p == 2:
        f = lambda x: x[:, 0]**2+x[:, 0]*x[:, 1]+2*x[:, 1]**2
        np.testing.assert_allclose(b@f(nodes), f(points), atol=1e-14)


def test_tensor_q2_has_nine_dofs_not_six_and_reproduces_xy_squared():
    z, _ = lobatto(2)
    nodes = np.array([(x, y) for x in z for y in z])
    np.testing.assert_allclose(tensor_basis(nodes, 2), np.eye(9), atol=1e-14)
    xy = np.array([[.2, -.4], [.8, .3]])
    b = tensor_basis(xy, 2)
    np.testing.assert_allclose(b@(nodes[:, 0]**2*nodes[:, 1]**2), xy[:, 0]**2*xy[:, 1]**2, atol=1e-14)


def test_invalid_parameters():
    for p in (-1, .5, True):
        with pytest.raises(ValueError): legendre([0], p)
    with pytest.raises(ValueError): lobatto(0)
    with pytest.raises(ValueError): lagrange([0], [0, 0])
    with pytest.raises(ValueError): element_matrices(2, length=0)
    with pytest.raises(ValueError): interval_basis([0], 2, 'unknown')
    with pytest.raises(ValueError): triangle_lagrange([[0, 0]], 3)


def test_scalar_and_multidimensional_tabulation():
    assert legendre(.3, 3).shape == (4,)
    assert legendre(.3, 3, derivative=True).shape == (4,)
    z, _ = lobatto(2)
    points = np.array([[0., .1], [.2, .3]])
    assert lagrange(points, z).shape == (2, 2, 3)
    np.testing.assert_allclose(np.einsum('...j,j->...', lagrange(points, z), z**2), points**2, atol=1e-14)


def test_chebyshev_orthogonality_requires_its_weight():
    n = 10
    theta = (np.arange(n)+.5)*np.pi/n
    b = interval_basis(np.cos(theta), 5, 'chebyshev')
    weighted = np.einsum('qi,qj->ij', b, b)*np.pi/n
    np.testing.assert_allclose(weighted, np.diag([np.pi]+[np.pi/2]*5), atol=2e-14)
    m, _ = element_matrices(5, 'chebyshev')
    assert abs(m[0, 2]+2/3) < 2e-14  # T0 and T2 are not orthogonal under dxi.
    x = np.linspace(-1, 1, 21)
    np.testing.assert_allclose(interval_basis(x, 3, 'chebyshev', derivative=True)[:, 3], 12*x*x-3, atol=2e-14)
