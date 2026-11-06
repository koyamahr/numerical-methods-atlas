"""Matched constant-coefficient Dirichlet Poisson experiments.

All 2D paths solve the same five-point SPD system. FFT means orthonormal
DST-I via an odd extension, not periodic boundary conditions. DST+Thomas
separates one direction and solves n tridiagonal systems in the other.
Legacy kernels are unchanged to preserve published artifact provenance.
"""
from dataclasses import dataclass
from time import perf_counter
import numpy as np
from .linear import thomas
from .multigrid import laplacian_operator,red_black_gauss_seidel,v_cycle

METHODS=('jacobi','weighted-jacobi','rbgs','sor','cg','multigrid','dst-thomas','fft-dst')


def dst1(a,axis=0):
    """Orthonormal DST-I, its own inverse; implemented using NumPy FFT."""
    a=np.asarray(a,dtype=float)
    if a.ndim<1 or not -a.ndim<=axis<a.ndim or not np.all(np.isfinite(a)):raise ValueError('Finite array and valid axis required')
    a=np.moveaxis(a,axis,0);n=len(a)
    if n<1:raise ValueError('Empty transform')
    extended=np.zeros((2*(n+1),)+a.shape[1:]);extended[1:n+1]=a;extended[n+2:]=-a[::-1]
    result=-np.fft.fft(extended,axis=0).imag[1:n+1]/np.sqrt(2*(n+1))
    return np.moveaxis(result,0,axis)


def eigenvalues(n):
    return 4*(n+1)**2*np.sin(np.pi*np.arange(1,n+1)/(2*(n+1)))**2


def direct_1d(f,method='thomas'):
    f=np.asarray(f,dtype=float);n=len(f)
    if f.ndim!=1 or n<2 or not np.all(np.isfinite(f)):raise ValueError('Finite 1D forcing, n>=2 required')
    if method=='thomas':return thomas(-np.ones(n-1),2*np.ones(n),-np.ones(n-1),f/(n+1)**2)
    if method=='fft-dst':return dst1(dst1(f)/eigenvalues(n))
    raise ValueError('Choose thomas or fft-dst')


def direct_2d(f,method='fft-dst'):
    f=np.asarray(f,dtype=float)
    if f.ndim!=2 or f.shape[0]!=f.shape[1] or len(f)<2 or not np.all(np.isfinite(f)):raise ValueError('Finite square forcing required')
    n=len(f);lam=eigenvalues(n);h=1/(n+1)
    if method=='fft-dst':return dst1(dst1(dst1(dst1(f,0),1)/(lam[:,None]+lam[None,:]),0),1)
    if method=='dst-thomas':
        transformed=dst1(f,1);solution=np.empty_like(f)
        for j in range(n):solution[:,j]=thomas(-np.ones(n-1),np.full(n,2+h*h*lam[j]),-np.ones(n-1),h*h*transformed[:,j])
        return dst1(solution,1)
    raise ValueError('Choose fft-dst or dst-thomas')


def problem(n=63,case='manufactured'):
    if not isinstance(n,int) or n<3:raise ValueError('n>=3 required')
    x=(np.arange(n)+1)/(n+1);xx,yy=np.meshgrid(x,x,indexing='ij')
    if case=='manufactured':
        def g(x,a):return x*(1-x)*np.exp(a*x)
        def ddg(x,a):return (a*a*x*(1-x)+2*a*(1-2*x)-2)*np.exp(a*x)
        exact=g(xx,2)*g(yy,-1.5);f=-ddg(xx,2)*g(yy,-1.5)-g(xx,2)*ddg(yy,-1.5)
    elif case=='localized':
        f=100*np.exp(-((xx-.28)**2+(yy-.35)**2)/.006)-60*np.exp(-((xx-.7)**2+(yy-.65)**2)/.012);exact=None
    elif case=='single-mode':
        exact=np.sin(np.pi*xx)*np.sin(np.pi*yy);f=2*np.pi**2*exact
    else:raise ValueError('Unknown Poisson problem')
    return x,f,exact


@dataclass
class PoissonRun:
    q: np.ndarray
    history: np.ndarray # completed units, elapsed seconds, recomputed relative residual
    steps: int
    seconds: float
    converged: bool
    omega: float


def solve(f,method='cg',tolerance=1e-8,max_steps=200000):
    start=perf_counter();f=np.asarray(f,dtype=float)
    if f.ndim!=2 or f.shape[0]!=f.shape[1] or len(f)<3 or not np.all(np.isfinite(f)):raise ValueError('Finite square forcing required')
    if method not in METHODS or not np.isfinite(tolerance) or not 0<tolerance<1 or not isinstance(max_steps,int) or max_steps<1:raise ValueError('Invalid solver controls')
    n=len(f);h=1/(n+1)
    if method=='multigrid' and (n+1)&n:raise ValueError('Multigrid needs n=2^k-1')
    norm=float(np.sqrt(np.sum(f*f)));scale=norm if norm else 1.;q=np.zeros_like(f)
    omega=2/(1+np.sin(np.pi/(n+1))) if method=='sor' else 2/3 if method=='weighted-jacobi' else 1.
    history=[[0,perf_counter()-start,1. if norm else 0.]]
    if norm==0:return PoissonRun(q,np.asarray(history),0,perf_counter()-start,True,omega)
    if method in ('fft-dst','dst-thomas'):
        q=direct_2d(f,method);relative=float(np.sqrt(np.sum((f-laplacian_operator(q,h))**2))/scale)
        history.append([1,perf_counter()-start,relative])
        return PoissonRun(q,np.asarray(history),1,perf_counter()-start,relative<=tolerance,omega)
    if method=='cg':r=f.copy();p=r.copy();rr=float(np.sum(r*r))
    for step in range(1,max_steps+1):
        if method in ('jacobi','weighted-jacobi'):
            a=np.pad(q,1);candidate=.25*(h*h*f+a[:-2,1:-1]+a[2:,1:-1]+a[1:-1,:-2]+a[1:-1,2:])
            q+=omega*(candidate-q)
        elif method in ('rbgs','sor'):q=red_black_gauss_seidel(q,f,h,1,omega)
        elif method=='multigrid':q=v_cycle(q,f,h)
        else:
            ap=laplacian_operator(p,h);denominator=float(np.sum(p*ap))
            if denominator<=0 or not np.isfinite(denominator):raise RuntimeError('CG lost SPD curvature')
            alpha=rr/denominator;q+=alpha*p;r-=alpha*ap;next_rr=float(np.sum(r*r))
        actual=f-laplacian_operator(q,h);relative=float(np.sqrt(np.sum(actual*actual))/scale)
        history.append([step,perf_counter()-start,relative])
        if relative<=tolerance:return PoissonRun(q,np.asarray(history),step,perf_counter()-start,True,omega)
        if method=='cg':
            # Recurrence residual only chooses directions. The stopping rule
            # always uses the explicitly recomputed true residual above.
            if next_rr<np.finfo(float).tiny:r=actual.copy();p=r.copy();rr=float(np.sum(r*r))
            else:p=r+(next_rr/rr)*p;rr=next_rr
    return PoissonRun(q,np.asarray(history),max_steps,perf_counter()-start,False,omega)
