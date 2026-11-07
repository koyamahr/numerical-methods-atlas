"""Specified AUSM+ / AUSM+-up fluxes for ideal-gas Euler.

Independent implementation of Liou's M4/P5 splitting and the directional
critical-sound-speed interface used in the 2006 formulation. Defaults for up:
Kp=.25, Ku=.75, sigma=1, reference Mach cutoff=.1. No implicit preconditioning.
The older common-arithmetic-sound-speed AUSM implementation stays separate.
"""
import numpy as np


def mach4(m, sign):
    if sign not in (-1, 1): raise ValueError('Require sign +/-1')
    m = np.asarray(m)
    return np.where(abs(m) < 1, sign*(.25*(m+sign)**2+.125*(m*m-1)**2), .5*(m+sign*abs(m)))


def pressure5(m, sign, alpha=3/16):
    if sign not in (-1, 1): raise ValueError('Require sign +/-1')
    m = np.asarray(m)
    return np.where(abs(m) < 1, .25*(m+sign)**2*(2-sign*m)+sign*alpha*m*(m*m-1)**2,
                    .5*(1+sign*np.sign(m)))


def flux(left, right, gamma=1.4, axis=0, variant='up', mach_cutoff=.1, kp=.25, ku=.75):
    if variant not in ('plus', 'up') or not np.isfinite(gamma) or gamma <= 1:
        raise ValueError('Require plus/up and gamma>1')
    if not np.isfinite(mach_cutoff) or not 0 < mach_cutoff <= 1 or not all(np.isfinite(v) and 0 <= v <= 1 for v in (kp, ku)):
        raise ValueError('Require 0<reference Mach<=1 and diffusion coefficients in [0,1]')
    left, right = np.broadcast_arrays(np.asarray(left, float), np.asarray(right, float))
    if left.ndim == 0 or left.shape[-1] not in (3, 4) or axis not in range(left.shape[-1]-2):
        raise ValueError('Invalid Euler state shape or axis')
    def state(q):
        rho = q[..., 0]
        if not np.all(np.isfinite(q)) or np.any(rho <= 0): raise ValueError('Invalid density/state')
        velocity = q[..., 1:-1]/rho[..., None]
        pressure = (gamma-1)*(q[..., -1]-.5*rho*np.sum(velocity**2, axis=-1))
        if np.any(pressure <= 0): raise ValueError('Invalid pressure')
        enthalpy = (q[..., -1]+pressure)/rho
        return rho, velocity, pressure, enthalpy
    rl, vl, pl, hl = state(left); rr, vr, pr, hr = state(right)
    al = np.sqrt(2*(gamma-1)/(gamma+1)*hl); ar = np.sqrt(2*(gamma-1)/(gamma+1)*hr)
    sound = np.minimum(al*al/np.maximum(al, vl[..., axis]), ar*ar/np.maximum(ar, -vr[..., axis]))
    ml, mr = vl[..., axis]/sound, vr[..., axis]/sound
    mean_mach2 = .5*(ml*ml+mr*mr)
    if variant == 'up':
        m0 = np.sqrt(np.minimum(1, np.maximum(mean_mach2, mach_cutoff**2)))
        fa = m0*(2-m0)
        alpha = 3/16*(5*fa*fa-4)
    else:
        fa, alpha = 1., 3/16
    pp, pm = pressure5(ml, 1, alpha), pressure5(mr, -1, alpha)
    mach = mach4(ml, 1)+mach4(mr, -1)
    pressure = pp*pl+pm*pr
    if variant == 'up':
        rho = .5*(rl+rr)
        mach -= kp/fa*np.maximum(1-mean_mach2, 0)*(pr-pl)/(rho*sound*sound)
        pressure -= ku*fa*pp*pm*(rl+rr)*sound*(vr[..., axis]-vl[..., axis])
    mass = sound*(np.maximum(mach, 0)*rl+np.minimum(mach, 0)*rr)
    velocity = np.where((mass >= 0)[..., None], vl, vr)
    result = np.empty_like(left); result[..., 0] = mass
    result[..., 1:-1] = mass[..., None]*velocity
    result[..., 1+axis] += pressure
    result[..., -1] = mass*np.where(mass >= 0, hl, hr)
    return result
