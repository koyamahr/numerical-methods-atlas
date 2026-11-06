import numpy as np
import pytest
from numart.euler2d import conserved, primitive, physical_flux
from numart.shock_cases import (oblique_shock, normal_flux, reflected, wedge_mesh,
    solve_wedge, shock_cell_fractions, step_geometry, step_rhs, solve_forward_step)


def test_weak_shock_matches_nasa_table_and_rankine_hugoniot():
    r=oblique_shock(2.5,15.)
    assert abs(np.rad2deg(r['beta'])-36.94490)<1e-5
    assert abs(r['pressure_ratio']-2.467500)<1e-6
    assert abs(r['density_ratio']-1.866549)<1e-6
    assert abs(r['downstream_mach']-1.873526)<1e-6
    nx,ny=-np.sin(r['beta']),np.cos(r['beta'])
    flux=lambda q:nx*physical_flux(q,0)+ny*physical_flux(q,1)
    np.testing.assert_allclose(flux(r['upstream']),flux(r['downstream']),atol=3e-14)
    with pytest.raises(ValueError): oblique_shock(1.1,30.)


def test_oriented_flux_consistency_and_shared_face_cancellation():
    left=conserved([1.2,2.,-.3,.7]);right=conserved([.8,-.2,.5,1.])
    nx,ny=np.cos(.7),np.sin(.7)
    np.testing.assert_allclose(normal_flux(left,left,nx,ny),nx*physical_flux(left,0)+ny*physical_flux(left,1),atol=1e-14)
    np.testing.assert_allclose(normal_flux(left,right,nx,ny),-normal_flux(right,left,-nx,-ny),atol=1e-14)
    ghost=reflected(left,nx,ny)
    assert abs(normal_flux(left,ghost,nx,ny)[0])<1e-14
    assert abs(normal_flux(left,ghost,nx,ny)[3])<1e-14


def test_body_fitted_face_geometry_closes_and_has_correct_area():
    x,y,volumes,vertical,lengths,(nx,ny)=wedge_mesh(12)
    assert np.all(volumes>0)
    np.testing.assert_allclose(vertical[1:]-vertical[:-1]+nx[:,1:]*lengths[:,1:]-nx[:,:-1]*lengths[:,:-1],0,atol=3e-16)
    np.testing.assert_allclose(ny[:,1:]*lengths[:,1:]-ny[:,:-1]*lengths[:,:-1],0,atol=3e-16)
    assert abs(volumes.sum()-(1.5*1.2-.5*np.tan(np.deg2rad(15))))<1e-14
    assert np.any(x[:,0]==0.)


def test_polygon_shock_average_splits_a_cell_exactly():
    x,y=np.meshgrid([0.,1.],[0.,1.],indexing='ij')
    np.testing.assert_allclose(shock_cell_fractions(x,y,np.pi/4),[[.5]],atol=1e-15)
    np.testing.assert_allclose(shock_cell_fractions(x-2,y,np.pi/4),0)


def test_step_mask_preserves_wall_mass_and_energy_balance():
    x,y,fluid=step_geometry(10)
    assert abs(fluid.sum()*.01-2.52)<1e-14
    q=np.broadcast_to(conserved([1.4,3.,0.,1.]),(*fluid.shape,4)).copy()
    rhs=step_rhs(q,fluid,.1)
    np.testing.assert_allclose(rhs[~fluid],0)
    inflow=physical_flux(q[0,0],0)
    np.testing.assert_allclose(rhs.sum(axis=(0,1))[[0,3]]*.01,.2*inflow[[0,3]],atol=1e-13)


def test_short_wedge_run_and_step_snapshots_stay_physical():
    wedge=solve_wedge(8,final_time=.05)
    assert wedge.time==.05 and wedge.steps>1
    assert np.all(primitive(wedge.q)[...,[0,3]]>0)
    plain=solve_forward_step(10,final_time=.04)
    sampled=solve_forward_step(10,final_time=.04,snapshot_times=[0.,.02,.04])
    np.testing.assert_array_equal(plain.q,sampled.q)
    assert sampled.snapshots[0].time==0 and sampled.snapshots[-1].time==.04
    assert np.all(primitive(sampled.q)[sampled.fluid][:,[0,3]]>0)


def test_wedge_refines_against_integrated_shock_reference():
    reference=oblique_shock(2.5)
    errors=[]
    for n in (10,20):
        result=solve_wedge(n,2.5,final_time=3.)
        fraction=shock_cell_fractions(result.x_nodes,result.y_nodes,reference['beta'])
        exact_density=1+(reference['density_ratio']-1)*fraction
        errors.append(np.sum(result.volumes*abs(result.q[...,0]-exact_density))/result.volumes.sum())
    assert errors[1]<.8*errors[0]
