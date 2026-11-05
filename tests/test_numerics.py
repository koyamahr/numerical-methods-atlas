import numpy as np
import pytest
from numart import get_problem, list_problems, solve
from numart.equations import Euler, Barotropic
from numart.riemann import numerical_flux, exact_euler
from numart.solvers import _weno_left
from numart.advection import (amplification, difference_step, fourier_derivative,
    spectral_advection, dg_advection, rd_residual, dual_time_advection, conditioning_example)
from numart.mhd import solve_orszag_tang, primitive, initial_orszag_tang


@pytest.mark.parametrize("eq",[Euler(),Barotropic(),Barotropic("isothermal")])
@pytest.mark.parametrize("solver",["rusanov","hll","hlle","hllc","roe"])
def test_flux_consistency(eq,solver):
    if solver in ("hllc","roe","hlle") and not isinstance(eq,Euler):
        pytest.skip("HLLC/Roe are intentionally Euler-only")
    w = np.array([[1.,.4,1.],[.5,-.2,.6]]) if isinstance(eq,Euler) else np.array([[1.,.4],[.5,-.2]])
    q = eq.conserved(w)
    np.testing.assert_allclose(numerical_flux(q,q,eq,solver),eq.flux(q),atol=2e-15)


def test_hllc_stationary_contact_is_exact():
    eq = Euler()
    ql,qr = eq.conserved(np.array([[1.,0.,1.],[.125,0.,1.]]))
    np.testing.assert_allclose(numerical_flux(ql,qr,eq,"hllc"),[0.,1.,0.],atol=1e-14)


def test_exact_sod_star_and_regions():
    # Independent canonical star values, shock and undisturbed states.
    w = exact_euler(np.array([-2.,0.,1.,2.]))
    np.testing.assert_allclose(w[1],[.426319428,.927452620,.303130178],rtol=2e-8)
    np.testing.assert_allclose(w[2],[.265573712,.927452620,.303130178],rtol=2e-8)
    np.testing.assert_allclose(w[[0,3]],[[1,0,1],[.125,0,.1]])


@pytest.mark.parametrize("left,right",[((1.,0.,1.),(.125,0.,.1)),((.445,.698,3.528),(.5,0.,.571)),((1.,-1.,.4),(1.,1.,.4))])
def test_exact_riemann_reflection_symmetry(left,right):
    xi=np.linspace(-3,3,137)
    a=exact_euler(xi,left,right)
    b=exact_euler(-xi,(right[0],-right[1],right[2]),(left[0],-left[1],left[2]))
    b[:,1]*=-1
    np.testing.assert_allclose(a,b,atol=1e-13)


@pytest.mark.parametrize("method",["godunov","muscl","weno5"])
def test_sod_accuracy_and_refinement(method):
    p=get_problem("sod")
    errors=[]
    for n in (80,160):
        r=solve(p,n,method=method)
        w=p.equation.primitive(r.q)
        assert np.all(w[:,[0,2]]>0)
        errors.append(np.mean(abs(r.q[:,0]-p.reference(r.x,r.time)[:,0])))
    assert errors[1]<.85*errors[0]
    assert errors[1]<.035


@pytest.mark.parametrize("method",["muscl","weno5"])
def test_periodic_euler_conservation_and_entropy_wave(method):
    p=get_problem("entropy-wave")
    r=solve(p,80,method=method,final_time=.2)
    np.testing.assert_allclose(r.q.sum(axis=0),p.initial(r.x).sum(axis=0),rtol=2e-13,atol=2e-13)
    assert np.mean(abs(r.q[:,0]-p.reference(r.x,r.time)[:,0]))<.003


@pytest.mark.parametrize("name",list_problems())
def test_benchmark_default_horizon_smoke(name):
    p=get_problem(name)
    r=solve(p,64,riemann="hlle" if name == "double-rarefaction" else "hll" if p.equation.name != "euler" else "hllc")
    assert r.time == p.final_time
    assert np.all(np.isfinite(p.equation.primitive(r.q)))


def test_weno_spatial_fifth_order():
    errors=[]
    for n in (40,80,160):
        x=(np.arange(n)+.5)/n
        q=np.sin(2*np.pi*x)[:,None]
        f=_weno_left(np.pad(q,((3,3),(0,0)),mode="wrap"))[:-1]
        errors.append(np.mean(abs((f[1:,0]-f[:-1,0])*n-2*np.pi*np.cos(2*np.pi*x))))
    assert min(np.log2(np.array(errors[:-1])/errors[1:]))>4.5


@pytest.mark.parametrize("method",["upwind","lax-friedrichs","lax-wendroff"])
@pytest.mark.parametrize("c",[-.8,.8,1.1])
def test_amplification_matches_actual_discrete_mode(method,c):
    n,k=64,13
    q=np.exp(2j*np.pi*k*np.arange(n)/n)
    np.testing.assert_allclose(difference_step(q,c,method),amplification(2*np.pi*k/n,c,method)*q,atol=2e-14)
    maxg=max(abs(amplification(np.linspace(0,np.pi,1000),c,method)))
    assert (maxg <= 1+1e-12) == (abs(c)<=1)


