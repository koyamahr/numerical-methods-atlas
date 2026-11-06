"""Ideal-gas 1D Euler Roe matrix via quadratic parameter vectors.

Roe 1981 Property U: linear mapping for a fixed state pair; coincident-state
Jacobian limit; exact flux-jump mapping; independent eigenvectors. Entropy
smoothing belongs to the flux, not to these matrix properties.
"""
import numpy as np
from .equations import Euler
from .reconstruction import euler_eigenbasis


def parameter(q,gamma=1.4):
    w=Euler(gamma).primitive(q);root=np.sqrt(w[...,0]);h=(q[...,2]+w[...,2])/w[...,0]
    return np.stack((root,root*w[...,1],root*h),axis=-1)


def parameter_maps(z,gamma=1.4):
    z=np.asarray(z);a,b,c=np.moveaxis(z,-1,0)
    q=np.stack((a*a,a*b,(a*c+.5*(gamma-1)*b*b)/gamma),axis=-1)
    f=np.stack((a*b,((gamma+1)*b*b/2+(gamma-1)*a*c)/gamma,b*c),axis=-1)
    return q,f


def roe_matrix(left,right,gamma=1.4):
    z=.5*(parameter(left,gamma)+parameter(right,gamma));a,b,c=np.moveaxis(z,-1,0)
    shape=z.shape[:-1]+(3,3);du=np.zeros(shape);df=np.zeros(shape)
    du[...,0,0]=2*a;du[...,1,0]=b;du[...,1,1]=a
    du[...,2,0]=c/gamma;du[...,2,1]=(gamma-1)*b/gamma;du[...,2,2]=a/gamma
    df[...,0,0]=b;df[...,0,1]=a
    df[...,1,0]=(gamma-1)*c/gamma;df[...,1,1]=(gamma+1)*b/gamma;df[...,1,2]=(gamma-1)*a/gamma
    df[...,2,1]=c;df[...,2,2]=b
    return np.linalg.solve(np.swapaxes(du,-1,-2),np.swapaxes(df,-1,-2)).swapaxes(-1,-2)


def flux_jacobian(q,gamma=1.4):
    w=Euler(gamma).primitive(q);u=w[...,1];h=(q[...,2]+w[...,2])/w[...,0]
    a=np.zeros(q.shape[:-1]+(3,3));a[...,0,1]=1
    a[...,1,0]=.5*(gamma-3)*u*u;a[...,1,1]=(3-gamma)*u;a[...,1,2]=gamma-1
    a[...,2,0]=u*(.5*(gamma-1)*u*u-h);a[...,2,1]=h-(gamma-1)*u*u;a[...,2,2]=gamma*u
    return a


def eigensystem(left,right,gamma=1.4):
    r,l=euler_eigenbasis(left,right,gamma)
    z=parameter(left,gamma)+parameter(right,gamma);u=z[...,1]/z[...,0];h=z[...,2]/z[...,0]
    a=np.sqrt((gamma-1)*(h-.5*u*u));values=np.stack((u-a,u,u+a),axis=-1)
    return values,r,l


def normal_shock(mach=2.,speed=0.,reverse=False,gamma=1.4):
    if mach<=1:raise ValueError('Require supersonic Mach')
    ratio=(gamma+1)*mach**2/(2+(gamma-1)*mach**2)
    pressure=1+2*gamma/(gamma+1)*(mach**2-1)
    left=np.array([1.,mach+speed,1/gamma]);right=np.array([ratio,mach/ratio+speed,pressure/gamma])
    eq=Euler(gamma)
    return (eq.conserved(right),eq.conserved(left)) if reverse else (eq.conserved(left),eq.conserved(right))
