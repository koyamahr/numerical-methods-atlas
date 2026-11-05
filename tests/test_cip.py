import numpy as np
import pytest
from numart.cip import (hermite,cip_step,periodic_reconstruction,periodic_hermite_mass,
                       initial_profile,solve_advection,mass_counterexample)


def test_cubic_and_derivative_are_exactly_reproduced():
    p=lambda x:2.-3*x+.7*x*x+1.2*x**3
    d=lambda x:-3+1.4*x+3.6*x*x
    left,right=-.4,.7;s=np.linspace(0,1,41);x=left+(right-left)*s
    value,gradient=hermite(p(left),p(right),d(left),d(right),right-left,s)
    np.testing.assert_allclose(value,p(x),atol=2e-15)
    np.testing.assert_allclose(gradient,d(x),atol=4e-15)


@pytest.mark.parametrize('speed',[-1.,1.])
def test_integer_cell_shift_and_constant_state(speed):
    rng=np.random.default_rng(8);q=rng.normal(size=32);g=rng.normal(size=32)
    result,dresult=cip_step(q,g,1/32,1/32,speed)
    np.testing.assert_array_equal(result,np.roll(q,int(speed)))
    np.testing.assert_array_equal(dresult,np.roll(g,int(speed)))
    q=np.full(32,2.5);g=np.zeros(32)
    result,dresult=cip_step(q,g,1/32,.6/32,speed)
    np.testing.assert_array_equal(result,q);np.testing.assert_array_equal(dresult,g)


@pytest.mark.parametrize('speed',[-1.,1.])
@pytest.mark.parametrize('gradient',['analytic','centered'])
def test_smooth_refinement_and_gradient_transport(speed,gradient):
    errors=[];derivative_errors=[]
    for n in (32,64,128):
        result=solve_advection(n,speed=speed,gradient=gradient,final_time=.37)
        exact,dexact=initial_profile(result.x,'sine',.37,speed)
        errors.append(np.mean(abs(result.q-exact)));derivative_errors.append(np.mean(abs(result.gradient-dexact)))
    assert min(np.log2(np.array(errors[:-1])/errors[1:]))>2.7
    assert min(np.log2(np.array(derivative_errors[:-1])/derivative_errors[1:]))>2.6


def test_no_universal_conservation_claim_from_the_sine_test():
    result=solve_advection(64,final_time=.37)
    assert max(abs(h['mass']-1) for h in result.history)<2e-13
    case=mass_counterexample()
    difference=case['mass_after']-case['mass_before']
    assert abs(difference)>1e-3
    assert difference==pytest.approx(case['analytic_mass_change'],abs=1e-15)
    fine=(np.arange(32*101)+.5)/(32*101)
    shifted,_=periodic_reconstruction(np.ones(32),np.ones(32),fine-case['dt'])
    assert np.mean(shifted)==pytest.approx(1.,abs=2e-8)


def test_cip_is_not_a_bound_preserving_limiter():
    result=solve_advection(128,'square',final_time=.25,gradient='centered')
    assert result.q.min() < -1e-3 and result.q.max() > 1+1e-3
    linear=solve_advection(128,'square',method='linear',final_time=.25)
    assert linear.q.min()>=0 and linear.q.max()<=1
    assert linear.gradient is None


def test_zero_velocity_and_invalid_inputs():
    result=solve_advection(speed=0,final_time=1.)
    assert result.steps==0 and result.time==1.
    np.testing.assert_array_equal(result.q,initial_profile(result.x)[0])
    for kwargs in (dict(n=3),dict(n=12.5),dict(cfl=1.2),dict(final_time=-1),dict(speed=np.nan),dict(gradient='typo')):
        with pytest.raises(ValueError):solve_advection(**kwargs)
    with pytest.raises(ValueError):cip_step(np.ones(8),np.ones(8),.1,.11)
    with pytest.raises(ValueError):cip_step(np.ones(8),np.ones(7),.1,.01)