def test_fourier_derivative_and_propagator():
    x=np.arange(64)/64
    np.testing.assert_allclose(fourier_derivative(np.sin(6*np.pi*x)),6*np.pi*np.cos(6*np.pi*x),atol=3e-13)
    np.testing.assert_allclose(spectral_advection(np.sin(6*np.pi*x),.173),np.sin(6*np.pi*(x-.173)),atol=4e-15)


@pytest.mark.parametrize("degree",[0,1,2])
@pytest.mark.parametrize("speed",[-1.,1.])
def test_dg_order_and_conservation(degree,speed):
    errors=[]
    for n in (16,32):
        x,u,modes=dg_advection(n,degree,.2,speed)
        errors.append(np.sqrt(np.mean((u-np.sin(2*np.pi*(x-speed*.2)))**2)))
        assert abs(modes[:,0].mean())<1e-14
    assert np.log2(errors[0]/errors[1])>degree+.5


@pytest.mark.parametrize("speed",[-1.,1.])
def test_rd_global_conservation_and_upwind_equivalence(speed):
    q=np.random.default_rng(42).normal(size=64)
    residual=rd_residual(q,speed)
    assert abs(residual.sum())<1e-12
    np.testing.assert_allclose(q+.005*residual,difference_step(q,speed*.005*64,"upwind"),atol=1e-15)


def test_dual_time_satisfies_implicit_equations_above_explicit_cfl():
    n,dt=32,.05
    x,q,history=dual_time_advection(n,dt,.1,order=2,tolerance=1e-12)
    d=n*(np.eye(n)-np.roll(np.eye(n),1,axis=0))
    q0=np.sin(2*np.pi*x)
    q1=np.linalg.solve(np.eye(n)/dt+d,q0/dt)
    q2=np.linalg.solve(1.5*np.eye(n)/dt+d,(2*q1-.5*q0)/dt)
    np.testing.assert_allclose(q,q2,atol=2e-11)
    assert history[-1]<history[0]*1e-9
    assert abs(q.mean())<1e-14


def test_symmetric_jacobi_conditioning():
    a,p=conditioning_example()
    assert np.linalg.cond(p)<np.linalg.cond(a)/100
    assert np.linalg.eigvalsh(p).min()>0


@pytest.mark.parametrize("method",["ct","glm"])
def test_orszag_tang_positivity_and_periodic_conservation(method):
    r=solve_orszag_tang(24,.5,method)
    assert primitive(r.q)[3].min()>0
    np.testing.assert_allclose(r.history[-1,2:],r.history[0,2:],rtol=1e-13)
    if method == "ct":
        assert abs(r.divergence).max()<1e-11


def test_glm_damps_injected_longitudinal_error():
    r=solve_orszag_tang(32,.1,"glm",magnetic_error=.01)
    assert r.history[0,1]>.05
    assert r.history[-1,1]<.8*r.history[0,1]


def test_invalid_combinations_fail_explicitly():
    with pytest.raises(ValueError):
        solve(get_problem("dam-break"),32,riemann="hllc")
    with pytest.raises(ValueError):
        exact_euler([0.],(1.,-10.,1.),(1.,10.,1.))
    with pytest.raises(ValueError):
        solve(get_problem("sod"),32,cfl=1.2)


def test_hlle_low_density_expansion_stays_positive():
    p=get_problem("double-rarefaction")
    r=solve(p,100,method="godunov",riemann="hlle")
    w=p.equation.primitive(r.q)
    assert w[:,0].min()>0
    assert w[:,2].min()>0
    assert w[:,0].min()<.1  # actually reached the dilute central region


def test_roe_acoustic_entropy_fix_changes_transonic_rarefaction():
    from numart.riemann import roe_flux
    eq=Euler()
    q=eq.conserved(np.array([[1.,-.5,.4],[1.,.5,.4]]))
    # Shift the Roe-averaged acoustic eigenvalue to zero, creating a sonic wave.
    r,u,p=np.moveaxis(eq.primitive(q),-1,0)
    h=(q[:,2]+p)/r
    a=np.sqrt((eq.gamma-1)*h.mean())
    shifted=eq.conserved(np.stack((r,u+a,p),axis=-1))
    assert np.max(abs(roe_flux(*shifted,eq,entropy_fraction=0)-roe_flux(*shifted,eq)))>1e-5


def test_spatial_stencil_direction_and_orders():
    from numart.advection import finite_difference
    errors={s:[] for s in ("forward","backward","centered")}
    for n in (40,80):
        x=np.arange(n)/n
        for s in errors:
            errors[s].append(np.linalg.norm(finite_difference(np.sin(2*np.pi*x),1/n,s)-2*np.pi*np.cos(2*np.pi*x))/np.sqrt(n))
        np.testing.assert_allclose(finite_difference(x,1/n,"upwind",-1),finite_difference(x,1/n,"forward"))
    for s in errors:
        assert np.log2(errors[s][0]/errors[s][1])>(1.8 if s == "centered" else .9)
