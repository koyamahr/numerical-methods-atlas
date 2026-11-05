"""Geometric multigrid for -Laplacian u=f, square grid, zero Dirichlet.

Full weighting, bilinear prolongation, rediscretized five-point coarse operator,
red-black Gauss–Seidel pre/post smoothing, exact solve on a one-unknown grid.
References: Fedorenko (1961), Brandt (1977). Not algebraic multigrid.
"""
import numpy as np


def laplacian_operator(q,h):
    a=np.pad(q,1)
    return (4*q-a[:-2,1:-1]-a[2:,1:-1]-a[1:-1,:-2]-a[1:-1,2:])/(h*h)


def red_black_gauss_seidel(q,f,h,sweeps=1,omega=1.):
    """Return updated copy; omega=1 is GS, 0<omega<2 gives RB-SOR."""
    if q.shape != f.shape or not 0 < omega < 2 or h <= 0 or sweeps < 0:
        raise ValueError("Matching grids, h>0, sweeps>=0, 0<omega<2 required")
    q=np.array(q,dtype=float,copy=True)
    parity=np.indices(q.shape).sum(axis=0)%2
    for _ in range(sweeps):
        for color in (0,1):
            a=np.pad(q,1)
            relaxed=.25*(h*h*f+a[:-2,1:-1]+a[2:,1:-1]+a[1:-1,:-2]+a[1:-1,2:])
            mask=parity==color
            q[mask]+=omega*(relaxed[mask]-q[mask])
    return q


def restrict_full_weighting(r):
    a=np.pad(r,1)
    return (4*a[2:-1:2,2:-1:2]
            +2*(a[1:-2:2,2:-1:2]+a[3::2,2:-1:2]+a[2:-1:2,1:-2:2]+a[2:-1:2,3::2])
            +a[1:-2:2,1:-2:2]+a[1:-2:2,3::2]+a[3::2,1:-2:2]+a[3::2,3::2])/16


def prolong_bilinear(e):
    n=2*e.shape[0]+1
    p=np.zeros((n+2,n+2))
    p[::2,::2]=np.pad(e,1)
    p[1::2,::2]=.5*(p[:-2:2,::2]+p[2::2,::2])
    p[:,1::2]=.5*(p[:,:-2:2]+p[:,2::2])
    return p[1:-1,1:-1]


def v_cycle(q,f,h,pre=3,post=3):
    if q.shape == (1,1):
        return f*h*h/4
    q=red_black_gauss_seidel(q,f,h,pre)
    r=f-laplacian_operator(q,h)
    fc=restrict_full_weighting(r)
    correction=v_cycle(np.zeros_like(fc),fc,2*h,pre,post)
    q+=prolong_bilinear(correction)
    return red_black_gauss_seidel(q,f,h,post)


def solve_poisson_multigrid(f,tolerance=1e-10,max_cycles=100):
    f=np.asarray(f,dtype=float)
    if f.ndim!=2 or f.shape[0]!=f.shape[1] or f.shape[0]<1:
        raise ValueError("A square interior grid is required")
    n=f.shape[0]
    if (n+1)&n or tolerance<=0 or not np.all(np.isfinite(f)):
        raise ValueError("Require n=2^k-1, finite forcing and positive tolerance")
    h=1/(n+1)
    q=np.zeros_like(f)
    history=[float(np.linalg.norm(f))]
    target=tolerance*max(1.,history[0])
    if history[0]<=target:
        return q,np.asarray(history)
    for _ in range(max_cycles):
        q=v_cycle(q,f,h)
        history.append(float(np.linalg.norm(f-laplacian_operator(q,h))))
        if history[-1]<=target:
            return q,np.asarray(history)
    raise RuntimeError("V-cycles did not reach the residual tolerance")
