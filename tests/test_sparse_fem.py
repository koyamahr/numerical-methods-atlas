import numpy as np
import pytest
from numart.krylov import (apply, CSR, gmres, bicgstab, jacobi_preconditioner,
    ilu0_preconditioner, advection_diffusion_matrix, newton)
from numart.fem import poisson_1d, poisson_2d, error_norms, triangle_quadrature


def test_sparse_assembly_accumulates_duplicate_entries():
    a = CSR.from_coo([0, 0, 1, 1], [0, 0, 0, 1], [2., 3., -1., 4.], (2, 2))
    np.testing.assert_allclose(a.matvec([2., 3.]), [10., 10.])


@pytest.mark.parametrize('solver', [gmres, bicgstab])
@pytest.mark.parametrize('preconditioner', [None, jacobi_preconditioner, ilu0_preconditioner])
def test_nonsymmetric_solve_true_residual_and_error(solver, preconditioner):
    a = advection_diffusion_matrix(n=9)
    expected = np.random.default_rng(24).normal(size=81)
    b = a.matvec(expected)
    result = solver(a, b, preconditioner=preconditioner(a) if preconditioner else None, maxiter=600)
    assert result.converged, result.reason
    assert np.linalg.norm(a.matvec(result.x)-b) <= 1e-10*np.linalg.norm(b)
    np.testing.assert_allclose(result.x, expected, atol=2e-8)


def test_gmres_restart_and_failure_are_explicit():
    a = advection_diffusion_matrix(n=8)
    b = np.ones(64)
    short = gmres(a, b, restart=3, maxiter=1)
    assert not short.converged
    assert short.reason == 'iteration limit'
    result = gmres(a, b, restart=8, maxiter=500)
    assert result.converged
    assert result.iterations > 8


def test_ilu_tridiagonal_is_exact_and_zero_pivot_fails():
    dense = 4*np.eye(12)-np.eye(12, k=1)-np.eye(12, k=-1)
    i, j = np.nonzero(dense)
    a = CSR.from_coo(i, j, dense[i, j], dense.shape)
    b = np.arange(12.)
    np.testing.assert_allclose(ilu0_preconditioner(a)(b), np.linalg.solve(dense, b), atol=2e-15)
    bad = CSR.from_coo([0, 1], [0, 1], [0., 1.], (2, 2))
    with pytest.raises(np.linalg.LinAlgError):
        ilu0_preconditioner(bad)


def test_damped_newton_backtracks_and_reports_failure():
    function = lambda x: x**3-1
    jacobian = lambda x: np.diag(3*x*x)
    result = newton(function, jacobian, [.1])
    assert result.converged
    assert min(result.step_lengths) < 1
    np.testing.assert_allclose(result.x, [1.], atol=1e-10)
    assert not newton(function, jacobian, [.1], maxiter=1).converged


def test_bratu_newton_krylov_refines_to_continuous_reference():
    errors = []
    lam = 2/np.cosh(.5)**2
    for n in (31, 63):
        x = np.arange(1, n+1)/(n+1)
        d = 2*np.eye(n)-np.eye(n, k=1)-np.eye(n, k=-1)
        d *= (n+1)**2
        def jacobian(u):
            dense = d-np.diag(lam*np.exp(u))
            i, j = np.nonzero(dense)
            return CSR.from_coo(i, j, dense[i, j], dense.shape)
        result = newton(lambda u: apply(d, u)-lam*np.exp(u), jacobian, np.zeros(n), linear_solver='gmres')
        assert result.converged, result.reason
        exact = -2*np.log(np.cosh(x-.5)/np.cosh(.5))
        errors.append(np.max(abs(result.x-exact)))
    assert errors[1] < .27*errors[0]


def test_interval_mass_stiffness_and_linear_patch():
    r = poisson_1d(16, forcing=lambda x: 0., boundary=lambda x: 1+2*x)
    np.testing.assert_allclose(r.u, 1+2*r.points[:, 0], atol=5e-14)
    np.testing.assert_allclose(r.stiffness.matvec(np.ones(17)), 0., atol=1e-14)
    assert abs(r.mass.data.sum()-1) < 1e-14


def test_triangle_patch_nonzero_boundary_and_energy():
    r = poisson_2d(5, forcing=lambda p: 0., boundary=lambda p: 2+p[:, 0]-3*p[:, 1])
    np.testing.assert_allclose(r.u, 2+r.points[:, 0]-3*r.points[:, 1], atol=2e-10)
    assert abs(r.u@r.stiffness.matvec(r.u)-10) < 1e-9
    assert abs(r.mass.data.sum()-1) < 1e-13


def test_triangle_fem_l2_and_h1_convergence():
    exact = lambda p: np.sin(np.pi*p[:, 0])*np.sin(np.pi*p[:, 1])
    gradient = lambda p: np.pi*np.column_stack((np.cos(np.pi*p[:, 0])*np.sin(np.pi*p[:, 1]), np.sin(np.pi*p[:, 0])*np.cos(np.pi*p[:, 1])))
    errors = np.array([error_norms(poisson_2d(n), exact, gradient) for n in (4, 8, 16)])
    rates = np.log2(errors[:-1]/errors[1:])
    assert min(rates[:, 0]) > 1.8
    assert min(rates[:, 1]) > .9


def test_quadrature_orientation_and_linear_gradients():
    vertices = np.array([[0., 0.], [2., 0.], [0., 3.]])
    for v in (vertices, vertices[[0, 2, 1]]):
        points, weights, basis, gradients = triangle_quadrature(v)
        assert abs(weights.sum()-3) < 1e-14
        np.testing.assert_allclose(v[:, 0]@gradients, [1, 0], atol=1e-15)
