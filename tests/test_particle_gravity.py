import numpy as np
import pytest
from numart.particle_gravity import (cic_deposit,cic_interpolate,periodic_poisson,
    pm_acceleration,direct_acceleration,tree_acceleration)


def test_periodic_cic_mass_wrap_and_constant_interpolation():
    rng=np.random.default_rng(9);x=rng.uniform(-2,3,(31,3));m=rng.uniform(.1,1,31)
    rho=cic_deposit(x,m,n=12,length=2)
    np.testing.assert_allclose(rho.sum()*(2/12)**3,m.sum(),rtol=2e-15)
    np.testing.assert_allclose(rho,cic_deposit(x+2,m,n=12,length=2),atol=3e-13)
    np.testing.assert_allclose(cic_interpolate(np.ones((3,12,12,12))*2.7,x,length=2),2.7,atol=1e-14)


def test_periodic_poisson_sinusoid_gauge_and_mean_removal():
    n=16;x=np.arange(n)/n
    rho=np.broadcast_to(np.cos(2*np.pi*x)[:,None,None],(n,n,n))
    phi,force=periodic_poisson(rho+3)
    np.testing.assert_allclose(phi,-rho/np.pi,atol=1e-14)
    np.testing.assert_allclose(force[0],np.broadcast_to(-2*np.sin(2*np.pi*x)[:,None,None],rho.shape),atol=2e-14)
    np.testing.assert_allclose(force[1:],0,atol=2e-14)
    assert abs(phi.mean())<1e-15
    uniform,zero=periodic_poisson(np.ones_like(rho)*3)
    np.testing.assert_allclose(uniform,0);np.testing.assert_allclose(zero,0)


def test_pm_self_force_and_total_internal_force_with_matched_cic():
    x=np.array([[.234,.421,.653]])
    acceleration,_,_=pm_acceleration(x,np.array([1.]),n=16)
    np.testing.assert_allclose(acceleration,0,atol=2e-13)
    rng=np.random.default_rng(7);x=rng.random((19,3));m=rng.uniform(.5,1.5,19)
    a,_,_=pm_acceleration(x,m,n=16)
    np.testing.assert_allclose(np.sum(m[:,None]*a,axis=0),0,atol=5e-12)


def test_direct_force_reciprocity_and_tree_exact_opening_limit():
    rng=np.random.default_rng(3);x=rng.random((35,3));m=rng.uniform(.1,1,35)
    direct=direct_acceleration(x,m)
    np.testing.assert_allclose(np.sum(m[:,None]*direct,axis=0),0,atol=3e-13)
    for order in (0,2):
        tree,counts=tree_acceleration(x,m,theta=0,order=order)
        np.testing.assert_allclose(tree,direct,rtol=3e-15,atol=2e-13)
        assert counts['direct_pairs']==35*34 and counts['accepted_nodes']==0


def test_second_moment_improves_selected_cluster_force_and_theta_refinement():
    rng=np.random.default_rng(17);x=rng.random((100,3));m=np.ones(100)/100
    exact=direct_acceleration(x,m);errors={}
    for order in (0,2):
        for theta in (.4,.8):
            a,counts=tree_acceleration(x,m,theta=theta,order=order)
            errors[order,theta]=np.linalg.norm(a-exact)/np.linalg.norm(exact)
            assert counts['accepted_nodes']>0
    assert errors[0,.4]<errors[0,.8]
    assert errors[2,.8]<errors[0,.8]/2
    assert errors[2,.4]<errors[2,.8]


def test_coincident_particles_terminate_and_bad_parameters_fail():
    x=np.zeros((3,3));m=np.ones(3)
    tree,_=tree_acceleration(x,m)
    np.testing.assert_allclose(tree,0)
    for kwargs in ({'theta':-1},{'order':1},{'softening':0}):
        with pytest.raises(ValueError):tree_acceleration(x,m,**kwargs)
