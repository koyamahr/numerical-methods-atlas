import numpy as np
import pytest
from numart.coordinates import (cylindrical_velocity_gradient, newtonian_stress,
    cylindrical_stress_divergence, cylindrical_basis)


def test_solid_rotation_has_no_viscous_stress():
    r, omega = .7, 2.3
    u = [0., omega*r, 0.]
    d = np.zeros((3,3)); d[1,0] = omega
    g = cylindrical_velocity_gradient(r,u,d)
    np.testing.assert_allclose(g,[[0,-omega,0],[omega,0,0],[0,0,0]])
    np.testing.assert_allclose(newtonian_stress(g,1.7,.9),0.,atol=1e-14)


def test_pipe_poiseuille_viscous_force_and_pressure_balance():
    mu, peak, radius = 1.3, 2.1, 1.8
    for r in (.1,.6,1.2):
        u = [0.,0.,peak*(1-r*r/radius**2)]
        d = np.zeros((3,3)); d[2,0] = -2*peak*r/radius**2
        t = newtonian_stress(cylindrical_velocity_gradient(r,u,d),mu)
        dt = np.zeros((3,3,3)); dt[2,0,0] = dt[0,2,0] = -2*mu*peak/radius**2
        force = cylindrical_stress_divergence(r,t,dt)
        np.testing.assert_allclose(force,[0,0,-4*mu*peak/radius**2])
        pressure_gradient = np.array([0.,0.,-4*mu*peak/radius**2])
        np.testing.assert_allclose(-pressure_gradient+force,0.,atol=1e-14)


def test_cylindrical_couette_torque_and_zero_azimuthal_force():
    a,b,mu = 1.1,.4,2.
    r = .8
    d = np.zeros((3,3));d[1,0] = a-b/r**2
    t = newtonian_stress(cylindrical_velocity_gradient(r,[0,a*r+b/r,0],d),mu)
    np.testing.assert_allclose(t[0,1],-2*mu*b/r**2)
    dt = np.zeros((3,3,3));dt[0,1,0] = dt[1,0,0] = 4*mu*b/r**3
    np.testing.assert_allclose(cylindrical_stress_divergence(r,t,dt),0.,atol=1e-14)


def test_affine_cartesian_fields_transform_and_constant_stress_has_zero_divergence():
    rng = np.random.default_rng(19)
    for _ in range(12):
        m = rng.normal(size=(3,3)); b = rng.normal(size=3)
        r,phi,z = rng.uniform(.2,2),rng.uniform(-np.pi,np.pi),rng.normal()
        q = cylindrical_basis(phi)
        dq = np.array([[-np.sin(phi),-np.cos(phi),0],[np.cos(phi),-np.sin(phi),0],[0,0,0]])
        xyz = np.array([r*np.cos(phi),r*np.sin(phi),z]);cart = m@xyz+b
        u = q.T@cart
        d = np.column_stack((q.T@m@q[:,0],dq.T@cart+q.T@m@(r*q[:,1]),q.T@m@q[:,2]))
        g = cylindrical_velocity_gradient(r,u,d)
        np.testing.assert_allclose(g,q.T@m@q,atol=3e-14)
        t = newtonian_stress(g,1.7,.8);tcart = newtonian_stress(m,1.7,.8)
        np.testing.assert_allclose(q@t@q.T,tcart,atol=3e-14)
        dt = np.zeros((3,3,3));dt[:,:,1] = dq.T@tcart@q+q.T@tcart@dq
        np.testing.assert_allclose(cylindrical_stress_divergence(r,t,dt),0.,atol=5e-14)


def test_bulk_viscosity_and_nonnegative_dissipation():
    for g in (2*np.eye(3),np.array([[1.,2.,3.],[-1.,0.,4.],[0.,5.,-2.]])):
        mu,zeta = 1.4,.6
        t = newtonian_stress(g,mu,zeta);d = .5*(g+g.T);theta = np.trace(d)
        deviator = d-theta/3*np.eye(3)
        np.testing.assert_allclose(np.sum(t*d),2*mu*np.sum(deviator**2)+zeta*theta**2)
        assert np.sum(t*d)>=0
    np.testing.assert_allclose(newtonian_stress(2*np.eye(3),1.4,.6),3*.6*2*np.eye(3))


def test_coordinate_operators_reject_axis_and_invalid_material():
    with pytest.raises(ValueError):cylindrical_velocity_gradient(0,np.zeros(3),np.zeros((3,3)))
    with pytest.raises(ValueError):newtonian_stress(np.eye(3),-1)
    with pytest.raises(ValueError):cylindrical_stress_divergence(1,np.ones((3,2)),np.zeros((3,3,3)))
