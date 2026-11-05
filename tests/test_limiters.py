import numpy as np
import pytest
from numart import get_problem, solve
from numart.limiters import (LIMITERS, limited_slope, limiter_function, tvb_minmod,
                             positive_reconstruction, euler_pressure)
from numart.tvd import solve_advection, cell_average, advection_rhs, total_variation


@pytest.mark.parametrize("limiter", LIMITERS)
def test_sweby_bounds_symmetry_and_plateaus(limiter):
    r = np.r_[np.linspace(-4, 0, 51), np.geomspace(1.e-8, 1.e8, 401), 1.]
    phi = limiter_function(r, limiter)
    assert np.all(phi >= 0)
    assert np.all(phi <= np.maximum(0, np.minimum(2*r, 2))+1.e-14)
    assert limiter_function(1., limiter) == pytest.approx(1.)
    a = np.array([-2., -.1, 0., 0., 2., 1., -1.])
    b = np.array([-1., -2., 0., 3., 0., 3., 2.])
    assert np.allclose(limited_slope(a,b,limiter), limited_slope(b,a,limiter))
    assert np.allclose(limited_slope(-a,-b,limiter), -limited_slope(a,b,limiter))
    for scale in (1.e-150, 1.e150):
        assert np.allclose(limited_slope(a*scale,b*scale,limiter)/scale, limited_slope(a,b,limiter))
    assert np.array_equal(limited_slope(a,b,limiter)[2:5], [0.,0.,0.])


@pytest.mark.parametrize("limiter", LIMITERS)
@pytest.mark.parametrize("speed", [-1., 1.])
def test_scalar_tvd_mass_and_bounds(limiter, speed):
    r = solve_advection(64, limiter=limiter, speed=speed, final_time=.37, cfl=.5)
    tv = np.array([h['tv'] for h in r.history])
    assert np.max(np.diff(tv)) < 2.e-13
    assert r.q.min() >= -1.e-13 and r.q.max() <= 1+1.e-13
    assert max(abs(h['mass']-.2) for h in r.history) < 2.e-13
    rng = np.random.default_rng(123)
    q = rng.uniform(-1.,1.,128)
    forward_euler = q+.5/128*advection_rhs(q, 1/128, speed, limiter)
    assert total_variation(forward_euler) <= total_variation(q)+1.e-12


@pytest.mark.parametrize("limiter", LIMITERS)
def test_smooth_refinement_and_sod(limiter):
    errors = []
    for n in (40, 80, 160):
        r = solve_advection(n, profile="sine", limiter=limiter, final_time=.2)
        errors.append(np.mean(abs(r.q-cell_average(r.x, 1/n, "sine", r.time))))
    assert errors[0]/errors[1] > 2.5 and errors[1]/errors[2] > 2.5
    result = solve(get_problem("sod"), 96, limiter=limiter)
    assert np.all(np.isfinite(result.q))
    assert get_problem("sod").equation.primitive(result.q)[:,[0,2]].min() > 0


def test_tvb_extremum_bypass_and_zero_limit():
    assert tvb_minmod(.001, -.001, .003, .01, M=10) == pytest.approx(.001)
    assert tvb_minmod(.001, -.001, .003, .01, M=0) == 0
    a, b = np.array([1.,-2.,1.]), np.array([3.,-1.,-1.])
    assert np.allclose(tvb_minmod(.5*(a+b),a,b,.1,0), limited_slope(a,b))
    tvd = solve_advection(80, "sine", final_time=.3)
    tvb = solve_advection(80, "sine", limiter="tvb", tvb_M=50, final_time=.3)
    ref = cell_average(tvb.x,1/80,"sine",tvb.time)
    assert np.mean(abs(tvb.q-ref)) < np.mean(abs(tvd.q-ref))


@pytest.mark.parametrize("delta", [[1.2,0.,0.],[0.,3.,0.],[1.2,3.,1.]])
def test_positive_scaling_conservation_and_pressure(delta):
    mean = np.array([1.,0.,2.5])
    nodes = np.array([-1.,0.,1.])
    states = mean+nodes[:,None]*delta
    weights = np.array([1/6,2/3,1/6])
    result, theta = positive_reconstruction(mean,states,density_floor=1.e-8,pressure_floor=1.e-8)
    assert 0 < theta < 1
    assert result[:,0].min() >= 1.e-8*(1-1.e-6)
    assert euler_pressure(result).min() >= 1.e-8*(1-1.e-6)
    assert np.allclose(weights@result, mean, atol=1.e-15)
    assert np.allclose(result,mean+theta*(states-mean))


def test_positive_scaling_identity_and_inadmissible_means():
    mean=np.array([1.,0.,2.5]);states=np.array([[.8,.1,2.],[1.2,-.1,3.]])
    result,theta=positive_reconstruction(mean,states)
    assert theta == 1 and np.array_equal(result,states)
    for bad in ([0.,0.,2.5], [1.,3.,1.]):
        with pytest.raises(ValueError,match="mean"):
            positive_reconstruction(bad,states)
    with pytest.raises(ValueError):
        limited_slope(1.,2.,"typo")
    with pytest.raises(ValueError):
        solve(get_problem('sod'),method='weno5',limiter='superbee')
    for dx,M in ((0.,1.),(.1,-1.),(.1,np.nan)):
        with pytest.raises(ValueError):
            tvb_minmod(1.,1.,1.,dx,M)
