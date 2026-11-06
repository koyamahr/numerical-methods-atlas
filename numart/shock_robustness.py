"""Controlled grid-aligned shock diagnostic; independent of legacy exhibits.

2D Euler Roe (optional acoustic entropy smoothing), Davis HLL, Einfeldt-type
HLLE, and an explicitly labeled pressure-sensor Roe/HLLE blend. First-order
space / SSPRK2, Cartesian grids. Not the original Quirk perturbed-grid duct,
not a blunt-body test, and not a rotated-hybrid Riemann solver.
"""
from dataclasses import dataclass
import numpy as np
from .euler2d import GAMMA,conserved,primitive,physical_flux
from .ausm import flux as ausm_flux


def roe_basis(left,right,axis=0):
    wl,wr=primitive(left),primitive(right)
    a,b=np.sqrt(wl[...,0]),np.sqrt(wr[...,0]);den=a+b
    velocity=(a[...,None]*wl[...,1:3]+b[...,None]*wr[...,1:3])/den[...,None]
    h=(a*(left[...,3]+wl[...,3])/wl[...,0]+b*(right[...,3]+wr[...,3])/wr[...,0])/den
    speed=np.sqrt((GAMMA-1)*(h-.5*np.sum(velocity**2,axis=-1)))
    normal=velocity[...,axis];tangent=velocity[...,1-axis];one=np.ones_like(normal);zero=np.zeros_like(normal)
    r=np.stack((np.stack((one,normal-speed,tangent,h-normal*speed),axis=-1),
                np.stack((one,normal,tangent,.5*np.sum(velocity**2,axis=-1)),axis=-1),
                np.stack((zero,zero,one,tangent),axis=-1),
                np.stack((one,normal+speed,tangent,h+normal*speed),axis=-1)),axis=-1)
    # Momentum permutation to global Cartesian components.
    if axis==1:r=r[...,[0,2,1,3],:]
    eigenvalues=np.stack((normal-speed,normal,normal,normal+speed),axis=-1)
    return r,eigenvalues,velocity,h,speed


def flux(left,right,axis=0,solver='roe',entropy_fraction=.1,blend=None):
    if solver not in ('roe','hll','hlle','hybrid','ausm') or axis not in (0,1):raise ValueError('Invalid flux controls')
    if solver=='ausm':return ausm_flux(left,right,GAMMA,axis)
    wl,wr=primitive(left),primitive(right);fl,fr=physical_flux(left,axis),physical_flux(right,axis)
    r,eigenvalues,velocity,h,c=roe_basis(left,right,axis)
    ul,ur=wl[...,1+axis],wr[...,1+axis]
    cl=np.sqrt(GAMMA*wl[...,3]/wl[...,0]);cr=np.sqrt(GAMMA*wr[...,3]/wr[...,0])
    sl=np.minimum(ul-cl,eigenvalues[...,0]);sr=np.maximum(ur+cr,eigenvalues[...,3])
    if solver=='hll':sl=np.minimum(ul-cl,ur-cr);sr=np.maximum(ul+cl,ur+cr)
    sl=np.minimum(sl,0.);sr=np.maximum(sr,0.)
    hlle=(sr[...,None]*fl-sl[...,None]*fr+(sl*sr)[...,None]*(right-left))/(sr-sl)[...,None]
    if solver in ('hll','hlle'):return hlle
    jump=right-left;dr=jump[...,0]
    dp=(GAMMA-1)*(jump[...,3]-np.sum(velocity*jump[...,1:3],axis=-1)+.5*np.sum(velocity**2,axis=-1)*dr)
    dnormal=jump[...,1+axis]-velocity[...,axis]*dr
    dtangent=jump[...,2-axis]-velocity[...,1-axis]*dr
    strengths=np.stack(((dp-c*dnormal)/(2*c*c),dr-dp/(c*c),dtangent,(dp+c*dnormal)/(2*c*c)),axis=-1)
    speeds=abs(eigenvalues);delta=entropy_fraction*c
    if entropy_fraction:
        if not np.isfinite(entropy_fraction) or entropy_fraction<0:raise ValueError('Invalid entropy fraction')
        for k in (0,3):speeds[...,k]=np.where(speeds[...,k]<delta,.5*(speeds[...,k]**2/delta+delta),speeds[...,k])
    result=.5*(fl+fr-np.einsum('...ij,...j->...i',r,strengths*speeds))
    if solver=='hybrid':
        if blend is None or np.any((blend<0)|(blend>1)):raise ValueError('Hybrid requires face blend in [0,1]')
        result=(1-blend[...,None])*result+blend[...,None]*hlle
    return result


