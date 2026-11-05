import numpy as np
import pytest
from numart.time_integration import linear_trajectory,leapfrog_roots
from numart.geometry import (example_meshes,cubic_spline_kernel,sph_reconstruct,
    moving_volume_uniform_test)


@pytest.mark.parametrize('method,order',[('forward-euler',1),('backward-euler',1),('heun',2),('ssprk3',3),('rk4',4),('midpoint',2),('leapfrog',2)])
def test_time_refinement_against_exact_exponential(method,order):
    errors=[]
    for n in (20,40,80):
        t,y=linear_trajectory(dt=1/n,steps=n,method=method)
        errors.append(abs(y[-1]-np.exp(1j)))
    assert min(np.log2(np.array(errors[:-1])/errors[1:]))>order-.15


def test_leapfrog_roots_and_computational_mode():
    for z in (.2j,.9j,1.2j):
        roots=leapfrog_roots(z)
        for root in roots:np.testing.assert_allclose(root*root-2*z*root-1,0,atol=1e-14)
    assert max(abs(r) for r in leapfrog_roots(1.2j))>1
    t,y=linear_trajectory(rate=0j,dt=.1,steps=8,method='leapfrog',startup_perturbation=.01)
    np.testing.assert_allclose(y[::2],1);np.testing.assert_allclose(y[1::2],1.01)


def test_midpoint_preserves_oscillation_amplitude():
    _,y=linear_trajectory(dt=.5,steps=80,method='midpoint')
    np.testing.assert_allclose(abs(y),1,atol=3e-14)


def test_mesh_areas_topology_and_neighbors_cover_unit_square():
    for mesh in example_meshes().values():
        v,e,f=len(mesh['points']),len(mesh['edges']),len(mesh['cells'])
        assert v-e+f==1
        np.testing.assert_allclose(sum(mesh['areas']),1,atol=1e-14)
        assert min(mesh['areas'])>0
        for i,neighbors in enumerate(mesh['neighbors']):
            for j in neighbors:assert i in mesh['neighbors'][j]
        visited={0};todo=[0]
        while todo:
            for j in mesh['neighbors'][todo.pop()]:
                if j not in visited:visited.add(j);todo.append(j)
        assert len(visited)==f


def test_sph_kernel_normalization_and_constant_reproduction():
    x=np.linspace(-.2,.2,20001);h=.04
    np.testing.assert_allclose(np.sum(.5*(cubic_spline_kernel(x,h)[1:]+cubic_spline_kernel(x,h)[:-1])*np.diff(x)),1,atol=1e-12)
    p=(np.arange(32)+.5)/32+.007*np.sin(np.arange(32)*1.7)
    samples=np.linspace(0,1,101)
    q,partition=sph_reconstruct(samples,p,np.ones(32)*3,.045,normalize=True)
    np.testing.assert_allclose(q,3,atol=1e-14)
    assert np.max(abs(partition-1))>.001


@pytest.mark.parametrize('phase',[-1.5,-.4,.6,1.5])
def test_ale_uniform_state_preservation_on_moving_volumes(phase):
    old,new,q=moving_volume_uniform_test(phase=phase)
    assert np.min(np.diff(new))>0
    np.testing.assert_allclose(q,1,atol=2e-15)
