import numpy as np
from numart.muscl2d import (geometry,gradients,hll,solve_shock,smooth_entropy,entropy_average)
from numart.shock_cases import wedge_mesh,normal_flux,step_geometry
from numart.euler2d import conserved,primitive


def test_oriented_hll_retains_the_existing_acoustic_flux():
    rng=np.random.default_rng(52)
    left=rng.uniform(.2,2,(20,4));right=rng.uniform(.2,2,(20,4))
    nx,ny=np.cos(.37),np.sin(.37)
    np.testing.assert_allclose(hll(left,right,nx,ny),normal_flux(conserved(left),conserved(right),nx,ny),rtol=2e-14,atol=2e-14)


def test_physical_centroids_and_limited_gradients_reproduce_affine_fields():
    x,y,*_=wedge_mesh(10);g=geometry(x,y)
    a=np.array([.1,.3,.2,.1]);b=np.array([.2,-.1,.1,-.2])
    w=2+g.cx[...,None]*a+g.cy[...,None]*b
    for kind in ('minmod','mc'):
        gx,gy=gradients(w,g.cx,g.cy,kind)
        np.testing.assert_allclose(gx,np.broadcast_to(a,gx.shape),atol=5e-13)
        np.testing.assert_allclose(gy,np.broadcast_to(b,gy.shape),atol=5e-13)


def test_smooth_2d_cell_average_refinement_and_periodic_conservation():
    errors=[]
    for n in (16,32,64):
        r=smooth_entropy(n)
        errors.append(np.mean(abs(r.q[...,0]-entropy_average(n,.5)[...,0])))
        np.testing.assert_allclose(r.q.sum(axis=(0,1)),entropy_average(n,0).sum(axis=(0,1)),rtol=3e-14,atol=1e-10)
        assert r.retries==0
    assert np.log2(errors[-2]/errors[-1])>1.8


def test_shock_cases_do_not_depend_on_snapshot_requests():
    plain=solve_shock('step',10,limiter='mc',final_time=.05)
    saved=solve_shock('step',10,limiter='mc',final_time=.05,snapshot_times=[0,.025,.05])
    np.testing.assert_array_equal(plain.q,saved.q)
    assert saved.snapshots[-1].time==.05
    assert np.all(primitive(saved.q)[saved.fluid][:,[0,3]]>0)
    wedge=solve_shock('wedge',10,limiter='minmod',final_time=.05)
    assert np.all(primitive(wedge.q)[...,[0,3]]>0)


def test_blocked_step_walls_preserve_the_initial_mass_and_energy_budget():
    from numart.muscl2d import boundary_rhs
    from numart.euler2d import physical_flux
    x,y,fluid=step_geometry(10);g=geometry(x,y);w=np.array([1.4,3.,0.,1.])
    q=np.broadcast_to(conserved(w),(*fluid.shape,4)).copy()
    for kind in ('first','minmod','mc'):
        rhs,scaled=boundary_rhs(q,g,kind,'step',w,fluid)
        total=np.sum(rhs*g.volume[...,None],axis=(0,1))
        np.testing.assert_allclose(total[[0,3]],.2*physical_flux(conserved(w),0)[[0,3]],atol=3e-13)
        np.testing.assert_array_equal(rhs[~fluid],0)
