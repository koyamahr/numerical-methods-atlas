import numpy as np
from numart.euler2d import conserved,physical_flux,primitive,GAMMA
from numart.keep import keep_flux,rhs,vortex_state,solve_vortex


def test_keep_equal_state_consistency_and_symmetric_two_point_flux():
    left=conserved([1.2,.7,-.3,.9]);right=conserved([.8,-.2,.4,1.1])
    for axis in (0,1):
        np.testing.assert_allclose(keep_flux(left,left,axis),physical_flux(left,axis),atol=5e-16)
        np.testing.assert_array_equal(keep_flux(left,right,axis),keep_flux(right,left,axis))


def test_keep_periodic_primary_conservation_and_kinetic_pressure_work_identity():
    c=(np.arange(16)+.5)/16;x,y=np.meshgrid(c,c,indexing='ij')
    w=np.stack((1+.1*np.sin(2*np.pi*x),.4+.2*np.sin(2*np.pi*y),
                .3+.1*np.cos(2*np.pi*x),1+.15*np.cos(2*np.pi*(x+y))),axis=-1)
    q=conserved(w);dq=rhs(q,length=1.)
    np.testing.assert_allclose(dq.sum(axis=(0,1)),0,atol=3e-14)
    velocity=w[...,1:3];dK=np.sum(velocity*dq[...,1:3],axis=-1)-.5*np.sum(velocity**2,axis=-1)*dq[...,0]
    divu=sum(8*(np.roll(velocity[...,a],-1,axis=a)-np.roll(velocity[...,a],1,axis=a)) for a in (0,1))
    np.testing.assert_allclose(dK.sum(),(w[...,3]*divu).sum(),atol=8e-15)


def test_original_keep_does_not_implicitly_claim_pressure_equilibrium_preservation():
    n=24;c=np.arange(n)/n;x,y=np.meshgrid(c,c,indexing='ij')
    w=np.stack((1+.2*np.sin(2*np.pi*(x+y)),np.ones_like(x)*.7,
                np.ones_like(x)*.4,np.ones_like(x)),axis=-1)
    q=conserved(w);dq=rhs(q,length=1.)
    dK=np.sum(w[...,1:3]*dq[...,1:3],axis=-1)-.5*np.sum(w[...,1:3]**2,axis=-1)*dq[...,0]
    dp=(GAMMA-1)*(dq[...,3]-dK)
    assert abs(dp).max()>1e-4  # deliberate diagnostic, not a PEP variant


def test_vortex_reference_is_isentropic_and_periodic_at_test_box_precision():
    c=np.linspace(-9.9,9.9,41);x,y=np.meshgrid(c,c,indexing='ij')
    q=vortex_state(x,y,time=.7);w=primitive(q)
    np.testing.assert_allclose(w[...,3]/w[...,0]**GAMMA,1,atol=3e-16)
    np.testing.assert_allclose(vortex_state(x+20,y,time=.7),q,atol=6e-15)


def test_keep_vortex_refines_and_primary_totals_are_conservative():
    errors=[]
    for n in (32,64,128):
        r=solve_vortex(n,.1,cfl=.25,snapshot_times=[0,.1])
        errors.append(r.density_l1)
        for key in ('mass','momentum_x','momentum_y','total_energy'):
            np.testing.assert_allclose(r.history[-1][key],r.history[0][key],rtol=4e-15)
        assert r.snapshots[-1].time==.1
    assert min(np.log2(np.array(errors[:-1])/errors[1:]))>1.7
