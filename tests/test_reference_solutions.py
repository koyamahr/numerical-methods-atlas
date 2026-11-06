import numpy as np
import pytest

from numart.reference_riemann import RiemannSolution
from numart.reference_solutions import get_reference, list_references, riemann_reference
from numart.riemann import exact_euler


@pytest.mark.parametrize('left,right', [((1,0,1),(.125,0,.1)),((.445,.698,3.528),(.5,0,.571)),
                                      ((1,-2,.4),(1,2,.4)),((1,1,1),(2,1,1)),((1,2,1),(1,-2,1))])
def test_euler_matches_existing_independent_reference(left,right):
    r=RiemannSolution('euler',left,right)
    xi=np.linspace(-8,8,1001)
    np.testing.assert_allclose(r.primitive(r.sample(xi)),exact_euler(xi,left,right),rtol=2e-11,atol=2e-12)


@pytest.mark.parametrize('model,left,right,p',[
    ('euler',(1,0,1),(.125,0,.1),1.4),('euler',(1,3,1),(1,-3,1),5/3),
    ('shallow-water',(2,0),(1,0),1.),('shallow-water',(1,2),(1,-2),9.81),
    ('isothermal',(1,0),(.125,0),1.),('isothermal',(1,3),(1,-2),.7)])
def test_reference_shocks_satisfy_rankine_hugoniot_and_lax(model,left,right,p):
    r=RiemannSolution(model,left,right,p)
    for wave in r.waves:
        if wave['kind']!='shock':continue
        s=wave['speeds'][0];ql,qr=r.sample(np.array([s-1e-6,s+1e-6]))
        np.testing.assert_allclose(r.flux(qr)-r.flux(ql),s*(qr-ql),rtol=2e-10,atol=2e-10)
        wl,wr=r.primitive(np.array([ql,qr]));side=wave['family']
        assert wr[1]+side*r._sound(wr) < s < wl[1]+side*r._sound(wl)


@pytest.mark.parametrize('model,left,right,p',[
    ('euler',(1,-4,.4),(1,4,.4),1.4),('euler',(0,0,0),(1,0,1),1.4),
    ('euler',(1,0,1),(0,0,0),1.4),('shallow-water',(1,-3),(1,3),1.),
    ('shallow-water',(1,0),(0,0),1.),('shallow-water',(0,0),(1,0),1.)])
def test_vacuum_and_dry_fans_have_nonnegative_states_and_correct_pde(model,left,right,p):
    r=RiemannSolution(model,left,right,p);assert r.vacuum
    q=r.sample(np.linspace(-10,10,2001));assert np.all(q[:,0]>=0)
    assert np.all(q[q[:,0]==0]==0)
    for wave in r.waves:
        a,b=sorted(wave['speeds']);xi=(a+b)/2;h=1e-5
        # Similarity ODE: dF/dxi = xi dU/dxi, independently differenced.
        minus,plus=r.sample(np.array([xi-h,xi+h]))
        np.testing.assert_allclose((r.flux(plus)-r.flux(minus))/(2*h),xi*(plus-minus)/(2*h),rtol=3e-7,atol=3e-8)


def test_isothermal_fan_invariants_and_no_finite_middle_vacuum():
    r=RiemannSolution('isothermal',(1,-100),(1,100),1.)
    assert not r.vacuum and r.star>0
    assert r.sample(0.)[0]>0
    for wave,w in zip(r.waves,(r.left,r.right)):
        xi=np.linspace(*sorted(wave['speeds']),15)[1:-1]
        primitive=r.primitive(r.sample(xi));side=wave['family']
        np.testing.assert_allclose(primitive[:,1]-side*np.log(primitive[:,0]),w[1]-side*np.log(w[0]),atol=1e-12)


@pytest.mark.parametrize('name',list_references())
def test_catalog_shapes_initial_data_and_quadrature_reports(name):
    c=get_reference(name)
    assert c.kind in ('analytic','semi-analytic','manufactured')
    if c.dimension!=1:return
    a,b=c.bounds[0];edges=np.array([a,a+.137*(b-a),a+.503*(b-a),a+.811*(b-a),b])
    report=c.cell_average_report(edges,c.final_time)
    assert report['values'].shape==(4,len(c.components))
    assert max(report['max_order_difference']) < 3e-10
    assert c.point(a,c.final_time).shape==(len(c.components),)
    assert c.point(np.linspace(a,b,8),0).shape==(8,len(c.components))


