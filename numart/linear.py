"""Diffusion, elliptic problems and structured linear algebra.

Crank–Nicolson (1947); Thomas elimination has no pivoting and requires suitable
diagonal pivots (e.g. the strictly diagonally dominant diffusion matrices here).
"""
import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class Boundary:
    """alpha*u + beta*du/dn = value, outward normal on either end."""
    alpha: float
    beta: float
    value: float

    @classmethod
    def dirichlet(cls,value):
        return cls(1.,0.,value)

    @classmethod
    def neumann(cls,value):
        return cls(0.,1.,value)


def poisson_boundary_1d(n,forcing,left,right,mean=0.):
    """-u''=f on [0,1], n interior nodes plus two boundary nodes.

    Robin/Neumann use ghost-point elimination and half-weight endpoint rows.
    Pure Neumann enforces discrete compatibility and fixes trapezoidal mean.
    Dirichlet is beta=0. beta<0 and alpha<0 combinations are not restricted,
    so ill-posed or singular Robin problems may fail Thomas elimination.
    """
    if n<2 or any(b.alpha==0 and b.beta==0 for b in (left,right)):
        raise ValueError("Require n>=2 and nonzero boundary coefficient pair")
    x=np.linspace(0,1,n+2)
    h=1/(n+1)
    f=np.asarray(forcing(x) if callable(forcing) else forcing,dtype=float)
    if f.ndim==0:
        f=np.full(n+2,float(f))
    if f.shape!=(n+2,):
        raise ValueError("forcing must be scalar, callable, or length n+2")
    lower,upper=-np.ones(n+1),-np.ones(n+1)
    d=2*np.ones(n+2)
    rhs=h*h*f
    for i,b in ((0,left),(-1,right)):
        if b.beta==0:
            d[i]=1.
            rhs[i]=b.value/b.alpha
            if i==0:
                upper[0]=0.
            else:
                lower[-1]=0.
        else:
            d[i]=1+h*b.alpha/b.beta
            rhs[i]=.5*h*h*f[i]+h*b.value/b.beta
    pure_neumann=left.alpha==0 and right.alpha==0
    if pure_neumann:
        scale=max(1.,float(abs(rhs).sum()))
        if abs(rhs.sum())>1e-11*scale:
            raise ValueError("Incompatible Neumann data: integral f = -sum(outward derivatives)")
        d[0],upper[0],rhs[0]=1.,0.,0.
    q=thomas(lower,d,upper,rhs)
    if pure_neumann:
        discrete_mean=h*(q.sum()-.5*(q[0]+q[-1]))
        q+=mean-discrete_mean
    return x,q


def iteration_matrix(a,method="jacobi",omega=1.):
    """Stationary iteration e[k+1]=T*e[k]; small dense educational matrices."""
    a=np.asarray(a,dtype=float)
    d=np.diag(np.diag(a))
    l,u=np.tril(a,-1),np.triu(a,1)
    if method=="jacobi":
        return np.eye(len(a))-omega*np.linalg.solve(d,a)
    if method=="gauss-seidel":
        return -np.linalg.solve(d+l,u)
    if method=="sor":
        return np.linalg.solve(d+omega*l,(1-omega)*d-omega*u)
    raise ValueError("Choose jacobi, gauss-seidel, or sor")


def spectral_radius(a):
    return float(abs(np.linalg.eigvals(a)).max())


def thomas(lower, diagonal, upper, rhs):
    """Solve tridiagonal Ax=b in O(n), without modifying inputs, no pivoting.

    lower/upper have length n-1; diagonal/rhs have length n.
    Singular or numerically tiny pivots raise rather than silently divide by zero.
    """
    d = np.array(diagonal,dtype=float,copy=True)
    b = np.array(rhs,dtype=float,copy=True)
    l,u = np.asarray(lower,dtype=float),np.asarray(upper,dtype=float)
    n = len(d)
    if n < 1 or d.shape != (n,) or b.shape != (n,) or l.shape != (n-1,) or u.shape != (n-1,):
        raise ValueError("Require diagonal/rhs length n>=1, lower/upper length n-1")
    if not all(np.all(np.isfinite(a)) for a in (d,b,l,u)):
        raise ValueError("Inputs must be finite")
    threshold = np.finfo(float).eps*max(float(abs(d).max()),float(abs(l).max(initial=0)),float(abs(u).max(initial=0)))
    for i in range(1,n):
        if abs(d[i-1]) <= threshold:
            raise np.linalg.LinAlgError("Thomas algorithm encountered a small pivot")
        factor = l[i-1]/d[i-1]
        d[i] -= factor*u[i-1]
        b[i] -= factor*b[i-1]
    if abs(d[-1]) <= threshold:
        raise np.linalg.LinAlgError("Thomas algorithm encountered a small pivot")
    x = np.empty(n)
    x[-1] = b[-1]/d[-1]
    for i in range(n-2,-1,-1):
        x[i] = (b[i]-u[i]*x[i+1])/d[i]
    return x


