import numpy as np
import pytest
from numart.poisson_comparison import dst1,direct_1d,direct_2d,problem,solve,METHODS
from numart.multigrid import laplacian_operator


def test_fft_dst_matches_independent_sine_matrix_and_is_self_inverse():
    rng=np.random.default_rng(31);a=rng.normal(size=(7,4))
    s=np.sqrt(2/8)*np.sin(np.pi*np.arange(1,8)[:,None]*np.arange(1,8)[None,:]/8)
    np.testing.assert_allclose(dst1(a),s@a,atol=3e-15)
    np.testing.assert_allclose(dst1(dst1(a)),a,atol=1e-15)
    np.testing.assert_allclose(dst1(a,1),a@ (np.sqrt(2/5)*np.sin(np.pi*np.arange(1,5)[:,None]*np.arange(1,5)[None,:]/5)),atol=2e-15)


def test_direct_methods_match_dense_discrete_systems():
    n=7;t=np.diag(np.full(n,2.))-np.diag(np.ones(n-1),1)-np.diag(np.ones(n-1),-1)
    f=np.random.default_rng(19).normal(size=n)
    for method in ['thomas','fft-dst']:np.testing.assert_allclose(direct_1d(f,method),np.linalg.solve(t*64,f),atol=2e-17)
    f=np.random.default_rng(2).normal(size=(n,n));a=64*(np.kron(t,np.eye(n))+np.kron(np.eye(n),t))
    for method in ['fft-dst','dst-thomas']:np.testing.assert_allclose(direct_2d(f,method).ravel(),np.linalg.solve(a,f.ravel()),atol=3e-17)


@pytest.mark.parametrize('method',METHODS)
def test_all_methods_use_the_same_true_relative_residual_and_solution(method):
    _,f,_=problem(15,'localized');original=f.copy();r=solve(f,method)
    assert r.converged and r.history[-1,2]<=1e-8
    actual=np.linalg.norm(f-laplacian_operator(r.q,1/16))/np.linalg.norm(f)
    np.testing.assert_allclose(r.history[-1,2],actual,rtol=2e-15,atol=2e-16)
    np.testing.assert_allclose(r.q,direct_2d(f),atol=2e-8)
    np.testing.assert_array_equal(f,original)
    assert np.all(np.diff(r.history[:,1])>=0)


def test_broad_source_avoids_single_mode_cg_benchmark_trap():
    _,f,_=problem(31,'single-mode');assert solve(f,'cg').steps==1
    _,f,_=problem(31,'manufactured');assert solve(f,'cg').steps>20


def test_manufactured_solution_second_order_and_zero_forcing():
    errors=[]
    for n in [15,31,63]:
        _,f,exact=problem(n);errors.append(np.max(abs(direct_2d(f)-exact)))
    assert min(np.log2(np.array(errors[:-1])/errors[1:]))>1.9
    for method in METHODS:
        r=solve(np.zeros((7,7)),method);assert r.steps==0 and r.converged
    with pytest.raises(ValueError):solve(np.ones((10,10)),'multigrid')
    assert not solve(problem(31)[1],'jacobi',max_steps=2).converged
