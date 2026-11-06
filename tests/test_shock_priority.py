import numpy as np
import pytest
from numart.equations import Euler
from numart.riemann import roe_flux,exact_euler
from numart.roe_properties import parameter,parameter_maps,roe_matrix,flux_jacobian,eigensystem,normal_shock
from numart.shock_robustness import flux,roe_basis,shock_states,solve_shock,initial_shock,pressure_sensor
from numart.euler2d import conserved,physical_flux


def test_roe_quadratic_maps_jump_identity_and_consistency():
    rng=np.random.default_rng(91);w=rng.uniform(.1,2,(240,3));w[:,1]-=1
    eq=Euler();left=eq.conserved(w);right=eq.conserved(w[::-1]);a=roe_matrix(left,right)
    q,f=parameter_maps(parameter(left));np.testing.assert_allclose(q,left,atol=3e-15);np.testing.assert_allclose(f,eq.flux(left),atol=3e-15)
    np.testing.assert_allclose(np.einsum('nij,nj->ni',a,right-left),eq.flux(right)-eq.flux(left),rtol=3e-13,atol=8e-15)
    np.testing.assert_allclose(roe_matrix(left,left),flux_jacobian(left),atol=3e-14)
    lam,r,l=eigensystem(left,right)
    np.testing.assert_allclose(a,np.einsum('nij,nj,njk->nik',r,lam,l),atol=3e-14)
    np.testing.assert_allclose(l@r,np.broadcast_to(np.eye(3),r.shape),atol=3e-14)


@pytest.mark.parametrize('speed',[0.,.7,-.4])
def test_single_shock_and_contact_are_recognized_without_entropy_smoothing(speed):
    eq=Euler();left,right=normal_shock(3,speed)
    np.testing.assert_allclose(eq.flux(right)-eq.flux(left),speed*(right-left),atol=3e-14)
    np.testing.assert_allclose(roe_matrix(left,right)@(right-left),speed*(right-left),atol=3e-14)
    expected=eq.flux(left if speed>=0 else right)
    np.testing.assert_allclose(roe_flux(left,right,eq,0),expected,atol=3e-14)
    left,right=eq.conserved(np.array([[1.,speed,1.],[2.,speed,1.]]))
    np.testing.assert_allclose(roe_flux(left,right,eq,0),eq.flux(left if speed>=0 else right),atol=3e-14)


def test_property_u_does_not_select_the_entropy_solution():
    eq=Euler();left,right=normal_shock(2,reverse=True)
    np.testing.assert_allclose(eq.flux(left),eq.flux(right),atol=3e-15)
    np.testing.assert_allclose(roe_flux(left,right,eq,0),eq.flux(left),atol=4e-15)
    state=eq.conserved(exact_euler(np.array([0.]),eq.primitive(left),eq.primitive(right)))[0]
    assert np.linalg.norm(eq.flux(state)-eq.flux(left))>.01
    assert np.linalg.norm(roe_flux(left,right,eq,.1)-eq.flux(left))>.01


@pytest.mark.parametrize('axis',[0,1])
def test_2d_roe_jump_matrix_and_constant_flux(axis):
    rng=np.random.default_rng(73);wl=rng.uniform(.2,2,(30,4));wr=rng.uniform(.2,2,(30,4));wl[:,1:3]-=1;wr[:,1:3]-=1
    left,right=conserved(wl),conserved(wr);r,lam,*_=roe_basis(left,right,axis)
    a=np.einsum('nij,nj,njk->nik',r,lam,np.linalg.inv(r))
    np.testing.assert_allclose(np.einsum('nij,nj->ni',a,right-left),physical_flux(right,axis)-physical_flux(left,axis),atol=1e-14)
    for solver in ['roe','hll','hlle','hybrid']:
        np.testing.assert_allclose(flux(left,left,axis,solver,blend=np.full(30,.5)),physical_flux(left,axis),atol=2e-15)


def test_unperturbed_stationary_shock_and_pressure_contact_sensor():
    r=solve_shock(32,entropy_fraction=0,amplitude=0,final_time=.04)
    q=initial_shock(32,amplitude=0)[2]
    np.testing.assert_allclose(r.q,q,atol=3e-13)
    assert np.max(r.history[:,1:4])<1e-13
    w=np.ones((16,8,4));w[...,1:3]=0;w[:8,:,0]=2
    np.testing.assert_array_equal(pressure_sensor(conserved(w)),0)


def test_controlled_odd_even_mode_growth_and_phase_sensitivity():
    # Diagnostic-specific behavior, not a universal carbuncle-free claim.
    roe=solve_shock(32,final_time=.15);hlle=solve_shock(32,'hlle',final_time=.15)
    assert roe.history[-1,1]>10*roe.history[0,1]
    assert hlle.history[-1,1]<hlle.history[0,1]
    assert roe.retried_steps==hlle.retried_steps==0


def test_ausm_splits_contacts_supersonic_upwinding_and_mach_boundaries():
    from numart.ausm import flux as ausm,mach_split,pressure_split
    m=np.array([-3.,-1.,-.9,0.,.9,1.,3.])
    np.testing.assert_allclose(mach_split(m,1)+mach_split(m,-1),m,atol=2e-16)
    np.testing.assert_allclose(pressure_split(m,1)+pressure_split(m,-1),1.,atol=2e-16)
    eq=Euler()
    for u in [-.3,0.,.3]:
        a,b=eq.conserved(np.array([[1.,u,1.],[2.,u,1.]]))
        np.testing.assert_allclose(ausm(a,b),eq.flux(a if u>=0 else b),atol=2e-15)
    a,b=eq.conserved(np.array([[1.,5.,1.],[2.,6.,1.]]))
    np.testing.assert_allclose(ausm(a,b),eq.flux(a),atol=2e-14)
    a,b=eq.conserved(np.array([[1.,-5.,1.],[2.,-6.,1.]]))
    np.testing.assert_allclose(ausm(a,b),eq.flux(b),atol=2e-14)
    for axis in [0,1]:
        q=conserved(np.array([1.2,.3,-.2,1.]))
        np.testing.assert_allclose(ausm(q,q,axis=axis),physical_flux(q,axis),atol=2e-15)