def diffusion_1d(n=63, final_time=.1, diffusivity=1., dt=None, method="crank-nicolson"):
    """u_t=nu*u_xx, [0,1], zero Dirichlet, u0=sin(pi*x); interior unknowns.

    Returns x,u, metadata. FTCS requires nu*dt/dx² <= 1/2.
    """
    theta = {"ftcs":0.,"backward-euler":1.,"crank-nicolson":.5}
    if method not in theta or n < 2 or final_time <= 0 or diffusivity <= 0:
        raise ValueError("Require a supported method, n>=2, t>0, nu>0")
    h=1/(n+1)
    x=np.arange(1,n+1)*h
    q=np.sin(np.pi*x)
    dt=.4*h*h/diffusivity if dt is None else dt
    if dt <= 0:
        raise ValueError("dt must be positive")
    steps=int(np.ceil(final_time/dt))
    dt=final_time/steps
    r=diffusivity*dt/(h*h)
    if method == "ftcs" and r > .5+1e-14:
        raise ValueError("FTCS diffusion is unstable for nu*dt/dx²>1/2")
    t=theta[method]
    for _ in range(steps):
        padded=np.pad(q,1)
        rhs=q+(1-t)*r*(padded[:-2]-2*q+padded[2:])
        q=rhs if t == 0 else thomas(np.full(n-1,-t*r),np.full(n,1+2*t*r),np.full(n-1,-t*r),rhs)
    return x,q,{"dt":dt,"diffusion_number":r,"steps":steps,"time":final_time}


def poisson_1d(n=63):
    """-u_xx=pi² sin(pi*x), u(0)=u(1)=0; second order + Thomas."""
    if n < 2:
        raise ValueError("n>=2 required")
    h=1/(n+1)
    x=np.arange(1,n+1)*h
    q=thomas(-np.ones(n-1),2*np.ones(n),-np.ones(n-1),h*h*np.pi**2*np.sin(np.pi*x))
    return x,q


def poisson_2d(n=31, tolerance=1.e-10, max_iterations=10000, forcing=None):
    """-Laplacian u=f on unit square, zero Dirichlet, five points + matrix-free CG.

    Default f=2*pi²*sin(pi*x)*sin(pi*y). Optional forcing is an (n,n) array.
    Returns mesh x,y,solution,residual 2-norm history. Requires SPD operator.
    """
    if n < 2 or tolerance <= 0:
        raise ValueError("n>=2 and positive tolerance required")
    h=1/(n+1)
    x,y=np.meshgrid(np.arange(1,n+1)*h,np.arange(1,n+1)*h,indexing="ij")
    f=2*np.pi**2*np.sin(np.pi*x)*np.sin(np.pi*y) if forcing is None else np.asarray(forcing,dtype=float)
    if f.shape != (n,n) or not np.all(np.isfinite(f)):
        raise ValueError("forcing must be finite and shape (n,n)")
    def apply(v):
        a=np.pad(v,1)
        return (4*v-a[:-2,1:-1]-a[2:,1:-1]-a[1:-1,:-2]-a[1:-1,2:])/(h*h)
    q=np.zeros_like(f,dtype=float)
    r=f.copy()
    p=r.copy()
    rr=float(np.sum(r*r))
    history=[np.sqrt(rr)]
    target=tolerance*max(1.,history[0])
    if history[0]<=target:
        return x,y,q,np.asarray(history)
    for _ in range(max_iterations):
        ap=apply(p)
        alpha=rr/np.sum(p*ap)
        q+=alpha*p
        r-=alpha*ap
        newrr=float(np.sum(r*r))
        history.append(np.sqrt(newrr))
        if history[-1]<=target:
            return x,y,q,np.asarray(history)
        p=r+(newrr/rr)*p
        rr=newrr
    raise RuntimeError("CG did not reach the residual tolerance")


def spectral_diffusion(q, final_time, diffusivity=1., length=1.):
    """Periodic heat equation, exact integration of the truncated Fourier modes."""
    if final_time < 0 or diffusivity <= 0 or length <= 0:
        raise ValueError("Require t>=0, diffusivity>0, length>0")
    k=2*np.pi*np.fft.fftfreq(len(q),d=length/len(q))
    return np.fft.ifft(np.fft.fft(q)*np.exp(-diffusivity*k*k*final_time)).real
