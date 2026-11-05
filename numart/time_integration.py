"""Time integrators for the scalar linear test equation y'=rate*y.

This is an ODE laboratory, separate from space discretization and PDE CFL.
Leapfrog is the two-step first-order-system recurrence, with RK4 startup.
"""
import cmath
import numpy as np
from .runge_kutta import EXPLICIT_METHODS, stability_function

METHODS = ('forward-euler','backward-euler','heun','explicit-midpoint','ralston',
           'kutta3','ssprk3','ssprk43','rk4','ssprk54','midpoint','leapfrog')


def stability_factor(z, method):
    if method == 'forward-euler': return 1+z
    if method == 'backward-euler': return 1/(1-z)
    if method == 'heun': return 1+z+z*z/2
    if method == 'ssprk3': return 1+z+z*z/2+z**3/6
    if method == 'rk4': return 1+z+z*z/2+z**3/6+z**4/24
    if method in EXPLICIT_METHODS: return stability_function(z,method)
    if method == 'midpoint': return (1+z/2)/(1-z/2)
    raise ValueError('Use a one-step method; leapfrog has two amplification roots')


def leapfrog_roots(z):
    root = cmath.sqrt(1+z*z)
    return z+root,z-root


def linear_trajectory(rate=1j, dt=.1, steps=200, method='rk4', startup_perturbation=0.):
    if method not in METHODS or not isinstance(steps,int) or steps < 0 or steps > 10000:
        raise ValueError('Unknown method or invalid step count')
    if dt <= 0 or not np.isfinite(dt) or not np.isfinite(rate) or not np.isfinite(startup_perturbation):
        raise ValueError('Require finite parameters and dt > 0')
    z = complex(rate)*dt
    values = np.ones(steps+1,dtype=complex)
    if method == 'leapfrog' and steps:
        values[1] = stability_factor(z,'rk4')+startup_perturbation
        for k in range(1,steps):values[k+1] = values[k-1]+2*z*values[k]
    elif method != 'leapfrog':
        factor = stability_factor(z,method)
        for k in range(steps):values[k+1] = factor*values[k]
    return np.arange(steps+1)*dt,values
