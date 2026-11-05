import numpy as np
import pytest
from numart.stiff import integrate, adaptive_sdirk2, sdirk2_step
from numart.incompressible import divergence, gradient, project, taylor_green
from numart.lattice_boltzmann import equilibrium, moments, step, shear_wave, poiseuille, CS2
from numart.scalar_gallery import solve, godunov, riemann_cell_averages


@pytest.mark.parametrize('method,minimum', [('be', .85), ('bdf2', 1.75), ('sdirk2', 1.85), ('imex-euler', .85)])
def test_implicit_orders_on_nonautonomous_nonlinear_exact_solution(method, minimum):
    # y=1/(1+t); nonlinear and time-dependent forcing.
    f = lambda t, y: -y*y + np.sin(t)*(y-1/(1+t))
    jac = lambda t, y: np.diag(-2*y+np.sin(t))
    errors = []
    for dt in (.05, .025, .0125):
        _, y = integrate(f, jac, [1.], dt=dt, method=method, explicit=lambda t,y: np.zeros_like(y))
        errors.append(abs(y[-1,0]-.5))
    assert min(np.log2(np.array(errors[:-1])/errors[1:])) > minimum


def test_stiff_decay_and_local_error_control():
    f = lambda t,y: -1000*(y-np.cos(t))-np.sin(t)
    jac = lambda t,y: -1000*np.eye(len(y))
    coarse = adaptive_sdirk2(f,jac,[1.],rtol=1e-3)
    fine = adaptive_sdirk2(f,jac,[1.],rtol=1e-6)
    assert fine.times[-1] == 1.
    assert max(abs(fine.states[:,0]-np.cos(fine.times))) < 3e-6
    assert fine.accepted > coarse.accepted
    decay = sdirk2_step(lambda t,y:-1e8*y,lambda t,y:-1e8*np.eye(1),0.,np.ones(1),1.)
    assert abs(decay[0]) < 1e-6
    with pytest.raises(RuntimeError):
        adaptive_sdirk2(f,jac,[1.],maxsteps=1)


def test_periodic_projection_adjoint_and_divergence():
    rng=np.random.default_rng(12)
    u,v,p=rng.normal(size=(3,18,18)); h=.3
    gx,gy=gradient(p,h)
    np.testing.assert_allclose(np.sum(p*divergence(u,v,h)), -np.sum(u*gx+v*gy),atol=1e-11)
    a,b=project(u,v,h)
    assert np.max(abs(divergence(a,b,h))) < 2e-14
    aa,bb=project(a,b,h)
    np.testing.assert_allclose(aa,a,atol=2e-15)
    assert np.sum(a*a+b*b) <= np.sum(u*u+v*v)


def test_taylor_green_refinement_energy_and_pressure():
    errors=[]
    for n in (16,32,64):
        result=taylor_green(n)
        errors.append(result['error'])
        assert max(result['history'][:,2]) < 1e-13
        assert np.all(np.diff(result['history'][:,1]) < 0)
        assert abs(result['pressure'].mean()) < 1e-16
    assert min(np.log2(np.array(errors[:-1])/errors[1:])) > 1.9


def test_lbm_equilibrium_moments_and_periodic_conservation():
    rng=np.random.default_rng(32)
    rho=1+.001*rng.normal(size=(8,9)); u=.01*rng.normal(size=(2,8,9))
    f=equilibrium(rho,u)
    rr,uu=moments(f)
    np.testing.assert_allclose(rr,rho,atol=5e-16)
    np.testing.assert_allclose(uu,u,atol=1e-16)
    before=np.array([f.sum(),np.sum(rho*u[0]),np.sum(rho*u[1])])
    for _ in range(20): f=step(f)
    rr,uu=moments(f)
    after=np.array([f.sum(),np.sum(rr*uu[0]),np.sum(rr*uu[1])])
    np.testing.assert_allclose(after,before,atol=2e-13)
    with pytest.raises(ValueError):step(f,tau=.5)


def test_lbm_shear_viscosity_refines():
    errors=[]
    for n in (16,32,64):
        result=shear_wave(n,steps=n*n//8)
        measured=-np.log(result['amplitude'][-1]/result['amplitude'][0])/(result['time'][-1]*(2*np.pi/n)**2)
        errors.append(abs(measured-result['viscosity']))
        assert result['viscosity'] == pytest.approx(CS2*.3)
    assert min(np.log2(np.array(errors[:-1])/errors[1:])) > 1.8


def test_lbm_channel_halfway_wall_refinement():
    errors=[]
    for n in (8,16):
        result=poiseuille(n)
        errors.append(result['error'])
        assert result['max_mach'] < .02
        assert np.max(abs(result['rho']-1)) < 2e-11
        np.testing.assert_allclose(result['velocity'],result['velocity'][::-1],atol=1e-14)
    assert errors[0]/errors[1] > 3.8


def test_godunov_transonic_entropy_fluxes():
    assert godunov(-1.,1.) == 0.
    assert godunov(.9,.1,'traffic') == .25
    assert godunov(.3,.9,'traffic') == pytest.approx(.09)


@pytest.mark.parametrize('equation,left,right',[('burgers',1.,0.),('burgers',0.,1.),('traffic',.3,.9),('traffic',.9,.1)])
def test_scalar_riemann_refinement(equation,left,right):
    errors=[]
    for n in (80,160):
        initial=riemann_cell_averages(n,0,left,right,equation)
        result=solve(initial,.3,equation,order=1)
        exact=riemann_cell_averages(n,.3,left,right,equation)
        errors.append(np.mean(abs(result['u']-exact)))
    assert errors[1] < .8*errors[0]


def test_periodic_scalar_conservation_and_snapshot_observation():
    x=(np.arange(100)+.5)/100; u=.5+.35*np.sin(2*np.pi*x)
    a=solve(u,.2,'traffic',boundary='periodic')
    b=solve(u,.2,'traffic',boundary='periodic',snapshot_times=np.linspace(0,.2,13))
    np.testing.assert_array_equal(a['u'],b['u'])
    assert abs(a['u'].sum()-u.sum()) < 1e-12
    assert a['u'].min() >= u.min()-1e-14 and a['u'].max() <= u.max()+1e-14


def test_hyperbolic_diffusion_steady_refinement_and_failure():
    from numart.hyperbolic_diffusion import steady_sine
    errors=[]
    for n in (32,64,128):
        r=steady_sine(n)
        errors.append(r['error'])
        assert r['history'][-1] <= 1e-9
        assert abs(r['u'].mean()) < 2e-12
    assert min(np.log2(np.array(errors[:-1])/errors[1:])) > .85
    with pytest.raises(RuntimeError):steady_sine(maxsteps=1)
