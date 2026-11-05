import numpy as np
import pytest
from numart.multigrid import (red_black_gauss_seidel,laplacian_operator,
    solve_poisson_multigrid,prolong_bilinear,restrict_full_weighting)
from numart.linear import poisson_2d


def test_red_black_fixed_point_solves_discrete_equation():
    n=9
    h=1/(n+1)
    rng=np.random.default_rng(9)
    exact=rng.normal(size=(n,n))
    f=laplacian_operator(exact,h)
    np.testing.assert_allclose(red_black_gauss_seidel(exact,f,h,3),exact,atol=2e-15)


def test_grid_transfer_shapes_and_injection():
    e=np.arange(9,dtype=float).reshape(3,3)
    fine=prolong_bilinear(e)
    assert fine.shape==(7,7)
    np.testing.assert_array_equal(fine[1::2,1::2],e)
    assert restrict_full_weighting(fine).shape==(3,3)


def test_multigrid_against_cg_and_residual():
    n=31
    f=np.random.default_rng(21).normal(size=(n,n))
    q,history=solve_poisson_multigrid(f)
    _,_,cg,_=poisson_2d(n,forcing=f,tolerance=1e-12)
    np.testing.assert_allclose(q,cg,atol=1e-11)
    assert np.linalg.norm(f-laplacian_operator(q,1/(n+1)))<1e-8
    assert len(history)<30


def test_multigrid_removes_smooth_error_faster_than_relaxation():
    n=31
    f=np.ones((n,n))
    q,hist=solve_poisson_multigrid(f,tolerance=1e-8)
    relaxed=red_black_gauss_seidel(np.zeros_like(f),f,1/(n+1),6*(len(hist)-1))
    assert np.linalg.norm(f-laplacian_operator(relaxed,1/(n+1)))>hist[-1]*1000


def test_multigrid_rejects_non_nested_grid():
    with pytest.raises(ValueError):
        solve_poisson_multigrid(np.ones((30,30)))