def test_front_split_cell_integrals_conserve_mass_momentum_and_energy():
    for name,t,initial,net_flux in [
        ('euler-sod',.2,np.array([.5625,0,1.375]),np.array([0,.9,0])),
        ('swe-dam-break',.1,np.array([1.5,0]),np.array([0,1.5]))]:
        c=get_reference(name);edges=np.linspace(0,1,38)
        q=c.cell_average(edges,t)
        np.testing.assert_allclose(np.einsum('i,ij->j',np.diff(edges),q),initial+t*net_flux,atol=2e-12)
    # A discontinuity cuts this cell: its average is not its center value.
    c=get_reference('burgers-shock');edges=np.array([.5,.7]);t=.123
    np.testing.assert_allclose(c.cell_average(edges,t),[[.3075]],atol=1e-14)
    assert c.point(.6,t)[0]==0


def test_smooth_means_and_nonuniform_error_norms_have_independent_integrals():
    c=get_reference('sine-advection');e=np.array([0,.13,.44,1.]);t=.37
    exact=1+.25*(np.cos(2*np.pi*(e[:-1]-t))-np.cos(2*np.pi*(e[1:]-t)))/(2*np.pi*np.diff(e))
    np.testing.assert_allclose(c.cell_average(e,t)[:,0],exact,atol=4e-16)
    norms=c.compare_means(c.cell_average(e,t)+np.array([[1],[2],[3]]),e,t)
    w=np.diff(e)
    np.testing.assert_allclose(norms['l1'],[w@[1,2,3]])
    np.testing.assert_allclose(norms['l2'],[np.sqrt(w@[1,4,9])])
    np.testing.assert_allclose(norms['linf'],[3])


def test_taylor_green_box_means_and_continuum_equations():
    c=get_reference('taylor-green');lo=np.array([.2,.4]);hi=np.array([1.1,1.7]);t=.23
    sinmean=(np.cos(lo)-np.cos(hi))/(hi-lo);cosmean=(np.sin(hi)-np.sin(lo))/(hi-lo)
    cos2mean=(np.sin(2*hi)-np.sin(2*lo))/(2*(hi-lo));d=np.exp(-.2*t)
    np.testing.assert_allclose(c.box_average(lo,hi,t),[sinmean[0]*cosmean[1]*d,-cosmean[0]*sinmean[1]*d,.25*sum(cos2mean)*d*d],atol=5e-16)
    p=np.array([.7,1.2]);h=2e-4;q=c.point(p,t)
    ex=np.array([h,0]);ey=np.array([0,h])
    dx=(c.point(p+ex,t)-c.point(p-ex,t))/(2*h);dy=(c.point(p+ey,t)-c.point(p-ey,t))/(2*h)
    dt=(c.point(p,t+h)-c.point(p,t-h))/(2*h)
    lap=(c.point(p+ex,t)+c.point(p-ex,t)+c.point(p+ey,t)+c.point(p-ey,t)-4*q)/h**2
    assert abs(dx[0]+dy[1])<1e-9
    np.testing.assert_allclose(dt[:2]+q[0]*dx[:2]+q[1]*dy[:2],-np.array([dx[2],dy[2]])+.1*lap[:2],atol=2e-8)


def test_manufactured_forcing_and_channel_profiles():
    c=get_reference('poisson-manufactured');x=np.linspace(.1,.9,11);h=1e-4
    minus_second=-(c.point(x+h)-2*c.point(x)+c.point(x-h))/h**2
    np.testing.assert_allclose(minus_second,c.source(x),rtol=4e-8)
    assert np.max(abs(c.point(np.array([0,1]))))<2e-16
    np.testing.assert_allclose(get_reference('couette').cell_average([0,1]),[[.5]])
    np.testing.assert_allclose(get_reference('poiseuille').cell_average([0,1]),[[5/6]])


def test_reject_invalid_states_times_and_cells():
    for args in [('isothermal',(0,0),(1,0),1.),('euler',(1,0,0),(1,0,1),1.4),
                 ('euler',(1,0,1),(1,0,1),1.),('shallow-water',(-1,0),(1,0),1.)]:
        with pytest.raises(ValueError):RiemannSolution(*args)
    c=get_reference('euler-sod')
    for edges in [[0,0,1],[1,0],[0,float('nan')]]:
        with pytest.raises(ValueError):c.cell_average(edges,.1)
    with pytest.raises(ValueError):c.point(0,-1)
    with pytest.raises(ValueError):c.cell_average([0,1],order=0)
    with pytest.raises(ValueError):c.compare_means(np.zeros((1,1)),[0,1],.1)
    with pytest.raises(ValueError):get_reference('taylor-green').cell_average([0,1])
    with pytest.raises(ValueError):get_reference('missing')
