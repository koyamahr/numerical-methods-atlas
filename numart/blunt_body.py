"""Inviscid Mach-6 circular-cylinder forebody on a conforming polygon mesh.

Annular half-domain r in [1,4], theta in [pi/2,3pi/2]. Cartesian conserved
variables and shared normal fluxes give a conservative geometric FV update.
Slip inner wall, fixed free stream outside, extrapolated angular exits.
No viscous wake, full-cylinder drag/Strouhal validation, or exact bow shock.
"""
from dataclasses import dataclass
import numpy as np
from .euler2d import GAMMA, conserved, primitive
from .rotated_flux import normal_flux


def geometry(nr=24, nt=None):
    nt = 2*nr if nt is None else nt
    if not isinstance(nr,int) or not isinstance(nt,int) or nr < 4 or nt < 8 or nt % 2:
        raise ValueError('Require nr>=4 and even nt>=8')
    r = np.linspace(1.,4.,nr+1); theta = np.linspace(np.pi/2,3*np.pi/2,nt+1)
    mid = .5*(theta[:-1]+theta[1:]); dr = np.diff(r); angle = np.pi/nt
    radial = np.stack((np.cos(mid),np.sin(mid)),axis=-1)
    angular = np.stack((-np.sin(theta),np.cos(theta)),axis=-1)
    sr = np.broadcast_to(2*r[:,None]*np.sin(angle/2),(nr+1,nt)).copy()
    st = np.broadcast_to(dr[:,None],(nr,nt+1)).copy()
    volume = np.broadcast_to(.5*(r[1:]**2-r[:-1]**2)[:,None]*np.sin(angle),(nr,nt)).copy()
    vertices = np.stack((r[:,None]*np.cos(theta),r[:,None]*np.sin(theta)),axis=-1)
    return dict(r=r,theta=theta,radial=radial,angular=angular,sr=sr,st=st,volume=volume,vertices=vertices)


def reflect(q,normal):
    result = q.copy(); dot = np.sum(q[...,1:3]*normal,axis=-1)
    result[...,1:3] -= 2*dot[...,None]*normal
    return result


def rhs(q,mesh,far,solver='hlle',wall=True):
    inner = reflect(q[0],mesh['radial']) if wall else q[0]
    g = np.concatenate((inner[None],q,np.broadcast_to(far,q[:1].shape)),axis=0)
    fr = normal_flux(g[:-1],g[1:],mesh['radial'],solver)*mesh['sr'][...,None]
    g = np.concatenate((q[:,:1],q,q[:,-1:]),axis=1)
    ft = normal_flux(g[:,:-1],g[:,1:],mesh['angular'],solver)*mesh['st'][...,None]
    rate = -(fr[1:]-fr[:-1]+ft[:,1:]-ft[:,:-1])/mesh['volume'][...,None]
    outgoing = np.sum(fr[-1]-fr[0],axis=0)+np.sum(ft[:,-1]-ft[:,0],axis=0)
    wall_pressure = np.sum(fr[0,:,1:3]*mesh['radial'],axis=-1)/mesh['sr'][0]
    return rate,outgoing,wall_pressure


def stagnation_pressure(mach=6.):
    pressure = 1+2*GAMMA/(GAMMA+1)*(mach*mach-1)
    downstream_mach2 = (1+.5*(GAMMA-1)*mach*mach)/(GAMMA*mach*mach-.5*(GAMMA-1))
    return pressure*(1+.5*(GAMMA-1)*downstream_mach2)**(GAMMA/(GAMMA-1))


@dataclass
class BluntResult:
    mesh: dict
    q: np.ndarray
    time: float
    steps: int
    rejected_steps: int
    history: np.ndarray
    wall_pressure: np.ndarray
    conservation_residual: np.ndarray


def solve(nr=24,nt=None,solver='hlle',mach=6.,amplitude=1e-4,final_time=1.,cfl=.4):
    if solver not in ('roe','hlle','ausm-plus','ausm-up','rotated') or not np.isfinite(mach) or mach <= 1:
        raise ValueError('Invalid solver or Mach number')
    if not np.isfinite(amplitude) or not 0 <= amplitude < .01 or not np.isfinite(final_time) or final_time < 0 or not np.isfinite(cfl) or not 0 < cfl <= .45:
        raise ValueError('Invalid perturbation/time/CFL')
    mesh = geometry(nr,nt); nr,nt = mesh['volume'].shape
    far = conserved([1.4,mach,0.,1.]); q = np.broadcast_to(far,(nr,nt,4)).copy()
    radius = .5*(mesh['r'][:-1]+mesh['r'][1:]); angle = .5*(mesh['theta'][:-1]+mesh['theta'][1:])
    w = primitive(q)
    w[...,0] *= 1+amplitude*np.exp(-((radius[:,None]-1.5)/.3)**2)*np.sin(12*(angle[None,:]-np.pi))
    q = conserved(w); volume = mesh['volume']; scale = np.maximum(abs(far),1.)
    initial = np.einsum('ij,ijk->k',volume,q); boundary = np.zeros(4)
    t = 0.; steps = rejected = 0; history = []
    def record(rate=0.):
        w = primitive(q); rho = w[...,0]
        symmetry = np.sqrt(np.sum(volume*(rho-rho[:,::-1])**2)/volume.sum())/far[0]
        history.append([t,float(rate),float(symmetry),float(w[...,0].min()),float(w[...,3].min())])
    record()
    while t < final_time:
        w = primitive(q); sound = np.sqrt(GAMMA*w[...,3]/w[...,0]); velocity = w[...,1:3]
        ur = abs(np.sum(velocity*mesh['radial'],axis=-1))
        ut1 = abs(np.sum(velocity*mesh['angular'][:-1],axis=-1)); ut2 = abs(np.sum(velocity*mesh['angular'][1:],axis=-1))
        spectral = (ur+sound)*(mesh['sr'][:-1]+mesh['sr'][1:])+(ut1+sound)*mesh['st'][:,:-1]+(ut2+sound)*mesh['st'][:,1:]
        dt = min(cfl*np.min(volume/spectral),final_time-t)
        first,b0,_ = rhs(q,mesh,far,solver)
        for attempt in range(14):
            try:
                a = q+dt*first; primitive(a)
                second,b1,_ = rhs(a,mesh,far,solver)
                trial = .5*q+.5*(a+dt*second); primitive(trial)
                break
            except ValueError:
                if attempt == 13: raise
                dt *= .5; rejected += 1
        rate = np.sqrt(np.sum(volume[...,None]*((trial-q)/(dt*scale))**2)/volume.sum())
        boundary += .5*dt*(b0+b1); q = trial; t += dt; steps += 1
        if steps % 10 == 0 or t == final_time: record(rate)
    _,_,pressure = rhs(q,mesh,far,solver)
    residual = np.einsum('ij,ijk->k',volume,q)-initial+boundary
    return BluntResult(mesh,q,t,steps,rejected,np.asarray(history),pressure,residual)
