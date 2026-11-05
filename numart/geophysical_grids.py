"""A/B/C linear rotating shallow-water Fourier symbols on a square grid.

Periodic f-plane, centered second-order pressure/divergence operators; C-grid
Coriolis uses the symmetric four-point average. Variables (u,v,c*eta/H)
have their physical staggering phases removed and share an energy norm.
These are semi-discrete symbols, not a nonlinear geophysical time integrator.
"""
import numpy as np


def effective_wavenumbers(grid, k, ell, h=1., coriolis=1.):
    if grid not in ('A','B','C') or not np.isfinite(h) or h <= 0:
        raise ValueError('Choose A/B/C and a finite positive square spacing')
    if not np.all(np.isfinite([k,ell,coriolis])):
        raise ValueError('Finite wavenumbers and Coriolis parameter required')
    if grid == 'A':
        return np.sin(k*h)/h, np.sin(ell*h)/h, coriolis
    if grid == 'B':
        return (2*np.sin(k*h/2)*np.cos(ell*h/2)/h,
                2*np.cos(k*h/2)*np.sin(ell*h/2)/h, coriolis)
    return (2*np.sin(k*h/2)/h,2*np.sin(ell*h/2)/h,
            coriolis*np.cos(k*h/2)*np.cos(ell*h/2))


def symbol(grid, k, ell, h=1., wave_speed=1., coriolis=1.):
    if not np.isfinite(wave_speed) or wave_speed <= 0:
        raise ValueError('Positive finite gravity wave speed required')
    dx,dy,rotation=effective_wavenumbers(grid,k,ell,h,coriolis)
    cx,cy=wave_speed*dx,wave_speed*dy
    return np.array([[0.,rotation,-1j*cx],[-rotation,0.,-1j*cy],[-1j*cx,-1j*cy,0.]],dtype=complex)


def gravity_frequency(grid,k,ell,h=1.,wave_speed=1.,coriolis=1.):
    """Positive oscillatory frequency; the third branch is geostrophic zero."""
    matrix=symbol(grid,k,ell,h,wave_speed,coriolis)
    return float(np.sqrt(np.sum(abs(matrix)**2)/2))
