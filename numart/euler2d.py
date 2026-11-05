"""First-order 2D ideal-gas Euler + HLL, SSPRK2; educational DMR baseline.

Woodward–Colella geometry and moving shock boundary. No PPM, AMR, viscosity,
RANS, or claim to reproduce the paper's fine-scale structures.
"""
from dataclasses import dataclass
import numpy as np
from .snapshots import SnapshotRecorder

GAMMA = 1.4


def conserved(w):
    w=np.asarray(w,dtype=float);rho,u,v,p=np.moveaxis(w,-1,0)
    return np.stack((rho,rho*u,rho*v,p/(GAMMA-1)+.5*rho*(u*u+v*v)),axis=-1)


def primitive(q):
    rho=q[...,0];u=q[...,1]/rho;v=q[...,2]/rho
    p=(GAMMA-1)*(q[...,3]-.5*rho*(u*u+v*v))
    if np.any(rho<=0) or np.any(p<=0) or not np.all(np.isfinite(q)):
        raise ValueError('Nonphysical 2D Euler state')
    return np.stack((rho,u,v,p),axis=-1)


def physical_flux(q,axis):
    w=primitive(q);rho,u,v,p=np.moveaxis(w,-1,0);normal=u if axis==0 else v
    f=q*normal[...,None];f[...,1+axis]+=p;f[...,3]=(q[...,3]+p)*normal
    return f


def hll_flux(left,right,axis):
    wl,wr=primitive(left),primitive(right)
    ul,ur=wl[...,1+axis],wr[...,1+axis]
    cl=np.sqrt(GAMMA*wl[...,3]/wl[...,0]);cr=np.sqrt(GAMMA*wr[...,3]/wr[...,0])
    sl=np.minimum(np.minimum(ul-cl,ur-cr),0);sr=np.maximum(np.maximum(ul+cl,ur+cr),0)
    fl,fr=physical_flux(left,axis),physical_flux(right,axis)
    return (sr[...,None]*fl-sl[...,None]*fr+(sl*sr)[...,None]*(right-left))/(sr-sl)[...,None]


def double_mach_states():
    return conserved([8.,8.25*np.sqrt(3)/2,-4.125,116.5]),conserved([1.4,0.,0.,1.])


def double_mach_initial(nx,ny):
    x=(np.arange(nx)+.5)*4/nx;y=(np.arange(ny)+.5)/ny
    hot,cold=double_mach_states()
    q=np.where((x[:,None]<1/6+y[None,:]/np.sqrt(3))[...,None],hot,cold)
    return x,y,q


def double_mach_ghost(q,time,x):
    g=np.pad(q,((1,1),(1,1),(0,0)),mode='edge')
    hot,cold=double_mach_states();g[0,:,:]=hot
    g[1:-1,0,:]=q[:,0,:];g[1:-1,0,2]*=-1
    g[1:-1,0,:]=np.where((x<1/6)[:,None],hot,g[1:-1,0,:])
    shock=1/6+(1+20*time)/np.sqrt(3)
    g[1:-1,-1,:]=np.where((x<shock)[:,None],hot,cold)
    return g


def _rhs(q,time,x,dx,dy):
    g=double_mach_ghost(q,time,x)
    fx=hll_flux(g[:-1,1:-1],g[1:,1:-1],0)
    fy=hll_flux(g[1:-1,:-1],g[1:-1,1:],1)
    return -(fx[1:]-fx[:-1])/dx-(fy[:,1:]-fy[:,:-1])/dy


@dataclass
class Euler2DResult:
    x: np.ndarray
    y: np.ndarray
    q: np.ndarray
    time: float
    steps: int
    snapshots: object = None


def solve_double_mach(ny=64,final_time=.2,cfl=.4,snapshot_times=None):
    if not isinstance(ny,int) or ny<8 or final_time<0 or not np.isfinite(final_time) or not 0<cfl<=.45:
        raise ValueError('Require ny >= 8, time >= 0, 0 < CFL <= .45')
    recorder=SnapshotRecorder(snapshot_times,final_time)
    nx=4*ny;dx=dy=1/ny
    x,y,q=double_mach_initial(nx,ny);time=0.;steps=0
    recorder.capture(time,steps,q)
    while time<final_time:
        w=primitive(q);sound=np.sqrt(GAMMA*w[...,3]/w[...,0])
        dt=min(cfl/(np.max(abs(w[...,1])+sound)/dx+np.max(abs(w[...,2])+sound)/dy),final_time-time)
        first=q+dt*_rhs(q,time,x,dx,dy)
        q=.5*q+.5*(first+dt*_rhs(first,time+dt,x,dx,dy))
        primitive(q);time+=dt;steps+=1
        recorder.capture(time,steps,q)
    return Euler2DResult(x,y,q,time,steps,recorder.frames)
