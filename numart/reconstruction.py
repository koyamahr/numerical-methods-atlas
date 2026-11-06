"""Educational PPM/MUSCL finite volumes and characteristic FD WENO-JS/Z.

The PPM path is a method-of-lines limited parabolic reconstruction, not the
complete original traced/flattened/contact-steepened Colella--Woodward scheme.
Legacy solvers remain unchanged so their published provenance stays valid.
"""
from dataclasses import dataclass
import numpy as np
from numpy.polynomial.legendre import leggauss
from .benchmarks import Problem, get_problem
from .equations import Euler
from .limiters import limited_slope, positive_reconstruction
from .riemann import numerical_flux
from .ausm import flux as ausm_flux

METHODS=('muscl','ppm','weno-js','weno-z')


def euler_eigenbasis(qleft,qright=None,gamma=1.4):
    """Conservative right/left eigenvectors at a local or Roe-averaged state."""
    eq=Euler(gamma);left=np.asarray(qleft);wl=eq.primitive(left)
    if qright is None:
        u=wl[...,1];enthalpy=(left[...,2]+wl[...,2])/wl[...,0]
    else:
        right=np.asarray(qright);wr=eq.primitive(right)
        al,ar=np.sqrt(wl[...,0]),np.sqrt(wr[...,0]);den=al+ar
        u=(al*wl[...,1]+ar*wr[...,1])/den
        enthalpy=(al*(left[...,2]+wl[...,2])/wl[...,0]+ar*(right[...,2]+wr[...,2])/wr[...,0])/den
    c2=(gamma-1)*(enthalpy-.5*u*u)
    if np.any(c2<=0):raise ValueError('Invalid characteristic sound speed')
    c=np.sqrt(c2);one=np.ones_like(u)
    r=np.stack((np.stack((one,u-c,enthalpy-u*c),axis=-1),
                np.stack((one,u,.5*u*u),axis=-1),
                np.stack((one,u+c,enthalpy+u*c),axis=-1)),axis=-1)
    return r,np.linalg.inv(r)


def ppm_edges(stencil):
    """Monotone parabolic edges from five cell averages on axis -2."""
    a,b,c,d,e=np.moveaxis(np.asarray(stencil),-2,0)
    dm=limited_slope(b-a,c-b,'mc');dc=limited_slope(c-b,d-c,'mc');dp=limited_slope(d-c,e-d,'mc')
    left=.5*(b+c)-(dc-dm)/6;right=.5*(c+d)-(dp-dc)/6
    left=np.maximum(np.minimum(left,np.maximum(b,c)),np.minimum(b,c))
    right=np.maximum(np.minimum(right,np.maximum(c,d)),np.minimum(c,d))
    extremum=(right-c)*(c-left)<=0
    left=np.where(extremum,c,left);right=np.where(extremum,c,right)
    delta=right-left;six=6*c-3*(left+right)
    fix_left=delta*six>delta*delta;fix_right=delta*six < -delta*delta
    new_left=np.where(fix_left,3*c-2*right,left)
    new_right=np.where(fix_right,3*c-2*left,right)
    return new_left,new_right


def weno_left(stencil,variant='js',epsilon=1e-6):
    """FD flux reconstruction from a five-point stencil; WENO-Z exponent 2."""
    if variant not in ('js','z') or not np.isfinite(epsilon) or epsilon<=0:
        raise ValueError('Require js/z weights and finite epsilon>0')
    a,b,c,d,e=np.moveaxis(np.asarray(stencil),-2,0)
    candidates=np.stack(((2*a-7*b+11*c)/6,(-b+5*c+2*d)/6,(2*c+5*d-e)/6))
    beta=np.stack((13/12*(a-2*b+c)**2+.25*(a-4*b+3*c)**2,
                   13/12*(b-2*c+d)**2+.25*(b-d)**2,
                   13/12*(c-2*d+e)**2+.25*(3*c-4*d+e)**2))
    linear=np.array([.1,.6,.3]).reshape((3,)+(1,)*(beta.ndim-1))
    alpha=linear/(epsilon+beta)**2 if variant=='js' else linear*(1+(abs(beta[0]-beta[2])/(epsilon+beta))**2)
    weights=alpha/alpha.sum(axis=0)
    return np.sum(weights*candidates,axis=0)


def _pad(q,problem,width=3):
    g=np.pad(q,((width,width),(0,0)),mode='wrap' if problem.boundary=='periodic' else 'edge')
    if problem.boundary=='fixed':
        g[:width]=problem.initial(np.array([problem.domain[0]]))[0]
        g[-width:]=problem.initial(np.array([problem.domain[1]]))[0]
    return g


