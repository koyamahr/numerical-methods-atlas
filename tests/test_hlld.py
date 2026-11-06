import numpy as np
import pytest
from numart.hlld import conserved,primitive,physical_flux,riemann
from numart.mhd_tests import (solve_1d,alfven_average,initial_loop,divergence,
    solve_loop,ct_contact_emf,interface_flux,loop_rhs)


@pytest.mark.parametrize('axis',[0,1,2])
def test_uniform_flux_and_vector_rotation(axis):
    w=np.array([1.2,.3,-.2,.1,.8,.7,-.4,.2])
    f,a,stats=riemann(w,w,axis=axis)
    np.testing.assert_allclose(f,physical_flux(w,axis=axis),rtol=2e-14,atol=2e-14)
    assert stats['hlle_fallback_faces']==0
    np.testing.assert_allclose(primitive(conserved(w)),w,atol=2e-15)


def test_hlld_resolves_moving_contact_and_stationary_rotation():
    left=np.array([1.,.3,0,0,1.,.75,1.,0]);right=left.copy();right[0]=2.
    f,_,stats=riemann(left,right)
    np.testing.assert_allclose(f,physical_flux(left),atol=2e-14)
    left=np.array([1.,-.75,-.3,0,1.,.75,.3,0]);right=np.array([1.,-.75,0,-.3,1.,.75,0,.3])
    np.testing.assert_allclose(physical_flux(left),physical_flux(right),atol=2e-14)
    f,_,_=riemann(left,right)
    np.testing.assert_allclose(f,physical_flux(left),atol=2e-14)
    f,_,_=riemann(left,right,solver='hlle')
    assert np.linalg.norm(f-physical_flux(left))>.01


def test_zero_normal_field_and_parallel_field_degeneracies_are_finite():
    for w in (np.array([1.,0,0,0,.1,2.,0,0]),np.array([1.,.2,0,0,1.,0,0,0])):
        f,_,stats=riemann(w,w)
        np.testing.assert_allclose(f,physical_flux(w),atol=2e-14)
        assert stats['degenerate_faces']>0
    a=np.array([1.,0,0,0,1.,.5,.2,.1]);b=a.copy();b[5]=.6
    with pytest.raises(ValueError,match='one normal'):riemann(a,b)


def test_brio_wu_retains_longitudinal_field_and_positive_states():
    for solver in ('hlle','hlld'):
        r=solve_1d('brio-wu',128,solver=solver)
        w=primitive(r.q,2.)
        assert np.min(w[:,0])>0 and np.min(w[:,4])>0
        np.testing.assert_allclose(w[:,5],.75,atol=2e-14)
        assert r.stats['retried_steps']==0


def test_circular_alfven_refinement_and_periodic_conservation():
    errors=[]
    for n in (32,64,128):
        r=solve_1d('alfven',n)
        errors.append(np.mean(abs(r.q[:,6:8]-alfven_average(n,1)[:,6:8])))
        np.testing.assert_allclose(r.q.sum(axis=0),alfven_average(n).sum(axis=0),atol=2e-11)
    assert np.log2(errors[-2]/errors[-1])>1.7


def test_ct_corner_emf_reduces_to_1d_face_flux():
    q=np.repeat(alfven_average(32)[:,None,:],8,axis=1)
    bx=np.ones((32,8));by=q[...,6].copy()
    fx,_,_=interface_flux(q,0,'hlld','mc',bx)
    fy,_,_=interface_flux(q,1,'hlld','mc',by)
    ez=ct_contact_emf(fx,fy,primitive(q),1/32,1/8)
    np.testing.assert_allclose(ez,-fx[...,6],atol=2e-14)


@pytest.mark.parametrize('method',['ct','glm'])
def test_loop_initialization_and_short_evolution(method):
    q,bx,by,dx,dy=initial_loop(16,method)
    assert np.max(abs(divergence(q,dx,dy,bx,by)))<1e-14
    r=solve_loop(16,.1,method,snapshot_times=[0,.05,.1])
    assert r.snapshots[0].time==0 and r.snapshots[-1].time==.1
    np.testing.assert_allclose(r.q[...,0].mean(),q[...,0].mean(),atol=2e-14)
    np.testing.assert_allclose(r.q[...,4].mean(),q[...,4].mean(),atol=2e-13)
    if method=='ct':assert np.max(abs(divergence(r.q,dx,dy,r.bx,r.by)))<1e-13
    assert r.stats['retried_steps']==0


def test_invalid_hlld_intermediate_state_uses_the_counted_hlle_fallback():
    # Positive high-shear input states, but an inadmissible HLLD intermediate.
    left=np.array([1.50926005,2.31774355,-7.05154876,7.88046939,.03012983,-3.13384788,5.34328653,-1.87355438])
    right=np.array([26.75847098,-4.75310389,4.27165121,8.54084505,4.79867510,-3.13384788,.96521633,4.78402266])
    flux,_,stats=riemann(left,right)
    reference,_,_=riemann(left,right,solver='hlle')
    assert stats['hlle_fallback_faces']==1
    assert np.all(np.isfinite(flux))
    np.testing.assert_array_equal(flux,reference)
