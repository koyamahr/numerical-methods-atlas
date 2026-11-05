"""Original cubic-Hermite CIP for 1D constant-speed periodic advection.

Evolves point values and independent point derivatives. No limiter, rational
interpolant, conservative moment, variable-velocity split, or fluid solver.
"""
from dataclasses import dataclass
from typing import Optional
import numpy as np


def hermite(left, right, dleft, dright, width, fraction):
    """Value and physical derivative of the endpoint-constrained cubic."""
    if not np.isfinite(width) or width <= 0:
        raise ValueError('Hermite interval width must be finite and positive')
    s=np.asarray(fraction,dtype=float)
    value=left+(right-left)*(-2*s**3+3*s*s)+width*(dleft*(s**3-2*s*s+s)+dright*(s**3-s*s))
    gradient=(right-left)*(6*s-6*s*s)/width+dleft*(3*s*s-4*s+1)+dright*(3*s*s-2*s)
    return value,gradient


def _state(q,gradient,dx):
    q,g=np.asarray(q,dtype=float),np.asarray(gradient,dtype=float)
    if q.ndim != 1 or len(q)<4 or g.shape != q.shape or not np.all(np.isfinite(q)) or not np.all(np.isfinite(g)):
        raise ValueError('Require compatible finite 1D value and gradient arrays, n>=4')
    if not np.isfinite(dx) or dx<=0:
        raise ValueError('dx must be finite and positive')
    return q,g


def cip_step(q,gradient,dx,dt,speed=1.):
    """Trace x-a*dt into the adjacent upwind interval; require |a dt/dx|<=1."""
    q,g=_state(q,gradient,dx)
    if not np.isfinite(dt) or dt<0 or not np.isfinite(speed):
        raise ValueError('Require finite dt>=0 and finite speed')
    c=speed*dt/dx
    if abs(c)>1+8*np.finfo(float).eps:
        raise ValueError('This adjacent-cell CIP implementation requires |Courant|<=1')
    if c==0:return q.copy(),g.copy()
    c=float(np.clip(c,-1,1))
    if abs(c)==1:return np.roll(q,int(c)),np.roll(g,int(c))
    if c>0:
        return hermite(np.roll(q,1),q,np.roll(g,1),g,dx,1-c)
    return hermite(q,np.roll(q,-1),g,np.roll(g,-1),dx,-c)


def periodic_reconstruction(q,gradient,x,length=1.):
    """Evaluate the periodic piecewise-Hermite field, including between nodes."""
    q,g=_state(q,gradient,1.)
    if not np.isfinite(length) or length<=0:
        raise ValueError('Periodic length must be finite and positive')
    x=np.asarray(x,dtype=float)
    if not np.all(np.isfinite(x)):
        raise ValueError('Sample positions must be finite')
    dx=length/len(q);coordinate=np.mod(x,length)/dx
    index=np.floor(coordinate).astype(int)%len(q);fraction=coordinate-np.floor(coordinate)
    return hermite(q[index],q[(index+1)%len(q)],g[index],g[(index+1)%len(q)],dx,fraction)


def periodic_hermite_mass(q,gradient,dx):
    """Exact integral of the represented periodic cubic field, not quadrature."""
    q,g=_state(q,gradient,dx)
    return float(np.sum(.5*dx*(q+np.roll(q,-1))+dx*dx*(g-np.roll(g,-1))/12))


def initial_profile(x,profile='sine',time=0.,speed=1.):
    """Exact translated point samples; square slopes are zero away from jumps.

    Zero slopes assigned at sampled square-pulse jumps are an initialization
    convention, not the derivative of a discontinuous function there.
    """
    y=np.mod(np.asarray(x)-speed*time,1.)
    if profile=='sine':return 1+.2*np.sin(2*np.pi*y),.4*np.pi*np.cos(2*np.pi*y)
    if profile=='square':return ((y>=.2)&(y<.4)).astype(float),np.zeros_like(y)
    raise ValueError('profile must be sine or square')


@dataclass
class CIPResult:
    x: np.ndarray
    q: np.ndarray
    gradient: Optional[np.ndarray]
    time: float
    steps: int
    history: list


def solve_advection(n=128,profile='sine',method='cip',speed=1.,cfl=.6,final_time=1.,gradient='analytic'):
    if isinstance(n,bool) or not isinstance(n,(int,np.integer)) or n<8:
        raise ValueError('n must be an integer >=8')
    if method not in ('cip','linear') or gradient not in ('analytic','centered'):
        raise ValueError('Unknown CIP/comparison method or initial-gradient convention')
    if not np.isfinite(speed) or not np.isfinite(cfl) or not 0<cfl<=1 or not np.isfinite(final_time) or final_time<0:
        raise ValueError('Require finite speed, 0<CFL<=1, and finite final_time>=0')
    dx=1/n;x=np.arange(n)*dx;q,g=initial_profile(x,profile)
    if gradient=='centered':g=(np.roll(q,-1)-np.roll(q,1))/(2*dx)
    def diagnostic(time):
        return dict(time=float(time),mass=periodic_hermite_mass(q,g,dx) if method=='cip' else float(dx*q.sum()),
                    minimum=float(q.min()),maximum=float(q.max()))
    time,steps=0.,0;history=[diagnostic(0.)]
    while time<final_time and speed!=0:
        dt=min(cfl*dx/abs(speed),final_time-time)
        if method=='cip':q,g=cip_step(q,g,dx,dt,speed)
        else:
            courant=abs(speed)*dt/dx
            q=(1-courant)*q+courant*np.roll(q,1 if speed>0 else -1)
        time+=dt;steps+=1;history.append(diagnostic(time))
    return CIPResult(x,q,g if method=='cip' else None,final_time,steps,history)


def mass_counterexample(n=32,courant=.35):
    """Valid periodic C1 Hermite field q_i=1, g_i=1: remapping changes mass.

    The original field has small subcell ripples, not a uniform function.
    Exact translation preserves its integral. This is a grid-scale diagnostic.
    """
    if isinstance(n,bool) or not isinstance(n,(int,np.integer)) or n<8 or not np.isfinite(courant) or not 0<courant<=1:
        raise ValueError('Require integer n>=8 and 0<Courant<=1')
    q=np.ones(n);g=np.ones(n);dx=1/n;dt=courant*dx
    new,dnew=cip_step(q,g,dx,dt)
    theta=1-courant
    predicted_change=dx*theta*(1-theta)*(1-2*theta)
    return dict(n=n,courant=courant,dt=dt,q=new,gradient=dnew,
                mass_before=periodic_hermite_mass(q,g,dx),mass_after=periodic_hermite_mass(new,dnew,dx),
                analytic_mass_change=predicted_change)