def finite_volume_edges(q,problem,method='ppm',basis='characteristic'):
    """Return both edges for each cell, including one ghost cell per end.

    Conservative local characteristic basis; a common affine limiter on
    left/midpoint/right quadrature states repairs inadmissible reconstruction
    only. This is not a fully discrete positivity theorem.
    """
    g=_pad(q,problem);center=g[2:-2];count=len(center)
    stencil=np.stack([g[k:k+count] for k in range(5)],axis=1)-center[:,None,:]
    r=None
    if basis=='characteristic':
        r,l=euler_eigenbasis(center,gamma=problem.equation.gamma)
        stencil=np.einsum('nij,nkj->nki',l,stencil)
    elif basis!='component':raise ValueError('Unknown reconstruction basis')
    if method=='ppm':left,right=ppm_edges(stencil)
    elif method=='muscl':
        slope=limited_slope(-stencil[:,1],stencil[:,3],'mc');left,right=-.5*slope,.5*slope
    else:raise ValueError('Finite-volume reconstruction must be ppm or muscl')
    if r is not None:
        left=np.einsum('nij,nj->ni',r,left);right=np.einsum('nij,nj->ni',r,right)
    left,right=center+left,center+right
    midpoint=1.5*center-.25*(left+right)
    nodes=np.stack((left,midpoint,right),axis=1)
    density=nodes[...,0];safe=np.maximum(density,1e-300)
    pressure=(problem.equation.gamma-1)*(nodes[...,2]-.5*nodes[...,1]**2/safe)
    bad=np.any((density<=1e-12)|(pressure<=1e-12),axis=1)
    for i in np.flatnonzero(bad):
        scaled,_=positive_reconstruction(center[i],nodes[i],gamma=problem.equation.gamma)
        left[i],right[i]=scaled[0],scaled[2]
    return left,right,int(bad.sum())


def weno_flux(q,problem,variant='z',basis='characteristic',epsilon=1e-6):
    """Global LF split, face-frozen Roe characteristics, pointwise FD fluxes."""
    g=_pad(q,problem);eq=problem.equation;physical=eq.flux(g)
    sm,sp=eq.speeds(g);speed=np.max(np.maximum(abs(sm),abs(sp)))
    plus=.5*(physical+speed*g);minus=.5*(physical-speed*g)
    indices=np.arange(len(q)+1)[:,None]+np.arange(5)[None,:]
    fp,fm=plus[indices],minus[indices[:,::-1]+1]
    r=None
    if basis=='characteristic':
        r,l=euler_eigenbasis(g[2:-3],g[3:-2],eq.gamma)
        fp=np.einsum('nij,nkj->nki',l,fp);fm=np.einsum('nij,nkj->nki',l,fm)
    elif basis!='component':raise ValueError('Unknown reconstruction basis')
    flux=weno_left(fp,variant,epsilon)+weno_left(fm,variant,epsilon)
    return np.einsum('nij,nj->ni',r,flux) if r is not None else flux


def averaged_state(problem,x,dx,time=None,quadrature=8):
    """Gauss-integrated conservative cell means; state input is not mutated."""
    z,w=leggauss(quadrature);points=x[:,None]+.5*dx*z
    values=problem.initial(points) if time is None else problem.reference(points,time)
    return .5*np.einsum('q,nqk->nk',w,values)


def contact_problem():
    eq=Euler()
    def reference(x,t):
        density=np.where(np.mod(x-t,1)<.5,1.,2.)
        return eq.conserved(np.stack((density,np.ones_like(x),np.ones_like(x)),axis=-1))
    return Problem('moving-contact',eq,(0.,1.),1.,'periodic',lambda x:reference(x,0),reference)


@dataclass
class HighOrderResult:
    x: np.ndarray
    q: np.ndarray
    time: float
    steps: int
    rejected_steps: int
    scaled_reconstructions: int
    representation: str


def solve_euler(problem,n=200,method='ppm',basis='characteristic',riemann='hllc',cfl=.3,
                final_time=None,epsilon=1e-6):
    if method not in METHODS or basis not in ('component','characteristic') or problem.equation.name!='euler':
        raise ValueError('Require an Euler problem and a supported reconstruction/basis')
    if not np.isfinite(cfl) or not 0<cfl<=.5:raise ValueError('Require 0<CFL<=0.5')
    x=problem.grid(n);dx=(problem.domain[1]-problem.domain[0])/n
    fv=method in ('muscl','ppm');q=averaged_state(problem,x,dx) if fv else problem.initial(x)
    end=problem.final_time if final_time is None else final_time
    if not np.isfinite(end) or end<0:raise ValueError('Require finite nonnegative final time')
    eq=problem.equation;scaled=0
    def rhs(v):
        nonlocal scaled
        if fv:
            left,right,count=finite_volume_edges(v,problem,method,basis);scaled+=count
            flux=ausm_flux(right[:-1],left[1:],eq.gamma) if riemann=='ausm' else numerical_flux(right[:-1],left[1:],eq,riemann)
        else:flux=weno_flux(v,problem,'z' if method=='weno-z' else 'js',basis,epsilon)
        return -(flux[1:]-flux[:-1])/dx
    time,steps,rejected=0.,0,0
    while time<end:
        sm,sp=eq.speeds(q);dt=min(cfl*dx/np.max(np.maximum(abs(sm),abs(sp))),end-time)
        for retry in range(13):
            try:
                a=q+dt*rhs(q);eq.primitive(a)
                b=.75*q+.25*(a+dt*rhs(a));eq.primitive(b)
                new=q/3+2/3*(b+dt*rhs(b));eq.primitive(new)
                break
            except ValueError:
                if retry==12:raise
                rejected+=1;dt*=.5
        q=new;time+=dt;steps+=1
    return HighOrderResult(x,q,time,steps,rejected,scaled,'cell averages' if fv else 'point values')
