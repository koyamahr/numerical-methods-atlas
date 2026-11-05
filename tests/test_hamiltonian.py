import numpy as np
import pytest
from numart.hamiltonian import METHODS,J,canonical_step,energy,trajectory


@pytest.mark.parametrize('method,order',[('symplectic-euler',1),('verlet',2),('yoshida4',4),('midpoint',2),('rk4',4)])
def test_canonical_oscillator_refinement_order(method,order):
    exact=np.array([np.cos(1)+.2*np.sin(1),-np.sin(1)+.2*np.cos(1)])
    errors=[]
    for n in (20,40,80):
        _,z=trajectory(h=1/n,steps=n,method=method)
        errors.append(np.linalg.norm(z[-1]-exact))
    assert min(np.log2(np.array(errors[:-1])/errors[1:]))>order-.15


@pytest.mark.parametrize('system',['harmonic','quartic'])
@pytest.mark.parametrize('method',METHODS)
def test_map_jacobians_against_independent_differences_and_symplectic_form(method,system):
    z=np.array([.7,.4]);h=.35;eps=1e-6
    _,m=canonical_step(z,h,method,system,True)
    fd=np.column_stack([(canonical_step(z+eps*e,h,method,system)-canonical_step(z-eps*e,h,method,system))/(2*eps) for e in np.eye(2)])
    np.testing.assert_allclose(m,fd,atol=2e-10,rtol=2e-9)
    defect=np.linalg.norm(m.T@J@m-J)
    if method=='rk4':assert defect>1e-6
    else:assert defect<2e-14


@pytest.mark.parametrize('method',['verlet','yoshida4','midpoint'])
def test_symmetric_maps_reverse_fixed_steps_for_nonlinear_system(method):
    initial=np.array([.7,.4]);z=initial.copy()
    for _ in range(20):z=canonical_step(z,.2,method,'quartic')
    for _ in range(20):z=canonical_step(z,-.2,method,'quartic')
    np.testing.assert_allclose(z,initial,atol=1e-13)


def test_energy_is_distinct_from_symplecticity():
    h=.2
    _,sv=trajectory(h=h,steps=4000,method='verlet')
    # A modified quadratic is exact for this oscillator map, not the original H.
    modified=.5*(sv[:,1]**2+(1-h*h/4)*sv[:,0]**2)
    np.testing.assert_allclose(modified,modified[0],atol=2e-13)
    assert np.max(abs(energy(sv)-energy(sv[0])))>1e-3
    _,mid=trajectory(h=h,steps=2000,method='midpoint')
    np.testing.assert_allclose(energy(mid),energy(mid[0]),atol=2e-13)
    _,nonlinear=trajectory(h=h,steps=500,method='midpoint',system='quartic')
    assert np.max(abs(energy(nonlinear,'quartic')-energy(nonlinear[0],'quartic')))>1e-4


def test_large_step_can_be_symplectic_and_unstable():
    # Symplecticity alone does not give oscillator stability at h > 2.
    _,m=canonical_step([1.,0.],2.2,'verlet',return_jacobian=True)
    np.testing.assert_allclose(m.T@J@m,J,atol=1e-14)
    assert max(abs(np.linalg.eigvals(m)))>1


def test_symplectic_euler_is_not_time_symmetric_and_invalid_parameters_fail():
    z=np.array([.7,.4]);forward=canonical_step(z,.2,'symplectic-euler')
    assert np.linalg.norm(canonical_step(forward,-.2,'symplectic-euler')-z)>1e-3
    for kwargs in ({'method':'unknown'},{'system':'unknown'},{'h':float('nan')},{'steps':-1}):
        with pytest.raises(ValueError):trajectory(**kwargs)
