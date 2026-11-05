"""Second-order Cartesian KEEP flux, Kuya–Totani–Kawai (2018) baseline.

The two-point flux follows Eq. (9) of Kuya & Kawai, ICCFD11 paper 0401 (2022).
Original arithmetic-mean internal energy; no 2021 PEP/2022 redefinition,
shock sensor, upwind dissipation, positivity limiter, or curvilinear metrics.
Periodic 2D ideal-gas Euler, gamma=1.4, with classical RK4 time integration.
Kinetic-energy consistency is semidiscrete; entropy is not exact to roundoff.
"""
from dataclasses import dataclass
import numpy as np
from .euler2d import GAMMA,conserved,primitive
from .snapshots import SnapshotRecorder


def keep_flux(left,right,axis):
    if axis not in (0,1):raise ValueError('Use axis 0 or 1')
    wl,wr=primitive(left),primitive(right)
    rho=.5*(wl[...,0]+wr[...,0]);velocity=.5*(wl[...,1:3]+wr[...,1:3])
    mass=rho*velocity[...,axis]
    specific_internal=.5*(wl[...,3]/wl[...,0]+wr[...,3]/wr[...,0])/(GAMMA-1)
    kinetic=.5*np.sum(wl[...,1:3]*wr[...,1:3],axis=-1)
    pressure_diffusion=.5*(wl[...,1+axis]*wr[...,3]+wr[...,1+axis]*wl[...,3])
    flux=np.empty_like(np.asarray(left,dtype=float));flux[...,0]=mass
    flux[...,1:3]=mass[...,None]*velocity
    flux[...,1+axis]+=.5*(wl[...,3]+wr[...,3])
    flux[...,3]=mass*(kinetic+specific_internal)+pressure_diffusion
    return flux


def rhs(q,length=20.):
    if q.ndim!=3 or q.shape[0]!=q.shape[1] or q.shape[-1]!=4 or length<=0:
        raise ValueError('Require square 2D Euler grid and positive length')
    derivative=np.zeros_like(q);inverse_dx=q.shape[0]/length
    for axis in (0,1):
        flux=keep_flux(q,np.roll(q,-1,axis=axis),axis)
        derivative-=inverse_dx*(flux-np.roll(flux,1,axis=axis))
    return derivative


def vortex_state(x,y,time=0.,length=20.,beta=3.,velocity=(1.,.5)):
    """Whole-plane isentropic vortex, translated on a large periodic square.

    Minimum-image coordinates; L=20 leaves boundary tails below roundoff for
    beta=3. This is an analytic reference, not a generic compact periodic vortex.
    """
    if length<=0 or beta<0 or not np.all(np.isfinite([time,length,beta,*velocity])):
        raise ValueError('Require finite vortex parameters')
    dx=(np.asarray(x)-velocity[0]*time+length/2)%length-length/2
    dy=(np.asarray(y)-velocity[1]*time+length/2)%length-length/2
    radius2=dx*dx+dy*dy;rotation=beta/(2*np.pi)*np.exp(.5*(1-radius2))
    temperature=1-(GAMMA-1)*beta*beta/(8*GAMMA*np.pi**2)*np.exp(1-radius2)
    if np.any(temperature<=0):raise ValueError('Vortex temperature is nonpositive')
    rho=temperature**(1/(GAMMA-1));pressure=rho**GAMMA
    return conserved(np.stack(np.broadcast_arrays(rho,velocity[0]-rotation*dy,
                                                 velocity[1]+rotation*dx,pressure),axis=-1))


def diagnostics(q,length=20.):
    w=primitive(q);rho,u,v,p=np.moveaxis(w,-1,0);dv=(length/q.shape[0])**2
    return {'mass':float(q[...,0].sum()*dv),'momentum_x':float(q[...,1].sum()*dv),
            'momentum_y':float(q[...,2].sum()*dv),'total_energy':float(q[...,3].sum()*dv),
            'kinetic_energy':float((.5*rho*(u*u+v*v)).sum()*dv),
            'entropy_proxy':float((rho*np.log(p/rho**GAMMA)).sum()*dv),
            'min_density':float(rho.min()),'min_pressure':float(p.min())}


@dataclass
class KEEPResult:
    q: np.ndarray
    time: float
    steps: int
    history: list
    snapshots: list
    density_l1: float


def solve_vortex(n=96,final_time=1.,cfl=.25,length=20.,snapshot_times=None):
    if (not isinstance(n,int) or n<16 or not np.all(np.isfinite([final_time,cfl,length]))
            or final_time<0 or not 0<cfl<=.5 or length!=20.):
        raise ValueError('Require n>=16, time>=0, 0<CFL<=.5, L=20 for the tested vortex')
    coordinate=(np.arange(n)+.5)*length/n-length/2
    x,y=np.meshgrid(coordinate,coordinate,indexing='ij');q=vortex_state(x,y)
    recorder=SnapshotRecorder(snapshot_times,final_time);t=0.;steps=0;history=[]
    def record():
        d={'time':t,**diagnostics(q,length)};history.append(d);recorder.capture(t,steps,q,d)
    record()
    while t<final_time:
        w=primitive(q);sound=np.sqrt(GAMMA*w[...,3]/w[...,0])
        dt=min(cfl/((np.max(abs(w[...,1])+sound)+np.max(abs(w[...,2])+sound))*n/length),final_time-t)
        k1=rhs(q,length);k2=rhs(q+.5*dt*k1,length)
        k3=rhs(q+.5*dt*k2,length);k4=rhs(q+dt*k3,length)
        q=q+dt/6*(k1+2*k2+2*k3+k4);primitive(q)
        t+=dt;steps+=1;record()
    exact=vortex_state(x,y,t)
    return KEEPResult(q,t,steps,history,recorder.frames,float(np.mean(abs(q[...,0]-exact[...,0]))))
