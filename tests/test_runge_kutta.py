import math
import numpy as np
import pytest
from numart.runge_kutta import (TABLEAUS,rk_step,stability_polynomial,stability_function,
                               nonlinear_trajectory)
from numart.time_integration import linear_trajectory
from numart.tvd import advection_rhs,total_variation


@pytest.mark.parametrize('method',TABLEAUS)
def test_rk_order_conditions_and_manufactured_nonlinear_time_dependence(method):
    m=TABLEAUS[method];a,b,c=m['A'],m['b'],m['c'];order=m['order']
    assert np.array_equal(a,np.tril(a,-1))
    conditions=[(b.sum(),1.)]
    if order>=2:conditions += [(b@c,.5)]
    if order>=3:conditions += [(b@(c*c),1/3),(b@a@c,1/6)]
    if order>=4:conditions += [(b@(c**3),.25),(b@(c*(a@c)),.125),
                              (b@a@(c*c),1/12),(b@a@a@c,1/24)]
    for actual,expected in conditions:assert actual==pytest.approx(expected,abs=4e-14)
    errors=[]
    for n in (20,40,80):
        y=1.;h=1/n
        for i in range(n):y=rk_step(lambda t,y:-y*y+np.exp(2*t)+np.exp(t),i*h,y,h,method)
        errors.append(abs(y-np.e))
    assert min(np.log2(np.array(errors[:-1])/errors[1:]))>order-.2


@pytest.mark.parametrize('method',TABLEAUS)
def test_linear_stability_matches_actual_stages_and_refinement(method):
    for z in (-.5,.2j,-.8+.7j):
        value=rk_step(lambda t,y:z*y,0.,np.array([1.,2.]),1.,method)
        np.testing.assert_allclose(value,stability_function(z,method)*np.array([1.,2.]),atol=2e-15)
    for k in range(TABLEAUS[method]['order']+1):
        assert stability_polynomial(method)[k]==pytest.approx(1/math.factorial(k),abs=4e-14)
    errors=[]
    for n in (20,40,80):
        _,y=linear_trajectory(dt=1/n,steps=n,method=method)
        errors.append(abs(y[-1]-np.exp(1j)))
    assert min(np.log2(np.array(errors[:-1])/errors[1:]))>TABLEAUS[method]['order']-.15


@pytest.mark.parametrize('method',[k for k,m in TABLEAUS.items() if m['ssp_coefficient']>0])
def test_ssp_decomposition_and_nonlinear_spatial_tvd(method):
    meta=TABLEAUS[method];a,b=meta['A'],meta['b'];c=meta['ssp_coefficient']
    # Absolute monotonicity conditions for the full tableau, not merely R(z).
    K=np.zeros((len(b)+1,len(b)+1));K[:-1,:-1]=a;K[-1,:-1]=b
    inverse=np.linalg.inv(np.eye(len(K))+c*K)
    assert (inverse@np.ones(len(K))).min()>=-5e-14
    assert (c*K@inverse).min()>=-5e-14
    rng=np.random.default_rng(42);q=rng.uniform(-1.,1.,64);dx=1/64
    new=rk_step(lambda t,q:advection_rhs(q,dx,1.,'superbee'),0.,q,c*.5*dx,method)
    assert total_variation(new)<=total_variation(q)+1e-12
    assert new.min()>=q.min()-1e-13 and new.max()<=q.max()+1e-13
    assert new.sum()==pytest.approx(q.sum(),abs=2e-13)


def test_rk2_same_linear_factor_different_nonlinear_stages_and_ssp():
    methods=('heun','explicit-midpoint','ralston')
    for method in methods:
        np.testing.assert_array_equal(stability_polynomial(method),[1.,1.,.5])
    values=[float(rk_step(lambda t,y:-y*y,0.,1.,.5,k)) for k in methods]
    assert len(set(values))==3
    for method in ('explicit-midpoint','kutta3','rk4'):
        m=TABLEAUS[method];s=len(m['b']);K=np.zeros((s+1,s+1));K[:s,:s]=m['A'];K[s,:s]=m['b']
        r=1e-4;inv=np.linalg.inv(np.eye(s+1)+r*K)
        assert (r*K@inv).min()<0
    result,stages=rk_step(lambda t,y:-y*y,0.,1.,.5,'heun',return_stages=True)
    assert [float(s['value']) for s in stages]==[1.,.5]
    assert float(result)==.6875
    np.testing.assert_allclose(nonlinear_trajectory('ssprk54',80)[1][-1],.5,atol=1e-10)


def test_invalid_explicit_rk_requests_fail():
    np.testing.assert_allclose(rk_step(lambda t,y:-y,0.,[1.,2.],.1),[.9048375,1.809675])
    for method,dt in (('midpoint',.1),('typo',.1),('rk4',0.),('rk4',np.nan)):
        with pytest.raises(ValueError):rk_step(lambda t,y:y,0.,1.,dt,method)
    with pytest.raises(ValueError):rk_step(lambda t,y:np.array([1.,2.]),0.,1.,.1)
