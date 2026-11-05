"""Cylindrical physical components, r > 0, in the orthonormal (er,ephi,ez) basis.

Partial derivatives are with respect to coordinate values (r,phi,z), not arc
length. These are local tensor operations, not a cylindrical Navier–Stokes solver.
"""
import numpy as np


def cylindrical_velocity_gradient(radius, velocity, partials):
    """L[i,j] = e_i dot directional_derivative(e_j, u).

    velocity[...,i], partials[...,i,j] = partial_j velocity_i.
    """
    r = np.asarray(radius, dtype=float)
    u, d = np.asarray(velocity, dtype=float), np.asarray(partials, dtype=float)
    if np.any(r <= 0) or not np.all(np.isfinite(r)):
        raise ValueError('Use r > 0; axis limits need a separate regularity treatment')
    if u.shape[-1:] != (3,) or d.shape != u.shape[:-1]+(3,3):
        raise ValueError('Require velocity (...,3) and partials (...,3,3)')
    if not np.all(np.isfinite(u)) or not np.all(np.isfinite(d)):
        raise ValueError('Velocity and derivatives must be finite')
    result = d.copy()
    result[...,0,1] = (d[...,0,1]-u[...,1])/r
    result[...,1,1] = (d[...,1,1]+u[...,0])/r
    result[...,2,1] = d[...,2,1]/r
    return result


def newtonian_stress(gradient, viscosity=1., bulk_viscosity=0.):
    """3D isotropic viscous stress: tau=2mu D+(zeta-2mu/3) div(u) I.

    Returns viscous stress only; total Cauchy stress is -p I + tau.
    """
    g = np.asarray(gradient, dtype=float)
    mu, zeta = np.asarray(viscosity), np.asarray(bulk_viscosity)
    if g.shape[-2:] != (3,3) or not np.all(np.isfinite(g)):
        raise ValueError('Require finite (...,3,3) velocity gradient')
    if np.any(mu < 0) or np.any(zeta < 0) or not np.all(np.isfinite(mu)) or not np.all(np.isfinite(zeta)):
        raise ValueError('Shear and bulk viscosities must be finite and nonnegative')
    theta = np.trace(g, axis1=-2, axis2=-1)
    return mu[...,None,None]*(g+np.swapaxes(g,-1,-2))+(zeta-2*mu/3)[...,None,None]*theta[...,None,None]*np.eye(3)


def cylindrical_stress_divergence(radius, stress, partials):
    """div(tau) for symmetric physical stress; partials[...,i,j,k]=partial_k tau_ij."""
    r = np.asarray(radius, dtype=float)
    t, d = np.asarray(stress, dtype=float), np.asarray(partials, dtype=float)
    if np.any(r <= 0) or not np.all(np.isfinite(r)):
        raise ValueError('Use r > 0; handle the symmetry axis by limits')
    if t.shape[-2:] != (3,3) or d.shape != t.shape[:-2]+(3,3,3):
        raise ValueError('Require stress (...,3,3) and partials (...,3,3,3)')
    if not np.all(np.isfinite(t)) or not np.all(np.isfinite(d)) or not np.allclose(t,np.swapaxes(t,-1,-2)):
        raise ValueError('Require finite symmetric stress and finite derivatives')
    out = d[..., :,0,0]+d[..., :,1,1]/r[...,None]+d[..., :,2,2]
    out[...,0] += (t[...,0,0]-t[...,1,1])/r
    out[...,1] += 2*t[...,0,1]/r
    out[...,2] += t[...,2,0]/r
    return out


def cylindrical_basis(angle):
    """Columns are the cylindrical unit vectors expressed in Cartesian components."""
    phi = np.asarray(angle, dtype=float)
    q = np.zeros(phi.shape+(3,3))
    q[...,0,0], q[...,1,0] = np.cos(phi), np.sin(phi)
    q[...,0,1], q[...,1,1] = -np.sin(phi), np.cos(phi)
    q[...,2,2] = 1.
    return q
