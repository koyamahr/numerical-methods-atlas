"""Periodic 1D first-order hyperbolic diffusion demonstration.

Nishikawa-inspired equivalent steady system, first-order upwind FV and SSPRK2.
This small baseline does not implement the paper's second-order RD schemes.
Pseudo-time is an iteration coordinate, not physical diffusion time.
"""
import numpy as np


def steady_sine(n=64, viscosity=1., relaxation=None, cfl=.5, tolerance=1e-9, maxsteps=100000):
    tr = 1/(8*np.pi**2*viscosity) if relaxation is None else relaxation
    if (n < 8 or not np.isfinite(viscosity) or viscosity <= 0 or not np.isfinite(tr)
            or tr <= 0 or not 0 < cfl <= .5 or tolerance <= 0 or maxsteps < 1):
        raise ValueError('Invalid hyperbolic diffusion controls')
    h = 1/n; x = (np.arange(n)+.5)*h
    speed = np.sqrt(viscosity/tr); dt = cfl/(speed/h+1/tr)
    forcing = viscosity*(2*np.pi)**2*np.sin(2*np.pi*x)
    q = np.zeros((2,n)); history=[]
    def rhs(state):
        physical_flux = np.array([-viscosity*state[1], -state[0]/tr])
        face = .5*(physical_flux+np.roll(physical_flux,-1,axis=1))-.5*speed*(np.roll(state,-1,axis=1)-state)
        rate = -(face-np.roll(face,1,axis=1))/h
        rate[0] += forcing; rate[1] -= state[1]/tr
        return rate
    for k in range(maxsteps+1):
        rate = rhs(q)
        residual = float(np.sqrt(np.mean(rate[0]**2+(rate[1]/(2*np.pi))**2)))
        history.append(residual)
        if residual <= tolerance:
            exact = np.sin(2*np.pi*x)
            return dict(x=x,u=q[0],gradient=q[1],exact=exact,exact_gradient=2*np.pi*np.cos(2*np.pi*x),
                        history=np.array(history),steps=k,dt=dt,relaxation=tr,speed=speed,
                        error=float(np.sqrt(np.mean((q[0]-exact)**2))))
        if not np.isfinite(residual): raise RuntimeError('Nonfinite pseudo-time residual')
        a = q+dt*rate
        q = .5*q+.5*(a+dt*rhs(a))
    raise RuntimeError('Hyperbolic diffusion did not converge')