def shock_states(mach=6.):
    if not np.isfinite(mach) or mach<=1:raise ValueError('Require Mach>1')
    rho,p=1.4,1.;speed=mach # upstream sound speed is one
    compression=(GAMMA+1)*mach**2/(2+(GAMMA-1)*mach**2)
    pressure=1+2*GAMMA/(GAMMA+1)*(mach**2-1)
    return conserved([rho,speed,0.,p]),conserved([rho*compression,speed/compression,0.,p*pressure])


def initial_shock(n=64,phase=0.,amplitude=1e-4,mach=6.):
    if not isinstance(n,int) or n<16 or n%4 or not 0<=phase<1 or not 0<=amplitude<.1:raise ValueError('Invalid shock grid/perturbation')
    ny=n//4;dx=dy=1/n;x=(np.arange(n)+.5)*dx;y=(np.arange(ny)+.5)*dy
    left,right=shock_states(mach);location=.5+phase*dx
    # Integrate a row-shifted discontinuity exactly in x; each row's shock
    # moves by +/- amplitude*dx. This seeds the Nyquist transverse mode.
    shock=location+amplitude*dx*(-1.)**np.arange(ny)
    upstream=np.clip((shock[None,:]-(x[:,None]-.5*dx))/dx,0,1)
    q=upstream[...,None]*left+(1-upstream[...,None])*right
    return x,y,q,left,right,dx,dy,location


def pressure_sensor(q):
    p=primitive(q)[...,3];s=np.zeros_like(p)
    for axis in (0,1):
        for shift in (-1,1):
            neighbor=np.roll(p,shift,axis=axis)
            if axis==0:neighbor[0 if shift==1 else -1]=p[0 if shift==1 else -1]
            s=np.maximum(s,abs(neighbor-p)/np.minimum(neighbor,p))
    # Broadens shock detection to neighboring transverse faces; a contact
    # at constant pressure has sensor zero. Explicit educational thresholds.
    return np.clip((s-.05)/.2,0,1)


def rhs(q,left,right,dx,dy,solver,entropy_fraction):
    g=np.pad(q,((1,1),(1,1),(0,0)),mode='wrap');g[0]=left;g[-1]=right
    blendx=blendy=None
    if solver=='hybrid':
        sensor=pressure_sensor(q);s=np.pad(sensor,((1,1),(1,1)),mode='wrap');s[0]=s[1];s[-1]=s[-2]
        blendx=np.maximum(s[:-1,1:-1],s[1:,1:-1]);blendy=np.maximum(s[1:-1,:-1],s[1:-1,1:])
    fx=flux(g[:-1,1:-1],g[1:,1:-1],0,solver,entropy_fraction,blendx)
    fy=flux(g[1:-1,:-1],g[1:-1,1:],1,solver,entropy_fraction,blendy)
    return -(fx[1:]-fx[:-1])/dx-(fy[:,1:]-fy[:,:-1])/dy


@dataclass
class ShockResult:
    x: np.ndarray
    y: np.ndarray
    q: np.ndarray
    history: np.ndarray
    time: float
    steps: int
    retried_steps: int
    location: float


def solve_shock(n=64,solver='roe',entropy_fraction=.1,phase=0.,amplitude=1e-4,mach=6.,final_time=.5,cfl=.3):
    if solver not in ('roe','hll','hlle','hybrid','ausm') or not 0<cfl<=.4 or final_time<0 or not np.isfinite(final_time):raise ValueError('Invalid shock controls')
    if entropy_fraction<0 or not np.isfinite(entropy_fraction):raise ValueError('Invalid entropy smoothing')
    x,y,q,left,right,dx,dy,location=initial_shock(n,phase,amplitude,mach)
    history=[];t=0.;steps=retries=0
    band=abs(x-location)<.1
    def record():
        w=primitive(q);density=w[...,0];average=density.mean(axis=1)
        alt=np.mean((density-average[:,None])*(-1.)**np.arange(len(y))[None,:],axis=1)
        # Shock position for each row via an integrated mass-deficit estimate.
        position=dx*np.sum((right[0]-density)/(right[0]-left[0]),axis=0)
        history.append((t,float(np.max(abs(alt[band]))),float(np.max(abs(w[band,:,2]))),
                        float(np.ptp(position)),float(w[...,0].min()),float(w[...,3].min())))
    record()
    while t<final_time:
        w=primitive(q);c=np.sqrt(GAMMA*w[...,3]/w[...,0])
        dt=min(cfl/(np.max(abs(w[...,1])+c)/dx+np.max(abs(w[...,2])+c)/dy),final_time-t)
        for attempt in range(13):
            try:
                a=q+dt*rhs(q,left,right,dx,dy,solver,entropy_fraction);primitive(a)
                trial=.5*q+.5*(a+dt*rhs(a,left,right,dx,dy,solver,entropy_fraction));primitive(trial);break
            except ValueError:
                if attempt==12:raise
                retries+=1;dt*=.5
        q=trial;t+=dt;steps+=1;record()
    return ShockResult(x,y,q,np.asarray(history),t,steps,retries,location)
