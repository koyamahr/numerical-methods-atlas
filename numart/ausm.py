"""AUSM-family baseline: common arithmetic sound speed, cubic pressure split.

Liou--Steffen 1993 is the original bibliographic source. This explicitly
specified variant is cross-checked against FEST-3D's documented AUSM formulas;
not AUSM+, AUSM+-up, SLAU, or a claim to reproduce every original variant.
Independent vectorized implementation; Euler conservative order rho,m...,E.
"""
import numpy as np


def mach_split(m,sign):
    if sign not in (-1,1):raise ValueError('Sign must be +/-1')
    return np.where(abs(m)<1,sign*.25*(m+sign)**2,.5*(m+sign*abs(m)))


def pressure_split(m,sign):
    if sign not in (-1,1):raise ValueError('Sign must be +/-1')
    return np.where(abs(m)<1,.25*(m+sign)**2*(2-sign*m),.5*(1+sign*np.sign(m)))


def flux(left,right,gamma=1.4,axis=0):
    left,right=np.broadcast_arrays(np.asarray(left,dtype=float),np.asarray(right,dtype=float))
    if left.shape[-1] not in (3,4) or axis not in range(left.shape[-1]-2) or gamma<=1:raise ValueError('Invalid Euler flux controls')
    def state(q):
        rho=q[...,0];v=q[...,1:-1]/rho[...,None]
        p=(gamma-1)*(q[...,-1]-.5*rho*np.sum(v*v,axis=-1))
        if not np.all(np.isfinite(q)) or np.any(rho<=0) or np.any(p<=0):raise ValueError('Invalid AUSM state')
        return rho,v,p,np.sqrt(gamma*p/rho),(q[...,-1]+p)/rho
    rl,vl,pl,cl,hl=state(left);rr,vr,pr,cr,hr=state(right)
    sound=.5*(cl+cr);ml=vl[...,axis]/sound;mr=vr[...,axis]/sound
    mach=mach_split(ml,1)+mach_split(mr,-1)
    mass_plus=sound*np.maximum(mach,0)*rl;mass_minus=sound*np.minimum(mach,0)*rr
    result=np.empty_like(left);result[...,0]=mass_plus+mass_minus
    result[...,1:-1]=mass_plus[...,None]*vl+mass_minus[...,None]*vr
    result[...,1+axis]+=pl*pressure_split(ml,1)+pr*pressure_split(mr,-1)
    result[...,-1]=mass_plus*hl+mass_minus*hr
    return result
