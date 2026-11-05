"""Small force laboratories with explicitly different boundary conditions.

3D periodic PM: CIC assignment/interpolation, mean-subtracted spectral Poisson.
Isolated 3D tree: softened Newton kernel, monopole or full second-moment term.
No P3M, TreePM split, FMM translations, cosmological expansion, or time stepping.
"""
from dataclasses import dataclass
from itertools import product
import numpy as np


def _particles(positions,masses):
    x,m=np.asarray(positions,dtype=float),np.asarray(masses,dtype=float)
    if x.ndim!=2 or x.shape[1]!=3 or m.shape!=(len(x),) or len(x)==0:
        raise ValueError('Require nonempty positions (N,3) and masses (N,)')
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(m)) or np.any(m<=0):
        raise ValueError('Require finite positions and positive finite masses')
    return x,m


def cic_deposit(positions,masses,n=16,length=1.):
    """Mass density on periodic mesh nodes at coordinates i*L/n."""
    x,m=_particles(positions,masses)
    if not isinstance(n,int) or n<4 or not np.isfinite(length) or length<=0:raise ValueError('Invalid mesh')
    coordinate=(x%length)*n/length;lower=np.floor(coordinate).astype(int);fraction=coordinate-lower
    rho=np.zeros((n,n,n))
    for bits in product((0,1),repeat=3):
        offset=np.array(bits);index=(lower+offset)%n
        weight=np.prod(np.where(offset,fraction,1-fraction),axis=1)
        np.add.at(rho,tuple(index.T),m*weight/(length/n)**3)
    return rho


def cic_interpolate(field,positions,length=1.):
    field=np.asarray(field,dtype=float);x=np.asarray(positions,dtype=float)
    if field.ndim!=4 or field.shape[0]!=3 or len(set(field.shape[1:]))!=1:
        raise ValueError('Require vector mesh (3,n,n,n)')
    if x.ndim!=2 or x.shape[1]!=3 or not np.all(np.isfinite(x)) or not np.all(np.isfinite(field)) or not np.isfinite(length) or length<=0:
        raise ValueError('Require finite field, (N,3) positions and positive length')
    n=field.shape[1];coordinate=(x%length)*n/length
    lower=np.floor(coordinate).astype(int);fraction=coordinate-lower;result=np.zeros_like(x)
    for bits in product((0,1),repeat=3):
        offset=np.array(bits);index=(lower+offset)%n
        weight=np.prod(np.where(offset,fraction,1-fraction),axis=1)
        result+=field[(slice(None),)+tuple(index.T)].T*weight[:,None]
    return result


def periodic_poisson(rho,length=1.,gravity=1.):
    """Solve Laplacian(phi)=4*pi*G*(rho-mean), continuum Fourier symbol.

    phi_hat[0]=0 fixes the gauge. Spectral force derivatives zero the unpaired
    even-grid Nyquist mode along their own axis to keep a real odd operator.
    """
    rho=np.asarray(rho,dtype=float)
    if rho.ndim!=3 or len(set(rho.shape))!=1 or rho.shape[0]<4 or not np.all(np.isfinite(rho)):
        raise ValueError('Require finite cubic density mesh')
    if not np.isfinite(length) or length<=0 or not np.isfinite(gravity) or gravity<=0:raise ValueError('Invalid units')
    n=rho.shape[0];k=2*np.pi*np.fft.fftfreq(n,d=length/n)
    wave=np.meshgrid(k,k,k,indexing='ij');k2=sum(v*v for v in wave)
    inverse=np.zeros_like(k2);np.divide(1.,k2,out=inverse,where=k2>0)
    phihat=-4*np.pi*gravity*np.fft.fftn(rho-rho.mean())*inverse;phihat[0,0,0]=0
    potential=np.fft.ifftn(phihat).real;acceleration=[]
    for axis,v in enumerate(wave):
        derivative=v.copy()
        if n%2==0:
            selection=[slice(None)]*3;selection[axis]=n//2;derivative[tuple(selection)]=0
        acceleration.append(np.fft.ifftn(-1j*derivative*phihat).real)
    return potential,np.asarray(acceleration)


def pm_acceleration(positions,masses,n=16,length=1.):
    rho=cic_deposit(positions,masses,n,length)
    potential,field=periodic_poisson(rho,length)
    return cic_interpolate(field,positions,length),rho,potential


def direct_acceleration(positions,masses,softening=.03):
    x,m=_particles(positions,masses)
    if not np.isfinite(softening) or softening<=0:raise ValueError('Require positive finite softening')
    displacement=x[:,None,:]-x[None,:,:]
    r2=np.sum(displacement**2,axis=-1)+softening**2
    np.fill_diagonal(r2,np.inf)
    return -np.sum(m[None,:,None]*displacement/r2[...,None]**1.5,axis=1)


@dataclass
class _Node:
    indices: np.ndarray
    center: np.ndarray
    half: float
    mass: float
    com: np.ndarray
    second: np.ndarray
    children: list


def _build(x,m,indices,center,half,depth=0):
    mass=float(m[indices].sum());com=np.sum(x[indices]*m[indices,None],axis=0)/mass
    delta=x[indices]-com;second=np.einsum('n,ni,nj->ij',m[indices],delta,delta)
    children=[]
    if len(indices)>1 and depth<32 and half>1e-14:
        codes=np.sum((x[indices]>=center)*np.array([1,2,4]),axis=1)
        for code in range(8):
            subset=indices[codes==code]
            if len(subset):
                direction=np.array([1 if code&(1<<a) else -1 for a in range(3)])
                children.append(_build(x,m,subset,center+direction*half/2,half/2,depth+1))
    return _Node(indices,center,half,mass,com,second,children)


def tree_acceleration(positions,masses,theta=.6,order=0,softening=.03):
    """Barnes–Hut octree, isolated Plummer-softened kernel, G=1.

    order=0 is monopole; order=2 adds the full second-moment Taylor term of the
    same softened kernel. Nodes containing the target are always opened.
    Interaction counts are work diagnostics, not wall-clock timings.
    """
    x,m=_particles(positions,masses)
    if not np.isfinite(theta) or theta<0 or order not in (0,2) or not np.isfinite(softening) or softening<=0:
        raise ValueError('Require theta>=0, order 0 or 2 and positive softening')
    center=(x.min(axis=0)+x.max(axis=0))/2
    half=max(float(np.ptp(x,axis=0).max())/2,1e-10)*(1+1e-12)
    root=_build(x,m,np.arange(len(x)),center,half)
    result=np.zeros_like(x);counts={'accepted_nodes':0,'direct_pairs':0}
    for i,target in enumerate(x):
        stack=[root]
        while stack:
            node=stack.pop();r=target-node.com;distance=float(np.linalg.norm(r))
            contains=np.all(abs(target-node.center)<=node.half*(1+1e-12))
            if node.children and not contains and distance>0 and 2*node.half/distance<theta:
                s2=float(r@r+softening**2);s=np.sqrt(s2)
                force=-node.mass*r/s**3
                if order==2:
                    sr=node.second@r;a=float(r@sr);trace=float(np.trace(node.second))
                    force+=3*sr/s**5-7.5*a*r/s**7+1.5*trace*r/s**5
                result[i]+=force;counts['accepted_nodes']+=1
            elif node.children:stack.extend(node.children)
            else:
                indices=node.indices[node.indices!=i]
                delta=target-x[indices];r2=np.sum(delta**2,axis=1)+softening**2
                result[i]-=np.sum(m[indices,None]*delta/r2[:,None]**1.5,axis=0)
                counts['direct_pairs']+=len(indices)
    return result,counts
